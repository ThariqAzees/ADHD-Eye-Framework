import os
import json
import streamlit as st
import pandas as pd
from tracking.mediapipe_tracker import gaze_tracker
from sternberg.feature_extractor import extract_features_from_logs, save_sternberg_session
from ml.inference import predict_adhd_risk

st.title("🧠 Sternberg Working Memory Task")
st.subheader("Cognitive Task Replication & Feature Extraction Page")

# Load configuration for calibration
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "config.json")
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
else:
    config = {"calibration": {"excellent": 25.0, "good": 50.0, "fair": 75.0}}
    
cal_thresholds = config["calibration"]

# Disclaimer
st.markdown("""
<div style="background-color: rgba(22, 27, 34, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); padding: 16px; border-radius: 8px; margin-bottom: 24px;">
    <strong>ℹ️ RESEARCH MODULE OVERVIEW</strong><br>
    This page replicates the Sternberg delayed visuospatial working-memory task used in the Rojas-Líbano clinical study. 
    It captures your response accuracy, reaction times, fixation stability, and pupil diameter changes. 
    Upon completion, your aggregate task features will be fed into our machine learning model to estimate pattern similarity 
    to observed clinical cohorts.
</div>
""", unsafe_allow_html=True)

# Participant ID check
from experiment.Experiment_Manager import transition_experiment_state, ExperimentLogger, update_session_telemetry, STATE_ORDER
current_state = st.session_state.get("experiment_state", "NOT_STARTED")
required_state = "SESSION_CREATED"

if "session_id" not in st.session_state or not st.session_state["session_id"] or STATE_ORDER.index(current_state) < STATE_ORDER.index(required_state):
    st.warning("⚠️ **No active experiment session.**\n\nPlease start or resume an experiment using the Experiment Manager before collecting data.")
    if st.button("Open Experiment Manager", use_container_width=True):
        st.switch_page("pages/Experiment_Manager.py")
    st.stop()

# Retrieve values from session state
subject_id = st.session_state["participant_id"]
session_id = st.session_state["session_id"]
st.write(f"**Current Participant:** `{subject_id}` | **Session:** `{session_id}`")

# Transition and log Calibration Started
logger = ExperimentLogger(session_id)
if current_state == "SESSION_CREATED":
    logger.log_tracking_event("Calibration Started")
    transition_experiment_state("CALIBRATION_STARTED")

# Check if model has been trained
models_path = os.path.join(base_dir, "ml", "models_v1.0.pkl")
models_exist = os.path.exists(models_path)

if not models_exist:
    st.warning("⚠️ Machine Learning models are not trained yet. Gaze tracking features will be extracted, but model predictions will not be available. Please train models on the Home page first.")

# Component invocation
component_val = gaze_tracker(
    task_type="sternberg_task",
    calibration_thresholds=cal_thresholds,
    key="sternberg_tracker"
)

