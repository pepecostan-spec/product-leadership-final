# Metric Diagnosis: Retention Decline & What the Weekly Summary Fixed

*Builds on `data/metric-findings.md`. New queries run against the same SQLite load of `Nudge Dataset.xlsx` to decompose retention into stages and profile who still churns in treatment.*

---

## 1. Metric tree: decomposing 30-day retention

30-day retention isn't one number — it's the product of three sequential survival stages, each with different drivers available in the schema:

```
30-Day Retention
= P(Day 1 activation)  ×  P(Day 7 | Day 1)      ×  P(Day 30 | Day 7)
     "did onboarding      "did early habit          "did it stick
      complete?"            form in week 1?"          long-term?"
       ~90-97%               THE DECLINE               FLAT, UNTOUCHED
     (stable, not             DRIVER                   by the fix
      the problem)         (weeks 1-4: 66.7%→47.8%;   (~47-53% every
                             fixed in treatment:         cohort, incl.
                             50.0%→86.4%)                treatment)
```

**Sub-drivers feeding each stage, from the available schema:**
- **Day-1 activation**: account connected, first spending breakdown viewed (`nudge_sessions`, `screen = 'spending_breakdown'`).
- **Day 7 | Day 1**: week-1 savings-goal setting (`goal_set_date` within 7 days of `signup_date`), session frequency in week 1, weekly-summary/nudge delivery and opens in week 1.
- **Day 30 | Day 7**: ongoing nudge relevance (`nudge_type`, `opened`, `acted_on`), sustained weekly-summary opens across weeks 2–4, platform/acquisition-channel effects.

```sql
SELECT cohort_week,
       COUNT(*) AS users,
       ROUND(100.0*SUM(day_1)/COUNT(*),1) AS day1_pct,
       ROUND(100.0*SUM(day_7)/NULLIF(SUM(day_1),0),1) AS day7_given_day1_pct,
       ROUND(100.0*SUM(day_30)/NULLIF(SUM(day_7),0),1) AS day30_given_day7_pct
FROM nudge_retention
GROUP BY cohort_week ORDER BY cohort_week;
```

| Cohort week | Day 1 | Day 7 \| Day 1 | Day 30 \| Day 7 |
|---|---|---|---|
| 1 | 90.0% | 66.7% | 53.3% |
| 2 | 90.0% | 58.9% | 47.2% |
| 3 | 97.0% | 49.5% | 52.1% |
| 4 | 92.0% | 47.8% | 50.0% |
| 5 | 90.0% | 67.8% | 47.5% |

---

## 2. What caused the decline, weeks 1–4

The decomposition makes it precise: **Day-1 activation is stable (90–97%) — onboarding isn't the problem.** The decline is concentrated entirely in the **Day 7 | Day 1** stage, which erodes cohort over cohort: 66.7% → 58.9% → 49.5% → 47.8%. The **Day 30 | Day 7** stage, by contrast, is flat and noisy around 47–53% the whole time — it isn't getting worse, it just starts from a smaller base each cohort because fewer people survive to day 7 in the first place.

In plain terms: users aren't failing to start, and once someone's past their first week, their odds of making it to day 30 haven't changed. What's changing, cohort over cohort, is the fraction of people who make it through the first week at all — consistent with the project's working hypothesis that the app stops feeling relevant after the initial aha moment, and reinforced by average session counts, which also decline steadily by cohort (5.74 → 5.08 → 4.48 → 3.69), showing less early engagement, not just worse eventual survival.

---

## 3. What the week 5 split tells us about what the feature fixed

```sql
SELECT u.variant, COUNT(*) AS users,
       ROUND(100.0*SUM(r.day_1)/COUNT(*),1) AS day1_pct,
       ROUND(100.0*SUM(r.day_7)/NULLIF(SUM(r.day_1),0),1) AS day7_given_day1_pct,
       ROUND(100.0*SUM(r.day_30)/NULLIF(SUM(r.day_7),0),1) AS day30_given_day7_pct
FROM nudge_users u JOIN nudge_retention r ON r.user_id = u.user_id
WHERE u.cohort_week = 5
GROUP BY u.variant;
```

| Variant | Day 1 | Day 7 \| Day 1 | Day 30 \| Day 7 |
|---|---|---|---|
| Control | 92.0% | 50.0% | 47.8% |
| Weekly summary | 88.0% | **86.4%** | 47.4% |

This is the key diagnostic finding: **the feature's entire effect operates on the Day 7 \| Day 1 transition** — it more than doubles the odds of surviving the first week relative to control (50.0% → 86.4%). It does **not** move the Day 30 \| Day 7 stage at all (47.8% vs. 47.4% — a difference within noise). The weekly summary is fixing early habit formation, not long-term stickiness. Put differently: it gets people through the week the current decline is actually happening in (per Q2), but it hasn't yet touched whatever causes people to drop between week 1 and week 4 once they're already engaged.

