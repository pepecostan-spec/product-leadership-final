# Weekly Summary: Results & Recommendation — For Marcus

*Revised 2026-07-29 after statistically pressure-testing the pilot — see `data/experiment-design.md`. The original version of this memo recommended scaling now; that recommendation has changed.*

## Situation
We shipped the personalized weekly summary (top spending insight, one contextual nudge, savings goal progress) as a controlled test to a slice of new users (n=50/arm), to find out whether it addresses the 30-day retention decline (44%→37%) by giving users a reason to come back after the first-week aha moment fades. We've since run a formal significance check on the pilot and designed a fully powered follow-up test.

## Evidence
- **Day-7 retention lift is real and statistically significant**: 46.0% (control) → 76.0% (treatment), p=0.002 — the feature reliably fixes the early week-1 drop-off, which decomposition shows is where the underlying retention decline actually happens (`data/metric-diagnosis.md`).
- **Day-30 retention lift is not statistically significant at this sample size**: 22.0% → 36.0% looks large, but at n=50/arm the p-value is ≈0.12–0.19 — not distinguishable from noise. This was the number the original "scale now" recommendation rested on.
- **A fully powered test is fast and cheap**: detecting a 5-point lift at 80% power/95% significance needs ~1,200 users/arm and ~7 weeks — well inside our 8-week ceiling, and far cheaper than committing Raj's limited capacity to a full build on unproven evidence.

## Recommendation
Run the fully powered test (~7 weeks) before committing engineering resources to a full-scale rollout, while keeping the weekly summary live for the existing pilot users in the meantime.

## Ask
Approval to launch the ~7-week powered test now (sized to detect a 5pp lift at 80% power / 95% significance) rather than proceeding straight to full-scale rollout, and sign-off to keep the feature running for current pilot users while that test is in flight.

## Risk if we wait
The 7-week test itself adds little real delay — the bigger risk is on the other side: committing Raj's already-scarce engineering capacity to a full-scale build on a day-30 result that doesn't yet clear statistical significance, and discovering later it doesn't hold up at scale.