# Handle results from component
if component_val is not None:
    st.success("Sternberg Working Memory Task completed successfully!")
    
    # Retrieve logs
    raw_log = component_val.get('raw_log', [])
    responses = component_val.get('responses', [])
    cal_diagnostics = component_val.get('calibration_diagnostics', {})
    
    # Log events & transition state
    logger = ExperimentLogger(session_id)
    phase_ts = component_val.get('phase_timestamps', {})
    
    # 1. Log Calibration Started (in case it wasn't logged or to keep DB records exact)
    logger.log_tracking_event("Calibration Started", timestamp=phase_ts.get("calibration_started"))
    
    # 2. Log Calibration Completed
    logger.log_tracking_event("Calibration Completed", {
        "quality": cal_diagnostics.get('quality', "Poor"),
        "mean_error": cal_diagnostics.get('mean_error', 999),
        "rms_error": cal_diagnostics.get('rms_error', 999),
        "head_motion_score": cal_diagnostics.get('head_motion_score', 1.0)
    }, timestamp=phase_ts.get("calibration_completed"))
    
    # 3. Log Sternberg Started
    logger.log_task_event("Sternberg Started", timestamp=phase_ts.get("sternberg_started"))
    
    # 4. Log Sternberg Completed
    logger.log_task_event("Sternberg Completed", timestamp=phase_ts.get("sternberg_completed"))
    
    # Sequentially update session states
    transition_experiment_state("CALIBRATION_STARTED")
    transition_experiment_state("CALIBRATION_COMPLETED")
    transition_experiment_state("STERNBERG_STARTED")
    transition_experiment_state("STERNBERG_COMPLETED")
    
    # Update session telemetry/device metadata from JS if available
    device_metadata = component_val.get('device_metadata')
    if device_metadata:
        update_session_telemetry(
            session_id=session_id,
            browser=device_metadata.get('browser'),
            operating_system=device_metadata.get('operating_system'),
            screen_resolution=device_metadata.get('screen_resolution'),
            webcam_information=device_metadata.get('webcam_information')
        )
    
    # Export calibration report (JSON and CSV)
    from tracking.calibration import export_calibration_report
    cal_json_path, cal_csv_path = export_calibration_report(cal_diagnostics, subject_id)
    
    cal_metrics = {
        "mean_error": cal_diagnostics.get('mean_error', 999),
        "median_error": cal_diagnostics.get('median_error', 999),
        "max_error": cal_diagnostics.get('max_error', 999),
        "p95_error": cal_diagnostics.get('p95_error', 999),
        "rms_error": cal_diagnostics.get('rms_error', 999),
        "gaze_jitter": cal_diagnostics.get('gaze_jitter', 999.0),
        "sample_loss_rate": cal_diagnostics.get('sample_loss_rate', 999.0),
        "head_motion_score": cal_diagnostics.get('head_motion_score', 999.0),
        "calibration_status": "completed",
        "quality_rating": cal_diagnostics.get('quality', "Poor")
    }
    
    with st.spinner("Extracting engineered features from raw gaze and pupil logs..."):
        # Run feature extractor
        trial_features_list, agg_features = extract_features_from_logs(
            raw_log=raw_log,
            responses=responses,
            subject_id=subject_id
        )
        
    st.success("Engineered features extracted successfully!")
    
    # Save the session to raw, processed, exports
    csv_raw_path, csv_feats_path, meta_path = save_sternberg_session(
        raw_log=raw_log,
        responses=responses,
        agg_features=agg_features,
        calibration_metrics=cal_metrics,
        metadata_args=st.session_state.get('device_info', {})
    )
    
    st.info(f"Raw CSV log saved: `{csv_raw_path}`")
    st.info(f"Engineered features CSV saved: `{csv_feats_path}`")
    st.info(f"Session metadata JSON saved: `{meta_path}`")
    if cal_json_path:
        st.info(f"Calibration JSON report saved: `{cal_json_path}`")
    if cal_csv_path:
        st.info(f"Calibration verification CSV saved: `{cal_csv_path}`")
    
    # Perform Model Inference if models are trained
    predictions = {}
    if models_exist:
        with st.spinner("Running model prediction..."):
            try:
                for model_name in ['logistic_regression', 'random_forest', 'xgboost']:
                    prob = predict_adhd_risk(agg_features, model_name=model_name)
                    predictions[model_name] = prob
                st.success("Model prediction complete.")
            except Exception as e:
                st.error(f"Prediction error: {e}")
                
    # Save session data to session state for Results page viewing
    st.session_state['sternberg_results'] = {
        "raw_log": raw_log,
        "responses": responses,
        "trial_features": [t.__dict__ for t in trial_features_list],
        "agg_features": agg_features,
        "calibration_metrics": cal_metrics,
        "predictions": predictions
    }
    
    st.balloons()
    
    st.markdown("### 📊 Next Steps")
    if st.button("View Detailed Results Dashboard", use_container_width=True):
        st.switch_page("pages/Results.py")
else:
    st.info("Waiting for session to start and complete. Click 'Start Calibration' above to begin.")
