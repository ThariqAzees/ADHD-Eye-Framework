# ADHD Eye Framework

**A Webcam-Based Interactive System for Multi-Modal Gaze and Cognitive Task Assessment: Design, Implementation, and Evaluation**

An HCI systems project exploring how consumer-grade webcam eye-tracking can be integrated into an interactive research tool for cognitive-behavioral screening tasks — emphasizing interaction design, usability, and system robustness over model accuracy.

> **Research Framing Note**
> This project is presented as a **human-computer interaction system paper**, not a machine learning paper. The ML classification module is one *evaluated component* of a larger interactive system; the primary contributions are the system's **design**, its **interaction model**, and a **multi-track empirical evaluation** (usability, performance, robustness, and applied case study).

---

## Research Disclaimer & Intended Use

This software is an exploratory research and engineering platform, not a clinical diagnostic instrument. It does not diagnose, treat, or detect ADHD or any other clinical condition. Any similarity scores produced by the system's ML component are exploratory outputs for research purposes only and must never substitute for professional clinical evaluation.

---

## 1. Overview

The ADHD Eye Framework is an interactive, browser-based research instrument that combines real-time webcam gaze tracking with structured cognitive tasks. It is designed around two core HCI questions:

1. **Can a low-cost, consumer-hardware interaction pipeline (webcam + browser) support reliable, repeatable cognitive task administration for research use?**
2. **What interaction design and system architecture choices are needed to make such a pipeline usable, robust, and trustworthy for both researchers (session control, calibration, logging) and participants (task clarity, feedback, comfort)?**

The system is built as a multi-page Streamlit application with a custom JavaScript/MediaPipe front-end component for gaze tracking, backed by a session logging and feature-extraction pipeline.

---

## 2. System Architecture

The framework is deliberately partitioned into two independent interaction modules, a design decision central to the system's validity:

- **Module 1 — Smooth Pursuit (Engineering Validation Interface):** A real-time gaze-tracking demo across horizontal, vertical, circular, figure-8, and zig-zag trajectories. Used to validate tracking quality and calibration fidelity. Logs from this module are stored locally and are **never** passed into the downstream classification pipeline.
- **Module 2 — Sternberg Working Memory Task (Cognitive Assessment Interface):** A browser-driven replication of the working-memory paradigm from Rojas-Líbano et al. (2019). Gaze stability, reaction time, omission rate, and pupil-proxy features extracted here feed the ML case-study component.

```
User ──> Calibration UI ──> Task Selection ──> [Smooth Pursuit | Sternberg Task]
                                                        │
                                             Real-time Logging Layer
                                                        │
                                          Feature Extraction / Session Store
                                                        │
                                         Results Dashboard ──> Researcher Export
```

Supporting subsystems:
- `tracking/` — calibration, gaze mapping, MediaPipe integration, client-side tracker
- `sternberg/` — task state machine, stimulus rendering, response logging, feature extraction
- `ml/` — case-study classification pipeline (Random Forest, Gradient Boosting, SVM, XGBoost)
- `visualizations/` — trajectory overlays, heatmaps, timelines, dashboards
- **`experiment/`** *(in progress)* — Experiment Manager panel for session configuration, participant tracking, and structured logging instrumentation supporting the usability study

---

## 3. Evaluation Methodology

The system is evaluated along **four tracks**, reflecting standard HCI systems-paper practice of triangulating quantitative system performance with user-centered evidence:

| Track | Focus | Method |
|---|---|---|
| **1. Usability Study** | Task clarity, calibration experience, perceived workload, trust in the interface | Moderated study, N = 15–20 participants, standard usability instruments (e.g. SUS) + task completion metrics |
| **2. System Performance Benchmarking** | Frame rate, calibration accuracy, tracking latency, logging integrity | Automated benchmarks across hardware/browser configurations |
| **3. Robustness Testing** | Behavior under degraded conditions (poor lighting, head movement, webcam variance) | Controlled stress-test scenarios with logged failure modes |
| **4. ADHD ML Case Study** | Illustrative application of the Sternberg-derived features on a classification task | Applied study on the Rojas-Líbano dataset, reported as a bounded case study, not a generalizable diagnostic claim |

This structure allows the ML component to be honestly scoped as *one applied case study within a larger system evaluation*, rather than the paper's central claim.

---

## 4. Design Constraints & Threats to Validity

Transparency about system limitations is treated as part of the contribution, not an afterthought:

- **Hardware mismatch:** Reference clinical data was collected on a 1 kHz EyeLink 1000 with chin-rest stabilization; this system uses unconstrained 30 Hz webcam tracking. Fine-grained saccadic dynamics are necessarily smoothed.
- **Population mismatch:** The reference dataset reflects a Chilean pediatric clinical cohort (ages 10–12); findings from the case study should not be generalized to adult or other populations.
- **Measurement unit mismatch:** Reference pupil data uses IR camera units; this system uses an iris-landmark radius pixel proxy.
- **Scope exclusion:** Smooth Pursuit metrics are intentionally excluded from the classification pipeline due to the absence of public smooth-pursuit datasets with clinical ADHD labels — this is a system design decision, not an oversight.

---

## 5. Setup & Running Instructions

### Prerequisites
Python 3.9+ and the following packages:
```bash
pip install streamlit pandas numpy scipy scikit-learn xgboost plotly pymatreader
```

### Directory Structure
```
ADHD_Eye_Framework/
├── app.py
├── config.json
├── README.md
├── pages/
│   ├── Home.py
│   ├── Smooth_Pursuit.py
│   ├── Sternberg_Task.py
│   └── Results.py
├── tracking/
├── sternberg/
├── ml/
├── visualizations/
├── reports/
│   └── final_report.md
└── data/
    ├── raw/
    ├── processed/
    └── exports/
```

### Running the ML Case Study Pipeline
1. Launch the app and go to **Home**.
2. Click **Extract Features & Run Validation** (uses `data/raw/Pupil_dataset.mat`).
3. Click **Train Machine Learning Pipeline (Nested CV)** — trains and evaluates the case-study models.

### Running the Interactive System
```bash
python -m streamlit run app.py
```
Open the provided local URL (Chrome recommended for optimal MediaPipe performance).

---

## 6. Citing This Work

If referencing this system in academic work, please cite (placeholder — update on publication):

```bibtex
@misc{amanulla2026adhdeye,
  author = {Amanulla, Thariq Azees},
  title  = {ADHD Eye Framework: A Webcam-Based Interactive System for Multi-Modal Gaze and Cognitive Task Assessment},
  year   = {2026},
  note   = {Manuscript in preparation}
}
```

---

## License

Copyright © 2026 Thariq Azees Amanulla. All rights reserved.

This repository is made available for **viewing purposes only** as part of
an ongoing academic research submission. No permission is granted to copy,
modify, distribute, or use this code or its associated documentation, in
whole or in part, for any purpose without the express written consent of
the author.

