import os
import zipfile
import json

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
v_path = os.path.join(APP_DIR, "version.json")
try:
    with open(v_path, "r", encoding="utf-8") as f:
        v_data = json.load(f)
        VERSION = v_data.get("version", "3.2.0-beta.1")
except Exception:
    VERSION = "3.2.0-beta.1"

ZIP_NAME = f"Audio_Studio_Tycoon_v{VERSION}_Linux.zip"

# Liste der zu inkludierenden Dateien/Ordner
INCLUDE = [
    "main.py", "audio.py", "logic.py", "models.py", "game_data.py", 
    "translations.py", "competitor_ai.py", "mod_manager.py", "network.py",
    "assets", "menus", "Audio_Studio_Tycoon_Linux.sh", "README.md", "version.json"
]

def create_linux_zip():
    print(f"Erstelle {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item in INCLUDE:
            path = os.path.join(APP_DIR, item)
            if not os.path.exists(path):
                print(f"WARNUNG: {item} nicht gefunden.")
                continue
                
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.pyc') or '__pycache__' in root:
                            continue
                        abs_path = os.path.join(root, file)
                        rel_path = os.path.relpath(abs_path, APP_DIR)
                        zf.write(abs_path, rel_path)
            else:
                zf.write(path, item)
    print("Fertig!")

if __name__ == "__main__":
    create_linux_zip()
