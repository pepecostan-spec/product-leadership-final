# Capstone Session: Full Workspace Review

*Reviewed `CLAUDE.md`, `agents/`, and `workspace-audit.md`, then assessed everything built this quarter for confidence and handoff-readiness.*

## 1. What's been built
A full PM workflow arc for Nudge Engage v2: discovery (interviews, NPS, competitive research) → root-cause diagnosis against real data → a piloted fix → statistical pressure-testing and a fully-powered follow-up design → a PRD and adversarial review → leadership communication (decision brief, memo, deck) → reusable tooling (4 skills, 1 verified automation agent). Full file-by-file inventory lives in `CLAUDE.md`'s "Working files" section.

## 2. Confidence assessment

| Artifact cluster | Confidence | What would get it to 95% |
|---|---|---|
| Interview synthesis, NPS analysis | ~40-45% | Small, non-representative samples (3 interviews, 10 comments) — need real sample sizes with proper selection. |
| Competitive matrix | ~55-60% | Built from public sources, not hands-on product use — need direct use of each competitor. |
| Metric findings & diagnosis | ~85-90% on the math | Computation is sound and sanity-checked; dataset's retention rates were never reconciled against the company topline figure quoted elsewhere. |
| Experiment design | ~90% on the math | Cross-validated two ways; the WAU-to-enrollment mapping was never checked against real production feature-flag/randomization infrastructure. |
| Prototype | ~65% | Real and verified working, but built on fabricated sample data; "tested across multiple rounds" was reported, not independently verified. |
| PRD, spec review, design review, QA checklist, objection log | ~50-60% | Logically sound but inherit the confidence ceiling of the research and prototype testing beneath them. |
| Decision brief, recommendation memo, deck | Mixed | Statistical claims inside are ~95% confident (it's just math); the strategic narrative wrapped around them inherits the lower qualitative-research confidence. |
| Codebase summary (maybe-finance) | ~90% accuracy, unverified relevance | Read the real code, so it's accurate; never confirmed how closely it resembles Nudge's actual stack. |
| Skills (4) | ~80% for 3 of them, ~60% for competitive-pulse | Three were exercised with real workspace content; competitive-pulse has never been triggered end-to-end. |
| Monday retention agent | ~90% | Ran twice with real, verified output including the failure path; never tested against a live Slack webhook or real cron/n8n deployment. |

## 3. Fixes identified before handing this to a real collaborator

1. **Data provenance gap** — pilot dataset retention rates (22-36%) were never reconciled against the company topline (44%→37%). **Not yet applied** — pending your input on whether the dataset is the full population or a subset/construct.
2. **Structural gaps from `workspace-audit.md` never actually built** — `docs/open-questions.md` and a home for the day-7→30 durability workstream were recommended but never created. **Not yet applied.**
3. **Simulated stakeholder feedback needed labeling** — `docs/objection-log.md`'s Raj/Marcus/Tom objections are Claude-simulated pressure-testing, not real statements from those people. **Applied**: added a disclaimer to the top of that file clarifying this, and noting real feedback should supersede the simulated version when it arrives.

## 4. Reproducible setup prompt
A copy-pasteable prompt for recreating this same CLAUDE.md-driven workspace pattern for a different product was provided in-conversation — it covers the interview-first setup, the top+bottom CLAUDE.md structure, the folder conventions (research/data/docs/prototype/skills/agents), the proactive-update-prompting behavior, and the instruction to label simulated stakeholder input as simulated.

## Still open
Fixes 1 and 2 above remain unapplied by your choice. They're tracked in `CLAUDE.md`'s "Right now" and "Recap" sections so they surface again in future sessions rather than getting lost.
