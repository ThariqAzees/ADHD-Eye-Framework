# Pre-Registered Analysis Plan: ADHD Diagnostic Eye Framework

This document pre-registers the experimental setup, feature definitions, and machine learning pipeline configurations for the Rojas-Líbano (2019) clinical dataset audit and recovery. This protocol is frozen prior to execution and evaluation.

---

## 1. Cohort Inclusion & Exclusion Criteria
To establish a rigorous diagnostic classification baseline (ADHD vs. Control) and prevent subject leakage:
*   **Target Population**: Unmedicated ADHD (`off-ADHD`) and healthy controls (`Ctrl`).
*   **Inclusions**:
    *   Sessions with exactly 160 completed trials.
    *   Sessions with valid continuous eye-tracking recording streams.
    *   This includes exactly **28 ADHD** (off-medication) and **12 Control** sessions (Total $N = 40$).
*   **Exclusions**:
    *   Medicated ADHD sessions (`on-ADHD`, $N = 17$) are excluded to prevent subject-level leakage during cross-validation (since they are repeated measures of the same 28 ADHD participants).
    *   Incomplete Control sessions ($N = 10$, Subjects 41–50) are excluded due to missing or empty trial structures (having 0 or 1 trials recorded in their HDF5 tables).

---

## 2. Unit of Analysis
*   The unit of analysis is **one row per unique participant** ($N = 40$ rows total).
*   Since each of the 40 included sessions represents a unique participant, subject leakage is naturally prevented.

---

## 3. Feature Definitions and Analysis Splits

### Analysis A: Faithful Reconstruction (Original Definitions)
This analysis reproduces the original feature set with the exact definitions implemented in the legacy codebase:
*   **Reaction Time Features**:
    *   `mean_reaction_time_ms`: Mean of reaction times for valid trials ($0 < \text{RT} < 1500$ ms).
    *   `median_reaction_time_ms`: Median of reaction times for valid trials.
    *   `rt_variability`: Standard deviation of reaction times for valid trials.
    *   `rt_coefficient_of_variation`: $\text{rt\_variability} / \text{mean\_reaction\_time\_ms}$.
*   **Behavioral Performance Features**:
    *   `accuracy_overall`: Average accuracy across all 160 trials.
    *   `accuracy_by_load_diff`: $\text{accuracy}_{\text{Load 1}} - \text{accuracy}_{\text{Load 2}}$.
    *   `accuracy_by_distractor_diff`: $\text{accuracy}_{\text{None}} - \text{accuracy}_{\text{Emotional}}$.
    *   `omission_rate`: Ratio of trials with $\text{RT} \le 0$ or $\text{RT} \ge 1500$ ms.
    *   `hit_rate`: Ratio of correct "Present" responses to target trials.
    *   `false_alarm_rate`: Ratio of incorrect "Present" responses to lure trials.
*   **Legacy Eye-Tracking Features**:
    *   `mean_pupil_proxy`: Average of the trial-level mean z-scored pupil diameters. (Expected to be approximately 0.0 due to session-level z-scoring).
    *   `mean_fixation_stability`: Average of trial-level fixation instabilities calculated in raw pixel units: $\sqrt{\text{var}(x_{\text{pixel}}) + \text{var}(y_{\text{pixel}})}$.

