from typing import List, Optional
from experiment.database import insert_participant, get_participant, get_participants_by_study
from experiment.models import Participant

def register_participant(
    participant_id: str,
    study_id: str,
    age_group: str,
    vision_correction: Optional[str] = None,
    dominant_hand: Optional[str] = None,
    consent_obtained: bool = False
) -> Participant:
    """Registers an anonymous participant in the database for a specific study."""
    part_data = {
        'participant_id': participant_id,
        'study_id': study_id,
        'age_group': age_group,
        'vision_correction': vision_correction,
        'dominant_hand': dominant_hand,
        'consent_obtained': consent_obtained
    }
    insert_participant(part_data)
    return Participant(
        participant_id=participant_id,
        study_id=study_id,
        age_group=age_group,
        vision_correction=vision_correction,
        dominant_hand=dominant_hand,
        consent_obtained=consent_obtained
    )

def get_participant_details(participant_id: str, study_id: str) -> Optional[Participant]:
    """Retrieves participant details by their ID within a specific study."""
    data = get_participant(participant_id, study_id)
    if not data:
        return None
    return Participant(
        participant_id=data['participant_id'],
        study_id=data['study_id'],
        age_group=data['age_group'],
        vision_correction=data['vision_correction'],
        dominant_hand=data['dominant_hand'],
        consent_obtained=bool(data['consent_obtained']),
        created_at=data['created_at']
    )

def is_duplicate_participant(participant_id: str, study_id: str) -> bool:
    """Checks if a participant ID is already registered for a specific study."""
    return get_participant(participant_id, study_id) is not None

def list_participants_for_study(study_id: str) -> List[Participant]:
    """Lists all participants registered for a study."""
    rows = get_participants_by_study(study_id)
    return [
        Participant(
            participant_id=r['participant_id'],
            study_id=r['study_id'],
            age_group=r['age_group'],
            vision_correction=r['vision_correction'],
            dominant_hand=r['dominant_hand'],
            consent_obtained=bool(r['consent_obtained']),
            created_at=r['created_at']
        ) for r in rows
    ]
