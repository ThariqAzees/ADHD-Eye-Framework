# Feature Definitions for Paper

This document lists and defines all features extracted from the Rojas-Líbano et al. (2019) dataset and used in the final clinical ADHD classification models.

---

## Behavioral Features

### 1. `accuracy_overall`
*   **Category**: Behavioral
*   **Mathematical Definition**: 
    $$	ext{Accuracy Overall} = rac{N_{	ext{correct}}}{N_{	ext{total}}}$$
*   **Unit**: Ratio ($0.0$ to $1.0$)
*   **Source Variables**: `Task_epocs.Perform` (value $1$ is correct, $0$ is error/omission).
*   **Aggregation Method**: Mean over all trials.
*   **Scientific Interpretation**: Represents working-memory matching capacity and response accuracy.
*   **Measurement**: Directly measured trial outcomes.
*   **ML Inclusion**: YES (Primary feature).
*   **Limitations**: Does not capture distractor or working memory load effects.

### 2. `accuracy_by_load_diff`
*   **Category**: Behavioral
*   **Mathematical Definition**: 
    $$	ext{Acc}_{	ext{Load 1}} - 	ext{Acc}_{	ext{Load 2}}$$
*   **Unit**: Ratio difference
*   **Source Variables**: `Task_epocs.Perform` filtered by `Task_epocs.Load` ($1$ dot vs. $2$ dots).
*   **Aggregation Method**: Mean accuracy under Load 1 minus mean accuracy under Load 2.
*   **Scientific Interpretation**: Measures working memory decay and capacity limits as cognitive load increases.
*   **Measurement**: Engineered difference score.
*   **ML Inclusion**: YES.
*   **Limitations**: Limited to 2 load levels in the paradigm.

### 3. `accuracy_by_distractor_diff`
*   **Category**: Behavioral
*   **Mathematical Definition**: 
    $$	ext{Acc}_{	ext{No Distractor}} - 	ext{Acc}_{	ext{Emotional Distractor}}$$
*   **Unit**: Ratio difference
*   **Source Variables**: `Task_epocs.Perform` filtered by `Task_epocs.Distr` ($4$ = empty grid vs. $6$ = emotional face).
*   **Aggregation Method**: Mean accuracy under no-distractor trials minus mean accuracy under emotional distractor trials.
*   **Scientific Interpretation**: Measures emotional vulnerability and failure of filtering mechanisms.
*   **Measurement**: Engineered difference score.
*   **ML Inclusion**: YES.
*   **Limitations**: Emotional faces represent only one type of cognitive distractor.

### 4. `omission_rate`
*   **Category**: Behavioral
*   **Mathematical Definition**: 
    $$rac{N_{	ext{omission}}}{N_{	ext{total}}}$$
*   **Unit**: Ratio ($0.0$ to $1.0$)
*   **Source Variables**: Omission trials are defined by `Task_epocs.RTime == 0`.
*   **Aggregation Method**: Sum of omission trials divided by total trials.
*   **Scientific Interpretation**: Indicates severe attentional disengagement, sleepiness, or disengagement.
*   **Measurement**: Directly measured trial response failures.
*   **ML Inclusion**: YES.

### 5. `false_alarm_rate`
*   **Category**: Behavioral
*   **Mathematical Definition**: 
    $$rac{N_{	ext{incorrect mismatch selections}}}{N_{	ext{mismatch trials}}}$$
*   **Unit**: Ratio ($0.0$ to $1.0$)
*   **Source Variables**: Trials where target is mismatch (`Task_epocs.Match == 0`) but response is incorrect (`Task_epocs.Perform == 0`).
*   **Aggregation Method**: Ratio of incorrect responses on mismatch trials.
*   **Scientific Interpretation**: Measures inhibitory control failure and motor impulsivity.
*   **Measurement**: Engineered ratio.
*   **ML Inclusion**: YES.

### 6. `hit_rate`
*   **Category**: Behavioral
*   **Mathematical Definition**: 
    $$rac{N_{	ext{correct match selections}}}{N_{	ext{match trials}}}$$
*   **Unit**: Ratio ($0.0$ to $1.0$)
*   **Source Variables**: Trials where target is match (`Task_epocs.Match == 1`) and response is correct (`Task_epocs.Perform == 1`).
*   **Aggregation Method**: Ratio of correct responses on match trials.
*   **Scientific Interpretation**: Standard target recognition capacity.
*   **Measurement**: Engineered ratio.
*   **ML Inclusion**: YES.

---

## Reaction Time Features

### 7. `mean_reaction_time_ms`
*   **Category**: Reaction Time
*   **Mathematical Definition**: Mean of `Task_epocs.RTime` for correct trials.
*   **Unit**: milliseconds (ms)
*   **Source Variables**: `Task_epocs.RTime` for correct response trials.
*   **Aggregation Method**: Mean.
*   **Scientific Interpretation**: General processing speed.
*   **Measurement**: Directly measured.
*   **ML Inclusion**: YES.

