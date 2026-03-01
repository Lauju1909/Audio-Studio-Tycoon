import os
import shutil
import subprocess
import zipfile

VERSION = "v2.0"
EXE_NAME = f"Audio_Studio_Tycoon_{VERSION}.exe"
ZIP_NAME = f"Audio_Studio_Tycoon_{VERSION}.zip"
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def build():
    os.chdir(APP_DIR)
    
    # Run PyInstaller
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Audio_Studio_Tycoon_{VERSION}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    spec_file = f"Audio_Studio_Tycoon_{VERSION}.spec"
    with open(spec_file, "w") as f:
        f.write(spec_content)
        
    print(f"Running PyInstaller for {VERSION}...")
    subprocess.run(["pyinstaller", spec_file, "--noconfirm"], check=True)
    
    print(f"Creating {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add exe
        exe_path = os.path.join("dist", EXE_NAME)
        if os.path.exists(exe_path):
            zf.write(exe_path, EXE_NAME)
        else:
            raise Exception(f"EXE not found at {exe_path}")
            
        # Add DLLs and Readme
        zf.write("nvdaControllerClient64.dll", "nvdaControllerClient64.dll")
        zf.write("Tolk.dll", "Tolk.dll")
        zf.write("README.md", "README.md")
        
        # Add assets
        for root, _, files in os.walk("assets"):
            for file in files:
                file_path = os.path.join(root, file)
                zf.write(file_path, file_path)
                
    print("Build and package completed successfully!")

if __name__ == "__main__":
    build()
