# START HERE — CONFERENCE PAPER EVIDENCE PACKAGE (v1.1)

PUBLICATION EVIDENCE HANDOFF v1.1
Correction type: DOCUMENTATION / REPORT RECONCILIATION

This directory contains the complete corrected handoff evidence package prepared for Claude to draft the conference paper focusing on the ADHD Eye Framework clinical classification.

---

## Recommended Reading Order for Claude

1.  **`README_CLAUDE_HANDOFF.md`**: (This manifest, defining files and scope boundaries).
2.  **`PUBLICATION_EVIDENCE_CORRECTION_LOG.md`**: Log documenting reconciliation changes from v1.0.
3.  **`PUBLICATION_EVIDENCE_REPORT.md`**: The corrected publication evidence report.
4.  **`PUBLICATION_ANALYSIS_FREEZE_v1.0.md`**: The frozen dataset, script, and pipeline configurations.
5.  **`KEY_VERIFIED_NUMBERS.md`**: The corrected quick-reference sheet for all numerical metrics in the paper.
6.  **`CLAIMS_GUARDRAILS.md`**: Strict limitations on clinical, ML, and webcam-related claims.
7.  **`COHORT_AND_DATASET_SUMMARY.md`**: Details on inclusions, exclusions, and participant flow.
8.  **`FEATURE_DEFINITIONS_FOR_PAPER.md`**: Details on the 13 features and excluded variables.
9.  **`ML_METHODOLOGY_FOR_PAPER.md`**: Grid searches, double CV loop, and shuffles.
10. **`STATISTICAL_METHODOLOGY_FOR_PAPER.md`**: Group comparisons and FDR correction.
11. **`COGNITIVE_TASK_FOR_PAPER.md`**: Visuospatial delayed-recognition task specifications.
12. **`FIGURE_MANIFEST.md`**: Mapping of PNG files to main and supplementary captions.
13. **Supporting CSVs**: Raw and summarized results.

---

## Authoritative File Inventory & Manifest

| Filename | Type | Authoritative / Frozen? | Purpose / Description | SHA256 Checksum |
| :--- | :---: | :---: | :--- | :--- |
| `dataset_features_REAL_v1.0.csv` | CSV | YES (Frozen) | The real parsed participant-level feature matrix ($N=40$). | `CB3760A29DBE0AB93D4557F72C44743483961984CC60A1D62C319DE59A4E2B8C` |
| `PUBLICATION_EVIDENCE_CORRECTION_LOG.md` | Doc | YES (Authoritative) | *Generated* | `374b748ca07e7ffe5b32400b319a1b80419a5696895d1712f0af907b051911cd` | Reconciliation log mapping differences from Handoff v1.0. | *Generated* |
| `PUBLICATION_EVIDENCE_REPORT.md` | Doc | YES (Frozen) | Key outcomes, sensitivity checks, and ablation verdicts. | *Generated* |
| `KEY_VERIFIED_NUMBERS.md` | Doc | YES (Authoritative) | *Generated* | `eebb2e8557cd8463cf4f67804d17189cc987453b1f665a198a0cb7fc42daa0cf` | Corrected reference sheet for all numbers. | *Generated* |
| `CLAIMS_GUARDRAILS.md` | Doc | YES (Authoritative) | *Generated* | `3e15654786611d2c73c86ea42da86638e66109ed264fc8895b71b3640d529589` | Safeguards against exaggeration. | *Generated* |
| `descriptive_statistics.csv` | CSV | YES (Frozen) | Source for N, Mean, SD, Median, Min, Max. | *Generated* |
| `statistical_comparisons.csv` | CSV | YES (Frozen) | Source for U-test, p-value, FDR q-value, Cohen's d. | *Generated* |
| `model_performance_summary.csv` | CSV | YES (Frozen) | Nested CV mean performance metrics. | *Generated* |
| `ablation_summary.csv` | CSV | YES (Frozen) | Ablation performance values for the 9 conditions. | *Generated* |
| `permutation_results.csv` | CSV | YES (Frozen) | Shuffled null distributions and empirical p-values. | *Generated* |
| `feature_groups.csv` | CSV | YES (Frozen) | Mapping of features to modalities. | *Generated* |
| `feature_lineage.csv` | CSV | YES (Frozen) | Mapping of features to extraction functions. | *Generated* |
| `dataset_provenance.csv` | CSV | YES (Frozen) | Checksums and Figshare details. | *Generated* |
| `dataset_integrity_report.csv` | CSV | YES (Frozen) | Missing values and outlier metrics. | *Generated* |
| `sensitivity_pupil_proxy.csv` | CSV | YES (Frozen) | Sensitivity check with/without `mean_pupil_proxy`. | *Generated* |
| `single_feature_performance.csv` | CSV | YES (Frozen) | Individual feature ranking scores. | *Generated* |
| `out_of_fold_predictions.csv` | CSV | YES (Frozen) | Out-of-fold predictions for confusion matrices. | *Generated* |
| `cohort inclusion/exclusion CSV` | CSV | **NOT GENERATED** | Represented in `COHORT_AND_DATASET_SUMMARY.md`. | - |
| `class-imbalance/baseline results` | CSV | **NOT GENERATED** | Defined in `PERFORMANCE_METRICS.md` and report. | - |
| `confidence-interval results` | CSV | **NOT GENERATED** | Included inside `model_performance_summary.csv`. | - |
| `learning-curve numerical results` | CSV | **NOT GENERATED** | Represented in PNG files under `figures/`. | - |

---

## 3. Synthetic Assets Quarantined (DO NOT USE FOR PUBLICATION RESULTS)
*   `dataset_features_SYNTHETIC_v1.0.csv`
*   `model_SYNTHETIC_v1.0.pkl`
*   `Pupil_dataset_SYNTHETIC.mat`