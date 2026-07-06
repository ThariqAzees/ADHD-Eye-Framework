# ADHD Eye Framework

**A Webcam-Based Eye Movement Analysis Framework Integrating Smooth Pursuit Tracking and Cognitive Task-Based Feature Extraction for Exploratory ADHD Screening Research**

---

> [!WARNING]
> **CRITICAL RESEARCH DISCLAIMER & INTENDED USE**  
> This software is an exploratory research engineering platform and **not** a clinical diagnostic instrument. It does not diagnose, treat, or detect ADHD or any other clinical condition. The machine learning model outputs similarity scores comparing task performance patterns to a specific historical clinical dataset. Every screening/similarity result is purely exploratory and should not be used as a substitute for professional clinical evaluation. A qualified healthcare specialist must be consulted for any diagnostic concerns.

---

## Technical Overview & Intent

This framework integrates webcam-based gaze tracking and cognitive tasks for exploratory screening research. It is architected into two separate modules:
1. **Module 1: Smooth Pursuit (Engineering Demo):** Uses face mesh and iris landmark tracking to display target tracking error over horizontal, vertical, circular, figure-8, and zig-zag trajectories. Gaze logs from this module are stored locally and are *never* used to train or predict with the machine learning models.
2. **Module 2: Sternberg Working Memory Task (Research Module):** Replicates the cognitive working-memory task used in the Rojas-Líbano et al. (2019) clinical study. Extracted gaze stability, reaction times, omission rates, and pupil proxy features from this module are fed into the machine learning models trained on neurologist-certified clinical data.

---

## Fundamental Limitations

Any researcher or user evaluating this platform must be aware of the following design limitations:
- **Hardware Mismatch:** The model is trained on a 1 kHz EyeLink 1000 eye-tracker with active chin-rest chin-stabilization, whereas webcam data is captured at 30 Hz with unconstrained head movement. Gaze dynamics (saccades, tremors) are smoothed.
- **Population Mismatch:** The model is trained on a Chilean pediatric clinical cohort (10–12 years old). Performance patterns may not generalize to adults or other demographics.
- **Pupil Unit Mismatch:** Pupil size in the baseline dataset is represented in arbitrary IR-based camera units, whereas webcam pupil tracking uses an iris landmark radius pixel proxy.
- **Exclusion of Smooth Pursuit:** Smooth pursuit metrics are excluded from classification due to the absence of public smooth pursuit datasets with clinical ADHD labels.

---

## Setup & Running Instructions

### 1. Prerequisites
Ensure you have Python 3.9+ installed. The following packages are required and can be installed via pip:
```bash
pip install streamlit pandas numpy scipy scikit-learn xgboost plotly pymatreader
```

### 2. File Organization
Verify your directory structure matches:
```
ADHD_Eye_Framework/
├── app.py                  # Main entry point (redirects to Home)
├── config.json             # Calibration quality threshold settings
├── README.md               # Setup & disclaimer overview
├── pages/
│   ├── Home.py             # Configuration & Model Training controller
│   ├── Smooth_Pursuit.py   # Engineering gaze tracker validator
│   ├── Sternberg_Task.py   # Client-side cognitive task sequencer
│   └── Results.py          # Dual-module dashboard & CSV/JSON exporter
├── tracking/
│   ├── calibration.py      # Calibration docs
│   ├── gaze_mapping.py     # Gaze mapping equations docs
│   ├── mediapipe_tracker.py# Streamlit custom component wrapper
│   ├── smooth_pursuit.py   # Smooth pursuit backend logger
│   └── frontend/
│       └── index.html      # Client-side MediaPipe & Task sequencer
├── sternberg/
│   ├── task_engine.py      # Sternberg state-machine docs
│   ├── stimulus.py         # Stimulus drawing details
│   ├── response_logger.py  # Response parsing helper
│   └── feature_extractor.py# Main frame log compiler
├── ml/
│   ├── train_model.py      # Nested 5-fold CV training pipeline
│   ├── inference.py        # Risks similarity predictor
│   ├── features.py         # Schema details
│   └── model.pkl           # Saved model package
├── visualizations/
│   ├── trajectory.py       # Gaze overlay plots
│   ├── heatmap.py          # 2D density maps
│   ├── timeline.py         # Error & pupil timelines
│   └── dashboard.py        # Cognitive accuracy bars
├── reports/
│   └── final_report.md     # Technical and validation report
└── data/
    ├── raw/                # Contains Pupil_dataset.mat
    ├── processed/          # Contains dataset_features_v1.0.csv
    └── exports/            # Local session CSV and JSON exports
```

### 3. Training the ML Pipeline
Prior to running task sessions, train the models on the Rojas-Líbano dataset:
1. Open the app and navigate to **Home**.
2. Click **Extract Features & Run Validation** (uses `data/raw/Pupil_dataset.mat`).
3. Click **Train Machine Learning Pipeline (Nested CV)**. This trains Logistic Regression, Random Forest, and XGBoost models, reporting outer fold metrics, and saves the package to `ml/model.pkl` and `ml/models_v1.0.pkl`.

### 4. Running the Web Application
Start the Streamlit server:
```bash
python -m streamlit run app.py
```
Open the provided URL (default `http://localhost:8501`) in your browser (Chrome recommended for optimal webcam MediaPipe tracking).
