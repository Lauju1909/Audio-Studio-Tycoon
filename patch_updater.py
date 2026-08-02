import re, ast

c = open('updater.py', encoding='utf-8').read()

# Change _extract_release_info
extract_replacement = '''
def _extract_release_info(release: dict) -> tuple:
    """Extrahiert (download_url, sha256_hash, changelog) aus einem Release-Objekt."""
    if not release:
        return None, None, ""

    # Changelog: erste 4 Zeilen
    changelog = " | ".join([
        line.strip("- ") for line in release.get("body", "").split("\\n") if line.strip()
    ][:4])

    d_url, e_hash = None, None
    for asset in release.get("assets", []):
        name = asset.get("name", "").lower()
        if name.endswith(".exe"):
            d_url = asset.get("browser_download_url")
        elif "checksum" in name or "sha256" in name:
            try:
                import urllib.request
                with urllib.request.urlopen(
                    asset.get("browser_download_url"), timeout=5
                ) as h_res:
                    lines = h_res.read().decode("utf-8").split("\\n")
                    e_hash = next(
                        (line.split()[0] for line in lines if ".exe" in line.lower()), None
                    )
            except Exception:
                pass

    return d_url, e_hash, changelog
'''
c = re.sub(r'def _extract_release_info\(release: dict\) -> tuple:.*?(?=\ndef check_for_updates)', extract_replacement.strip('\n') + '\n\n', c, flags=re.DOTALL)

# Change download_and_apply_update
download_replacement = '''
def download_and_apply_update(
    url: str,
    expected_hash: Optional[str] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None
) -> bool:
    """
    Lädt das neue .exe herunter, wendet den .old Trick an und startet neu.
    """
    import os, sys, subprocess, urllib.request

    new_exe_name = "update_new.exe"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AST-Updater/3.2"})
        with urllib.request.urlopen(req, timeout=120) as res:
            total = int(res.headers.get("Content-Length", 0))
            downloaded = 0
            with open(new_exe_name, "wb") as f_out:
                while True:
                    chunk = res.read(65536)  # 64 KB Chunks
                    if not chunk:
                        break
                    f_out.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total > 0:
                        progress_callback(downloaded, total)

        print(f"[Updater] Download abgeschlossen: {downloaded:,} Bytes.")

    except Exception as err:
        print(f"[Updater] Download-Fehler: {err}")
        _cleanup(new_exe_name)
        return False

    # SHA-256-Validierung
    if expected_hash:
        if not verify_file_hash(new_exe_name, expected_hash):
            print("[Updater] FEHLER: Hash-Verifizierung fehlgeschlagen!")
            _cleanup(new_exe_name)
            return False
        print("[Updater] Hash-Verifikation erfolgreich.")
    else:
        print("[Updater] Warnung: Keine Checksum verfügbar – Verifizierung übersprungen.")

    print("[Updater] Installiere neues Update...")
    is_frozen = getattr(sys, "frozen", False)
    
    if is_frozen:
        exe_path = sys.executable
        old_path = exe_path + ".old"
        
        # Alte .old entfernen
        if os.path.exists(old_path):
            try: os.remove(old_path)
            except Exception: pass
            
        # Aktuelle exe umbenennen
        os.rename(exe_path, old_path)
        
        # Neue exe an den Platz der alten setzen
        os.rename(new_exe_name, exe_path)
        new_exe = exe_path
    else:
        # Running as python script, just use the new exe
        new_exe = "Audio_Studio_Tycoon.exe"
        if os.path.exists(new_exe):
            try: os.remove(new_exe)
            except Exception: pass
        os.rename(new_exe_name, new_exe)

    print("[Updater] Update abgeschlossen! Starte neu...")
    subprocess.Popen([new_exe])
    os._exit(0)
    return True
'''
c = re.sub(r'def download_and_apply_update\([^)]*\)\s*->\s*bool:.*?(?=\ndef _cleanup)', download_replacement.strip('\n') + '\n\n', c, flags=re.DOTALL)

open('updater.py', 'w', encoding='utf-8').write(c)
ast.parse(c)
