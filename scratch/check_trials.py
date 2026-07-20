from pymatreader import read_mat
import pandas as pd
import numpy as np

mat_data = read_mat('data/raw/Pupil_dataset.mat')
pupil_ds = mat_data['Pupil_dataset']

df_prov = pd.read_csv('experimental_audit/results/dataset_provenance_REAL_v1.0.csv')
included_sessions = df_prov[df_prov['Exclusion Reason'] == 'Included']['Session Index'].values

trial_counts = []
for idx in included_sessions:
    s_idx = idx - 1
    subj_id = f"subject_{int(pupil_ds['Subject'][s_idx])}"
    group = pupil_ds['Group'][s_idx]
    task_epoch = pupil_ds['Task_epocs'][s_idx]
    
    trials = task_epoch.get('Trial', [])
    n_trials = len(trials) if isinstance(trials, (list, np.ndarray)) else 0
    trial_counts.append({
        'Session_Index': idx,
        'Subject_ID': subj_id,
        'Group': group,
        'Trial_Count': n_trials
    })

df_trials = pd.DataFrame(trial_counts)
print(f"Total included sessions: {len(df_trials)}")
print(f"Unique trial counts across included sessions: {df_trials['Trial_Count'].unique()}")
print("\nTrial Count Summary:")
print(df_trials['Trial_Count'].value_counts())
print("\nDetailed per session:")
print(df_trials.to_string())
