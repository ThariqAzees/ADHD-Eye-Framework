import streamlit as st
import pandas as pd
import datetime
from experiment.Experiment_Manager import (
    create_study, list_studies, get_study_details,
    register_participant, get_participant_details, is_duplicate_participant,
    create_session, get_session_details, close_active_session, list_all_sessions_records,
    ExperimentLogger, transition_experiment_state
)
from experiment.database import get_events_by_session

st.title("🔬 Experiment Manager")
st.subheader("Researcher Instrumentation & Control Dashboard")

# Render active session context banner
session_id = st.session_state.get("session_id")
participant_id = st.session_state.get("participant_id")
study_id = st.session_state.get("study_id")
experiment_state = st.session_state.get("experiment_state", "NOT_STARTED")

if session_id:
    st.success(f"📡 **Active Session Connected:** Participant `{participant_id}` | Study `{study_id}` | Session `{session_id}` | State: `{experiment_state}`")
else:
    st.info("📡 **No Active Session:** Register a participant or configure a study below to begin standardise experiment execution.")

# Setup tabs
tab_config, tab_register, tab_monitor, tab_records = st.tabs([
    "⚙️ Study Configuration", 
    "👤 Participant Registration", 
    "📊 Experiment Monitor", 
    "📂 Study Records"
])

# ==============================================================================
# TAB 1: STUDY CONFIGURATION
# ==============================================================================
with tab_config:
    st.markdown("### ⚙️ Configure HCI Human-Subject Study")
    st.write("Define a standardized study configuration before onboarding participants. These settings will override application defaults during active sessions.")
    
    with st.form("study_config_form"):
        col_name, col_ver = st.columns(2)
        with col_name:
            study_name = st.text_input("Study Name:", placeholder="e.g. HCI Eye Tracking Study 2026")
        with col_ver:
            version = st.text_input("Version:", value="1.0", placeholder="e.g. 1.0")
            
        col_proto, col_trials = st.columns(2)
        with col_proto:
            calibration_protocol = st.selectbox(
                "Calibration Protocol:",
                options=["9-Point Grid (Standard)", "5-Point Grid (Fast)", "13-Point Grid (High Precision)"]
            )
        with col_trials:
            practice_trials = st.number_input("Number of Practice Trials:", min_value=0, max_value=10, value=2)
            
        col_order, col_counter = st.columns(2)
        with col_order:
            task_order = st.selectbox(
                "Task Order:",
                options=["Calibration -> Sternberg Task"]
            )
        with col_counter:
            counterbalancing_enabled = st.checkbox("Enable Task Counterbalancing", value=False)
            
        notes = st.text_area("Study Notes & Documentation:", placeholder="Add researcher instructions or details here...")
        
        submit_study = st.form_submit_button("Save Study Configuration")
        
    if submit_study:
        if not study_name.strip():
            st.error("Please enter a valid study name.")
        else:
            # Generate unique study ID
            generated_study_id = f"study_{study_name.lower().replace(' ', '_')}_{version.replace('.', '_')}"
            try:
                study = create_study(
                    study_id=generated_study_id,
                    study_name=study_name.strip(),
                    version=version.strip(),
                    calibration_protocol=calibration_protocol,
                    practice_trials=int(practice_trials),
                    task_order=task_order,
                    counterbalancing_enabled=counterbalancing_enabled,
                    notes=notes.strip() if notes else None
                )
                st.session_state["study_id"] = generated_study_id
                transition_experiment_state("STUDY_CONFIGURED")
                st.success(f"✅ Study Configuration saved successfully! ID: `{generated_study_id}`")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save study configuration: {e}")

