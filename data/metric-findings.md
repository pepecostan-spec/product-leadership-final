# Metric Findings: Retention & Weekly Summary A/B Test

**Source**: `Nudge Dataset.xlsx` (5 sheets: Users, Sessions, Retention, Nudges, Weekly_Summary_Sends). Loaded into a local SQLite database and queried directly — all numbers below are computed from the actual data, not estimated. 500 users across 5 cohort weeks (100/week). Data quality check passed: `churned` is a perfect inverse of `day_30` for all 500 rows.

**Note on scale**: This dataset's absolute retention rates (22–36%) run lower than the company-wide 30-day retention figure quoted elsewhere in this project (44% → 37%). Treat this as a sample/test dataset for analysis purposes — comparisons *within* it (cohort vs. cohort, variant vs. variant) are reliable; its absolute levels shouldn't be read as literally reconciling to the topline company metric.

**Cohort week 5 = the weekly summary A/B test population** (confirmed via join: all 100 users with a `variant` value are cohort week 5, and match exactly to the 100 users in `Weekly_Summary_Sends`).

---

## 1. 30-day retention by cohort week

```sql
SELECT cohort_week,
       COUNT(*) AS users,
       ROUND(100.0 * SUM(day_1)  / COUNT(*), 1) AS day1_pct,
       ROUND(100.0 * SUM(day_7)  / COUNT(*), 1) AS day7_pct,
       ROUND(100.0 * SUM(day_30) / COUNT(*), 1) AS day30_pct
FROM nudge_retention
GROUP BY cohort_week
ORDER BY cohort_week;
```

**Plain English**: For each signup cohort week, what share of users were still active on day 1, day 7, and day 30 after signup.

| Cohort week | Users | Day 1 | Day 7 | Day 30 |
|---|---|---|---|---|
| 1 | 100 | 90.0% | 60.0% | 32.0% |
| 2 | 100 | 90.0% | 53.0% | 25.0% |
| 3 | 100 | 97.0% | 48.0% | 25.0% |
| 4 | 100 | 92.0% | 44.0% | 22.0% |
| 5 | 100 | 90.0% | 61.0% | 29.0% |

**What the decline looks like**: Day-1 retention is stable (~90–97%) across every cohort — the acquisition/onboarding experience isn't the problem. The drop is entirely in what happens after: day-30 retention declines steadily from 32.0% (week 1) to 22.0% (week 4) — a 10-point slide over 4 weeks, consistent with the app-goes-stale hypothesis this whole project is built around. Week 5 breaks the pattern and ticks back up to 29.0% — but that's because week 5 is a blend of two very different sub-groups (see Q3): its control arm alone lands at 22.0%, exactly matching week 4's baseline, while its treatment arm pulls the average up. In other words, the underlying decline hadn't reversed on its own — it had plateaued around 22–25%, and the uptick in week 5's blended number is explained by the treatment, not a natural recovery.

**What this means for scaling the weekly summary**: The decline is real, monotonic, and appears to have flattened around 22–25% by week 4 without intervention — reinforcing that this is a persistent problem, not noise, and that doing nothing isn't going to self-correct.

---

## 2. Does setting a savings goal in week 1 improve retention?

```sql
SELECT
  CASE WHEN u.goal_set_date IS NOT NULL
            AND julianday(u.goal_set_date) - julianday(u.signup_date) BETWEEN 0 AND 7
       THEN 'goal_set_in_week1' ELSE 'no_goal_in_week1' END AS goal_group,
  COUNT(*) AS users,
  ROUND(100.0 * SUM(r.day_7)  / COUNT(*), 1) AS day7_pct,
  ROUND(100.0 * SUM(r.day_30) / COUNT(*), 1) AS day30_pct
FROM nudge_users u
JOIN nudge_retention r ON r.user_id = u.user_id
GROUP BY goal_group;
```

**Plain English**: Split all 500 users into two groups — those who set a savings goal within 7 days of signing up, and those who didn't (whether they set one later or never) — and compare day-7 and day-30 retention between the groups.

| Group | Users | Day 7 | Day 30 |
|---|---|---|---|
| Goal set in week 1 | 165 | 67.3% | 36.4% |
| No goal in week 1 | 335 | 46.3% | 21.8% |

