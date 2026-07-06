from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Study:
    study_id: str
    study_name: str
    version: str
    calibration_protocol: str
    practice_trials: int
    task_order: str
    counterbalancing_enabled: bool
    notes: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class Participant:
    participant_id: str
    study_id: str
    age_group: str
    vision_correction: Optional[str] = None
    dominant_hand: Optional[str] = None
    consent_obtained: bool = False
    created_at: Optional[str] = None

@dataclass
class Session:
    session_id: str
    participant_id: str
    study_id: str
    start_time: str
    end_time: Optional[str] = None
    status: str = "NOT_STARTED"
    browser: Optional[str] = None
    operating_system: Optional[str] = None
    screen_resolution: Optional[str] = None
    webcam_information: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class Event:
    event_id: Optional[int]
    session_id: str
    timestamp: str
    event_category: str
    event_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
