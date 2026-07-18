import h5py

def trace_classes():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        # Let's inspect the first few items in #refs# to see if they represent fields
        print("Tracing HDF5 #refs# objects...")
        
        # Let's look at the first object reference in Pupil_data/Task_data
        pdata = f['Pupil_data']
        first_ref = pdata['Task_data'][0, 0]
        
        # Resolve target
        target = f[first_ref]
        print(f"Target object name: {target.name}")
        print("Target attributes:")
        for attr_k in target.attrs.keys():
            print(f"  {attr_k}: {target.attrs[attr_k]}")
            
        # Let's look at #refs# keys
        ref_keys = list(f['#refs#'].keys())
        print(f"Total objects in #refs#: {len(ref_keys)}")
        
        # Print attributes of a few objects in #refs# to find where structures are
        count = 0
        for rk in ref_keys[:50]:
            obj = f['#refs#'][rk]
            # Check if it has attributes that identify it as a MATLAB class or struct
            matlab_class = obj.attrs.get('MATLAB_class')
            if matlab_class:
                print(f"Object {rk}: MATLAB_class = {matlab_class}, type = {type(obj)}")
                if isinstance(obj, h5py.Group):
                    print(f"  Keys: {list(obj.keys())}")
                elif isinstance(obj, h5py.Dataset):
                    print(f"  Shape: {obj.shape}, Dtype: {obj.dtype}")
                count += 1
                if count >= 10:
                    break

if __name__ == "__main__":
    trace_classes()
