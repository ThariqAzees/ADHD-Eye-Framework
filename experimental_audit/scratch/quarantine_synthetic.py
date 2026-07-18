import os
import shutil

def quarantine():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    archive_dir = os.path.join(base_dir, "data", "synthetic_archive")
    os.makedirs(archive_dir, exist_ok=True)
    
    files_to_quarantine = [
        ("data/raw/Pupil_dataset.mat", "Pupil_dataset_SYNTHETIC.mat"),
        ("data/processed/dataset_features_v1.0.csv", "dataset_features_v1.0_SYNTHETIC.csv"),
        ("data/processed/dataset_features_v1.0_metadata.json", "dataset_features_v1.0_metadata_SYNTHETIC.json"),
        ("ml/models_v1.0.pkl", "models_v1.0_SYNTHETIC.pkl"),
        ("ml/model.pkl", "model_SYNTHETIC.pkl")
    ]
    
    print("Quarantining synthetic files to:", archive_dir)
    for rel_path, dest_name in files_to_quarantine:
        src = os.path.join(base_dir, rel_path)
        dst = os.path.join(archive_dir, dest_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {rel_path} -> {dest_name}")
        else:
            print(f"File not found: {rel_path}")
            
    # Create manifest
    manifest_path = os.path.join(archive_dir, "manifest.txt")
    with open(manifest_path, "w") as f:
        f.write("SYNTHETIC — NOT FOR PUBLICATION RESULTS.\n")
        f.write("=========================================\n")
        f.write("This archive contains the high-fidelity mock/synthetic reference dataset,\n")
        f.write("derived processed features, validation metadata, and trained models.\n")
        f.write("These files were used for testing and pipeline verification, but do not contain\n")
        f.write("genuine clinical recordings. They MUST NOT be used for publication results.\n")
        f.write("Archived on: 2026-07-18\n")
    print("Created manifest at:", manifest_path)

if __name__ == "__main__":
    quarantine()
