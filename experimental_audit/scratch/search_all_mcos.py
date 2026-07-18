import h5py
import numpy as np

def search_mcos():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        mcos = f['#subsystem#/MCOS']
        print(f"Total MCOS objects: {mcos.shape[1]}")
        
        # We want to find which MCOS objects represent the variable names list.
        # Let's search for objects that are cell arrays of characters containing the table column names.
        for idx in range(mcos.shape[1]):
            ref = mcos[0, idx]
            try:
                target = f[ref]
                if isinstance(target, h5py.Dataset) and target.dtype == object:
                    # It's a cell array. Let's inspect its elements.
                    # Cell arrays of char usually point to char datasets.
                    chars_found = []
                    for child_ref in target[()].flatten():
                        try:
                            child = f[child_ref]
                            if child.attrs.get('MATLAB_class') == b'char':
                                val = child[()]
                                text = val.tobytes().decode('utf-16') if val.dtype == 'uint16' else val.tobytes().decode('ascii')
                                chars_found.append(text.strip())
                        except:
                            pass
                    
                    if chars_found and any(name in chars_found for name in ['Time', 'Diameter', 'Trial', 'Load', 'Rtime']):
                        print(f"MCOS Index {idx}: name={target.name}, type=cell array")
                        print(f"  Contents: {chars_found}")
            except Exception as e:
                pass

if __name__ == "__main__":
    search_mcos()
