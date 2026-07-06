import os
import json
import streamlit as st
import pandas as pd
import numpy as np
from visualizations import (
    plot_gaze_vs_target_trajectory,
    plot_gaze_error_timeline,
    plot_gaze_density_heatmap
)
from tracking.mediapipe_tracker import gaze_tracker
from tracking.smooth_pursuit import save_smooth_pursuit_session

st.title("👁️ Smooth Pursuit Tracking Demonstration")
st.subheader("Eye-Tracking Engineering Validation Page")

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
<div style="background-color: rgba(0, 229, 255, 0.05); border-left: 4px solid #00E5FF; padding: 16px; border-radius: 4px; margin-bottom: 24px;">
    <strong>ℹ️ ENGINEERING DEMONSTRATION</strong><br>
    This page serves as a technical validation of webcam-based gaze tracking calibration and smooth pursuit follow performance. 
    It records tracking errors and calibration indices for hardware verification. 
    <strong>No clinical classification, ADHD-risk estimation, or machine learning models are loaded or used on this page.</strong>
</div>
""", unsafe_allow_html=True)

# Participant ID check
subject_id = st.session_state.get('subject_id', 'participant_01')
st.write(f"**Current Participant:** `{subject_id}`")

# Render custom eye tracker component
st.markdown("### Gaze Calibration & Tracking Environment")
st.write("Ensure your camera is active. Complete calibration, verify that the validation cursor is accurate, then start the smooth pursuit trajectories.")

# Component invocation
# We pass the thresholds from config.json and set task_type = 'smooth_pursuit'
component_val = gaze_tracker(
    task_type="smooth_pursuit",
    calibration_thresholds=cal_thresholds,
    key="smooth_pursuit_tracker"
)

# Handle results from component
if component_val is not None:
    st.success("Session completed and raw eye-tracking logs retrieved successfully!")
    
    # Save the session
    raw_log = component_val.get('raw_log', [])
    cal_diagnostics = component_val.get('calibration_diagnostics', {})
    
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
    
    # Save to disk
    csv_path, meta_path = save_smooth_pursuit_session(
        raw_log=raw_log,
        subject_id=subject_id,
        calibration_metrics=cal_metrics,
        metadata_args=st.session_state.get('device_info', {})
    )
    
    st.info(f"Raw CSV log written to: `{csv_path}`")
    st.info(f"Session metadata written to: `{meta_path}`")
    if cal_json_path:
        st.info(f"Calibration JSON report written to: `{cal_json_path}`")
    if cal_csv_path:
        st.info(f"Calibration verification CSV written to: `{cal_csv_path}`")
    
    # Convert log to dataframe for visualizations
    df = pd.DataFrame(raw_log)
    
    # ----------------------------------------------------
    # VISUALIZATIONS SECTION
    # ----------------------------------------------------
    st.markdown("## 📊 Engineering Gaze Performance Analytics")
    
    # Compute errors (Euclidean distance between gaze_x, gaze_y and target_x, target_y)
    df['error_px'] = np.sqrt((df['gaze_x'] - df['target_x'])**2 + (df['gaze_y'] - df['target_y'])**2)
    # Filter out NaNs (e.g. blink states or face detection lost)
    df_valid = df.dropna(subset=['error_px', 'gaze_x', 'gaze_y'])
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.markdown("#### 👁️ Gaze Trajectory vs Target Path Overlay")
        fig_traj = plot_gaze_vs_target_trajectory(df_valid)
        st.plotly_chart(fig_traj, use_container_width=True)
        
    with col_v2:
        st.markdown("#### 📈 Gaze Tracking Error Timeline")
        fig_err = plot_gaze_error_timeline(df_valid)
        st.plotly_chart(fig_err, use_container_width=True)
        
    col_v3, col_v4 = st.columns(2)
    
    with col_v3:
        st.markdown("#### 🗺️ Gaze Density Heatmap")
        fig_hm = plot_gaze_density_heatmap(df_valid, title="Gaze Position Density Map")
        st.plotly_chart(fig_hm, use_container_width=True)
        
    with col_v4:
        st.markdown("#### 📊 Summary Statistics")
        mean_err = df_valid['error_px'].mean()
        median_err = df_valid['error_px'].median()
        max_err = df_valid['error_px'].max()
        std_err = df_valid['error_px'].std()
        
        st.markdown(f"""
        - **Mean Smooth Pursuit Error:** `{mean_err:.1f} pixels`
        - **Median Smooth Pursuit Error:** `{median_err:.1f} pixels`
        - **Max Smooth Pursuit Error:** `{max_err:.1f} pixels`
        - **Smooth Pursuit Jitter (SD):** `{std_err:.1f} pixels`
        - **Total Frames Logged:** `{len(df)}`
        - **Valid Gaze Frames:** `{len(df_valid)}` ({(len(df_valid)/len(df))*100:.1f}%)
        """)
        
        # Calibration quality display
        cal_quality = cal_metrics["quality_rating"]
        mean_cal = cal_metrics["mean_error"]
        rms_cal = cal_metrics["rms_error"]
        loss_cal = cal_metrics["sample_loss_rate"]
        
        st.markdown("#### 🛠️ Calibration Diagnostics")
        st.markdown(f"""
        - **Quality Rating:** **{cal_quality}**
        - **Mean Verification Error:** `{mean_cal} px`
        - **RMS Gaze Error:** `{rms_cal} px`
        - **Calibration Loss Rate:** `{loss_cal * 100:.1f}%`
        - **Jitter:** `{cal_metrics['gaze_jitter']} px`
        - **Head Motion Score:** `{cal_metrics['head_motion_score']:.5f}`
        """)
else:
    st.info("Waiting for tracking session to start and complete. Click 'Start Calibration' to begin.")
