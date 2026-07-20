# Final Forensic Ablation Provenance & Feature Count Audit Report

**Audit Date**: July 20, 2026  
**Status**: PASSED / VERIFIED  
**Lead Auditor**: Advanced Agentic Coding Assistant (Antigravity)  

---

## 1. Executive Verdict

A complete forensic data-lineage and computational audit was conducted to resolve the blocking discrepancy identified in Phase 6 regarding feature-ablation results (`ablation_summary.csv` and `ablation_detailed.csv`). 

*   **Origin of E1–E9 Results**: Generated on July 18, 2026 by `experimental_audit/scripts/run_audit_experiments.py` executing on the **legacy synthetic dataset** (50 mock subjects). Synthetic Gaussian RT and Gaze features had near-zero variance and artificial group separation, causing $1.00$ Accuracy/ROC-AUC on conditions E2 and E3.
*   **Origin of A–I Results**: Generated on July 18, 2026 by `scratch/generate_publication_evidence.py` executing on the **checksum-verified real clinical dataset** (`dataset_features_REAL_v1.0.csv`, $N=40$). These reflect authentic clinical performance across feature groups A through I.
*   **Packaging Error Root Cause**: In `scratch/reconcile_and_build_handoff_FINAL.py`, the staging registry mapped `ablation_summary.csv` and `ablation_detailed.csv` to `experimental_audit/results/` (the legacy synthetic folder) instead of `experimental_audit/publication_evidence/` (the real clinical folder).
*   **Abstract Verification**: The key metrics in the approved Phase 5 Abstract (Behavioral-only Random Forest ROC-AUC $\approx 0.763$, Full Multimodal Random Forest ROC-AUC $\approx 0.690$) are **authentic, verified, and reproduced** from the real clinical dataset.

---

## 2. Inventory of Ablation Artifacts

| File Path | Size (Bytes) | SHA-256 Checksum | Modality Schema | Dataset Source | Scientific Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `experimental_audit/publication_evidence/ablation_summary.csv` | 5,022 | `5203A9151E0C93BC70815706C4B77DED04AAA1BEF7FCB32EFD10D3EB6C45EDB0` | Groups A–I | `dataset_features_REAL_v1.0.csv` | **AUTHORITATIVE** |
| `experimental_audit/publication_evidence/ablation_detailed.csv` | 17,102 | `696712154F67E73FB23B90ABC0DB6CE35F7FF8185C1BAFF449C35C3477016C20` | Groups A–I | `dataset_features_REAL_v1.0.csv` | **AUTHORITATIVE** |
| `experimental_audit/final_ablation_verification/ablation_summary_REPRODUCED.csv` | 5,022 | `5203A9151E0C93BC70815706C4B77DED04AAA1BEF7FCB32EFD10D3EB6C45EDB0` | Groups A–I | `dataset_features_REAL_v1.0.csv` | **VERIFIED REPRODUCTION** |
| `experimental_audit/legacy_synthetic_artifacts/ablation_summary.csv` | 2,600 | `7A45005EC945D1264747BF232B3FB252938DF136DA2C57D9DBDE05CDED7131F3` | Experiments E1–E9 | Legacy Synthetic N=50 | **QUARANTINED** |
| `experimental_audit/legacy_synthetic_artifacts/ablation_detailed.csv` | 8,687 | `F386348252005B4EFD72BF5ECC7A4D35273CF916D50A8F64910FE1BAB865348A` | Experiments E1–E9 | Legacy Synthetic N=50 | **QUARANTINED** |

---

## 3. Provenance Comparison: E1–E9 vs. A–I Results

| Property | Legacy E1–E9 Experiment | Authoritative A–I Publication Experiment |
| :--- | :--- | :--- |
| **Generating Script** | `experimental_audit/scripts/run_audit_experiments.py` | `scratch/generate_publication_evidence.py` |
| **Input Dataset** | `data/processed/dataset_features_v1.0.csv` (Synthetic) | `data/processed/dataset_features_REAL_v1.0.csv` (Real Clinical) |
| **Cohort Size** | $N=50$ (Synthetic mock participants) | $N=40$ (28 unmedicated ADHD, 12 Controls) |
| **Data Authenticity** | Fully Synthetic (`np.random.normal`) | 100% Real MATLAB Cell Arrays (Figshare v3) |
| **Group Naming** | E1–E9 (`E1_Behavioral_only`, `E2_RT_only`, etc.) | A–I (`A_Behavioral_only`, `B_Reaction_Time_only`, etc.) |
| **E2 (RT) & E3 (Gaze) Perf.** | $1.000$ Accuracy / ROC-AUC (Synthetic separation) | $0.660$ & $0.352$ (LR AUC), $0.705$ & $0.655$ (RF AUC) |
| **Nested CV Strategy** | 5-Fold Stratified K-Fold | 5-Fold Outer / 3-Fold Inner Stratified Nested CV |
| **Imputation** | `SimpleImputer(strategy='median')` | `SimpleImputer(strategy='median')` fit inside CV folds |

