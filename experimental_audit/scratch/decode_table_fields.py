import h5py
import numpy as np

def decode():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        pdata = f['Pupil_data']
        
        # Dereference Task_data and Task_epocs for Subject 1 (idx 0)
        task_data_ref = pdata['Task_data'][0, 0]
        task_epocs_ref = pdata['Task_epocs'][0, 0]
        
        task_data_ds = f[task_data_ref]
        task_epocs_ds = f[task_epocs_ref]
        
        print("Task_data dataset shape:", task_data_ds.shape, "dtype:", task_data_ds.dtype)
        print("Task_epocs dataset shape:", task_epocs_ds.shape, "dtype:", task_epocs_ds.dtype)
        
        # Let's see what each column of Task_data points to
        print("\n--- Task_data columns dereference ---")
        for col_idx in range(task_data_ds.shape[1]):
            addr = task_data_ds[0, col_idx]
            # addr is an HDF5 object reference. We can resolve it by f[addr]
            try:
                target = f[addr]
                print(f"Col {col_idx}: Name={target.name}, Type={type(target)}")
                if isinstance(target, h5py.Dataset):
                    print(f"  Shape: {target.shape}, Dtype: {target.dtype}")
                    # Let's check attributes
                    print("  Attributes:")
                    for k, v in target.attrs.items():
                        print(f"    {k}: {v}")
                    # Print first 5 elements
                    if target.ndim == 2:
                        print(f"  Sample: {target[0, :5]}")
                    else:
                        print(f"  Sample: {target[:5]}")
            except Exception as e:
                print(f"Col {col_idx} resolve error: {e}")
                
        # Let's see what each column of Task_epocs points to
        print("\n--- Task_epocs columns dereference ---")
        for col_idx in range(task_epocs_ds.shape[1]):
            addr = task_epocs_ds[0, col_idx]
            try:
                target = f[addr]
                print(f"Col {col_idx}: Name={target.name}, Type={type(target)}")
                if isinstance(target, h5py.Dataset):
                    print(f"  Shape: {target.shape}, Dtype: {target.dtype}")
                    print("  Attributes:")
                    for k, v in target.attrs.items():
                        print(f"    {k}: {v}")
                    if target.ndim == 2:
                        print(f"  Sample: {target[0, :5]}")
                    else:
                        print(f"  Sample: {target[:5]}")
            except Exception as e:
                print(f"Col {col_idx} resolve error: {e}")

if __name__ == "__main__":
    decode()
