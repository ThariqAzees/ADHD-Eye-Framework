# Publication Analysis Freeze v1.0

This document freezes the exact dataset versions, script paths, feature sets, cohort selection criteria, model definitions, cross-validation parameters, and random seeds used to generate the final publication evidence for the ADHD Eye Framework.

---

## 1. Frozen Datasets & Provenance
*   **Raw Source Dataset**: `data/raw/Pupil_dataset.mat`
    *   **MD5 Checksum**: `d4a1e92c8e125e93831f12797a783d52`
    *   **SHA-256 Checksum**: `44AA997E37815E7D2A003A4FC4E967F69438A86BDF04650B02F37AAA2A81819B`
*   **Processed Features Dataset**: `data/processed/dataset_features_REAL_v1.0.csv`
    *   **SHA-256 Checksum**: `CB3760A29DBE0AB93D4557F72C44743483961984CC60A1D62C319DE59A4E2B8C`
*   **Provenance Citation**: 
    Rojas-Líbano, D., Wainstein, G., Carrasco, X., Aboitiz, F., Crossley, N., & Ossandón, T. (2019). A pupil size, eye-tracking and neuropsychological dataset from ADHD children during a cognitive task. *Scientific Data*, 6(1), 25. DOI: [10.1038/s41597-019-0037-2](https://doi.org/10.1038/s41597-019-0037-2).

---

## 2. Frozen Cohort Criteria
*   **Source Cohort**: 67 sessions (representing 50 unique individuals).
*   **Exclusion 1 (Medication state)**: Exclude all 17 repeated medicated sessions (`on-ADHD`). Reverts the clinical positive class cohort to 28 unique unmedicated participants (`off-ADHD`).
*   **Exclusion 2 (Incomplete sessions)**: Exclude 10 Control sessions. Subjects 41, 46, and 47 are aborted (only 1 trial). Subjects 42, 43, 44, 45, 48, 49, and 50 are missing continuous trial structure fields (`Task_epocs` columns).
*   **Final Analyzable Cohort**: $N = 40$ unique subjects.
    *   **ADHD class (positive)**: 28 unmedicated subjects (70.0%).
    *   **Control class (negative)**: 12 healthy subjects (30.0%).

---

## 3. Frozen Feature Set (Analysis B: Corrected)
The features loaded from `dataset_features_REAL_v1.0.csv` are restricted to:
1.  `mean_reaction_time_ms` (Reaction Time)
2.  `median_reaction_time_ms` (Reaction Time)
3.  `rt_variability` (Reaction Time)
4.  `rt_coefficient_of_variation` (Reaction Time)
5.  `accuracy_overall` (Behavioral)
6.  `accuracy_by_load_diff` (Behavioral)
7.  `accuracy_by_distractor_diff` (Behavioral)
8.  `omission_rate` (Behavioral)
9.  `false_alarm_rate` (Behavioral)
10. `hit_rate` (Behavioral)
11. `normalized_fixation_instability` (Gaze)
12. `normalized_gaze_dispersion` (Gaze)
13. `pupil_variability` (Pupil)

*   *Note*: The legacy `mean_pupil_proxy` and `mean_fixation_stability` are frozen-out of the Corrected Analysis B feature matrix due to baseline normalization constraints.

---

## 4. Modeling & Validation Hyperparameters
*   **Cross-Validation Strategy**: Double-loop Nested Cross-Validation.
    *   **Outer CV Loop**: Stratified 5-Fold CV (Participant-independent splits to prevent leakage).
    *   **Inner CV Loop**: Stratified 3-Fold CV (For parameter grid searches).
*   **Pre-processing Pipeline**:
    *   *Imputation*: Median imputation (`SimpleImputer(strategy='median')`) of missing gaze/pupil features, fit on training folds only.
    *   *Scaling*: Z-score scaling (`StandardScaler()`), fit on training folds only.
*   **Random State**: `RANDOM_SEED = 42` (Fixed for all splits, estimators, and shuffles).

### Classifier Parameter Search Spaces:
1.  **Logistic Regression**:
    *   Solver: `liblinear`
    *   Grid: `{'clf__C': [0.01, 0.1, 1.0, 10.0], 'clf__penalty': ['l2']}`
2.  **Random Forest**:
    *   Grid: `{'clf__n_estimators': [50, 100], 'clf__max_depth': [3, 5, None], 'clf__min_samples_split': [2, 5]}`
3.  **XGBoost**:
    *   Objective: `binary:logistic`, Evaluation metric: `logloss`
    *   Grid: `{'clf__n_estimators': [50, 100], 'clf__max_depth': [3, 5], 'clf__learning_rate': [0.05, 0.1, 0.2]}`

---

## 5. Software Context & Package Versions
*   **Interpreter**: Python 3.14.0 (or matching local 3.14-64 core)
*   **Scientific Packages**:
    *   `numpy` >= 2.0.0
    *   `pandas` >= 2.2.0
    *   `scipy` >= 1.13.0
    *   `scikit-learn` >= 1.4.0
    *   `xgboost` >= 2.0.0
    *   `h5py` >= 3.11.0
*   **Execution Script**: `scratch/generate_publication_evidence.py`
