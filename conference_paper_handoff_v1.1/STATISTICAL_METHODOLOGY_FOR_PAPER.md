# Statistical Methodology for Paper

This document describes the statistical test framework, multiple-comparison corrections, and effect size calculations.

---

## 1. Group Comparisons
*   **Statistical Test**: Two-sided Mann-Whitney U test (non-parametric comparison of medians). Selected because the features (specifically response accuracy, omission rate, and pupil variability) violate normality assumptions.
*   **Confidence Threshold**: $lpha = 0.05$.

---

## 2. Multiple-Comparison Correction
*   **Correction Method**: Benjamini-Hochberg False Discovery Rate (FDR) procedure.
*   **Application**: Applied across the entire set of features (13 total) to control the false discovery rate under multiple testing.
*   *Note*: Features are reported as statistically significant in the paper **only** if their FDR-adjusted $q$-value survives the $lpha = 0.05$ threshold.

---

## 3. Effect Size
*   **Metric**: Cohen's $d$ (parametric effect size metric representing standardized mean differences, reported alongside Mann-Whitney U for clinical comparison).
*   **Formula**:
    $$d = rac{\mu_1 - \mu_2}{s_{	ext{pooled}}}$$
    where $s_{	ext{pooled}} = \sqrt{rac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}}$.
*   **Interpretative Benchmarks**:
    *   $|d| < 0.2$: Negligible
    *   $0.2 \le |d| < 0.5$: Small
    *   $0.5 \le |d| < 0.8$: Medium
    *   $|d| \ge 0.8$: Large