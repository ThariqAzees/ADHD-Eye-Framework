import h5py
import numpy as np

def inspect_variables():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        # Let's inspect some of the groups in #refs# that have table property keys
        ref_keys = list(f['#refs#'].keys())
        
        print("Searching for table property groups and their variables...")
        for rk in ref_keys:
            obj = f['#refs#'][rk]
            matlab_class = obj.attrs.get('MATLAB_class')
            
            # Table properties usually have a MATLAB_class of 'table' or are a group with properties
            if isinstance(obj, h5py.Group) and 'VariableDescriptions' in obj:
                print(f"\nGroup: {obj.name}")
                print(f"  Keys: {list(obj.keys())}")
                
                # Check DimensionNames
                if 'DimensionNames' in obj:
                    dn = obj['DimensionNames']
                    print(f"  DimensionNames shape: {dn.shape}")
                    for idx, ref in enumerate(dn[:, 0] if dn.ndim == 2 else dn):
                        try:
                            target = f[ref]
                            if target.dtype.kind == 'u' or target.dtype.kind == 'i':
                                text = target[()].tobytes().decode('utf-16')
                            else:
                                text = target[()].tobytes().decode('ascii', errors='ignore')
                            print(f"    Dim {idx}: {repr(text)}")
                        except Exception as e:
                            print(f"    Dim {idx} failed to read: {e}")
                            
                # Check if there is a variable list in the subsystem or refs
                # Sometimes VariableNames or similar is stored inside properties.
                # Let's check all datasets inside this group
                for k in obj.keys():
                    child = obj[k]
                    if isinstance(child, h5py.Dataset):
                        print(f"  Child Dataset '{k}': shape={child.shape}, dtype={child.dtype}")
                        if child.dtype == object and child.size < 100:
                            # Dereference it
                            print(f"    Dereferencing '{k}':")
                            for idx, ref in enumerate(child[()].flatten()):
                                try:
                                    target = f[ref]
                                    if target.attrs.get('MATLAB_class') == b'char':
                                        val = target[()]
                                        text = val.tobytes().decode('utf-16') if val.dtype == 'uint16' else val.tobytes().decode('ascii')
                                        print(f"      Idx {idx}: {repr(text)}")
                                    else:
                                        print(f"      Idx {idx}: name={target.name}, class={target.attrs.get('MATLAB_class')}")
                                except Exception as e:
                                    print(f"      Idx {idx} error: {e}")

if __name__ == "__main__":
    inspect_variables()
