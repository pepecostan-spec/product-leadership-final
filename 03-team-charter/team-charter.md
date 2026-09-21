# Team Charter: Meridian Foundations

> Module 3 · Lead and Develop High-Performing Teams, ★ Deliverable 3
>
> Define how your team operates. Two completed components: **What We Own** and **How We Decide**.

## 1. What We Own

_The team's mandate: the outcomes and surfaces this team is accountable for end-to-end, and the explicit edges where your ownership stops._

| Area | We own it | We influence it (don't own) |
|---|---|---|
| Field capture experience | The offline-first mobile app (camera, voice, one-tap status) and its field UI | The enterprise desktop UI |
| Capture-to-record pipeline | Auto-tagging (geolocation, timestamp, OCR) and sync into the system of record | The core data model and RFI/cost-code schemas (core platform team) |
| Field adoption and rollout | Pilot playbook, champions, the validation checkpoint, and KR1–KR3 | Enterprise account strategy and renewals (sales, account management) |
| Field data for the office | Nothing beyond existing views | Manager dashboards and ERP/analytics (enterprise team) |

> Our mission in one line: Make Meridian the first tool superintendents and foremen reach for on the jobsite, without touching anything finance and compliance already rely on.

**Out of scope:** mid-market land-and-expand, ERP/analytics depth, a field-data manager dashboard, and rollout beyond the pilot accounts until the validation checkpoint passes. These come straight from the Module 1 and 2 hard nos.

## 2. How We Decide

_The team's decision-making operating model: the decisions you make, who makes each call, and how disagreements resolve._

| Decision type | Who decides | Who's consulted | How we break a tie |
|---|---|---|---|
| Feature and scope calls on the field surface | PM | Mobile eng lead, UX research, customer success | The OKR test: does it move KR1, KR2 or KR3? If still split, the PM decides |
| Technical approach (sync design, tagging models) | Mobile eng lead | PM | If a technical choice changes what ships or when, it becomes a scope call and the PM decides |
| Which accounts roll out, and when | Customer success lead and PM jointly | Account owners | Pilot checkpoint evidence |
| Anything touching the core platform or an enterprise contract | Joint call with the enterprise platform lead | Finance and compliance stakeholders | Escalate to the Head of Product. We never remove a feature finance or compliance uses |

> Our default: the PM decides scope; we escalate to the Head of Product when a call touches the core platform or a customer contract, or when a cross-team conflict isn't resolved in 48 hours. Escalations from outside the team are resolved by the Head of Product.

**Where this charter leaves room for conflict:** the line between "technical approach" and "scope" is the boundary the Module 3 exercise below diagnosed, and this charter now names it. The softer spot is "influence" on the core platform: nothing says how fast the platform team must respond, so field work could stall while we wait on them.

## 3. Module 3 lab guide exercise

_Difficult-conversation exercise from the Module 3 lab guide. The situation is invented and illustrative (an Amazon Key PM lead); it describes no real people._

**Name the situation.** I lead a team of three PMs on Amazon Key. A dotted-line program manager from the central launch-readiness org supports us. For about eight weeks, this PgM has been agreeing launch dates and dependencies directly with partner teams instead of going through the PMs who own those features. Two of my PMs have separately told me they find out about commitments in the weekly status doc. It has happened four times, and the dates were reasonable each time.

**Diagnosis.** A decision I made, not their behavior. At the start I told my PMs to "loop in the PgM" on launches and told the PgM to "drive readiness." I never said who owns launch-date commitments versus who owns the plan behind them. Nobody crossed a line I drew, because I never drew one.

**Opening line.**
- *One next action in the next two weeks:* Hold a 1:1 with the PgM first, then a 45-minute session with them and my PMs to agree a one-page decision-rights table covering launch dates, dependencies, and status.
- *First sentence of the conversation:* "I want to start with something I got wrong: I asked you to drive readiness and told my PMs to loop you in, but I never said who commits to a launch date, so the friction you've been running into is on me before it's on you."

**AI role-play: what changed.** The role-play showed me my opening line took responsibility but left the PgM with nothing to do next. Their first reaction was "what else was I supposed to do?", and I didn't have an answer ready. It also surfaced something I hadn't diagnosed: they set dates because the PMs weren't providing them and partner teams were waiting, so part of this is a PM responsiveness issue I need to address separately. For real, I'll keep the ownership, acknowledge that they were solving a genuine problem, and pair it with the proposal: PMs commit to dates, the PgM drives the process to get them.

## Link to full artifact

_[link to this deliverable in your repo]_
