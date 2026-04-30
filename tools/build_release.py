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
        VERSION = v_data.get("version", "3.0.1")
        channel = v_data.get("channel", "stable")
except Exception:
    VERSION = "3.0.1"
    channel = "stable"

suffix = "-beta" if channel == "beta" else ""
EXE_NAME = f"Audio_Studio_Tycoon_v{VERSION}.exe"
ZIP_NAME = f"Audio_Studio_Tycoon_v{VERSION}{suffix}.zip"

def build():
    os.chdir(APP_DIR)
    
    # Run PyInstaller with PyInstaller one-dir mode
    # --clean:          Löscht alten Build-Cache (verhindert veraltete Dateien)
    # --exclude-module: Entfernt Debug-Module die Windows Defender triggern
    print(f"Running PyInstaller ONE-DIR for {VERSION}...")
    subprocess.run([
        "python", "-m", "PyInstaller", "main.py",
        "--noconfirm",
        "--onedir",
        "--clean",
        "--distpath", "releases",
        "--name", f"Audio_Studio_Tycoon_v{VERSION}",
        "--hidden-import", "urllib.request",
        "--hidden-import", "urllib.error",
        "--exclude-module", "tkinter",
        "--exclude-module", "test",
        "--exclude-module", "unittest",
        "--exclude-module", "distutils",
        "--exclude-module", "pdb",
    ], check=True)
    
    # The output is in releases/Audio_Studio_Tycoon_v2.0/
    base_dist = os.path.join("releases", f"Audio_Studio_Tycoon_v{VERSION}")
    
    # Copy essential files into the directory BEFORE zipping so everything is grouped
    essential_files = ["nvdaControllerClient64.dll", "Tolk.dll", "README.md", "version.json"]
    for f in essential_files:
        if os.path.exists(f):
            dest = os.path.join(base_dist, f)
            shutil.copy2(f, dest)
            
    # Copy assets folder into base_dist
    if os.path.exists("assets"):
        assets_dest = os.path.join(base_dist, "assets")
        if os.path.exists(assets_dest):
            shutil.rmtree(assets_dest)
        shutil.copytree("assets", assets_dest)
        
    print(f"Creating {ZIP_NAME} with _internal folder...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Walk the base_dist and zip everything inside it
        for root, dirs, files in os.walk(base_dist):
            for file in files:
                abs_path = os.path.join(root, file)
                # Ensure the zip structure includes the base package folder but not "dist"
                rel_path = os.path.relpath(abs_path, "releases")
                zf.write(abs_path, rel_path)
                
    print("Build and package completed successfully! Contains _internal folder.")

if __name__ == "__main__":
    build()
