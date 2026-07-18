import os
import urllib.request
import hashlib

DATASET_URL = "https://ndownloader.figshare.com/files/14298953"
EXPECTED_MD5 = "d4a1e92c8e125e93831f12797a783d52"
DEST_PATH = "data/raw/Pupil_dataset.mat"

def download_and_verify():
    os.makedirs(os.path.dirname(DEST_PATH), exist_ok=True)
    
    print(f"Downloading from {DATASET_URL}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(DATASET_URL, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            total_size = int(response.info().get('Content-Length', 0))
            print(f"File size: {total_size / (1024*1024):.2f} MB")
            
            block_size = 1024 * 256  # 256 KB
            downloaded = 0
            
            with open(DEST_PATH, 'wb') as out_file:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    downloaded += len(buffer)
                    out_file.write(buffer)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100.0
                        if int(downloaded / block_size) % 100 == 0 or downloaded == total_size:
                            print(f"Downloaded {percent:.1f}% ({downloaded / (1024*1024):.2f} MB)")
            
            print("Download completed. Verifying MD5 checksum...")
            md5 = hashlib.md5()
            with open(DEST_PATH, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5.update(chunk)
            
            actual_md5 = md5.hexdigest()
            print(f"Actual MD5:   {actual_md5}")
            print(f"Expected MD5: {EXPECTED_MD5}")
            
            if actual_md5 == EXPECTED_MD5:
                print("SUCCESS: MD5 matches! Real clinical dataset successfully recovered.")
            else:
                print("ERROR: MD5 verification failed. The downloaded file might be corrupted.")
                
    except Exception as e:
        print(f"Failed to download dataset: {e}")

if __name__ == "__main__":
    download_and_verify()
