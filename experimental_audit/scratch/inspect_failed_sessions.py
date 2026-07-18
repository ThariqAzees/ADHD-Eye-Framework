import h5py
import numpy as np

def inspect_failed():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        pdata = f['Pupil_data']
        mcos = f['#subsystem#/MCOS']
        
        # Let's inspect sessions 57 to 66
        for idx in range(57, 67):
            print(f"\n================ SESSION {idx} ================")
            
            # Print subject, group, age references
            for key in ['Subject', 'Group', 'Age', 'Task_data', 'Task_epocs']:
                ref = pdata[key][idx, 0]
                print(f"  {key}: ref={ref}, type={type(ref)}")
                try:
                    target = f[ref]
                    print(f"    Target path={target.name}, type={type(target)}")
                    if isinstance(target, h5py.Dataset):
                        print(f"      Shape={target.shape}, Dtype={target.dtype}")
                        if target.dtype != object and target.size < 10:
                            print(f"      Value={target[()]}")
                    elif isinstance(target, h5py.Group):
                        print(f"      Keys={list(target.keys())}")
                        # Print attributes
                        print(f"      Attributes={list(target.attrs.items())}")
                except Exception as e:
                    print(f"    Failed to read/resolve: {e}")

if __name__ == "__main__":
    inspect_failed()
