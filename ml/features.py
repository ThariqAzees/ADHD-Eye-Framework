"""
ML Features Definitions and Schema Mapping for the ADHD Eye Framework.
Aligns with the subject and trial aggregates defined in dataset/schema.py.
"""

from typing import List

# Complete list of engineered features used in the ML training and inference
FEATURE_NAMES: List[str] = [
    'mean_reaction_time_ms',
    'median_reaction_time_ms',
    'rt_variability',
    'rt_coefficient_of_variation',
    'accuracy_overall',
    'accuracy_by_load_diff',
    'accuracy_by_distractor_diff',
    'mean_fixation_stability',
    'mean_pupil_proxy',
    'omission_rate',
    'false_alarm_rate',
    'hit_rate'
]

FEATURE_DESCRIPTIONS = {
    'mean_reaction_time_ms': 'Mean reaction time in milliseconds for correct trials.',
    'median_reaction_time_ms': 'Median reaction time in milliseconds for correct trials.',
    'rt_variability': 'Standard deviation of reaction times (indicates performance variability).',
    'rt_coefficient_of_variation': 'Reaction time standard deviation divided by mean reaction time.',
    'accuracy_overall': 'Overall accuracy across all trials (0.0 to 1.0).',
    'accuracy_by_load_diff': 'Accuracy on load 1 (1 dot) minus accuracy on load 2 (2 dots). Shows working memory load effect.',
    'accuracy_by_distractor_diff': 'Accuracy on trials with no distractor minus accuracy on emotional distractor trials.',
    'mean_fixation_stability': 'Standard deviation of gaze coordinates during fixation delays (lower = more stable).',
    'mean_pupil_proxy': 'Mean of iris radius size proxy across trials (units not comparable to baseline EyeLink data).',
    'omission_rate': 'Rate of trials with no response (timeout or missed response).',
    'false_alarm_rate': 'Rate of incorrect "Yes" responses when the probe target was not in memory.',
    'hit_rate': 'Rate of correct "Yes" responses when the probe target was in memory.'
}
