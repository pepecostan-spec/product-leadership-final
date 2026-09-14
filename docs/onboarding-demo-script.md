# 15-Minute Live Onboarding Demo Script

*Goal: by minute 15, your teammate is running their own first Claude Code session — not watching you run yours. Have `docs/onboarding-guide.md` open for them to skim beforehand if there's a spare minute.*

**Before you start**: have this Nudge workspace open in a terminal, and know where you'll create a brand-new empty folder for step 4.

---

## Minutes 0-2 — Open the folder, show what Claude already knows

1. In the terminal, `cd` into the Nudge workspace folder and run `claude`.
2. Let them watch it start up. Say out loud: "The first thing it does is read a file called CLAUDE.md in this folder — that's the persistent memory for this whole project."
3. Ask Claude, live, in front of them: **"What's our core metric and what's the current open decision?"**
4. Point at the answer and say: "I never told it that in this conversation — it already knew, because it's written down in CLAUDE.md and it reads that file every single time, automatically." This is the entire point of the habit: nothing has to be re-explained.

## Minutes 2-7 — Run the AI interview, show plan mode

1. Say: "Now I'll show you how this workspace got started in the first place — with an interview, not a one-line request."
2. Open `docs/onboarding-slack-thread.md`, and paste its contents into a **new** Claude Code conversation (a fresh session, not this loaded one — you want them to see the *before* state) along with an instruction like: *"Here's a Slack thread from my team. Before you create any files, interview me — ask one question at a time until you're confident you understand what I need."*
3. Let Claude ask its first question. **Hand it to your teammate here** — let them answer one or two of the interview questions themselves, out loud, so they feel what the back-and-forth is like.
4. When Claude summarizes what it understood and presents a plan before writing anything, pause and point at it: "This is plan mode — it stops and shows me what it's about to do and waits for a yes before touching any files. Nothing gets built on a guess."
5. Say the punchline: "Notice it didn't write a single file until it understood the actual situation. That's habit #2 from the guide."

## Minutes 7-12 — Run the weekly status skill, then hand over the keyboard

1. Back in the main Nudge session, say: "Here's a different kind of thing this setup can do — turning your messy weekly notes into a real update, using a skill we saved once and reuse every week."
2. Paste a short example of raw notes (make one up on the spot, 4-5 bullets: something shipped, something in progress, one blocker) and ask Claude to turn it into a status update.
3. Point out the two outputs it produces: a conversational version for teammates, a compressed version for a manager. Say: "This is `skills/weekly-status.md` — a process we wrote out once and now just point Claude at."
4. **Hand them the keyboard now.** Have them paste 3-5 real bullets about their own actual week — whatever they're genuinely working on — and run it themselves.
5. Let them read their own output. This is the first thing in the demo they made happen, not just watched.

## Minutes 12-15 — They start their own workspace

1. Say: "Last thing — let's set up your own version of this, for your own work, right now."
2. Have them create a brand-new, empty folder for their own product/project and open a terminal there.
3. Have **them** run `claude` and paste in the reusable setup prompt below — typing/pasting it themselves, not you.
4. The moment Claude asks its first interview question back, stop narrating. Let them answer it themselves. The demo ends here, with them mid-interview in their own workspace.

---

## The reusable setup prompt (have them paste this)

```
I'm a PM working on [PRODUCT NAME] — [one-sentence description of what it does].
I want to set up a persistent working directory with you as my thinking partner
across many sessions, not just this one conversation.

Before you create any files or write any code, interview me. Ask me one question
at a time until you have 95% confidence you understand what I actually need — not
just what I said. When confident, summarize what you've learned and wait for my
approval before proceeding.

Cover at minimum: my role and team, the product and its core metric, the key
tension I'm navigating, the open decision I need to resolve, and any constraints
that should load every session (team capacity, deadlines, things already ruled
out).

Once I approve, set up:

1. A root CLAUDE.md that becomes the always-loaded context file. Structure it
   with the most load-bearing facts (core metric, open decision, standing
   constraints) at the TOP under a "Right now" section AND repeated compactly
   at the BOTTOM under a "Recap" section — model attention degrades on info
   buried in the middle of long context, so the critical stuff goes at both
   ends. Also include: the product, my role, the situation, and a "Working
   files" list grouped by category (not one flat list) as the workspace grows.

2. Root tracking files: project.md (what the product is, squad, current phase,
   stakeholders), strategy.md (working hypothesis, updated in place as evidence
   comes in — never delete old reasoning, append dated sections instead),
   change_log.md (dated log of every milestone).

3. Folder structure as work happens, not upfront:
   - research/ — qualitative discovery (interviews, NPS, competitive research)
   - data/ — quantitative analysis (real SQL/stats, not estimates)
   - docs/ — specs, decision briefs, PRDs, QA checklists, leadership decks
   - prototype/ — any clickable prototypes
   - skills/ — reusable workflows I ask you to productize
   - agents/ — any automation scripts, with a spec file alongside the code

4. A standing instruction in CLAUDE.md: whenever something in our conversation
   would update one of these files (a phase change, new stakeholder, hypothesis
   shift, milestone worth logging), proactively ask whether to save/update it
   rather than waiting for me to ask. Always ask before writing to change_log.md
   or CLAUDE.md specifically — don't auto-save those.

5. Ground everything in evidence, not invented detail. If I give you raw data
   (a spreadsheet, a Slack thread, interview transcripts), analyze the real
   thing — don't estimate when you could compute. If something is a small
   sample or unverified, say so explicitly in the document rather than implying
   more confidence than the evidence supports. If you simulate a stakeholder's
   perspective (a skeptical engineer, a churned user) for pressure-testing,
   label it clearly as simulated, not real feedback.

Start by asking your first interview question.
```
