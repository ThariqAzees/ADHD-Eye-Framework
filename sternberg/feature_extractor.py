import os
import json
import datetime
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from dataset.schema import TrialFeatures, SubjectAggregateFeatures

def is_valid_response(rt: float, user_resp: int) -> bool:
    # RT must be strictly between 0 and 5000, and user_response must be valid (0 or 1)
    return rt > 0.0 and rt < 5000.0 and user_resp in (0, 1)

def is_omission(rt: float, user_resp: int) -> bool:
    return user_resp == -1 or rt <= 0.0 or rt >= 5000.0

def extract_features_from_logs(
    raw_log: List[Dict[str, Any]],
    responses: List[Dict[str, Any]],
    subject_id: str,
    viewport_width: float = 1280.0,
    viewport_height: float = 720.0
) -> Tuple[List[TrialFeatures], SubjectAggregateFeatures]:
    """
    Parses the raw frame logs and behavioral responses from a live Sternberg task session
    and extracts trial-by-trial features and subject aggregates.
    """
    df_raw = pd.DataFrame(raw_log)
    df_resp = pd.DataFrame(responses)

    trial_features_list = []
    num_trials = len(df_resp)

    # 1. Coordinate scaling factors to map layout viewport to standard 1280x720 canvas
    scale_x = 1280.0 / viewport_width
    scale_y = 720.0 / viewport_height

    # 2. Extract frame-level pupil sizes for session-wide frame-level z-scoring normalization
    session_frame_pupils = []
    for j in range(len(df_raw)):
        if df_raw.iloc[j]['blink_state'] == 0:
            left_r = df_raw.iloc[j]['left_iris_radius']
            right_r = df_raw.iloc[j]['right_iris_radius']
            vals = []
            if not np.isnan(left_r) and left_r > 0:
                vals.append(left_r)
            if not np.isnan(right_r) and right_r > 0:
                vals.append(right_r)
            if vals:
                session_frame_pupils.append(np.mean(vals))

    p_mean = 0.0
    p_std = 1.0
    has_valid_pupil_session = False
    if len(session_frame_pupils) > 1:
        p_mean = float(np.mean(session_frame_pupils))
        p_std = float(np.std(session_frame_pupils))
        if p_std > 0:
            has_valid_pupil_session = True

    # 3. Process trial-by-trial logs
    for i in range(num_trials):
        resp_row = df_resp.iloc[i]
        trial_id = int(resp_row['trial'])
        load = int(resp_row['load'])
        dist_type = str(resp_row['distractor_type']).strip().lower()
        perf = int(resp_row['accuracy'])
        rt = float(resp_row['reaction_time_ms'])

        # Filter raw frames for this trial
        trial_frames = df_raw[df_raw['trial'] == trial_id]

        fixation_stability = None
        gaze_dispersion = None
        normalized_fixation_instability = None
        normalized_gaze_dispersion = None
        pupil_mean = None
        pupil_slope = None

        if len(trial_frames) > 0:
            # 3.1 Pupil Proxy z-scored at frame level
            if has_valid_pupil_session:
                left_r = trial_frames['left_iris_radius'].values
                right_r = trial_frames['right_iris_radius'].values
                blink_state = trial_frames['blink_state'].values

                trial_z_pupils = []
                for j in range(len(trial_frames)):
                    if blink_state[j] == 0:
                        vals = []
                        if not np.isnan(left_r[j]) and left_r[j] > 0:
                            vals.append(left_r[j])
                        if not np.isnan(right_r[j]) and right_r[j] > 0:
                            vals.append(right_r[j])
                        if vals:
                            raw_p = np.mean(vals)
                            z_p = (raw_p - p_mean) / p_std
                            trial_z_pupils.append(z_p)

                if trial_z_pupils:
                    pupil_mean = float(np.mean(trial_z_pupils))

                    t_vec = trial_frames['timestamp'].values
                    t_rel = (t_vec - t_vec[0]) / 1000.0
                    t_valid = []
                    for idx in range(len(trial_frames)):
                        if blink_state[idx] == 0:
                            l_val = left_r[idx]
                            r_val = right_r[idx]
                            if (not np.isnan(l_val) and l_val > 0) or (not np.isnan(r_val) and r_val > 0):
                                t_valid.append(t_rel[idx])

                    if len(t_valid) == len(trial_z_pupils) and len(t_valid) > 1:
                        try:
                            slope, _ = np.polyfit(t_valid, trial_z_pupils, 1)
                            pupil_slope = float(slope)
                        except:
                            pupil_slope = None

            # 3.2 Fixation Stability (during fixation phases)
            fix_frames = trial_frames[trial_frames['trial_phase'].str.startswith('fixation', na=False)]
            if len(fix_frames) > 0:
                valid_gaze = fix_frames[(fix_frames['blink_state'] == 0) &
                                        (~fix_frames['gaze_x'].isna()) &
                                        (~fix_frames['gaze_y'].isna())]
                if len(valid_gaze) > 1:
                    gaze_x_scaled = valid_gaze['gaze_x'].values * scale_x
                    gaze_y_scaled = valid_gaze['gaze_y'].values * scale_y
                    var_x = np.var(gaze_x_scaled)
                    var_y = np.var(gaze_y_scaled)
                    fixation_stability = float(np.sqrt(var_x + var_y))

                    # Normalized coordinate fixation instability
                    gaze_x_norm = valid_gaze['gaze_x'].values / viewport_width
                    gaze_y_norm = valid_gaze['gaze_y'].values / viewport_height
                    normalized_fixation_instability = float(np.sqrt(np.var(gaze_x_norm) + np.var(gaze_y_norm)))

            # 3.3 Gaze Dispersion (during array encoding presentation)
            arr_frames = trial_frames[trial_frames['trial_phase'].str.startswith('array', na=False)]
            if len(arr_frames) > 0:
                valid_gaze_arr = arr_frames[(arr_frames['blink_state'] == 0) &
                                            (~arr_frames['gaze_x'].isna()) &
                                            (~arr_frames['gaze_y'].isna())]
                if len(valid_gaze_arr) > 1:
                    gaze_x_scaled_arr = valid_gaze_arr['gaze_x'].values * scale_x
                    gaze_y_scaled_arr = valid_gaze_arr['gaze_y'].values * scale_y
                    var_x_arr = np.var(gaze_x_scaled_arr)
                    var_y_arr = np.var(gaze_y_scaled_arr)
                    gaze_dispersion = float(np.sqrt(var_x_arr + var_y_arr))

                    # Normalized coordinate gaze dispersion
                    gaze_x_norm_arr = valid_gaze_arr['gaze_x'].values / viewport_width
                    gaze_y_norm_arr = valid_gaze_arr['gaze_y'].values / viewport_height
                    normalized_gaze_dispersion = float(np.sqrt(np.var(gaze_x_norm_arr) + np.var(gaze_y_norm_arr)))

        trial_features_list.append(TrialFeatures(
            subject_id=subject_id,
            group=None,
            load=load,
            distractor_type=dist_type,
            trial_accuracy=perf,
            reaction_time_ms=rt,
            fixation_stability=fixation_stability / 12.0 if fixation_stability is not None else None,
            pupil_proxy_mean=pupil_mean,
            pupil_proxy_trial_slope=pupil_slope,
            gaze_dispersion_during_array=gaze_dispersion / 12.0 if gaze_dispersion is not None else None,
            normalized_fixation_instability=normalized_fixation_instability,
            normalized_gaze_dispersion=normalized_gaze_dispersion
        ))

    # 4. Aggregate subject features
    # Centralized valid reaction times selection (strictly valid responses: 0 < RT < 5000)
    valid_rts = []
    for t, r in zip(trial_features_list, responses):
        rt_val = float(r['reaction_time_ms'])
        resp_val = int(r['user_response'])
        if is_valid_response(rt_val, resp_val):
            valid_rts.append(rt_val)

    mean_rt = float(np.mean(valid_rts)) if valid_rts else 0.0
    median_rt = float(np.median(valid_rts)) if valid_rts else 0.0
    rt_sd = float(np.std(valid_rts)) if valid_rts else 0.0
    rt_cv = (rt_sd / mean_rt) if mean_rt > 0 else 0.0

    accuracies = [t.trial_accuracy for t in trial_features_list]
    acc_overall = float(np.mean(accuracies)) if accuracies else 0.0

    # Accuracy by load diff
    load1_accs = [t.trial_accuracy for t in trial_features_list if t.load == 1]
    load2_accs = [t.trial_accuracy for t in trial_features_list if t.load == 2]
    if len(load1_accs) > 0 and len(load2_accs) > 0:
        acc_load1 = float(np.mean(load1_accs))
        acc_load2 = float(np.mean(load2_accs))
        acc_by_load_diff = float(acc_load1 - acc_load2)
    else:
        acc_by_load_diff = None

    # Accuracy by distractor diff
    dist_none_accs = [t.trial_accuracy for t in trial_features_list if t.distractor_type == 'none']
    dist_emot_accs = [t.trial_accuracy for t in trial_features_list if t.distractor_type == 'emotional']
    if len(dist_none_accs) > 0 and len(dist_emot_accs) > 0:
        acc_dist_none = float(np.mean(dist_none_accs))
        acc_dist_emot = float(np.mean(dist_emot_accs))
        acc_by_dist_diff = float(acc_dist_none - acc_dist_emot)
    else:
        acc_by_dist_diff = None

    fix_stabs = [t.fixation_stability for t in trial_features_list if t.fixation_stability is not None and t.fixation_stability > 0]
    mean_fix_stab = float(np.mean(fix_stabs)) if fix_stabs else None

    fix_stabs_norm = [t.normalized_fixation_instability for t in trial_features_list if t.normalized_fixation_instability is not None]
    mean_fix_stab_norm = float(np.mean(fix_stabs_norm)) if fix_stabs_norm else None

    gaze_disps_norm = [t.normalized_gaze_dispersion for t in trial_features_list if t.normalized_gaze_dispersion is not None]
    mean_gaze_disp_norm = float(np.mean(gaze_disps_norm)) if gaze_disps_norm else None

    pupil_means = [t.pupil_proxy_mean for t in trial_features_list if t.pupil_proxy_mean is not None]
    mean_pupil = float(np.mean(pupil_means)) if pupil_means else None
    pupil_var = float(np.std(pupil_means)) if pupil_means else None

    # Cognitive task metrics: omission, hit, false alarm
    hits = 0
    targets_present = 0
    false_alarms = 0
    lures_present = 0
    omissions = 0

    for row in responses:
        rt = row['reaction_time_ms']
        # Omission: reaction time is 0 (no response)
        if rt <= 0 or rt >= 5000:
            omissions += 1
            continue

        corr_resp = int(row['corr_response'])
        resp = int(row['user_response'])

        if corr_resp == 1:
            targets_present += 1
            if resp == 1:
                hits += 1
        else:
            lures_present += 1
            if resp == 1:
                false_alarms += 1

    omission_rate = float(omissions / num_trials) if num_trials > 0 else 0.0
    hit_rate = float(hits / targets_present) if targets_present > 0 else None
    false_alarm_rate = float(false_alarms / lures_present) if lures_present > 0 else None

    agg_features = SubjectAggregateFeatures(
        subject_id=subject_id,
        group=None,
        mean_reaction_time_ms=mean_rt,
        median_reaction_time_ms=median_rt,
        rt_variability=rt_sd,
        rt_coefficient_of_variation=rt_cv,
        accuracy_overall=acc_overall,
        accuracy_by_load_diff=acc_by_load_diff,
        accuracy_by_distractor_diff=acc_by_dist_diff,
        mean_fixation_stability=mean_fix_stab,
        mean_pupil_proxy=mean_pupil,
        normalized_fixation_instability=mean_fix_stab_norm,
        normalized_gaze_dispersion=mean_gaze_disp_norm,
        pupil_variability=pupil_var,
        omission_rate=omission_rate,
        false_alarm_rate=false_alarm_rate,
        hit_rate=hit_rate
    )

    return trial_features_list, agg_features

