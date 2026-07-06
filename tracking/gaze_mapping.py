"""
ADHD Eye Framework - Gaze Mapping Documentation

NOTE ON ARCHITECTURE:
To maintain real-time low-latency feedback (~60fps rendering), predicted gaze (x, y) coordinates
are calculated client-side in HTML5/JavaScript inside:
`tracking/frontend/index.html` (lines 311-375 and lines 574-608)

This module documents the mathematical mapping equations.
"""

# The feature vector for polynomial regression:
# For relative iris offset dx and dy:
# feat = [1, dx, dy, dx^2, dy^2, dx*dy]
#
# The model maps features to screen pixel locations:
# Gaze_X = wX^T * feat * ScreenWidth
# Gaze_Y = wY^T * feat * ScreenHeight
#
# Weights wX and wY are solved using L2-regularized Ridge Regression client-side:
# w = (X^T * X + lambda * I)^-1 * X^T * Y

def get_mapping_formula() -> str:
    """Returns mapping formula description."""
    return "Polynomial Ridge Regression: w = (X^T * X + lambda * I)^-1 * X^T * Y"