Concretely, of the 32 treatment users who still churned by day 30: 6 (19%) never activated on day 1, 6 (19%) dropped in the day 1–7 window the feature mostly fixed, and **20 (63%) dropped in the day 7–30 window the feature doesn't touch.**

---

## 4. Four ranked hypotheses: why did some treatment users still churn?

```sql
WITH t AS (
  SELECT u.user_id, u.goal_set_date, r.day_30
  FROM nudge_users u JOIN nudge_retention r ON r.user_id = u.user_id
  WHERE u.cohort_week = 5 AND u.variant = 'summary_v1'
),
sess AS (SELECT user_id, COUNT(*) AS session_count FROM nudge_sessions GROUP BY user_id),
ws AS (SELECT user_id, SUM(opened) AS opens, SUM(acted_on) AS acts FROM nudge_weekly_summary_sends GROUP BY user_id)
SELECT t.day_30 AS retained, COUNT(*) AS users,
       ROUND(AVG(COALESCE(sess.session_count,0)),2) AS avg_sessions,
       ROUND(AVG(COALESCE(ws.opens,0)),2) AS avg_opens_of_4,
       ROUND(AVG(COALESCE(ws.acts,0)),2) AS avg_acts_of_4
FROM t
LEFT JOIN sess ON sess.user_id = t.user_id
LEFT JOIN ws ON ws.user_id = t.user_id
GROUP BY t.day_30;
```

| Retained by day 30? | Users | Avg. sessions | Avg. summary opens (of 4) | Avg. summary acts (of 4) |
|---|---|---|---|---|
| No (churned) | 32 | 5.22 | 1.88 | 0.78 |
| Yes | 18 | 5.39 | 1.89 | 0.56 |

**Hypothesis 1 (strongest): The feature fixes activation, not durability — churn simply relocated to a later, unaddressed stage.**
Evidence: Day 30 \| Day 7 is identical between treatment and control (47.4% vs. 47.8%); 63% of all remaining treatment churn happens in that window specifically. The feature was never designed to address whatever drives the day-7-to-day-30 drop — it just gets more people to the starting line of that stage.

**Hypothesis 2: Engagement with the feature doesn't predict who stays — opening or acting on it isn't enough on its own.**
Evidence: churned and retained treatment users open the summary at nearly identical average rates (1.88 vs. 1.89 of 4 sends), and churned users actually *act on* nudges slightly more on average (0.78 vs. 0.56). If acting on the feature reliably drove retention, this gap should point the other way. This suggests either the content itself isn't compelling enough to change behavior once engaged, or an action taken (e.g., "set a budget") isn't being followed through on or reinforced afterward — echoing the "goal set, never mentioned again" complaint already found in `research/nps-analysis.md`.

**Hypothesis 3: A residual group still never meaningfully engages, even with the feature.**
Evidence: 6 of 50 treatment users (12%) still failed the day 1→7 transition despite the feature — far better than control's 50% failure rate, but not zero. These are plausibly the users the entry-point gap already flagged in `docs/design-review.md`: the summary lives on the home feed, which only reaches users who already open the app.

**Hypothesis 4 (weakest, flag not conclude): Platform or acquisition-channel skew may be confounding the treatment effect.**
Evidence: churn counts within the treatment arm aren't evenly spread across platform/channel combinations (e.g., Android+organic shows the highest raw churn count), but cell sizes are tiny (1–9 users per combination in a 50-person arm) — not enough to distinguish a real segment effect from noise.

---

## 5. What data would confirm or rule out each hypothesis

| Hypothesis | Confirms it | Rules it out |
|---|---|---|
| H1 — churn relocated to day 7–30 | Day 60/90 retention data showing the treatment effect stays flat through that window too, and/or evidence that day-7-30 churners stopped engaging with later sends (weeks 3–4) specifically | The treatment effect reappearing at day 60/90 (e.g., if Priya's "~3 months to click" pattern shows up at scale), which would mean it's a timing lag, not a genuinely unaddressed stage |
| H2 — engaging isn't enough | Tracking whether an acted-on nudge (e.g., a budget) was still in place weeks later, or a satisfaction/NPS pulse specifically from churned-but-engaged treatment users | Adding a `nudge_content_id`/insight-type field to `weekly_summary_sends` (currently missing) and finding certain insight/nudge types do correlate with retention — would mean it's a targeting problem, not a fundamental engagement-doesn't-matter problem |
| H3 — residual non-engagers | Session logs showing these 6 users never opened the app at all in week 1 (vs. opened but ignored the card) | Evidence they did open the app and saw the card but actively dismissed it — would point to a content/relevance problem instead of a reach problem |
| H4 — platform/channel skew | A larger sample (more cohort weeks in the same test) showing the same segment pattern holds with adequate cell sizes, ideally via a formal variant × platform / variant × channel interaction test | The pattern washing out once cell sizes are large enough — most likely outcome given how thin the current cells are |
