import pandas as pd
import numpy as np
from pymatreader import read_mat

mat_data = read_mat('data/raw/Pupil_dataset.mat')
pupil_ds = mat_data['Pupil_data']

df_prov = pd.read_csv('experimental_audit/results/dataset_provenance_REAL_v1.0.csv')
included_sessions = df_prov[df_prov['Exclusion Reason'] == 'Included']['Session Index'].values

subject_trial_counts = []
per_session_details = []

for idx in included_sessions:
    s_idx = idx - 1
    subj_id = f"subject_{int(pupil_ds['Subject'][s_idx])}"
    task_epoch = pupil_ds['Task_epocs'][s_idx]
    
    trials = task_epoch['Trial']
    loads = task_epoch['Load']
    distractors = task_epoch['Distractor']
    perform = task_epoch['Perform']
    rtime = task_epoch['RTime']
    corr_resp = task_epoch['CorrResponse']
    
    n_trials = len(trials)
    subject_trial_counts.append(n_trials)
    
    per_session_details.append({
        'Session_Index': idx,
        'Subject_ID': subj_id,
        'Group': pupil_ds['Group'][s_idx],
        'Total_Trials': n_trials,
        'Loads_Present': str(sorted(list(set(loads)))),
        'Distractors_Present': str(sorted(list(set(distractors)))),
        'Perform_Values': str(dict(pd.Series(perform).value_counts()))
    })

df_details = pd.DataFrame(per_session_details)
print(f"Total Included Sessions Checked: {len(subject_trial_counts)}")
print(f"Unique Total Trial Counts across all N=40 sessions: {set(subject_trial_counts)}")

print("\nPer-Session Summary (First 10 sessions):")
print(df_details.head(10).to_string())

print("\nValue Counts of Total Trials across all 40 sessions:")
print(df_details['Total_Trials'].value_counts())
