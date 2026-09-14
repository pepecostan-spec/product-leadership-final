# Nudge — Context

## Right now
- **Core metric**: 30-day retention — % of users still active 30 days after connecting their first account. Dropped from 44% to 37% over the last two quarters.
- **Open decision**: The weekly summary / notification ranking feature is built and in QA (`docs/qa-checklist.md`). Pilot A/B test (n=50/arm) showed a day-7 lift that's statistically significant (p=0.002) and fixes the actual driver of the retention decline (`data/metric-diagnosis.md`) — but the day-30 lift is **not** significant at this sample size (p≈0.12–0.19). Recommendation to Marcus changed from "scale now" to "run a fully powered test first" (~1,200/arm, ~7 weeks — `data/experiment-design.md`), keeping the feature live for existing pilot users meanwhile. `docs/recommendation-memo.md` reflects this, and a quarterly review deck (`docs/presentation.md`) makes this same ask to Marcus. Open now: get the full test running, plus a separate hypothesis still needed for day-7→30 durability, which this feature doesn't touch either way — see `workspace-audit.md`, this has no home yet.
- **Standing constraint**: Engineering capacity — competing priorities are pulling Raj onto other work. Scope proposals accordingly; don't assume full-time Raj bandwidth.
- **Capstone review done (2026-08-02)**: Full confidence audit of every artifact in this workspace — see `docs/capstone-session.md`. `docs/objection-log.md` now carries a disclaimer that its Raj/Marcus/Tom objections are Claude-simulated pressure-testing, not real stakeholder statements. Two fixes were surfaced but **not yet applied** — pending your call: (1) the pilot dataset's retention rates (22-36%) were never reconciled against the company topline (44%→37%) quoted elsewhere; (2) `docs/open-questions.md` and a home for the day-7→30 durability workstream were recommended in `workspace-audit.md` but never built.

## The product
Nudge is a consumer personal finance app that helps people build better money habits. Users connect their bank accounts, see where their money is going, set savings goals, and get nudges to stay on track.

- Launched 4 years ago
- Series B funded ($42M)
- 2.1M registered users
- 340K monthly active users
- Growing 28% YoY on MAU

## My role
PM at Nudge, owns the Engage squad — everything related to keeping users active after they connect their first account: home feed, weekly money summaries, savings nudges, push notifications.

Triad: Raj (Senior Engineer), Lena (Product Designer), me.
Reports to: Marcus (Head of Product).

## The situation
Core acquisition funnel works — users sign up, connect a bank account, see their spending breakdown. Problem is what happens next: after the initial aha moment, a large portion of users go passive (open the app less, stop responding to nudges, eventually churn).

Marcus wants to understand why and what to do about it.

## Current initiative: Engage v2
Hypothesis: users go passive because the app stops feeling relevant after the first week. The initial spending breakdown is compelling, but after that Nudge hasn't given users a reason to come back that feels personal, timely, or actionable.

This quarter ran the full arc on that hypothesis: discovery → root-cause diagnosis against real data → a piloted fix → statistical pressure-testing → a PRD and adversarial review → a quarterly review deck for Marcus. Full history in `change_log.md`.

## Agent Stack
Three automated agents run against this workspace (full detail, data sources, and owners in `agents/registry.md`):
- **Metric Pulse** — nightly compute, Monday 8am Slack digest on 30-day retention by acquisition channel (organic/paid/referral), alerts at ±2pts week-over-week. `agents/metric_pulse.py`.
- **Anomaly-to-Hypothesis** — fires only when Pulse alerts, never on a quiet week. Decomposes the move via the metric tree (day-1→7, day-7→30, sessions, push open rate), ranks 3 hypotheses, writes confirmation SQL, posts to Slack. `agents/anomaly_diagnosis.py`.
- **Weekly Insight Report** — Friday 4pm, pulls retention metrics + `change_log.md` completions + NPS themes into a Done/Changed/Watch report, saved to `reports/YYYY-MM-DD.md` + Slack. `agents/weekly_insight.py`.

Chain today: Pulse → Anomaly (built, in-process function call). **Not yet connected**: Anomaly diagnoses don't feed into Weekly Insight's "Watch" pick yet — it still only scans `change_log.md` for keywords. See the Connection Plan in `agents/registry.md` for the scoped fix.

All three post to Slack via `SLACK_WEBHOOK_URL` and run manually today (dry-run by default) — none are on a live cron/n8n schedule yet. `agents/monday_retention.py` is an earlier prototype superseded by Metric Pulse, kept but not part of the active stack.

## Working files

