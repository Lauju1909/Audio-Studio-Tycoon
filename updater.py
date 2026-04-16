"""
Modul für automatische Updates des Spiels.
Überprüft Versionen auf GitHub (NUR Stable-Releases).
Lädt ZIPs herunter und validiert diese via SHA-256.

Release-Kanäle:
  stable → GitHub Release mit prerelease=False (der Updater lädt NUR diesen)
  beta   → GitHub Release mit prerelease=True  (nur für freiwillige Tester)
"""

import json
import os
import subprocess
import urllib.request
import hashlib
import shutil

GITHUB_API = "https://api.github.com/repos/Lauju1909/Audio-Studio-Tycoon/releases"


def _parse_version(v_str):
    """Wandelt '3.0.0' in [3, 0, 0] um."""
    parts = [int(x) for x in v_str.strip().lstrip("v").split(".") if x.isdigit()]
    while len(parts) < 3:
        parts.append(0)
    return parts


def get_latest_stable_release():
    """
    Holt das neueste Stable-Release von GitHub (prerelease=False, draft=False).
    Gibt das Release-Objekt als Dict zurück oder None bei Fehler.
    """
    try:
        # Alle Releases abrufen (nicht nur /latest, das ignoriert Pre-Releases)
        req = urllib.request.Request(
            f"{GITHUB_API}?per_page=20",
            headers={"User-Agent": "AST-Updater"}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            if res.status != 200:
                return None
            releases = json.loads(res.read().decode("utf-8"))

        # Nur Stable-Releases (prerelease=False, draft=False)
        stable = [r for r in releases if not r.get("prerelease", True) and not r.get("draft", True)]
        if not stable:
            return None

        # Höchste Versionsnummer gewinnt (nach semantischer Versionierung sortieren)
        stable.sort(key=lambda r: _parse_version(r.get("tag_name", "0.0.0")), reverse=True)
        return stable[0]

    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"Fehler beim Abrufen der Releases: {err}")
        return None


def get_latest_beta_release():
    """
    Holt das neueste Beta-Release (prerelease=True) von GitHub.
    Gibt das Release-Objekt als Dict zurück oder None.
    """
    try:
        req = urllib.request.Request(
            f"{GITHUB_API}?per_page=20",
            headers={"User-Agent": "AST-Updater"}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            if res.status != 200:
                return None
            releases = json.loads(res.read().decode("utf-8"))

        betas = [r for r in releases if r.get("prerelease", False) and not r.get("draft", True)]
        if not betas:
            return None

        betas.sort(key=lambda r: _parse_version(r.get("tag_name", "0.0.0")), reverse=True)
        return betas[0]

    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"Fehler beim Abrufen der Beta-Releases: {err}")
        return None


def _extract_release_info(release):
    """Extrahiert ZIP-URL, Hash und Changelog aus einem Release-Objekt."""
    if not release:
        return None, None, ""

    changelog = " | ".join([
        l.strip("- ") for l in release.get("body", "").split("\n") if l.strip()
    ][:4])

    d_url, e_hash = None, None
    for asset in release.get("assets", []):
        name = asset.get("name", "")
        if name.endswith(".zip"):
            d_url = asset.get("browser_download_url")
        elif "checksum" in name.lower() or "sha256" in name.lower():
            try:
                with urllib.request.urlopen(asset.get("browser_download_url")) as h_res:
                    lines = h_res.read().decode("utf-8").split("\n")
                    e_hash = next((l.split()[0] for l in lines if ".zip" in l), None)
            except Exception:  # pylint: disable=broad-exception-caught
                pass

    return d_url, e_hash, changelog


def check_for_updates(current_version, channel="stable"):
    """
    Prüft auf Updates.

    Args:
        current_version: Aktuell installierte Version (z.B. '3.0.0').
        channel: 'stable' (Standard) oder 'beta'.
                 Der Updater lädt im Spiel IMMER nur 'stable'.

    Returns:
        Dict mit update_available, version, changelog, download_url, hash
    """
    try:
        if channel == "beta":
            release = get_latest_beta_release()
            # Beta-Check: Wenn keine Beta existiert, auf Stable zurückfallen
            if not release:
                release = get_latest_stable_release()
        else:
            # Standard: NUR Stable
            release = get_latest_stable_release()

        if not release:
            return {"update_available": False}

        rem_v = release.get("tag_name", "0.0.0").lstrip("v")
        d_url, e_hash, changelog = _extract_release_info(release)

        v_c = _parse_version("0.0.0" if current_version == "TEST" else current_version)
        v_r = _parse_version(rem_v)

        if v_r > v_c:
            return {
                "update_available": True,
                "version": rem_v,
                "changelog": changelog,
                "download_url": d_url,
                "hash": e_hash,
                "channel": channel,
                "is_prerelease": release.get("prerelease", False),
            }
        return {"update_available": False}

    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"Update-Check Fehler: {err}")
        return {"update_available": False}


def verify_file_hash(f_path, expected):
    """Validiert SHA-256."""
    sha = hashlib.sha256()
    try:
        with open(f_path, "rb") as f_in:
            for chunk in iter(lambda: f_in.read(4096), b""):
                sha.update(chunk)
        return sha.hexdigest() == expected
    except Exception:  # pylint: disable=broad-exception-caught
        return False


def download_and_apply_update(url, expected):
    """Download und Installation via Batch-Skript."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AST-Updater"})
        with urllib.request.urlopen(req, timeout=60) as res, open("update.zip", "wb") as f:
            shutil.copyfileobj(res, f)

        if expected:
            if not verify_file_hash("update.zip", expected):
                print("Hash-Verifizierung fehlgeschlagen!")
                if os.path.exists("update.zip"):
                    os.remove("update.zip")
                return False
        else:
            print("Warnung: Keine Hash-Verifizierung möglich (Checksum fehlt).")

    except Exception as e:
        print(f"Download-Fehler: {e}")
        if os.path.exists("update.zip"):
            os.remove("update.zip")
        return False

    bat_content = """@echo off
setlocal enabledelayedexpansion
echo Audio Studio Tycoon wird aktualisiert...
timeout /t 5 /nobreak >nul

if exist "temp_update" rmdir /s /q "temp_update"
mkdir "temp_update"

echo Entpacke Dateien...
powershell -Command "Expand-Archive -Force -Path 'update.zip' -DestinationPath 'temp_update'"
del "update.zip"

echo Installiere Updates...
set "SOURCE_DIR=temp_update"
:: Pruefen ob alles in einem Unterordner liegt (typisch fuer Releases)
for /d %%D in ("temp_update\\*") do (
    set "SOURCE_DIR=%%D"
)

xcopy /s /e /y /c "!SOURCE_DIR!\\*" "."
rmdir /s /q "temp_update"

echo Suche neue Programmversion...
set "NEW_EXE=Audio_Studio_Tycoon.exe"
for /f "delims=" %%I in ('dir /b Audio_Studio_Tycoon_v*.exe 2^>nul') do (
    set "NEW_EXE=%%I"
)

echo Starte !NEW_EXE!...
start "" "!NEW_EXE!"
del "%~f0"
"""
    try:
        with open("apply.bat", "w", encoding="utf-8") as f_bat:
            f_bat.write(bat_content)
        subprocess.Popen(["cmd.exe", "/c", "apply.bat"], creationflags=0x10)
        os._exit(0)
    except Exception as e:
        print(f"Fehler beim Starten des Update-Skripts: {e}")
        return False
    return True
