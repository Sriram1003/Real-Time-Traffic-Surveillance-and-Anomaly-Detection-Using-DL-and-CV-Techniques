import shutil
import pathlib
import os

# 1. Find the hidden cache directory on your specific computer
user_home = pathlib.Path.home()
cache_path = user_home / ".cache" / "torch" / "hub"
target_folder = cache_path / "WongKinYiu_yolov7_main"

print(f"Looking for corrupted cache at: {target_folder}")

# 2. Force Delete it
if target_folder.exists():
    try:
        shutil.rmtree(target_folder)
        print("\n✅ SUCCESS: Corrupted YOLOv7 files have been deleted!")
        print("Now restart your server, and it will download fresh, clean files.")
    except Exception as e:
        print(f"\n❌ ERROR: Could not delete folder. Reason: {e}")
        print("Try closing VS Code and running this terminal as Administrator.")
else:
    print("\n⚠️ Folder not found. It might have been deleted already, or the path is different.")
    print(f"Check manually in: {cache_path}")