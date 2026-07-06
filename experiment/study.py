from typing import List, Optional
from experiment.database import insert_study, get_study, get_all_studies
from experiment.models import Study

def create_study(
    study_id: str,
    study_name: str,
    version: str,
    calibration_protocol: str,
    practice_trials: int,
    task_order: str,
    counterbalancing_enabled: bool,
    notes: Optional[str] = None
) -> Study:
    """Creates a new study configuration and stores it in the database."""
    study_data = {
        'study_id': study_id,
        'study_name': study_name,
        'version': version,
        'calibration_protocol': calibration_protocol,
        'practice_trials': practice_trials,
        'task_order': task_order,
        'counterbalancing_enabled': counterbalancing_enabled,
        'notes': notes
    }
    insert_study(study_data)
    return Study(
        study_id=study_id,
        study_name=study_name,
        version=version,
        calibration_protocol=calibration_protocol,
        practice_trials=practice_trials,
        task_order=task_order,
        counterbalancing_enabled=counterbalancing_enabled,
        notes=notes
    )

def get_study_details(study_id: str) -> Optional[Study]:
    """Retrieves the details of a study configuration by its ID."""
    data = get_study(study_id)
    if not data:
        return None
    return Study(
        study_id=data['study_id'],
        study_name=data['study_name'],
        version=data['version'],
        calibration_protocol=data['calibration_protocol'],
        practice_trials=data['practice_trials'],
        task_order=data['task_order'],
        counterbalancing_enabled=bool(data['counterbalancing_enabled']),
        notes=data['notes'],
        created_at=data['created_at']
    )

def list_studies() -> List[Study]:
    """Lists all study configurations registered in the database."""
    rows = get_all_studies()
    return [
        Study(
            study_id=r['study_id'],
            study_name=r['study_name'],
            version=r['version'],
            calibration_protocol=r['calibration_protocol'],
            practice_trials=r['practice_trials'],
            task_order=r['task_order'],
            counterbalancing_enabled=bool(r['counterbalancing_enabled']),
            notes=r['notes'],
            created_at=r['created_at']
        ) for r in rows
    ]
