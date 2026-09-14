---
name: weekly-status
description: Turn raw, unstructured weekly notes into status updates for two different audiences — a conversational team update (for peers like an engineer or designer) and a condensed leadership update (for a manager who wants the compressed version). Use this whenever the user pastes in rough notes, a brain dump, or messy bullets from their week and asks for a status update, weekly update, team update, leadership update, or something to send to their manager or team — even if they don't use the word "skill."
---

# Weekly Status Update

The same week needs to read differently depending on who's reading it. A teammate wants enough detail to know what's relevant to them and what's being asked of them. A manager wants the compressed version, fast, without padding. This skill produces both from the same raw notes.

## Input
Raw bullet-point notes covering what got done, what's in progress, what's blocked, and any context worth knowing — including things like people's schedules or who flagged what. Notes may be messy or out of order.

## Shared process
1. Sort every item into: Shipped, In Progress, Blockers, or Context (schedules, availability, who-said-what — not a deliverable itself, but it shapes how or when to deliver the update, e.g. a stakeholder being out).
2. Write in plain, declarative language — say what happened or what's true, not how it felt or how hard it was.
3. Keep names and specific asks intact. Don't anonymize "Raj flagged X" into "a blocker was identified" — the team update especially loses all its usefulness if it does that.
4. Don't pad either format to hit a fixed bullet count. If only one thing shipped, say one thing. If two in-progress items are related, combine them into one bullet rather than listing both.

## Format 1: Team Update
Audience: peers — an engineer, a designer, the immediate working group. Tone: conversational, specific, addresses people by name.

- Open with a one-line overview.
- Cover Shipped and In Progress in flowing sentences, not necessarily bullets — call out anything specifically relevant to a particular person as you go (e.g., "Lena, the prototype's live in Figma").
- State each blocker as a direct ask to whoever owns it, not a passive observation.
- Close with any logistics that affect the week — someone's availability, a scheduling constraint — so the team can plan around it.

## Format 2: Leadership Update
Audience: a manager who is busy and not close to the day-to-day. Tone: compressed, scannable, no elaboration.

Structure — shape flexes to what actually happened; don't force a fixed count:
```
# Weekly Status Update — [Date]

Shipped:
- [one bullet per genuinely shipped item]

In Progress:
- [condense related items into as few bullets as make sense — don't list every single one separately]

Blockers:
- [only the blocker(s) that actually affect timeline or need the reader's help — omit the section if there are none]

[One line]: a single sentence on overall status — on track, at risk, or blocked, and why.
```

---

## Example (Nudge Engage v2, this week)

**Input:**
- Interview synthesis complete (Priya, Tom, Amara)
- Competitive matrix done — 3 competitors, 2 white space gaps
- Prototype v1 live in Figma
- PRD first draft — 70% done
- Usability session scheduling — 3 of 5 confirmed
- Raj flagged the ranking logic needs a data backfill — estimate TBD
- Marcus out Thu–Fri, async review only

**Team Update output** (for Raj and Lena):
```
Hey team — quick rundown of where things stand.

Good progress this week: interview synthesis is done (Priya, Tom, Amara all synthesized),
and the competitive matrix is done too — landed on 3 competitors and 2 real white-space
gaps. Lena, the prototype v1 is live in Figma whenever you want to take a look.

Still moving: the PRD first draft is about 70% there, will share once it's in better shape.
Usability sessions are filling up — 3 of 5 confirmed, working on the last two.

Raj — flagging that the ranking logic needs a data backfill before we can move forward,
and we don't have an estimate yet. Let me know what you need from me to help size that,
since it'll affect the PRD timeline.

Heads up: Marcus is out Thu–Fri, async review only — plan around that if you're waiting
on a decision from him this week.
```

**Leadership Update output** (for Marcus):
```
# Weekly Status Update — [Date]

Shipped:
- Interview synthesis complete (Priya, Tom, Amara)
- Competitive matrix done — 3 competitors, 2 white-space gaps identified
- Prototype v1 live in Figma

In Progress:
- PRD first draft (70% done); usability testing on track with 3 of 5 sessions confirmed

Blockers:
- Ranking logic needs a data backfill before implementation — estimate still TBD from Raj

Where we stand: Discovery and design work are complete and usability testing is underway;
the main open risk is the ranking logic backfill timeline, which could affect the PRD and
build schedule.
```
