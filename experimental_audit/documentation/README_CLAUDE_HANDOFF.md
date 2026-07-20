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
| `PUBLICATION_EVIDENCE_CORRECTION_LOG.md` | Doc | YES (Authoritative) | *Generated* | `3A98C102BFC32A478E85BC74B8E6F0D93EB1B7D0B73E12241B42E1B928E1638E` |
| `PUBLICATION_EVIDENCE_REPORT.md` | Doc | YES (Authoritative) | Key outcomes, sensitivity checks, and ablation verdicts. | `FFF5A92345F59798D2020DA2359F3D2BCB5C54600C3A0B4BC41E5A21E33C633A` |
| `KEY_VERIFIED_NUMBERS.md` | Doc | YES (Authoritative) | *Generated* | `174FDE029D7EECA991185C1061A87A3AE3846D36A5572AB4F44DF9E4F9B07439` |
| `CLAIMS_GUARDRAILS.md` | Doc | YES (Authoritative) | *Generated* | `3E15654786611D2C73C86EA42DA86638E66109ED264FC8895B71B3640D529589` |
| `descriptive_statistics.csv` | Doc | YES (Authoritative) | Source for N, Mean, SD, Median, Min, Max. | `F813041DD759564F2F0F67A47B0FA3973E3C5829EBEB2F1C4EEE8DC9A1006376` |
| `statistical_comparisons.csv` | Doc | YES (Authoritative) | Source for U-test, p-value, FDR q-value, Cohen's d. | `74B18436AD1C30EFD4777AE34BEDF1660E8E10A65EE6145F3E8D0B82927B559D` |
| `model_performance_summary.csv` | Doc | YES (Authoritative) | Nested CV mean performance metrics. | `7BFD8B696F8B0F7C89DEA8090307F431F901F0BB74BC52338F1F8057242C4C73` |
| `ablation_summary.csv` | Doc | YES (Authoritative) | Ablation performance values for the 9 conditions. | `5203A9151E0C93BC70815706C4B77DED04AAA1BEF7FCB32EFD10D3EB6C45EDB0` |
| `permutation_results.csv` | Doc | YES (Authoritative) | Shuffled null distributions and empirical p-values. | `09671B297917A0633043BE4E8EE5652B17ECB9B9FA4D09B3D5EDE3FB108EE0EA` |
| `feature_groups.csv` | Doc | YES (Authoritative) | Mapping of features to modalities. | `B1692DBE8723DB07E3E3313F989859D95BF369260EEA8E81D297F63078171959` |
| `feature_lineage.csv` | CSV | YES (Frozen) | Maps features to raw MAT variables and parsing functions. | `E863D98CA2ABD02A5D63AC58632E85C6CADC856E42943BD1A1B0F9672357B32C` |
| `dataset_provenance.csv` | CSV | YES (Frozen) | Verified Figshare raw file details and N=40 participant inclusion flow. | `65C64A865D9030D2232DFD9E426B2B35D74A03BC4B0D1CB068AF272A1205081A` |
| `dataset_integrity_report.csv` | CSV | YES (Frozen) | Data integrity metrics, coordinate missingness rates, and min/max bounds. | `5D1833B4A616E8D91F7841498F4E485E78C77718D27883092796269A6D772B24` |
| `sensitivity_pupil_proxy.csv` | Doc | YES (Authoritative) | Sensitivity check with/without `mean_pupil_proxy`. | `89EB3FDDBCF35F4420F91631D75D050A2BCE9C8E76C51719B96286FD3407D27F` |
| `single_feature_performance.csv` | Doc | YES (Authoritative) | Individual feature ranking scores. | `74D8B444E9B73ACB58A5FA2DB9B8061A28D11001007AE06A157CDE0AF153045C` |
| `out_of_fold_predictions.csv` | Doc | YES (Authoritative) | Out-of-fold predictions for confusion matrices. | `1162DFE5ED047C04F200534A06C90001B26A074FD38B76D8FA9FA87B5BD02D96` |
| `cohort inclusion/exclusion CSV` | CSV | **NOT GENERATED** | Represented in `COHORT_AND_DATASET_SUMMARY.md`. | - |
| `class-imbalance/baseline results` | CSV | **NOT GENERATED** | Defined in `PERFORMANCE_METRICS.md` and report. | - |
| `confidence-interval results` | CSV | **NOT GENERATED** | Included inside `model_performance_summary.csv`. | - |
| `learning-curve numerical results` | CSV | **NOT GENERATED** | Represented in PNG files under `figures/`. | - |

---

## 3. Synthetic Assets Quarantined (DO NOT USE FOR PUBLICATION RESULTS)
*   `dataset_features_SYNTHETIC_v1.0.csv`
*   `model_SYNTHETIC_v1.0.pkl`
*   `Pupil_dataset_SYNTHETIC.mat`