# Design Review: Weekly Summary Prototype

*Reviewing `prototype/index.html` against evidence from `research/interview-synthesis.md`.*

## 1. User needs addressed well

**"Tell me what to do, not just what happened."** Tom: *"I kept waiting for it to give me something to act on and it never really did."* Amara: *"I have been waiting for Nudge to tell me the next step."* The nudge card gives one specific, single action ("Set $20 budget") directly on the summary screen — a direct answer to this complaint from both users.

**"The app never changes."** Tom: *"The app just showed me the same dashboard every time."* Amara: *"I check it occasionally but nothing has changed since the first day."* The home-feed entry point ("Your weekly money summary is ready") is explicit new content each week, deliberately shown against the muted static feed for contrast — targets this complaint directly.

## 2. User needs not yet addressed

**Nothing pulls a passive user back to see it.** Tom churned entirely; Amara only "check[s] it occasionally." The prototype's only entry point is a card on the home feed — which only reaches users who already opened the app. That's not the population that's actually at risk. The flow doesn't yet address *getting* a Tom or Amara back into the app in the first place, only what they'd see once there.

**Unproven: does the insight feel like it "knows" the user?** Priya's retention hinges on the app *"surfac[ing] patterns I had not consciously registered."* The prototype is a single scripted scenario (per `prototype/README.md`) — it demonstrates the interaction, not whether the underlying insight-selection logic can actually produce that quality of discovery, or whether it would just restate the obvious.

**Unproven: does this hold up over repeated weeks?** Priya's habit *"took about three months to get there."* A one-time test can't show whether the weekly insight stays compelling over time or becomes repetitive — the exact failure mode Tom and Amara already describe with the current product.

## 3. Highest-impact change for week-1 retention

**Add an active re-engagement trigger** (e.g., a notification) that surfaces the summary directly, rather than relying on the user to open the app and notice a card. The biggest gap above isn't what's on the screen — it's that Tom and Amara-type users don't reliably get to the screen at all. Fixing what's on the summary screen only helps users who are already opening the app; the retention problem is specifically about users who've stopped.

## 4. Lena's call vs. a product decision

**Lena owns**: visual/interaction execution — card styling and copy tone, the nudge confirmation's morph/animation treatment, information hierarchy on the summary screen, how the "new vs. static" contrast reads visually on the home feed, mobile ergonomics (tap targets, scroll).

**Requires a product decision, not design alone**:
- The re-engagement trigger mechanism (push vs. email vs. other) — has infra/privacy implications and directly touches the NPS finding that poorly-targeted nudges already cause opt-outs (`research/nps-analysis.md`); getting this wrong risks the same failure mode it's meant to fix.
- Insight-selection logic and the minimum-data ("cold start") threshold — already flagged as open in `docs/spec-readiness.md`, pending Raj.
- Whether nudge actions persist a real backend change or are suggestion-only in v1 — a scope call, not a styling one.
- What a user with no savings goal sees instead of goal progress — ties to the existing finding that goal-setting in week 1 roughly halves churn, making this a strategic call, not a UI fallback.
