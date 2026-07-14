import os
import json
import streamlit as st
import pandas as pd
import numpy as np
from visualizations import (
    plot_gaze_density_heatmap,
    plot_dispersion_vs_stability,
    plot_accuracy_by_load,
    plot_accuracy_by_distractor,
    plot_reaction_time_timeline,
    plot_pupil_proxy_trace
)

st.title("📊 Analysis Results Dashboard")
st.subheader("Single Cognitive-Task Validation & Evaluation Dashboard")

# Read session configuration thresholds
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "config.json")
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
else:
    config = {"calibration": {"excellent": 25.0, "good": 50.0, "fair": 75.0}}

cal_thresholds = config["calibration"]

# Check if results are present in session state
# Gating check
from experiment.Experiment_Manager import transition_experiment_state, ExperimentLogger, close_active_session
from experiment.session import STATE_ORDER
current_state = st.session_state.get("experiment_state", "NOT_STARTED")
required_state = "STERNBERG_COMPLETED"

if "session_id" not in st.session_state or not st.session_state["session_id"] or STATE_ORDER.index(current_state) < STATE_ORDER.index(required_state):
    st.warning("⚠️ **No active experiment session.**\n\nPlease start or resume an experiment using the Experiment Manager before collecting data.")
    if st.button("Open Experiment Manager", use_container_width=True):
        st.switch_page("pages/Experiment_Manager.py")
    st.stop()

# Retrieve values from session state
subject_id = st.session_state["participant_id"]
session_id = st.session_state["session_id"]
st.write(f"**Current Participant:** `{subject_id}` | **Session:** `{session_id}`")

# Log Results Viewed event
logger = ExperimentLogger(session_id)
if f"results_viewed_logged_{session_id}" not in st.session_state:
    logger.log_user_event("Results Viewed")
    st.session_state[f"results_viewed_logged_{session_id}"] = True
    transition_experiment_state("RESULTS_REVIEWED")

if 'sternberg_results' not in st.session_state:
    st.warning("⚠️ No completed Sternberg Working Memory Task session found. Please complete the task module first before viewing this dashboard.")
    if st.button("Go to Sternberg Task"):
        st.switch_page("pages/Sternberg_Task.py")
    st.stop()

# Retrieve results
results = st.session_state['sternberg_results']
raw_log = results['raw_log']
responses = results['responses']
trial_features = results['trial_features']
agg_features = results['agg_features']
cal_metrics = results['calibration_metrics']
predictions = results['predictions']

df_raw = pd.DataFrame(raw_log)
df_resp = pd.DataFrame(responses)
df_trial = pd.DataFrame(trial_features)

# ==============================================================================
# SECTION 1: ENGINEERING EVALUATION
# ==============================================================================
st.markdown("## 🛠️ 1. Engineering Evaluation")
st.caption("Hardware, Calibration Quality, Gaze Stability, and Tracker Accuracy Analytics")

col_e1, col_e2 = st.columns([1, 2])

with col_e1:
    st.markdown("#### 📐 Calibration Quality & Accuracy")
    with st.container(border=True):
        mean_err = cal_metrics.get("mean_error")
        med_err = cal_metrics.get("median_error")
        max_err = cal_metrics.get("max_error")
        p95_err = cal_metrics.get("p95_error")
        rms_err = cal_metrics.get("rms_error")
        jitter = cal_metrics.get("gaze_jitter")
        loss_rate = cal_metrics.get("sample_loss_rate")
        head_motion = cal_metrics.get("head_motion_score")
        quality = cal_metrics.get("quality_rating", "Poor")

        # Formatting helpers
        def fmt_px(val):
            return f"{val} px" if val is not None and val != 999 else "N/A"

        def fmt_pct(val):
            return f"{val * 100:.1f}%" if val is not None and val != 999.0 else "N/A"

        def fmt_val(val, decimals=5):
            return f"{val:.{decimals}f}" if val is not None and val != 999.0 else "N/A"

        # Classify quality coloring
        quality_color = "#FF3366"
        if quality == "Excellent":
            quality_color = "#39FF14"
        elif quality == "Good":
            quality_color = "#58A6FF"
        elif quality == "Fair":
            quality_color = "#D29922"

        st.markdown(f"**Calibration Quality Rating:** <span style='font-size: 20px; font-weight: bold; color: {quality_color};'>{quality}</span>", unsafe_allow_html=True)
        st.markdown(f"""
        - **Mean Gaze Error:** `{fmt_px(mean_err)}`
        - **Median Gaze Error:** `{fmt_px(med_err)}`
        - **Max Gaze Error:** `{fmt_px(max_err)}`
        - **95th Percentile:** `{fmt_px(p95_err)}`
        - **RMS Error:** `{fmt_px(rms_err)}`
        - **Gaze Jitter:** `{fmt_px(jitter)}`
        - **Sample Loss Rate:** `{fmt_pct(loss_rate)}`
        - **Head Motion Score:** `{fmt_val(head_motion)}`
        """)

        # Summary Gaze Stats
        total_frames = len(df_raw)
        blink_frames = len(df_raw[df_raw['blink_state'] == 1])
        valid_frames_pct = ((total_frames - blink_frames) / total_frames) * 100 if total_frames > 0 else 0

        st.markdown("**Gaze Acquisition Summary**")
        st.write(f"- Total Frames: `{total_frames}`")
        st.write(f"- Blink Frames: `{blink_frames}`")
        st.write(f"- Signal Quality: `{valid_frames_pct:.1f}%` valid frames")

