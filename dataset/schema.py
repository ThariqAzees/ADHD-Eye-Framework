from dataclasses import dataclass
from typing import Optional

@dataclass
class TrialFeatures:
    subject_id: str
    group: Optional[str]                          # 'ADHD' / 'Control' / None for live users
    load: int                                     # 1 or 2 dots
    distractor_type: str                          # 'neutral' / 'task_related' / 'emotional' / 'none'
    trial_accuracy: int                           # 0 or 1
    reaction_time_ms: float
    fixation_stability: float                     # Legacy pixel-based
    pupil_proxy_mean: float                       # Legacy mean of trial pupil z-scores
    pupil_proxy_trial_slope: float
    gaze_dispersion_during_array: float           # Legacy pixel-based
    normalized_fixation_instability: Optional[float]  # Normalized coordinate fixation instability
    normalized_gaze_dispersion: Optional[float]       # Normalized coordinate gaze dispersion

@dataclass
class SubjectAggregateFeatures:
    subject_id: str
    group: Optional[str]
    mean_reaction_time_ms: float
    median_reaction_time_ms: float
    rt_variability: float                         # Standard deviation of RTs
    rt_coefficient_of_variation: float            # RT SD / Mean RT
    accuracy_overall: float
    accuracy_by_load_diff: Optional[float]        # accuracy(1-dot) - accuracy(2-dot)
    accuracy_by_distractor_diff: Optional[float]  # accuracy(none) - accuracy(emotional)
    mean_fixation_stability: float               # Legacy pixel-based
    mean_pupil_proxy: float                      # Legacy mean of z-scores (near zero)
    normalized_fixation_instability: Optional[float]  # Normalized coordinate fixation instability
    normalized_gaze_dispersion: Optional[float]       # Normalized coordinate gaze dispersion
    pupil_variability: Optional[float]                # Session-level SD of trial means
    omission_rate: float                          # Rate of trials with no response (e.g. timeout)
    false_alarm_rate: Optional[float]             # Rate of incorrect 'yes' responses
    hit_rate: Optional[float]                     # Rate of correct 'yes' responses
    
    # Version metadata
    framework_version: str = "1.0.0"
    feature_extractor_version: str = "1.0.0"
    model_version: str = "1.0.0"
    dataset_version: str = "Rojas-Libano-2019-v3"
