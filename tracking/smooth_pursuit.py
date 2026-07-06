import os
import json
import datetime
import pandas as pd
from dataset.build_dataset import get_data_dirs

def save_smooth_pursuit_session(raw_log: list, subject_id: str, calibration_metrics: dict, metadata_args: dict = None) -> tuple:
    """
    Saves the complete frame-by-frame smooth pursuit logs and exports session metadata separately.
    """
    raw_dir, _, exports_dir = get_data_dirs()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Save Complete Raw Frame Logs
    df = pd.DataFrame(raw_log)
    # Add constraint columns visible in the data itself
    df['used_in_model'] = False
    
    csv_filename = f"smooth_pursuit_session_{timestamp}.csv"
    csv_path = os.path.join(raw_dir, csv_filename)
    df.to_csv(csv_path, index=False)
    
    # 2. Save Session Metadata separately
    meta_filename = f"session_metadata_{timestamp}.json"
    meta_path = os.path.join(exports_dir, meta_filename)
    
    metadata = {
        "participant_id": subject_id,
        "date": datetime.datetime.now().isoformat(),
        "task_type": "smooth_pursuit",
        "device": metadata_args.get("device", "Unknown"),
        "browser": metadata_args.get("browser", "Unknown"),
        "camera_resolution": metadata_args.get("camera_resolution", "Unknown"),
        "fps": metadata_args.get("fps", 30),
        "calibration_metrics": calibration_metrics,
        "framework_version": "1.0.0",
        "feature_extractor_version": "1.0.0",
        "model_version": "1.0.0",
        "dataset_version": "Rojas-Libano-2019-v3"
    }
    
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Smooth pursuit raw log saved to {csv_path}")
    print(f"Session metadata saved to {meta_path}")
    
    return csv_path, meta_path
