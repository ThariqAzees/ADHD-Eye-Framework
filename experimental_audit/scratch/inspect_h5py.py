import h5py
import numpy as np

def inspect_hdf5():
    path = "data/raw/Pupil_dataset.mat"
    print("Opening MAT file with h5py...")
    with h5py.File(path, 'r') as f:
        print("Root level keys:", list(f.keys()))
        
        # Let's check 'Pupil_data'
        if 'Pupil_data' in f:
            pdata = f['Pupil_data']
            print("\nPupil_data type:", type(pdata))
            print("Pupil_data keys:", list(pdata.keys()))
            
            # Let's inspect 'Task_data' and 'Task_epocs' references
            for k in ['Task_data', 'Task_epocs', 'Wisc']:
                if k in pdata:
                    ref_arr = pdata[k]
                    print(f"\nSubgroup '{k}':")
                    print(f"  Shape: {ref_arr.shape}")
                    print(f"  Dtype: {ref_arr.dtype}")
                    print(f"  Type: {type(ref_arr)}")
                    
                    # Resolve first reference
                    if len(ref_arr) > 0:
                        first_ref = ref_arr[0][0] if ref_arr.ndim == 2 else ref_arr[0]
                        print(f"  First item reference value: {first_ref}")
                        print(f"  Is it HDF5 Reference? {isinstance(first_ref, h5py.Reference)}")
                        
                        try:
                            # Dereference it
                            deref = f[first_ref]
                            print(f"  Resolved target type: {type(deref)}")
                            if isinstance(deref, h5py.Group):
                                print(f"  Resolved target keys: {list(deref.keys())}")
                                for child_k in deref.keys():
                                    child_val = deref[child_k]
                                    print(f"    Child '{child_k}' shape: {child_val.shape}, dtype: {child_val.dtype if hasattr(child_val, 'dtype') else 'group'}")
                            elif isinstance(deref, h5py.Dataset):
                                print(f"  Resolved target shape: {deref.shape}, dtype: {deref.dtype}")
                                print(f"  Resolved target sample: {deref[()]}")
                        except Exception as e:
                            print(f"  Failed to dereference: {e}")

if __name__ == "__main__":
    inspect_hdf5()
