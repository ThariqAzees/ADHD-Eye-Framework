import datetime
import uuid
from typing import List, Optional, Dict, Any
import streamlit as st
from experiment.database import insert_session, get_session, update_session_status, update_session_device_info, get_all_sessions
from experiment.models import Session

STATE_ORDER = [
    "NOT_STARTED",
    "STUDY_CONFIGURED",
    "PARTICIPANT_REGISTERED",
    "SESSION_CREATED",
    "CALIBRATION_STARTED",
    "CALIBRATION_COMPLETED",
    "STERNBERG_STARTED",
    "STERNBERG_COMPLETED",
    "RESULTS_REVIEWED",
    "SESSION_CLOSED"
]

def create_session(
    participant_id: str,
    study_id: str,
    browser: Optional[str] = None,
    operating_system: Optional[str] = None,
    screen_resolution: Optional[str] = None,
    webcam_information: Optional[str] = None
) -> Session:
    """Creates a new experiment session in the database and initializes its state."""
    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    start_time = datetime.datetime.now().isoformat()
    
    session_data = {
        'session_id': session_id,
        'participant_id': participant_id,
        'study_id': study_id,
        'start_time': start_time,
        'status': 'SESSION_CREATED',
        'browser': browser,
        'operating_system': operating_system,
        'screen_resolution': screen_resolution,
        'webcam_information': webcam_information
    }
    
    insert_session(session_data)
    
    # Store session in Streamlit session state
    st.session_state["session_id"] = session_id
    st.session_state["participant_id"] = participant_id
    st.session_state["study_id"] = study_id
    transition_experiment_state("SESSION_CREATED")
    
    # Log session creation event
    from experiment.logger import ExperimentLogger
    logger = ExperimentLogger(session_id)
    logger.log_system_event(
        "Session Created", 
        {"participant_id": participant_id, "study_id": study_id, "start_time": start_time}
    )
    
    return Session(
        session_id=session_id,
        participant_id=participant_id,
        study_id=study_id,
        start_time=start_time,
        status='SESSION_CREATED',
        browser=browser,
        operating_system=operating_system,
        screen_resolution=screen_resolution,
        webcam_information=webcam_information
    )

def get_session_details(session_id: str) -> Optional[Session]:
    """Retrieves session details from the database."""
    data = get_session(session_id)
    if not data:
        return None
    return Session(
        session_id=data['session_id'],
        participant_id=data['participant_id'],
        study_id=data['study_id'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        status=data['status'],
        browser=data['browser'],
        operating_system=data['operating_system'],
        screen_resolution=data['screen_resolution'],
        webcam_information=data['webcam_information'],
        created_at=data['created_at']
    )

def transition_experiment_state(new_state: str) -> None:
    """Transitions the experiment state machine to a new state and synchronizes with DB."""
    st.session_state["experiment_state"] = new_state
    
    # Sync with DB if session is active
    session_id = st.session_state.get("session_id")
    if session_id:
        end_time = None
        if new_state == "SESSION_CLOSED":
            end_time = datetime.datetime.now().isoformat()
            
        update_session_status(session_id, new_state, end_time)
        
        # Log state transition as a system event
        from experiment.logger import ExperimentLogger
        logger = ExperimentLogger(session_id)
        logger.log_system_event("State Transition", {"new_state": new_state})

def close_active_session() -> None:
    """Closes the current active session, setting status to SESSION_CLOSED."""
    session_id = st.session_state.get("session_id")
    if session_id:
        transition_experiment_state("SESSION_CLOSED")
        
        # Clear active session state variables
        st.session_state["session_id"] = None
        st.session_state["participant_id"] = None
        # We keep study_id for configuration convenience, or reset if desired

def update_session_telemetry(
    session_id: str,
    browser: Optional[str],
    operating_system: Optional[str],
    screen_resolution: Optional[str],
    webcam_information: Optional[str]
) -> None:
    """Updates the session device telemetry in the database."""
    device_data = {
        'browser': browser,
        'operating_system': operating_system,
        'screen_resolution': screen_resolution,
        'webcam_information': webcam_information
    }
    update_session_device_info(session_id, device_data)
    
    # Also log a tracking event indicating device telemetry has been captured
    from experiment.logger import ExperimentLogger
    logger = ExperimentLogger(session_id)
    logger.log_tracking_event("Device Telemetry Captured", device_data)

def list_all_sessions_records() -> List[Dict[str, Any]]:
    """Lists all session records formatted for data tables."""
    return get_all_sessions()
