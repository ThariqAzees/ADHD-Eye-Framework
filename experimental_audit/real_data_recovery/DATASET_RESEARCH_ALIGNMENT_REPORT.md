# Dataset–Research Alignment Audit Report

This report presents a rigorous methodological audit and scientific alignment analysis of the Rojas-Líbano et al. (2019) dataset (`Pupil_dataset.mat`) and its suitability for the ADHD Eye Framework project.

---

## 1. Exact Details of the Original Study
Based on the peer-reviewed publication associated with the authentic dataset:

*   **Full Dataset Title**: A pupil size, eye-tracking and neuropsychological dataset from ADHD children during a cognitive task.
*   **Full Paper Title**: A pupil size, eye-tracking and neuropsychological dataset from ADHD children during a cognitive task.
*   **Authors**: Daniel Rojas-Líbano, Gabriel Wainstein, Ximena Carrasco, Francisco Aboitiz, Nicolás Crossley, and Tomás Ossandón.
*   **Year**: 2019.
*   **DOI of Publication**: [10.1038/s41597-019-0037-2](https://doi.org/10.1038/s41597-019-0037-2).
*   **Figshare DOI**: [10.6084/m9.figshare.7218725](https://doi.org/10.6084/m9.figshare.7218725).
*   **Participant Population**: Children and adolescents aged 7 to 17 years old.
*   **ADHD/Control Composition**: 50 unique individuals total: 28 diagnosed with ADHD, 22 typically developing healthy controls. 
    *   *Recording Sessions (67 total)*: 28 unmedicated ADHD sessions (`off-ADHD`), 17 medicated repeated ADHD sessions (`on-ADHD`), and 22 healthy control sessions.
*   **Age Range**: 7 to 17 years old (ADHD group: $10.6 \pm 2.3$ years; Control group: $11.0 \pm 2.0$ years).
*   **Diagnostic/Clinical Criteria**: Clinically diagnosed by a child psychiatrist/neurologist based on the Diagnostic and Statistical Manual of Mental Disorders, Fourth/Fifth Edition (DSM-IV or DSM-5) criteria, semi-structured interviews, and validated clinical questionnaires (Conners' rating scales). General cognitive function was evaluated using WISC-III/IV subtest scores.
*   **Medication Conditions**: ADHD participants treated with methylphenidate underwent a wash-out period of at least 24 hours (typically 48 hours) prior to the `off-ADHD` session. The repeated `on-ADHD` sessions were conducted under the participants' regular medication regime.
*   **Eye-Tracking Hardware**: SR Research EyeLink 1000 tower-mount eye tracker.
*   **Sampling Rate**: 1000 Hz (both gaze position and pupil size).
*   **Cognitive Task Used**: A delayed visuospatial working-memory task adapted from Dolcos & McCarthy (2006).
*   **Number of Trials**: 160 trials per recording session.
*   **Experimental Conditions**:
    *   *Working Memory Load*: 1 dot (Load 1) or 2 dots (Load 2) presented across consecutive arrays.
    *   *Distractor Types*: Task-related dot arrays (Class 5), neutral natural images (Class 3), emotional images (Class 6), or empty grid/none (Class 4).
*   **Behavioral Measurements**: Behavioral response correctness (0 or 1), response type (target/lure button), and reaction time (ms).
*   **Eye-Tracking Measurements**: Continuous gaze coordinates ($X, Y$ in screen pixels) mapped onto the display canvas.
*   **Pupil Measurements**: Continuous pupil size time series (arbitrary units, z-scored at the session/frame level).

---

## 2. Verification of Cognitive Task Paradigm
**Verdict**: **C. A visuospatial Sternberg working-memory task** (specifically, a delayed-recognition visuospatial working-memory task utilizing a Sternberg-type sequence).

### Task Sequence Description
Each of the 160 trials is structured as follows:

$$\text{Encoding (Memoranda)} \longrightarrow \text{Retention Delay (Distractor)} \longrightarrow \text{Retrieval (Probe)} \longrightarrow \text{Response} \longrightarrow \text{Feedback}$$

1.  **Encoding (Memoranda)**: 
    *   Participants are shown a sequence of **three consecutive dot-arrays** on a $4 \times 4$ grid. 
    *   Each grid is presented for **750 ms**, separated by a **500 ms** fixation cross screen.
    *   Each array contains either **1 dot** (Load 1) or **2 dots** (Load 2) in pseudorandom spatial locations.
    *   *What is memorized*: The precise spatial locations (out of 16 coordinates) of the dots presented in the grid.
2.  **Retention Delay (Distractor)**:
    *   Following the encoding phase, a delay period is introduced during which a **distractor image** is shown for **1500 ms**.
    *   *Distractor conditions*: A task-related dot array, a neutral natural image, emotionally valenced image, or no distractor (empty grid).
    *   *What participants do*: Maintain the spatial locations of the encoded dots in working memory while ignoring or filtering out the distractor.
3.  **Probe (Retrieval)**:
    *   A single probe dot is displayed on the grid for **1.5 seconds**.
4.  **Response**:
    *   The participant has a response window to press one of two keys indicating whether the probe dot occupies a location identical to *any* of the dots memorized during the encoding phase (Target = Match, Lure = Mismatch).
5.  **Feedback**:
    *   Performance feedback ("correct" or "incorrect") is displayed for **1500 ms**.

### Final Verdict on Terminology
*   **Verdict**: **CORRECT ONLY TO CALL IT A MODIFIED/VISUOSPATIAL STERNBERG-TYPE TASK**.
*   **Paper Terminology**: We must standardize on: **"a delayed visuospatial working-memory task using a Sternberg-type paradigm"** or **"a modified visuospatial Sternberg task"** in all manuscript sections.

---

## 3. Suitability for ADHD Eye-Tracking & ML Research

*   **ADHD cohort**: **YES**. Provides a clinically characterized sample ($N=28$) diagnosed by clinical psychiatric assessment and wash-out protocols.
*   **Control cohort**: **YES**. Matched healthy controls ($N=12$ after exclusions) provide a baseline comparison.
*   **Working-memory task**: **YES**. The task tests visuospatial working memory maintenance under varying loads and distractors.
*   **Behavioral accuracy**: **YES**. Trial-level accuracy allows modeling working-memory efficacy.
*   **Reaction time**: **YES**. Reaction times are recorded in milliseconds, allowing analysis of reaction-time variability (a hallmark of ADHD).
*   **Gaze information**: **YES**. High-fidelity 1000 Hz gaze coordinates are available, although limited by missing values in 26 sessions.
*   **Pupil information**: **YES**. 1000 Hz pupil trace data allows examining autonomic pupil dynamics.
*   **Distractor conditions**: **YES**. Four distractor types are available.
*   **Participant-level ML classification**: **YES, WITH LIMITATIONS**. The dataset is small ($N=40$ unique subjects), meaning that participant-level cross-validation (nested CV) is critical to prevent data leakage and inflation of performance metrics.
*   **Multimodal feature analysis**: **YES, WITH LIMITATIONS**. Allows combining behavioral, RT, gaze, and pupil features. A limitation is the 65% missing gaze coordinate rate, which requires robust imputer steps (e.g., median imputation).

---

## 4. Dataset-Selection Rationale and Feature Comparison

The Rojas-Líbano dataset was selected because it is the only publicly available dataset that provides synchronized high-fidelity eye-tracking (1000 Hz), pupillometry, trial-level behavioral performance, and reaction times for clinically characterized children with ADHD (under unmedicated off-medication and repeated medicated on-medication states) and healthy controls during a standardized visuospatial working memory task with distractor manipulation.

| Research Requirement | Dataset Provides It? | Evidence | How We Use It | Limitation |
| --- | --- | --- | --- | --- |
| Clinical ADHD cohort | **YES** | 28 ADHD subjects diagnosed via DSM-IV/V. | Target class labels (label 1). | ADHD sample is larger than the control sample (70% vs. 30%). |
| Matched controls | **YES** | 12 healthy controls with complete data. | Baseline comparison class (label 0). | 10 control sessions are corrupted/aborted, reducing controls to 12. |
| Working memory task | **YES** | 160-trial visuospatial delayed recognition task. | Behavioral accuracy measures. | Grid-dot memory task conflates visual memory capacity with attention. |
| Reaction time dynamics | **YES** | Trial-level reaction times in milliseconds. | Reaction-time variability (CV, SD, mean, median). | Extreme RT values require boundary limits (0 to 5000 ms). |
| High-resolution gaze | **YES** | EyeLink 1000 continuous gaze coordinates. | Spatial fixation stability and search dispersion. | 26 sessions lack continuous gaze data due to tracking/calibration dropouts. |
| High-resolution pupil | **YES** | EyeLink 1000 continuous pupil size series. | Mean pupil proxy and pupil variability features. | Arbitrary z-score units prevent examining absolute baseline diameter. |
| Distractor manipulation | **YES** | Four distractor valence categories. | Behavioral accuracy differences by condition. | Small number of trials per distractor sub-type. |
| Medication states | **YES** | 17 repeated ADHD sessions recorded "on-ADHD". | Quarantined for separate secondary analyses. | Repeated cohort is limited to 17 participants. |

---

## 5. Research Question Alignment
*   **Research Question**: *"Do gaze and pupil-related features provide complementary information beyond behavioral and reaction-time measures for differentiating ADHD-associated cognitive patterns during a working-memory task?"*
*   **Alignment Rating**: **STRONGLY ALIGNED**.
*   **Rationale**:
    1.  The dataset provides synchronized, multi-modal measurements of all four modalities on the same participants.
    2.  Our nested cross-validation and feature ablation experiments directly compare classifiers trained on behavioral + RT features against classifiers trained on behavioral + RT + gaze + pupil features.
    3.  The ablation F1/AUC differences and statistical Mann-Whitney U test results evaluate whether eye-tracking and pupil dynamics add predictive value.

---

## 6. Detailed Feature-Task Mapping

| Feature | Raw Dataset Variable | Task Component | Cognitive/Behavioral Interpretation | Why Relevant to ADHD | Directly Measured or Engineered |
| --- | --- | --- | --- | --- | --- |
| `accuracy_overall` | `Task_performance` | Probe Response | General task engagement and spatial working memory capacity. | ADHD exhibits lower spatial memory accuracy due to lapses in attention. | Directly Measured |
| `accuracy_by_load_diff` | `Task_performance` & `Load` | Encoding & Probe Response | Impact of cognitive load (1 vs 2 dots) on recall correctness. | ADHD subjects show steeper performance drop-offs as cognitive load increases. | Engineered |
| `accuracy_by_distractor_diff` | `Task_performance` & `Distractor` | Retention Delay & Probe Response | Ability to maintain target representation under visual/emotional distraction. | ADHD is characterized by increased distractibility and impaired emotional gating. | Engineered |
| `omission_rate` | `Task_performance` & `RTime` | Probe Response | Trials with missing or excessively delayed responses. | Reflects severe attentional lapses, task-disengagement, or extreme inattention. | Engineered |
| `false_alarm_rate` | `Task_performance` & `CorrResponse` | Probe Response | Incorrectly identifying a lure probe as a target. | Reflects motor impulsivity and failure of inhibitory response control. | Engineered |
| `hit_rate` | `Task_performance` & `CorrResponse` | Probe Response | Correctly identifying a matching target probe. | Measures baseline spatial recognition performance. | Engineered |
| `mean_reaction_time_ms` | `RTime` | Probe Response | Basic motor and processing speed during retrieval. | Slowed processing speed can occur in clinical populations. | Directly Measured |
| `median_reaction_time_ms` | `RTime` | Probe Response | Median motor response time, less sensitive to outliers. | Provides a robust baseline speed reference. | Directly Measured |
| `rt_variability` | `RTime` | Probe Response | Trial-to-trial reaction time standard deviation. | ADHD is consistently characterized by increased intra-individual RT variability. | Engineered |
| `rt_coefficient_of_variation` | `RTime` | Probe Response | Relative reaction time variability normalized by the mean speed. | A highly robust clinical marker for attentional fluctuation and lapses in ADHD. | Engineered |
| `normalized_fixation_instability` | `Position` ($X, Y$) | Central Fixation Epochs | RMS spatial gaze deviation during fixation delay. | Reflects visual inattention, micro-saccadic hyperactivity, or poor gaze control. | Engineered |
| `normalized_gaze_dispersion` | `Position` ($X, Y$) | Memoranda Encoding Epochs | Spatial spread of gaze during encoding stimulus presentations. | Measures searching patterns and spatial encoding strategy consistency. | Engineered |
| `pupil_variability` | `Pupil` | Session-level aggregate of trial means | Standard deviation of average pupil sizes across trials. | Proxy for locus coeruleus-norepinephrine (LC-NE) autonomic arousal instability. | Engineered |

### Feature Rationale Assessment
*   `accuracy_by_distractor_diff` is relatively weak in our analysis because the emotional and task-related distractors do not show statistically significant differences after FDR adjustment, and the mean difference is close to zero.

---

## 7. Distractor Relevance and Attentional Control
*   **Original Purpose**: Distractors were introduced to study cognitive control and emotional interference. Specifically, they test whether negative emotional valence or task-related visual load degrades spatial memory retention.
*   **Cognitive Mechanism**: Attentional filtering, inhibitory control, and emotional regulation. ADHD children typically show impaired inhibitory control, making them more susceptible to emotional or visual distractors.
*   **Relevance to ADHD**: Distractibility and difficulty filtering out irrelevant stimuli are core symptoms of ADHD.
*   **Defensibility of `accuracy_by_distractor_diff`**: Yes, but only as an exploratory metric. The results show that children with ADHD do not experience a significantly different distractor penalty on accuracy compared to controls in this specific task setup, which might indicate that the visuospatial grid maintenance itself is the primary bottleneck rather than the distractor.

---

## 8. Medication-State Relevance and Analysis Isolation
*   **Rationale for using `off-ADHD` (Unmedicated) sessions**:
    1.  Methylphenidate (Ritalin) normalizes attention, motor speed, and eye-tracking/pupil markers in children with ADHD.
    2.  Using medicated sessions in the primary classification task would confound the diagnostic signals and mask the underlying ADHD-associated cognitive patterns.
    3.  This isolation is scientifically mandatory for participant-independent diagnostic ML experiments.
*   **Secondary Analysis of `on-ADHD` sessions (Medicated repeated measurements)**:
    *   The 17 medicated repeated sessions can be used for a within-subject medication-effect analysis to see if methylphenidate restores eye-tracking or behavioral metrics toward control levels (e.g., paired t-test between off-ADHD and on-ADHD states).
    *   *Thesis / Conference Material*: It could become thesis material or a secondary conference-paper analysis because it directly evaluates the physiological efficacy of treatment on cognitive biomarkers.

---

## 9. Dataset Limitations and Claims Verification

*   **Original Sample Size**: Small ($N=50$ participants), which restricts model generalizability.
*   **Final Analyzable Cohort ($N=40$)**: The loss of 10 controls due to missing data structures reduces the control class, decreasing overall statistical power.
*   **Class Imbalance (28 ADHD vs. 12 Control)**: Standard accuracy is biased; we must evaluate classifiers using F1 score, ROC-AUC, and balanced accuracy.
*   **Age/Population Specificity**: Evaluates only children and adolescents (7–17 years old); results cannot be generalized to adult ADHD.
*   **Laboratory Hardware**: EyeLink 1000 is a high-fidelity, tower-mounted laboratory eye tracker; findings cannot be assumed to translate directly to low-cost webcam trackers.
*   **Lack of External Validation**: The models are trained and tested on the same dataset (via nested CV), presenting a risk of dataset-specific overfitting.
*   **Pupil Normalization**: Pupil data is provided as pre-calculated session-level z-scores, which prevents analyzing absolute resting pupil sizes.

---

## 10. Laboratory Dataset vs. Our Live Webcam HCI System

The offline scientific dataset and the live webcam prototype are distinct systems. Successful classification on the laboratory dataset does **not** validate the webcam system.

| Aspect | Rojas-Líbano Dataset | Our Webcam System | Comparable? | Implication |
| --- | --- | --- | --- | --- |
| **Participants** | Clinical cohort (ADHD/Control). | General users / prototype testers. | **NO** | Webcam predictions are exploratory; cannot claim clinical diagnostic power. |
| **Eye Tracker** | EyeLink 1000 tower-mount. | Built-in webcam. | **NO** | Webcam has substantially higher measurement noise and lower resolution. |
| **Gaze Tracking** | Infrared corneal reflection (1000 Hz). | MediaPipe iris landmarks (30 Hz). | **NO** | Webcam cannot resolve high-frequency micro-saccades or spatial fixation stability. |
| **Pupil Tracking** | Absolute pupil contour (1000 Hz). | Iris/pupil pixel area (30 Hz). | **NO** | Webcam pupil area is highly sensitive to ambient light and head distance. |
| **Task** | Visuospatial working-memory task. | Webcam Sternberg task prototype. | **YES** | Task structure is similar, but environment is uncontrolled. |
| **Calibration** | 9-point calibration. | Quick webcam calibration. | **NO** | Webcam calibration is less precise and drifts quickly. |
| **Environment** | Controlled chin-rest laboratory. | Uncontrolled home/office environment. | **NO** | Head movements, lighting shifts, and distractors are uncontrolled in the webcam system. |
| **Feature Extraction** | Offline parser (`parse_mat.py`). | Real-time logger (`feature_extractor.py`).| **YES** | Extract identical feature categories, but source inputs differ in quality. |

---

## 11. Alternative Dataset and Suitability Analysis
*   **Verdict**: **YES, WITH IMPORTANT LIMITATIONS**.
*   **Rationale**: The Rojas-Líbano dataset is a highly reasonable choice because no other public repository combines synchronized 1000 Hz pupillometry, high-fidelity gaze coordinates, clinical ADHD wash-out states, and trial-level working-memory metrics.
*   **Ideal Dataset Components**:
    1.  Simultaneous dual-recording: EyeLink 1000 and standard web camera recorded on the same participants.
    2.  Larger, balanced sample size ($N > 200$) with age-matched controls.
    3.  Multi-day, longitudinal recordings to test stability.
    4.  Detailed clinical subtype documentation (ADHD-I, ADHD-H, ADHD-C).

---

## 12. Publication-Ready Dataset Justification

"To evaluate the predictive utility of eye-tracking and pupillometric features in characterizing attention-deficit/hyperactivity disorder (ADHD), we utilized the public clinical dataset published by Rojas-Líbano et al. (2019) (DOI: 10.1038/s41597-019-0037-2). The dataset provides synchronized, high-resolution (1000 Hz) gaze coordinates and pupil diameter measurements collected via an EyeLink 1000 tower-mount system, alongside trial-level behavioral accuracy and reaction times. These measurements were recorded during a delayed visuospatial working-memory task (a modified visuospatial Sternberg paradigm) containing working memory load (1 vs. 2 dots) and distractor valence manipulations (neutral, emotional, task-related, or none). To ensure a clean clinical signal and prevent subject-leakage, our primary analysis isolated unmedicated ADHD sessions ($N = 28$ unique participants, following a stimulant medication wash-out period of $\geq 24$ hours) and healthy control sessions ($N = 12$ unique participants, excluding 10 sessions due to missing trial structure data), resulting in a final analyzable cohort of $N = 40$. Major limitations of this dataset include the relatively small sample size, clinical class imbalance, and laboratory-specific tracking hardware, which prevents direct generalizability to low-cost webcam tracking applications."

---

## Final Verdict

1.  **Exact task name we should use in the paper**: A delayed visuospatial working-memory task using a Sternberg-type paradigm (or a modified visuospatial Sternberg task).
2.  **Is "Sternberg task" technically correct?**: Correct only to call it a modified/visuospatial Sternberg-type task.
3.  **Why this dataset is being used**: It is the only public dataset combining synchronized 1000 Hz gaze tracking, pupillometry, trial-level reaction times, and clinical ADHD unmedicated/control classes during a spatial memory task.
4.  **What research question it can answer**: Whether spatial gaze stability, search dispersion, and pupil dynamics provide complementary classification power beyond behavioral accuracy and reaction-time variability in laboratory settings.
5.  **What it cannot answer**: Whether webcam-based eye-tracking is capable of diagnostic ADHD classification in uncontrolled home environments.
6.  **Why Pupil_dataset.mat is important**: It serves as the high-fidelity clinical baseline to validate the theoretical relationship between ADHD-associated cognitive patterns and eye-tracking biomarkers.
7.  **Whether N=40 primary analysis is defensible**: Yes, provided that participant-level nested cross-validation is strictly enforced to prevent data leakage and optimism bias.
8.  **Whether the dataset supports behavioral + RT + gaze + pupil multimodal analysis**: Yes, all four modalities are synchronized on a trial-by-trial basis.
9.  **Whether the dataset supports webcam validation**: No, it uses high-end EyeLink laboratory equipment which does not validate webcam implementation.
10. **Final dataset suitability rating**: **SUITABLE WITH LIMITATIONS**.

---
*Report compiled and verified on 2026-07-18.*
