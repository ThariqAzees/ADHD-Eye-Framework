import hdf5storage

def try_hdf5storage():
    path = "data/raw/Pupil_dataset.mat"
    print("Loading MAT file with hdf5storage...")
    try:
        data = hdf5storage.loadmat(path)
        print("Root level keys:", list(data.keys()))
        if "Pupil_data" in data:
            pdata = data["Pupil_data"]
            print("Pupil_data keys:", pdata.dtype.names if hasattr(pdata, 'dtype') else 'No names')
            
            # If it's a structured numpy array
            print("Pupil_data shape:", pdata.shape)
            print("First item Subject:", pdata[0, 0]['Subject'])
            print("First item Group:", pdata[0, 0]['Group'])
            print("First item Age:", pdata[0, 0]['Age'])
            
            # Let's inspect Task_epocs at index 0
            tepoc = pdata[0, 0]['Task_epocs']
            print("\nTask_epocs type:", type(tepoc))
            if hasattr(tepoc, 'dtype'):
                print("Task_epocs field names:", tepoc.dtype.names)
                print("Task_epocs shape:", tepoc.shape)
            else:
                print("Task_epocs value:", tepoc)
                
            # Let's inspect Task_data at index 0
            tdata = pdata[0, 0]['Task_data']
            print("\nTask_data type:", type(tdata))
            if hasattr(tdata, 'dtype'):
                print("Task_data field names:", tdata.dtype.names)
                print("Task_data shape:", tdata.shape)
            else:
                print("Task_data value:", tdata)
    except Exception as e:
        print("Failed to load hdf5storage:", e)

if __name__ == "__main__":
    try_hdf5storage()
