# Workspace Audit — Nudge Engage v2

*Reviewed the full folder structure (24 files across root, `docs/`, `data/`, `research/`, `prototype/`, `skills/`) and CLAUDE.md's current content.*

## Current shape
- Root: `CLAUDE.md`, `project.md`, `strategy.md`, `change_log.md` — 4 core tracking files.
- `research/` (3 files, ~220 lines) — qualitative discovery: interviews, NPS, competitive matrix.
- `data/` (3 files, ~340 lines) — quantitative: retention findings, metric diagnosis, experiment design.
- `docs/` (12 files, ~540 lines) — everything else: specs, memos, QA, meeting prep, presentation materials.
- `prototype/` — clickable HTML prototype + README.
- `skills/` — one reusable skill (weekly status).

`docs/` has grown the fastest and now mixes several distinct purposes in one flat folder — flagged below.

---

## 1. What's missing

**A consolidated open-questions tracker.** The same unresolved items are currently scattered across multiple documents rather than living in one place: the cold-start data threshold appears as "open" in `docs/spec-readiness.md`, then again in `docs/prd.md`, then again in `docs/objection-log.md` — which specifically calls out that it's gone unresolved across documents. That repetition is a direct symptom of not having one place these live. A single `docs/open-questions.md` (threshold, nudge-persistence decision, day-7→30 ownership, etc.) would let each doc link to it instead of re-stating it.

**A home for the day-7→30 durability workstream.** It's been named as a needed, separate initiative in at least five places now (`strategy.md`, `data/metric-diagnosis.md`, `docs/prd.md`, `docs/objection-log.md`, `docs/presentation.md`) but has no actual file of its own — no hypothesis, no research plan, nothing. If Marcus signs off on the deck's ask #3, there's currently nowhere for that work to start.

**A placeholder for the powered-test results.** `data/experiment-design.md` is the *design* of the ~7-week follow-up test. There's no `data/experiment-results.md` waiting for when it concludes — worth creating now as an empty stub so the next session knows where that goes rather than deciding fresh.

**A lightweight "waiting on" list.** Several things are currently in flight only inside prose (change log entries, the weekly-status example): Raj's data-backfill estimate, the last 2 of 5 usability sessions, Marcus's sign-off on the deck. None of these are tracked as a live, checkable list anywhere.

## 2. Reorganization suggestions

**Don't physically move existing files.** Nearly every document in this workspace links to others by relative path (e.g., `docs/decision-brief.md`, `data/metric-diagnosis.md`). Moving files into subfolders now would silently break those cross-references across ~15 documents unless every link were rewritten at the same time — real risk for a cosmetic gain. If you want deeper structure later (e.g., `docs/decisions/`, `docs/specs/`, `docs/presentations/`), I can do it as its own pass with all links updated — just flagging it's not a quick win to bundle in here.

**Lower-risk alternative, done now**: group CLAUDE.md's working-files list by category instead of one flat list of 18 lines (see updated CLAUDE.md) — same files, no moves, easier to scan.

**Add the two new tracking files from Section 1** (`docs/open-questions.md`, `data/experiment-results.md` stub) — pure additions, zero risk to existing links.

## 3. CLAUDE.md
Updated and saved — see `CLAUDE.md`. Changes: working files grouped by category instead of one flat list; "Current initiative" note that the quarter culminated in a leadership deck; everything else re-verified against current file contents rather than assumed current.
