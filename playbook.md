# The Claude Code Playbook for PMs

*Built from running the complete Claude Code workflow — discovery, research, prototyping, data analysis, communication, and a connected agent stack — on a real product initiative, then generalized so it works for any project you bring to it, in any company, starting tomorrow.*

---

## Part 1: The Mental Model

### Chat vs. Code
Claude.ai (chat) is conversational and stateless — you get text back, you copy-paste it, nothing touches your files. **Claude Code** operates directly on a project: it reads your files, writes new ones, runs commands, and remembers what it did *within* a session. Use chat to think through a problem; use Claude Code to actually produce and maintain the artifacts.

### Skill → Agent → System — one ladder, two questions
Every automation you build is one of these three things. The only difference between them is **when it fires** and **where the output goes**.

| | What it is | Example |
|---|---|---|
| **Skill** 🍳 | A recipe card — you pick it up and run it when you want it | A prompt that turns raw notes into a formatted status update; anything you paste and run |
| **Agent** 🚚 | A skill + a trigger + a destination — runs on a schedule or event, whether you're there or not | A nightly metric check that posts a Monday digest to Slack; a Friday summary saved to a versioned file |
| **System** 🍽️ | Multiple agents, coordinated, sharing context — one change updates all | A monitoring agent detects a threshold breach → a diagnosis agent fires automatically → a shared registry keeps them aligned |

**The jump from skill to agent is just: add a trigger (when) + a destination (where). That's it.** You don't need new skills to get from a recipe card to a running kitchen — you need a schedule and a place for the output to land.

### The three-part shape of every agent
1. **What watches** — the trigger: a schedule, an alert, an event.
2. **What it does** — the action: reads data, runs a query, writes a summary.
3. **Where it lands** — the destination: Slack, a versioned file, an email.

---

## Part 2: The Habits That Actually Matter

These are the load-bearing habits. Everything else in this playbook is detail; these are the ones that determine whether your Claude Code practice compounds or stalls.

1. **Interview before build — every time, no exceptions.** Never let Claude create files or write code until it has interviewed you about what you actually need. One question at a time, not ten at once — sequential questioning forces real answers instead of shallow ones. This is the single most important habit in the entire practice.
2. **95% confidence, not "got the gist."** Claude should keep asking until it can describe back what you need, not just repeat what you said. "Build a status tool" → confirmed as "for the engineering team specifically, not leadership" is the difference between output you use and output you rewrite.
3. **Plan mode is your last cheap edit.** After the interview, Claude should summarize the plan and wait for your approval before touching a single file. Read it carefully — catching a misunderstanding here costs a sentence; catching it after the build costs an hour.
4. **CLAUDE.md is persistent memory — session memory isn't.** Everything Claude learns in a conversation disappears when you close the terminal, unless it's written into CLAUDE.md. Update it at the end of every session — two minutes now saves ten minutes of re-explaining next time. **A stale CLAUDE.md is worse than none** — Claude will confidently work from outdated context and you won't know why the output feels off.
5. **Ground everything in evidence, not invention.** If a file you expect doesn't exist, or a number in your data doesn't match an example you were given, say so — don't paper over the gap or quietly conform the output to what was "supposed" to happen. This one is easy to state and easy to skip under time pressure; don't skip it.
6. **Save everything, and let Claude prompt you to.** Tell Claude explicitly: proactively ask before saving to your core tracking files, and don't wait to be asked when something in conversation should update a file. This is what turns "we talked about it" into "it's in the workspace."
7. **Run it by hand before you schedule it.** Never put an agent on a cron job or n8n trigger you haven't run manually and inspected first. The manual run is your quality check — if the output is wrong, you want to find that out yourself, not via a 6am Slack message that's wrong in front of your team.

---

## Part 3: The File Architecture

Build this as you go — don't create every folder on day one. Only add structure you'll actually maintain.

```
your-project/
├── CLAUDE.md              # Persistent memory — loads every session
├── project.md             # What the product is, your squad, current phase
├── strategy.md            # Your current best-guess hypothesis, updated as you learn
├── change_log.md          # Dated log of decisions, pivots, what you ruled out and why
├── research/              # Qualitative: interviews, feedback themes, competitive matrix
├── docs/                  # Specs, decision briefs, PRDs, QA checklists, presentations
├── prototype/             # Clickable prototypes + the PM brief that produced them
├── data/                  # Quantitative: SQL findings, metric diagnosis, experiment design
├── reports/               # Versioned output from scheduled agents, one file per run
├── skills/                # Reusable SKILL.md files — recipe cards you run on demand
└── agents/                # Agent specs + scripts — scheduled or event-triggered
```

