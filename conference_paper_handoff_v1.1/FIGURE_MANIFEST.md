# Figure Manifest for Paper (v1.1)

This manifest lists all 22 PNG figures generated during the experimental audit, classifying them by recommendation status (RECOMMENDED FOR PAPER, OPTIONAL/SUPPLEMENTARY, or DO NOT USE), along with captions and recommended figure numbers.

---

### Recommended For Main Paper

| Filename | Modality / Purpose | Recommended Figure No. | Recommended Caption | Safe Interpretation |
| :--- | :--- | :---: | :--- | :--- |
| `roc_curves.png` | Model ROC curve | **Figure 3 (Left)** | Receiver Operating Characteristic (ROC) curves of the Logistic Regression, Random Forest, and XGBoost models evaluated using Stratified 5-Fold Nested Cross-Validation. | Displays threshold-independent discrimination; Random Forest shows moderate performance (ROC-AUC = 0.69) but is not statistically significant. |
| `pr_curves.png` | Model PR curve | **Figure 3 (Right)** | Precision-Recall (PR) curves for the three models, showing classification threshold boundaries against the naive majority-class baseline (0.70). | Displays precision decay at high recall; the naive baseline is 0.70. |
| `confusion_matrices.png` | Confusion matrices | **Figure 3 (Center)** | Confusion matrices showing predicted vs. true classes (Control and ADHD) for the three nested cross-validated classifiers. | Provides the absolute counts and proportions of true/false positives and negatives. |
| `ablation_study_accuracy.png` | Feature ablation comparison | **Figure 4** | Feature ablation results comparing classification performance (ROC-AUC and F1-Score) across the 9 feature groups. | Visually demonstrates that Behavioral-only features yield the highest performance; adding eye-tracking degrades AUC. |
| `boxplot_accuracy_overall.png` | Overall task accuracy boxplot | **Figure 2 (A)** | Boxplot comparing overall task response accuracy between unmedicated ADHD and healthy Control subjects. | Shows the primary statistical difference (p=0.0017 FDR-corrected); ADHD shows significant cognitive deficit. |
| `boxplot_rt_coefficient_of_variation.png` | Reaction time variation boxplot | **Figure 2 (B)** | Boxplot comparing reaction time coefficient of variation between unmedicated ADHD and healthy Control subjects. | Displays larger variance in ADHD (d = +0.75), but does not survive FDR correction. |
| `boxplot_hit_rate.png` | Target recognition hit rate boxplot | **Figure 2 (C)** | Boxplot comparing target recognition match hit rates between unmedicated ADHD and healthy Control subjects. | Shows significant target-recognition deficit in unmedicated ADHD (p=0.0040 FDR-corrected). |

---

### Optional / Supplementary Appendix Figures

| Filename | Modality / Purpose | Recommended Appendix Fig. | Recommended Caption | Safe Interpretation |
| :--- | :--- | :---: | :--- | :--- |
| `boxplot_rt_variability.png` | RT standard deviation boxplot | **Appendix Fig. 1** | Boxplot showing raw reaction time standard deviation (ms) for correct trials. | ADHD has higher SD (d = +0.68) but does not survive FDR correction. |
| `boxplot_mean_reaction_time_ms.png` | Mean reaction time boxplot | **Appendix Fig. 2** | Boxplot showing mean reaction time (ms) for correct trials. | Processing speed difference is not statistically significant between groups. |
| `boxplot_median_reaction_time_ms.png` | Median reaction time boxplot | **Appendix Fig. 3** | Boxplot showing median reaction time (ms) for correct trials. | Processing speed medians are not statistically significant. |
| `boxplot_omission_rate.png` | Attention lapses omission rate | **Appendix Fig. 4** | Boxplot showing trial omission rates. | ADHD shows more lapses (d = +0.61) but does not survive FDR. |
| `boxplot_accuracy_by_load_diff.png` | Load decay accuracy boxplot | **Appendix Fig. 5** | Boxplot showing accuracy decay under Load 2. | Memory load effect is similar between groups. |
| `boxplot_accuracy_by_distractor_diff.png` | Emotional capture boxplot | **Appendix Fig. 6** | Boxplot showing distractor emotional capture. | Emotional face interference is not significantly different. |
| `model_calibration_curves.png` | Calibration curves | **Appendix Fig. 7** | Calibration curves for the Logistic Regression, Random Forest, and XGBoost models. | Assesses probability calibration; Random Forest shows high overconfidence. |
| `learning_curve_random_forest.png` | RF Learning curve | **Appendix Fig. 8** | Training and validation F1-scores as a function of training sample size. | RF shows high training overfitting and flat validation progress. |
| `learning_curve_logistic_regression.png` | LR Learning curve | **Appendix Fig. 9** | Training and validation F1-scores for Logistic Regression. | Shows linear classifier fitting limits. |
| `learning_curve_xgboost.png` | XGBoost Learning curve | **Appendix Fig. 10** | Training and validation F1-scores for XGBoost. | Shows high training overfitting. |
| `permutation_test_random_forest.png` | RF Permutation shuffle | **Appendix Fig. 11** | Permutation null distribution vs observed score for Random Forest. | F1 is significant due to imbalance bias, but AUC is not significant. |
| `permutation_test_logistic_regression.png` | LR Permutation shuffle | **Appendix Fig. 12** | Permutation null distribution vs observed score for Logistic Regression. | Not statistically significant. |
| `permutation_test_xgboost.png` | XGBoost Permutation shuffle | **Appendix Fig. 13** | Permutation null distribution vs observed score for XGBoost. | Not statistically significant. |

---

### Do Not Use (Legacy Figures / Normalization Artifacts)

| Filename | Modality / Purpose | Reason for Exclusion |
| :--- | :--- | :--- |
| `boxplot_mean_pupil_proxy.png` | Legacy pupil proxy boxplot | Excluded as a session-level normalization artifact (blinks) rather than a biological pupil size biomarker. |
| `boxplot_mean_fixation_stability.png` | Legacy fixation stability boxplot | Excluded. Gaze stability is analyzed specifically during encoding/delay epochs in main figures. |
| `boxplot_false_alarm_rate.png` | False alarm rate boxplot | Excluded. False alarm rate is zero for all participants in this cohort. |