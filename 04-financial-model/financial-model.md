# Financial Model: Meridian Foundations

> Module 5 · Master Product Financials & Strategic Bets, ★ Deliverable 5
>
> The business case for funding your bet, and the explicit kill criteria that would tell you to stop.

## 1. Business case

_Why this initiative is worth funding over the alternatives. Include the key unit economics assumptions, CAC, LTV, payback period, where relevant._

This is a retention-protection bet, not an acquisition funnel, so the table below replaces CAC/LTV with the assumptions that actually drive the return.

| Assumption | Value | Source / rationale |
|---|---|---|
| Retention-risk reduction from adoption | 10 points (15% → 5% non-renewal/downgrade risk) | Estimated — the assumption doing the most work in this case. Not yet measured; needs validation against real account-health data once the pilot runs. |
| Average enterprise contract value | ~$150,000/year | Order-of-magnitude estimate for a system-of-record used on $50M+ projects; pending confirmation from finance. |
| Baseline non-renewal/downgrade risk, low-engagement accounts | ~15% | Estimated from typical multi-persona-adoption retention patterns; validate against Meridian's own account-health data. |
| Investment required (Now horizon, 2 quarters) | ~$1.1M | 10-person cross-functional team (product, mobile engineering, UX research, customer success), fully loaded, for two quarters. |
| Expected return, at scale (Later horizon, ~12 mo) | ~$570,000/year ARR protected | 38 enterprise accounts × $15,000 expected value protected per account (10-point risk reduction × $150,000 contract value). |

> **The case in one paragraph:** Meridian Foundations is a defensive bet, not a growth bet — full-account adoption, not just office-role usage, is what typically holds an enterprise renewal together, so raising field-role WAU in existing top-100 accounts should reduce the probability a low-engagement account churns or downgrades at renewal. At scale, that's roughly $570,000/year in expected ARR protected against a ~$1.1M Now-horizon investment — about a 1.9-year payback through retention alone, with real but unpriced optionality if the mid-market hard no is later revisited. The whole case rests on one largely unvalidated number: a 10-point retention-risk reduction from adoption. If that number is actually 3–4 points instead of 10, expected value protected falls by 60–70%, which is exactly what the pilot and kill criterion below are built to catch before the Later-horizon rollout is funded.

## 2. Kill criteria

_The specific signals that would tell you this bet is no longer worth pursuing. Be explicit about the metric, the threshold, and the timeline._

> If, after the pilot (Now + Next horizons, ~6 months), field-role WAU has not reached 45% **and** pilot accounts show no measurable renewal-risk improvement relative to a matched non-pilot comparison cohort, we will not fund the Later-horizon full rollout, and will reallocate the mobile-engineering capacity to the enterprise-analytics roadmap instead. The comparison cohort is required deliberately: without one, a rising WAU number could reflect general account health improving for unrelated reasons, not the feature — the same measurement gap flagged in the Part 1 evaluation above.

## 3. Module 5 lab guide exercise: evaluate a sample case

_Critique exercise from the Module 5 lab guide, evaluating a separate hypothetical Meridian bet (not the Foundations field-adoption initiative) before building the business case below._

**The sample case.** Meridian builds an AI-assisted bid estimation layer into the Standard tier, reducing time-to-quote for project managers by 20%. Assumptions: Standard-to-Enterprise upsell improves from 6% to 8% within two quarters; average Enterprise contract $28,000/year; annual Enterprise churn 12%; Standard CAC $620. Expected return: 8% across 400 Standard accounts = 32 upsells in Year 1, $896,000 incremental ARR; payback for the $180,000 feature build: 2.4 months. Kill criterion: if upsell has not reached 7% by end of Q3, the feature is paused and Q4 engineering capacity reallocated before headcount is committed.

**What assumption is doing the most work?** The upsell-rate lift (6% → 8%) — every other number is a mechanical multiplication of that one percentage. If it's 20–30% off, the incremental accounts don't drop proportionally; they drop much further, because the baseline 6% (24 of 400 accounts) would have upsold anyway. A 25% miss on the lift itself could wipe out most of the claimed incremental value, since the case rests on a thin 2-point delta, not the 8% headline rate.

**The structural problem.** The model counts all 32 upsells (8% of 400) as incremental ARR from the feature. But 24 of those accounts (the 6% baseline) would have upgraded with no AI feature at all. The feature can only be credited with the delta: 8 accounts × $28,000 = $224,000 in truly incremental ARR, not $896,000 — roughly a 4x overstatement. Rerun on the real number: $180,000 ÷ $224,000 ≈ 9–10 months payback, not 2.4. CAC and churn are listed as "key assumptions" but never enter the calculation anywhere — decoration that makes the case look more rigorous than it is.

**Is the kill criterion complete and actionable?** Structurally yes — it names the metric, threshold, date, and a real consequence (feature paused, capacity reallocated before headcount is committed), not a decision handed back to the room. But it inherits the same flaw as the headline number: it triggers off the gross Standard-to-Enterprise rate, not a feature-attributable lift. With no control cohort or trend-adjusted baseline, normal quarter-to-quarter variation in the existing upsell motion could clear (or miss) 7% for reasons unrelated to the feature.

**Verdict: FUND WITH ONE CONDITION.** The underlying bet is still probably worth funding — a ~9–10 month payback on a $180K build is reasonable even after correcting the math. The condition: rebuild the model and the kill criterion around the incremental lift attributable to the feature (a holdout cohort or trend-adjusted baseline), not the gross conversion rate. As written, the case could pass its own kill criterion for reasons that have nothing to do with what was actually built.

## Link to full artifact

_[link to this deliverable in your repo]_
