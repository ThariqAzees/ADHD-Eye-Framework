import h5py
import numpy as np
import pandas as pd

def decode_mat_value(f, ref):
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

def inspect_cohort():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        pdata = f['Pupil_data']
        mcos = f['#subsystem#/MCOS']
        num_sessions = pdata['Subject'].shape[0]
        
        sessions_info = []
        for i in range(num_sessions):
            # Subject ID
            subj_ref = pdata['Subject'][i, 0]
            subj_val = decode_mat_value(f, subj_ref)
            
            # Group
            group_ref = pdata['Group'][i, 0]
            group_val = decode_mat_value(f, group_ref)
            
            # Age
            age_ref = pdata['Age'][i, 0]
            age_val = decode_mat_value(f, age_ref)
            
            # Continuous data (Task_data)
            has_continuous = False
            total_samples = 0
            valid_gaze_samples = 0
            valid_pupil_samples = 0
            
            try:
                td_idx = 9 + 7 * i
                td_cell_ref = mcos[0, td_idx]
                td_cell = f[td_cell_ref]
                
                time_ref = td_cell[0, 0] if td_cell.ndim == 2 else td_cell[0]
                time_shape = f[time_ref].shape
                total_samples = time_shape[1] if len(time_shape) == 2 else time_shape[0]
                
                pos_ref = td_cell[2, 0] if td_cell.ndim == 2 else td_cell[2]
                pos_ds = f[pos_ref]
                pos_val = pos_ds[()]
                
                diam_ref = td_cell[1, 0] if td_cell.ndim == 2 else td_cell[1]
                diam_ds = f[diam_ref]
                diam_val = diam_ds[()]
                
                valid_gaze_samples = np.sum(~np.isnan(pos_val[0]) & ~np.isnan(pos_val[1])) if pos_val.ndim == 2 else np.sum(~np.isnan(pos_val))
                valid_pupil_samples = np.sum(~np.isnan(diam_val))
                has_continuous = True
            except Exception as e:
                pass
                
            # Trial-by-trial data (Task_epocs)
            trials_count = 0
            has_trials = False
            try:
                te_idx = 541 + 7 * i
                te_cell_ref = mcos[0, te_idx]
                te_cell = f[te_cell_ref]
                trial_ref = te_cell[0, 0] if te_cell.ndim == 2 else te_cell[0]
                trials_shape = f[trial_ref].shape
                trials_count = trials_shape[1] if len(trials_shape) == 2 else trials_shape[0]
                has_trials = True
            except Exception as e:
                pass
                
            # Check if this index belongs to the control sessions at the end where we failed
            # Let's inspect the raw header to see what trials shape it has
            if not has_trials:
                try:
                    # Let's look at the Task_epocs ref directly
                    te_ref = pdata['Task_epocs'][i, 0]
                    te_target = f[te_ref]
                    # Check if it has a shape or value that we can read
                    val = te_target[()]
                    # If the 5th value is an index in MCOS
                    m_idx = int(val.flatten()[4])
                    ref_in_mcos = mcos[0, m_idx - 1]
                    target_mcos = f[ref_in_mcos]
                    # Let's print its class and type
                    mclass = target_mcos.attrs.get('MATLAB_class', b'none').decode('ascii')
                    trials_count = f"Failed MCOS ({target_mcos.name}, class={mclass}, shape={getattr(target_mcos, 'shape', 'No shape')})"
                except Exception as e2:
                    trials_count = f"Error: {e2}"
            
            sessions_info.append({
                'session_idx': i,
                'subject_id': subj_val,
                'original_group': group_val,
                'total_samples': total_samples,
                'valid_gaze_samples': valid_gaze_samples,
                'valid_pupil_samples': valid_pupil_samples,
                'trials_count': trials_count,
                'has_continuous': has_continuous,
                'has_trials': has_trials
            })
            
        df = pd.DataFrame(sessions_info)
        pd.set_option('display.max_rows', 100)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        print(df)
        
        # Let's output to a JSON/CSV for safe processing
        df.to_csv("experimental_audit/scratch/cohort_info.csv", index=False)

if __name__ == "__main__":
    inspect_cohort()
