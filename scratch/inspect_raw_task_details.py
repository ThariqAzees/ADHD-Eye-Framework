import pandas as pd
import numpy as np
from pymatreader import read_mat

mat_data = read_mat('data/raw/Pupil_dataset.mat')
pupil_ds = mat_data['Pupil_data']

df_prov = pd.read_csv('experimental_audit/results/dataset_provenance_REAL_v1.0.csv')
included_sessions = df_prov[df_prov['Exclusion Reason'] == 'Included']['Session Index'].values

print("=== DISTRACTOR AND LOAD CODES ACROSS ALL INCLUDED SESSIONS ===")
all_loads = []
all_dists = []
all_perfs = []
all_corrs = []

for idx in included_sessions:
    s_idx = idx - 1
    task_epoch = pupil_ds['Task_epocs'][s_idx]
    
    all_loads.extend(task_epoch['Load'])
    all_dists.extend(task_epoch['Distractor'])
    all_perfs.extend(task_epoch['Perform'])
    all_corrs.extend(task_epoch['CorrResponse'])

print("Unique Memory Load values:", pd.Series(all_loads).value_counts().to_dict())
print("Unique Distractor values:", pd.Series(all_dists).value_counts().to_dict())
print("Unique Perform values:", pd.Series(all_perfs).value_counts(dropna=False).to_dict())
print("Unique CorrResponse values:", pd.Series(all_corrs).value_counts(dropna=False).to_dict())

print("\n=== PARSING FALSE ALARM RATE CALCULATION IN CODE ===")
# Let's inspect dataset/parse_mat.py for false_alarm_rate calculation
with open('dataset/parse_mat.py', 'r') as f:
    content = f.read()
    for i, line in enumerate(content.split('\n'), 1):
        if 'false_alarm' in line.lower() or 'perform' in line.lower() or 'corrresponse' in line.lower():
            print(f"L{i}: {line.strip()}")