### 8. `median_reaction_time_ms`
*   **Category**: Reaction Time
*   **Mathematical Definition**: Median of `Task_epocs.RTime` for correct trials.
*   **Unit**: milliseconds (ms)
*   **Source Variables**: `Task_epocs.RTime` for correct response trials.
*   **Aggregation Method**: Median.
*   **Scientific Interpretation**: Robust processing speed, resistant to outliers/skew.
*   **Measurement**: Directly measured.
*   **ML Inclusion**: YES.

### 9. `rt_variability`
*   **Category**: Reaction Time
*   **Mathematical Definition**: Standard deviation of `Task_epocs.RTime` for correct trials.
*   **Unit**: milliseconds (ms)
*   **Source Variables**: `Task_epocs.RTime` for correct response trials.
*   **Aggregation Method**: Sample standard deviation.
*   **Scientific Interpretation**: Intra-individual response variability, a primary cognitive marker of ADHD.
*   **Measurement**: Engineered.
*   **ML Inclusion**: YES.

### 10. `rt_coefficient_of_variation`
*   **Category**: Reaction Time
*   **Mathematical Definition**: 
    $$	ext{RT CV} = rac{	ext{RT SD}}{	ext{RT Mean}}$$
*   **Unit**: Ratio
*   **Source Variables**: Derived from `rt_variability` and `mean_reaction_time_ms`.
*   **Aggregation Method**: SD divided by Mean.
*   **Scientific Interpretation**: Normalized index of attentional instability and periodic lapse frequency.
*   **Measurement**: Engineered.
*   **ML Inclusion**: YES.

---

## Gaze Features

### 11. `normalized_fixation_instability`
*   **Category**: Gaze
*   **Mathematical Definition**: 
    $$	ext{RMSD} = \sqrt{rac{1}{N}\sum (x_t - ar{x})^2 + (y_t - ar{y})^2}$$
    during the delay (fixation) epoch.
*   **Unit**: Normalized screen coordinate units
*   **Source Variables**: Continuous `Gaze` coordinates from trial start to probe start, excluding encoding.
*   **Aggregation Method**: RMS deviation of gaze coordinates.
*   **Scientific Interpretation**: Measures spatial gaze stability and occurrence of micro-saccades during delay epochs.
*   **Measurement**: Engineered.
*   **ML Inclusion**: YES.
*   **Limitations**: Two engineered gaze-stability features had valid coordinate data in 14 of 40 sessions (35%); 26 sessions (65%) lacked valid continuous gaze coordinates for these two engineered features. Handled via mean imputation within cross-validation folds.

### 12. `normalized_gaze_dispersion`
*   **Category**: Gaze
*   **Mathematical Definition**: 
    $$	ext{RMSD}$$
    during the encoding (dot stimulus display) epoch.
*   **Unit**: Normalized screen coordinate units
*   **Source Variables**: Continuous `Gaze` coordinates during the first $2000$ ms of the trial.
*   **Aggregation Method**: RMS deviation.
*   **Scientific Interpretation**: Measures spatial search visual spread during memory encoding.
*   **Measurement**: Engineered.
*   **ML Inclusion**: YES.
*   **Limitations**: Two engineered gaze-stability features had valid coordinate data in 14 of 40 sessions (35%); 26 sessions (65%) lacked valid continuous gaze coordinates for these two engineered features. Handled via mean imputation within cross-validation folds.

---

## Pupil Features

### 13. `pupil_variability`
*   **Category**: Pupil
*   **Mathematical Definition**: 
    Standard deviation of average trial pupil sizes.
*   **Unit**: Arbitrary unit (relative to session z-score)
*   **Source Variables**: Trial-level pupil means derived from continuous tracking data.
*   **Aggregation Method**: Standard deviation of mean pupil sizes across all trials.
*   **Scientific Interpretation**: Represents tonic autonomic arousal stability, reflecting locus coeruleus norepinephrine (LC-NE) dysregulation.
*   **Measurement**: Engineered.
*   **ML Inclusion**: YES.
*   **Limitations**: High blink artifacts in clinical cohorts; trials with >50% blinks are filtered out.

---

## Excluded Legacy Features

### `mean_pupil_proxy` (EXCLUDED)
*   **Description**: Session-level mean pupil size.
*   **Status**: **EXCLUDED** from final corrected machine learning models.
*   **Scientific Reason**: The raw Figshare pupil dataset is z-scored at the session/frame level, forcing the absolute mean of each session to be mathematically close to `0.0`. Including it in ML introduces artifactual leakage: since ADHD subjects blink more (yielding more NaNs), their valid frame averages skew slightly. The model exploits this missingness artifact rather than any physiological pupil marker.

### `mean_fixation_stability` (EXCLUDED)
*   **Description**: Average gaze deviation over the whole session.
*   **Status**: **EXCLUDED** (superseded by `normalized_fixation_instability` and `normalized_gaze_dispersion` which isolate specific cognitive epochs).