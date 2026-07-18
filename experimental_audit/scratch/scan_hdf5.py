import h5py

def scan():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        print("Traversing HDF5 groups...")
        
        def visitor(name, node):
            if isinstance(node, h5py.Dataset):
                # Print datasets that are not inside #refs# or print a few inside #refs#
                if not name.startswith('#refs#') or 'qd' in name or 'Task_data' in name:
                    print(f"Dataset: {name}, Shape: {node.shape}, Dtype: {node.dtype}")
                    if len(node.attrs) > 0:
                        print("  Attributes:")
                        for k, v in node.attrs.items():
                            print(f"    {k}: {v}")
            elif isinstance(node, h5py.Group):
                if not name.startswith('#refs#') or 'qd' in name:
                    print(f"Group: {name}")
                    if len(node.attrs) > 0:
                        print("  Attributes:")
                        for k, v in node.attrs.items():
                            print(f"    {k}: {v}")
                            
        f.visititems(visitor)

if __name__ == "__main__":
    scan()
