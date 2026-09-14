#!/usr/bin/env python3
"""
Monday Retention Check - Nudge Engage v2

Compares the most recent cohort against the previous one on:
  - 30-day retention rate
  - average sessions per user
  - push notification open rate

Prints a 3-line plain-English digest. Posts to Slack only if --post is
passed AND SLACK_WEBHOOK_URL is set - otherwise it always just prints,
so it's safe to run manually to check output before wiring it to a
schedule.

Usage:
    python monday_retention.py                 # dry run, prints digest
    python monday_retention.py --post           # also posts to Slack
    python monday_retention.py --db other.db    # point at a different database
"""

import argparse
import json
import os
import sqlite3
import sys
import urllib.request

LABELS = {
    "retention": "30-day retention",
    "sessions": "average sessions per user",
    "open_rate": "push notification open rate",
}

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "data", "nudge.db")


def get_connection(db_path):
    if not os.path.exists(db_path):
        sys.exit(f"Database not found at {db_path}")
    return sqlite3.connect(db_path)


def latest_two_cohort_weeks(conn):
    """
    In this dataset, 'week' = signup cohort week. In production, swap this
    for 'the cohort that crossed day-30 this week' vs 'last week' - same
    idea, driven by rolling calendar dates instead of a fixed dataset.
    """
    cur = conn.execute(
        "SELECT DISTINCT cohort_week FROM nudge_users ORDER BY cohort_week DESC LIMIT 2"
    )
    weeks = [row[0] for row in cur.fetchall()]
    if len(weeks) < 2:
        sys.exit("Need at least 2 cohort weeks of data to compare.")
    return weeks[0], weeks[1]  # current, baseline


def retention_rate(conn, cohort_week):
    cur = conn.execute(
        """
        SELECT COUNT(*), SUM(r.day_30)
        FROM nudge_retention r
        JOIN nudge_users u ON u.user_id = r.user_id
        WHERE u.cohort_week = ?
        """,
        (cohort_week,),
    )
    total, retained = cur.fetchone()
    return (retained or 0) / total * 100 if total else 0.0


def avg_sessions(conn, cohort_week):
    cur = conn.execute(
        """
        SELECT COUNT(DISTINCT u.user_id), COUNT(s.session_id)
        FROM nudge_users u
        LEFT JOIN nudge_sessions s ON s.user_id = u.user_id
        WHERE u.cohort_week = ?
        """,
        (cohort_week,),
    )
    users, sessions = cur.fetchone()
    return (sessions or 0) / users if users else 0.0


def notification_open_rate(conn, cohort_week):
    cur = conn.execute(
        """
        SELECT COUNT(*), SUM(n.opened)
        FROM nudge_nudges n
        JOIN nudge_users u ON u.user_id = n.user_id
        WHERE u.cohort_week = ?
        """,
        (cohort_week,),
    )
    total, opened = cur.fetchone()
    return (opened or 0) / total * 100 if total else 0.0


def relative_change(current, baseline):
    return 0.0 if baseline == 0 else (current - baseline) / baseline * 100


def suggest_action(metric_name, falling):
    if metric_name == "retention":
        return (
            "Retention dropped the most - pull this week's cohort and check "
            "whether it overlaps with the pilot or control group before reacting."
            if falling else
            "Retention moved the most - check whether this tracks with the "
            "weekly summary rollout or test cohort before reading too much into it."
        )
    if metric_name == "sessions":
        return (
            "Session counts dropped the most - worth a quick look at whether "
            "anything changed in the home feed or onboarding this week."
            if falling else
            "Session counts are up the most - check whether it's broad or "
            "concentrated in one channel or platform before calling it a trend."
        )
    if metric_name == "open_rate":
        return (
            "Notification open rate dropped the most - check for a spike in "
            "opt-outs or a recent change to nudge content or timing."
            if falling else
            "Notification open rate is up the most - see if it's concentrated "
            "in the weekly summary send specifically, since that's what we're testing."
        )
    return "Take a closer look at this week's numbers before standup."


def build_digest(metrics):
    retention_cur, retention_base, _ = metrics["retention"]
    point_change = retention_cur - retention_base
    headline = (
        f"30-day retention is {retention_cur:.1f}% this week, "
        f"vs {retention_base:.1f}% last week ({point_change:+.1f} points)."
    )

    movers = [
        (name, cur, base, relative_change(cur, base), unit)
        for name, (cur, base, unit) in metrics.items()
    ]
    name, cur, base, rel, unit = max(movers, key=lambda m: abs(m[3]))
    direction = "up" if rel >= 0 else "down"
    signal = (
        f"Biggest mover: {LABELS[name]} is {direction} {abs(rel):.0f}% "
        f"week-over-week ({base:.1f}{unit} -> {cur:.1f}{unit})."
    )

    action = suggest_action(name, falling=(rel < 0))
    return headline, signal, action


def format_slack_message(headline, signal, action):
    return (
        ":bar_chart: *Nudge Monday Retention Digest*\n"
        f"- *Headline:* {headline}\n"
        f"- *Signal to watch:* {signal}\n"
        f"- *Suggested action:* {action}"
    )


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
    parser = argparse.ArgumentParser(description="Monday retention check for Nudge Engage v2")
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--post", action="store_true", help="Post to Slack (default: dry-run print only)")
    args = parser.parse_args()

    conn = get_connection(args.db)
    current_week, baseline_week = latest_two_cohort_weeks(conn)

    metrics = {
        "retention": (retention_rate(conn, current_week), retention_rate(conn, baseline_week), "%"),
        "sessions": (avg_sessions(conn, current_week), avg_sessions(conn, baseline_week), ""),
        "open_rate": (notification_open_rate(conn, current_week), notification_open_rate(conn, baseline_week), "%"),
    }

    headline, signal, action = build_digest(metrics)
    message = format_slack_message(headline, signal, action)

    print(message)

    if args.post:
        post_to_slack(message)
        print("\nPosted to Slack.")


if __name__ == "__main__":
    main()
