# Agent Spec: Metric Pulse — 30-Day Retention

**Purpose**: Runs nightly, delivers a Monday 8am Slack digest on 30-day retention — headline number, channel breakdown (organic/paid/referral), and an alert if the metric moved 2+ percentage points week-over-week.

**Script**: `agents/metric_pulse.py` — real, runnable, verified against `data/nudge.db` (same database as `agents/monday_retention.py`).

---

## 1. The agent script

`agents/metric_pulse.py` computes:
- **Headline**: overall 30-day retention for the current cohort vs. the previous one. If there's no previous week yet (first run), it falls back to the configured `BASELINE_RETENTION_PCT = 37.0` instead of failing — so day one has something to compare against.
- **Channel breakdown**: the same comparison, filtered to `organic`, `paid`, `referral` (from `nudge_users.acquisition_channel`).
- **Alert**: fires if the headline movement is >= `ALERT_THRESHOLD_PP = 2.0` points, in either direction — a big unexplained jump deserves a look just as much as a drop.
- **Top signal**: whichever channel moved the most in absolute terms (ties favor the decline, since drops are the higher-priority read), with a direction-specific suggested check (6 templates: 3 channels x up/down).
- **Follow-up prompt**: only appended when the alert fires, matching the requested format.

**Design note — ASCII output, not arrow glyphs**: the spec's sample uses ↓/↑/→ symbols. The script instead prints "up"/"down"/"flat" as words. This mirrors a real issue hit while building `agents/monday_retention.py`: those Unicode arrows crash `print()` on a default Windows console (`UnicodeEncodeError`, cp1252 can't encode them). Slack itself renders Unicode fine, so if this is deployed as a true Slack-only integration, swap the words back for arrow glyphs in `format_point_change()` — just don't rely on printing them to a Windows terminal for the manual-verification step below.

## 2. Slack message template

```
:bar_chart: *Nudge Retention Pulse - [Date]*

30-day retention: [X]% ([up/down Npts | flat] vs last week) [:warning: ALERT if >=2pt move]

By channel:
  Organic   [X]% ([up/down Npts | flat])
  Paid      [X]% ([up/down Npts | flat])  [<- watch this, on the worst decliner]
  Referral  [X]% ([up/down Npts | flat])

Top signal: [Channel] channel [drop accelerating | up sharply] ([+/-N]pts). [Suggested check].

[Only if alert fired:]
Next: run anomaly diagnosis? Reply YES to trigger.
```

Note on that last line: this script produces a one-way digest (webhook post), so "Reply YES" isn't wired to anything yet — see Section 4 for what real interactivity would require.

## 3. How to run it manually (verify before scheduling)

```bash
python agents/metric_pulse.py
```

Always prints to console, never posts — safe to re-run freely. Options:
- `--date "Mon May 12"` — override the displayed date (defaults to today)
- `--db path/to/other.db` — point at a different database
- `--post` — actually post to Slack (see below)

To post for real:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python agents/metric_pulse.py --post
```
Verified: without `SLACK_WEBHOOK_URL` set, `--post` prints the digest, then exits with `SLACK_WEBHOOK_URL not set - can't post. Run without --post to dry-run.` — it fails loudly rather than silently doing nothing.

## 4. Real-world wiring

This is a spec + verified script, not a live schedule. Three ways to actually run it nightly with Monday 8am delivery:

- **Python + cron** (simplest if a machine is always on): run the script nightly for data freshness, but only pass `--post` on Mondays —
  `0 2 * * * python /path/to/agents/metric_pulse.py > /var/log/metric_pulse.log` (nightly, silent)
  `0 8 * * 1 SLACK_WEBHOOK_URL=... python /path/to/agents/metric_pulse.py --post` (Monday delivery)
- **n8n**: a nightly scheduled trigger runs the script for logging/caching, and a separate Monday-8am trigger runs it with `--post`. If "Reply YES to trigger anomaly diagnosis" needs to be real, that requires a Slack app with an Events API subscription (not just an incoming webhook) wired to an n8n webhook-trigger node — worth flagging as separate scope, not a cron/script change.
- **Developer ticket** (if this needs to run against the real production warehouse instead of `data/nudge.db`): the ticket is narrow — swap `get_connection()` for the production DB connection, and confirm `nudge_users`/`nudge_retention` column names match the real schema (`acquisition_channel`, `cohort_week`, `day_30`). The comparison logic, alerting, and Slack formatting don't need to change.

## 5. Test run against the Nudge metrics snapshot

Real output, verified by actually running the script against `data/nudge.db` (cohort week 5 vs. cohort week 4 — the same "current vs. previous" pairing used in `agents/monday_retention.py`):

```
:bar_chart: *Nudge Retention Pulse - Mon May 12*

30-day retention: 29% (up 7pts vs last week) :warning: ALERT

By channel:
  Organic   37% (up 11pts)
  Paid      16% (flat)
  Referral  29% (up 8pts)

Top signal: Organic channel up sharply (+11pts). Check if this tracks with a recent onboarding change, or could be cohort-size noise.

Next: run anomaly diagnosis? Reply YES to trigger.
```

**Read this honestly, not just as a demo**: the sample in the spec showed an illustrative decline; this dataset's actual current-vs-previous cohort comparison is a genuine +7-point increase, driven mainly by organic (+11pts). That's real output from real data, not adjusted to match the illustrative example — the script reports what's actually there. The alert still fires because the threshold is direction-agnostic, which is why a big unexplained jump gets flagged the same as a drop.
