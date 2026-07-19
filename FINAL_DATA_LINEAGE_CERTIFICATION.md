# Final Data Lineage Certification (Clean-Room Rebuild)

**Date**: July 19, 2026  
**Status**: APPROVED & FROZEN  
**Subject**: ADHD Eye Framework Clinical Dataprovenance & Integrity Certification  

---

## 1. Executive Summary
This document certifies that a complete, clean-room forensic data-lineage audit has been performed on the ADHD Eye Framework dataset. We verify that **100% of the reported statistical and machine learning results are derived exclusively from the authentic, clinical Rojas-Líbano et al. (2019) dataset with zero synthetic contamination**. 

All inconsistencies identified in previous handoff versions (v1.0–v1.2) have been resolved. Stale Mann-Whitney U-statistics have been updated using independent SciPy recomputations, and legacy synthetic metadata files have been quarantined.

---

## 2. Complete Data Lineage Pipeline

```mermaid
graph TD
    A["Raw Figshare Archive: Pupil_dataset.mat (v3)<br>MD5: d4a1e92c8e125e93831f12797a783d52<br>SHA256: 44AA997E37815E7D2A003A4FC4E967F69438A86BDF04650B02F37AAA2A81819B"] 
    --> B["HDF5 parser (dataset/build_dataset.py via h5py)"]
    B --> C["Total Recorded Sessions: 67 (50 unique participants)"]
    C --> D["Medication Filter: Exclude repeated 'on-ADHD' (17 sessions)"]
    C --> E["Completeness Filter: Exclude incomplete 'Ctrl' trials != 160 (10 sessions)"]
    D --> F["Final Analyzable Cohort: N=40 (28 off-ADHD + 12 Control)"]
    E --> F
    F --> G["Feature Extraction (dataset/parse_mat.py)"]
    G --> H["Clean Feature Matrix: dataset_features_REAL_v1.0.csv<br>SHA256: CB3760A29DBE0AB93D4557F72C44743483961984CC60A1D62C319DE59A4E2B8C"]
    H --> I["Statistical Analyses (SciPy descriptive & inferential tests)"]
    H --> J["ML Pipelines (Stratified 5-Fold Nested Cross-Validation)"]
    J --> K["Feature Ablation Study (9 feature configurations)"]
    J --> L["Permutation Testing (1,000 label shuffles)"]
```

### Exact Stage Identifiers & Hashes
1.  **Stage 1: Raw Data Entry**
    *   Input File: `data/raw/Pupil_dataset.mat` (Size: $1,257,809,856$ bytes)
    *   MD5 Checksum: `d4a1e92c8e125e93831f12797a783d52` (Matches Figshare official DOI: `10.6084/m9.figshare.7218725.v3` exactly)
    *   SHA-256 Checksum: `44AA997E37815E7D2A003A4FC4E967F69438A86BDF04650B02F37AAA2A81819B`
2.  **Stage 2: Parsing & Cohort Selection**
    *   Script: `dataset/build_dataset.py` (specifically `build_processed_dataset()`)
    *   Exclusion 1: Medicated ADHD measurements (`group == 'on-ADHD'`) -> 17 sessions excluded.
    *   Exclusion 2: Aborted/incomplete control runs (`group == 'Ctrl'` and trial count $\neq 160$) -> 10 sessions excluded.
    *   Cohort Output: $N=40$ unique subjects (28 unmedicated `off-ADHD` + 12 health Controls).
3.  **Stage 3: Feature Extraction & Aggregation**
    *   Script: `dataset/parse_mat.py` (specifically `extract_subject_features()`)
    *   Output File: `data/processed/dataset_features_REAL_v1.0.csv`
    *   SHA-256 Checksum: `CB3760A29DBE0AB93D4557F72C44743483961984CC60A1D62C319DE59A4E2B8C`
