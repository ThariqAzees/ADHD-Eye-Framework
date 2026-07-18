import os
from pymatreader import read_mat
import numpy as np

def inspect_mat():
    path = "data/raw/Pupil_dataset.mat"
    print("Loading MAT file...")
    data = read_mat(path)
    print("Top level keys:", list(data.keys()))
    
    if "Pupil_data" in data:
        pdata = data["Pupil_data"]
        print("Type of Pupil_data:", type(pdata))
        if isinstance(pdata, dict):
            print("Pupil_data keys:", list(pdata.keys()))
            for k in pdata.keys():
                val = pdata[k]
                print(f"\nKey: {k}")
                print(f"  Type: {type(val)}")
                if isinstance(val, list):
                    print(f"  Length: {len(val)}")
                    if len(val) > 0:
                        print(f"  First element type: {type(val[0])}")
                        if isinstance(val[0], dict):
                            print(f"  First element keys: {list(val[0].keys())}")
                        elif isinstance(val[0], np.ndarray):
                            print(f"  First element shape: {val[0].shape}, dtype: {val[0].dtype}")
                            # Print a sample value
                            print(f"  First element sample: {val[0][:5]}")
                        else:
                            print(f"  First element value: {val[0]}")
                elif isinstance(val, np.ndarray):
                    print(f"  Shape: {val.shape}, dtype: {val.dtype}")
                    print(f"  Sample: {val[:5]}")
                else:
                    print(f"  Value: {val}")

if __name__ == "__main__":
    inspect_mat()
