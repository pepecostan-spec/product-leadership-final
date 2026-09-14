---
name: research-synthesis
description: Turn a raw dump of new user feedback, support tickets, or NPS comments into a themed research synthesis for Nudge Engage v2 — ranked themes with verbatim quotes, contradictions/outliers, and how it connects to the working hypothesis in strategy.md. Use whenever the user pastes raw feedback, tickets, or comments and asks for a synthesis, theme extraction, or wants to know what's new in user feedback this week.
---

# Weekly Research Synthesis (Nudge Engage v2)

## Trigger
Paste the raw material directly along with the request, in one message — no back-and-forth needed:
```
/research-synthesis
[paste raw feedback, support tickets, or NPS comments here]
```

## Steps
1. Read every item in the pasted batch fully — don't skim; each one is a potential data point.
2. Extract themes mentioned more than once, ranked by frequency. Only count something as a "theme" if 2+ distinct items support it — flag single-mention items separately as notable-but-unranked rather than inflating them to hit a round number.
3. Pull the actual verbatim quotes supporting each theme — never paraphrase a quote into something punchier than what was actually said.
4. Separate praise from complaints.
5. Note contradictions or outliers explicitly, including anything that cuts against the working hypothesis in `strategy.md` — don't quietly drop inconvenient data points because they complicate the story.
6. Connect findings back to `strategy.md`'s working hypothesis and any prior synthesis already in `research/`: does this batch corroborate existing themes, add something genuinely new, or complicate the picture?
7. If the sample size is small (under roughly 15-20 items), say so plainly in the output — small batches are directional, not conclusive, and the reader should know which kind they're looking at.

## Output format
```
# Research Synthesis — [Date]

**Source**: [what was pasted — e.g., "12 NPS comments" or "8 support tickets"]
**Sample size note**: [flag if small]

## Themes (ranked by frequency)
### [theme name] ([N] mentions)
- "[verbatim quote]" — [source/id if given]
(repeat per theme)

## Single-mention signals worth flagging
[if any — concrete but not ranked as themes]

## Contradictions / outliers
[explicit call-outs, including anything against the working hypothesis]

## Connection to strategy.md
[corroborates existing signal / adds something new / complicates the picture — be specific about which and why]
```

## Where it's saved
`research/synthesis-YYYY-MM-DD.md` — a new dated file each time, so weekly batches stay distinct and comparable rather than overwriting each other or getting appended into one ever-growing file.