4.  **Stage 4: Statistical Testing & Machine Learning**
    *   Scripts: `scratch/generate_publication_evidence.py` and `scratch/reconcile_and_build_handoff_v1.3.py`
    *   Inputs Loaded: `data/processed/dataset_features_REAL_v1.0.csv` (SHA256: `CB3760A29DBE0AB93D4557F72C44743483961984CC60A1D62C319DE59A4E2B8C`)
    *   Outputs: Descriptive stats, Mann-Whitney U-tests, Stratified 5-Fold Nested CV scores, ablation matrices, and permutation null distributions.

---

## 3. Participant-Level Raw-to-Feature Verification Spot Checks

Six participants (3 ADHD + 3 Controls) were selected from `dataset_features_REAL_v1.0.csv` and re-evaluated by extracting raw arrays directly from `Pupil_dataset.mat` via `h5py` and applying the parsing logic.

### ADHD Participants

#### Subject: `subject_4`
*   **Raw Session in MAT**: Index 3 (Group: `off-ADHD`, Trials: 160)
*   **Gaze Availability**: Valid gaze coordinates present.
*   **Recomputation Comparison**:
    *   `accuracy_overall`: Recomputed = `0.362500` | CSV = `0.362500` | Diff = `0.000000` | **PASS**
    *   `hit_rate`: Recomputed = `0.400000` | CSV = `0.400000` | Diff = `0.000000` | **PASS**
    *   `mean_reaction_time_ms`: Recomputed = `759.787879` | CSV = `759.787879` | Diff = `0.000000` | **PASS**
    *   `rt_coefficient_of_variation`: Recomputed = `0.435771` | CSV = `0.435771` | Diff = $<10^{-16}$ | **PASS**
    *   `pupil_variability`: Recomputed = `0.106660` | CSV = `0.106660` | Diff = `0.000000` | **PASS**
    *   `normalized_fixation_instability` (Gaze): Recomputed = `0.031310` | CSV = `0.031310` | Diff = $<10^{-16}$ | **PASS**

#### Subject: `subject_5`
*   **Raw Session in MAT**: Index 4 (Group: `off-ADHD`, Trials: 160)
*   **Gaze Availability**: Valid gaze coordinates present.
*   **Recomputation Comparison**:
    *   `accuracy_overall`: Recomputed = `0.775000` | CSV = `0.775000` | Diff = `0.000000` | **PASS**
    *   `hit_rate`: Recomputed = `0.705128` | CSV = `0.705128` | Diff = `0.000000` | **PASS**
    *   `mean_reaction_time_ms`: Recomputed = `720.288462` | CSV = `720.288462` | Diff = `0.000000` | **PASS**
    *   `rt_coefficient_of_variation`: Recomputed = `0.205686` | CSV = `0.205686` | Diff = $<10^{-16}$ | **PASS**
    *   `pupil_variability`: Recomputed = `0.082046` | CSV = `0.082046` | Diff = $<10^{-16}$ | **PASS**
    *   `normalized_fixation_instability` (Gaze): Recomputed = `0.045056` | CSV = `0.045056` | Diff = $<10^{-16}$ | **PASS**

#### Subject: `subject_8`
*   **Raw Session in MAT**: Index 7 (Group: `off-ADHD`, Trials: 160)
*   **Gaze Availability**: Valid gaze coordinates present.
*   **Recomputation Comparison**:
    *   `accuracy_overall`: Recomputed = `0.906250` | CSV = `0.906250` | Diff = `0.000000` | **PASS**
    *   `hit_rate`: Recomputed = `0.912500` | CSV = `0.912500` | Diff = `0.000000` | **PASS**
    *   `mean_reaction_time_ms`: Recomputed = `794.617834` | CSV = `794.617834` | Diff = `0.000000` | **PASS**
    *   `rt_coefficient_of_variation`: Recomputed = `0.245871` | CSV = `0.245871` | Diff = `0.000000` | **PASS**
    *   `pupil_variability`: Recomputed = `0.123546` | CSV = `0.123546` | Diff = $<10^{-16}$ | **PASS**
    *   `normalized_fixation_instability` (Gaze): Recomputed = `0.070329` | CSV = `0.070329` | Diff = $<10^{-16}$ | **PASS**

