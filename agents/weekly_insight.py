#!/usr/bin/env python3
"""
Weekly Insight Agent - Nudge Engage v2

Pulls from 3 sources and produces a 3-2-1 weekly report:
  1. Retention metrics (data/nudge.db)
  2. Sprint completions this week (change_log.md)
  3. Top NPS themes (freshest research/synthesis-*.md, or research/nps-analysis.md
     as a fallback if no dated weekly synthesis exists yet)

Saves the full report to reports/YYYY-MM-DD.md and prints (or posts, with
--post) a compact 3-2-1 Slack summary.

Design note: every judgment call below is rule-based (recency for "Done",
magnitude of movement for "Changed", a keyword scan for open blockers to pick
"Watch") rather than requiring a separate LLM API call. That keeps the whole
pipeline runnable with no extra external dependency beyond the Slack webhook
for delivery - see agents/weekly-insight.md Section on real-world wiring for
where an LLM synthesis step could replace this if the rules stop being good
enough as the workspace grows.

Usage:
    python weekly_insight.py                # dry run, prints + saves report
    python weekly_insight.py --post          # also posts the 3-2-1 to Slack
    python weekly_insight.py --days 7        # override the lookback window
"""

import argparse
import datetime
import json
import os
import re
import sqlite3
import sys
import urllib.request

ROOT = os.path.join(os.path.dirname(__file__), "..")
DEFAULT_DB = os.path.join(ROOT, "data", "nudge.db")
CHANGE_LOG = os.path.join(ROOT, "change_log.md")
RESEARCH_DIR = os.path.join(ROOT, "research")
REPORTS_DIR = os.path.join(ROOT, "reports")

BLOCKER_KEYWORDS = ["tbd", "blocker", "estimate", "pending", "waiting on", "not yet applied"]

UNICODE_REPLACEMENTS = {
    "→": "->", "←": "<-", "↑": "up", "↓": "down",
    "—": "-", "–": "-", "‘": "'", "’": "'",
    "“": '"', "”": '"', "…": "...",
}


def ascii_safe(text):
    """Source text (change_log titles, NPS theme names) can contain characters
    that crash print() on a default Windows console (cp1252). Normalize known
    ones, then drop anything else that still doesn't fit rather than crashing."""
    for char, replacement in UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    return text.encode("ascii", "replace").decode("ascii")


# ---------- Source 1: retention metrics ----------

def get_connection(db_path):
    if not os.path.exists(db_path):
        return None
    return sqlite3.connect(db_path)


def retention_rate(conn, cohort_week, channel=None):
    query = """
        SELECT COUNT(*), SUM(r.day_30)
        FROM nudge_retention r
        JOIN nudge_users u ON u.user_id = r.user_id
        WHERE u.cohort_week = ?
    """
    params = [cohort_week]
    if channel:
        query += " AND u.acquisition_channel = ?"
        params.append(channel)
    total, retained = conn.execute(query, params).fetchone()
    return (retained or 0) / total * 100 if total else None


def notification_open_rate(conn, cohort_week):
    total, opened = conn.execute(
        """
        SELECT COUNT(*), SUM(n.opened)
        FROM nudge_nudges n JOIN nudge_users u ON u.user_id = n.user_id
        WHERE u.cohort_week = ?
        """,
        (cohort_week,),
    ).fetchone()
    return (opened or 0) / total * 100 if total else None


def gather_retention_signals(conn):
    """Returns a list of {label, current, change} dicts, one per candidate
    'changed this week' signal, sorted by nothing yet (caller ranks by magnitude)."""
    if conn is None:
        return []

    weeks = [
        row[0]
        for row in conn.execute(
            "SELECT DISTINCT cohort_week FROM nudge_users ORDER BY cohort_week DESC LIMIT 2"
        ).fetchall()
    ]
    if len(weeks) < 2:
        return []
    current_week, baseline_week = weeks

    signals = []

    overall_cur = retention_rate(conn, current_week)
    overall_base = retention_rate(conn, baseline_week)
    if overall_cur is not None and overall_base is not None:
        signals.append({
            "label": "Overall 30-day retention",
            "current": overall_cur,
            "change": overall_cur - overall_base,
            "unit": "%",
        })

    for ch in ["organic", "paid", "referral"]:
        cur = retention_rate(conn, current_week, ch)
        base = retention_rate(conn, baseline_week, ch)
        if cur is not None and base is not None:
            signals.append({
                "label": f"{ch.capitalize()} channel retention",
                "current": cur,
                "change": cur - base,
                "unit": "%",
            })

    notif_cur = notification_open_rate(conn, current_week)
    notif_base = notification_open_rate(conn, baseline_week)
    if notif_cur is not None and notif_base is not None:
        signals.append({
            "label": "Push notification open rate",
            "current": notif_cur,
            "change": notif_cur - notif_base,
            "unit": "%",
        })

    return signals