with col_e2:
    st.markdown("#### 🗺️ Gaze Density Heatmap (During Task)")
    # Gaze positions during the active task trials, excluding blink states
    df_valid_gaze = df_raw[(df_raw['blink_state'] == 0) & (~df_raw['gaze_x'].isna()) & (~df_raw['gaze_y'].isna())]

    if len(df_valid_gaze) > 0:
        fig_hm = plot_gaze_density_heatmap(df_valid_gaze, title="Gaze Position Density Layout during Cognitive Trials")
        st.plotly_chart(fig_hm, use_container_width=True)
    else:
        st.info("No valid gaze coordinates logged.")

# Fixation Stability plot
st.markdown("#### 📈 Gaze Fixation Stability & Dispersion by Trial")
if len(df_trial) > 0:
    fig_stab = plot_dispersion_vs_stability(df_trial)
    st.plotly_chart(fig_stab, use_container_width=True)

st.markdown("---")

# ==============================================================================
# SECTION 2: RESEARCH EVALUATION
# ==============================================================================
st.markdown("## 🧠 2. Research Evaluation")
st.caption("Cognitive Performance, Pupillometry Metrics, and Research Model Risk Outputs")

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown("#### 🎯 Cognitive Accuracy Breakdown")

    fig_acc = plot_accuracy_by_load(df_resp)
    st.plotly_chart(fig_acc, use_container_width=True)

    fig_dist = plot_accuracy_by_distractor(df_resp)
    st.plotly_chart(fig_dist, use_container_width=True)

with col_r2:
    st.markdown("#### ⚡ Reaction Time & Pupil Proxy Timelines")

    fig_rt = plot_reaction_time_timeline(df_resp)
    st.plotly_chart(fig_rt, use_container_width=True)

    fig_pupil = plot_pupil_proxy_trace(df_trial)
    st.plotly_chart(fig_pupil, use_container_width=True)

# ----------------------------------------------------
# FEATURES SUMMARY TABLE
# ----------------------------------------------------
st.markdown("#### 📋 Session Feature Summary Table")

# Formatting helpers to handle None (N/A) and fix negative zero globally
def clean_negative_zero(formatted_str: str) -> str:
    if formatted_str.startswith('-'):
        stripped = formatted_str[1:]
        check_str = stripped.replace('%', '').replace('ms', '').replace('pixels', '').replace('pixel', '').strip()
        if all(c in ('0', '.') for c in check_str):
            return stripped
    return formatted_str

