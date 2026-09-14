# Full Test Design: Weekly Summary Retention Experiment

*Pressure-testing the n=50/arm pilot and designing a properly powered follow-up. Computed with `scipy`/`statsmodels`, not hand-estimated — code shown inline.*

**Parameters given**: MDE = 5 percentage points, power = 80%, significance = 95% (two-sided), available WAU = 85,000, max test duration = 8 weeks.

---

## 1. Is the pilot result statistically significant at n=50?

```python
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats

# Day 7: treatment 38/50 vs control 23/50
proportions_ztest([38, 23], [50, 50])       # -> z=3.075, p=0.0021
stats.fisher_exact([[38, 12], [23, 27]])    # -> p=0.0038

# Day 30: treatment 18/50 vs control 11/50
proportions_ztest([18, 11], [50, 50])       # -> z=1.543, p=0.1229
stats.fisher_exact([[18, 32], [11, 39]])    # -> p=0.1856
```

| Metric | Control | Treatment | z-test p | Fisher's exact p | Significant at 95%? |
|---|---|---|---|---|---|
| Day 7 | 46.0% | 76.0% | 0.0021 | 0.0038 | **Yes** |
| Day 30 | 22.0% | 36.0% | 0.1229 | 0.1856 | **No** |

**This is the single most important correction to the earlier recommendation**: the day-7 lift is real and statistically solid — both tests agree, comfortably under p<0.05. But the **day-30 lift — the number cited as "retention nearly doubled" in the results memo — is not statistically significant** at n=50 (p≈0.12–0.19). With only 50 users per arm, an 11-vs-18 split on a binary outcome is well within the range noise alone could produce. The day-30 headline number is directionally encouraging but not yet proven.

---

## 2. Required sample size per variant for the full test

Powering on **day-30 retention** (the core company metric), using the pilot's control rate as baseline:

```python
import math

def sample_size_two_proportion(p1, p2, alpha=0.05, power=0.80):
    z_alpha, z_beta = 1.959964, 0.841621  # 95% two-sided, 80% power
    pbar = (p1 + p2) / 2
    num = (z_alpha*math.sqrt(2*pbar*(1-pbar)) + z_beta*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2
    return num / (p1-p2)**2

sample_size_two_proportion(0.22, 0.27)   # baseline 22%, MDE +5pp -> 27%
```
**Result: ≈1,161 users per arm** (cross-checked independently via `statsmodels`' Cohen's-h power solver — 1,159, consistent). Rounding up for a practical buffer: **~1,200 per arm, ~2,400 total.**

Baseline note: 22% is the pilot's own control-arm day-30 rate — the most directly relevant baseline available, since it's the same population and product state. It's lower than the company-wide topline (44%→37%) referenced elsewhere in this project; that gap was already flagged in `data/metric-findings.md` and likely reflects this dataset being a sample rather than the full base. Using the pilot's own control rate is the more defensible choice for sizing this specific test.

For reference, powering on **day-7** instead (baseline 46%, +5pp → 51%) requires **≈1,568 per arm** — larger, because the required sample size grows as the baseline rate approaches 50% (where variance is highest). Day-30 is both the more decision-relevant metric and the cheaper one to power on.

---

## 3. How many weeks does the full test need to run?

Enrollment speed is not the constraint — even at a conservative 5% of the 85,000 weekly active users allocated to the test per week (2,125/arm/week), the ~1,200/arm requirement is met in **under 1 week**:

| % of WAU/week allocated | Users/arm/week | Weeks to enroll required sample |
|---|---|---|
| 100% | 42,500 | 0.03 |
| 20% | 8,500 | 0.14 |
| 5% | 2,125 | 0.56 |

**The real constraint is the 30-day observation window** — every enrolled user needs a full 30 days to produce a day-30 data point, regardless of how fast enrollment fills. Recommended shape:
- **~2 weeks of enrollment** (not 1 day) — spreads recruitment across multiple signup cohorts to avoid a single day's traffic mix (channel, platform, day-of-week) dominating the result, a cheap hedge against the kind of segment skew already flagged as a weak hypothesis in `data/metric-diagnosis.md`.
- **+30 days (~4.3 weeks) observation** for the last-enrolled user to reach day 30.
- **+~1 week analysis buffer.**

**Total: ~7 weeks — inside the 8-week ceiling**, with about a week of margin.

---

## 4. Wait for the full test, or scale now?

**Wait — run the full test before committing to a full-scale rollout.** The previous recommendation memo's headline claim ("retention nearly doubled") rests on the day-30 number, which Q1 shows is not statistically distinguishable from noise at n=50. Recommending a full-scale rollout on that basis would be committing real engineering effort (already scarce, per the standing capacity constraint) on evidence that doesn't yet clear a basic significance bar.

This isn't a full walk-back, though: the **day-7 effect is real and strong**, and the full test only takes ~7 weeks — cheap relative to the cost of scaling on unproven evidence, or of abandoning a possibly-real effect too early. Recommended path: **keep the feature live for the existing pilot users (don't roll it back), and run the properly powered test in parallel** rather than pausing entirely — the fully powered result should be in hand well before any large engineering commitment would need to be made.

---

## 5. Leading indicators to monitor while the full test runs

Day-30 results take a month to mature per user, so these should be watched weekly as early signal and as guardrails:

- **Day-7 retention, by arm** — already proven significant; track continuously as the earliest read on whether the effect is holding at larger scale.
- **Day-1 activation rate** — should stay ~90%+ in both arms; a drop would signal something broke, not a real effect.
- **Weekly summary open rate, by send number (1–4)** — watch for the same ramp-then-plateau pattern seen in the pilot (28%→52%→56%); a flat or declining trend at scale would undercut the "habit forming" interpretation.
- **Notification opt-out rate** — a critical guardrail given `research/nps-analysis.md` already found poorly-targeted nudges cause opt-outs; a spike here could quietly cap the feature's ceiling even if retention looks good.
- **Day-7→30 transition rate, by arm** — the pilot showed this stage is untouched by the feature (`data/metric-diagnosis.md`); confirm that holds at scale rather than assuming it.
- **Sample ratio mismatch (actual split vs. intended 50/50)** — a basic data-integrity check; a skewed split partway through would undermine the whole test.
- **Platform / acquisition-channel cuts** — the pilot's small cells couldn't rule out segment effects (H4 in `data/metric-diagnosis.md`); larger scale is the first real chance to check this properly.
