import os
import shutil
import subprocess
import zipfile
import json

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
v_path = os.path.join(APP_DIR, "version.json")
try:
    with open(v_path, "r", encoding="utf-8") as f:
        v_data = json.load(f)
        VERSION = v_data.get("version", "1.0.0")
except Exception:
    VERSION = "1.0.0"

EXE_NAME = f"Audio_Studio_Tycoon_v{VERSION}.exe"
ZIP_NAME = f"Audio_Studio_Tycoon_v{VERSION}.zip"
DIST_DIR = os.path.join(APP_DIR, "dist")
BUILD_DIR = os.path.join(APP_DIR, "releases")

def build():
    os.chdir(APP_DIR)
    
    # Run PyInstaller with PyInstaller one-file mode to produce Audio_Studio_Tycoon_v[Version].exe
    print(f"Running PyInstaller for {VERSION}...")
    subprocess.run([
        "python", "-m", "PyInstaller", "main.py", "--noconfirm", "--onefile",
        "--name", f"Audio_Studio_Tycoon_v{VERSION}",
        "--hidden-import", "urllib.request",
        "--hidden-import", "urllib.error"
    ], check=True)
    
    # Ensure releases directory exists
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)
        
    zip_path = os.path.join(BUILD_DIR, ZIP_NAME)
    print(f"Creating {zip_path}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add exe
        exe_path = os.path.join(DIST_DIR, EXE_NAME)
        root_folder = f"Audio_Studio_Tycoon_v{VERSION}"
        if os.path.exists(exe_path):
            zf.write(exe_path, f"{root_folder}/{EXE_NAME}")
        else:
            raise Exception(f"EXE not found at {exe_path}")
            
        # Add essential files
        essential_files = ["nvdaControllerClient64.dll", "Tolk.dll", "README.md", "version.json"]
        for f in essential_files:
            if os.path.exists(f):
                zf.write(f, f"{root_folder}/{f}")
        
        # Add assets
        if os.path.exists("assets"):
            for root, _, files in os.walk("assets"):
                for file in files:
                    file_path = os.path.join(root, file)
                    zf.write(file_path, f"{root_folder}/{file_path}")
                    
    print(f"Build and package completed successfully! ({zip_path})")

if __name__ == "__main__":
    build()