**What this means**: Yes — users who set a goal in week 1 retain meaningfully better at both checkpoints. At day 30, they're retained at 36.4% vs. 21.8% (retention is ~1.7x higher). One correction to the record: the team's earlier working assumption (in `strategy.md`) was that non-goal-setters churn at "almost double" the rate. The real numbers show that's closer to true at day 7 (churn is ~1.6x higher without a week-1 goal) but narrows to ~1.2x by day 30 — the effect is real and directionally consistent, but moderates over time rather than holding at "double." Worth updating `strategy.md` to cite the precise ratio instead of the earlier anecdotal one.

**What this means for scaling the weekly summary**: This corroborates the goal-aware design direction — since the weekly summary's savings-goal-progress component specifically targets this exact lever (users who see and re-engage with a goal), and the effect on real retention is confirmed here, not just anecdotal.

---

## 3. Week 5 only: day-7 and day-30 retention, treatment vs. control

```sql
SELECT u.variant,
       COUNT(*) AS users,
       ROUND(100.0 * SUM(r.day_7)  / COUNT(*), 1) AS day7_pct,
       ROUND(100.0 * SUM(r.day_30) / COUNT(*), 1) AS day30_pct
FROM nudge_users u
JOIN nudge_retention r ON r.user_id = u.user_id
WHERE u.cohort_week = 5
GROUP BY u.variant;
```

**Plain English**: Within cohort week 5 — the group that was actually split into a controlled test — compare day-7 and day-30 retention between users who got the weekly summary (`summary_v1`) and users who didn't (`control`).

| Variant | Users | Day 7 | Day 30 |
|---|---|---|---|
| Control | 50 | 46.0% | 22.0% |
| Weekly summary (summary_v1) | 50 | 76.0% | 36.0% |

**What this means**: A large, consistent lift in both directions — day-7 retention is 30 points higher (46.0% → 76.0%, ~1.65x) and day-30 retention is 14 points higher (22.0% → 36.0%, ~1.64x) for the treatment group. The multiplicative effect is nearly identical at both checkpoints, which is a good sign the lift is real and durable rather than a short-lived novelty bump that fades by day 30.

**Caveat**: n=50 per arm, one cohort week, no formal significance test run here. The effect size is large enough to be compelling, but this should be read as strong directional evidence from a single test cohort, not a statistically certified result — worth noting explicitly if this goes to Marcus.

**What this means for scaling the weekly summary**: This is the single strongest piece of evidence in this dataset for scaling — a controlled comparison, not just a correlational cohort trend, showing the feature roughly doubles the retention gap that's been declining for a month.

---

## 4. Did the weekly summary open rate improve across the 4 sends vs. control?

```sql
SELECT variant, week_number,
       COUNT(*) AS sends,
       ROUND(100.0 * SUM(opened) / COUNT(*), 1) AS open_rate_pct
FROM nudge_weekly_summary_sends
GROUP BY variant, week_number
ORDER BY week_number, variant;
```

**Plain English**: For each of the 4 weekly sends, what share of recipients opened it — split by whether they were in the control or treatment arm.

| Week | Control open rate | Treatment (summary_v1) open rate |
|---|---|---|
| 1 | 4.0% | 28.0% |
| 2 | 4.0% | 52.0% |
| 3 | 4.0% | 52.0% |
| 4 | 6.0% | 56.0% |

**What this means**: Yes, clearly. The treatment's open rate nearly doubled from week 1 to week 2 (28.0% → 52.0%) and then held steady at 52–56% through weeks 3 and 4 — a pattern consistent with a habit forming after the first exposure, then sustaining, rather than a one-time novelty spike that decays. Control stayed flat and low (4–6%) across all 4 weeks, which confirms the lift is attributable to the feature itself, not a seasonal or cohort-wide effect that would have shown up in both arms.

**What this means for scaling the weekly summary**: The open-rate trend is the mechanism behind the retention lift in Q3 — it shows *why* retention improved (people are actually opening and, per the underlying data, acting on it more than control), and that the behavior is sticking rather than fading, which is exactly the durability question that matters before committing more engineering time.

---

## Bottom line for the scale decision

All four analyses point the same direction: the pre-existing decline is real and had plateaued (Q1), the goal-aware design premise is grounded in actual retention data, not just anecdote (Q2, with one number to correct in `strategy.md`), and the controlled test shows a large, consistent lift in both retention (Q3) and the open-rate behavior that likely drives it (Q4). The main caveat is sample size (n=50/arm, single cohort) — enough to justify scaling, but worth a larger or longer follow-up test before treating the exact magnitude (~1.6x) as a fixed expectation.
