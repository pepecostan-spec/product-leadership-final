#!/usr/bin/env python3
"""
Metric Pulse Agent - Nudge Engage v2

Monitors 30-day retention week-over-week, broken down by acquisition channel
(organic, paid, referral), and produces a Monday-morning Slack digest.

Alerts when the headline (all-channel) retention moves >= ALERT_THRESHOLD_PP
percentage points versus the prior week, in either direction. Falls back to
BASELINE_RETENTION when there's no prior week to compare against yet (e.g.
the very first run).

When the alert fires, this chains into anomaly_diagnosis.py to produce a full
diagnostic (metric tree decomposition, ranked hypotheses, confirmation SQL) -
see agents/anomaly-diagnosis.md. The diagnostic only ever runs on alert, never
on a quiet week.

Usage:
    python metric_pulse.py                 # dry run, prints digest (+ diagnosis if alert)
    python metric_pulse.py --post           # also posts to Slack (both messages, if alert)
    python metric_pulse.py --db other.db    # point at a different database
    python metric_pulse.py --no-diagnosis   # skip the chained diagnosis even on alert
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys
import urllib.request

import anomaly_diagnosis

BASELINE_RETENTION_PCT = 37.0   # documented company baseline, see CLAUDE.md
ALERT_THRESHOLD_PP = 2.0        # percentage points, either direction
FLAT_THRESHOLD_PP = 1.0         # below this, a channel is reported as "flat"
CHANNELS = ["organic", "paid", "referral"]

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "data", "nudge.db")

CHANNEL_CHECKS = {
    ("organic", "down"): "check for a recent change to the home feed or content/SEO funnel",
    ("organic", "up"): "check if this tracks with a recent onboarding change, or could be cohort-size noise",
    ("paid", "down"): "check campaign changes or ad spend/targeting shifts from last week",
    ("paid", "up"): "check if this tracks with a specific campaign or targeting change",
    ("referral", "down"): "check for issues with the referral flow or a lapsed incentive",
    ("referral", "up"): "check if a referral incentive or program change is driving this",
}


def get_connection(db_path):
    if not os.path.exists(db_path):
        sys.exit(f"Database not found at {db_path}")
    return sqlite3.connect(db_path)


def latest_two_cohort_weeks(conn):
    """
    In this dataset, 'week' = signup cohort week. In production, swap this for
    rolling calendar weeks of the cohort crossing day-30 - same idea, driven by
    live dates instead of a fixed dataset. See agents/metric-pulse.md Section 4.
    """
    cur = conn.execute(
        "SELECT DISTINCT cohort_week FROM nudge_users ORDER BY cohort_week DESC LIMIT 2"
    )
    weeks = [row[0] for row in cur.fetchall()]
    if not weeks:
        sys.exit("No cohort data found.")
    current = weeks[0]
    baseline_week = weeks[1] if len(weeks) > 1 else None
    return current, baseline_week


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
    cur = conn.execute(query, params)
    total, retained = cur.fetchone()
    if not total:
        return None
    return (retained or 0) / total * 100


def arrow(change_pp):
    if change_pp is None:
        return "-"
    if abs(change_pp) < FLAT_THRESHOLD_PP:
        return "flat"
    return "up" if change_pp > 0 else "down"


def format_point_change(change_pp):
    """Renders '(down 2pts)' / '(flat)' / '(up 1pt)' style fragments."""
    if change_pp is None:
        return "(no prior week - vs baseline)"
    direction = arrow(change_pp)
    if direction == "flat":
        return "(flat)"
    pts = abs(change_pp)
    unit = "pt" if round(pts) == 1 else "pts"
    return f"({direction} {pts:.0f}{unit})"


def collect_metrics(conn, current_week, baseline_week):
    overall_current = retention_rate(conn, current_week)
    if baseline_week is not None:
        overall_baseline = retention_rate(conn, baseline_week)
    else:
        overall_baseline = BASELINE_RETENTION_PCT  # first-run fallback

    overall_change = (
        overall_current - overall_baseline if overall_baseline is not None else None
    )

    channels = {}
    for ch in CHANNELS:
        cur_val = retention_rate(conn, current_week, ch)
        if baseline_week is not None:
            base_val = retention_rate(conn, baseline_week, ch)
        else:
            base_val = None  # no per-channel baseline fallback - only headline has one
        change = (cur_val - base_val) if (cur_val is not None and base_val is not None) else None
        channels[ch] = {"current": cur_val, "baseline": base_val, "change": change}

    return {
        "overall": {"current": overall_current, "baseline": overall_baseline, "change": overall_change},
        "channels": channels,
    }


def worst_or_biggest_mover(channels):
    """Returns (channel_name, change) for the channel with the largest absolute
    move. Ties favor the decline, since drops are the higher-priority signal."""
    scored = [
        (name, data["change"])
        for name, data in channels.items()
        if data["change"] is not None
    ]
    if not scored:
        return None, None
    scored.sort(key=lambda x: (-abs(x[1]), x[1]))
    return scored[0]


def build_top_signal(channels):
    name, change = worst_or_biggest_mover(channels)
    if name is None or abs(change) < FLAT_THRESHOLD_PP:
        return "Top signal: No major channel-level movement this week."
    direction = "down" if change < 0 else "up"
    verb = "drop accelerating" if direction == "down" else "up sharply"
    check = CHANNEL_CHECKS[(name, direction)]
    return f"Top signal: {name.capitalize()} channel {verb} ({change:+.0f}pts). {check.capitalize()}."


def build_digest(metrics, date_str):
    overall = metrics["overall"]
    alert = overall["change"] is not None and abs(overall["change"]) >= ALERT_THRESHOLD_PP

    vs_label = "vs baseline" if overall["baseline"] == BASELINE_RETENTION_PCT else "vs last week"
    if overall["change"] is None:
        headline_change = f"(no prior week - {vs_label})"
    else:
        direction = arrow(overall["change"])
        if direction == "flat":
            headline_change = f"(flat {vs_label})"
        else:
            pts = abs(overall["change"])
            unit = "pt" if round(pts) == 1 else "pts"
            headline_change = f"({direction} {pts:.0f}{unit} {vs_label})"
    headline = f"30-day retention: {overall['current']:.0f}% {headline_change}"
    if alert:
        headline += " :warning: ALERT"

    channel_lines = []
    for ch in CHANNELS:
        data = metrics["channels"][ch]
        if data["current"] is None:
            continue
        change_str = format_point_change(data["change"])
        name, _ = worst_or_biggest_mover(metrics["channels"])
        watch = "  <- watch this" if ch == name and data["change"] is not None and data["change"] <= -FLAT_THRESHOLD_PP else ""
        channel_lines.append(f"  {ch.capitalize():<10}{data['current']:.0f}% {change_str}{watch}")

    top_signal = build_top_signal(metrics["channels"])

    lines = [
        f":bar_chart: *Nudge Retention Pulse - {date_str}*",
        "",
        headline,
        "",
        "By channel:",
        *channel_lines,
        "",
        top_signal,
    ]
    if alert:
        lines += ["", "Next: run anomaly diagnosis? Reply YES to trigger."]

    return "\n".join(lines), alert


def post_to_slack(message):
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        sys.exit("SLACK_WEBHOOK_URL not set - can't post. Run without --post to dry-run.")
    payload = json.dumps({"text": message}).encode("utf-8")
    req = urllib.request.Request(
        webhook, data=payload, headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)


def main():
    parser = argparse.ArgumentParser(description="Metric pulse agent for Nudge Engage v2")
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--post", action="store_true", help="Post to Slack (default: dry-run print only)")
    parser.add_argument("--date", default=None, help="Override the displayed date (e.g. 'Mon May 12')")
    parser.add_argument(
        "--no-diagnosis", action="store_true",
        help="Skip the chained anomaly diagnosis even if the alert fires",
    )
    args = parser.parse_args()

    conn = get_connection(args.db)
    current_week, baseline_week = latest_two_cohort_weeks(conn)
    metrics = collect_metrics(conn, current_week, baseline_week)

    date_str = args.date or datetime.date.today().strftime("%a %b ") + str(datetime.date.today().day)
    message, alert = build_digest(metrics, date_str)

    print(message)
    if args.post:
        post_to_slack(message)
        print("\nPosted to Slack.")

    # Chained anomaly diagnosis - only ever runs when the alert fires.
    if alert and not args.no_diagnosis:
        diagnostic = anomaly_diagnosis.run_diagnosis(db_path=args.db)
        print("\n" + diagnostic)
        if args.post:
            post_to_slack(diagnostic)
            print("\nPosted diagnostic to Slack.")

    sys.exit(0)


if __name__ == "__main__":
    main()
