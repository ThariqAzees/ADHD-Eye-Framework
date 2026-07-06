"""
ADHD Eye Framework - Sternberg Task Engine Documentation

NOTE ON ARCHITECTURE:
To ensure sub-millisecond precision, keyboard event listeners, and low-latency canvas rendering, 
the Sternberg trial sequencer, timers, and state machine are implemented client-side in HTML5/JavaScript inside:
`tracking/frontend/index.html` (lines 916-1008 and lines 1277-1311)

This module provides a documentation bridge for backend verification.
"""

TRIAL_PHASES = {
    "fixation1": "Central fixation cross — 500ms.",
    "array1": "Dot array #1 (1 or 2 dots on a 4×4 grid) — 750ms.",
    "fixation2": "Fixation cross — 500ms.",
    "array2": "Dot array #2 — 750ms.",
    "fixation3": "Fixation cross — 500ms.",
    "array3": "Dot array #3 — 750ms.",
    "distractor": "Distractor image (neutral / task-related / emotional / none) — 500ms.",
    "probe": "Probe dot + Yes/No response capture — up to 1500ms (timeout leads to omission).",
    "feedback": "Feedback screen (CORRECT / INCORRECT / TIMEOUT) — 800ms."
}

def get_trial_parameters() -> dict:
    """Returns task parameters."""
    return {
        "num_trials": 40,
        "load_types": [1, 2],
        "distractors": ["none", "neutral", "emotional", "task_related"],
        "probe_timeout_ms": 1500
    }
