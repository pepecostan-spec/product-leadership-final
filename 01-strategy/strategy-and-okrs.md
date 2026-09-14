# Product Strategy One-Pager & OKRs: Meridian Foundations

> Module 1 · Craft an Advanced Product Strategy, ★ Deliverable 1
>
> Your one spine: the **Playing to Win** cascade, one deliberate **hard no**, and an **OKR cascade** that flows directly from it.
> Draft the cascade + hard no in Sprint 1, then add the OKRs in Sprint 2. The goal: specific enough that a skeptical board member couldn't poke a hole in it.

## 0. Chosen scenario

**Path:** Meridian Foundations (B2B · adoption + expansion)

I picked Meridian over Fable because I wanted reps on a B2B trade-off I haven't led before: protecting a high-value enterprise contract while fixing an adoption gap at the frontline, rather than a straight consumer-retention problem.

## 1. Playing to Win cascade

| Question | Your choice |
|---|---|
| **Winning aspiration**: winning in the customer's terms, not internal metrics | Superintendents and foremen run the job, not paperwork about the job. The moment something happens on site — a delay, a defect, a safety call, a milestone hit — it's captured once, in the flow of the work, and instantly becomes protection (a documented record if it's ever disputed) and progress (visible to whoever needs to act on it) without the foreman ever having to sit down and "do the admin." |
| **Where to play**: segment, geography, channel, use case (the no's matter too) | Field crews (superintendents, foremen, crew leads) *inside Meridian's existing enterprise accounts* — the 38 of the top 100 US GCs already under contract. Not new-logo acquisition. Jobsite-native surfaces only: phone camera, voice notes, one-tap status — not the enterprise desktop workflow re-skinned for mobile. |
| **How to win**: your differentiator competitors can't easily replicate | Every mobile point solution and the group-text status quo still requires someone — usually a PM — to retype field data into the system of record later. Meridian's edge is closing that loop at the point of capture: a foreman's photo becomes a tagged, project- and cost-code-linked record automatically, with zero re-entry, so using Meridian is strictly faster than texting it and hoping someone catches it. |
| **Capabilities required**: what you must be world-class at (build / buy / partner) | Offline-first capture that syncs reliably on spotty jobsite connectivity; auto-tagging (project / RFI / cost-code) via geolocation, timestamp, and lightweight OCR so foremen never type metadata; a field UI designed and tested with actual supers and foremen, not a responsive shrink of the enterprise product; a trust-building rollout motion with field champions, since an earlier generation of "enterprise-first" tooling already lost this audience once. |
| **Management systems**: the metrics and rituals that reinforce your choices | Weekly field-adoption review per pilot account (active field users, % of updates captured natively vs. texted around), owned jointly by product and customer success; monthly rollup to leadership against the OKRs below; no roadmap capacity spent on enterprise-side requests that don't move field adoption until the metric moves. |

> **Where-to-play map** — Segment × role is a 2×2: enterprise/office (already won), enterprise/field (the gap, chosen), mid-market/office (eroding), mid-market/field (lost to point solutions). We picked enterprise/field because the contract's already won — this is a rollout problem, not a sales problem, sized right for a 10-person team. Within that: GC's own supers/foremen first (we can mandate training), not subs (no lever over them) or later; a dedicated app, not texting integration (unstructured, off-platform, can't sync offline).

> **Vision check** — Why now: field workflows have hardened around phone cameras/texts as mobile point solutions matured, while auto-tagging (geolocation, OCR, voice-to-text) only just got cheap enough to close the loop. Why us: we're the only player who owns the back-office system of record, so we're the only one who can kill the reconciliation tax instead of adding a second app to reconcile. Why us, now: team size fits an additive capture layer, not a rebuild — but only if leadership stops letting the enterprise-analytics camp pull roadmap capacity away from it.

## 2. Your one hard no

_One valuable thing you are explicitly choosing **not** to do, and why it protects the focus of everything above. This is a deliberate trade-off, not a backlog of deprioritized items._

> We will not build mid-market land-and-expand features — new-logo acquisition tooling, discounted packaging, or a lighter standalone product for $5M–$50M firms — as part of Foundations, because splitting a 10-person team across an unproven field-adoption bet and an unproven acquisition motion means we execute neither well. Mid-market churn is itself a symptom of the same field-adoption gap we're solving for inside our existing base first; winning the field comes before winning new logos.

## 3. OKR cascade

_One Objective and three Key Results that flow directly from the cascade. Each KR must be a measurable **outcome**, not an output/milestone._

> **Objective:** Make Meridian the first tool superintendents and foremen reach for on the jobsite — not the group text — across our enterprise accounts.
>
> - **KR1:** Weekly active field users (superintendents/foremen) as % of assigned field roles, across pilot enterprise accounts: 10% → 60% by end of Q1 2027
> - **KR2:** % of daily field updates (photos, status, RFIs) captured natively in Meridian vs. texted/emailed and re-entered later by a PM: 15% → 70% by end of Q1 2027
> - **KR3:** Median time from field event to system-of-record entry: ~18 hours (next-day PM transcription) → under 15 minutes by end of Q1 2027

## 4. AI pressure-test notes

_Run the devil's-advocate prompt (in the Sprint 2 guide). Capture the verdict._

| Prompt question | What the AI surfaced | Change or defend? |
|---|---|---|
| Biggest assumption that could be wrong | The plan assumes the adoption gap is *friction* (retyping is slow), not *incentive misalignment* — the cost of re-entry falls on the PM today, not the foreman, so a faster capture tool may not give the foreman any personal reason to switch. | **Change.** Don't treat "friction is the blocker" as settled — add an explicit pilot checkpoint after the first 1–2 accounts that checks *why* adoption is or isn't moving (qualitative check with supers, not just the usage number) before rolling out to the remaining accounts. |
| The board question I can't yet answer | What's mechanically different this time that stops supers/foremen reverting to texting once the pilot's novelty and champion support fade? | **Change.** Add a "sustain" checkpoint to the management system — re-measure adoption at 90 days *after* active rollout support ends per account, not just during the champion-supported pilot window. |
| KRs that are outputs in disguise | KR3 (time to system-of-record entry) is closer to a process/pipeline metric than a customer outcome, and it's gameable — a fast, empty placeholder entry would count. | **Change.** Tighten KR3's definition to only count *complete* entries (required fields + tag + photo/note), not any touch, so it can't be gamed independently of KR1/KR2. |
| The "no" I should reconsider | Sitting out mid-market for two quarters cedes ground to competitors actively converting former default-win accounts right now — and the brief never actually establishes that enterprise accounts are at churn risk, only that field adoption is low. | **Defend.** Keep the hard no. Splitting a 10-person team across two unproven motions means neither gets done well, and mid-market churn is a symptom of the same field-adoption gap — the capability built for enterprise is the same lever we'd eventually point at mid-market, so build it once, correctly, first. |
| Strategy or wish list? Why? | It's a strategy — real customers, a specific mechanism, a resourcing constraint, a defended trade-off — but it rests on an unvalidated assumption (friction vs. incentive) that nothing in the current plan tests before committing two quarters of the team to it. | The pilot checkpoint added above is what turns that gap from a blind spot into a managed risk. |

## 5. Self-diagnostic (6 questions)

- [x] **Clear**: a new PM could read it and know exactly what we will and won't do
- [x] **Names the real challenge**: the diagnosis is specific enough to be uncomfortable
- [x] **Makes a hard bet**: it says no to something valuable
- [x] **Cascadable**: teams can translate it into their own OKRs
- [x] **Coherent**: every choice reinforces the others
- [ ] **Committed**: resources are actually moving toward it — not yet true. The Vision check flags this directly: "why us, now" only holds if leadership stops letting the enterprise-analytics camp pull roadmap capacity away from Foundations. That's a real, unresolved fight, not a formality.
