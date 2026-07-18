import h5py
import numpy as np

def trace_relations():
    path = "data/raw/Pupil_dataset.mat"
    with h5py.File(path, 'r') as f:
        mcos = f['#subsystem#/MCOS']
        pdata = f['Pupil_data']
        
        # Let's inspect session 0 (Subject 1)
        print("Session 0 (Subject 1):")
        
        # 1. Subject, Group, Age
        print("Subject ID:", pdata['Subject'][0, 0])
        print("Group:", pdata['Group'][0, 0])
        print("Age:", pdata['Age'][0, 0])
        
        # 2. Task_data reference
        td_ref = pdata['Task_data'][0, 0]
        td_ds = f[td_ref]
        td_val = td_ds[()]
        print("Task_data ref points to dataset:", td_ds.name, "shape:", td_ds.shape, "val:", td_val)
        
        # 3. Task_epocs reference
        te_ref = pdata['Task_epocs'][0, 0]
        te_ds = f[te_ref]
        te_val = te_ds[()]
        print("Task_epocs ref points to dataset:", te_ds.name, "shape:", te_ds.shape, "val:", te_val)
        
        # Wait, if td_val is [[3707764736, 2, 1, 1, 1, 1]], where is the data?
        # Let's search the entire MCOS table to see if there is an object that contains references to '/#refs#/qd'.
        # That is, which MCOS objects contain references to '/#refs#/qd'?
        qd_name = td_ds.name
        print("\nSearching for MCOS objects that point to or are related to", qd_name)
        for idx in range(mcos.shape[1]):
            ref = mcos[0, idx]
            try:
                obj = f[ref]
                # If it's a dataset of references, check if any reference name is qd_name
                if isinstance(obj, h5py.Dataset) and obj.dtype == object:
                    for r in obj[()].flatten():
                        if f[r].name == qd_name:
                            print(f"MCOS Index {idx} ({obj.name}) references {qd_name}")
            except:
                pass

if __name__ == "__main__":
    trace_relations()
