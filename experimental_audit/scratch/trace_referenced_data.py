import h5py
import numpy as np

def trace():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        print("Reading trial data for Subject 1...")
        
        # Check /#refs#/aqd
        if '/#refs#/aqd' in f:
            aqd = f['/#refs#/aqd'][()]
            print("aqd shape:", aqd.shape, "sample:", aqd[0, :10])
        else:
            print("aqd not found")
            
        # Check /#refs#/bqd
        if '/#refs#/bqd' in f:
            bqd = f['/#refs#/bqd'][()]
            print("bqd shape:", bqd.shape, "sample:", bqd[0, :10])
        else:
            print("bqd not found")
            
        # Check /#refs#/cqd
        if '/#refs#/cqd' in f:
            cqd = f['/#refs#/cqd'][()]
            print("cqd shape:", cqd.shape)
            print("cqd sample references:")
            for idx in range(5):
                ref = cqd[0, idx]
                print(f"  Col {idx}: ref={ref}")
                try:
                    target = f[ref]
                    print(f"    Target name: {target.name}, shape: {target.shape}, dtype: {target.dtype}")
                except Exception as e:
                    print(f"    Error dereferencing: {e}")
        else:
            print("cqd not found")
            
        # Check /#refs#/Dqd
        if '/#refs#/Dqd' in f:
            Dqd = f['/#refs#/Dqd'][()]
            print("Dqd shape:", Dqd.shape, "sample:", Dqd[0, :10])
        else:
            print("Dqd not found")

if __name__ == "__main__":
    trace()
