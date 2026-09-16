# Outcome Roadmap & Trade-off Memo: Meridian Foundations

> Module 2 · Prioritization & Roadmapping for Product Leaders, ★ Deliverable 2
>
> Translate your strategy into a multi-team, outcome-driven roadmap, and a memo defending the hard prioritization calls behind it.

## 1. Outcome roadmap

_A multi-team roadmap organized by **outcomes**, not feature lists. Show how near-term revenue pressure is balanced against long-term platform bets._

| Horizon | Outcome / bet | Owning team(s) | Success signal |
|---|---|---|---|
| Now (0 to 3 mo) | Ship offline-first field capture (camera, voice, one-tap status) so pilot field crews have a faster alternative to texting | Mobile engineering, Product | KR1 pilot-cohort WAU ≥ 25% (trajectory toward 60%) |
| Now (0 to 3 mo) | Ship auto-tagging (geolocation, timestamp, OCR) that closes the capture-to-record loop without manual re-entry | Mobile engineering, Product | KR2 native capture ≥ 40%; KR3 median time-to-record < 2 hrs, down from ~18 |
| Now (0 to 3 mo) | Run field rollout with champions in pilot accounts, including a checkpoint testing *why* adoption is or isn't moving before scaling further | Customer success, UX research | Pilot checkpoint completed; friction-vs-incentive hypothesis validated or revised |
| Next (3 to 6 mo) | Expand rollout to pilot-validated accounts using the refined playbook from the Now checkpoint | Customer success, Product | KR1 WAU ≥ 45% across expanded cohort |
| Next (3 to 6 mo) | Add the 90-day post-rollout "sustain" re-measurement to the management system | Product, Customer success | 90-day adoption holds within 10 pts of peak (no reversion to texting) |
| Later (6 to 12 mo) | Full rollout across all 38 top-100 enterprise accounts | Customer success, Product, Mobile engineering | KR1 ≥ 60%, KR2 ≥ 70%, KR3 < 15 min company-wide |
| Later (6 to 12 mo) | Revisit the mid-market hard no with real pilot evidence in hand | Product (leadership decision) | Data-backed go/no-go on extending the proven capability to mid-market land-and-expand |

## 2. Trade-off memo

_What did you sequence first, what did you push out, and what did you cut entirely, and why? Use WSJF / cost of delay reasoning where it helps._

> I chose to sequence the offline-first capture app and auto-tagging pipeline first because the entire differentiation claim — faster than texting, zero re-entry — depends on both; nothing else on the roadmap has a product to roll out without them.
>
> I pushed out full-scale rollout across all 38 enterprise accounts because Module 1's own pressure-test flagged an unvalidated assumption (friction vs. incentive); scaling before a small pilot confirms or corrects it risks rolling out the wrong fix everywhere at once.
>
> I cut deeper ERP/analytics integrations and a field-data manager dashboard entirely from this cycle because neither moves the field-adoption OKRs — they serve the office side of accounts that already use Meridian, not the gap this initiative exists to close.
>
> Each Now-horizon rock maps to a specific OKR: the capture app drives KR1 (nothing to be weekly-active on without it), the auto-tagging pipeline drives KR2 and collapses the KR3 baseline, and the rollout checkpoint is what makes hitting KR1's 60% target credible rather than assumed.

## Link to full artifact

_[link to this deliverable in your repo]_
