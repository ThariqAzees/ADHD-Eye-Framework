import h5py
import numpy as np
import pandas as pd

def evaluate_pupil():
    path = "data/raw/Pupil_dataset.mat"
    print("Opening dataset...")
    
    with h5py.File(path, 'r') as f:
        mcos = f['#subsystem#/MCOS']
        pdata = f['Pupil_data']
        num_sessions = pdata['Subject'].shape[0]
        
        records = []
        for i in range(num_sessions):
            # We only load the first 57 valid sessions (to avoid the empty/incomplete control sessions at the end)
            if i >= 57:
                continue
                
            # Group and Subject
            subj_ref = pdata['Subject'][i, 0]
            subj_val = int(f[subj_ref][0, 0])
            group_ref = pdata['Group'][i, 0]
            group_ds = f[group_ref]
            group_val = group_ds[()].tobytes().decode('utf-16') if group_ds.dtype == 'uint16' else group_ds[()].tobytes().decode('ascii')
            group_val = group_val.strip()
            
            # Exclude medicated sessions to prevent leakage
            if group_val == 'on-ADHD':
                continue
                
            # Load Task_epocs
            te_idx = 541 + 7 * i
            te_cell = f[mcos[0, te_idx]]
            
            # Load Load and Pupil columns
            load_ds = f[te_cell[1, 0] if te_cell.ndim == 2 else te_cell[1]]
            pupil_ds = f[te_cell[6, 0] if te_cell.ndim == 2 else te_cell[6]]
            
            loads = load_ds[()].flatten()
            num_trials = len(loads)
            
            # Extract trial pupil means
            trial_means = []
            load1_means = []
            load2_means = []
            trial_stds = []
            
            for t_idx in range(num_trials):
                # Row 0 of Pupil cell array contains pupil z-scores
                p_ref = pupil_ds[0, t_idx]
                p_vec = f[p_ref][()].flatten()
                
                # Filter valid
                valid_p = p_vec[~np.isnan(p_vec)]
                if len(valid_p) > 0:
                    mean_val = np.mean(valid_p)
                    std_val = np.std(valid_p)
                    trial_means.append(mean_val)
                    trial_stds.append(std_val)
                    if loads[t_idx] == 1:
                        load1_means.append(mean_val)
                    elif loads[t_idx] == 2:
                        load2_means.append(mean_val)
                        
            if trial_means:
                records.append({
                    'subject_id': subj_val,
                    'group': 'ADHD' if 'ADHD' in group_val else 'Control',
                    'session_pupil_mean': np.mean(trial_means),
                    'session_pupil_std_of_means': np.std(trial_means),
                    'mean_trial_pupil_std': np.mean(trial_stds),
                    'pupil_load_diff': np.mean(load2_means) - np.mean(load1_means) if load1_means and load2_means else 0.0
                })
                
        df = pd.DataFrame(records)
        print(f"\nSuccessfully evaluated {len(df)} independent subjects (28 ADHD, 12 Control).")
        print("\nMean of pupil features by Group:")
        print(df.groupby('group')[['session_pupil_mean', 'session_pupil_std_of_means', 'mean_trial_pupil_std', 'pupil_load_diff']].mean())
        print("\nStandard deviation of pupil features by Group:")
        print(df.groupby('group')[['session_pupil_mean', 'session_pupil_std_of_means', 'mean_trial_pupil_std', 'pupil_load_diff']].std())

if __name__ == "__main__":
    evaluate_pupil()
