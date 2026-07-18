import h5py
import numpy as np

def verify_global():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        print("Checking global 160-length datasets...")
        
        for name in ['g7', 'h7', 'i7', 'j7', 'k7', 'l7']:
            if '/#refs#/' + name in f:
                ds = f['/#refs#/' + name]
                val = ds[()]
                print(f"\nDataset: {name}")
                print(f"  Shape: {ds.shape}, Dtype: {ds.dtype}")
                print(f"  Values (first 10): {val.flatten()[:10]}")
                print(f"  Unique values: {np.unique(val[~np.isnan(val)])}")
            else:
                print(f"\n{name} not found")
                
        # Check cell array m7
        if '/#refs#/m7' in f:
            m7 = f['/#refs#/m7']
            print("\nm7 cell array shape:", m7.shape)
            print("m7 first 5 dereferences:")
            for col in range(5):
                ref = m7[0, col]
                try:
                    target = f[ref]
                    mclass = target.attrs.get('MATLAB_class', b'none').decode('ascii')
                    if mclass == 'char':
                        val = target[()]
                        text = val.tobytes().decode('utf-16') if val.dtype == 'uint16' else val.tobytes().decode('ascii')
                        print(f"  Col {col}: name={target.name}, class={mclass}, val={repr(text.strip())}")
                    else:
                        print(f"  Col {col}: name={target.name}, class={mclass}, shape={target.shape}")
                except Exception as e:
                    print(f"  Col {col} error: {e}")

if __name__ == "__main__":
    verify_global()