---

## 4. Verification of Approved Abstract Metrics

The headline numbers cited in the approved Phase 5 Abstract and publication reports were verified directly from `experimental_audit/publication_evidence/ablation_summary.csv`:

1.  **Behavioral-Only Random Forest ROC-AUC**:
    *   Row 1: `A_Behavioral_only` | `Random_Forest` | ROC-AUC = **0.763333** ($\approx \mathbf{0.763}$) | Balanced Accuracy = $0.7433$, F1 = $0.8727$.
    *   **Status**: **VERIFIED AUTHENTIC**
2.  **Full Multimodal Random Forest ROC-AUC**:
    *   Row 25: `I_Behavioral_RT_and_GazePupil` | `Random_Forest` | ROC-AUC = **0.690000** ($\approx \mathbf{0.690}$) | Balanced Accuracy = $0.7600$, F1 = $0.8692$.
    *   **Status**: **VERIFIED AUTHENTIC**

---

## 5. Statistical FDR Test Count Audit

*   **Discrepancy**: `STATISTICAL_METHODOLOGY_FOR_PAPER.md` previously cited FDR correction across "13 features", whereas `statistical_comparisons.csv` contains 15 rows.
*   **Resolution**: `dataset_features_REAL_v1.0.csv` contains 15 total features (13 ML input features + 2 raw pupil/gaze summary proxies).
*   **Code Audit**: The statistical calculation code applied the Benjamini-Hochberg FDR procedure jointly across all **15 tested features**.
*   **q-value Verification**:
    *   `accuracy_overall` ($p = 0.001746$): $q = 0.001746 \times 15 / 1 = \mathbf{0.026185}$ ($\approx 0.0262$).
    *   `hit_rate` ($p = 0.004003$): $q = 0.004003 \times 15 / 2 = \mathbf{0.030026}$ ($\approx 0.0300$).
*   **Correction**: `STATISTICAL_METHODOLOGY_FOR_PAPER.md` was updated to explicitly clarify the 15-feature test count.

---

## 6. Trial Count Verification

*   **Raw MAT Audit**: Parsed `Pupil_dataset.mat` via `pymatreader` across all 40 included clinical sessions.
*   **Result**: Every single included session contains **exactly 40 trials** ($N=40$ sessions, 40/40 completed trials, 100% completeness).
*   **Domain Shift Fact**: The reference laboratory task used 40 trials per subject, whereas the live webcam web deployment uses 10 trials per subject.

---

## 7. Packaging Script Fix

In `scratch/reconcile_and_build_handoff_FINAL.py`, the source registry entries for ablation CSVs were updated:

```python
        'ablation_summary.csv': {
            'Source_Path': 'experimental_audit/publication_evidence/ablation_summary.csv',
            'Generated_By': 'scratch/generate_publication_evidence.py',
            'Generated_From': 'data/processed/dataset_features_REAL_v1.0.csv',
            'Status': 'AUTHORITATIVE_SOURCE',
            'Reason': 'Authentic publication ablation metrics across groups A-I on REAL N=40 dataset.'
        },
        'ablation_detailed.csv': {
            'Source_Path': 'experimental_audit/publication_evidence/ablation_detailed.csv',
            'Generated_By': 'scratch/generate_publication_evidence.py',
            'Generated_From': 'data/processed/dataset_features_REAL_v1.0.csv',
            'Status': 'AUTHORITATIVE_SOURCE',
            'Reason': 'Fold-level authentic publication ablation details across groups A-I on REAL N=40 dataset.'
        },
```

---

## 8. Final Required Statements

ABLATION PROVENANCE: PASS  
A–I RESULTS REPRODUCED: YES  
BEHAVIORAL-ONLY RF ROC-AUC ≈ 0.763 VERIFIED: YES  
FULL MULTIMODAL RF ROC-AUC ≈ 0.690 VERIFIED: YES  
E1–E9 RESULTS EXPLAINED: YES  
SYNTHETIC/LEAKAGE CONTAMINATION IN PUBLICATION RESULTS: NO  
FDR FEATURE COUNT RESOLVED: YES  
TRIAL COUNT VERIFIED: YES  
PHASE 5 ABSTRACT STILL VALID: YES  
SAFE TO REBUILD FINAL CLAUDE HANDOFF: YES  
