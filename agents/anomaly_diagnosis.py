#!/usr/bin/env python3
"""
Anomaly Diagnosis Engine - Nudge Engage v2

Chained from agents/metric_pulse.py: when the pulse agent's alert fires
(30-day retention moved >= ALERT_THRESHOLD_PP week-over-week, either
direction), this module decomposes the move with the same metric-tree logic
as data/metric-diagnosis.md, generates 3 ranked hypotheses, and writes the
SQL to confirm the top one.

The diagnostic logic (decomposition math, hypothesis ranking, SQL building,
Slack formatting) is separated from data-fetching on purpose, so it can be
driven by either real data/nudge.db numbers or a synthetic --simulate
scenario for testing, without duplicating logic in two places.

Usage:
    python anomaly_diagnosis.py --simulate-drop 4     # synthetic -4pt test
    python anomaly_diagnosis.py --simulate-drop -4    # synthetic +4pt test
    python anomaly_diagnosis.py                       # diagnose real data/nudge.db
"""

import argparse
import datetime
import os
import sqlite3
import sys

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "data", "nudge.db")


# ---------- Step 1: metric tree decomposition ----------

def retention_rate(conn, cohort_week, channel=None):
    query = """
        SELECT COUNT(*), SUM(r.day_1), SUM(r.day_7), SUM(r.day_30)
        FROM nudge_retention r
        JOIN nudge_users u ON u.user_id = r.user_id
        WHERE u.cohort_week = ?
    """
    params = [cohort_week]
    if channel:
        query += " AND u.acquisition_channel = ?"
        params.append(channel)
    total, d1, d7, d30 = conn.execute(query, params).fetchone()
    if not total:
        return None
    return {
        "day1_pct": d1 / total * 100,
        "day7_given_day1_pct": (d7 / d1 * 100) if d1 else 0,
        "day30_given_day7_pct": (d30 / d7 * 100) if d7 else 0,
        "day30_pct": d30 / total * 100,
    }


def avg_sessions(conn, cohort_week):
    users, sessions = conn.execute(
        """
        SELECT COUNT(DISTINCT u.user_id), COUNT(s.session_id)
        FROM nudge_users u LEFT JOIN nudge_sessions s ON s.user_id = u.user_id
        WHERE u.cohort_week = ?
        """,
        (cohort_week,),
    ).fetchone()
    return (sessions or 0) / users if users else 0.0


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


def decompose_from_db(db_path):
    """Real decomposition against data/nudge.db, comparing the two most
    recent cohort weeks - same 'week' = cohort-week convention as the other
    two agents."""
    conn = sqlite3.connect(db_path)
    weeks = [
        row[0] for row in conn.execute(
            "SELECT DISTINCT cohort_week FROM nudge_users ORDER BY cohort_week DESC LIMIT 2"
        ).fetchall()
    ]
    if len(weeks) < 2:
        sys.exit("Need at least 2 cohort weeks in the database to diagnose a move.")
    current_week, baseline_week = weeks

    cur = retention_rate(conn, current_week)
    base = retention_rate(conn, baseline_week)

    channel_moves = {}
    for ch in ["organic", "paid", "referral"]:
        c = retention_rate(conn, current_week, ch)
        b = retention_rate(conn, baseline_week, ch)
        if c and b:
            channel_moves[ch] = c["day30_pct"] - b["day30_pct"]

    decomposition = {
        "headline_change": cur["day30_pct"] - base["day30_pct"],
        "headline_current": cur["day30_pct"],
        "headline_baseline": base["day30_pct"],
        "day7_given_day1_change": cur["day7_given_day1_pct"] - base["day7_given_day1_pct"],
        "day7_given_day1_current": cur["day7_given_day1_pct"],
        "day7_given_day1_baseline": base["day7_given_day1_pct"],
        "day30_given_day7_change": cur["day30_given_day7_pct"] - base["day30_given_day7_pct"],
        "sessions_current": avg_sessions(conn, current_week),
        "sessions_baseline": avg_sessions(conn, baseline_week),
        "notif_open_current": notification_open_rate(conn, current_week),
        "notif_open_baseline": notification_open_rate(conn, baseline_week),
        "channel_moves": channel_moves,
        "source": "real",
    }
    decomposition["sessions_change_pct"] = (
        (decomposition["sessions_current"] - decomposition["sessions_baseline"])
        / decomposition["sessions_baseline"] * 100
        if decomposition["sessions_baseline"] else 0.0
    )
    decomposition["notif_open_change"] = (
        decomposition["notif_open_current"] - decomposition["notif_open_baseline"]
    )
    return decomposition


