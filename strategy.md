# Strategy: Recovering the 7-Point Retention Drop

30-day retention dropped from 44% to 37% over the last two quarters. This document holds the working hypothesis — it is not a committed solution direction. Current phase is discovery; the open decision is to diagnose root cause before choosing a fix.

## Working hypothesis
Users go passive because the app stops feeling relevant after the first "aha moment." The initial spending breakdown is compelling, but after that Nudge hasn't given users a reason to come back that feels personal, timely, or actionable.

## Supporting signals (from team discussion, not yet validated as causal)
- Users who don't set a savings goal in week 1 churn at a meaningfully higher rate than users who do — ~1.6x higher at day 7, narrowing to ~1.2x by day 30 (validated against real retention data, see `data/metric-findings.md`; earlier "almost double" framing was an anecdotal read, accurate at day 7 but overstated by day 30).
- User research suggests people who connect their account and see the dashboard don't know what to do next — no clear next step after the spending breakdown.
- The home feed doesn't change based on recency of use — it looks the same whether a user last opened the app yesterday or three weeks ago.
- The weekly summary email has a 22% open rate, but the in-app experience doesn't continue the story the email started when users click through.

## Candidate direction (not yet decided)
A personalized in-app weekly summary screen has been floated — surfacing a top insight, one actionable nudge based on the user's own patterns, and progress toward their savings goal. Not scoped or committed; discovery work should confirm this addresses the actual root cause before any build decision.

## User research signal (2026-07-29)
Synthesis of 3 user interviews (`research/interview-synthesis.md`) adds texture to the working hypothesis, though sample size is small:
- Corroborates "no clear next step": both a churned user and a new user independently described being shown information (dashboard, spending breakdown) with no indication of what to do with it.
- Corroborates "static experience": both described the app looking the same on every visit, with nothing new since initial setup.
- New signal, not yet in the hypothesis: a single power user (18 months) reports that real personalization ("it knows my financial habits") only emerged after ~3 months of use, alongside a self-formed weekly ritual. Suggests there may be a real payoff on the other side of the passive period that the current experience fails to bridge users to before they churn — worth validating against actual cohort/retention data rather than one user's account.
- New signal, single data point: a churned user explicitly compared Nudge unfavorably to a competitor (YNAB) for being passive rather than "asking something" of him — frames the gap as passivity vs. prompting, not just staleness.

## NPS feedback signal (2026-07-29)
Analysis of 10 raw NPS comments (`research/nps-analysis.md`) independently corroborates the "no clear next step" and "static experience" signals above. Two new, concrete signals not previously captured:
- **Savings goal follow-through gap**: a user set a savings goal and the app never referenced it again — a specific, fixable defect rather than general staleness. Relevant given savings-goal-setting is already linked to lower churn in the team's own data.
- **Nudges driving notification opt-outs**: a user described nudges as feeling random (e.g., a $12 coffee purchase) and disabled notifications entirely as a result. Worth checking how widespread this is before leaning on push/notifications as the mechanism for any re-engagement fix — it could undercut a solution before it starts.

## Competitive context (2026-07-29)
Research on YNAB, Cleo, and Monarch Money (`research/competitive-matrix.md`) — the most relevant competitors on post-connection engagement — surfaces 2 white-space gaps, both based on public product documentation rather than hands-on testing:
- **Effort vs. prescription tradeoff**: every competitor reviewed sits on one side of a tradeoff — either real value requires ongoing manual effort (YNAB), or the experience is low-effort but only descriptive, not prescriptive (Monarch's weekly recap, Cleo's humor-driven nudges). None combine low-effort with telling the user a specific next action.
- **No sustained personal narrative**: even the best recap features (Monarch's weekly summary, Cleo's weekly chat review) are periodic report-outs, not an ongoing thread that references what the user has already told the app about themselves. This is the same gap as the savings-goal follow-through issue found in the NPS analysis — and it appears to be unsolved industry-wide, not just a Nudge problem.

Both gaps reinforce rather than replace the working hypothesis — they suggest the candidate direction (personalized weekly summary) should specifically aim for low-effort + prescriptive + goal-aware, since no competitor already owns that combination.

## Metric validation (2026-07-29)
Real SQL analysis of the actual retention/A-B-test dataset (`data/metric-findings.md`), not just qualitative signal:
- The pre-existing decline is real and monotonic (day-30 retention 32%→22% from cohort week 1 to week 4), and had plateaued around 22–25% without intervention — confirms this isn't noise and won't self-correct.
- Week-1 goal-setting is now confirmed against real retention data (see corrected ratio above), not just team anecdote.
- **Controlled test result**: in a live A/B test (cohort week 5, n=50/arm), the weekly summary lifted day-7 retention 46%→76% and day-30 retention 22%→36% (~1.6x at both checkpoints) versus control. Open rate rose 28%→52%→56% across the 4 weekly sends for the treatment group while control stayed flat at 4–6%, suggesting the behavior is habit-forming rather than a novelty spike.
- Caveat: single test cohort, n=50/arm, no formal significance test run — strong directional evidence, not a statistically certified result. Worth a larger/longer follow-up test before treating ~1.6x as a fixed expectation at full scale.

## Metric diagnosis: what the feature actually fixed (2026-07-29)
Decomposing 30-day retention into sequential stages (`data/metric-diagnosis.md`) reveals the fix is narrower than the topline lift suggests:
- **Day-1 activation is stable (~90-97%) across every cohort — never the problem.** The weeks-1-4 decline is entirely concentrated in the **day-1→day-7** transition (66.7%→47.8%, cohort over cohort). The **day-7→day-30** transition is flat (~47-53%) throughout.
- **The weekly summary fixes exactly the day-1→day-7 transition** (control 50.0% → treatment 86.4% in the week-5 test) **and has no measurable effect on day-7→day-30** (47.8% control vs. 47.4% treatment — within noise).
- Consequence: of the treatment users who still churned by day 30, 63% dropped in the day-7-to-30 window the feature doesn't touch. **The feature relocated where churn happens more than it eliminated churn.**
- Also found: churned and retained treatment users open/act on the weekly summary at nearly identical rates — engaging with the feature doesn't itself predict who stays, suggesting content relevance or follow-through (not just delivery/engagement) may be the next lever.

**Implication for the roadmap**: scaling this feature should close the day-1-7 gap at full scale, but a second, distinct problem — day-7-to-30 durability — remains completely unaddressed and needs its own hypothesis and likely its own solution, not just "more of the same feature."

## Statistical pressure-test — recommendation revised (2026-07-29)
Formal significance testing of the pilot (`data/experiment-design.md`) found the day-30 lift is **not statistically significant at n=50/arm** (p≈0.12–0.19) — only the day-7 lift clears significance (p=0.002). The day-30 number is what the "scale now" recommendation in `docs/decision-brief.md`/`docs/recommendation-memo.md` was resting on.

**Recommendation changed**: run a fully powered follow-up test (~1,200 users/arm, ~7 weeks — sized for MDE=5pp, 80% power, 95% significance, comfortably inside the 8-week ceiling) before committing engineering capacity to a full-scale build. Keep the feature live for existing pilot users in the meantime rather than rolling it back. `docs/recommendation-memo.md` has been updated to reflect this — it previously recommended scaling immediately.
