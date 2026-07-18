# Key Verified Numbers (v1.1)

This is the quick-reference sheet containing the exact frozen numerical values derived from the unmedicated ADHD and healthy Control groups. All numbers match the source CSV files exactly.

---

## 1. Cohort Sizes
*   Source Sessions: **67**
*   Source Individuals: **50**
*   Medicated repeated ADHD sessions: **17**
*   Aborted/Corrupted Controls: **10**
*   Final Cohort Size ($N$): **40** unique participants
    *   ADHD class size: **28** (70.0%)
    *   Control class size: **12** (30.0%)

---

## 2. Key Statistical Values (Descriptive & Inferential)

### Overall Response Accuracy (`accuracy_overall`)
*   ADHD Mean: **0.611384** (SD = **0.179756** [Sample SD], Median = **0.646875**, Min = **0.250000**, Max = **0.906250**)
*   Control Mean: **0.781250** (SD = **0.102421** [Sample SD], Median = **0.825000**, Min = **0.568750**, Max = **0.881250**)
*   Mann-Whitney U: **61.5** (Control rank sum: 352.5)
*   Raw $p$-value: **0.001746** (Survives FDR)
*   FDR $q$-value: **0.026185**
*   Cohen's $d$: **-1.0536** (Large effect size)

### Spatial Match Recognition (`hit_rate`)
*   ADHD Mean: **0.637515** (SD = **0.165618** [Sample SD], Median = **0.690749**, Min = **0.283333**, Max = **0.912500**)
*   Control Mean: **0.789239** (SD = **0.109034** [Sample SD], Median = **0.833333**, Min = **0.589744**, Max = **0.933333**)
*   Mann-Whitney U: **70.0**
*   Raw $p$-value: **0.004003** (Survives FDR)
*   FDR $q$-value: **0.030026**
*   Cohen's $d$: **-1.0019** (Large effect size)

### Reaction Time Instability (`rt_coefficient_of_variation`)
*   ADHD Mean: **0.299930** (SD = **0.103586** [Sample SD], Median = **0.278073**, Min = **0.164800**, Max = **0.581961**)
*   Control Mean: **0.232435** (SD = **0.038409** [Sample SD], Median = **0.228069**, Min = **0.193215**, Max = **0.343466**)
*   Mann-Whitney U: **227.0**
*   Raw $p$-value: **0.060911** (Does NOT survive FDR)
*   FDR $q$-value: **0.173766**
*   Cohen's $d$: **+0.7522** (Medium-large effect size)

### Pupil Tonic Arousal Variability (`pupil_variability`)
*   ADHD Mean: **0.091150** (SD = **0.041299** [Sample SD], Median = **0.094165**, Min = **0.007899**, Max = **0.175846**)
*   Control Mean: **0.066215** (SD = **0.025311** [Sample SD], Median = **0.067809**, Min = **0.021614**, Max = **0.101785**)
*   Mann-Whitney U: **225.0**
*   Raw $p$-value: **0.065091** (Does NOT survive FDR)
*   FDR $q$-value: **0.173766**
*   Cohen's $d$: **+0.6670** (Medium effect size)

---

## 3. Machine Learning Models Performance (Analysis B)

| Model | Accuracy (Mean ± SD) | Balanced Accuracy (Mean ± SD) | F1-Score (Mean ± SD) | ROC-AUC (Mean ± SD) |
| :--- | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.650 ± 0.105 | 0.603 ± 0.061 | 0.724 ± 0.136 | 0.670 ± 0.079 |
| Random Forest | 0.825 ± 0.143 | 0.760 ± 0.144 | 0.869 ± 0.128 | 0.690 ± 0.201 |
| XGBoost | 0.700 ± 0.143 | 0.623 ± 0.177 | 0.783 ± 0.115 | 0.683 ± 0.262 |

---

## 4. Single-Feature Performance (Baseline LR)
*   **`accuracy_overall`** (Behavioral): F1 = **0.857**, ROC-AUC = **0.827**, Balanced Accuracy = **0.693**.
*   **`hit_rate`** (Behavioral): F1 = **0.828**, ROC-AUC = **0.810**, Balanced Accuracy = **0.627**.
*   **`rt_variability`** (RT): F1 = **0.787**, ROC-AUC = **0.693**, Balanced Accuracy = **0.467**.
*   **`pupil_variability`** (Pupil): F1 = **0.775**, ROC-AUC = **0.647**, Balanced Accuracy = **0.477**.

---

## 5. Feature Ablation Summaries (Random Forest ROC-AUC)
*   **Behavioral only** (Group A): **0.763**
*   Reaction Time only (Group B): **0.705**
*   Gaze only (Group C): **0.655**
*   Pupil only (Group D): **0.515**
*   Gaze + Pupil (Group E): **0.640**
*   Behavioral + RT (Group F): **0.700**
*   Behavioral + RT + Gaze (Group G): **0.750**
*   Behavioral + RT + Pupil (Group H): **0.747**
*   **Behavioral + RT + Gaze + Pupil (All, Group I)**: **0.690**

---

## 6. Permutation Test Empirical p-values
*   Random Forest ROC-AUC: **0.0909** (Not significant)
*   Random Forest F1-Score: **0.0010** (Significant, driven by imbalance bias)
*   Logistic Regression ROC-AUC: **0.0739** (Not significant)
*   XGBoost ROC-AUC: **0.1479** (Not significant)

---

## 7. Data Missingness
*   Gaze Coordinate Missingness: **65.0%** (26 out of 40 sessions missing continuous gaze).
*   Pupil Coordinate Missingness: **0%** (for session-level variability, as all 40 subjects have valid trial-level pupil sizes computed).