# Agent Spec: Weekly Insight Report

**Purpose**: Runs Friday afternoons. Pulls from 3 sources — retention metrics, this week's shipped work, and NPS themes — and produces a 3-2-1 report: what got done, what changed, what to watch.

**Script**: `agents/weekly_insight.py` — real, runnable, verified against this workspace's actual files.

---

## 1. The 3 sources, and how each is pulled

1. **Retention metrics** (`data/nudge.db`) — same cohort-comparison approach as `agents/monday_retention.py` / `agents/metric_pulse.py`: overall retention, each acquisition channel, and notification open rate, current cohort vs. previous.
2. **Sprint completions this week** (`change_log.md`) — parses every `## YYYY-MM-DD — Title` entry, keeps ones inside the lookback window (default 7 days), sorts newest-first.
3. **Top NPS themes** — looks for the freshest `research/synthesis-YYYY-MM-DD.md` (the format `skills/research-synthesis.md` produces); if none exists yet, falls back to the original `research/nps-analysis.md`. The report always states which source it used, so a stale fallback is never silently mistaken for fresh data.

## 2. How the 3-2-1 picks get made

This deliberately uses **rules, not an LLM call**, so the whole pipeline runs with no extra API dependency beyond the Slack webhook:
- **Done (3 bullets)**: the 3 most recent change_log entries in the window, by title.
- **Changed (2 bullets)**: the 2 retention/engagement signals with the largest absolute point movement, ranked the same way `metric_pulse.py` picks its "biggest mover."
- **Watch (1 bullet)**: scans change_log entries most-recent-first for a keyword flagging something unresolved (`tbd`, `blocker`, `estimate`, `pending`, `waiting on`, `not yet applied`) and surfaces the first hit, truncated to a clean ~160 characters. If nothing matches, falls back to the next-biggest metric mover that didn't make the "Changed" cut.

**If the workspace outgrows these rules** (e.g., "most recent" stops being a good proxy for "most report-worthy," or NPS theme selection needs real judgment about relevance rather than raw mention count), the natural next step is swapping the rule-based picks for an actual LLM synthesis call — the script's `build_done_bullets` / `build_changed_bullets` / `build_watch_bullet` functions are the seams where that would plug in.

## 3. How to run it manually (verify before scheduling)

```bash
python agents/weekly_insight.py
```
Always prints the Slack-format summary and saves the full report — never posts. Options:
- `--days N` — override the lookback window (default 7)
- `--date "Fri May 9"` — override the *displayed* date string only; the saved file always uses today's real date (`reports/YYYY-MM-DD.md`), so archival stays consistent even if you're previewing a different label
- `--db path.db` — point at a different database
- `--post` — actually post the 3-2-1 summary to Slack

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python agents/weekly_insight.py --post
```
Verified: without `SLACK_WEBHOOK_URL` set, `--post` still prints and saves the report, then exits with `SLACK_WEBHOOK_URL not set - can't post. Run without --post to dry-run.`

**Also verified during development**: the first run crashed twice on Windows — once from an em-dash in the date header, once from a `→` character pulled straight out of a change_log entry title into the printed output (`UnicodeEncodeError` on the default Windows console encoding, the same class of issue hit building the two earlier agents). Fixed with an `ascii_safe()` pass applied to every piece of text pulled from a file before it's printed, not just the script's own literal strings — worth remembering for any future agent that prints content sourced from markdown files.

## 4. Real-world wiring

- **Python + cron**: `0 16 * * 5 SLACK_WEBHOOK_URL=... python /path/to/agents/weekly_insight.py --post` — Friday 4pm.
- **n8n**: a Friday 4pm scheduled trigger → Execute Command node running the script with the webhook env var set. No branching logic needed in n8n itself; the script handles source-gathering, ranking, and delivery.
- **Developer ticket** (to point this at production instead of `data/nudge.db`): narrow scope — swap `get_connection()`'s target and confirm the production schema's column names match (`acquisition_channel`, `cohort_week`, `day_30`, `opened`). The change_log/NPS file-reading logic is workspace-agnostic already, as long as the same file conventions are used.

## 5. Sample output — real data, verified by actually running it

```
:clipboard: *Nudge Weekly Insight - Fri May 9*

Done this week:
- Capstone review: confidence audit and handoff prep
- Onboarding kit for a new Claude Code teammate
- Metric pulse agent built and verified

Changed this week:
- Organic channel retention up 11.0pts to 37.0%
- Referral channel retention up 7.5pts to 28.6%

Watch next week:
- Identified 3 fixes before handing this to a real collaborator: (1) reconcile the pilot dataset's retention rates against the company topline - not yet applied,...

Saved full report to reports\2026-08-02.md
```

The full saved report (`reports/2026-08-02.md`) additionally includes a "Top NPS themes referenced" section, sourced from `research/nps-analysis.md` since no dated weekly synthesis exists yet — that fallback is stated explicitly in the file itself.

**Read honestly, not just as a demo**: this is real output from this actual workspace, not adjusted to resemble the spec's illustrative sample. The "Changed" bullets came out as increases (not the sample's illustrative "Paid channel retention dropped 4pts"), because that's what the underlying data in `data/nudge.db` actually shows for the current-vs-previous cohort comparison — consistent with the same honest-reporting approach used in `agents/metric-pulse.md`.
