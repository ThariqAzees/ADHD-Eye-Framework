import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from dataset.schema import TrialFeatures, SubjectAggregateFeatures

def extract_subject_features(subject_id: str, group: str, task_epoch: Dict[str, Any], task_data: Dict[str, Any]) -> Tuple[List[TrialFeatures], SubjectAggregateFeatures]:
    """
    Extracts trial-by-trial features and aggregates them for a single subject from the Rojas-Líbano dataset structures.
    """
    # task_epoch and task_data are parsed dictionaries from the MATLAB tables.
    # Columns in task_epoch: Trial, Load, Distractor, CorrResponse, Perform, RTime, Pupil
    trials = task_epoch.get('Trial', [])
    loads = task_epoch.get('Load', [])
    distractors = task_epoch.get('Distractor', [])
    performances = task_epoch.get('Perform', [])
    rtimes = task_epoch.get('RTime', [])
    pupil_data_list = task_epoch.get('Pupil', [])
    
    # task_data raw streams: Time, Diameter, Position, Events
    raw_time = np.array(task_data.get('Time', []))
    raw_pos = np.array(task_data.get('Position', []))
    
    # Handle raw position shape
    # Raw Position should be (M, 2)
    if raw_pos.ndim == 2:
        if raw_pos.shape[1] != 2 and raw_pos.shape[0] == 2:
            raw_pos = raw_pos.T
    elif raw_pos.ndim == 1:
        # If it's flattened, try to reshape
        raw_pos = raw_pos.reshape(-1, 2)
    else:
        raw_pos = np.zeros((len(raw_time), 2))
        
    num_trials = len(trials)
    trial_features_list = []
    
    for i in range(num_trials):
        trial_id = int(trials[i])
        load = int(loads[i])
        
        # Distractor can be a string or array/category
        dist = distractors[i]
        if isinstance(dist, list):
            dist = dist[0] if len(dist) > 0 else 'none'
        dist_type = str(dist).strip().lower()
        if dist_type == 'empty-grid' or dist_type == 'empty_grid':
            dist_type = 'none'
        elif dist_type not in ['neutral', 'task_related', 'task-related', 'emotional', 'none']:
            dist_type = 'none'
        
        perf = int(performances[i])
        rt = float(rtimes[i])
        
        # Get pupil trace for this trial
        # Pupil contains [timestamps, z-scored_pupil] or a structure
        pupil_entry = pupil_data_list[i]
        
        trial_start = 0.0
        trial_end = 0.0
        pupil_mean = 0.0
        pupil_slope = 0.0
        
        # Parse pupil_entry
        # Usually it is a 2D array or a list/tuple of two arrays
        if isinstance(pupil_entry, (list, tuple)) and len(pupil_entry) >= 2:
            t_vec = np.array(pupil_entry[0]).flatten()
            p_vec = np.array(pupil_entry[1]).flatten()
        elif isinstance(pupil_entry, np.ndarray):
            if pupil_entry.ndim == 2:
                if pupil_entry.shape[0] == 2:
                    t_vec = pupil_entry[0, :]
                    p_vec = pupil_entry[1, :]
                else:
                    t_vec = pupil_entry[:, 0]
                    p_vec = pupil_entry[:, 1]
            else:
                t_vec = np.arange(len(pupil_entry))
                p_vec = pupil_entry
        else:
            t_vec = np.array([])
            p_vec = np.array([])
            
        if len(t_vec) > 0:
            trial_start = float(t_vec[0])
            trial_end = float(t_vec[-1])
            
            # Filter valid pupil values
            valid_p_mask = ~np.isnan(p_vec) & ~np.isinf(p_vec)
            if np.any(valid_p_mask):
                pupil_mean = float(np.mean(p_vec[valid_p_mask]))
                # Fit linear regression for slope
                t_rel = t_vec[valid_p_mask] - trial_start
                p_valid = p_vec[valid_p_mask]
                if len(t_rel) > 1:
                    try:
                        slope, _ = np.polyfit(t_rel, p_valid, 1)
                        pupil_slope = float(slope)
                    except:
                        pupil_slope = 0.0
                        
        # Extract raw gaze features within the trial interval
        fixation_stability = 0.0
        gaze_dispersion = 0.0
        
        if trial_start > 0 and trial_end > trial_start:
            # Filter raw timestamps in this trial range
            trial_mask = (raw_time >= trial_start) & (raw_time <= trial_end)
            t_trial_raw = raw_time[trial_mask]
            pos_trial_raw = raw_pos[trial_mask]
            
            if len(t_trial_raw) > 0:
                t_rel_raw = t_trial_raw - trial_start
                
                # Fixation delays: [0, 500]ms, [1250, 1750]ms, [2500, 3000]ms
                fix_mask = ((t_rel_raw >= 0) & (t_rel_raw <= 500)) | \
                           ((t_rel_raw >= 1250) & (t_rel_raw <= 1750)) | \
                           ((t_rel_raw >= 2500) & (t_rel_raw <= 3000))
                           
                # Dot array presentations: [500, 1250]ms, [1750, 2500]ms, [3000, 3750]ms
                arr_mask = ((t_rel_raw >= 500) & (t_rel_raw <= 1250)) | \
                           ((t_rel_raw >= 1750) & (t_rel_raw <= 2500)) | \
                           ((t_rel_raw >= 3000) & (t_rel_raw <= 3750))
                           
                fix_gaze = pos_trial_raw[fix_mask]
                arr_gaze = pos_trial_raw[arr_mask]
                
                # Calculate stability (root-mean-square distance from mean)
                if len(fix_gaze) > 1:
                    # Filter out invalid coordinates (e.g. blinks represented as NaN or 0)
                    valid_fix = ~np.isnan(fix_gaze[:, 0]) & ~np.isnan(fix_gaze[:, 1]) & (fix_gaze[:, 0] > 0) & (fix_gaze[:, 1] > 0)
                    fix_gaze_v = fix_gaze[valid_fix]
                    if len(fix_gaze_v) > 1:
                        var_x = np.var(fix_gaze_v[:, 0])
                        var_y = np.var(fix_gaze_v[:, 1])
                        fixation_stability = float(np.sqrt(var_x + var_y))
                        
                # Calculate dispersion during dot array
                if len(arr_gaze) > 1:
                    valid_arr = ~np.isnan(arr_gaze[:, 0]) & ~np.isnan(arr_gaze[:, 1]) & (arr_gaze[:, 0] > 0) & (arr_gaze[:, 1] > 0)
                    arr_gaze_v = arr_gaze[valid_arr]
                    if len(arr_gaze_v) > 1:
                        var_x = np.var(arr_gaze_v[:, 0])
                        var_y = np.var(arr_gaze_v[:, 1])
                        gaze_dispersion = float(np.sqrt(var_x + var_y))
                        
        trial_features_list.append(TrialFeatures(
            subject_id=subject_id,
            group=group,
            load=load,
            distractor_type=dist_type,
            trial_accuracy=perf,
            reaction_time_ms=rt,
            fixation_stability=fixation_stability,
            pupil_proxy_mean=pupil_mean,
            pupil_proxy_trial_slope=pupil_slope,
            gaze_dispersion_during_array=gaze_dispersion
        ))
        
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
    # Handle NaNs
    acc_load1 = acc_load1 if not np.isnan(acc_load1) else 0.0
    acc_load2 = acc_load2 if not np.isnan(acc_load2) else 0.0
    acc_by_load_diff = float(acc_load1 - acc_load2)
    
    # Accuracy by distractor diff: none vs emotional
    acc_dist_none = np.mean([t.trial_accuracy for t in trial_features_list if t.distractor_type == 'none'])
    acc_dist_emot = np.mean([t.trial_accuracy for t in trial_features_list if t.distractor_type == 'emotional'])
    acc_dist_none = acc_dist_none if not np.isnan(acc_dist_none) else 0.0
    acc_dist_emot = acc_dist_emot if not np.isnan(acc_dist_emot) else 0.0
    acc_by_dist_diff = float(acc_dist_none - acc_dist_emot)
    
    mean_fix_stab = float(np.mean([t.fixation_stability for t in trial_features_list if t.fixation_stability > 0]))
    mean_pupil = float(np.mean([t.pupil_proxy_mean for t in trial_features_list]))
    
    # Cognitive task metrics: omission rate (rt == 0 or no response), hit rate, false alarm rate
    # Note: In Sternberg task, targets are array items. The probe matches array dot location.
    # Let's see: CorrResponse: Expected correct response (usually yes = 1, no = 0).
    # Hit: response is Yes (1) and CorrResponse is Yes (1).
    # False Alarm: response is Yes (1) and CorrResponse is No (0).
    # Since we only have trial_accuracy (Performance) and CorrResponse in the dataset:
    # Let's map participant's response:
    # Response = CorrResponse if trial_accuracy == 1 else (1 - CorrResponse)
    responses = []
    corr_responses = task_epoch.get('CorrResponse', [])
    for i in range(num_trials):
        corr_resp = int(corr_responses[i])
        perf = int(performances[i])
        resp = corr_resp if perf == 1 else (1 - corr_resp)
        responses.append(resp)
        
    hits = 0
    targets_present = 0
    false_alarms = 0
    lures_present = 0
    omissions = 0
    
    for i in range(num_trials):
        rt = rtimes[i]
        # Omission: reaction time is 0 (no response) or exceeds trial limit
        if rt <= 0 or rt >= 1500:
            omissions += 1
            continue
            
        corr_resp = int(corr_responses[i])
        resp = responses[i]
        
        if corr_resp == 1:  # Target was in memory (correct response is Yes)
            targets_present += 1
            if resp == 1:
                hits += 1
        else:  # Target was not in memory (correct response is No)
            lures_present += 1
            if resp == 1:
                false_alarms += 1
                
    omission_rate = float(omissions / num_trials) if num_trials > 0 else 0.0
    hit_rate = float(hits / targets_present) if targets_present > 0 else 0.0
    false_alarm_rate = float(false_alarms / lures_present) if lures_present > 0 else 0.0
    
    agg_features = SubjectAggregateFeatures(
        subject_id=subject_id,
        group=group,
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