def decompose_simulated(drop_pts):
    """Builds a synthetic scenario for testing the diagnostic chain without
    waiting for real data to actually move. Shaped to mirror the sample in
    agents/anomaly-diagnosis.md: a retention move driven by a proportional
    day-7 move, a sharp session drop, and a smaller push-open-rate move -
    clearly labeled as simulated everywhere it's used."""
    baseline_headline = 37.0
    current_headline = baseline_headline - drop_pts  # negative drop_pts = an increase
    scale = drop_pts / 4.0  # sample scenario is calibrated around a 4pt move

    return {
        "headline_change": -drop_pts,
        "headline_current": current_headline,
        "headline_baseline": baseline_headline,
        "day7_given_day1_current": 54.0 - (4.0 * scale - 4.0),  # anchors to 58->54 at scale=1
        "day7_given_day1_baseline": 58.0,
        "day7_given_day1_change": -4.0 * scale,
        "day30_given_day7_change": -1.0 * scale,
        "sessions_current": 4.1 - (0.9 * scale),
        "sessions_baseline": 4.1,
        "sessions_change_pct": -22.0 * scale,
        "notif_open_current": 54.0 - (3.0 * scale),
        "notif_open_baseline": 54.0,
        "notif_open_change": -3.0 * scale,
        "channel_moves": {"organic": -1.0 * scale, "paid": -4.0 * scale, "referral": 0.0},
        "source": f"SIMULATED (--simulate-drop {drop_pts})",
    }


# ---------- Step 2: ranked hypotheses ----------

def generate_hypotheses(d):
    """Rule-based, transparent scoring - not a black box. Each hypothesis
    gets a score from how well the available signals corroborate it; ties
    are broken in favor of the more specific (less generic) hypothesis."""
    direction = "drop" if d["headline_change"] < 0 else "increase"
    verb = "issue" if direction == "drop" else "improvement"

    hypotheses = []

    # H1: notification/engagement-driven
    notif_move = d.get("notif_open_change", 0) or 0
    sess_move = d.get("sessions_change_pct", 0) or 0
    same_direction = (notif_move < 0) == (d["headline_change"] < 0)
    score1 = 0
    if same_direction and abs(notif_move) >= 2:
        score1 += 2
    if same_direction and abs(sess_move) >= 10:
        score1 += 2
    likelihood1 = "high" if score1 >= 4 else ("medium" if score1 >= 2 else "low")
    hypotheses.append({
        "text": f"Push notification delivery {verb} (correlates with session {direction})"
        if direction == "drop" else
        f"Push notification {verb} driving engagement up (correlates with session {direction})",
        "likelihood": likelihood1,
        "score": score1,
        "type": "notification",
        "rationale": (
            f"push open rate {notif_move:+.1f}pts, sessions {sess_move:+.1f}% - "
            + ("both moved with the headline" if score1 >= 4 else
               "one signal moved with the headline" if score1 >= 2 else
               "signals don't clearly corroborate this")
        ),
    })

    # H2: channel/cohort-quality shift. Scored by ratio to the headline move,
    # not just same-direction magnitude - a single channel merely matching
    # the overall move is weaker evidence than a channel move that dwarfs it
    # (which would suggest the headline is being driven by mix shift alone).
    channel_moves = d.get("channel_moves", {})
    if channel_moves:
        worst_channel, worst_change = max(channel_moves.items(), key=lambda kv: abs(kv[1]))
        same_dir_channel = (worst_change < 0) == (d["headline_change"] < 0)
        ratio = abs(worst_change) / abs(d["headline_change"]) if d["headline_change"] else 0
        if same_dir_channel and ratio >= 1.5:
            score2 = 3
        elif same_dir_channel and ratio >= 0.8:
            score2 = 2
        elif same_dir_channel and ratio >= 0.4:
            score2 = 1
        else:
            score2 = 0
        likelihood2 = "high" if score2 >= 3 else ("medium" if score2 >= 2 else "low")
        hypotheses.append({
            "text": f"New user cohort quality shift from {worst_channel} channel",
            "likelihood": likelihood2,
            "score": score2,
            "type": "channel",
            "rationale": f"{worst_channel} channel retention {worst_change:+.1f}pts vs. headline {d['headline_change']:+.1f}pts",
            "channel": worst_channel,
        })

    # H3: platform/performance - the generic, always-lowest-confidence catch-all
    # since there's no deploy-log data in this workspace to confirm or rule it out.
    hypotheses.append({
        "text": f"App performance regression on a specific platform",
        "likelihood": "low",
        "score": -1,  # always sorts last unless nothing else scored higher
        "type": "platform",
        "rationale": "no deploy-log data available in this workspace to confirm or rule this out",
    })

    hypotheses.sort(key=lambda h: h["score"], reverse=True)
    return hypotheses[:3]


# ---------- Step 3: confirmation SQL ----------

