import h5py
import numpy as np
import pandas as pd
from collections import Counter

def decode_mat_value(f, ref):
    if not isinstance(ref, h5py.Reference):
        # It's a raw number or string already
        if isinstance(ref, np.ndarray):
            return ref.flatten()[0] if ref.size > 0 else None
        return ref
        
    target = f[ref]
    if isinstance(target, h5py.Dataset):
        val = target[()]
        mclass = target.attrs.get('MATLAB_class')
        
        # 1. Handle char array
        if mclass == b'char':
            if val.dtype == 'uint16':
                return val.tobytes().decode('utf-16').strip()
            else:
                return val.tobytes().decode('ascii', errors='ignore').strip()
                
        # 2. Handle numeric array representing character codes (often uint16/uint8)
        if target.dtype.kind in 'ui' and val.size > 0 and val.size < 100:
            try:
                # Try to decode as characters if they are in printable ASCII range
                chars = [chr(int(c)) for c in val.flatten()]
                if all(32 <= ord(c) < 127 for c in chars):
                    return "".join(chars).strip()
            except:
                pass
                
        # 3. Handle standard numeric value
        if val.size == 0:
            return None
        return val.flatten()[0]
    return target

def verify_all():
    path = "data/raw/Pupil_dataset.mat"
    print("Opening dataset...")
    
    with h5py.File(path, 'r') as f:
        mcos = f['#subsystem#/MCOS']
        pdata = f['Pupil_data']
        num_sessions = pdata['Subject'].shape[0]
        print(f"Total sessions in file: {num_sessions}")
        
        session_records = []
        
        for i in range(num_sessions):
            try:
                # 1. Subject ID
                subj_ref = pdata['Subject'][i, 0]
                subj_val = decode_mat_value(f, subj_ref)
                
                # 2. Group
                group_ref = pdata['Group'][i, 0]
                group_val = decode_mat_value(f, group_ref)
                
                # 3. Age
                age_ref = pdata['Age'][i, 0]
                age_val = decode_mat_value(f, age_ref)
                
                # 4. Task_data (Continuous stream length)
                td_idx = 9 + 7 * i
                td_cell_ref = mcos[0, td_idx]
                td_cell = f[td_cell_ref]
                time_ref = td_cell[0, 0] if td_cell.ndim == 2 else td_cell[0]
                time_shape = f[time_ref].shape
                samples_count = time_shape[1] if len(time_shape) == 2 else time_shape[0]
                
                # 5. Task_epocs (Number of trials)
                te_idx = 541 + 7 * i
                te_cell_ref = mcos[0, te_idx]
                te_cell = f[te_cell_ref]
                trial_ref = te_cell[0, 0] if te_cell.ndim == 2 else te_cell[0]
                trials_shape = f[trial_ref].shape
                trials_count = trials_shape[1] if len(trials_shape) == 2 else trials_shape[0]
                
                session_records.append({
                    'session_idx': i,
                    'subject_id': int(subj_val) if subj_val is not None else None,
                    'group': group_val,
                    'age': age_val,
                    'samples_count': samples_count,
                    'trials_count': trials_count
                })
            except Exception as e:
                import traceback
                print(f"Error loading session {i}: {e}")
                traceback.print_exc()
                
        df = pd.DataFrame(session_records)
        print("\nLoaded successfully! Summary of loaded sessions:")
        print(f"Total sessions loaded: {len(df)}")
        print("\nGroup counts:")
        print(Counter(df['group']))
        print("\nFirst 15 sessions:")
        print(df.head(15))
        print("\nLast 15 sessions:")
        print(df.tail(15))
        
        # Verify if all sessions have exactly 160 trials
        bad_trials = df[df['trials_count'] != 160]
        if len(bad_trials) > 0:
            print(f"\nWARNING: Found sessions without 160 trials:\n{bad_trials}")
        else:
            print("\nSUCCESS: All sessions have exactly 160 trials!")

if __name__ == "__main__":
    verify_all()
