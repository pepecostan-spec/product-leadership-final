# NPS Feedback Analysis — Findings for Marcus

**Source**: 10 raw NPS free-text comments from Nudge users.

**Note on sample size**: 10 comments is a small sample. Frequencies below are counts within this specific batch, not statistically representative of the broader user base — useful for spotting patterns to validate further, not for sizing impact.

---

## 1. Themes mentioned more than once, ranked by frequency

| Rank | Theme | Type | Mentions |
|---|---|---|---|
| 1 (tie) | Static/repetitive experience — no new insights over time | Complaint | 3 |
| 1 (tie) | No reason to return — app doesn't pull users back | Complaint | 3 |
| 3 | Lacks personalization — doesn't use or reference the user's own data/goals | Complaint | 2 |
| 3 | Initial experience/concept is well-liked | Praise | 2 |

---

## 2. Praise

**Theme: Initial experience and concept are well-liked (2 mentions)**
- "The first week was genuinely eye-opening." — #2
- "Love the concept." — #5

This praise is time-bound — both comments pair the compliment with a complaint about what happens afterward (see Complaints below). The concept and first-week moment land; nothing after that does.

---

## 3. Complaints (ranked by frequency)

**Theme A: Static/repetitive experience — no new insights over time (3 mentions)**
- "After that it just felt repetitive. I already know I spend too much on food." — #2
- "The home feed shows the same things every time I open it. There is nothing new to discover." — #7
- "I wish it would surface things I do not already know about my spending instead of just confirming what I already suspect." — #8

**Theme B: No reason to return — app doesn't pull users back (3 mentions)**
- "Nothing made me want to come back." — #1
- "I just forget it exists. If I got one really useful insight a week I would open it every week." — #5
- "The weekly email is the only thing keeping me engaged. The app itself has not given me a reason to open it." — #10

**Theme C: Lacks personalization — doesn't use or reference the user's own data/goals (2 mentions)**
- "I set a savings goal but Nudge has never once mentioned it since. It is like it forgot." — #6
- "The app did not feel like it knew me at all. Just generic money tips I could find anywhere." — #9

**Single-mention signals worth flagging (not ranked as themes, but concrete and high-signal):**
- "I want Nudge to feel like a financial coach, not a spending tracker... I need it to tell me what to do." — #3 (wants prescriptive guidance, not just descriptive tracking)
- "The nudges feel random. I got a notification that I spent $12 on coffee and I just turned off notifications entirely." — #4 (poorly targeted nudges are driving users to opt out of the notification channel entirely, not just ignore it)

---

## 4. Top 3 actionable issues

1. **The app doesn't surface anything new after initial setup.** (Theme A) Users are explicitly asking for insights they don't already know, not confirmation of what they suspect. *Action: build a mechanism that surfaces genuinely new, non-obvious findings on a recurring basis, not a static recap of the same data.*

2. **Nothing brings users back — the app is not the retention driver, other channels are.** (Theme B) One user says a weekly email is the only thing keeping them engaged; another says they'd return weekly for one good insight. *Action: a proactive, recurring touchpoint (in-app or push) that gives users a concrete reason to open the app each week — this is the direction already being explored as the candidate weekly summary screen.*

3. **The app doesn't remember or use what it already knows about the user.** (Theme C) A savings goal set by the user is never referenced again; another user says the tips are generic enough to find anywhere. *Action: this is a comparatively cheap, concrete fix — make existing user data (goals, connected accounts, history) visibly show up in the ongoing experience, not just at setup.*

---

## Connection to Engage v2

These findings independently corroborate the themes from the recent interview synthesis (`research/interview-synthesis.md`) and the working hypothesis in `strategy.md`: the app stops feeling relevant after the first week, and users lack a clear, personalized reason to return. Two new, concrete signals from this batch that aren't yet captured in strategy.md:
- The savings-goal follow-through gap (#6) is a specific, fixable defect, not just a general staleness complaint.
- Poorly targeted notifications are actively causing users to opt out of the channel entirely (#4) — worth checking whether this is widespread, since it would undercut any future push-based re-engagement strategy.