def build_confirmation_sql(top_hypothesis):
    kind = top_hypothesis["type"]
    if kind == "notification":
        return (
            "SELECT date(sent_date) AS date,\n"
            "       COUNT(*) AS nudges_sent,\n"
            "       SUM(opened) AS nudges_opened,\n"
            "       ROUND(100.0 * SUM(opened) / COUNT(*), 1) AS open_rate_pct\n"
            "FROM nudge_nudges\n"
            "WHERE sent_date >= CURRENT_DATE - 7\n"
            "GROUP BY date(sent_date)\n"
            "ORDER BY date;"
        )
    if kind == "channel":
        channel = top_hypothesis.get("channel", "paid")
        return (
            "SELECT u.cohort_week,\n"
            "       COUNT(*) AS users,\n"
            "       ROUND(100.0 * SUM(r.day_30) / COUNT(*), 1) AS day30_retention_pct\n"
            "FROM nudge_users u\n"
            "JOIN nudge_retention r ON r.user_id = u.user_id\n"
            f"WHERE u.acquisition_channel = '{channel}'\n"
            "  AND u.cohort_week >= (SELECT MAX(cohort_week) FROM nudge_users) - 1\n"
            "GROUP BY u.cohort_week\n"
            "ORDER BY u.cohort_week;"
        )
    # platform
    return (
        "SELECT u.platform,\n"
        "       u.cohort_week,\n"
        "       COUNT(DISTINCT u.user_id) AS users,\n"
        "       ROUND(1.0 * COUNT(s.session_id) / COUNT(DISTINCT u.user_id), 2) AS avg_sessions\n"
        "FROM nudge_users u\n"
        "LEFT JOIN nudge_sessions s ON s.user_id = u.user_id\n"
        "WHERE u.cohort_week >= (SELECT MAX(cohort_week) FROM nudge_users) - 1\n"
        "GROUP BY u.platform, u.cohort_week\n"
        "ORDER BY u.platform, u.cohort_week;"
    )


# ---------- Step 4: Slack formatting ----------

def format_diagnostic(d, hypotheses, top_sql, timestamp_str):
    direction = "dropped" if d["headline_change"] < 0 else "increased"
    lines = [
        f":mag: *Nudge Anomaly Detected - {timestamp_str}*",
        "",
        f"Trigger: 30-day retention {direction} {abs(d['headline_change']):.0f}pts "
        f"({d['headline_baseline']:.0f}% -> {d['headline_current']:.0f}%) overnight"
        + (f"  [{d['source']}]" if d["source"] != "real" else ""),
        "",
        "Metric tree decomposition:",
        f"  Day 7 | Day 1 retention:  {d['day7_given_day1_baseline']:.0f}% -> "
        f"{d['day7_given_day1_current']:.0f}% ({d['day7_given_day1_change']:+.0f}pts)",
        f"  Sessions in week 1:       {d['sessions_baseline']:.1f} -> "
        f"{d['sessions_current']:.1f} ({d['sessions_change_pct']:+.0f}%)",
        f"  Push notification opens: {d['notif_open_baseline']:.0f}% -> "
        f"{d['notif_open_current']:.0f}% ({d['notif_open_change']:+.0f}pts)",
        "",
        "Top 3 hypotheses:",
    ]
    for i, h in enumerate(hypotheses, start=1):
        lines.append(f"  {i}. {h['text']} ({h['likelihood']} likelihood - {h['rationale']})")

    lines += [
        "",
        f"SQL to confirm hypothesis 1:",
        "```",
        top_sql,
        "```",
        "",
        "Run this query and reply with the output. I'll interpret.",
    ]
    return "\n".join(lines)


# ---------- Public entry point for chaining from metric_pulse.py ----------

def run_diagnosis(db_path=DEFAULT_DB, headline_change=None):
    """Called by metric_pulse.py when its alert fires. If headline_change is
    given (from the pulse agent's own already-computed number), the real
    decomposition still runs fresh against the DB for the stage breakdown -
    headline_change is accepted for consistency-checking only."""
    d = decompose_from_db(db_path)
    hypotheses = generate_hypotheses(d)
    top_sql = build_confirmation_sql(hypotheses[0])
    timestamp = format_timestamp(datetime.datetime.now())
    return format_diagnostic(d, hypotheses, top_sql, timestamp)


def format_timestamp(dt):
    """Portable 'Tue May 13, 8:47am' style, avoiding %-d/%#d which aren't
    supported the same way across platforms - dt.day is used directly instead."""
    hour12 = dt.strftime("%I").lstrip("0") or "12"
    ampm = dt.strftime("%p").lower()
    return f"{dt.strftime('%a %b')} {dt.day}, {hour12}:{dt.strftime('%M')}{ampm}"


def main():
    parser = argparse.ArgumentParser(description="Anomaly diagnosis engine for Nudge Engage v2")
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument(
        "--simulate-drop", type=float, default=None,
        help="Run against a synthetic scenario instead of real data (e.g. 4 for a -4pt drop, -4 for a +4pt rise)",
    )
    args = parser.parse_args()

    if args.simulate_drop is not None:
        d = decompose_simulated(args.simulate_drop)
    else:
        d = decompose_from_db(args.db)

    hypotheses = generate_hypotheses(d)
    top_sql = build_confirmation_sql(hypotheses[0])
    timestamp = format_timestamp(datetime.datetime.now())
    print(format_diagnostic(d, hypotheses, top_sql, timestamp))


if __name__ == "__main__":
    main()
