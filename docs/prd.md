# PRD: Personalized Weekly Summary

*Audience: Raj, Lena. Sources: `research/interview-synthesis.md`, `research/nps-analysis.md`, `research/competitive-matrix.md`, `strategy.md`.*

## Problem Statement
30-day retention dropped from 44% to 37%. Users get real value from the initial spending breakdown, then the app goes static: no new insight, no clear next action, no reference to their own goal. Interviews and NPS data show the same pattern independently. No competitor (YNAB, Cleo, Monarch) solves this combination either — each is either effort-heavy, purely descriptive, or not goal-aware.

## User
A user in their first 30 days after connecting an account, before they've gone passive. Most at risk: users who haven't set a savings goal in week 1 — they churn at a meaningfully higher rate.

**Job to be done**: Tell me what changed with my money this week, and tell me one thing to do about it.

## Goals and Non-Goals

**Goals**
- Give users a reason to open the app weekly, tied to something specific about their own data.
- Give one clear action per week, not just information.
- Reference the user's own goal every time, not just at setup.

**Non-Goals**
- No ML-ranked insight selection in v1 — rules-based only.
- Nudge actions don't persist a real backend change in v1 — suggestion-only.
- Not solving day-7→30 retention. Diagnosis shows this feature only moves day-1→7; day-7→30 is flat regardless and needs separate work.
- No new data integrations — existing account data only.

## Success Metrics
- **Primary**: day-7 retention lift, treatment vs. control. Already significant in the pilot (p=0.002).
- **Secondary, not yet proven**: day-30 retention lift. Pilot number (22%→36%) isn't statistically significant at n=50 — a fully powered test (~1,200/arm, ~7 weeks) is running to confirm or reject it.
- **Leading indicators**: weekly summary open rate across sends (watch for the pilot's ramp-then-plateau pattern), nudge acted-on rate.
- **Guardrail**: notification opt-out rate must not increase — irrelevant nudges already cause opt-outs per NPS data.

## User Stories
1. As a user who hasn't opened the app in over a week, I get a weekly summary that tells me something specific about my spending, so I have a reason to come back.
2. As a user reading my weekly summary, I get one clear action to take, not just information, so I know what to do next.
3. As a user with a savings goal, I see my goal's progress in every summary, so the app doesn't feel like it forgot what I told it.
4. As a user with a quiet week (no notable insight), I still see something honest and useful, like a simple week-over-week comparison, rather than a forced or irrelevant nudge.
5. As a user, my nudges reflect my actual patterns, not random alerts, so I don't get frustrated and disable notifications.

## Open Questions
- What's the minimum data history required before a user is eligible for a personalized summary? Not yet defined — needs Raj's input.
- Does day-7→30 durability get its own feature/hypothesis, or does it ride on this roadmap later?
- Do we wait for the full-scale test (~7 weeks) before committing further engineering time beyond the current pilot?
- Should nudge actions ever persist a real backend change, or stay suggestion-only long-term?
