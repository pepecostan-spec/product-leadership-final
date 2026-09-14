# Spec Readiness: Weekly Summary — Skeptical Raj Review

**Spec under review**: `docs/pm-brief.md`, informed by `prototype/README.md`. This is a review of that brief through the eyes of a skeptical tech lead, before sprint kickoff.

---

## 1. Top 3 questions this spec doesn't answer

**Q1: What actually makes an insight "the top" insight?**
The brief says "top spending insight" as if selection is obvious. It isn't. Is it the largest dollar category? The biggest week-over-week change? The biggest deviation from the user's own rolling average? What breaks the tie if two candidates qualify? This is the core logic of the entire feature and it's currently undefined.

**Q2: How is the nudge chosen, and what happens when nothing qualifies?**
"One contextual nudge" implies a selection or generation process, but the brief doesn't say whether nudges come from a fixed template catalog, are dynamically generated, or something else — and it never addresses the case where no clear nudge-worthy condition exists that week. Is a nudge forced every time, or is "no nudge" a valid state?

**Q3: What's the minimum data needed to run this, and does the stated persona even clear that bar?**
The persona in the brief connected their account 2 weeks ago. The prototype's own insight ("$42 this week vs. your $14 usual") requires a historical baseline to compare against. With only 2 weeks of data, is there enough history to compute a reliable "usual"? The brief doesn't define a cold-start threshold, and the named persona may not clear it — which undermines the example the whole brief is built around.

---

## 2. What would resolve each gap

| Gap | What resolves it |
|---|---|
| Q1 — insight selection | A priority-ordered, deterministic list of insight types to evaluate (e.g., category spend vs. rolling average, new recurring charge, largest single transaction), plus an explicit tie-break rule. Also need a decision: rules-based v1 (fast, explainable) vs. ML-ranked (slower, needs training data) — given the capacity constraint, rules-based is the realistic v1 answer, but that's a call for Raj to confirm, not assume. |
| Q2 — nudge selection + fallback | A small fixed catalog of nudge templates, each mapped 1:1 to an insight type. An explicit fallback rule for weeks with no qualifying insight (recommend: show no nudge rather than forcing a generic one — a weak nudge is worse than no nudge, per the NPS finding that random-feeling nudges cause opt-outs). Also need to know whether accepting a nudge (e.g., "set a $20/week budget") persists a real change to the backend, or is suggestion-only in v1 — that determines whether this needs new write-paths, not just new read logic. |
| Q3 — cold start + trigger timing | A defined minimum history threshold (e.g., X weeks) below which a user doesn't get a personalized summary, or gets a simplified variant instead. Also need to define when this runs: a scheduled weekly background job for all eligible users, or computed on-demand when the user opens the app — this changes the infra shape, not just the logic. |

---

## 3. Rewritten spec — gaps filled (proposed, pending Raj's confirmation)

> Everything below is a **proposed default**, not a final decision — written to give the sprint kickoff conversation something concrete to react to instead of starting from a blank page. Items marked **[CONFIRM W/ RAJ]** are the ones most likely to change based on his input.

**Feature — Personalized Weekly Money Summary (v1 scope)**

- **Top spending insight**: Selected from a fixed, priority-ordered list of insight types, evaluated in order against the user's own trailing data — first qualifying insight wins:
  1. A spending category is >50% above the user's own trailing 4-week average for that category.
  2. A new recurring charge was detected this week that wasn't present in prior weeks.
  3. The single largest transaction of the week, if neither of the above qualifies.
  - **[CONFIRM W/ RAJ]** Rules-based selection for v1, not ML-ranked — chosen for speed and explainability given capacity constraints.
  - If no insight qualifies (e.g., a quiet week), fall back to a simple "total spend this week vs. last week" statement rather than forcing a stretch insight.

- **Contextual nudge**: A fixed catalog of nudge templates, each mapped 1:1 to one of the insight types above (e.g., category spike → "set a category budget" nudge). If no insight qualifies that week, **no nudge is shown** — a forced, low-relevance nudge is worse than none, per the notification-opt-out signal already found in `research/nps-analysis.md`.
  - **[CONFIRM W/ RAJ]** v1 nudges are suggestion-only: accepting a nudge (e.g., "set a $20/week budget") does not yet persist a real budget/goal change in the backend. It's tracked as an engagement signal, not a functional write. Making nudges actually do something is a v2 consideration, once we know the core loop works.

- **Savings goal progress**: Shown only if the user has an active goal. If they don't, this section is omitted entirely — not shown as an empty/zero state.

- **Constraint**: Use data Nudge already has — no new integrations. **[CONFIRM W/ RAJ]** Cold-start rule: users with fewer than [N — needs Raj's input on what's actually computable] weeks of transaction history do not receive a personalized summary in v1. Note this means the persona used throughout this brief and the prototype (connected 2 weeks ago) may be right at or below that threshold — needs explicit confirmation before we treat that persona as representative of who actually sees this feature at launch.

- **Trigger**: **[CONFIRM W/ RAJ]** Proposed as a scheduled weekly background job that generates the summary for all eligible users, rather than computed live when the user opens the app — flag if that assumption is wrong for infra reasons.

---

## 4. Slack message to Raj — proposing a scope constraint before sprint kickoff

---

Hey Raj — before we lock scope in the sprint kickoff, want to float a constraint given your bandwidth is already stretched thin:

Proposing v1 ships as **fully rules-based** insight and nudge selection (no ML ranking), with a **hard minimum-data threshold** for who's even eligible for a personalized summary, and nudges as **suggestion-only** — i.e., tapping "set a budget" doesn't persist anything to the backend yet, just logs that the user engaged. That should be enough to test whether the core loop (insight → nudge → goal progress) actually moves retention, before we invest in making nudges functionally do something.

Went through the brief like I was you, trying to poke holes — found 3 things it doesn't currently answer (insight selection logic, nudge fallback behavior, and cold-start data requirements — the test persona might not even clear the data bar we'd need). Wrote it up with proposed defaults so we're not starting from zero: `docs/spec-readiness.md`.

Can we grab 15 min async or sync before the session with Lena to confirm or adjust these before we walk in?

---
