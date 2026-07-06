"""
ADHD Eye Framework - Stimulus Rendering Documentation

NOTE ON ARCHITECTURE:
Stimulus elements are drawn on a high-refresh rate HTML5 Canvas element client-side inside:
`tracking/frontend/index.html` (lines 1126-1275)

This module describes how standard stimuli from the Rojas-Líbano dataset are drawn.
"""

STIMULI_DESCRIPTION = {
    "fixation_cross": "White cross on dark background drawn in screen center.",
    "4x4_grid": "4x4 grid of thin gray borders. Each cell is 80x80px.",
    "dots_array": "Light blue circles (14px radius) drawn in the center of randomized grid cells.",
    "distractor_neutral": "Solid gray square (300x300px) drawn in the center.",
    "distractor_task_related": "Complex overlay grid of thin blue cross lines drawn in the center.",
    "distractor_emotional": "Large bright red pulsing broken heart emoji (💔) drawn in the center.",
    "probe": "Single yellow circle (14px radius) drawn in a grid cell center.",
    "buttons": "Interactive YES and NO buttons drawn in green and red below the grid."
}
