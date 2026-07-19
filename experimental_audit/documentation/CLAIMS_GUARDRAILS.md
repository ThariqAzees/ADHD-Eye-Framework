# Claims Guardrails

This document provides a set of strict guidelines to prevent Claude from making exaggerated, unscientific, or unsupported claims in the conference paper.

---

## 1. Safe to Claim
*   Unmedicated ADHD participants show a statistically significant deficit in overall task accuracy and match hit rates compared to Controls ($p < 0.005$ FDR corrected).
*   Unmedicated ADHD participants show larger response time variability (RT CV) and autonomic pupil fluctuation (pupil variability) with large/medium effect sizes ($d = -1.05$ for accuracy, $+0.75$ for RT CV, $+0.67$ for pupil variability).
*   Behavioral performance metrics alone represent the strongest predictors of ADHD-associated cognitive patterns during the delayed-recognition working-memory task.
*   Single-feature models using overall task accuracy outperform high-dimensional multi-modal models, illustrating clinical Occam's Razor.
*   Double-loop Nested Cross-Validation represents the correct methodology to prevent hyperparameter leakage, revealing true clinical classification limits compared to naive CV splits.

---

## 2. Claim Only with Caution
*   Reaction-time variability and pupil variability can separate ADHD and Control classes. (Caution: While they show large effect sizes, their individual Mann-Whitney p-values do **not** survive FDR corrections. They must be characterized as promising *exploratory* biomarkers requiring larger cohorts).
*   Machine learning models can differentiate ADHD from Controls with $82.5\%$ accuracy. (Caution: Balanced Accuracy is $76.0\%$, and ROC-AUC is $0.690$. Apparent F1 is inflated by majority-class prevalence. Permutation tests on ROC-AUC are **not significant** ($p = 0.0909$). Model claims must be described as moderate, biased toward the majority class, and exploratory).

---

## 3. Do NOT Claim
*   **Do NOT claim** that our machine learning system can "diagnose" ADHD, screen patients, or be used as a "clinical diagnostic system".
*   **Do NOT claim** that gaze and pupil features provide significant incremental value or synergistic predictive information when combined with behavioral baselines. (They degrade performance).
*   **Do NOT claim** that low-cost webcams or MediaPipe iris tracking have been validated on ADHD cohorts. (Webcam features are a completely separate prototype evaluated on healthy testers only; all paper classification results derive from EyeLink 1000 laboratory data).
*   **Do NOT claim** that the machine learning results are globally significant. (ROC-AUC permutation tests are not significant).