---

### Control Participants

#### Subject: `subject_33`
*   **Raw Session in MAT**: Index 49 (Group: `Ctrl`, Trials: 160)
*   **Gaze Availability**: Valid gaze coordinates present.
*   **Recomputation Comparison**:
    *   `accuracy_overall`: Recomputed = `0.656250` | CSV = `0.656250` | Diff = `0.000000` | **PASS**
    *   `hit_rate`: Recomputed = `0.714286` | CSV = `0.714286` | Diff = `0.000000` | **PASS**
    *   `mean_reaction_time_ms`: Recomputed = `913.345324` | CSV = `913.345324` | Diff = `0.000000` | **PASS**
    *   `rt_coefficient_of_variation`: Recomputed = `0.236880` | CSV = `0.236880` | Diff = $<10^{-16}$ | **PASS**
    *   `pupil_variability`: Recomputed = `0.080980` | CSV = `0.080980` | Diff = $<10^{-16}$ | **PASS**
    *   `normalized_fixation_instability` (Gaze): Recomputed = `0.029116` | CSV = `0.029116` | Diff = $<10^{-16}$ | **PASS**

#### Subject: `subject_38`
*   **Raw Session in MAT**: Index 54 (Group: `Ctrl`, Trials: 160)
*   **Gaze Availability**: Valid gaze coordinates present.
*   **Recomputation Comparison**:
    *   `accuracy_overall`: Recomputed = `0.837500` | CSV = `0.837500` | Diff = `0.000000` | **PASS**
    *   `hit_rate`: Recomputed = `0.839506` | CSV = `0.839506` | Diff = `0.000000` | **PASS**
    *   `mean_reaction_time_ms`: Recomputed = `772.197452` | CSV = `772.197452` | Diff = `0.000000` | **PASS**
    *   `rt_coefficient_of_variation`: Recomputed = `0.239805` | CSV = `0.239805` | Diff = $<10^{-16}$ | **PASS**
    *   `pupil_variability`: Recomputed = `0.069241` | CSV = `0.069241` | Diff = `0.000000` | **PASS**
    *   `normalized_fixation_instability` (Gaze): Recomputed = `0.055123` | CSV = `0.055123` | Diff = $<10^{-16}$ | **PASS**

#### Subject: `subject_40`
*   **Raw Session in MAT**: Index 56 (Group: `Ctrl`, Trials: 160)
*   **Gaze Availability**: Valid gaze coordinates present.
*   **Recomputation Comparison**:
    *   `accuracy_overall`: Recomputed = `0.825000` | CSV = `0.825000` | Diff = `0.000000` | **PASS**
    *   `hit_rate`: Recomputed = `0.851852` | CSV = `0.851852` | Diff = `0.000000` | **PASS**
    *   `mean_reaction_time_ms`: Recomputed = `850.509677` | CSV = `850.509677` | Diff = `0.000000` | **PASS**
    *   `rt_coefficient_of_variation`: Recomputed = `0.239387` | CSV = `0.239387` | Diff = $<10^{-16}$ | **PASS**
    *   `pupil_variability`: Recomputed = `0.064399` | CSV = `0.064399` | Diff = $<10^{-16}$ | **PASS**
    *   `normalized_fixation_instability` (Gaze): Recomputed = `0.058194` | CSV = `0.058194` | Diff = $<10^{-16}$ | **PASS**

*Lineage certification is fully validated and spot checks show zero deviations.*

---

## 4. Scientific Concordance
Descriptive and inferential tests verify that the unmedicated ADHD group shows statistically significant performance drops in overall accuracy ($p=0.0017$) and spatial target hit rates ($p=0.0040$) relative to Controls. Machine learning cross-validation confirms that simple behavioral and reaction-time variability features are the primary classification drivers, while eye-tracking gaze parameters do not provide significant incremental value.

This data lineage is formally certified for submission to scientific publication venues.
