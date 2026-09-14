# Agent Spec: Anomaly Diagnosis (chained to Metric Pulse)

**Purpose**: When `agents/metric_pulse.py`'s alert fires (30-day retention moves >=2pp week-over-week, either direction), automatically decompose the move with the metric tree, generate 3 ranked hypotheses, write the SQL to confirm the top one, and post the full diagnostic to Slack — no separate schedule, no manual trigger. Only ever runs on alert.

**Scripts**: `agents/anomaly_diagnosis.py` (the diagnostic engine, real and runnable) + a small chaining change to `agents/metric_pulse.py`.

---

## 1. The updated pulse agent

`agents/metric_pulse.py` now imports `anomaly_diagnosis` and, in `main()`, checks the `alert` flag its own digest already computes:

```python
if alert and not args.no_diagnosis:
    diagnostic = anomaly_diagnosis.run_diagnosis(db_path=args.db)
    print("\n" + diagnostic)
    if args.post:
        post_to_slack(diagnostic)
```

That's the entire chain — no new trigger mechanism, no polling. The pulse agent already computes `alert` for its own digest; the diagnosis just reads that same flag. A new `--no-diagnosis` flag exists to run the plain pulse digest without it, for cases where you want the headline without the deep-dive.

## 2. The diagnostic chain: metric tree -> hypotheses -> SQL

**Step 1 — Metric tree decomposition** (`decompose_from_db` / `decompose_simulated`): re-runs the same day-1 / day-1→7 / day-7→30 decomposition as `data/metric-diagnosis.md`, plus average sessions and push notification open rate, current cohort vs. previous. This answers *where* in the funnel the move actually happened, not just that it happened.

**Step 2 — 3 ranked hypotheses** (`generate_hypotheses`): rule-based and transparent, not a black box —
- **Notification/engagement**: scores up when push open rate *and* session count both moved the same direction as the headline. Both moving together = high; one moving = medium; neither = low.
- **Channel/cohort-quality shift**: scores by the *ratio* of the worst-moving channel's change to the headline change — a channel move that dwarfs the headline (ratio ≥1.5) reads as high confidence; one that merely matches it (ratio ≥0.8) reads as medium, since matching the headline doesn't by itself prove the channel is driving it rather than just reflecting it.
- **Platform/performance regression**: always the generic, lowest-confidence catch-all, since this workspace has no deploy-log data to confirm or rule it out — stated explicitly rather than guessed at.

Hypotheses are sorted by score and the top 3 returned, direction-aware (the same logic frames language as "issue"/"drop" for a decline or "improvement"/"increase" for a rise).

**Step 3 — Confirmation SQL** (`build_confirmation_sql`): templated per hypothesis type, using this workspace's **real** table names (`nudge_nudges`, `nudge_users`, `nudge_sessions`, `nudge_retention`) — not the illustrative `nudge_notifications` table name from the original spec sample, which doesn't exist in this schema.

## 3. The Slack diagnostic format

```
:mag: *Nudge Anomaly Detected - [Day Mon D, H:MMam/pm]*

Trigger: 30-day retention [dropped/increased] Npts (X% -> Y%) overnight

Metric tree decomposition:
  Day 7 | Day 1 retention:  X% -> Y% (+/-Npts)
  Sessions in week 1:       X -> Y (+/-N%)
  Push notification opens:  X% -> Y% (+/-Npts)

Top 3 hypotheses:
  1. [Hypothesis text] ([likelihood] likelihood - [rationale])
  2. [Hypothesis text] ([likelihood] likelihood - [rationale])
  3. [Hypothesis text] ([likelihood] likelihood - [rationale])

SQL to confirm hypothesis 1:
```
[templated SQL for the #1-ranked hypothesis]
```

Run this query and reply with the output. I'll interpret.
```

This posts as its own Slack message immediately after the regular pulse digest — not merged into one wall of text — so the headline alert stays scannable and the deep-dive is a clear follow-up.

## 4. Simulated test: a 4-point retention drop

```bash
python agents/anomaly_diagnosis.py --simulate-drop 4
```

Runs the diagnostic engine against a synthetic scenario instead of real data — clearly labeled `[SIMULATED (--simulate-drop 4.0)]` in the output so it's never mistaken for a real alert. **Verified real output**:

```
:mag: *Nudge Anomaly Detected - Sun Aug 2, 7:38pm*

Trigger: 30-day retention dropped 4pts (37% -> 33%) overnight  [SIMULATED (--simulate-drop 4.0)]

Metric tree decomposition:
  Day 7 | Day 1 retention:  58% -> 54% (-4pts)
  Sessions in week 1:       4.1 -> 3.2 (-22%)
  Push notification opens: 54% -> 51% (-3pts)

Top 3 hypotheses:
  1. Push notification delivery issue (correlates with session drop) (high likelihood - push open rate -3.0pts, sessions -22.0% - both moved with the headline)
  2. New user cohort quality shift from paid channel (medium likelihood - paid channel retention -4.0pts vs. headline -4.0pts)
  3. App performance regression on a specific platform (low likelihood - no deploy-log data available in this workspace to confirm or rule this out)

SQL to confirm hypothesis 1:
```
SELECT date(sent_date) AS date,
       COUNT(*) AS nudges_sent,
       SUM(opened) AS nudges_opened,
       ROUND(100.0 * SUM(opened) / COUNT(*), 1) AS open_rate_pct
FROM nudge_nudges
WHERE sent_date >= CURRENT_DATE - 7
GROUP BY date(sent_date)
ORDER BY date;
```

Run this query and reply with the output. I'll interpret.
```

This matches the ranking pattern from the original spec sample exactly (notification=high, channel=medium, platform=low) once the channel-hypothesis scoring was calibrated to use a ratio-to-headline check rather than simple magnitude — an initial version scored the paid-channel hypothesis "high" (since it merely matched the headline's magnitude), which is weaker evidence than a population-wide session+push correlation and got corrected to "medium" during verification.

**Also verified: the real, live chain** (`python agents/metric_pulse.py`, no simulation flag) — the current data in `data/nudge.db` actually crosses the alert threshold (+7pts, an increase), so the chain fired for real, not just in simulation:

```
Top 3 hypotheses:
  1. New user cohort quality shift from organic channel (high likelihood - organic channel retention +11.0pts vs. headline +7.0pts)
  2. Push notification improvement driving engagement up (correlates with session increase) (medium likelihood - push open rate +1.0pts, sessions +21.4% - one signal moved with the headline)
  3. App performance regression on a specific platform (low likelihood - no deploy-log data available in this workspace to confirm or rule this out)
```

Note the ranking flipped versus the simulated drop — here the channel signal (organic, ratio 11/7 ≈ 1.6) outranks the notification signal, which the rule-based scoring gets right without any special-casing for direction.
