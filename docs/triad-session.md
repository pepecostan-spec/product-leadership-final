# Triad Working Session — Weekly Summary Prototype

## 1. Session Agenda (30 min)

**Purpose**: Share the tested prototype with Raj and Lena, get engineering and design input, and decide whether/how this direction moves toward a scoped build.

**Pre-read** (send with the invite): `docs/decision-brief.md`, `prototype/README.md`

| Time | What | Who |
|---|---|---|
| 0–3 min | Context recap: retention problem, why this direction (`docs/decision-brief.md`) | Me |
| 3–8 min | Live walkthrough of the clickable prototype (home → summary → nudge → confirmation) | Me |
| 8–16 min | Findings from testing across multiple rounds — *[PM: fill in the key patterns, quotes, and surprises from your test sessions before this meeting]* | Me |
| 16–24 min | Discussion — engineering and design input (see questions below) | Raj, Lena |
| 24–30 min | Decide and assign next steps | All |

### Questions for Raj (engineering feasibility)
- Given the capacity constraint (competing priorities pulling you onto other work), what's realistic to scope for a v1 vs. what has to be cut?
- The constraint is no new integrations — using only data Nudge already has. Any technical unknowns or risks in generating the insight/nudge/goal-progress logic from existing data?
- Rough sizing: what would a scoped v1 pilot take, and what's the fastest path to something real users could try (vs. the prototype's hardcoded scenario)?

### Questions for Lena (design)
- Does the prototype's interaction model and visual direction hold up against what came out of testing? What needs to change before it's build-ready?
- Any usability friction that showed up repeatedly across test rounds that needs a design fix before this goes further?
- Does the nudge/insight framing feel consistent with how we want Nudge to sound (per the "coach, not tracker" feedback in `research/nps-analysis.md`)?

### Decisions to walk out with
1. **Go / no-go** — does this direction proceed toward a scoped build, or does it need another round of iteration first?
2. **If go** — what's the minimum viable v1 scope, sized to Raj's actual available capacity?
3. **Ownership and timeline** — who owns what over the next 2 weeks, and what's the next checkpoint (e.g., a readout to Marcus)?

---

## 2. Post-Session Alignment Doc (template)

*Fill this out immediately after the session and share with Marcus.*

**Date**: [ ]
**Attendees**: [ ]
**Prototype tested**: `prototype/index.html` (see `prototype/README.md`)

### Decision
- [ ] Go — proceed to scoped v1 build
- [ ] No-go / needs another iteration — [reason]

### Scope agreed (if go)
- What's in v1: [ ]
- What's explicitly cut / deferred: [ ]
- Data/integration constraints confirmed: [ ]

### Engineering input (Raj)
- Feasibility notes: [ ]
- Capacity/timeline estimate: [ ]
- Open technical risks: [ ]

### Design input (Lena)
- Changes needed before build: [ ]
- Usability issues surfaced in testing: [ ]

### Open questions / risks
- [ ]

### Next steps
| Action | Owner | Due |
|---|---|---|
| | | |

### Next checkpoint
[Date/context — e.g., readout to Marcus]
