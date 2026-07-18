import h5py
import numpy as np

def verify_layout():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        m = f['#subsystem#/MCOS']
        print(f"Total MCOS size: {m.shape[1]}")
        
        # Let's inspect the repeating block structure.
        # We'll print the first 3 blocks (indices 0 to 20) and their properties.
        for block_idx in range(4):
            print(f"\n--- Block {block_idx} (Indices {block_idx*7} to {block_idx*7 + 6}) ---")
            for offset in range(7):
                idx = block_idx * 7 + offset
                ref = m[0, idx]
                try:
                    obj = f[ref]
                    name = obj.name.split('/')[-1]
                    mclass = obj.attrs.get('MATLAB_class', b'none').decode('ascii')
                    shape = getattr(obj, 'shape', 'No shape')
                    
                    # Inspect contents
                    content = ""
                    if isinstance(obj, h5py.Dataset):
                        if obj.dtype == object:
                            # Cell array of references
                            refs_list = []
                            for r in obj[()].flatten():
                                if r:
                                    try:
                                        target = f[r]
                                        tname = target.name.split('/')[-1]
                                        tclass = target.attrs.get('MATLAB_class', b'none').decode('ascii')
                                        if tclass == 'char':
                                            val = target[()]
                                            text = val.tobytes().decode('utf-16') if val.dtype == 'uint16' else val.tobytes().decode('ascii')
                                            refs_list.append(f"{tname}('Char:{text.strip()}')")
                                        else:
                                            refs_list.append(f"{tname}({tclass}:{getattr(target, 'shape', '')})")
                                    except:
                                        refs_list.append("error")
                                else:
                                    refs_list.append("empty")
                            content = f"cells: {refs_list}"
                        elif obj.dtype.kind in 'uif':
                            if obj.size < 10:
                                content = f"val: {obj[()].flatten()}"
                            else:
                                content = f"val shape {obj.shape}"
                    print(f"  Idx {idx} ({name}): class={mclass}, shape={shape}, {content}")
                except Exception as e:
                    print(f"  Idx {idx} failed to read: {e}")

if __name__ == "__main__":
    verify_layout()
