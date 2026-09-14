# Nudge Engage v2 — Quarterly Review Deck (Narrative Structure)

*6 slides. Audience: Marcus. Supporting detail lives in the linked working docs — this deck is the compressed version.*

---

## Slide 1 — The Problem

**Headline number**: 30-day retention: **44% → 37%** (last two quarters)

**The one insight**: The decline isn't in acquisition — day-1 activation is stable at 90–97% every cohort. It's concentrated entirely in the first week after signup: users get real value from the initial spending breakdown, then the app goes static and gives them no reason to come back.

*Visual: a single big stat (44%→37%) next to the day-1 / day-7 / day-30 stage chart from `data/metric-diagnosis.md`, with the day-1→7 stage highlighted as where the decline lives.*

---

## Slide 2 — Why Now

**What changed**: We ran structured discovery this quarter — user interviews, NPS analysis, a competitive scan — and, critically, went back and diagnosed the decline against real retention data instead of relying on team anecdote.

**What we learned**:
- Users want to be told what to *do*, not just shown more data (interviews + NPS, independently).
- No competitor (YNAB, Cleo, Monarch) combines low-effort with prescriptive, goal-aware guidance — real white space, not a solved problem elsewhere.
- The decline is precisely where a candidate fix could plausibly work: the day-1→7 stage.
- We also found a second, separate problem — day-7→30 durability — that nothing yet addresses. Naming it now, not burying it.

---

## Slide 3 — The Proposal

**What it is**: A personalized weekly summary — one non-obvious spending insight, one contextual nudge, savings goal progress. In-app, low-effort, built entirely from data Nudge already has. Currently in QA.

**What it isn't**:
- Not an ML-ranked system in v1 — rules-based insight selection.
- Not a system that acts on the user's behalf yet — nudges are suggestion-only.
- Not a fix for day-7→30 durability — that's a separate, still-open problem.
- Not a new data integration — no new permissions or connections required.

---

## Slide 4 — Evidence

**Prototype**: Clickable prototype tested against the target persona (a user who connects an account and goes quiet within 2 weeks) — validated the interaction, not just the concept.

**User voice**:
- Tom (churned, week 5): *"I kept waiting for it to give me something to act on and it never really did."*
- Amara (10 days in): *"I have been waiting for Nudge to tell me the next step."*
- NPS respondent: *"I want Nudge to feel like a financial coach, not a spending tracker."*

**Data**: Pilot A/B test (n=50/arm) — day-7 retention 46%→76%, statistically significant (p=0.002). Day-30 retention 22%→36%, directionally strong but **not yet statistically significant** at this sample size. Open rate climbed 28%→56% across the 4 weekly sends while control stayed flat — looks like habit formation, not novelty.

---

## Slide 5 — The Plan

**Timeline**:
- Now: feature in QA; kept live for existing pilot users.
- Next ~7 weeks: fully powered follow-up test (~1,200 users/arm, sized for a 5-point MDE at 80% power / 95% significance) to confirm or reject the day-30 effect. Comfortably inside our 8-week window.
- After: scale decision based on the powered result; in parallel, scope a distinct initiative for day-7→30 durability.

**Milestones**: QA sign-off → powered test launch → weekly leading-indicator checks (day-7 retention, open-rate trend, opt-out rate) → results readout (~7 weeks) → scale decision.

**Risks**:
- The day-30 effect may not hold up at full power — that's exactly what we're testing for, not assuming.
- Engineering flagged the ranking logic needs a data backfill; estimate still TBD — could affect timeline.
- Notification opt-outs are a guardrail to watch — irrelevant nudges already cause opt-outs per our own NPS data.
- Standing constraint: engineering capacity is limited, so scope stays intentionally tight.

---

## Slide 6 — The Ask

1. Approval to run the ~7-week powered test rather than commit to a full-scale build now.
2. Keep the feature live for existing pilot users in the meantime — not rolling it back.
3. Sign-off that day-7→30 durability is a distinct, separate problem requiring its own future initiative — not something this feature already solves.
