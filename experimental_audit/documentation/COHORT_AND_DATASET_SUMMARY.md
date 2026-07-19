# Cohort and Dataset Summary

This document summarizes the clinical participant cohort and the inclusion/exclusion criteria applied to the data for the final conference paper.

---

## 1. Source Cohort vs. Analyzable Cohort

*   **Source Figure Dataset**:
    *   **50 unique participants** (28 diagnosed with ADHD, 22 healthy Controls).
    *   **67 recorded sessions** total (including 17 repeated medicated ADHD sessions).
*   **Final Analyzable Cohort**:
    *   **$N = 40$ unique participants** (28 unmedicated ADHD + 12 healthy Controls).
    *   One session per unique individual (preventing repeated-measures leakage).

---

## 2. Exclusion Rationale and Criteria

### Exclusion 1: Medicated Sessions (`on-ADHD`)
*   **Count Excluded**: 17 sessions.
*   **Rationale**: The 17 sessions recorded under methylphenidate (`on-ADHD`) are repeated measurements of individuals already present in the unmedicated ADHD group. Including them in the primary ADHD-vs-Control classifier violates the assumption of independence, introduces leakage, and biases performance. Isolating the unmedicated sessions allows for clean baseline clinical classification.

### Exclusion 2: Incomplete/Unusable Controls
*   **Count Excluded**: 10 Control sessions.
*   **Exclusion Details**:
    *   *Aborted Runs*: Subjects 41, 46, and 47 aborted the task immediately (only 1 trial recorded).
    *   *Missing Trial Structures*: Subjects 42, 43, 44, 45, 48, 49, and 50 are missing continuous trial structure fields (`Task_epocs` cell arrays) in the raw MATLAB file, preventing feature extraction.

---

## 3. Cohort Inclusion Table

| Participant ID | Clinical Group | Session ID | Status | Inclusion/Exclusion Reason |
| :--- | :--- | :--- | :--- | :--- |
| `subject_1` to `subject_28` | ADHD (unmedicated) | Session 1 | **INCLUDED** | Primary clinical unmedicated ADHD cohort. |
| `subject_29` to `subject_40` | Healthy Control | Session 1 | **INCLUDED** | Valid control sessions with complete trial structures. |
| `subject_41` | Healthy Control | Session 1 | EXCLUDED | Aborted session (only 1 trial). |
| `subject_42` to `subject_45` | Healthy Control | Session 1 | EXCLUDED | Missing trial structure cell arrays in MATLAB file. |
| `subject_46` | Healthy Control | Session 1 | EXCLUDED | Aborted session (only 1 trial). |
| `subject_47` | Healthy Control | Session 1 | EXCLUDED | Aborted session (only 1 trial). |
| `subject_48` to `subject_50` | Healthy Control | Session 1 | EXCLUDED | Missing trial structure cell arrays in MATLAB file. |
| Repeated sessions | ADHD (medicated) | Session 2 | EXCLUDED | Repeated measurements under medication (`on-ADHD`). |

---

## 4. Participant-Leakage Prevention
*   **Unit of Analysis**: One row per unique participant ($N=40$ total rows).
*   **Split Strategy**: Folds in the Stratified K-Fold cross-validation are divided at the participant level. No data from a single participant ever appears in both the training and testing sets of a fold, ensuring strict leakage prevention.