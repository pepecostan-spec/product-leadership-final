# Interview Synthesis — Nudge User Research

**Sources**: 3 user interviews
- Priya S. — Power user, 18 months on Nudge
- Tom R. — Churned user, left after 5 weeks
- Amara L. — New user, 10 days in

**Note on sample size**: 3 transcripts is a small, non-representative sample. Treat the themes below as directional hypotheses to validate further, not confirmed findings.

---

## Top 5 Themes

### 1. The experience feels static after initial setup
Once onboarding (connecting accounts, setting a budget, seeing the first breakdown) is done, both a churned user and a brand-new user report that nothing in the app visibly changes over time.

**Quotes:**
- "After the initial setup it felt like nothing changed." — Tom R.
- "The app just showed me the same dashboard every time." — Tom R.
- "I check it occasionally but nothing has changed since the first day." — Amara L.

*Supported by 2 of 3 users (Tom, Amara).*

### 2. Users don't know what to do with the insights they're given
Both Tom and Amara describe the same gap: the app surfaces information (a budget, a spending breakdown) but doesn't tell them what action to take next.

**Quotes:**
- "I kept waiting for it to give me something to act on and it never really did." — Tom R.
- "I do not really know what to do with that information." — Amara L.
- "I have been waiting for Nudge to tell me the next step." — Amara L.

*Supported by 2 of 3 users (Tom, Amara).*

### 3. Deep value (personalized pattern recognition) only emerges after sustained use
Priya's experience is qualitatively different from the other two: the product eventually started surfacing patterns specific to her behavior, but only after a long runway.

**Quotes:**
- "The thing that made it stick for me was when I noticed it started surfacing patterns I had not consciously registered — like that I always overspend in the last week of the month." — Priya S.
- "I feel like Nudge actually knows my financial habits now." — Priya S.
- "But it took about three months to get there and I think most people give up before that." — Priya S.

*Supported by 1 of 3 users (Priya) — single-source theme. The "three months" figure and the churn speculation are Priya's own belief, not measured data.*

### 4. Ritual and habit formation is what sustains long-term engagement
Priya's retention isn't driven by any single feature but by a repeated weekly habit that became self-reinforcing.

**Quotes:**
- "I open Nudge every Sunday morning before I start my week." — Priya S.
- "It has become a ritual." — Priya S.
- "Once I saw that I started planning around it." — Priya S.

*Supported by 1 of 3 users (Priya) — single-source theme. Notably, neither Tom nor Amara describe anything resembling a habit or routine.*

### 5. The initial spending breakdown is a strong hook, but momentum doesn't carry forward
The "aha" moment at signup is real and valuable, but it appears to be a one-time event rather than the start of an ongoing relationship.

**Quotes:**
- "The spending breakdown was shocking in a useful way — I had no idea I was spending that much on subscriptions." — Amara L.
- "I really wanted it to work." — Tom R.

*Only 2 verbatim quotes support this theme (Amara, Tom) — the transcripts don't give a third distinct quote on this point. Priya's transcript doesn't reference the initial breakdown at all.*

---

## Contradictions and Outliers

- **Central contradiction**: Priya describes Nudge as something that "knows" her and has become ritualized; Tom and Amara describe the same product as static and directionless. The most likely explanative variable in this sample is tenure (18 months vs. 5 weeks vs. 10 days) rather than a difference in the product itself — but with only 3 users, this is a hypothesis, not a confirmed causal link.
- **Outlier — competitive comparison**: Tom is the only user who directly compared Nudge to a competitor: "I switched to YNAB because at least that feels like it is asking something of me." This frames the problem as Nudge being *passive* where a competitor is *active/prompting* — a distinct angle from "static dashboard" that's worth probing in future interviews.
- **Unverified claim**: Priya's belief that "most people give up before" the 3-month mark is speculation from a single power user, not data. It should be checked against actual retention/cohort data rather than taken at face value.
- **Possible gap, not a contradiction**: Tom's transcript never mentions the spending breakdown specifically (he mentions connecting accounts and setting a budget), while Amara calls it out as a highlight. It's unclear whether Tom didn't have the same reaction, didn't think to mention it, or the onboarding experience differed for him — worth clarifying in future research rather than assuming either explanation.

---

## Implications for Open Decision (root cause of retention drop)

These themes line up closely with the working hypothesis already in `strategy.md` (app stops feeling relevant after the first week) and add texture:
- The problem isn't just "nothing new happens" — users specifically want to be told what to *do*, not just shown more data (Theme 2).
- There may be a real payoff waiting on the other side of the passive period (Theme 3, 4), but the current experience doesn't bridge users to it before they churn.
- Worth testing whether an active/prompting experience (vs. a dashboard users have to check) addresses the passivity complaint directly (Tom's outlier comparison to YNAB).