# ==============================================================================
# TAB 2: PARTICIPANT REGISTRATION
# ==============================================================================
with tab_register:
    st.markdown("### 👤 Register Participant & Start Session")
    st.write("Enroll an anonymous subject to generate a new experiment session ID. Strictly no PII (names, emails, etc.) should be recorded.")
    
    # Check if a study is selected/configured
    studies_list = list_studies()
    if not studies_list:
        st.warning("⚠️ No studies configured. Please save a Study Configuration in the first tab before registering participants.")
    else:
        study_options = {s.study_id: f"{s.study_name} (v{s.version})" for s in studies_list}
        selected_study_id = st.selectbox("Select Study context:", options=list(study_options.keys()), format_func=lambda x: study_options[x])
        
        # Display duplicate validation options if flagged in session state
        if st.session_state.get("duplicate_participant_data"):
            dup_data = st.session_state["duplicate_participant_data"]
            st.warning(f"⚠️ **Duplicate Participant ID Detected:** `{dup_data['participant_id']}` is already registered for study `{dup_data['study_id']}`.")
            
            col_resume, col_new, col_cancel = st.columns(3)
            with col_resume:
                if st.button("Resume Existing Participant", use_container_width=True):
                    # Set current session info to match the existing participant details
                    st.session_state["participant_id"] = dup_data['participant_id']
                    st.session_state["study_id"] = dup_data['study_id']
                    
                    # Create a new session for them
                    sess = create_session(dup_data['participant_id'], dup_data['study_id'])
                    st.success(f"Resumed participant! Session: `{sess.session_id}`")
                    st.session_state["duplicate_participant_data"] = None
                    st.rerun()
            with col_new:
                if st.button("Create New Session", use_container_width=True):
                    sess = create_session(dup_data['participant_id'], dup_data['study_id'])
                    st.success(f"Created new session: `{sess.session_id}`")
                    st.session_state["duplicate_participant_data"] = None
                    st.rerun()
            with col_cancel:
                if st.button("Cancel Registration", use_container_width=True):
                    st.session_state["duplicate_participant_data"] = None
                    st.rerun()
        else:
            # Registration Form
            with st.form("participant_reg_form"):
                reg_participant_id = st.text_input("Participant ID (e.g. sub-024):", placeholder="e.g. sub-024")
                
                col_age, col_correction = st.columns(2)
                with col_age:
                    age_group = st.selectbox("Age Group / Category:", options=["Child (6-11)", "Adolescent (12-17)", "Adult (18-64)", "Elderly (65+)"])
                with col_correction:
                    vision_correction = st.selectbox("Vision Correction:", options=["None", "Glasses", "Contacts", "Other"])
                    
                dominant_hand = st.selectbox("Dominant Hand:", options=["Right", "Left", "Ambidextrous"])
                consent_obtained = st.checkbox("Consent Obtained (Mandatory for human subjects studies)")
                
                submit_reg = st.form_submit_button("Register & Initialize Session")
                
            if submit_reg:
                if not reg_participant_id.strip():
                    st.error("Please enter a valid Participant ID.")
                elif not consent_obtained:
                    st.error("You must obtain participant consent before starting the session.")
                else:
                    clean_part_id = reg_participant_id.strip()
                    # Check for duplicate ID
                    if is_duplicate_participant(clean_part_id, selected_study_id):
                        st.session_state["duplicate_participant_data"] = {
                            "participant_id": clean_part_id,
                            "study_id": selected_study_id,
                            "age_group": age_group,
                            "vision_correction": vision_correction,
                            "dominant_hand": dominant_hand,
                            "consent_obtained": consent_obtained
                        }
                        st.rerun()
                    else:
                        try:
                            # Register participant
                            part = register_participant(
                                participant_id=clean_part_id,
                                study_id=selected_study_id,
                                age_group=age_group,
                                vision_correction=vision_correction,
                                dominant_hand=dominant_hand,
                                consent_obtained=consent_obtained
                            )
                            transition_experiment_state("PARTICIPANT_REGISTERED")
                            
                            # Create new session
                            sess = create_session(clean_part_id, selected_study_id)
                            st.success(f"✅ Participant registered and Session created successfully! Session ID: `{sess.session_id}`")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Registration failed: {e}")

