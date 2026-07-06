import datetime
from typing import Dict, Any
from experiment.database import insert_event

class ExperimentLogger:
    """A reusable instrumentation logger for logging researcher, participant, and system events to SQLite."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id

    def log_event(self, category: str, event_type: str, payload: Dict[str, Any] = None, timestamp: str = None) -> None:
        """Logs a structured event linked to the active session."""
        if not self.session_id:
            return
        if not timestamp:
            timestamp = datetime.datetime.now().isoformat()
        insert_event(self.session_id, timestamp, category, event_type, payload or {})

    def log_system_event(self, event_type: str, payload: Dict[str, Any] = None, timestamp: str = None) -> None:
        """Logs system-related events, such as workflow status, state transitions, or device status."""
        self.log_event("SYSTEM_EVENT", event_type, payload, timestamp)

    def log_user_event(self, event_type: str, payload: Dict[str, Any] = None, timestamp: str = None) -> None:
        """Logs researcher or user interaction events, such as UI clicks or configuration adjustments."""
        self.log_event("USER_EVENT", event_type, payload, timestamp)

    def log_task_event(self, event_type: str, payload: Dict[str, Any] = None, timestamp: str = None) -> None:
        """Logs cognitive task milestones, like task start, step completion, or trials loaded."""
        self.log_event("TASK_EVENT", event_type, payload, timestamp)

    def log_tracking_event(self, event_type: str, payload: Dict[str, Any] = None, timestamp: str = None) -> None:
        """Logs tracking landmarks, calibration progress, validation errors, and confidence changes."""
        self.log_event("TRACKING_EVENT", event_type, payload, timestamp)

    def log_questionnaire_event(self, event_type: str, payload: Dict[str, Any] = None, timestamp: str = None) -> None:
        """Logs survey or subjective rating responses (reserved for Phase 2)."""
        self.log_event("QUESTIONNAIRE_EVENT", event_type, payload, timestamp)
