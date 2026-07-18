import h5py

def trace_mcos():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        mcos = f['#subsystem#/MCOS']
        print(f"MCOS shape: {mcos.shape}, dtype: {mcos.dtype}")
        
        # Let's inspect the first 10 references in MCOS
        for idx in range(min(50, mcos.shape[1])):
            ref = mcos[0, idx]
            print(f"\nIndex {idx}: ref={ref}")
            try:
                target = f[ref]
                print(f"  Target name: {target.name}")
                print(f"  Type: {type(target)}")
                if isinstance(target, h5py.Dataset):
                    print(f"  Shape: {target.shape}, Dtype: {target.dtype}")
                    print(f"  Sample: {target[()]}")
                elif isinstance(target, h5py.Group):
                    print(f"  Keys: {list(target.keys())}")
            except Exception as e:
                print(f"  Failed to resolve: {e}")

if __name__ == "__main__":
    trace_mcos()
