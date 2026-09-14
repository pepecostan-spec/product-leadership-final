# Objection Log: Pressure-Testing the Weekly Summary PRD

*Reviewing `docs/prd.md` through three adversarial lenses before this goes further.*

> **Note on what this is**: The "Raj," "Marcus," and "Tom" objections below are Claude simulating those perspectives as a pressure-testing exercise, grounded in real project evidence (Tom's actual interview quotes, real diagnosis data, real constraints) — they are **not** verbatim statements the real Raj, Marcus, or Tom actually said about this PRD. Treat this as a checklist of questions worth asking the real people, not a record that they were already asked. If real feedback from any of them comes in later, it should supersede the corresponding simulated objection here.

---

## 1. Skeptical Raj — engineering effort, feasibility, scope creep

**Q1: Goal #3 says the summary references the user's goal "every time" — is that new logic, or just copy?**
The PRD's non-goals explicitly scope v1 as rules-based and suggestion-only, matching what was already agreed in `docs/spec-readiness.md`. But "reference the user's own goal every time" implies persistent state-tracking and querying on every generation — that's either already covered by existing goal-progress logic, or it's new scope that hasn't been estimated. Which is it?

**Q2: The cold-start threshold is still an open question — same as it was two documents ago. When does it get an owner and a deadline?**
`docs/spec-readiness.md` flagged this as unresolved before sprint kickoff. It's still listed as open in this PRD. That number determines who's even eligible for the feature, which determines what "day-7 lift" even means at full scale. Repeatedly re-listing it as "open" without a decision date isn't a spec gap anymore — it's a blocked estimate.

---

## 2. Skeptical Marcus — strategic fit, resourcing, opportunity cost

**Q1: This PRD's own non-goals admit it doesn't touch day-7→30 durability — and diagnosis shows that's 63% of remaining churn even in the treatment group. What's the actual ceiling on 30-day retention recovery here, and is that ceiling big enough to justify more of Raj's limited time?**
`data/metric-diagnosis.md` is explicit: the feature fixes day-1→7 and does nothing measurable for day-7→30. If most of the remaining problem lives in a window this feature can't touch, I need the real size of the win before committing more capacity — not just "it helped in the part it helped."

**Q2: We already agreed to wait ~7 weeks for a fully powered test before scaling. Is this PRD for what's already being tested, or for a new v1 that assumes the test succeeds?**
If the fully powered test comes back non-significant on day-30 — a real possibility, since the pilot's day-30 result wasn't significant either — does this PRD become moot? If so, why scope it now instead of after the test resolves?

---

## 3. Tom (churned user) — does this solve why I stopped?

**Q1: I made it 5 weeks in before I left. Your own data says this doesn't move day-7-to-30 retention at all. How does this stop someone exactly like me from leaving?**
Tom's actual tenure (5 weeks) places his churn inside the day-7→30 window — the exact window `data/metric-diagnosis.md` shows the feature has zero measurable effect on. The feature is built for a version of Tom who churns in week 1. The real Tom churned later, and this PRD doesn't claim to help him.

**Q2: I said I kept waiting for the app to give me something to act on — but if I'd already stopped opening it, how would I even see this?**
`docs/design-review.md` already flagged that the entry point (a home-feed card) only reaches users who still open the app. Tom's own words describe someone who stopped checking. Nothing in this PRD explains how a passive user gets pulled back to see the card in the first place.

---

## Most likely to kill the initiative if not addressed upfront

**Marcus's ceiling/opportunity-cost question (Q1).** It's the one objection with actual authority to end the initiative rather than just slow it down — Marcus controls resourcing, and Raj's capacity is the standing constraint on everything this squad does. It's also the one most reinforced by the other two: the diagnosis data backs it directly (63% of remaining churn is in the untouched window), and Tom's real churn story is a concrete, human instance of exactly that gap. If Marcus asks "what's this actually worth" and the honest answer is "a fix for a shrinking fraction of the problem," he may reasonably conclude Raj's time is better spent elsewhere — especially since the day-7→30 problem this doesn't solve may be just as large or larger.

**How to address it upfront**: don't let the PRD imply this feature solves the retention problem. State plainly that it closes a real, proven, statistically significant part of it (day-1→7), and that day-7→30 needs its own scoped initiative in parallel — set that expectation now, rather than letting Marcus discover the ceiling later and feel the scope was oversold.
