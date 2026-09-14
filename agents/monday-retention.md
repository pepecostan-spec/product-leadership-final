# Agent Spec: Monday Retention Check

**Purpose**: Runs every Monday morning before standup. Checks Nudge 30-day retention against last week's baseline, compares session counts and push notification open rates, and posts a plain-English 3-line digest to Slack.

**Script**: `agents/monday_retention.py` — a real, runnable Python script, verified against `data/nudge.db` (the same SQLite database built during earlier metric analysis, see `data/metric-findings.md`).

---

## 1. What it checks

Three metrics, each comparing the most recent cohort against the previous one:
- **30-day retention rate** — from `nudge_retention.day_30`
- **Average sessions per user** — from `nudge_sessions`
- **Push notification open rate** — from `nudge_nudges.opened` (the general nudge stream, not the weekly-summary-specific send table, so this comparison is meaningful across every cohort, not just the pilot)

**Important assumption, stated plainly**: in this dataset, "week" is modeled as signup cohort week (`cohort_week`), since that's what the available data supports. In a real production deployment, this would instead compare "the cohort that crosses day-30 this week" against "the cohort that crossed day-30 last week" — the same logic, just driven by rolling calendar dates instead of a fixed dataset. The script's `latest_two_cohort_weeks()` function is the one piece that would change; everything downstream stays the same.

## 2. How to run it manually (verify before scheduling anything)

```bash
python agents/monday_retention.py
```

This always prints the digest to the console and never posts anywhere — safe to run as many times as needed while checking the output makes sense.

**Verified output against the current dataset**:
```
:bar_chart: *Nudge Monday Retention Digest*
- *Headline:* 30-day retention is 29.0% this week, vs 22.0% last week (+7.0 points).
- *Signal to watch:* Biggest mover: 30-day retention is up 32% week-over-week (22.0% -> 29.0%).
- *Suggested action:* Retention moved the most - check whether this tracks with the weekly summary rollout or test cohort before reading too much into it.
```

To actually post to Slack, set a webhook and pass `--post`:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python agents/monday_retention.py --post
```
Without `SLACK_WEBHOOK_URL` set, `--post` fails loudly and clearly rather than silently doing nothing — verified: running `--post` with no webhook configured prints the digest, then exits with `SLACK_WEBHOOK_URL not set - can't post. Run without --post to dry-run.`

## 3. Slack message template

```
:bar_chart: *Nudge Monday Retention Digest*
- *Headline:* [30-day retention this week] vs [last week] ([+/- point change])
- *Signal to watch:* Biggest mover: [metric name] is [up/down] [X]% week-over-week ([last week value] -> [this week value])
- *Suggested action:* [one tailored line based on which metric moved and which direction]
```

The "biggest mover" is whichever of the 3 metrics has the largest relative (%) change week-over-week — not whichever is easiest to explain. The suggested action is templated per metric and direction (6 variants total: 3 metrics x rising/falling), so the digest always names something concrete to look at rather than a generic "keep an eye on things."

## 4. Real-world deployment

This is a spec + verified script, not a live schedule. To actually run it every Monday morning:
- **Cron** (simplest, if the machine is always on): `0 8 * * 1 SLACK_WEBHOOK_URL=... python /path/to/agents/monday_retention.py --post`
- **n8n**: a scheduled trigger (Monday, e.g. 8am) -> Execute Command node running the script -> the script's own `--post` handles Slack delivery, so n8n just needs to invoke it with the webhook env var set.
- **Python on a timer**: `schedule` or `APScheduler` running `monday_retention.py --post` in a long-lived process, or a serverless function (Lambda/Cloud Function) on a weekly EventBridge/Cloud Scheduler trigger.

In any of these, the real data source (`data/nudge.db` here) would be swapped for a live query against the production warehouse — the script's SQL and comparison logic don't need to change, only `get_connection()` and the queries' table/column names if the production schema differs from `nudge_users` / `nudge_retention` / `nudge_sessions` / `nudge_nudges`.
