import os
import urllib.request
import hashlib
import json
import datetime
import numpy as np
import pandas as pd
import scipy.io as sio
from pymatreader import read_mat
from dataset.schema import SubjectAggregateFeatures
from dataset.parse_mat import extract_subject_features

# DOI: 10.6084/m9.figshare.7218725
DATASET_URL = "https://ndownloader.figshare.com/files/14298953"
EXPECTED_MD5 = "d4a1e92c8e125e93831f12797a783d52"

def get_data_dirs() -> tuple:
    """Returns absolute paths to data directories, creating them if needed."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    processed_dir = os.path.join(base_dir, "data", "processed")
    exports_dir = os.path.join(base_dir, "data", "exports")
    
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(exports_dir, exist_ok=True)
    
    return raw_dir, processed_dir, exports_dir

def check_file_md5(filepath: str, expected_md5: str) -> bool:
    """Checks the MD5 hash of a file."""
    if not os.path.exists(filepath):
        return False
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest() == expected_md5

def download_real_dataset(progress_callback=None) -> str:
    """
    Downloads the real Figshare dataset to data/raw/Pupil_dataset.mat.
    Updates progress_callback with float representing percentage.
    """
    raw_dir, _, _ = get_data_dirs()
    mat_path = os.path.join(raw_dir, "Pupil_dataset.mat")
    
    # Check if file exists and MD5 matches
    if os.path.exists(mat_path) and check_file_md5(mat_path, EXPECTED_MD5):
        if progress_callback:
            progress_callback(100.0)
        return mat_path
        
    # Download with progress tracking
    print(f"Downloading dataset from {DATASET_URL}...")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(DATASET_URL, headers=headers)
    
    with urllib.request.urlopen(req) as response:
        total_size = int(response.info().get('Content-Length', 0))
        block_size = 1024 * 256  # 256 KB
        downloaded = 0
        
        with open(mat_path, 'wb') as out_file:
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                downloaded += len(buffer)
                out_file.write(buffer)
                
                if total_size > 0 and progress_callback:
                    percent = (downloaded / total_size) * 100.0
                    progress_callback(percent)
                    
    # Verify MD5 after download
    if not check_file_md5(mat_path, EXPECTED_MD5):
        raise ValueError("MD5 verification failed. The downloaded file might be corrupted.")
        
    return mat_path

def generate_mock_dataset() -> str:
    """
    Generates a mock/synthetic Pupil_dataset.mat file with the correct fields and schema.
    Used for local offline testing and fast verification.
    """
    raw_dir, _, _ = get_data_dirs()
    mat_path = os.path.join(raw_dir, "Pupil_dataset.mat")
    
    print("Generating high-fidelity mock MATLAB dataset...")
    
    np.random.seed(42)
    subjects = []
    
    # Create 50 subjects matching the clinical layout (28 ADHD, 22 Control)
    for i in range(50):
        subject_id = f"sub_{i+1:02d}"
        is_control = (i < 22)
        group = 'Ctrl' if is_control else ('off-ADHD' if i % 2 == 0 else 'on-ADHD')
        
        # Determine performance probabilities to satisfy load effect: accuracy(1-dot) > accuracy(2-dot)
        if is_control:
            p_load1 = 0.90
            p_load2 = 0.80
            rt_mean = 600.0
            rt_sd = 100.0
            fix_mean = 1.2
            disp_mean = 1.8
        else:
            p_load1 = 0.78
            p_load2 = 0.64
            rt_mean = 750.0
            rt_sd = 160.0
            fix_mean = 2.4
            disp_mean = 3.2
            
        num_trials = 40
        trials = np.arange(1, num_trials + 1)
        loads = np.random.choice([1, 2], size=num_trials, p=[0.5, 0.5])
        distractors = np.random.choice(['none', 'neutral', 'emotional', 'task_related'], size=num_trials, p=[0.4, 0.2, 0.2, 0.2])
        corr_responses = np.random.choice([0, 1], size=num_trials)
        
        performances = []
        rtimes = []
        pupils = []
        
        # Generate trials
        for j in range(num_trials):
            ld = loads[j]
            p_acc = p_load1 if ld == 1 else p_load2
            perf = np.random.choice([1, 0], p=[p_acc, 1.0 - p_acc])
            performances.append(perf)
            
            # Omission (no response) probability
            is_omission = np.random.choice([False, True], p=[0.97, 0.03])
            if is_omission:
                rt = 0.0
            else:
                rt = max(200.0, np.random.normal(rt_mean, rt_sd))
            rtimes.append(rt)
            
            # Generate mock pupil trace
            # Timestamps: 10 points (100ms spacing)
            t_vec = np.arange(j * 5000, j * 5000 + 1000, 100).astype(float)
            p_vec = np.random.normal(0.0, 1.0, size=10)
            if not is_control:
                # Add a downward slope or different variance for ADHD
                p_vec += np.linspace(0.2, -0.2, 10)
            pupils.append([t_vec, p_vec])
            
        # Create raw task_data coordinates
        # Time steps every 10ms for 5000ms * 40 trials = 20000 points
        total_time_steps = 20000
        raw_t = np.arange(0, total_time_steps * 10, 10).astype(float)
        
        # Gaze position (centered at 960, 540 with variance)
        raw_x = np.random.normal(960.0, fix_mean if is_control else fix_mean * 2.0, size=total_time_steps)
        raw_y = np.random.normal(540.0, fix_mean if is_control else fix_mean * 2.0, size=total_time_steps)
        raw_p = np.stack([raw_x, raw_y], axis=1)
        
        raw_diam = np.random.normal(500.0, 50.0, size=total_time_steps)
        raw_events = ['' for _ in range(total_time_steps)]
        
        subj_dict = {
            'Subject': i + 1,
            'Age': float(10.5 + np.random.normal(0, 1.5)),
            'Group': group,
            'Task_data': {
                'Time': raw_t,
                'Diameter': raw_diam,
                'Position': raw_p,
                'Events': raw_events
            },
            'Task_epoch': {
                'Trial': trials.astype(float),
                'Load': loads.astype(float),
                'Distractor': list(distractors),
                'CorrResponse': corr_responses.astype(float),
                'Perform': np.array(performances).astype(float),
                'RTime': np.array(rtimes).astype(float),
                'Pupil': pupils
            },
            'WISC': {
                'Vocabulary': 10.0,
                'Similarities': 11.0
            }
        }
        subjects.append(subj_dict)
        
    sio.savemat(mat_path, {'Pupil_dataset': subjects})
    print(f"Mock dataset generated successfully at {mat_path}")
    return mat_path

def run_dataset_validation(features_df: pd.DataFrame) -> dict:
    """
    Runs the validation checks on the processed features.
    Returns a dictionary of reports and validation status.
    """
    report = {}
    
    # 1. Total number of participants
    num_participants = features_df['subject_id'].nunique()
    report['num_participants'] = int(num_participants)
    report['num_participants_valid'] = bool(num_participants == 40)
    
    # 2. Class Balance (ADHD vs Control)
    class_counts = features_df['group'].value_counts().to_dict()
    report['class_counts'] = {str(k): int(v) for k, v in class_counts.items()}
    num_adhd = class_counts.get('ADHD', 0)
    num_control = class_counts.get('Control', 0)
    report['class_balance_ratio'] = float(num_adhd / num_control) if num_control > 0 else 0.0
    # Expected exactly 28 ADHD and 12 Control
    report['class_balance_valid'] = bool(num_adhd == 28 and num_control == 12)
    
    # 3. Missing values
    missing_counts = features_df.isnull().sum().to_dict()
    report['missing_value_counts'] = {str(k): int(v) for k, v in missing_counts.items()}
    report['has_missing_values'] = bool(any(v > 0 for v in missing_counts.values()))
    
    # 4. Feature distributions (mean, std, min, max)
    distributions = {}
    numeric_cols = features_df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        distributions[col] = {
            'mean': float(features_df[col].mean()),
            'std': float(features_df[col].std()),
            'min': float(features_df[col].min()),
            'max': float(features_df[col].max())
        }
    report['feature_distributions'] = distributions
    
    # 5. Reaction time ranges
    rt_min = features_df['mean_reaction_time_ms'].min()
    rt_max = features_df['mean_reaction_time_ms'].max()
    report['rt_range'] = {'min': float(rt_min), 'max': float(rt_max)}
    # Reaction times should be positive and in reasonable ranges
    report['rt_range_valid'] = bool(rt_min > 200.0 and rt_max < 1500.0)
    
    # Verify working memory load effect
    mean_load_diff = features_df['accuracy_by_load_diff'].mean()
    report['mean_accuracy_by_load_diff'] = float(mean_load_diff)
    report['load_effect_valid'] = bool(mean_load_diff > 0.0)
    
    # Overall validation status
    report['all_valid'] = bool(
        report['num_participants_valid'] and
        report['class_balance_valid'] and
        not report['has_missing_values'] and
        report['rt_range_valid'] and
        report['load_effect_valid']
    )
    
    return report

def build_processed_dataset(mat_path: str) -> tuple:
    """
    Parses the authentic Pupil_dataset.mat file via h5py and MCOS indices,
    extracts SubjectAggregateFeatures, validates them, and saves features
    to data/processed/dataset_features_REAL_v1.0.csv.
    """
    import h5py
    from dataset.parse_mat import extract_subject_features
    
    # 1. Enforce hard-error checking on MD5
    expected_md5 = "d4a1e92c8e125e93831f12797a783d52"
    if not check_file_md5(mat_path, expected_md5):
        raise ValueError(f"MAT file at {mat_path} is missing or has an incorrect MD5 checksum. Recovery pipeline aborted.")
        
    _, processed_dir, _ = get_data_dirs()
    output_csv = os.path.join(processed_dir, "dataset_features_REAL_v1.0.csv")
    output_metadata = os.path.join(processed_dir, "dataset_features_REAL_v1.0_metadata.json")
    
    print(f"Parsing authentic MATLAB dataset from {mat_path} via HDF5...")
    
    subject_features_list = []
    
    with h5py.File(mat_path, 'r') as f:
        mcos = f['#subsystem#/MCOS']
        pdata = f['Pupil_data']
        num_sessions = pdata['Subject'].shape[0]
        
        print(f"Total sessions in raw file: {num_sessions}")
        
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
            
        included_count = 0
        for i in range(num_sessions):
            # Extract basic identifiers
            subj_ref = pdata['Subject'][i, 0]
            subj_val = decode_value(subj_ref)
            
            group_ref = pdata['Group'][i, 0]
            group_val = decode_value(group_ref)
            
            # Check None/NaN first to avoid value conversion errors
            if subj_val is None or (isinstance(subj_val, float) and np.isnan(subj_val)) or group_val is None:
                print(f"Excluding Session {i} because subject ID or group is missing/invalid.")
                continue
                
            # Exclusion 1: Repeated medicated sessions
            if group_val == 'on-ADHD':
                print(f"Excluding Session {i} (Subject {int(subj_val)}): repeated medicated measurement.")
                continue
                
            # Check trial count to filter incomplete control sessions
            trials_count = 0
            has_trials = False
            try:
                te_idx = 541 + 7 * i
                te_cell = f[mcos[0, te_idx]]
                trial_ref = te_cell[0, 0] if te_cell.ndim == 2 else te_cell[0]
                trials_shape = f[trial_ref].shape
                trials_count = trials_shape[1] if len(trials_shape) == 2 else trials_shape[0]
                has_trials = True
            except:
                pass
                
            # Exclusion 2: Incomplete sessions
            if trials_count != 160:
                print(f"Excluding Session {i} (Subject {int(subj_val)}): incomplete data (trials count = {trials_count}).")
                continue
                
            # Extract Task_data continuous streams
            td_idx = 9 + 7 * i
            td_cell = f[mcos[0, td_idx]]
            
            time_ref = td_cell[0, 0] if td_cell.ndim == 2 else td_cell[0]
            pos_ref = td_cell[2, 0] if td_cell.ndim == 2 else td_cell[2]
            diam_ref = td_cell[1, 0] if td_cell.ndim == 2 else td_cell[1]
            
            task_data = {
                'Time': f[time_ref][()].flatten(),
                'Position': f[pos_ref][()],
                'Diameter': f[diam_ref][()].flatten()
            }
            
            # Extract Task_epocs trial-by-trial columns
            load_ref = te_cell[1, 0] if te_cell.ndim == 2 else te_cell[1]
            dist_ref = te_cell[2, 0] if te_cell.ndim == 2 else te_cell[2]
            corr_ref = te_cell[3, 0] if te_cell.ndim == 2 else te_cell[3]
            perf_ref = te_cell[4, 0] if te_cell.ndim == 2 else te_cell[4]
            rt_ref = te_cell[5, 0] if te_cell.ndim == 2 else te_cell[5]
            pup_ref = te_cell[6, 0] if te_cell.ndim == 2 else te_cell[6]
            
            # Extract trials pupil traces cell array list
            pupil_ds = f[pup_ref]
            pupils_list = []
            for t in range(160):
                t_trace_ref = pupil_ds[1, t]
                p_trace_ref = pupil_ds[0, t]
                pupils_list.append((f[t_trace_ref][()].flatten(), f[p_trace_ref][()].flatten()))
                
            task_epoch = {
                'Trial': f[trial_ref][()].flatten(),
                'Load': f[load_ref][()].flatten(),
                'Distractor': f[dist_ref][()].flatten(),
                'CorrResponse': f[corr_ref][()].flatten(),
                'Perform': f[perf_ref][()].flatten(),
                'RTime': f[rt_ref][()].flatten(),
                'Pupil': pupils_list
            }
            
            subj_id_str = f"subject_{int(subj_val)}"
            group_mapped = 'ADHD' if 'ADHD' in group_val else 'Control'
            
            # Extract subject features
            _, agg_feat = extract_subject_features(subj_id_str, group_mapped, task_epoch, task_data)
            subject_features_list.append(agg_feat)
            included_count += 1
            
    # Convert to DataFrame
    features_df = pd.DataFrame([f.__dict__ for f in subject_features_list])
    
    clean_cols = [
        'subject_id', 'group',
        'mean_reaction_time_ms', 'median_reaction_time_ms', 'rt_variability', 'rt_coefficient_of_variation',
        'accuracy_overall', 'accuracy_by_load_diff', 'accuracy_by_distractor_diff',
        'mean_fixation_stability', 'mean_pupil_proxy',
        'normalized_fixation_instability', 'normalized_gaze_dispersion', 'pupil_variability',
        'omission_rate', 'false_alarm_rate', 'hit_rate'
    ]
    features_df_clean = features_df[clean_cols]
    features_df_clean.to_csv(output_csv, index=False)
    
    # Run validations
    validation_report = run_dataset_validation(features_df_clean)
    
    # Save metadata JSON
    metadata = {
        "framework_version": "1.0.0",
        "feature_extractor_version": "1.0.0",
        "dataset_version": "Rojas-Libano-2019-v3",
        "processed_timestamp": datetime.datetime.now().isoformat(),
        "num_subjects": int(included_count),
        "validation": validation_report
    }
    
    with open(output_metadata, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Dataset features saved to {output_csv}")
    print(f"Validation report saved to {output_metadata}")
    
    return features_df_clean, validation_report
