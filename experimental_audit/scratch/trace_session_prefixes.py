import h5py
import numpy as np

def trace_prefixes():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        print("Scanning all #refs# datasets ending in 'qd'...")
        refs = f['#refs#']
        matching = []
        for k in refs.keys():
            if k.endswith('qd'):
                matching.append(k)
        
        # Sort matching keys by length and alphabetically
        matching.sort(key=lambda x: (len(x), x))
        print(f"Found {len(matching)} datasets ending in 'qd'")
        
        for k in matching:
            obj = refs[k]
            if isinstance(obj, h5py.Dataset):
                # Check shape and sample
                shape = obj.shape
                dtype = obj.dtype
                matlab_class = obj.attrs.get('MATLAB_class')
                
                # Check if it is a 1D or 2D array of length 160 or 8000
                is_160 = (160 in shape)
                is_8000 = (8000 in shape)
                
                # Let's print details for the column candidates
                # Usually column datasets are of shape (1, 160) or (1, 8000) or similar
                if is_160 or is_8000 or len(k) <= 3:
                    print(f"\nDataset: #refs#/{k}")
                    print(f"  Shape: {shape}, Dtype: {dtype}, MATLAB_class: {matlab_class}")
                    try:
                        val = obj[()]
                        if val.dtype == object:
                            print(f"  Object references sample: {val.flatten()[:3]}")
                        elif val.dtype.kind == 'u' or val.dtype.kind == 'i' or val.dtype.kind == 'f':
                            print(f"  Numeric values sample: {val.flatten()[:5]}")
                        else:
                            print(f"  Sample bytes: {val.tobytes()[:20]}")
                    except Exception as e:
                        print(f"  Failed to read sample: {e}")

if __name__ == "__main__":
    trace_prefixes()
