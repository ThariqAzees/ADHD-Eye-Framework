import os
import streamlit.components.v1 as components

# Get the path to the frontend directory containing index.html
parent_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(parent_dir, "frontend")

# Declare the Streamlit component using path
_component_func = components.declare_component(
    "gaze_tracker",
    path=frontend_dir
)

def gaze_tracker(task_type: str, calibration_thresholds: dict, key=None):
    """
    Renders the custom client-side eye tracking, calibration and task sequencer component.
    
    Parameters:
    - task_type: 'calibration_only' or 'sternberg_task'
    - calibration_thresholds: dict from config.json containing excellent, good, fair thresholds.
    - key: unique identifier for the Streamlit component instance.
    
    Returns:
    - Dict/object sent back from JavaScript containing the session logs or status.
    """
    return _component_func(
        task_type=task_type,
        calibration_thresholds=calibration_thresholds,
        key=key,
        default=None,
        height=700
    )
