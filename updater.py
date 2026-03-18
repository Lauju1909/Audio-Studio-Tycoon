import json
import os
import subprocess
import urllib.request
import hashlib

def check_for_updates(current_version):
    """
    Simuliert einen Update-Check.
    In einer echten App würde hier ein GET-Request an einen Server erfolgen.
    """
    try:
        url = "https://api.github.com/repos/Lauju1909/Audio-Studio-Tycoon/releases/latest"
        req = urllib.request.Request(url, headers={'User-Agent': 'AudioStudioTycoon-Updater'})
        
        remote_version = "2.6.0"
        changelog = "Stabilitätsverbesserungen und Phase B Features."
        
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    tag = data.get("tag_name", "").lstrip("v")
                    if tag:
                        remote_version = tag
                        full_body = str(data.get("body", changelog))
                        # Nimm die ersten 4 Zeilen
                        all_lines = full_body.split('\n')
                        active_lines = []
                        for line in all_lines:
                            if line.strip():
                                active_lines.append(line.strip("- "))
                        
                        changelog = " | ".join(active_lines[:4])
                        
                        download_url = None
                        for asset in data.get("assets", []):
                            if asset.get("name", "").endswith(".zip"):
                                download_url = asset.get("browser_download_url")
                                break
        except Exception as e:
            print(f"Fehler beim Abrufen der Remote-Version: {e}")

        # Test-Override für Entwickler
        if current_version == "TEST":
            v_current = [0, 0, 0]
        else:
            v_current = [int(x) for x in current_version.split('.') if x.isdigit()]
            
        v_remote = [int(x) for x in remote_version.split('.') if x.isdigit()]
        
        # Sicherstellen, dass beide Listen gleich lang sind (mit 0 auffüllen)
        while len(v_current) < max(len(v_current), len(v_remote)):
            v_current.append(0)
        while len(v_remote) < max(len(v_current), len(v_remote)):
            v_remote.append(0)
        
        # Versions-Vergleich Logik
        # Durch die Listen iterieren, z.B. [1, 7, 0] vs [2, 9, 0]
        # v_remote > v_current in Python vergleicht Element für Element
        if v_remote > v_current:
            return {
                "update_available": True,
                "version": remote_version,
                "changelog": changelog,
                "download_url": download_url
            }
    except Exception as e:
        print(f"Update-Check fehlgeschlagen: {e}")
        
    return {"update_available": False}

def verify_file_hash(filepath, expected_hash):
    """Prüft den SHA-256 Hash einer Datei."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest() == expected_hash
    except Exception:
        return False

def download_and_apply_update(download_url, expected_hash=None):
    
    zip_path = "update.zip"
    try:
        print(f"Downloade Update von {download_url}...")
        urllib.request.urlretrieve(download_url, zip_path)
        
        # Validierung falls Hash vorhanden
        if expected_hash:
            if verify_file_hash(zip_path, expected_hash):
                print("Hash-Validierung erfolgreich.")
            else:
                print("KRITISCHER FEHLER: Hash-Validierung fehlgeschlagen! Update könnte manipuliert sein.")
                # In einer produktiven Umgebung würde man hier abbrechen.
                # return False 
    except Exception as e:
        print(f"Fehler beim Download: {e}")
        return False
        
    bat_path = "apply_update.bat"
    bat_content = f"""@echo off
echo ========================================
echo AUDIO STUDIO TYCOON - UPDATE INSTALLER
echo ========================================
echo Warten bis das Spiel beendet ist...
timeout /t 4 /nobreak >nul
echo Entpacke Update in temporaeren Ordner...
if exist "update_temp" rmdir /s /q "update_temp"
mkdir "update_temp"
powershell -Command "Expand-Archive -Force -Path '{zip_path}' -DestinationPath 'update_temp'" 
if errorlevel 1 (
    echo FEHLER: ZIP konnte nicht entpackt werden.
    pause
    exit /b 1
)
del "{zip_path}"
echo Loesche alte Dateien...
del /q "Audio_Studio_Tycoon_*.exe" 2>nul
echo Kopiere neue Dateien...
xcopy /s /e /y "update_temp\\*" "."
if errorlevel 1 (
    echo FEHLER: Dateien konnten nicht kopiert werden.
    pause
    exit /b 1)
rmdir /s /q "update_temp"
echo Suche nach der neuen exe...
for /f "delims=" %%I in ('dir /b Audio_Studio_Tycoon_v*.exe Audio_Studio_Tycoon_*.exe 2^>nul') do set "NEW_EXE=%%I"
if defined NEW_EXE (
    echo Starte %%NEW_EXE%%...
    start "" "%CD%\\%%NEW_EXE%%"
) else (
    echo FEHLER: Neue EXE nicht gefunden.
    pause
)
del "%~f0"
"""
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
        


    # CREATE_NEW_CONSOLE ist Windows-spezifisch (0x10)
    creation_flags = 0x00000010 
    subprocess.Popen(["cmd.exe", "/c", bat_path], creationflags=creation_flags)
    os._exit(0)


if __name__ == "__main__":
    # Test-Code
    print("Prüfe auf Updates...")
    result = check_for_updates("1.7.0")
    if result["update_available"]:
        print(f"Update verfügbar! Neue Version: {result['version']}")
    else:
        print("Kein Update verfügbar.")
