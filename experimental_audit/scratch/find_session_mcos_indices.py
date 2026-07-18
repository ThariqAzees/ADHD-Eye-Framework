import h5py

def find_indices():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        pdata = f['Pupil_data']
        
        # Print for first 3 sessions
        for i in range(3):
            print(f"\n--- Session {i} (Subject {pdata['Subject'][i, 0]}) ---")
            
            for key in ['Task_data', 'Task_epocs', 'Wisc']:
                ref = pdata[key][i, 0]
                target = f[ref]
                val = target[()]
                print(f"  {key}: path={target.name}, shape={target.shape}, val={val.flatten()}")

if __name__ == "__main__":
    find_indices()
