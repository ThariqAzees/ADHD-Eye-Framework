import h5py
import numpy as np

def inspect_nested_hdf5():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        pdata = f['Pupil_data']
        
        # Let's inspect Task_data at index 0
        ref_obj = pdata['Task_data'][0, 0]
        print(f"pdata['Task_data'][0, 0] raw ref type: {type(ref_obj)}")
        
        target = f[ref_obj]
        print(f"Target dataset: shape={target.shape}, dtype={target.dtype}")
        
        # In MATLAB, structure arrays or cell arrays are often stored in #refs# or inside subsystem.
        # Let's look at the actual elements of this target dataset.
        # It has shape (1, 6) or similar. Let's see if we can dereference them.
        for idx in range(target.shape[1]):
            val = target[0, idx]
            print(f"  Col {idx}: value={val}, type={type(val)}")
            # Try to resolve if it is a reference
            try:
                # We can construct a reference using h5py.h5r.Reference or simply passing the val if it's a ref.
                # In h5py, object references can be resolved by passing the h5py.Reference object.
                # If it's a uint32, it might be a region reference or object reference ID.
                # Let's check if the value is in f or if we can use f.id.get_name_by_addr(val)
                # Actually, in h5py, f[ref] can take an address (integer) directly!
                # Let's try to resolve it.
                addr = val
                # addr in h5py is the byte address of the object in the file
                # In h5py v3+, we can resolve address using f.id.get_name_by_addr(addr) or f[addr]
                name = f.id.get_name_by_addr(addr)
                print(f"    Resolved name: {name}")
                obj = f[name]
                print(f"    Object type: {type(obj)}")
                if isinstance(obj, h5py.Dataset):
                    print(f"    Shape: {obj.shape}, Dtype: {obj.dtype}")
                    if obj.size < 50:
                        print(f"    Data: {obj[()]}")
                elif isinstance(obj, h5py.Group):
                    print(f"    Keys: {list(obj.keys())}")
            except Exception as e:
                print(f"    Failed to resolve address {val}: {e}")

if __name__ == "__main__":
    inspect_nested_hdf5()
