---
name: friday-status
description: Compile a Friday status update (shipped / in progress / blocked) for Nudge Engage v2 by reading this week's entries straight out of change_log.md and CLAUDE.md — no need to paste notes. Use whenever the user says "Friday status," "run my status update," "/friday-status," or asks to compile what shipped, is in progress, or is blocked this week.
---

# Friday Status Update (Nudge Engage v2)

## Trigger
A single paste, nothing else required:
```
/friday-status
```
(or in plain language: "Run my Friday status update")

## Why no pasted notes are needed
This workspace already logs every milestone in `change_log.md` as it happens, dated. Instead of asking the user to re-summarize their week from memory, this workflow reads that log directly — the raw material already exists and re-typing it would just be duplicate work.

## Steps
1. Determine the reporting window: the 7 days ending today, or since the last Friday status was generated, whichever actually reflects the gap.
2. Read `change_log.md` and pull every entry dated inside that window.
3. Read `CLAUDE.md`'s "Right now" section for anything blocker-relevant that hasn't yet made it into a change log entry (e.g., a standing constraint newly biting this week).
4. Classify each item using the same logic as `skills/weekly-status.md`: Shipped (done), In Progress (started, not done), Blocked (waiting on someone or something).
5. If a week genuinely has nothing in a category, say so plainly — don't invent filler to make the week look busier than it was.
6. Produce both output formats already defined in `skills/weekly-status.md`: the conversational **Team Update** and the compressed **Leadership Update**. This skill's job is gathering the input; `skills/weekly-status.md` owns the two output shapes — don't redefine that formatting here, reference it.

## Output format
Both formats from `skills/weekly-status.md`, back to back, each clearly labeled: Team Update first, then Leadership Update.

## Where it's saved
`status/YYYY-MM-DD-friday-status.md` (create the `status/` folder if it doesn't exist yet). Each week gets its own dated file rather than overwriting a single running file, so past updates stay available for reference.