def save_sternberg_session(raw_log: list, responses: list, agg_features: SubjectAggregateFeatures, calibration_metrics: dict, metadata_args: dict = None) -> tuple:
    """
    Saves raw logs, clean features, and session metadata to the appropriate paths.
    """
    from dataset.build_dataset import get_data_dirs
    raw_dir, _, exports_dir = get_data_dirs()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    subject_id = agg_features.subject_id

    # 1. Save Complete Raw Frame Logs
    df_raw = pd.DataFrame(raw_log)
    csv_raw_path = os.path.join(raw_dir, f"sternberg_session_{timestamp}.csv")
    df_raw.to_csv(csv_raw_path, index=False)

    # 2. Save Clean Session Features (only engineered features, no software versions inside columns)
    clean_cols = [
        'subject_id', 'group',
        'mean_reaction_time_ms', 'median_reaction_time_ms', 'rt_variability', 'rt_coefficient_of_variation',
        'accuracy_overall', 'accuracy_by_load_diff', 'accuracy_by_distractor_diff',
        'mean_fixation_stability', 'mean_pupil_proxy',
        'omission_rate', 'false_alarm_rate', 'hit_rate'
    ]
    feats_dict = {col: getattr(agg_features, col, None) for col in clean_cols}
    df_feats = pd.DataFrame([feats_dict])

    csv_feats_path = os.path.join(exports_dir, f"session_features_{timestamp}.csv")
    df_feats.to_csv(csv_feats_path, index=False)

    # 3. Save Session Metadata separately
    meta_path = os.path.join(exports_dir, f"session_metadata_{timestamp}.json")
    metadata = {
        "participant_id": subject_id,
        "date": datetime.datetime.now().isoformat(),
        "task_type": "sternberg_task",
        "device": metadata_args.get("device", "Unknown"),
        "browser": metadata_args.get("browser", "Unknown"),
        "camera_resolution": metadata_args.get("camera_resolution", "Unknown"),
        "fps": metadata_args.get("fps", 30),
        "calibration_metrics": calibration_metrics,
        "framework_version": agg_features.framework_version,
        "feature_extractor_version": agg_features.feature_extractor_version,
        "model_version": agg_features.model_version,
        "dataset_version": agg_features.dataset_version
    }

    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"Sternberg raw log saved to {csv_raw_path}")
    print(f"Sternberg clean features saved to {csv_feats_path}")
    print(f"Session metadata saved to {meta_path}")

    return csv_raw_path, csv_feats_path, meta_path
