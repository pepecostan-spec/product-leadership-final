# QA Artifact: Weekly Summary / Notification Ranking

*Scope: personalized weekly summary (top insight, nudge, savings goal progress) plus the notification trigger that surfaces it — per `docs/pm-brief.md` and the v1 scope proposed in `docs/spec-readiness.md`.*

## 1. Edge Case List

### Empty states
- No transactions at all this week (user didn't spend) — what renders instead of a "top insight"?
- No transaction history at all yet (brand-new account) — should this even trigger a summary?
- No active savings goal — goal section must be fully omitted, not shown as a broken $0/$0 bar.
- No new recurring charges detected — the "new recurring charge" insight type must not fire on nothing.
- A quiet week where no insight condition qualifies — verify the defined fallback (e.g., "total spend this week vs. last week") renders, not a blank or error state.
- No nudge conditions met — verify no nudge is forced/shown; confirm this doesn't also suppress the rest of the summary.
- Account still syncing / sync incomplete — summary should not generate off partial data.

### Edge data conditions
- Exactly one transaction in the week — does it produce a sensible insight, or a trivial/odd one ("largest transaction" of one)?
- Duplicate or inconsistent categories (e.g., "Coffee" vs. "Coffee Shops") — could fragment or falsely inflate a spend-spike detection.
- Refunds / reversed / negative-amount transactions — must not be misread as a spending spike.
- Pending vs. posted transactions — confirm consistent handling if a pending charge changes amount or disappears after the summary is generated.
- Transfers between the user's own accounts — must be excluded from spend insights (a savings transfer isn't "spending").
- A single large one-time transaction (rent, a big purchase) — verify it doesn't dominate every future week's "top insight" as a false recurring signal.
- User exactly at the cold-start data threshold boundary — off-by-one risk on the minimum-history rule from `docs/spec-readiness.md`.
- A data gap (bank temporarily disconnected mid-week) — check whether this skews the rolling average used for "usual" spend.

### Multi-account scenarios
- User has multiple connected accounts (e.g., checking + credit card) — confirm insights aggregate across accounts, not just the first/primary one.
- The same real-world transaction appears on two accounts (e.g., a credit card payment showing as an expense on the card and a transfer from checking) — must not be double-counted.
- One of several accounts loses connection/needs re-auth while others stay active — does the summary still generate, and does it disclose the data may be incomplete?
- A second account is newly connected mid-week — verify this doesn't read as a false spending spike simply because more transactions became visible.
- Shared/joint accounts, if supported — whose historical baseline applies, and who receives the notification?

### Permission states
- Push notifications off at the OS level — is there a defined fallback (e.g., the in-app home-feed card), or does the user simply never get reached? This matters because the notification trigger was identified as the highest-impact fix in `docs/design-review.md` — if it silently fails, that fix doesn't ship.
- Notification permission revoked mid-week, after the ranking job already started — confirm the job doesn't error, and ideally skips wasted processing.
- Bank/Plaid access revoked or needs re-auth — the notification must not fire using stale data.
- Location permission — **not applicable**: location isn't part of Nudge's current data model per the "no new integrations" constraint. Worth an explicit check that no location-based signal was accidentally introduced during ranking work.
- Granular notification settings (if the app distinguishes "nudges" from other push categories) — ranking/eligibility must respect the specific category setting, not just a global on/off toggle.

## 2. PM QA Checklist — top 10 before sign-off

1. No nudge is ever forced when no insight condition qualifies — the defined empty/fallback state renders instead.
2. Savings goal section is fully omitted for users with no active goal (not a broken zero-progress bar).
3. Transfers between the user's own accounts are excluded from spend-based insights.
4. Users below the cold-start data threshold receive no personalized summary or notification — including the exact boundary case.
5. If notification permission is off, a defined fallback exists — the user isn't simply unreachable with no alternative.
6. Multi-account users get insights reflecting all connected accounts, with no cross-account double-counting.
7. A single large one-time transaction doesn't dominate subsequent weeks' insights as a false recurring signal.
8. Pending transactions are handled consistently, including what happens if they change or disappear after the summary generates.
9. No signal outside the stated data constraint made it into ranking (e.g., confirm nothing location-based).
10. Nudge actions are confirmed suggestion-only in this release — tapping a nudge doesn't silently persist a real budget/goal change, matching the scope agreed with Raj.

## 3. PR Comment Template (first meaningful code review)

```
Thanks for putting this together — reviewing from a product/QA angle rather than
code style, so flag if any of this is out of scope for this particular PR.

**Confirming scoped behavior**
- [ ] No nudge renders when no insight condition qualifies (vs. a generic fallback nudge)
- [ ] Savings goal section is omitted (not zero-state) when no goal exists
- [ ] Nudge actions are suggestion-only — no backend write on tap, per the agreed v1 scope

**Edge cases I want to confirm before sign-off** (see docs/qa-checklist.md for the full list)
- [ ] What happens with zero transactions this week?
- [ ] How are transfers between the user's own accounts handled — excluded from spend insights?
- [ ] What's the behavior right at the cold-start data threshold (the boundary, not just clearly-below cases)?
- [ ] If notification permission is off, is there a fallback, or does the user just not get reached?
- [ ] For multi-account users, do insights aggregate across all accounts, or only one?

**Questions, not blockers**
- [Add anything specific to this PR's diff — e.g., "this looks like it only queries the primary account, is that intentional for v1?"]

Happy to pair on any of these if it's faster than back-and-forth in comments.
```
