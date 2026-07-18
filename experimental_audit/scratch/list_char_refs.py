import h5py

def list_chars():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        print("Finding char datasets...")
        def visitor(name, node):
            if isinstance(node, h5py.Dataset):
                matlab_class = node.attrs.get('MATLAB_class')
                if matlab_class == b'char':
                    try:
                        val = node[()]
                        if val.dtype == 'uint16':
                            text = val.tobytes().decode('utf-16')
                        else:
                            text = val.tobytes().decode('ascii', errors='ignore')
                        # Print if the text is short (variable names/labels)
                        if len(text) < 50:
                            print(f"{name}: {repr(text)}")
                    except Exception as e:
                        pass
        f.visititems(visitor)

if __name__ == "__main__":
    list_chars()
