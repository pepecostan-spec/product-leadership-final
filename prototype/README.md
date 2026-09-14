# Prototype: Personalized Weekly Money Summary

## What this is
A clickable, single-file HTML prototype of the Engage v2 candidate feature, built for a user test with someone matching the target persona: a 28-year-old who connected a Chase account 2 weeks ago and hasn't opened Nudge since.

**Job to be done being tested**: understand where their money went this week, and take one action.

## How to run it
Open `index.html` directly in any browser — no server, no build step, no dependencies. Works on desktop (rendered inside a phone-frame mockup) or on an actual phone browser.

To reset between test participants, click **"Restart flow"** above the phone frame.

## The flow
1. **Home feed** — a "Your weekly money summary is ready" card represents the new Engage v2 entry point (distinct from today's static feed, shown muted below it for contrast).
2. **Weekly Summary screen** — the three required elements:
   - **Top spending insight**: coffee spend this week vs. the user's usual (a stat tile with a two-bar comparison).
   - **Contextual nudge**: a specific, single action tied to the insight ("Set a $20/week coffee budget"), framed against the user's savings goal.
   - **Savings goal progress**: a progress meter for "Emergency Fund" with this week's contribution.
3. **Action taken**: tapping the nudge's CTA morphs the card into a confirmation state — this is the "take one action" moment.

## What's fabricated
Everything on screen is scripted sample data, not connected to any real account or backend:
- A 2-week transaction history for a persona named "Alex" (coffee spend spike, groceries, gas, a round-up transfer).
- One savings goal ("Emergency Fund," $640 of $3,000).
- The insight, nudge copy, and goal numbers are hardcoded — there's no logic that would generalize to a different user or week.

## Known limitations
- Single scripted scenario only — doesn't handle other spending patterns, no goal, or a different persona.
- No real Chase/Plaid data — this only demonstrates the UI/interaction, not feasibility of the underlying insight-ranking or nudge-generation logic (that's a separate, unanswered question for Raj).
- "Not now" (dismissing the nudge) just dims the card — there's no alternate flow built for that path.
- Not wired to any analytics — it's for a moderated user test, not instrumented self-serve testing.

## Why this exists
This prototype exists to get a reaction from someone matching the target persona before committing engineering time to the real feature — see `docs/decision-brief.md` and `strategy.md` for the research and reasoning behind this direction.
