import os
import sys
import unittest
import numpy as np

# Ensure repository root is in search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sternberg.feature_extractor import extract_features_from_logs, is_valid_response, is_omission

# UI formatting helpers replicate Result.py UI functions
def clean_negative_zero(formatted_str: str) -> str:
    if formatted_str.startswith('-'):
        stripped = formatted_str[1:]
        check_str = stripped.replace('%', '').replace('ms', '').replace('pixels', '').replace('pixel', '').strip()
        if all(c in ('0', '.') for c in check_str):
            return stripped
    return formatted_str

def safe_pct(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return clean_negative_zero(f"{val * 100:.1f}%")

def safe_ms(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return clean_negative_zero(f"{val:.1f} ms")

def safe_pixels(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return clean_negative_zero(f"{val:.2f} pixels")

def safe_val(val, fmt="{:.4f}"):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return clean_negative_zero(fmt.format(val))


class TestFeatureExtractor(unittest.TestCase):
    def setUp(self):
        self.subject_id = "test_subject"

    def test_rt_boundary_functions(self):
        # RT = -1
        self.assertTrue(is_omission(-1.0, 1))
        self.assertFalse(is_valid_response(-1.0, 1))

        # RT = 0
        self.assertTrue(is_omission(0.0, 1))
        self.assertFalse(is_valid_response(0.0, 1))

        # RT = 1
        self.assertFalse(is_omission(1.0, 1))
        self.assertTrue(is_valid_response(1.0, 1))

        # RT = 4999
        self.assertFalse(is_omission(4999.0, 1))
        self.assertTrue(is_valid_response(4999.0, 1))

        # RT = 5000
        self.assertTrue(is_omission(5000.0, 1))
        self.assertFalse(is_valid_response(5000.0, 1))

        # RT = 5001
        self.assertTrue(is_omission(5001.0, 1))
        self.assertFalse(is_valid_response(5001.0, 1))

    def test_rt_boundary_sessions(self):
        boundary_rts = [-1.0, 0.0, 1.0, 4999.0, 5000.0, 5001.0]
        expected_valid = [False, False, True, True, False, False]

        for rt, is_val in zip(boundary_rts, expected_valid):
            responses = [{"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": rt}]
            raw_log = [{"trial": 1, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 0.0}]

            _, agg = extract_features_from_logs(raw_log, responses, self.subject_id)

            if is_val:
                self.assertEqual(agg.omission_rate, 0.0)
                self.assertEqual(agg.mean_reaction_time_ms, rt)
            else:
                self.assertEqual(agg.omission_rate, 1.0)
                self.assertEqual(agg.mean_reaction_time_ms, 0.0)

    def test_case_a_perfect_responses(self):
        responses = [
            {"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": 500.0},
            {"trial": 2, "load": 2, "distractor_type": "emotional", "corr_response": 0, "user_response": 0, "accuracy": 1, "reaction_time_ms": 600.0}
        ]
        raw_log = [
            {"trial": 1, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 0.0},
            {"trial": 2, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 1000.0}
        ]

        _, agg = extract_features_from_logs(raw_log, responses, self.subject_id)

        self.assertEqual(agg.accuracy_overall, 1.0)
        self.assertEqual(agg.hit_rate, 1.0)
        self.assertEqual(agg.false_alarm_rate, 0.0)
        self.assertEqual(agg.omission_rate, 0.0)

    def test_case_b_mixed_responses(self):
        responses = [
            {"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": 1000.0},
            {"trial": 2, "load": 2, "distractor_type": "none", "corr_response": 1, "user_response": 0, "accuracy": 0, "reaction_time_ms": 1200.0},
            {"trial": 3, "load": 1, "distractor_type": "emotional", "corr_response": 0, "user_response": 1, "accuracy": 0, "reaction_time_ms": 800.0},
            {"trial": 4, "load": 2, "distractor_type": "emotional", "corr_response": 0, "user_response": 0, "accuracy": 1, "reaction_time_ms": 900.0}
        ]
        raw_log = [
            {"trial": 1, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 0.0},
            {"trial": 2, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 1000.0},
            {"trial": 3, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 2000.0},
            {"trial": 4, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 3000.0}
        ]

        _, agg = extract_features_from_logs(raw_log, responses, self.subject_id)

        self.assertEqual(agg.accuracy_overall, 0.5)
        self.assertEqual(agg.hit_rate, 0.5)
        self.assertEqual(agg.false_alarm_rate, 0.5)
        self.assertEqual(agg.omission_rate, 0.0)
        self.assertAlmostEqual(agg.mean_reaction_time_ms, 975.0)
        self.assertAlmostEqual(agg.median_reaction_time_ms, 950.0)

    def test_missing_subgroups(self):
        responses = [
            {"trial": 1, "load": 2, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": 500.0}
        ]
        raw_log = [{"trial": 1, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 0.0}]

        _, agg = extract_features_from_logs(raw_log, responses, self.subject_id)

        self.assertIsNone(agg.accuracy_by_load_diff)
        self.assertIsNone(agg.accuracy_by_distractor_diff)

    def test_no_targets_or_lures(self):
        responses = [
            {"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": 500.0}
        ]
        raw_log = [{"trial": 1, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 0.0}]
        _, agg = extract_features_from_logs(raw_log, responses, self.subject_id)

        self.assertEqual(agg.hit_rate, 1.0)
        self.assertIsNone(agg.false_alarm_rate)

    def test_all_omitted_trials(self):
        responses = [
            {"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": -1, "accuracy": 0, "reaction_time_ms": 0.0}
        ]
        raw_log = [{"trial": 1, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 0.0}]
        _, agg = extract_features_from_logs(raw_log, responses, self.subject_id)

        self.assertEqual(agg.omission_rate, 1.0)
        self.assertEqual(agg.mean_reaction_time_ms, 0.0)
        self.assertEqual(agg.median_reaction_time_ms, 0.0)
        self.assertEqual(agg.rt_variability, 0.0)
        self.assertEqual(agg.rt_coefficient_of_variation, 0.0)

    def test_negative_zero_formatting(self):
        values = [-0.0001, -0.0, -0.00000003]
        for val in values:
            self.assertEqual(safe_pct(val), "0.0%")
            self.assertEqual(safe_ms(val), "0.0 ms")
            self.assertEqual(safe_pixels(val), "0.00 pixels")
            self.assertEqual(safe_val(val, "{:.2f}"), "0.00")

    def test_pupil_filtering(self):
        responses = [
            {"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": 500.0}
        ]
        raw_log = [
            {"trial": 1, "trial_phase": "fixation", "left_iris_radius": 10.0, "right_iris_radius": 10.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 0.0},
            {"trial": 1, "trial_phase": "fixation", "left_iris_radius": 10.0, "right_iris_radius": 10.0, "blink_state": 1, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 50.0},
            {"trial": 1, "trial_phase": "fixation", "left_iris_radius": float('nan'), "right_iris_radius": 10.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 100.0},
            {"trial": 1, "trial_phase": "fixation", "left_iris_radius": 0.0, "right_iris_radius": 10.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 150.0},
            {"trial": 1, "trial_phase": "fixation", "left_iris_radius": -5.0, "right_iris_radius": 10.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 200.0}
        ]

        trial_feats, agg = extract_features_from_logs(raw_log, responses, self.subject_id)
        self.assertIsNone(trial_feats[0].pupil_proxy_mean)

    def test_fixation_filtering_and_scaling(self):
        responses = [
            {"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": 500.0}
        ]
        raw_log = [
            {"trial": 1, "trial_phase": "fixation_1", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 100.0, "gaze_y": 100.0, "timestamp": 0.0},
            {"trial": 1, "trial_phase": "fixation_1", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 102.0, "gaze_y": 100.0, "timestamp": 50.0},
            {"trial": 1, "trial_phase": "array_encoding", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 500.0, "gaze_y": 500.0, "timestamp": 100.0},
            {"trial": 1, "trial_phase": "fixation_2", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 1, "gaze_x": 100.0, "gaze_y": 100.0, "timestamp": 150.0},
            {"trial": 1, "trial_phase": "fixation_2", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": float('nan'), "gaze_y": 100.0, "timestamp": 200.0}
        ]

        # Test default viewport dimensions (1280x720)
        # Gaze X coordinates: 100.0, 102.0. var_x = 1.0, var_y = 0.0. RMS = 1.0.
        # Instability = 1.0 / 12.0
        trial_feats, _ = extract_features_from_logs(raw_log, responses, self.subject_id, viewport_width=1280.0, viewport_height=720.0)
        self.assertAlmostEqual(trial_feats[0].fixation_stability, 1.0 / 12.0)

        # Test different viewport dimensions (2560x1440)
        # scale_x = 0.5. scaled X coordinates: 50.0, 51.0. var_x = 0.25. RMS = 0.5.
        # Instability = 0.5 / 12.0 = 1.0 / 24.0
        trial_feats_scaled, _ = extract_features_from_logs(raw_log, responses, self.subject_id, viewport_width=2560.0, viewport_height=1440.0)
        self.assertAlmostEqual(trial_feats_scaled[0].fixation_stability, 1.0 / 24.0)

    def test_empty_slice_warnings(self):
        # Passes raw log and responses that are empty
        responses = []
        raw_log = []

        # Must not raise RuntimeWarning (which is treated as error under -W error)
        trial_feats, agg = extract_features_from_logs(raw_log, responses, self.subject_id)

        # Verify unavailable metrics return None (missing values)
        self.assertIsNone(agg.accuracy_by_load_diff)
        self.assertIsNone(agg.accuracy_by_distractor_diff)
        self.assertIsNone(agg.hit_rate)
        self.assertIsNone(agg.false_alarm_rate)
        self.assertIsNone(agg.mean_fixation_stability)
        self.assertIsNone(agg.mean_pupil_proxy)

        # Verify RT metrics return 0.0 (or appropriate type-matching default, not NaN)
        self.assertEqual(agg.mean_reaction_time_ms, 0.0)
        self.assertEqual(agg.median_reaction_time_ms, 0.0)
        self.assertEqual(agg.rt_variability, 0.0)
        self.assertEqual(agg.rt_coefficient_of_variation, 0.0)
        self.assertEqual(agg.accuracy_overall, 0.0)

    def test_model_imputation_handles_missing_values(self):
        # Check if the models file exists
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pkl_path = os.path.join(base_dir, "ml", "models_v1.0.pkl")
        if not os.path.exists(pkl_path):
            self.skipTest("models_v1.0.pkl not found. Skipping model imputation test.")

        import pickle
        with open(pkl_path, 'rb') as f:
            package = pickle.load(f)

        # Create a feature dictionary with missing values (None)
        feature_order = package['feature_order']
        input_data = {col: [None] for col in feature_order}

        # Pass to the pipeline's imputer and scaler
        imputer = package['imputer']
        scaler = package['scaler']

        import pandas as pd
        df_input = pd.DataFrame(input_data)

        # Impute
        imputed = imputer.transform(df_input.values)
        self.assertFalse(np.isnan(imputed).any(), "Imputer failed to replace None/NaN values!")

        # Scale
        scaled = scaler.transform(imputed)
        self.assertEqual(scaled.shape, (1, len(feature_order)))

    def test_production_call_signature(self):
        # Replicates the call in pages/Sternberg_Task.py exactly
        raw_log = [{"trial": 1, "trial_phase": "fixation", "left_iris_radius": 5.0, "right_iris_radius": 5.0, "blink_state": 0, "gaze_x": 640.0, "gaze_y": 360.0, "timestamp": 0.0}]
        responses = [{"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": 500.0}]
        subject_id = "smoke_test_subject"
        viewport_width = 1920.0
        viewport_height = 1080.0

        # This call must match the production call in pages/Sternberg_Task.py exactly
        trial_features_list, agg_features = extract_features_from_logs(
            raw_log=raw_log,
            responses=responses,
            subject_id=subject_id,
            viewport_width=viewport_width,
            viewport_height=viewport_height
        )
        self.assertIsNotNone(agg_features)

if __name__ == '__main__':
    unittest.main()
