# ruff: noqa
import os
import shutil
import subprocess
import json
from datetime import datetime

VERSION = "2.2.1"
VERSION_STR = "2.2.1"
EXE_NAME = f"Audio_Studio_Tycoon_v{VERSION}"
ZIP_NAME = f"Audio_Studio_Tycoon_v{VERSION}.zip"
SPEC_FILE = "Audio_Studio_Tycoon_v2.2.1.spec"

print(f"=== Audio Studio Tycoon - Release {VERSION_STR} ===")

CHANGELOG = """
=== Audio Studio Tycoon v2.2.1 - Historisches Bugfix Release ===

Fehlerbehebungen:
- Fix: UnboundLocalError bei Jahreswechsel (week_in_year).
- Fix: Rivalen-Score skaliert jetzt korrekt ab 1930 (vorher direkter Max-Boost).
- Fix: Game of the Year (GOTY) filtert jetzt präzise nach dem Veröffentlichungsjahr (Rivalen & Spieler).

Features (aus v2.2.0):
- Vollständige historische Plattformen (1930-2026) von Abakus bis Neural-Box.
- 50+ historische Engine-Features mit Beschreibungen und Unlock-Jahren.
- 35+ historische Jahresevents mit Marktauswirkungen.
- Gesperrte Themen im Menü sichtbar (mit Jahreszahl).
- Start 1930 mit passenden Themen und Willkommens-E-Mail.
"""

# Update version.json
print("Updating version.json...")
version_data = {
    "version": VERSION_STR,
    "last_update": datetime.now().strftime("%Y-%m-%d"),
    "changelog": CHANGELOG
}
with open("version.json", "w", encoding="utf-8") as f:
    json.dump(version_data, f, indent=4, ensure_ascii=False)

# Clean previous build
print("Cleaning old build folders...")
for folder in ["build", f"dist/{EXE_NAME}"]:
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
        # Fallback falls ignore_errors=True den Ordner nur leer macht statt löschen
        try:
            if os.path.exists(folder):
                os.rmdir(folder)
        except Exception:
            pass

# Run pyinstaller
print("Running PyInstaller...")
try:
    subprocess.run(["pyinstaller", "-y", "--clean", SPEC_FILE], check=True)
except subprocess.CalledProcessError:
    print("PyInstaller failed.")
    exit(1)

# Package into zip file
print(f"Packaging {ZIP_NAME}...")
dist_dir = os.path.join("dist", EXE_NAME)
internal_dir = os.path.join(dist_dir, "_internal")

if os.path.exists("version.json"):
    shutil.copy("version.json", dist_dir)


# Pack everything within the folder:
# Resulting zip should contain Audio_Studio_Tycoon_v2.0.exe and _internal inside the root of the zip.
# Wait, the rule says:
# "Audio_Studio_Tycoon_v[Versionsnummer].zip"
import zipfile
with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            # Make the path relative to the dist_dir so exe and _internal are at the root
            rel_path = os.path.relpath(abs_path, dist_dir)
            zf.write(abs_path, rel_path)

print(f"\nDone! Created {ZIP_NAME} successfully.")
