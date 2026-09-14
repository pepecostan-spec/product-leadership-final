# Nudge PM Agent Registry

Last updated: 2/8/2026

**Note on `agents/monday_retention.py`**: an earlier prototype covering similar ground to the Metric Pulse Agent below (retention/session/notification digest, Monday delivery). It's superseded by Metric Pulse, which added the channel breakdown, an explicit alert threshold, and the anomaly chain — kept in the repo but not part of the active stack documented here.

---

## Metric Pulse Agent

- **Trigger**: nightly (cron or n8n in production); manually verified via `python agents/metric_pulse.py`
- **Data source**: `data/nudge.db` — real SQLite database built from the Nudge metrics snapshot (not a markdown file; see `agents/metric-pulse.md` Section 1)
- **Breakdown**: acquisition channel (organic, paid, referral)
- **Alert threshold**: ±2pts week-over-week, either direction
- **Output format**: Slack digest — headline retention number, per-channel breakdown, top signal, alert flag if threshold crossed
- **Delivery channel**: Slack (via `SLACK_WEBHOOK_URL`) — intended for #pm-nudge-engage; the script itself is channel-agnostic, the destination is set wherever the webhook is configured in Slack, not in code
- **Schedule**: computes nightly, delivers Monday 8am
- **Owner**: Pepe
- **Spec**: `agents/metric-pulse.md`

## Weekly Insight Report

- **Trigger**: Friday 4pm (cron or n8n in production); manually verified via `python agents/weekly_insight.py`
- **Data sources**: `data/nudge.db` (retention/session/notification signals), `change_log.md` (sprint completions this week), freshest `research/synthesis-YYYY-MM-DD.md` or `research/nps-analysis.md` as fallback (top NPS themes)
- **Output format**: 3-2-1 report — Done this week (3), Changed this week (2), Watch next week (1)
- **Delivery channel**: `reports/YYYY-MM-DD.md` (versioned file, one per week) + Slack summary via `SLACK_WEBHOOK_URL`
- **Schedule**: weekly, Friday 4pm
- **Owner**: Pepe
- **Spec**: `agents/weekly-insight.md`

## Anomaly-to-Hypothesis Agent

- **Trigger**: fired in-process by the Metric Pulse Agent when its alert threshold (±2pts) is crossed — not on its own schedule
- **Data source**: `data/nudge.db`, independently re-queried for its own metric-tree decomposition (see Connection Plan below — this is currently a gap, not a strength)
- **Output format**: metric tree decomposition (day-1→7, day-7→30, sessions, push open rate) → 3 ranked hypotheses (notification, channel-mix, platform) → templated confirmation SQL
- **Delivery channel**: Slack via `SLACK_WEBHOOK_URL`, posted as a second, separate message immediately after the pulse digest — **not** a true Slack thread reply. That would require the Slack Web API (`chat.postMessage` with `thread_ts`) rather than a plain incoming webhook, which can only post standalone messages. Worth fixing if a real threaded diagnostic matters more than sequential messages.
- **Schedule**: event-driven, only runs on alert
- **Owner**: Pepe
- **Spec**: `agents/anomaly-diagnosis.md`

---

## Connection Plan

### Pulse -> Anomaly (built)
Mechanism: a direct in-process function call, not a queue or event system. `metric_pulse.py` computes `alert` as part of building its own digest; when true, it imports `anomaly_diagnosis` and calls `run_diagnosis(db_path=args.db)`.

**Real gap worth fixing**: the two agents currently share a *database*, not *computed values* — `anomaly_diagnosis.py` independently re-queries `data/nudge.db` for its own headline number instead of receiving the pulse agent's already-computed metrics directly. `run_diagnosis()` even has an unused `headline_change` parameter that was never wired up. This works today because both run in the same process moments apart, but it's redundant (retention queried twice) and would be a real consistency risk if these ever split into separate services. **Fix**: pass the pulse agent's `metrics` dict straight into `run_diagnosis()` instead of re-deriving it.

**If these become separate deployed services** (not just one script importing another): the connection would need to become a message, not a function call — the pulse agent publishing an "alert fired" event (with its computed metrics as payload) to a queue or webhook that the anomaly service subscribes to.

### Anomaly -> Weekly Insight (not yet built — this is the actual plan)
Today, nothing connects them. The Weekly Insight Report's "Watch next week" bullet comes from a keyword scan of `change_log.md` (`tbd`, `blocker`, `estimate`, etc.) — completely independent of anything the Anomaly Agent produces. If an anomaly fires mid-week, it won't show up in Friday's report unless someone happens to log it in a way that matches those keywords.

**Proposed connection**:
1. Have `anomaly_diagnosis.py` write a structured record every time it fires — e.g. `reports/anomalies/YYYY-MM-DD.md`, containing the direction, magnitude, and top hypothesis (mirroring how `weekly_insight.py` already saves dated reports).
2. Modify `weekly_insight.py`'s `build_watch_bullet()` to check for any anomaly record from the current week **first** — an actual detected anomaly is a stronger signal than a generic keyword match — and only fall back to the change_log scan if none fired.
3. Result: Pulse -> Anomaly (already built) -> structured anomaly log (new) -> Weekly Insight reads that log as its top-priority Watch source (new).

This isn't built yet — flagging it as a concrete, scoped next step rather than a vague aspiration.

---

## 6-Month Roadmap: one agent per month

Building toward a fully connected PM agent stack — each addition targets a real, already-identified gap rather than a generic capability:

**Month 1 — Experiment Monitor Agent**: tracks the fully-powered follow-up test designed in `data/experiment-design.md` (enrollment progress, day-7 retention, open-rate trend, opt-out rate, sample-ratio-mismatch) and flags if it's on track, underpowered, or safe to call early.

**Month 2 — Competitive Pulse, automated**: `skills/competitive-pulse.md` already defines the process manually; turn it into a real scheduled agent that runs the web searches itself and posts findings, no invocation needed.

**Month 3 — Stakeholder Digest Router**: auto-generates both formats from `skills/weekly-status.md` (Team Update for Raj/Lena, Leadership Update for Marcus) from the week's agent outputs, and routes each to the right channel — closing the loop between raw metrics and audience-specific communication.

**Month 4 — QA Regression Watcher**: runs the edge cases already catalogued in `docs/qa-checklist.md` (empty states, cold-start threshold, multi-account scenarios) against live data nightly, flagging regressions before users hit them.

**Month 5 — Open-Questions Tracker Agent**: closes the gap `workspace-audit.md` and `docs/capstone-session.md` both flagged and never built — scans every doc for unresolved markers (reusing the keyword-scan logic already in `weekly_insight.py`) and maintains a live `docs/open-questions.md` with staleness flags (e.g., "open 3+ weeks, ping owner").

**Month 6 — Retention Forecast Agent**: by now there's 6 months of real logged Metric Pulse history to fit a trend against — projects where 30-day retention is headed next month under current trajectory, and models simple what-if scenarios (e.g., "if day-7→30 durability were solved, retention would trend toward X").

**What "fully connected" looks like by month 6**: a stack that doesn't just monitor — it detects (Pulse), diagnoses (Anomaly), tracks whether diagnosed problems actually get resolved (Open-Questions Tracker), keeps the right humans informed in the right format (Stakeholder Router), catches regressions before they compound (QA Watcher), and projects forward instead of only looking backward (Forecast Agent).
