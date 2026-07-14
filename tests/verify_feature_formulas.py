import os
import sys
import numpy as np

# Ensure repository root is in search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sternberg.feature_extractor import extract_features_from_logs

def run_verification():
    print("--- STARTING FORMULA VERIFICATION AGAINST DETERMINISTIC SYNTHETIC SESSION ---")

    responses = [
        {"trial": 1, "load": 1, "distractor_type": "none", "corr_response": 1, "user_response": 1, "accuracy": 1, "reaction_time_ms": 1000.0},
        {"trial": 2, "load": 2, "distractor_type": "none", "corr_response": 1, "user_response": 0, "accuracy": 0, "reaction_time_ms": 1200.0},
        {"trial": 3, "load": 1, "distractor_type": "emotional", "corr_response": 0, "user_response": 1, "accuracy": 0, "reaction_time_ms": 800.0},
        {"trial": 4, "load": 2, "distractor_type": "emotional", "corr_response": 0, "user_response": 0, "accuracy": 1, "reaction_time_ms": 900.0}
    ]

    raw_log = []
    pupil_values_trial = [
        [10.0, 12.0],  # Mean = 11.0
        [14.0, 16.0],  # Mean = 15.0
        [18.0, 20.0],  # Mean = 19.0 (stability = 0.0, excluded from fixation stability mean)
        [22.0, 24.0]   # Mean = 23.0
    ]

    for i in range(4):
        t_id = i + 1
        g_coords = [
            (100.0, 100.0) if i==0 else (200.0, 200.0) if i==1 else (300.0, 300.0) if i==2 else (400.0, 400.0),
            (102.0, 100.0) if i==0 else (200.0, 204.0) if i==1 else (300.0, 300.0) if i==2 else (406.0, 408.0)
        ]

        for f_idx in range(2):
            raw_log.append({
                "timestamp": f_idx * 50.0 + i * 1000.0,
                "trial": t_id,
                "trial_phase": f"fixation_{f_idx+1}",
                "gaze_x": g_coords[f_idx][0],
                "gaze_y": g_coords[f_idx][1],
                "left_iris_radius": pupil_values_trial[i][f_idx],
                "right_iris_radius": pupil_values_trial[i][f_idx],
                "blink_state": 0
            })

        raw_log.append({
            "timestamp": 100.0 + i * 1000.0,
            "trial": t_id,
            "trial_phase": "array_presentation",
            "gaze_x": 500.0,
            "gaze_y": 500.0,
            "left_iris_radius": 15.0,
            "right_iris_radius": 15.0,
            "blink_state": 1
        })

    trial_feats, agg = extract_features_from_logs(raw_log, responses, "verifier_id", viewport_width=1280.0, viewport_height=720.0)

    expected_acc_overall = 0.5
    expected_mean_rt = 975.0
    expected_median_rt = 950.0
    expected_rt_sd = float(np.std([1000.0, 1200.0, 800.0, 900.0]))
    expected_rt_cv = expected_rt_sd / expected_mean_rt

    expected_omission_rate = 0.0
    expected_hit_rate = 0.5
    expected_fa_rate = 0.5
    expected_load_diff = 0.0
    expected_dist_diff = 0.0

    # Expected fixation stability values scaled by 12.0
    expected_mean_fixation = float(np.mean([1.0/12.0, 2.0/12.0, 5.0/12.0]))

    metrics_list = [
        ("Accuracy Overall", expected_acc_overall, agg.accuracy_overall, 1e-4),
        ("Mean Reaction Time", expected_mean_rt, agg.mean_reaction_time_ms, 1e-4),
        ("Median Reaction Time", expected_median_rt, agg.median_reaction_time_ms, 1e-4),
        ("Reaction Time SD", expected_rt_sd, agg.rt_variability, 1e-4),
        ("Reaction Time CV", expected_rt_cv, agg.rt_coefficient_of_variation, 1e-4),
        ("Omission Rate", expected_omission_rate, agg.omission_rate, 1e-4),
        ("Hit Rate", expected_hit_rate, agg.hit_rate, 1e-4),
        ("False Alarm Rate", expected_fa_rate, agg.false_alarm_rate, 1e-4),
        ("Accuracy Load Difference", expected_load_diff, agg.accuracy_by_load_diff, 1e-4),
        ("Accuracy Distractor Difference", expected_dist_diff, agg.accuracy_by_distractor_diff, 1e-4),
        ("Mean Fixation Instability", expected_mean_fixation, agg.mean_fixation_stability, 1e-4),
    ]

    print("\n" + "="*80)
    print(f"{'METRIC NAME':<35} | {'EXPECTED':<12} | {'ACTUAL':<12} | {'STATUS'}")
    print("="*80)

    all_passed = True
    for name, exp, act, tol in metrics_list:
        if exp is None or act is None:
            passed = (exp is None and act is None)
        else:
            passed = abs(exp - act) < tol

        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"{name:<35} | {str(exp)[:12]:<12} | {str(act)[:12]:<12} | {status}")

    print("="*80)

    t1_p_mean = trial_feats[0].pupil_proxy_mean
    t1_p_expected = -1.3093073
    pupil_passed = abs(t1_p_mean - t1_p_expected) < 1e-4
    print(f"Trial 1 Z-Scored Pupil Mean   | Expected: {t1_p_expected:.4f} | Actual: {t1_p_mean:.4f} | {'PASS' if pupil_passed else 'FAIL'}")
    if not pupil_passed:
        all_passed = False

    if all_passed:
        print("\n[VERIFICATION RESULT] ALL DETERMINISTIC METRIC FORMULA CHECKS PASSED.")
    else:
        print("\n[VERIFICATION RESULT] SOME METRIC FORMULA CHECKS FAILED.")
        sys.exit(1)

if __name__ == '__main__':
    run_verification()
