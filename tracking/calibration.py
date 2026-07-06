"""
ADHD Eye Framework - Calibration Module Documentation

NOTE ON ARCHITECTURE:
To satisfy sub-millisecond precision requirements and avoid streaming high-frequency raw frame data
over HTTP/WebSockets (which introduces network lag and UI stutter), calibration and eye-tracking 
fitting are implemented client-side in HTML5/JavaScript inside:
`tracking/frontend/index.html` (lines 615-785)

This module provides a documentation bridge for the backend.
"""

import os
import json
import datetime
import pandas as pd
from dataset.build_dataset import get_data_dirs

CALIBRATION_STEPS = [
    "1. Present 9 points on a randomized grid on the screen (0.1, 0.5, 0.9 screen boundaries).",
    "2. Prompt the user to fixate on each target dot for 1000ms to allow saccade settling.",
    "3. Collect normalized pupil-center-to-iris-center coordinates (dx, dy) for 1000ms at 20Hz (50ms intervals).",
    "4. Fit a 2nd-degree polynomial mapping using L2-regularized Ridge Regression (Normal Equations) client-side.",
    "5. Evaluate validation quality using a 5-point grid, calculating Mean and Median Euclidean Error in pixels."
]

def get_calibration_metadata() -> dict:
    """Returns metadata regarding the calibration parameters."""
    return {
        "num_calibration_points": 9,
        "collection_rate_hz": 20,
        "settling_delay_ms": 1000,
        "fit_degree": 2,
        "regularization_lambda": 0.001
    }

def export_calibration_report(calibration_diagnostics: dict, subject_id: str) -> tuple:
    """
    Exports the calibration summary metrics to JSON and high-frequency verification samples to CSV.
    """
    if not calibration_diagnostics:
        return None, None
        
    _, _, exports_dir = get_data_dirs()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Separate verification frame log
    verification_log = calibration_diagnostics.pop('verification_log', [])
    
    # 2. Write verification frame log to CSV
    csv_path = None
    if verification_log:
        df = pd.DataFrame(verification_log)
        csv_filename = f"calibration_verification_{timestamp}.csv"
        csv_path = os.path.join(exports_dir, csv_filename)
        df.to_csv(csv_path, index=False)
        
    # 3. Write summary report to JSON
    json_filename = f"calibration_report_{timestamp}.json"
    json_path = os.path.join(exports_dir, json_filename)
    
    report = {
        "participant_id": subject_id,
        "timestamp": datetime.datetime.now().isoformat(),
        **calibration_diagnostics
    }
    
    # Put verification_log back just in case the caller needs it
    calibration_diagnostics['verification_log'] = verification_log
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    return json_path, csv_path