**Core tracking**
- `project.md` — what Nudge is, squad, current phase, key stakeholders
- `strategy.md` — working hypothesis for recovering the retention drop, updated as evidence came in
- `change_log.md` — dated log of every milestone this quarter
- `workspace-audit.md` — gaps and reorganization notes from the last workspace review
- `docs/capstone-session.md` — full confidence audit of every artifact + reproducible workspace-setup prompt

**Research (qualitative)**
- `research/interview-synthesis.md` — synthesized themes from user interviews (Priya, Tom, Amara)
- `research/nps-analysis.md` — ranked themes and actionable issues from NPS feedback
- `research/competitive-matrix.md` — YNAB/Cleo/Monarch comparison and white-space gaps

**Data & experiments (quantitative)**
- `data/metric-findings.md` — real SQL analysis of retention + weekly summary A/B test data
- `data/metric-diagnosis.md` — metric tree, decline diagnosis, 4 ranked hypotheses for residual treatment churn
- `data/experiment-design.md` — significance check on the pilot + fully powered follow-up test design

**Feature spec & review**
- `docs/pm-brief.md` — PM brief for the weekly summary prototype
- `docs/spec-readiness.md` — skeptical-Raj gap review of the brief + proposed v1 scope
- `docs/design-review.md` — prototype review vs. interview evidence, highest-impact change, Lena vs. product-decision split
- `docs/qa-checklist.md` — edge case list, PM QA sign-off checklist, PR comment template
- `docs/prd.md` — 1-page PRD for Raj/Lena
- `docs/objection-log.md` — 3-persona pressure test of the PRD (Raj, Marcus, churned user Tom)

**Decisions & leadership comms**
- `docs/decision-brief.md` — 1-page synthesis and recommendation for Marcus
- `docs/recommendation-memo.md` — results memo for Marcus (revised: run full test first, not scale now)
- `docs/presentation.md` + `docs/presentation-notes.md` — 6-slide quarterly review deck + full speaker notes

**Working sessions**
- `docs/triad-session.md` — agenda + post-session alignment template for the Raj/Lena working session

**Reference**
- `docs/codebase-summary.md` — PM-level tour of maybe-finance/maybe (reference codebase)

**Prototype**
- `prototype/index.html` + `prototype/README.md` — clickable prototype for user testing

**Skills**
- `skills/weekly-status.md` — reusable skill: raw notes → team update + leadership update
- `skills/friday-status.md` — one-command Friday status, reads `change_log.md` directly, no pasted notes needed
- `skills/research-synthesis.md` — one-paste weekly synthesis of new feedback/tickets/NPS comments
- `skills/competitive-pulse.md` — one-command weekly web-search check on tracked competitors

**Agents**
- `agents/registry.md` — master registry of all agents (trigger, data sources, output, schedule, owner), connection plan, and 6-month roadmap
- `agents/monday_retention.py` + `agents/monday-retention.md` — verified weekly retention/session/open-rate digest script + spec, reads `data/nudge.db`, posts to Slack via `--post` (superseded prototype, not part of active stack)
- `agents/metric_pulse.py` + `agents/metric-pulse.md` — verified retention pulse with channel breakdown (organic/paid/referral) + alert threshold, reads `data/nudge.db`, posts to Slack via `--post`
- `agents/weekly_insight.py` + `agents/weekly-insight.md` — verified 3-2-1 weekly report (retention + change_log + NPS themes), saves to `reports/YYYY-MM-DD.md`, posts to Slack via `--post`
- `agents/anomaly_diagnosis.py` + `agents/anomaly-diagnosis.md` — chained to `metric_pulse.py`'s alert flag: metric tree decomposition → 3 ranked hypotheses → confirmation SQL, posted to Slack as a follow-up message

**Onboarding materials** (for a new teammate, not Nudge project work)
- `docs/onboarding-guide.md` — 1-page, 5-minute read: what Claude Code is, the 3 core habits, the most common mistake
- `docs/onboarding-demo-script.md` — 15-minute live demo script, ends with the teammate running their own first interview
- `docs/onboarding-slack-thread.md` — the original Nudge Slack thread that kicked off this workspace, saved for demo reuse

When something in the conversation would update one of these (a phase change, a new stakeholder, a hypothesis shift, a milestone worth logging) — or when a new tracking file should exist — proactively prompt to save/update it rather than waiting to be asked.

## Recap: what to hold onto every session
- Core metric: 30-day retention (44% → 37%)
- Open decision: pilot's day-7 win is significant, day-30 win isn't (yet) — running a fully powered test before recommending full-scale rollout
- Constraint: Raj's time is contended — scope accordingly
- Known gaps (see `docs/capstone-session.md`): day-7→30 durability has no owner or file yet; pilot dataset retention rates were never reconciled against the company topline; `docs/open-questions.md` still doesn't exist
