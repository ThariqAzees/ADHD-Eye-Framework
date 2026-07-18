import h5py
import numpy as np

def test_load():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        mcos = f['#subsystem#/MCOS']
        pdata = f['Pupil_data']
        
        # Test Session 0 (Subject 1) and Session 1 (Subject 2)
        for i in [0, 1]:
            print(f"\n================ SESSION {i} ================")
            # Subject details
            subj_id = pdata['Subject'][i, 0]
            group = pdata['Group'][i, 0]
            age = pdata['Age'][i, 0]
            print(f"Subject: {subj_id}, Group: {group}, Age: {age}")
            
            # 1. Load Task_data (Continuous streams)
            print("\n--- Task_data (Continuous streams) ---")
            td_ref_idx = 9 + 7 * i
            td_cell_ref = mcos[0, td_ref_idx]
            td_cell = f[td_cell_ref]
            print(f"Task_data cell array name: {td_cell.name}, shape: {td_cell.shape}")
            
            # Dereference the 4 channels: Time, Diameter, Position, Events
            channels = ['Time', 'Diameter', 'Position', 'Events']
            for col_idx, chan_name in enumerate(channels):
                chan_ref = td_cell[col_idx, 0] if td_cell.ndim == 2 else td_cell[col_idx]
                chan_ds = f[chan_ref]
                print(f"  Channel '{chan_name}': path={chan_ds.name}, shape={chan_ds.shape}, dtype={chan_ds.dtype}")
                # Print first 5 values
                val = chan_ds[()]
                if val.ndim == 2:
                    print(f"    Sample: {val[:, :5]}")
                else:
                    print(f"    Sample: {val[:5]}")
            
            # 2. Load Task_epocs (Trial-by-trial data)
            print("\n--- Task_epocs (Trial-by-trial data) ---")
            te_ref_idx = 541 + 7 * i
            te_cell_ref = mcos[0, te_ref_idx]
            te_cell = f[te_cell_ref]
            print(f"Task_epocs cell array name: {te_cell.name}, shape: {te_cell.shape}")
            
            # Dereference the 7 columns: Trial, Load, Distractor, CorrResponse, Perform, Rtime, Pupil
            columns = ['Trial', 'Load', 'Distractor', 'CorrResponse', 'Perform', 'Rtime', 'Pupil']
            for col_idx, col_name in enumerate(columns):
                col_ref = te_cell[col_idx, 0] if te_cell.ndim == 2 else te_cell[col_idx]
                col_ds = f[col_ref]
                print(f"  Column '{col_name}': path={col_ds.name}, shape={col_ds.shape}, dtype={col_ds.dtype}")
                
                # Print sample based on type
                if col_name == 'Pupil':
                    # Cell array of trial pupil traces
                    print(f"    Pupil is cell array of pupil traces. Sample references:")
                    for trial_idx in range(3):
                        # Row 0: Relative Time, Row 1: Pupil size
                        t_ref = col_ds[0, trial_idx]
                        p_ref = col_ds[1, trial_idx]
                        t_ds = f[t_ref]
                        p_ds = f[p_ref]
                        print(f"      Trial {trial_idx}: time_shape={t_ds.shape}, pupil_shape={p_ds.shape}")
                elif col_name == 'Distractor':
                    # Cell array of distractor codes/indices
                    val = col_ds[()]
                    print(f"    Sample codes: {val.flatten()[:5]}")
                else:
                    val = col_ds[()]
                    print(f"    Sample values: {val.flatten()[:5]}")

if __name__ == "__main__":
    test_load()