### Analysis B: Improved Methodology (Corrected Definitions)
This analysis introduces corrected features to resolve the zero-pupil-mean and uncalibrated pixel-gaze issues:
*   **Behavioral Features**: Identical to Analysis A.
*   **Scientific Eye-Tracking Features**:
    *   `pupil_variability` (Replaces `mean_pupil_proxy`): The standard deviation of the trial-level mean pupil z-scores across the session:
        $$\text{pupil\_variability} = \text{std}(\mu_{\text{trial}, 1}, \mu_{\text{trial}, 2}, \dots, \mu_{\text{trial}, 160})$$
    *   `normalized_fixation_instability` (Replaces `mean_fixation_stability`): Root-mean-square spatial deviation of gaze coordinates during fixation epochs ($t \in [0, 500]\text{ms}$, $[1250, 1750]\text{ms}$, $[2500, 3000]\text{ms}$ relative to trial start) normalized by screen dimensions:
        $$x_{\text{norm}} = \frac{x}{1920}, \quad y_{\text{norm}} = \frac{y}{1080}$$
        $$\text{normalized\_fixation\_instability} = \sqrt{\text{var}(x_{\text{norm}}) + \text{var}(y_{\text{norm}})}$$
    *   `normalized_gaze_dispersion` (Replaces legacy `gaze_dispersion_during_array`): Gaze deviation during dot array presentation epochs ($t \in [500, 1250]\text{ms}$, $[1750, 2500]\text{ms}$, $[3000, 3750]\text{ms}$ relative to trial start) normalized by screen dimensions:
        $$\text{normalized\_gaze\_dispersion} = \sqrt{\text{var}(x_{\text{norm}}) + \text{var}(y_{\text{norm}})}$$

---

## 4. Preprocessing Pipeline
*   **Imputation**: `SimpleImputer(strategy='median')` to handle any missing value entries robustly.
*   **Scaling**: `StandardScaler()` applied to all features to ensure zero mean and unit variance.

---

## 5. Machine Learning Classifiers & Hyperparameter Search
Three classification models will be optimized using grid search cross-validation:
1.  **Logistic Regression**:
    *   `C`: `[0.01, 0.1, 1.0, 10.0]` (L2 regularization strength)
2.  **Random Forest**:
    *   `n_estimators`: `[50, 100, 200]`
    *   `max_depth`: `[3, 5, None]`
3.  **XGBoost**:
    *   `n_estimators`: `[50, 100, 200]`
    *   `max_depth`: `[2, 3, 5]`
    *   `learning_rate`: `[0.01, 0.1, 0.2]`

---

## 6. Cross-Validation Configuration
*   **Outer CV**: 5-Fold Stratified K-Fold (for unbiased generalization performance estimation).
*   **Inner CV**: 3-Fold Stratified K-Fold (for hyperparameter tuning on the training splits).
*   **Fold Composition**:
    *   With $N = 40$ (28 ADHD, 12 Control), the 5 outer folds will have:
        *   Folds 1, 2, 5: 6 ADHD, 2 Controls (Total 8 subjects per fold)
        *   Folds 3, 4: 5 ADHD, 3 Controls (Total 8 subjects per fold)
*   **Leakage Prevention**: Imputer, scaler, and models are fit strictly on training folds and applied to test folds inside the pipeline.

---

## 7. Primary Performance Metrics
The primary metric is **F1-score** (used for optimization in grid search). We will also report:
*   Classification Accuracy
*   Balanced Accuracy (adjusted for class imbalance)
*   Precision
*   Recall / Sensitivity
*   Specificity
*   Receiver Operating Characteristic Area Under Curve (ROC-AUC)
*   Precision-Recall Area Under Curve (PR-AUC)
*   Uncertainty estimation: 95% Confidence Intervals (CI) calculated across outer folds.

---

## 8. Ablation Experiments
For both Analysis A and Analysis B, we will train and evaluate:
1.  **Behavioral Features Only** (10 features)
2.  **Eye-Tracking Features Only** (2 features: pupil variability & normalized fixation instability)
3.  **Combined Features** (All features)

---

## 9. Permutation Testing Procedure
To establish statistical significance of model performances against the null hypothesis:
*   A permutation test will be executed with **1,000 label permutations**.
*   In each iteration, group labels (ADHD/Control) will be shuffled, and the entire nested cross-validation pipeline will be re-run.
*   Empirical p-values for all classifiers will be computed as:
    $$p = \frac{\sum_{i=1}^{1000} \mathbb{I}(\text{Metric}_{\text{perm}, i} \ge \text{Metric}_{\text{actual}}) + 1}{1001}$$