# ---------- Source 2: change_log.md ----------

def gather_change_log_entries(days):
    if not os.path.exists(CHANGE_LOG):
        return []

    with open(CHANGE_LOG, encoding="utf-8") as f:
        text = f.read()

    entries = re.findall(r"^## (\d{4}-\d{2}-\d{2}) \W+ (.+)$", text, flags=re.MULTILINE)
    cutoff = datetime.date.today() - datetime.timedelta(days=days)

    recent = []
    for date_str, title in entries:
        try:
            entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        if entry_date >= cutoff:
            recent.append((entry_date, ascii_safe(title.strip())))

    recent.sort(key=lambda x: x[0], reverse=True)
    return recent


def scan_for_open_blockers(entries_with_body, days):
    """Look for the most recent change_log entry whose body mentions an
    unresolved item, using the full text (not just titles) within the window.
    Scans most-recent-first so a fresh, specific blocker outranks an old,
    incidental keyword hit (e.g. the word 'blocker' appearing inside an
    unrelated skill description)."""
    if not os.path.exists(CHANGE_LOG):
        return None

    with open(CHANGE_LOG, encoding="utf-8") as f:
        text = f.read()

    blocks = re.split(r"^## ", text, flags=re.MULTILINE)[1:]
    cutoff = datetime.date.today() - datetime.timedelta(days=days)

    dated_blocks = []
    for block in blocks:
        header, _, body = block.partition("\n")
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", header.strip())
        if not date_match:
            continue
        try:
            entry_date = datetime.datetime.strptime(date_match.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        if entry_date >= cutoff:
            dated_blocks.append((entry_date, body))

    dated_blocks.sort(key=lambda x: x[0], reverse=True)  # most recent first

    for _, body in dated_blocks:
        lower_body = body.lower()
        for kw in BLOCKER_KEYWORDS:
            if kw in lower_body:
                sentences = re.split(r"(?<=[.!?])\s+", body.replace("\n", " "))
                for s in sentences:
                    if kw in s.lower():
                        return ascii_safe(truncate_clause(s.strip(), kw))
    return None


def truncate_clause(sentence, keyword, max_len=160):
    """Long compound sentences (lists with semicolons, no internal periods)
    don't split cleanly - trim from the start rather than returning the whole
    thing verbatim. Starting from the beginning reads more coherently than
    centering on the matched keyword, which often lands mid-clause."""
    if len(sentence) <= max_len:
        return sentence
    cutoff = sentence.rfind(" ", 0, max_len)  # break on a word boundary
    if cutoff == -1:
        cutoff = max_len
    return sentence[:cutoff].strip() + "..."


# ---------- Source 3: NPS themes ----------

def find_latest_nps_source():
    """Prefer the freshest dated weekly synthesis; fall back to the original
    one-time nps-analysis.md if no weekly file exists yet."""
    if os.path.isdir(RESEARCH_DIR):
        dated = sorted(
            f for f in os.listdir(RESEARCH_DIR)
            if re.match(r"synthesis-\d{4}-\d{2}-\d{2}\.md$", f)
        )
        if dated:
            return os.path.join(RESEARCH_DIR, dated[-1]), "weekly synthesis"
    fallback = os.path.join(RESEARCH_DIR, "nps-analysis.md")
    if os.path.exists(fallback):
        return fallback, "fallback (no weekly synthesis yet)"
    return None, None


def gather_nps_themes():
    path, source_kind = find_latest_nps_source()
    if not path:
        return [], None, None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Matches both "**Theme A: Name (3 mentions)**" and "### Name (3 mentions)"
    themes = re.findall(r"(?:\*\*Theme \w+: |### )(.+?) \((\d+) mentions?\)", text)
    themes = [(ascii_safe(name), count) for name, count in themes]
    return themes, path, source_kind


# ---------- Report assembly ----------

def build_done_bullets(change_log_entries, limit=3):
    return [title for _, title in change_log_entries[:limit]]


def build_changed_bullets(retention_signals, limit=2):
    ranked = sorted(retention_signals, key=lambda s: abs(s["change"]), reverse=True)
    bullets = []
    for s in ranked[:limit]:
        direction = "up" if s["change"] > 0 else "down"
        bullets.append(
            f"{s['label']} {direction} {abs(s['change']):.1f}pt{'s' if round(abs(s['change']), 1) != 1 else ''} "
            f"to {s['current']:.1f}{s['unit']}"
        )
    return bullets, ranked[limit:]


def build_watch_bullet(change_log_entries, remaining_signals, days):
    blocker = scan_for_open_blockers(change_log_entries, days)
    if blocker:
        return blocker
    if remaining_signals:
        s = remaining_signals[0]
        direction = "up" if s["change"] > 0 else "down"
        return f"{s['label']} still moving ({direction} {abs(s['change']):.1f}pts) - confirm if it's a trend."
    return "No clear standout signal this week - worth a manual scan before next Friday."


def render_report(date_str, done, changed, watch, nps_themes, nps_source, nps_source_kind):
    lines = [
        f"# Nudge Weekly Insight - {date_str}",
        "",
        "## Done this week",
    ]
    lines += [f"- {b}" for b in done] if done else ["- Nothing logged in the lookback window."]
    lines += ["", "## Changed this week"]
    lines += [f"- {b}" for b in changed] if changed else ["- No metric movement detected."]
    lines += ["", "## Watch next week", f"- {watch}"]

    if nps_themes:
        lines += ["", "## Top NPS themes referenced", f"*Source: `{os.path.relpath(nps_source, ROOT)}` ({nps_source_kind})*", ""]
        lines += [f"- {name} ({count} mentions)" for name, count in nps_themes[:3]]

    return "\n".join(lines)


def render_slack_summary(date_str, done, changed, watch):
    lines = [f":clipboard: *Nudge Weekly Insight - {date_str}*", "", "Done this week:"]
    lines += [f"- {b}" for b in done]
    lines += ["", "Changed this week:"]
    lines += [f"- {b}" for b in changed]
    lines += ["", "Watch next week:", f"- {watch}"]
    return "\n".join(lines)


def post_to_slack(message):
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        sys.exit("SLACK_WEBHOOK_URL not set - can't post. Run without --post to dry-run.")
    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(webhook, data=payload, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)


def main():
    parser = argparse.ArgumentParser(description="Weekly insight agent for Nudge Engage v2")
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--days", type=int, default=7, help="Lookback window for change_log.md entries")
    parser.add_argument("--post", action="store_true", help="Post the 3-2-1 summary to Slack")
    parser.add_argument("--date", default=None, help="Override the report date (e.g. 'Fri May 9')")
    args = parser.parse_args()

    conn = get_connection(args.db)
    retention_signals = gather_retention_signals(conn)
    change_log_entries = gather_change_log_entries(args.days)
    nps_themes, nps_source, nps_source_kind = gather_nps_themes()

    done = build_done_bullets(change_log_entries)
    changed, remaining_signals = build_changed_bullets(retention_signals)
    watch = build_watch_bullet(change_log_entries, remaining_signals, args.days)

    today = datetime.date.today()
    date_str = args.date or today.strftime("%a %b ") + str(today.day)
    file_date = today.isoformat()

    report = render_report(date_str, done, changed, watch, nps_themes, nps_source, nps_source_kind)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, f"{file_date}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report + "\n")

    slack_summary = render_slack_summary(date_str, done, changed, watch)
    print(slack_summary)
    print(f"\nSaved full report to {os.path.relpath(report_path, ROOT)}")

    if args.post:
        post_to_slack(slack_summary)
        print("Posted to Slack.")


if __name__ == "__main__":
    main()
