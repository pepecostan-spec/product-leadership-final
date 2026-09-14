---
name: competitive-pulse
description: Run a quick weekly check for new moves from Nudge's tracked competitors (YNAB, Cleo, Monarch Money) via web search — pricing changes, feature launches, funding news — and flag whether research/competitive-matrix.md needs updating. Use whenever the user asks for a competitive pulse check, "what did competitors do this week," or "/competitive-pulse."
---

# Competitive Pulse Check (Nudge Engage v2)

## Trigger
A single paste, nothing else required:
```
/competitive-pulse
```
(or in plain language: "Run this week's competitive pulse check")

## Why no pasted input is needed
Unlike the other two workflows, the source material here is external (the web), not something the user already has. Web search is run directly — the user shouldn't need to gather anything first.

## Steps
1. Read `research/competitive-matrix.md` for the current tracked competitor list (YNAB, Cleo, Monarch Money) and each one's last-known "notable recent changes," so this check is measured against a known baseline rather than starting from scratch.
2. Run a targeted web search per competitor for news from roughly the last 1-2 weeks: pricing changes, new feature launches, funding announcements, notable press or reviews.
3. Filter out anything that's just a restatement of what's already captured in `competitive-matrix.md` — only surface genuinely new information.
4. For each genuinely new item, write one line on why it matters specifically for Nudge — tie it back to the white-space gaps already identified there (low-effort + prescriptive, sustained personal narrative) rather than reporting news for its own sake.
5. If nothing notable happened for a competitor that week, say so plainly rather than padding with minor UI tweaks or unrelated news just to have something to report.
6. End with an explicit recommendation: does `research/competitive-matrix.md` need a refresh based on this week's findings, or not yet?

## Output format
```
# Competitive Pulse — [Date]

## YNAB
[what's new, or "No notable changes this week"]
[if new: why it matters for Nudge]

## Cleo
[same structure]

## Monarch Money
[same structure]

## Does the competitive matrix need updating?
[Yes/No — and why]
```

## Where it's saved
`research/competitive-pulse-YYYY-MM-DD.md` — a new dated file each week. If the recommendation is "yes, update the matrix," that's a separate follow-up edit to `research/competitive-matrix.md` itself, not folded into this file.
