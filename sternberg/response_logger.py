"""
ADHD Eye Framework - Response Logger Documentation

NOTE ON ARCHITECTURE:
User responses (mouse clicks or keyboard presses) and millisecond reaction times (using performance.now())
are tracked client-side in HTML5/JavaScript inside:
`tracking/frontend/index.html` (lines 1046-1124)

Logged session features are exported via st.download_button or saved by the feature extractor on completion.
"""

def parse_raw_response(log_entry: dict) -> dict:
    """
    Parses a single trial response dictionary.
    Keys expected from frontend: trial, load, distractor_type, corr_response, user_response, accuracy, reaction_time_ms.
    """
    return {
        "trial": int(log_entry.get("trial", 0)),
        "load": int(log_entry.get("load", 1)),
        "distractor_type": str(log_entry.get("distractor_type", "none")),
        "correct_response": int(log_entry.get("corr_response", 0)),
        "user_response": int(log_entry.get("user_response", -1)),
        "accuracy": int(log_entry.get("accuracy", 0)),
        "reaction_time_ms": float(log_entry.get("reaction_time_ms", 0.0))
    }
