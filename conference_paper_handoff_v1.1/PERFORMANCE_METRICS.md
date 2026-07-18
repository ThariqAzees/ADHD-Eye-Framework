# Performance Metrics Definitions

This document lists the mathematical definitions of the performance metrics and explains their significance under the clinical class imbalance.

---

## 1. Metric Formulas

*   **Accuracy**:
    $$	ext{Accuracy} = rac{TP + TN}{TP + TN + FP + FN}$$
*   **Balanced Accuracy**:
    $$	ext{Balanced Accuracy} = rac{	ext{Sensitivity} + 	ext{Specificity}}{2}$$
    where Sensitivity $= rac{TP}{TP + FN}$ and Specificity $= rac{TN}{TN + FP}$.
*   **Precision**:
    $$	ext{Precision} = rac{TP}{TP + FP}$$
*   **Recall / Sensitivity**:
    $$	ext{Recall} = rac{TP}{TP + FN}$$
*   **Specificity**:
    $$	ext{Specificity} = rac{TN}{TN + FP}$$
*   **F1-Score**:
    $$	ext{F1} = 2 	imes rac{	ext{Precision} 	imes 	ext{Recall}}{	ext{Precision} + 	ext{Recall}}$$
*   **ROC-AUC**: Area under the Receiver Operating Characteristic curve (plotting Sensitivity vs. 1 - Specificity across decision thresholds).
*   **PR-AUC**: Area under the Precision-Recall curve (plotting Precision vs. Recall across thresholds).

---

## 2. Importance Under Clinical Class Imbalance

Our cohort features an imbalance of **28 ADHD (70.0%)** vs. **12 Control (30.0%)**:
1.  **Majority Class Baseline**: A naive classifier predicting the majority class (ADHD) for all instances achieves an Accuracy of **70.0%** and an F1-score of **82.35%** with zero clinical discriminative power.
2.  **Balanced Accuracy Significance**: By averaging sensitivity and specificity, Balanced Accuracy prevents majority-class bias. A naive classifier gets exactly **50.0%** Balanced Accuracy.
3.  **ROC-AUC & PR-AUC Significance**: These metrics evaluate threshold-independent discrimination, making them robust to prevalence shifts. PR-AUC is highly sensitive to false positives, making it critical for diagnostic screening.