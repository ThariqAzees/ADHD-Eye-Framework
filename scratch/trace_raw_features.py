import os
import h5py
import numpy as np
import pandas as pd
from scipy import stats

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mat_path = os.path.join(base_dir, "data", "raw", "Pupil_dataset.mat")
    csv_path = os.path.join(base_dir, "data", "processed", "dataset_features_REAL_v1.0.csv")
    
    df_real = pd.read_csv(csv_path)
    
    # Selected subjects
    adhd_subjects = ["subject_4", "subject_5", "subject_8"]
    control_subjects = ["subject_33", "subject_38", "subject_40"]
    all_trace_subjects = adhd_subjects + control_subjects
    
    # 1. PARSE RAW MAT VIA H5PY
    print("[TRACE] Parsing MATLAB file...")
    f = h5py.File(mat_path, 'r')
    pdata = f['Pupil_data']
    mcos = f['#subsystem#/MCOS']
    num_sessions = pdata['Subject'].shape[0]
    
    def decode_value(ref):
        if not isinstance(ref, h5py.Reference):
            if isinstance(ref, np.ndarray):
                return ref.flatten()[0] if ref.size > 0 else None
            return ref
        target = f[ref]
        if isinstance(target, h5py.Dataset):
            val = target[()]
            mclass = target.attrs.get('MATLAB_class')
            if mclass == b'char':
                if val.dtype == 'uint16':
                    return val.tobytes().decode('utf-16').strip()
                else:
                    return val.tobytes().decode('ascii', errors='ignore').strip()
            if target.dtype.kind in 'ui' and val.size > 0 and val.size < 100:
                try:
                    chars = [chr(int(c)) for c in val.flatten()]
                    if all(32 <= ord(c) < 127 for c in chars):
                        return "".join(chars).strip()
                except:
                    pass
            if val.size == 0:
                return None
            return val.flatten()[0]
        return target

    # Map raw session index for each selected subject
    subject_to_session = {}
    for i in range(num_sessions):
        subj_val = decode_value(pdata['Subject'][i, 0])
        group_val = decode_value(pdata['Group'][i, 0])
        
        # We only care about unmedicated ADHD and valid controls
        if group_val == 'on-ADHD':
            continue
            
        subj_id_str = f"subject_{int(subj_val)}"
        if subj_id_str in all_trace_subjects:
            subject_to_session[subj_id_str] = (i, group_val)
            
    print(f"[TRACE] Mapped subjects: {subject_to_session}")
    
    # Trace columns
    trace_rows = []
    
    for subj_id in all_trace_subjects:
        print(f"\n==================================================")
        print(f"TRACING SUBJECT: {subj_id}")
        print(f"==================================================")
        
        session_idx, raw_group = subject_to_session[subj_id]
        print(f"Raw Session Index in MAT: {session_idx}")
        print(f"Raw Group Label in MAT: {raw_group}")
        
        # Extract Task_epoch arrays
        te_idx = 541 + 7 * session_idx
        te_cell = f[mcos[0, te_idx]]
        
        trial_ref = te_cell[0, 0] if te_cell.ndim == 2 else te_cell[0]
        load_ref = te_cell[1, 0] if te_cell.ndim == 2 else te_cell[1]
        dist_ref = te_cell[2, 0] if te_cell.ndim == 2 else te_cell[2]
        corr_ref = te_cell[3, 0] if te_cell.ndim == 2 else te_cell[3]
        perf_ref = te_cell[4, 0] if te_cell.ndim == 2 else te_cell[4]
        rt_ref = te_cell[5, 0] if te_cell.ndim == 2 else te_cell[5]
        pup_ref = te_cell[6, 0] if te_cell.ndim == 2 else te_cell[6]
        
        trials = f[trial_ref][()].flatten()
        loads = f[load_ref][()].flatten()
        distractors = f[dist_ref][()].flatten()
        corr_responses = f[corr_ref][()].flatten()
        performances = f[perf_ref][()].flatten()
        rtimes = f[rt_ref][()].flatten()
        pupil_ds = f[pup_ref]
        
        print(f"Raw Trials Count: {len(trials)}")
        
        # Load continuous Gaze Positions for gaze features
        td_idx = 9 + 7 * session_idx
        td_cell = f[mcos[0, td_idx]]
        time_ref = td_cell[0, 0] if td_cell.ndim == 2 else td_cell[0]
        pos_ref = td_cell[2, 0] if td_cell.ndim == 2 else td_cell[2]
        raw_time = f[time_ref][()].flatten()
        raw_pos = f[pos_ref][()]
        if raw_pos.ndim == 2 and raw_pos.shape[1] != 2 and raw_pos.shape[0] == 2:
            raw_pos = raw_pos.T
            
        print(f"Raw time points: {len(raw_time)}")
        
        # 1. Recompute features
        # Overall Accuracy
        accuracies_clean = [int(p) if not np.isnan(p) else 0 for p in performances]
        recomp_acc_overall = float(np.mean(accuracies_clean))
        
        # Hit Rate & Omission Rate
        responses = []
        for i in range(160):
            corr_resp = int(corr_responses[i]) if not np.isnan(corr_responses[i]) else 0
            perf = int(performances[i]) if not np.isnan(performances[i]) else 0
            resp = corr_resp if perf == 1 else (1 - corr_resp)
            responses.append(resp)
            
        hits = 0
        targets_present = 0
        false_alarms = 0
        lures_present = 0
        omissions = 0
        
        for i in range(160):
            rt = rtimes[i]
            if rt <= 0 or rt >= 1500 or np.isnan(rt):
                omissions += 1
                continue
                
            corr_resp = int(corr_responses[i]) if not np.isnan(corr_responses[i]) else 0
            resp = responses[i]
            
            if corr_resp == 1:
                targets_present += 1
                if resp == 1:
                    hits += 1
            else:
                lures_present += 1
                if resp == 1:
                    false_alarms += 1
                    
        recomp_omission = float(omissions / 160)
        recomp_hit_rate = float(hits / targets_present) if targets_present > 0 else None
        
        # Reaction Time Mean & CV
        valid_rts = [float(rt) for rt in rtimes if rt > 0]
        recomp_mean_rt = float(np.mean(valid_rts)) if valid_rts else 0.0
        recomp_rt_sd = float(np.std(valid_rts)) if valid_rts else 0.0
        recomp_rt_cv = (recomp_rt_sd / recomp_mean_rt) if recomp_mean_rt > 0 else 0.0
        
        # Pupil Variability
        pupil_means = []
        for i in range(160):
            t_trace_ref = pupil_ds[1, i]
            p_trace_ref = pupil_ds[0, i]
            p_vec = f[p_trace_ref][()].flatten()
            valid_p = p_vec[~np.isnan(p_vec) & ~np.isinf(p_vec)]
            if len(valid_p) > 0:
                pupil_means.append(np.mean(valid_p))
            else:
                pupil_means.append(0.0)
        recomp_pupil_var = float(np.std(pupil_means)) if pupil_means else None
        
        # Gaze stability (for first trial as an example, but we aggregate them over all 160 trials)
        fix_stabs_norm = []
        for i in range(160):
            t_trace_ref = pupil_ds[1, i]
            t_vec = f[t_trace_ref][()].flatten()
            valid_t = t_vec[~np.isnan(t_vec) & ~np.isinf(t_vec)]
            if len(valid_t) > 0:
                t_start, t_end = valid_t[0], valid_t[-1]
                trial_mask = (raw_time >= t_start) & (raw_time <= t_end)
                t_trial = raw_time[trial_mask]
                pos_trial = raw_pos[trial_mask]
                if len(t_trial) > 0:
                    t_rel = t_trial - t_start
                    fix_mask = ((t_rel >= 0) & (t_rel <= 500)) | \
                               ((t_rel >= 1250) & (t_rel <= 1750)) | \
                               ((t_rel >= 2500) & (t_rel <= 3000))
                    fix_gaze = pos_trial[fix_mask]
                    if len(fix_gaze) > 1:
                        valid_fix = ~np.isnan(fix_gaze[:, 0]) & ~np.isnan(fix_gaze[:, 1]) & (fix_gaze[:, 0] > 0) & (fix_gaze[:, 1] > 0)
                        fix_gaze_v = fix_gaze[valid_fix]
                        if len(fix_gaze_v) > 1:
                            x_norm = fix_gaze_v[:, 0] / 1920.0
                            y_norm = fix_gaze_v[:, 1] / 1080.0
                            fix_stab = np.sqrt(np.var(x_norm) + np.var(y_norm))
                            fix_stabs_norm.append(fix_stab)
        recomp_fix_instab = float(np.mean(fix_stabs_norm)) if fix_stabs_norm else None
        
        # Load final CSV values
        csv_row = df_real[df_real['subject_id'] == subj_id].iloc[0]
        
        metrics_to_compare = [
            ('accuracy_overall', recomp_acc_overall, csv_row['accuracy_overall']),
            ('hit_rate', recomp_hit_rate, csv_row['hit_rate']),
            ('mean_reaction_time_ms', recomp_mean_rt, csv_row['mean_reaction_time_ms']),
            ('rt_coefficient_of_variation', recomp_rt_cv, csv_row['rt_coefficient_of_variation']),
            ('pupil_variability', recomp_pupil_var, csv_row['pupil_variability'])
        ]
        
        if recomp_fix_instab is not None and not np.isnan(csv_row['normalized_fixation_instability']):
            metrics_to_compare.append(('normalized_fixation_instability', recomp_fix_instab, csv_row['normalized_fixation_instability']))
            
        for name, recomp_val, csv_val in metrics_to_compare:
            diff = abs(recomp_val - csv_val)
            status = "PASS" if diff < 1e-6 else "FAIL"
            print(f"  * {name:32s}: Recomp={recomp_val:.6f} | CSV={csv_val:.6f} | Diff={diff:.6e} | {status}")
            trace_rows.append({
                'Subject ID': subj_id,
                'Metric': name,
                'Raw Recomputation': recomp_val,
                'Final CSV Value': csv_val,
                'Difference': diff,
                'Status': status
            })

    print(f"\n[SUCCESS] Completed trace for 6 subjects!")
    
if __name__ == '__main__':
    main()
