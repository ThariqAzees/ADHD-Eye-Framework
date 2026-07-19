# Legacy Provenance Forensic Report

This report documents the forensic tracing of `dataset_provenance.csv` and `dataset_integrity_report.csv`, which were discovered to describe the legacy synthetic dataset rather than the verified real-data clinical cohort.

---

## 1. Forensic Summary

| Parameter | `dataset_provenance.csv` | `dataset_integrity_report.csv` |
| :--- | :--- | :--- |
| **Current Path** | `experimental_audit/results/dataset_provenance.csv` | `experimental_audit/results/dataset_integrity_report.csv` |
| **SHA-256 Hash** | `5c9082c0a9454aec26b70e5cdb45cdd689ceb435a6383224981645a985b3e178` | `9c662e44bc7e761f2e22298248059855b57ab73e097accc56c6f51409ad41af4` |
| **Creation Script** | `experimental_audit/scripts/run_audit_experiments.py` | `experimental_audit/scripts/run_audit_experiments.py` |
| **Input Dataset Used** | `data/processed/dataset_features_v1.0.csv` (stale synthetic file) | `data/processed/dataset_features_v1.0.csv` (stale synthetic file) |
| **Output Described** | Old synthetic cohort of 50 subjects | Old synthetic cohort of 50 subjects |
| **Last Modified Time** | `2026-07-18 12:07:56` | `2026-07-18 12:07:56` |
| **Creation Stage** | Run *before* the real-data reconstruction rename | Run *before* the real-data reconstruction rename |
| **Renamed File Match** | `data/processed/dataset_features_SYNTHETIC_v1.0.csv` | `data/processed/dataset_features_SYNTHETIC_v1.0.csv` |
| **Copied in Handoff?** | Yes, by `build_handoff_package.py` / `reconcile_and_build_handoff_v1.1.py` | Yes, by `build_handoff_package.py` / `reconcile_and_build_handoff_v1.1.py` |

---

## 2. Forensic Timeline & Git History

1. **Before July 18th**: The repository contained `data/processed/dataset_features_v1.0.csv` as its main processed features file, which was generated from a mock synthetic MATLAB file.
2. **On July 18th, 12:07:07**: The previous developer last modified `experimental_audit/scripts/run_audit_experiments.py`.
3. **On July 18th, 12:07:56**: The developer ran `python experimental_audit/scripts/run_audit_experiments.py`. This script loaded the synthetic `data/processed/dataset_features_v1.0.csv` file, computed its metrics, and generated `dataset_provenance.csv` and `dataset_integrity_report.csv` in `experimental_audit/results/`.
4. **On July 18th, 00:41:27 (Commit `b774060`)**: The developer completed the real-data reconstruction download and parsing, generating the authentic `data/processed/dataset_features_REAL_v1.0.csv`. In this same commit, they:
   * Renamed the synthetic `dataset_features_v1.0.csv` to `data/processed/dataset_features_SYNTHETIC_v1.0.csv`.
   * Pushed the code and experimental audit results.
   * However, they did NOT modify or re-run `run_audit_experiments.py` on `dataset_features_REAL_v1.0.csv`. Consequently, `dataset_provenance.csv` and `dataset_integrity_report.csv` remained stale synthetic legacy artifacts.
5. **In the Handoff Packaging Scripts**: The packaging scripts utilized broad copy operations to move files from `experimental_audit/results/` to the handoff package, which copied the stale synthetic files into `conference_paper_handoff/` and `conference_paper_handoff_v1.1/` as "authoritative" documents.

---

## 3. Impact Assessment
* **Did they affect the ML models or statistical results?** **NO.** The machine learning models and descriptive/inferential statistical tables were generated from the authentic `dataset_features_REAL_v1.0.csv` via separate scripts (`run_real_data_reconstruction.py` and `generate_publication_evidence.py`).
* **Conclusion**: These files are legacy synthetic development artifacts and must be removed from the publication package and replaced with updated, real-data provenance files.