### Why it's shaped this way

The structure answers two independent questions — get these right and the rest follows: **how often does this need to load automatically?** and **what kind of thinking produced it?**

**Axis 1 — load frequency.** CLAUDE.md loads into *every* session, automatically, before you've said a word. Everything else loads only when something references it. This isn't a style preference — it's a real cost. If your entire research history and every past decision lived in CLAUDE.md, every session would spend context re-reading things irrelevant to today's task before you'd asked a single question. Worse, attention degrades on information buried in a long file, so a bloated CLAUDE.md doesn't just waste space — it makes the facts that actually matter (your core metric, your open decision) harder to weight correctly. Keep CLAUDE.md to what you'd otherwise have to re-explain from scratch; let everything else earn its way in by being referenced when relevant.

**Axis 2 — kind of thinking.** Each folder answers a different question, so you can tell how much to trust something, or where to go looking for it, just from the folder name:
- **research/** — qualitative, interpretive (interviews, feedback themes, competitive gaps). Confidence here is inherently softer — themes and judgment calls, not arithmetic.
- **data/** — quantitative, computed (real queries, metric diagnosis, experiment design). Confidence here is checkable — you can re-run the query.
- **docs/** — synthesis *for humans* (specs, briefs, decks, QA checklists), built by reading research/ and data/, not by re-deriving facts independently. This layer should almost never disagree with the two beneath it, because it's supposed to be downstream of them.
- **prototype/** — the thing people can click, kept separate from the document describing it.
- **skills/ vs. agents/** — easy to conflate, but they answer different questions: skills/ is "what one-off workflows do I have that I run by hand," agents/ is "what's running on its own, on a schedule, whether I'm there or not." Same underlying idea — a reusable recipe — but a different question when you're scanning the folder.
- **reports/** — versioned, dated, never overwritten. The value of a weekly report isn't the latest one — it's having *all* of them, so a trend becomes visible three months in. Overwrite the folder and you've destroyed the thing that made automating it worthwhile.

**Why three core files instead of one.** project.md (what's true now), strategy.md (your current best-guess reasoning), and change_log.md (an append-only history of how you got here) are separate for the same reason a database keeps current state separate from its event log. Mix them and you either scroll through months of pivot history to find out what the product *is* today, or you lose the ability to answer "why did we abandon that direction" because the old reasoning got overwritten instead of logged.

**The retrofit trap.** Structure is cheap to get right at the start and expensive to fix later. It's common for a `docs/` folder to grow into a dozen files spanning specs, memos, QA checklists, and decks — genuinely mixed purposes in one flat folder — and by the time that's obviously messy, those files often cross-reference each other by relative path. Reorganizing at that point means either rewriting every link at once or leaving the mess in place. Loosely deciding the folder architecture in your first session is what avoids paying that cost later.

**Loading pattern**: CLAUDE.md loads automatically — keep it tight, only what Claude needs *every* session. Research and docs load on demand when relevant. Skills and agents load only when triggered. Don't cram everything into CLAUDE.md just because it's important; that defeats the point of the other folders.

**The cold-start test**: open a fresh session. Does Claude know the product, the current state, and the open decision without you saying anything? If yes, your workspace is working. If no, something's missing from CLAUDE.md — run the workspace-audit prompt (Phase 6.1 below) and fix it. Run this test after every CLAUDE.md update.

**CLAUDE.md structure that survives long sessions**: put the most load-bearing facts (core metric, open decision, standing constraints) at the very **top** under a "Right now" section, *and* repeat them compactly at the **bottom** under a "Recap." Model attention degrades on information buried in the middle of a long file — bookending the critical facts is a cheap, real hedge against that.

---

## Part 4: The Phases, and the Prompt for Each

This is the reusable core. Replace `[bracketed]` content with your actual project's details. Everything else — the structure of the ask, the "don't invent," the save path — carries over as-is.

### Phase 0 — Get Oriented

**0.1 Turn messy notes into a PRD skeleton** (works from a Slack thread, a meeting transcript, an email chain — anything unstructured)
```
Here is [a Slack thread / messy notes] from a product discussion at my company.
Please organize this into a PRD skeleton with the following sections: Problem
Statement, Goals, Non-Goals, and Success Metrics. Keep it concise — this is a
starting point, not a finished document. Do not invent details that are not
in the source.

[paste the raw material]

Save the skeleton to project.md.
```

**0.2 The AI interview + CLAUDE.md setup** (run this before anything else on a new project)
```
I'm a [role] working on [product] — [one-sentence description]. I want to set
up a persistent working directory with you as my thinking partner across many
sessions, not just this one.

Before you create any files or write any code, interview me. Ask me one
question at a time until you have 95% confidence you understand what I
actually need — not just what I said. When confident, summarize what you've
learned and wait for my approval before proceeding.

Cover at minimum: my role and team, the product and its core metric, the key
tension I'm navigating, the open decision I need to resolve, and any
constraints that should load every session.

Once I approve, write a CLAUDE.md (top+bottom structure per Part 3 above),
and set up project.md / strategy.md / change_log.md.

Proactively prompt me to save/update any of these when something in our
conversation would change them — don't wait for me to ask. Always ask before
you actually write to change_log.md or CLAUDE.md, though — don't auto-save
those.

Ground everything in evidence, not invented detail. If you simulate a
stakeholder's perspective for pressure-testing, label it clearly as
simulated, not real feedback.

Start by asking your first interview question.
```

**0.3 Build your first reusable skill**
```
Help me build a reusable SKILL.md file for [recurring task, e.g. weekly status
updates].
The skill should:
- Accept [raw input format] as input
- Output [specific structured format]
- [any constraints — length caps, tone, sections]
Save it as skills/[name].md
```

### Phase 1 — Know Your Users

**1.1 Interview synthesis**
```
Here are [N] user interview transcripts. Please:
1. Identify the top 5 themes across all of them
2. Extract the 3 best verbatim quotes per theme
3. Note any contradictions or outliers
4. Produce a structured insight synthesis document

[paste transcripts]

Save to research/interview-synthesis.md.
```

**1.2 Large feedback sets (NPS, support tickets, reviews)**
```
Here is a set of raw [NPS feedback / support tickets / reviews]. Please:
1. Extract all themes mentioned more than once
2. Rank by frequency
3. Separate praise from complaints
4. Identify the top 3 actionable issues
5. Produce a findings report I can share with [stakeholder]

[paste feedback]

Save to research/nps-analysis.md.
```

**1.3 Competitive research** (Claude searches the web itself)
```
[Product] is a [category] focused on [core problem]. Search the web and
identify the 3 most relevant competitors. For each: core features, pricing
model, target customer, how they solve [core problem], notable recent
changes.

Then produce a comparison matrix and identify 2 gaps none of them are owning
well — the white space for [your initiative].

Save to research/competitive-matrix.md.
```

**1.4 Decision brief** (chains everything above)
```
Here are my research outputs:
- Interview synthesis: research/interview-synthesis.md
- Feedback analysis: research/nps-analysis.md
- Competitive matrix: research/competitive-matrix.md

Synthesize into a 1-page decision brief for [stakeholder]:
- Situation (2 sentences)
- Key Findings (max 5 bullets)
- Options Considered (2-3)
- Recommended Action (1 sentence)
- Why Now

Save to docs/decision-brief.md.
```

### Phase 2 — Build and Learn Fast

**2.1 Prototype from a PM brief** (always run the interview first)
```
I want to build a working prototype. Here is my PM brief:
User: [who]
Job to be done: [what they're trying to accomplish]
Feature: [what it shows/does]
Constraint: [technical or scope constraint]

Before you build anything — interview me. Ask one question at a time until
you have 95% confidence you understand what I need. When confident, show me
the plan and wait for my approval.

Save the brief to docs/pm-brief.md, and once I approve, save the prototype
to prototype/index.html and a readme to prototype/README.md.
```

**2.2 Usability iteration** (one change per round — resist fixing everything at once)
```
I just ran usability sessions on my [feature] prototype. Here are my
observations:
[paste session notes]

Please:
1. Identify what is working
2. Identify the top 2 friction points
3. Suggest the single highest-priority change to make before the next round
4. Update the prototype with that change

Save a session log to docs/iteration-log.md.
```

**2.3 Hypothesis statement** (the format matters — every word should be load-bearing)
```
Read iteration-log.md and decision-brief.md. Write a learning synthesis
(what we know, what we assume, what we still don't know) and a hypothesis
statement in this format:
"We believe that [feature] will [outcome] for [users] as measured by
[metric]."

Save to research/hypothesis.md.
```

**2.4 Stakeholder working session prep**
```
I have a prototype tested across multiple rounds. I'm about to share it with
[names/roles] in a [N]-minute working session.

Help me:
1. Write the session agenda — what to show, what questions to ask, what
   decisions we need to walk out with
2. Draft the post-session alignment doc template
3. Write the message inviting them to the session

Save the agenda and template to docs/triad-session.md.
```

### Phase 3 — Work With Your Team

**3.1 Codebase tour** (a PM-level map, not a code read)
```
Give me a PM-level tour of [repo URL], and help me answer:
1. What this product does in one sentence
2. How the codebase is organized — what each major folder does
3. The 3 most important files I should know about
4. The key data models and what they tell me about product decisions
5. What I'd need to understand to write a good ticket for [upcoming feature]

Save your summary to docs/codebase-summary.md.
```

**3.2 Spec readiness** (play the skeptical engineer before your actual engineer has to)
```
I'm working with my tech lead on [feature] spec. Please:
1. Play a skeptical engineer — identify the top 3 questions this spec does
   not answer
2. For each gap, suggest what information would resolve it
3. Rewrite the unclear sections with those gaps filled
4. Draft an async message proposing a scope constraint before sprint kickoff

Save to docs/spec-readiness.md.
```

**3.3 Design review** (grounded in evidence, not opinion)
```
I need to review [design/prototype] for [feature]. Help me structure my
feedback:
1. What user needs does this address well? Cite evidence from [specific
   interviewees/research].
2. What user needs are not yet addressed?
3. What one change would have the highest impact?
4. What should [designer] own vs. what requires a product decision?

Keep it to one page. Ground every point in evidence, not opinion.

Save to docs/design-review.md.
```

**3.4 QA and launch readiness**
```
[Feature] is heading into QA. Please generate:
1. A comprehensive edge case list grouped by category (empty states, edge
   data conditions, multi-[account/entity] scenarios, permission states)
2. A QA checklist — the 10 most important things to verify before sign-off
3. A PR comment template for my first meaningful code review

Save to docs/qa-checklist.md.
```

### Phase 4 — Read the Numbers

**4.1 SQL without SQL**
```
Here is my data schema. [paste schema, or a description of your tables]
I have pasted the [raw data / Excel data] below. [paste data, or attach the
file]

Answer these questions:
1. [specific question — e.g., show the metric by cohort/segment]
2. [specific question]
3. [specific question]

For each: write the SQL, explain it in plain English, and tell me what the
result means for the decision at hand.

Save your findings to data/metric-findings.md.
```

**4.2 Metric diagnosis** (stay in the same session — the query results are already in context)
```
Now that we have the query results:
1. Build a metric tree decomposing [your metric] into its component drivers
2. Explain what caused the [decline/change] we're seeing
3. Explain what [the test/treatment] tells us about what actually moved
4. Generate 4 ranked hypotheses — why might the effect be incomplete?
5. For each hypothesis, what data would confirm or rule it out?

Save your diagnosis to data/metric-diagnosis.md.
```

**4.3 Recommendation memo** (continue in the same session)
```
Now write a results memo for [stakeholder] based on what we found:
- Situation (what we shipped and what we were testing)
- Evidence (3 bullets — the numbers that matter)
- Recommendation (what to do next — one sentence)
- Ask (what you need from them)
- Risk if we wait (one sentence)

Then play a skeptical VP and give me the 3 hardest questions — starting with
whether our sample size is actually enough to trust this.

Save the memo to docs/recommendation-memo.md.
```

**4.4 Experiment design** (pressure-test before you commit resources)
```
Before we finalize the recommendation, I need to pressure-test the pilot
result and design the full test.
Parameters: MDE [X points], Power [Y%], Significance [Z%], Available
[users/traffic]: [N], Max test duration: [N weeks].

Please:
1. Is the pilot result statistically significant at this sample size?
2. Calculate required sample size per variant for the full test
3. How many weeks does the full test need to run?
4. Should I wait for the full test or recommend scaling now?
5. What leading indicators should I monitor while it runs?

Save your experiment design to data/experiment-design.md.
```

### Phase 5 — Communicate Clearly

**5.1 PRD from chained research** (Claude reads your workspace directly — no re-pasting)
```
Read the following files from the workspace:
- research/interview-synthesis.md
- research/nps-analysis.md
- research/competitive-matrix.md
- research/hypothesis.md

Using all of this as context, write the PRD for [feature].
Structure: Problem Statement, User (who, job to be done), Goals and
Non-Goals, Success Metrics, User Stories (3-5), Open Questions.
One page. Audience: [engineer/designer names], not leadership. Plain
declarative language.

Save to docs/prd.md.
```

**5.2 Pressure-test before the meeting** (continue in the same session — the PRD is already in context)
```
Now pressure-test the PRD you just wrote. Play three reviewers in sequence,
2 hardest questions each:
1. Skeptical [engineer] (effort, feasibility, scope creep)
2. Skeptical [strategic stakeholder] (fit, resourcing, opportunity cost)
3. [A real, specific user] — does this actually solve why they [churned /
   disengaged]?

After all three, tell me which objection is most likely to kill this if I
don't address it upfront.

Save the objection log to docs/objection-log.md.
```

**5.3 Status updates for two audiences, one paste**
```
Here is my week on [project]:
Shipped: [bullets]
In progress: [bullets]
Blockers: [bullets]

Generate two status updates:
1. Team update for [names] — conversational, specific, what they need to know
2. Leadership update for [stakeholder] — done/in-progress/blocker counts,
   1 line on where we stand

Save to skills/weekly-status.md as a reusable template.
```

**5.4 A presentation that makes an argument**
```
Using your knowledge of [initiative] from CLAUDE.md and the workspace files,
design the narrative structure for a 6-slide deck for [audience/occasion]:
- Slide 1: The problem (1 number, 1 insight)
- Slide 2: Why now (what changed, what we learned)
- Slide 3: The proposal (what it is, what it isn't)
- Slide 4: Evidence
- Slide 5: The plan (timeline, milestones, risks)
- Slide 6: The ask

Then write full speaker notes for every slide — full sentences, not bullets.
3-5 sentences each: what the slide shows, what it means, what you want the
audience to take away before you move on.

Save the narrative to docs/presentation.md and speaker notes to
docs/presentation-notes.md.
```

### Phase 6 — Make It Stick

**6.1 Workspace audit** (run this periodically, not just once)
```
Review my current project folder. Look at the structure, the files that
exist, and what's in CLAUDE.md. Then:
1. What's missing that would make Claude more useful next session?
2. Suggest any reorganization that would reduce friction.
3. Write a CLAUDE.md update that reflects everything I've built so far.

Save the updated CLAUDE.md. Save the audit summary to workspace-audit.md.
```

**6.2 Turn repetitive tasks into one-command skills**
```
Here are my [N] most repetitive PM tasks on [project]:
1. [task]
2. [task]
3. [task]

For each, design a one-command workflow:
- The trigger prompt (what I paste to start it)
- The steps you run
- The output format
- Where the output gets saved

I want each to run with a single paste, no additional input from me.
Save each workflow to skills/ (one file per workflow).
```

**6.3 Your first scheduled agent**
```
I want an agent that runs [schedule, e.g. every Monday before standup].
Task: [what it checks/compares].
Format: [output shape — e.g. one headline number, one signal to watch, one
suggested action].

Help me:
1. Write the agent script
2. Show me how to run it manually first to verify the output
3. Write the message template it posts

In the real world this would run via a cron job, n8n, or a scheduled script.
For now, save the agent spec to agents/[name].md.
```

### Phase 7 — Your Agent Stack

**7.1 Chain a diagnosis onto an alert** (event-driven, not scheduled — only fires on signal)
```
Take my [pulse/monitoring] agent and add an anomaly trigger. When [metric]
moves more than [threshold] in either direction:
1. Automatically run a full diagnosis (decompose the move)
2. Generate 3 ranked hypotheses for what caused it
3. Write the query to confirm the top hypothesis
4. Post the full diagnostic before [deadline]

Chain this to the existing agent so it only triggers on alert.
Build me: the updated agent, the diagnostic chain, the message format, and a
simulated test so I can verify the output before it runs for real.
Save the agent spec to agents/[name].md.
```

**7.2 Registry + connection plan**
```
Here are all the agents I've built: [list, one line each: name, trigger,
what it does].

Build me:
1. An agent registry document with, for each: name, trigger, data sources,
   output format, delivery channel, schedule, owner
2. A connection plan — how each agent's output could feed the next agent's
   input
3. A CLAUDE.md update that tells Claude about all of them, so every session
   inherits the full agent context
4. A roadmap: what would a fully connected stack look like if you added one
   agent per month for the next 6 months?

Save the registry to agents/registry.md.
```

### The Capstone (run this whenever you want a real gut-check)
```
Read my CLAUDE.md, my agents/ folder, and my workspace-audit.md. Based on
everything in the workspace, run a review session:
1. What have I built so far across this project?
2. What's your confidence level in each artifact? What would get each one
   to 95%?
3. Based on the gaps above, what are the 2-3 things worth fixing before I
   hand this to a real collaborator?
4. If I wanted to recreate this workspace for a different product, what
   prompt would I use? Write it out so I can copy-paste it into a fresh
   session.

For each fix in question 3, suggest it and ask if I want you to implement
it now. At the end, update CLAUDE.md and save a session summary to
docs/capstone-session.md.
```

---

## Part 5: Lessons From Actually Doing This

The patterns above are the theory. These are the specific, sometimes-annoying things that come up doing it for real — worth knowing before they cost you an hour each.

- **A file someone references might not exist.** More than once, a prompt referenced a file (`research/hypothesis.md`, an "original Slack thread") that had never actually been saved anywhere. The fix isn't to invent plausible content — it's to say so explicitly, and either substitute the closest real file or recreate the source material from what's actually been given to you.
- **Illustrative sample numbers and your real data will diverge — report the real ones.** A template, a sample output, or a worked example will sometimes show a decline where your actual data shows an increase, or a specific number that doesn't match what you compute. Never quietly conform your output to match the example. State plainly that your real numbers differ and why that's fine — the example was illustrative, not a target.
- **A result that "looks like a huge win" can fail a significance check.** A large lift on a small sample size is exciting and can also be statistically indistinguishable from noise. Always run the actual check before it becomes the basis of a recommendation — this is exactly what the skeptical-VP pass in Phase 4 exists to catch, and it will sometimes force you to revise a recommendation you already sent. That's a feature, not a failure.
- **Chained agents should pass computed values, not just share a data source.** If Agent B re-derives a number Agent A already computed, you've got redundant work and a real (if small) risk they disagree if anything changes between the two calls. Pass the value directly when you chain.
- **Automation output needs to be boring and portable.** Emoji and special characters (arrows, em-dashes, smart quotes) that render fine in Slack can crash a plain `print()` statement on a default Windows console. If a script's output might ever be viewed in a terminal, keep it plain ASCII, or handle the encoding explicitly.
- **A recommendation in an audit doc isn't a fix until you actually build it.** It's easy to write "we should build X" in a workspace-audit and then never do it. Track "flagged but not yet fixed" explicitly — in CLAUDE.md's recap section, not buried in a doc nobody re-reads.
- **Context drift is real in long sessions.** If you're deep into hour three of a session, periodically ask yourself whether CLAUDE.md still reflects the current state — it's easy for the file to fall behind the conversation. This is what the workspace audit prompt (Phase 6.1) is for; run it more than once per project.

---

## Part 6: Quick-Start Checklist for a New Project

- [ ] Open Claude Code in a fresh project folder
- [ ] Run the AI interview + CLAUDE.md setup prompt (Phase 0.2) — answer honestly, don't rush it
- [ ] Confirm the cold-start test passes: close the session, reopen, ask Claude to state back your role/product/metric/open decision
- [ ] Build your first reusable skill for whatever you'll do weekly (status updates are the easiest starting point)
- [ ] As research comes in, save it to `research/` — don't let it live only in your head or a Slack thread
- [ ] Before writing any spec or PRD, run the AI interview on it — every time, not just the first time
- [ ] Before any meeting with a hard question in it, run the skeptical-reviewer pass
- [ ] Update `change_log.md` at the end of every session — two minutes, non-negotiable
- [ ] Run a workspace audit every few weeks, not just once
- [ ] Once you're doing the same task by hand three times, turn it into a skill; once a skill needs a schedule, turn it into an agent
