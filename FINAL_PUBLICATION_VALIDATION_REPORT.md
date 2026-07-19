# Final Publication Validation Report

**Total Checks Run**: 15
**Passed**: 15
**Failed**: 0
**Status**: PASS

| Check Name | Status | Details |
| :--- | :---: | :--- |
| REAL CSV Cohort Count | PASS | N=40 (Expected 40) |
| REAL CSV Class Balance | PASS | ADHD=28, Control=12 (Expected 28, 12) |
| Descriptive Statistics Recomputation | PASS | All descriptive stats match CSV recomputation |
| Inferential Statistics Recomputation | PASS | All U-statistics, p-values, and Cohen's d match SciPy recomputation |
| Narrative U-statistics in Report | PASS | PUBLICATION_EVIDENCE_REPORT.md table matches SciPy exactly (U=232.0 and U=231.0) |
| Report Executive Summary SDs | PASS | ADHD $0.6114 \pm 0.1798$ and Control $0.7813 \pm 0.1024$ are present |
| Feature Lineage Real Status | PASS | Found 0 features labeled SYNTHETIC (Expected 0) |
| Dataset Provenance describes REAL data | PASS | Provenance records 67 sessions, 0% synthetic data |
| Dataset Integrity describes REAL N=40 data | PASS | Integrity shows 17 columns and exactly 26 nulls for gaze stability |
| Raw MAT SHA-256 Match | PASS | MAT SHA: 44AA997E37... (Expected 44AA997E37...) |
| Processed CSV SHA-256 Match | PASS | CSV SHA: CB3760A29D... (Expected CB3760A29D...) |
| ML/Ablation/Permutation Input Integrity | PASS | generate_publication_evidence.py loads dataset_features_REAL_v1.0.csv |
| No Legacy Handoff Embedded | PASS | No nested handoff folders found in staging directory |
| No Unallowlisted Files Included | PASS | All files in staging directory are in the allowlist |
| No Stale U-statistics in KEY_VERIFIED_NUMBERS.md | PASS | Stale values 227.0 and 225.0 are not present |