# ==============================================================================
# TAB 3: EXPERIMENT MONITOR
# ==============================================================================
with tab_monitor:
    st.markdown("### 📊 Live Experiment Monitor")
    st.write("Live status monitoring of active participant progress, calibration results, and interactive system events.")
    
    if not session_id:
        st.info("No active experiment session is running. Initialize a session to begin live telemetry.")
    else:
        # Load session details and events
        sess_details = get_session_details(session_id)
        events_list = get_events_by_session(session_id)
        
        # Calculate session duration
        start_dt = datetime.datetime.fromisoformat(sess_details.start_time)
        now_dt = datetime.datetime.now()
        duration_sec = int((now_dt - start_dt).total_seconds())
        duration_str = f"{duration_sec // 60}m {duration_sec % 60}s"
        
        # Extract recent telemetry metrics
        calibration_status = "Not Calibrated"
        tracking_confidence = "N/A"
        fps = sess_details.browser if sess_details.browser else "N/A" # fallback
        
        # Parse events for calibration data
        cal_events = [e for e in events_list if e['event_type'] == "Calibration Completed"]
        if cal_events:
            last_cal = cal_events[-1]
            calibration_status = "Completed"
            tracking_confidence = f"{last_cal['payload'].get('quality', 'Poor')} (Err: {last_cal['payload'].get('mean_error', 999)}px)"
            
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Current State", experiment_state)
            st.metric("Participant ID", participant_id)
        with col_m2:
            st.metric("Calibration Status", calibration_status)
            st.metric("Calibration Quality", tracking_confidence)
        with col_m3:
            st.metric("Session Duration", duration_str)
            st.metric("Browser / OS", f"{sess_details.browser or 'N/A'} / {sess_details.operating_system or 'N/A'}")
            
        # Display buttons to proceed or close
        col_actions1, col_actions2 = st.columns(2)
        with col_actions1:
            st.write("#### 🕹️ Navigation Actions")
            
            st.markdown("""
            **Current Experiment:**
            `Calibration` ➡️ `Sternberg Task`
            """)
            
            if experiment_state in ["SESSION_CREATED", "CALIBRATION_STARTED", "CALIBRATION_COMPLETED", "STERNBERG_STARTED"]:
                if st.button("▶ Start Calibration & Sternberg Task", use_container_width=True):
                    st.switch_page("pages/Sternberg_Task.py")
            elif experiment_state == "STERNBERG_COMPLETED":
                if st.button("📊 View Results Dashboard", use_container_width=True):
                    st.switch_page("pages/Results.py")
            elif experiment_state == "RESULTS_REVIEWED":
                if st.button("🏁 Close Session", use_container_width=True, type="primary"):
                    close_active_session()
                    st.success("Session closed!")
                    st.rerun()
                    
        with col_actions2:
            st.write("#### 🛠️ Administrator Controls")
            if st.button("🛑 Force Close Active Session", use_container_width=True, type="secondary"):
                close_active_session()
                st.warning("Active session has been force closed.")
                st.rerun()
                
            if st.button("🔄 Refresh Live Monitor", use_container_width=True):
                st.rerun()
                
        # Display Live Event Stream
        st.markdown("#### 📜 Live System Event Stream")
        if not events_list:
            st.write("No events logged for this session yet.")
        else:
            # Sort events descending for stream viewing
            sorted_events = sorted(events_list, key=lambda x: x['timestamp'], reverse=True)
            event_rows = []
            for ev in sorted_events:
                # Format timestamp
                time_str = ev['timestamp'].split('T')[-1][:8]
                event_rows.append({
                    "Timestamp": time_str,
                    "Category": ev['event_category'],
                    "Event Type": ev['event_type'],
                    "Payload / Details": str(ev['payload'])
                })
            st.dataframe(pd.DataFrame(event_rows), use_container_width=True)

# ==============================================================================
# TAB 4: STUDY RECORDS
# ==============================================================================
with tab_records:
    st.markdown("### 📂 Study Records")
    st.write("Explore and search logs of all experimental sessions recorded on this station.")
    
    sessions = list_all_sessions_records()
    if not sessions:
        st.info("No study records found in the database.")
    else:
        df_sessions = pd.DataFrame(sessions)
        
        # Rename columns for clear presentation
        df_sessions.rename(columns={
            'participant_id': 'Participant ID',
            'session_id': 'Session ID',
            'study_name': 'Study Name',
            'start_time': 'Start Time',
            'status': 'Status',
            'browser': 'Browser',
            'operating_system': 'OS',
            'screen_resolution': 'Resolution'
        }, inplace=True)
        
        # Search filter inputs
        col_filt1, col_filt2 = st.columns(2)
        with col_filt1:
            search_part = st.text_input("Filter by Participant ID:", value="")
        with col_filt2:
            filter_status = st.selectbox("Filter by Status:", options=["All", "SESSION_CREATED", "CALIBRATION_COMPLETED", "SMOOTH_PURSUIT_COMPLETED", "STERNBERG_COMPLETED", "RESULTS_REVIEWED", "SESSION_CLOSED"])
            
        # Apply search filters
        filtered_df = df_sessions.copy()
        if search_part.strip():
            filtered_df = filtered_df[filtered_df['Participant ID'].str.contains(search_part.strip(), case=False)]
        if filter_status != "All":
            filtered_df = filtered_df[filtered_df['Status'] == filter_status]
            
        columns_to_show = ['Participant ID', 'Session ID', 'Study Name', 'Start Time', 'Status', 'Browser', 'OS', 'Resolution']
        st.dataframe(filtered_df[columns_to_show], use_container_width=True)
