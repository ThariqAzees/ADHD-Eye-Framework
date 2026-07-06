import os
import json
import streamlit as st
import pandas as pd
from dataset.build_dataset import download_real_dataset, generate_mock_dataset, build_processed_dataset, get_data_dirs
from ml.train_model import train_and_evaluate_pipelines

# Setup session states
if 'subject_id' not in st.session_state:
    st.session_state['subject_id'] = "participant_01"
if 'device_info' not in st.session_state:
    st.session_state['device_info'] = {
        "device": "Webcam",
        "browser": "Chrome",
        "camera_resolution": "640x480",
        "fps": 30
    }

st.title("👁️ ADHD Eye Framework")
st.subheader("Webcam-Based Eye Movement Analysis & Cognitive Working Memory Research Platform")

# Disclaimer Box
st.markdown("""
<div class="disclaimer-box" style="background-color: rgba(210, 153, 34, 0.1); border-left: 4px solid #D29922; padding: 16px; border-radius: 4px; margin-bottom: 24px;">
    <strong>⚠️ IMPORTANT RESEARCH DISCLAIMER</strong><br>
    This software is an exploratory research engineering platform and <strong>not</strong> a diagnostic instrument or clinical tool. 
    It does not diagnose, treat, or detect ADHD or any other clinical condition. The machine learning model outputs similarity scores 
    comparing task performance patterns to a specific historical clinical dataset. A qualified healthcare professional must be consulted 
    for any actual diagnostic evaluation or healthcare concern.
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### 📋 Participant Configuration")
    with st.container(border=True):
        subj_id = st.text_input("Participant/Subject ID:", value=st.session_state['subject_id'])
        st.session_state['subject_id'] = subj_id
        
        st.markdown("**Session Metadata (Hardware/Browser Environment)**")
        col_dev, col_brow = st.columns(2)
        with col_dev:
            device = st.text_input("Device:", value=st.session_state['device_info']['device'])
        with col_brow:
            browser = st.text_input("Browser:", value=st.session_state['device_info']['browser'])
            
        col_res, col_fps = st.columns(2)
        with col_res:
            resolution = st.text_input("Camera Resolution:", value=st.session_state['device_info']['camera_resolution'])
        with col_fps:
            fps = st.number_input("Est. FPS:", value=st.session_state['device_info']['fps'], min_value=1, max_value=240)
            
        st.session_state['device_info'] = {
            "device": device,
            "browser": browser,
            "camera_resolution": resolution,
            "fps": int(fps)
        }

    st.markdown("### 💾 Dataset Management")
    with st.container(border=True):
        raw_dir, processed_dir, _ = get_data_dirs()
        mat_path = os.path.join(raw_dir, "Pupil_dataset.mat")
        features_path = os.path.join(processed_dir, "dataset_features_v1.0.csv")
        
        # Check mat file presence
        mat_exists = os.path.exists(mat_path)
        if mat_exists:
            st.success("✅ `Pupil_dataset.mat` is present in `data/raw/`.")
        else:
            st.warning("⚠️ `Pupil_dataset.mat` is missing.")
            
        col_dl_real, col_dl_mock = st.columns(2)
        
        # Real dataset download trigger
        with col_dl_real:
            if st.button("Download Figshare Dataset (~1.25 GB)", use_container_width=True, disabled=mat_exists):
                progress_bar = st.progress(0.0)
                status_text = st.empty()
                try:
                    def update_progress(pct):
                        progress_bar.progress(pct / 100.0)
                        status_text.text(f"Downloading... {pct:.1f}%")
                        
                    download_real_dataset(progress_callback=update_progress)
                    st.success("Download and checksum verification complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Download failed: {e}")
                    
        # Mock dataset generator fallback
        with col_dl_mock:
            if st.button("Generate Mock Dataset (Fast Testing)", use_container_width=True, disabled=mat_exists):
                with st.spinner("Generating mock data..."):
                    generate_mock_dataset()
                st.success("Mock dataset created successfully!")
                st.rerun()
                
        st.markdown("---")
        
        # Build features trigger
        features_exists = os.path.exists(features_path)
        if st.button("Extract Features & Run Validation", use_container_width=True, disabled=not mat_exists):
            with st.spinner("Parsing MATLAB structures and extracting features..."):
                _, validation_report = build_processed_dataset(mat_path)
                
            st.success("Feature extraction completed successfully!")
            
            # Show validation details
            st.markdown("#### 🔍 Dataset Validation Metrics")
            st.write(f"- **Total Participants:** {validation_report['num_participants']} (Valid: {validation_report['num_participants_valid']})")
            st.write(f"- **Class Counts:** {validation_report['class_counts']} (Control: 22, ADHD: 28)")
            st.write(f"- **Load-Effect Check (accuracy(1-dot) > accuracy(2-dot)):** {validation_report['mean_accuracy_by_load_diff']:.4f} (Passed: {validation_report['load_effect_valid']})")
            st.write(f"- **Reaction Time Range:** {validation_report['rt_range']['min']:.1f}ms to {validation_report['rt_range']['max']:.1f}ms (Valid: {validation_report['rt_range_valid']})")
            st.write(f"- **Missing Value Count:** {sum(validation_report['missing_value_counts'].values())} (Has Missing: {validation_report['has_missing_values']})")
            
            if validation_report['all_valid']:
                st.success("✅ All validation suite checks passed!")
            else:
                st.warning("⚠️ Some validation checks failed. Please check the reports.")

with col_right:
    st.markdown("### 🤖 ML Pipeline Control")
    with st.container(border=True):
        models_path = os.path.join(os.path.dirname(os.path.dirname(processed_dir)), "ml", "models_v1.0.pkl")
        models_exist = os.path.exists(models_path)
        
        if models_exist:
            st.success("✅ Trained models (`models_v1.0.pkl`) are ready.")
        else:
            st.warning("⚠️ Models have not been trained yet.")
            
        if st.button("Train Machine Learning Pipeline (Nested CV)", use_container_width=True, disabled=not os.path.exists(features_path)):
            with st.spinner("Running Nested Cross-Validation hyperparameter tuning and model training..."):
                metrics = train_and_evaluate_pipelines()
                st.success("Training and pipeline bundling completed!")
                st.rerun()
                
        # If models exist, display metrics comparison
        if models_exist:
            st.markdown("#### 📊 Model Selection Comparison (Nested CV Outer Folds)")
            
            with open(models_path, 'rb') as f:
                package = pickle_load_compatible = pd.read_pickle(models_path)
                
            metrics = package['metadata']['nested_cv_results']
            
            # Format comparison table
            comparison_data = []
            for model_name, metrics_dict in metrics.items():
                row = {
                    "Model": model_name.replace("_", " ").title(),
                    "Accuracy": f"{metrics_dict['accuracy']['mean']:.3f} ± {metrics_dict['accuracy']['std']:.3f}",
                    "Precision": f"{metrics_dict['precision']['mean']:.3f} ± {metrics_dict['precision']['std']:.3f}",
                    "Recall": f"{metrics_dict['recall']['mean']:.3f} ± {metrics_dict['recall']['std']:.3f}",
                    "F1 Score": f"{metrics_dict['f1']['mean']:.3f} ± {metrics_dict['f1']['std']:.3f}",
                    "ROC AUC": f"{metrics_dict['auc']['mean']:.3f} ± {metrics_dict['auc']['std']:.3f}"
                }
                comparison_data.append(row)
                
            st.table(pd.DataFrame(comparison_data))
            st.info("The packaged model uses the hyperparameter configuration that achieved the highest F1 score in outer folds.")
