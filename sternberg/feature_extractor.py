import os
import json
import datetime
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from dataset.schema import TrialFeatures, SubjectAggregateFeatures

def extract_features_from_logs(raw_log: List[Dict[str, Any]], responses: List[Dict[str, Any]], subject_id: str) -> Tuple[List[TrialFeatures], SubjectAggregateFeatures]:
    """
    Parses the raw frame logs and behavioral responses from a live Sternberg task session
    and extracts trial-by-trial features and subject aggregates.
    """
    df_raw = pd.DataFrame(raw_log)
    df_resp = pd.DataFrame(responses)
    
    trial_features_list = []
    num_trials = len(df_resp)
    
    for i in range(num_trials):
        resp_row = df_resp.iloc[i]
        trial_id = int(resp_row['trial'])
        load = int(resp_row['load'])
        dist_type = str(resp_row['distractor_type']).strip().lower()
        perf = int(resp_row['accuracy'])
        rt = float(resp_row['reaction_time_ms'])
        
        # Filter raw frames for this trial
        trial_frames = df_raw[df_raw['trial'] == trial_id]
        
        fixation_stability = 0.0
        gaze_dispersion = 0.0
        pupil_mean = 0.0
        pupil_slope = 0.0
        
        if len(trial_frames) > 0:
            # 1. Pupil Size Proxy: average of left and right iris radius (ignoring NaNs and blinks)
            left_r = trial_frames['left_iris_radius'].values
            right_r = trial_frames['right_iris_radius'].values
            
            # Average radius, ignoring frames with blinks
            blink_state = trial_frames['blink_state'].values
            avg_pupil = []
            for j in range(len(trial_frames)):
                if blink_state[j] == 0:
                    vals = []
                    if not np.isnan(left_r[j]) and left_r[j] > 0:
                        vals.append(left_r[j])
                    if not np.isnan(right_r[j]) and right_r[j] > 0:
                        vals.append(right_r[j])
                    if vals:
                        avg_pupil.append(np.mean(vals))
                    else:
                        avg_pupil.append(np.nan)
                else:
                    avg_pupil.append(np.nan)
                    
            avg_pupil = np.array(avg_pupil)
            valid_pupil_mask = ~np.isnan(avg_pupil)
            
            if np.any(valid_pupil_mask):
                pupil_mean = float(np.mean(avg_pupil[valid_pupil_mask]))
                
                # Fit linear regression for slope
                t_vec = trial_frames['timestamp'].values
                t_rel = (t_vec - t_vec[0]) / 1000.0 # in seconds
                t_valid = t_rel[valid_pupil_mask]
                p_valid = avg_pupil[valid_pupil_mask]
                
                if len(t_valid) > 1:
                    try:
                        slope, _ = np.polyfit(t_valid, p_valid, 1)
                        pupil_slope = float(slope)
                    except:
                        pupil_slope = 0.0
                        
            # 2. Fixation Stability (during fixation phases)
            fix_frames = trial_frames[trial_frames['trial_phase'].str.startswith('fixation', na=False)]
            if len(fix_frames) > 0:
                # Exclude blinks/NaNs
                valid_gaze = fix_frames[(fix_frames['blink_state'] == 0) & 
                                        (~fix_frames['gaze_x'].isna()) & 
                                        (~fix_frames['gaze_y'].isna())]
                if len(valid_gaze) > 1:
                    var_x = np.var(valid_gaze['gaze_x'].values)
                    var_y = np.var(valid_gaze['gaze_y'].values)
                    fixation_stability = float(np.sqrt(var_x + var_y))
                    
            # 3. Gaze Dispersion (during array presentation phases)
            arr_frames = trial_frames[trial_frames['trial_phase'].str.startswith('array', na=False)]
            if len(arr_frames) > 0:
                # Exclude blinks/NaNs
                valid_gaze = arr_frames[(arr_frames['blink_state'] == 0) & 
                                        (~arr_frames['gaze_x'].isna()) & 
                                        (~arr_frames['gaze_y'].isna())]
                
                print("="*60)
                print(f"Trial: {trial_id}")
                print("Frames in trial:", len(trial_frames))
                print("Unique phase names:", trial_frames['trial_phase'].unique())
                print("Array frames:", len(arr_frames))
                print("Valid array frames:", len(valid_gaze))
                if len(valid_gaze) > 0:
                    print(valid_gaze[['gaze_x','gaze_y']].head())
                    print(valid_gaze[['gaze_x','gaze_y']].describe())
                
                if len(valid_gaze) > 1:
                    var_x = np.var(valid_gaze['gaze_x'].values)
                    var_y = np.var(valid_gaze['gaze_y'].values)
                    print("Variance X:", var_x)
                    print("Variance Y:", var_y)
                    print("Dispersion:", np.sqrt(var_x + var_y))
                    gaze_dispersion = float(np.sqrt(var_x + var_y))
                    
        trial_features_list.append(TrialFeatures(
            subject_id=subject_id,
            group=None,
            load=load,
            distractor_type=dist_type,
            trial_accuracy=perf,
            reaction_time_ms=rt,
            fixation_stability=fixation_stability / 12.0,
            pupil_proxy_mean=pupil_mean,
            pupil_proxy_trial_slope=pupil_slope,
            gaze_dispersion_during_array=gaze_dispersion / 12.0
        ))
        
    # Z-score the trial pupil values within the session to match the clinical dataset's z-scored pupil scale
    raw_pupils = [t.pupil_proxy_mean for t in trial_features_list if t.pupil_proxy_mean > 0]
    if len(raw_pupils) > 1:
        p_mean = np.mean(raw_pupils)
        p_std = np.std(raw_pupils)
        if p_std > 0:
            for t in trial_features_list:
                if t.pupil_proxy_mean > 0:
                    t.pupil_proxy_mean = float((t.pupil_proxy_mean - p_mean) / p_std)
                else:
                    t.pupil_proxy_mean = 0.0
        else:
            for t in trial_features_list:
                t.pupil_proxy_mean = 0.0
    else:
        for t in trial_features_list:
            t.pupil_proxy_mean = 0.0
            
    # Aggregate subject features
    valid_rts = [t.reaction_time_ms for t in trial_features_list if t.reaction_time_ms > 0]
    mean_rt = float(np.mean(valid_rts)) if valid_rts else 0.0
    median_rt = float(np.median(valid_rts)) if valid_rts else 0.0
    rt_sd = float(np.std(valid_rts)) if valid_rts else 0.0
    rt_cv = (rt_sd / mean_rt) if mean_rt > 0 else 0.0
    
    accuracies = [t.trial_accuracy for t in trial_features_list]
    acc_overall = float(np.mean(accuracies)) if accuracies else 0.0
    
    # Accuracy by load diff
    acc_load1 = np.mean([t.trial_accuracy for t in trial_features_list if t.load == 1])
    acc_load2 = np.mean([t.trial_accuracy for t in trial_features_list if t.load == 2])
    acc_load1 = acc_load1 if not np.isnan(acc_load1) else 0.0
    acc_load2 = acc_load2 if not np.isnan(acc_load2) else 0.0
    acc_by_load_diff = float(acc_load1 - acc_load2)
    
    # Accuracy by distractor diff
    acc_dist_none = np.mean([t.trial_accuracy for t in trial_features_list if t.distractor_type == 'none'])
    acc_dist_emot = np.mean([t.trial_accuracy for t in trial_features_list if t.distractor_type == 'emotional'])
    acc_dist_none = acc_dist_none if not np.isnan(acc_dist_none) else 0.0
    acc_dist_emot = acc_dist_emot if not np.isnan(acc_dist_emot) else 0.0
    acc_by_dist_diff = float(acc_dist_none - acc_dist_emot)
    
    mean_fix_stab = float(np.mean([t.fixation_stability for t in trial_features_list if t.fixation_stability > 0]))
    mean_pupil = float(np.mean([t.pupil_proxy_mean for t in trial_features_list])) if trial_features_list else 0.0
    
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
    hit_rate = float(hits / targets_present) if targets_present > 0 else 0.0
    false_alarm_rate = float(false_alarms / lures_present) if lures_present > 0 else 0.0
    
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
        mean_fixation_stability=mean_fix_stab if not np.isnan(mean_fix_stab) else 0.0,
        mean_pupil_proxy=mean_pupil if not np.isnan(mean_pupil) else 0.0,
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
