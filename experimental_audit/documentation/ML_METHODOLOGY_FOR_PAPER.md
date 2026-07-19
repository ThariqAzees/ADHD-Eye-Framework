# Machine Learning Methodology for Paper

This document provides a highly detailed description of the machine learning pipeline used for classifying ADHD and Control participants.

---

## 1. Classification Target
*   **Positive Class**: ADHD (unmedicated, $N=28$).
*   **Negative Class**: Control ($N=12$).

---

## 2. Preprocessing & Data Pipeline
To prevent data leakage, all preprocessing steps are fit strictly on the training partition of each CV fold and applied to the test partition.
*   **Missing Data Imputation**: Imputed using `SimpleImputer(strategy='median')` to handle missing gaze metrics.
*   **Feature Scaling**: Z-score scaled using `StandardScaler()` to standardize reaction time, accuracy, and ocular features.

---

## 3. Classifiers and Parameter Search Grids
Grid searches are performed within the inner loop of the nested cross-validation to select parameters optimizing the F1-score.

1.  **Logistic Regression**:
    *   *Grid*: `{'clf__C': [0.01, 0.1, 1.0, 10.0], 'clf__penalty': ['l2']}`
    *   *Solver*: `liblinear`
2.  **Random Forest**:
    *   *Grid*: `{'clf__n_estimators': [50, 100], 'clf__max_depth': [3, 5, None], 'clf__min_samples_split': [2, 5]}`
3.  **XGBoost**:
    *   *Grid*: `{'clf__n_estimators': [50, 100], 'clf__max_depth': [3, 5], 'clf__learning_rate': [0.05, 0.1, 0.2]}`
    *   *Objective*: `binary:logistic`, *Eval Metric*: `logloss`

---

## 4. Cross-Validation Architecture
We implement a double-loop **Nested Cross-Validation** strategy to prevent hyperparameter tuning leakage:
*   **Outer Loop**: Stratified 5-Fold Cross-Validation. Computes the final unbiased generalization performance estimates on the outer test folds.
*   **Inner Loop**: Stratified 3-Fold Cross-Validation. Used for selecting the optimal parameters on the training folds.
*   **Stratification**: Partitions are stratified by clinical class to maintain the 28:12 class prevalence ratio across folds.
*   **Random Seed**: `RANDOM_SEED = 42` is fixed for all splits and model initializations.

---

## 5. Permutation Testing
To evaluate whether the classifiers perform significantly better than chance, we run a **1,000-shuffle permutation test** on the corrected features:
1.  The target labels ($y$) are randomly shuffled.
2.  The full Stratified 5-Fold Nested CV pipeline is run on the shuffled labels.
3.  Empirical $p$-values are computed as:
    $$p = rac{\sum [Score_{	ext{shuffled}} \ge Score_{	ext{observed}}] + 1}{N_{	ext{permutations}} + 1}$$

---

## 6. Feature Ablation Experiments
To isolate the contribution of each modality, we evaluate 9 feature subgroups:
*   **A. Behavioral only**: 6 features
*   **B. Reaction Time only**: 4 features
*   **C. Gaze only**: 2 features
*   **D. Pupil only**: 1 feature
*   **E. Gaze + Pupil**: 3 features
*   **F. Behavioral + RT**: 10 features
*   **G. Behavioral + RT + Gaze**: 12 features
*   **H. Behavioral + RT + Pupil**: 11 features
*   **I. Behavioral + RT + Gaze + Pupil (All)**: 13 features

For each subgroup, the Stratified K-Fold CV pipeline is executed identically.