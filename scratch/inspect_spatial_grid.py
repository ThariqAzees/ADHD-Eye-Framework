import pandas as pd
import numpy as np
from pymatreader import read_mat

mat_data = read_mat('data/raw/Pupil_dataset.mat')
pupil_ds = mat_data['Pupil_data']

# Inspect Task_data for first subject
subj0_data = pupil_ds['Task_data'][0]
print("Keys in Task_data[0]:", subj0_data.keys() if isinstance(subj0_data, dict) else type(subj0_data))

for k, v in subj0_data.items():
    if isinstance(v, (list, np.ndarray)):
        arr = np.array(v)
        print(f"  {k}: shape={arr.shape}, min={np.nanmin(arr)}, max={np.nanmax(arr)}")
