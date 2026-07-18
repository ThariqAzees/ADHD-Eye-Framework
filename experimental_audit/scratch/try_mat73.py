import mat73

def try_mat73():
    path = "data/raw/Pupil_dataset.mat"
    print("Loading MAT file with mat73...")
    try:
        data = mat73.loadmat(path)
        print("Root level keys:", list(data.keys()))
        if "Pupil_data" in data:
            pdata = data["Pupil_data"]
            print("Pupil_data type:", type(pdata))
            if isinstance(pdata, dict):
                print("Pupil_data keys:", list(pdata.keys()))
                
                # Check subject at index 0
                print("\nInspecting first session (index 0):")
                print("Subject:", pdata["Subject"][0])
                print("Group:", pdata["Group"][0])
                print("Age:", pdata["Age"][0])
                
                # Check Task_epocs
                tepoc = pdata["Task_epocs"]
                print("Type of Task_epocs:", type(tepoc))
                if isinstance(tepoc, list):
                    print("Task_epocs length:", len(tepoc))
                    print("Type of first element:", type(tepoc[0]))
                    if isinstance(tepoc[0], dict):
                        print("Keys of first element:", list(tepoc[0].keys()))
                
                # Check Task_data
                tdata = pdata["Task_data"]
                print("Type of Task_data:", type(tdata))
                if isinstance(tdata, list):
                    print("Task_data length:", len(tdata))
                    print("Type of first element:", type(tdata[0]))
                    if isinstance(tdata[0], dict):
                        print("Keys of first element:", list(tdata[0].keys()))
    except Exception as e:
        print("Failed to load mat73:", e)

if __name__ == "__main__":
    try_mat73()