def safe_pct(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return clean_negative_zero(f"{val * 100:.1f}%")

def safe_ms(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return clean_negative_zero(f"{val:.1f} ms")

def safe_pixels(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return clean_negative_zero(f"{val:.2f} pixels")

def safe_val(val, fmt="{:.4f}"):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return clean_negative_zero(fmt.format(val))

feat_summary_data = {
    "Feature Name": [
        "Accuracy Overall",
        "Accuracy Load Difference (1-dot - 2-dot)",
        "Accuracy Distractor Difference (none - emotional)",
        "Mean Reaction Time",
        "Median Reaction Time",
        "Reaction Time SD (Variability)",
        "Reaction Time Coefficient of Variation (CV)",
        "Mean Fixation Instability (Scaled RMS)",
        "Mean Z-Scored Pupil Proxy",
        "Omission Rate",
        "False-Alarm Rate",
        "Hit Rate"
    ],
    "Value": [
        safe_pct(agg_features.accuracy_overall),
        safe_pct(agg_features.accuracy_by_load_diff),
        safe_pct(agg_features.accuracy_by_distractor_diff),
        safe_ms(agg_features.mean_reaction_time_ms),
        safe_ms(agg_features.median_reaction_time_ms),
        safe_ms(agg_features.rt_variability),
        safe_val(agg_features.rt_coefficient_of_variation, "{:.4f}"),
        safe_pixels(agg_features.mean_fixation_stability),
        safe_pixels(agg_features.mean_pupil_proxy),
        safe_pct(agg_features.omission_rate),
        safe_pct(agg_features.false_alarm_rate),
        safe_pct(agg_features.hit_rate)
    ]
}
st.table(pd.DataFrame(feat_summary_data))

# Software Metadata Box
st.markdown(f"""
<div style="background-color: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 6px; font-size: 11px; color: #8B949E; margin-bottom: 24px;">
    <strong>REPRODUCIBILITY METADATA:</strong><br>
    Framework Version: {agg_features.framework_version} |
    Feature Extractor Version: {agg_features.feature_extractor_version} |
    Model Package Version: {agg_features.model_version} |
    Dataset Baseline Version: {agg_features.dataset_version}
</div>
""", unsafe_allow_html=True)

# Confusion Matrix and Gaze Diagnostics Expander
with st.expander("🛠️ System Diagnostics & Confusion Matrix (Researcher View)"):
    st.markdown("### 📊 Cognitive Task Confusion Matrix")

    # Calculate confusion matrix values
    total_trials = len(df_resp)

    # Omissions check (user_response == -1 or rt <= 0 or rt >= 5000)
    omissions = len(df_resp[(df_resp['user_response'] == -1) | (df_resp['reaction_time_ms'] <= 0) | (df_resp['reaction_time_ms'] >= 5000)])

    # Valid trials (non-omissions)
    df_valid = df_resp[(df_resp['user_response'] != -1) & (df_resp['reaction_time_ms'] > 0) & (df_resp['reaction_time_ms'] < 5000)]

    target_trials = len(df_resp[df_resp['corr_response'] == 1])
    lure_trials = len(df_resp[df_resp['corr_response'] == 0])

    hits = len(df_valid[(df_valid['corr_response'] == 1) & (df_valid['user_response'] == 1)])
    misses = len(df_valid[(df_valid['corr_response'] == 1) & (df_valid['user_response'] == 0)])
    correct_rejections = len(df_valid[(df_valid['corr_response'] == 0) & (df_valid['user_response'] == 0)])
    false_alarms = len(df_valid[(df_valid['corr_response'] == 0) & (df_valid['user_response'] == 1)])

    st.markdown(f"""
    - **Total Trials:** `{total_trials}`
    - **Target Trials (Yes expected):** `{target_trials}`
    - **Lure Trials (No expected):** `{lure_trials}`
    - **Hits (True Positives):** `{hits}`
    - **Misses (False Negatives):** `{misses}`
    - **Correct Rejections (True Negatives):** `{correct_rejections}`
    - **False Alarms (False Positives):** `{false_alarms}`
    - **Omissions (No Response):** `{omissions}`
    """)

    st.markdown("### 👁️ Gaze & Pupil Diagnostics")

    device_meta = results.get('device_metadata', {})
    viewport = device_meta.get('viewport_size', 'N/A')
    dpr = device_meta.get('device_pixel_ratio', 'N/A')

    total_frames = len(df_raw)
    blink_frames = len(df_raw[df_raw['blink_state'] == 1])
    valid_frames_pct = ((total_frames - blink_frames) / total_frames) * 100 if total_frames > 0 else 0.0

    # Pupil radius ranges
    pupil_samples = df_raw['left_iris_radius'].dropna()
    valid_pupil_sample_count = len(pupil_samples)
    min_pupil = float(pupil_samples.min()) if valid_pupil_sample_count > 0 else 0.0
    max_pupil = float(pupil_samples.max()) if valid_pupil_sample_count > 0 else 0.0
    mean_pupil = float(pupil_samples.mean()) if valid_pupil_sample_count > 0 else 0.0

    # Fixation samples
    fix_frames = df_raw[df_raw['trial_phase'].str.startswith('fixation', na=False)]
    fixation_sample_count = len(fix_frames)

    # Validation errors
    verification_log = cal_metrics.get('verification_log', [])
    errors_str = "None"
    if verification_log:
        err_list = [v.get('error') for v in verification_log if v.get('error') is not None]
        if err_list:
            errors_str = ", ".join(f"{e}px" for e in err_list[:20])

    st.markdown(f"""
    - **Gaze Canvas Dimensions:** `{viewport}` (devicePixelRatio: `{dpr}`)
    - **Webcam Video Stream Size:** `640 x 480`
    - **Total Frame Logs Collected:** `{total_frames}`
    - **Valid Gaze Frames:** `{total_frames - blink_frames}`
    - **Invalid Gaze Frames (Blinks/Loss):** `{blink_frames}`
    - **Raw Gaze Signal Quality:** `{valid_frames_pct:.1f}%`
    - **First 20 Validation Errors:** `{errors_str}`
    - **Valid Pupil Radius Sample Count:** `{valid_pupil_sample_count}`
    - **Min / Max / Mean Pupil Radius:** `{min_pupil:.2f}px / {max_pupil:.2f}px / {mean_pupil:.2f}px`
    - **Fixation Sample Count:** `{fixation_sample_count}`
    """)

# ----------------------------------------------------
# RESEARCH MODEL OUTPUT CARD (WITH MANDATORY DISCLAIMER IN FRAME)
# ----------------------------------------------------
st.markdown("### 🤖 Research Machine Learning Classifier Prediction")
if len(predictions) > 0:
    selected_model = st.selectbox(
        "Select Machine Learning Model to evaluate:",
        options=["xgboost", "random_forest", "logistic_regression"],
        format_func=lambda x: x.replace("_", " ").title()
    )

    risk_score = predictions.get(selected_model, 0.0)

    # Styled unified output card containing BOTH score and disclaimer in the same visual frame
    st.markdown(f"""
    <div style="background-color: #161B22; border: 2px solid #00E5FF; border-radius: 12px; padding: 24px; box-shadow: 0 4px 20px rgba(0, 229, 255, 0.15); margin-bottom: 30px;">
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 16px; margin-bottom: 16px;">
            <div style="font-size: 18px; font-weight: bold; color: #FFFFFF;">Research Model Pattern Similarity Score</div>
            <div style="background-color: rgba(0, 229, 255, 0.1); border: 1px solid #00E5FF; border-radius: 6px; padding: 4px 12px; font-size: 12px; color: #00E5FF; font-weight: bold;">
                {selected_model.upper()}
            </div>
        </div>
        <div style="display: flex; align-items: baseline; margin-bottom: 20px;">
            <span style="font-size: 64px; font-weight: 900; color: #00E5FF; line-height: 1;">{risk_score*100:.1f}%</span>
            <span style="font-size: 16px; color: #8B949E; margin-left: 12px;">similarity to historical ADHD clinical cohort patterns</span>
        </div>
        <div style="background-color: rgba(210, 153, 34, 0.08); border-left: 4px solid #D29922; padding: 12px; border-radius: 4px; font-size: 13px; color: #C9D1D9; line-height: 1.4;">
            <strong>⚠️ Clinical Disclaimer:</strong><br>
            This score represents the research model output indicating pattern similarity to participants within the Rojas-Líbano et al. (2019) clinical dataset.
            <strong>This is not a medical diagnosis.</strong> This is an exploratory research engineering demonstration and should not be used as a substitute for professional clinical advice, diagnosis, or treatment. Consult a licensed healthcare specialist for any medical evaluation.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Model predictions are not available because the models were not trained prior to this session.")

# ----------------------------------------------------
# EXPORT PORTION
# ----------------------------------------------------
st.markdown("### 💾 Export Session Outputs")
subject_id = getattr(agg_features, 'subject_id', 'unknown')
col_ex1, col_ex2 = st.columns(2)

with col_ex1:
    # Export clean features to CSV
    clean_cols = [
        'subject_id', 'group',
        'mean_reaction_time_ms', 'median_reaction_time_ms', 'rt_variability', 'rt_coefficient_of_variation',
        'accuracy_overall', 'accuracy_by_load_diff', 'accuracy_by_distractor_diff',
        'mean_fixation_stability', 'mean_pupil_proxy',
        'omission_rate', 'false_alarm_rate', 'hit_rate'
    ]
    feats_dict = {col: getattr(agg_features, col, None) for col in clean_cols}
    df_export = pd.DataFrame([feats_dict])

    csv_data = df_export.to_csv(index=False)
    st.download_button(
        label="📥 Download Session Features CSV",
        data=csv_data,
        file_name=f"session_features_{subject_id}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_ex2:
    # Export session metadata to JSON
    metadata = {
        "participant_id": subject_id,
        "date": pd.Timestamp.now().isoformat(),
        "task_type": "sternberg_task",
        "device": st.session_state.get('device_info', {}).get("device", "Unknown"),
        "browser": st.session_state.get('device_info', {}).get("browser", "Unknown"),
        "camera_resolution": st.session_state.get('device_info', {}).get("camera_resolution", "Unknown"),
        "fps": st.session_state.get('device_info', {}).get("fps", 30),
        "calibration_metrics": cal_metrics,
        "framework_version": agg_features.framework_version,
        "feature_extractor_version": agg_features.feature_extractor_version,
        "model_version": agg_features.model_version,
        "dataset_version": agg_features.dataset_version
    }
    json_data = json.dumps(metadata, indent=4)
    st.download_button(
        label="📥 Download Session Metadata JSON",
        data=json_data,
        file_name=f"session_metadata_{subject_id}.json",
        mime="application/json",
        use_container_width=True
    )

st.markdown("---")
st.markdown("### 🏁 End Experiment Session")
if st.button("Close Experiment Session & Lock Logs", use_container_width=True, type="primary"):
    close_active_session()
    st.success("🎉 Experiment session closed and locked successfully! Gaze logs are preserved. You can register a new participant in the Experiment Manager.")
    if st.button("Return to Home"):
        st.switch_page("pages/Home.py")
