"""
Modul für automatische Updates des Spiels.
Überprüft Versionen auf GitHub (Stable UND Beta).
Lädt ZIPs herunter, validiert via SHA-256 und installiert via Batch-Skript.

Release-Kanäle:
  stable → GitHub Release mit prerelease=False
  beta   → GitHub Release mit prerelease=True
"""

import json
import os
import subprocess
import threading
import urllib.request
import hashlib
import shutil
from typing import Callable, Optional

GITHUB_API = "https://api.github.com/repos/Lauju1909/Audio-Studio-Tycoon/releases"
UPDATE_TIMEOUT = 10  # Sekunden für den Update-Check


def _parse_version(v_str: str) -> list:
    """Wandelt '3.2.0-beta.1' in [3, 2, 0] um (ignoriert Suffix)."""
    try:
        core = v_str.strip().lstrip("v").split("-")[0]
        parts = [int(x) for x in core.split(".") if x.isdigit()]
        while len(parts) < 3:
            parts.append(0)
        return parts
    except Exception:  # pylint: disable=broad-exception-caught
        return [0, 0, 0]


def _fetch_releases(timeout: int = UPDATE_TIMEOUT) -> Optional[list]:
    """Holt alle Releases von der GitHub API. Gibt None bei Fehler zurück."""
    try:
        req = urllib.request.Request(
            f"{GITHUB_API}?per_page=30",
            headers={"User-Agent": "AST-Updater/3.2"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as res:
            if res.status != 200:
                return None
            return json.loads(res.read().decode("utf-8"))
    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"[Updater] GitHub-Fehler: {err}")
        return None


def get_latest_stable_release() -> Optional[dict]:
    """Holt das neueste Stable-Release (prerelease=False, draft=False)."""
    releases = _fetch_releases()
    if not releases:
        return None
    stable = [r for r in releases if not r.get("prerelease", True) and not r.get("draft", True)]
    if not stable:
        return None
    stable.sort(key=lambda r: _parse_version(r.get("tag_name", "0.0.0")), reverse=True)
    return stable[0]


def get_latest_beta_release() -> Optional[dict]:
    """Holt das neueste Beta-Release (prerelease=True, draft=False)."""
    releases = _fetch_releases()
    if not releases:
        return None
    betas = [r for r in releases if r.get("prerelease", False) and not r.get("draft", True)]
    if not betas:
        return None
    betas.sort(key=lambda r: _parse_version(r.get("tag_name", "0.0.0")), reverse=True)
    return betas[0]


def _extract_release_info(release: dict) -> tuple:
    """Extrahiert (download_url, sha256_hash, changelog) aus einem Release-Objekt."""
    if not release:
        return None, None, ""

    # Changelog: erste 4 Zeilen
    changelog = " | ".join([
        line.strip("- ") for line in release.get("body", "").split("\n") if line.strip()
    ][:4])

    d_url, e_hash = None, None
    for asset in release.get("assets", []):
        name = asset.get("name", "").lower()
        if name.endswith(".zip"):
            d_url = asset.get("browser_download_url")
        elif "checksum" in name or "sha256" in name:
            try:
                with urllib.request.urlopen(
                    asset.get("browser_download_url"), timeout=5
                ) as h_res:
                    lines = h_res.read().decode("utf-8").split("\n")
                    e_hash = next(
                        (line.split()[0] for line in lines if ".zip" in line.lower()), None
                    )
            except Exception:  # pylint: disable=broad-exception-caught
                pass

    return d_url, e_hash, changelog


def check_for_updates(current_version: str, channel: str = "stable") -> dict:
    """
    Prüft auf Updates.

    Args:
        current_version: Aktuelle Version (z.B. '3.2.0-beta.1').
        channel: 'stable' oder 'beta'.

    Returns:
        Dict mit: update_available, version, changelog, download_url, hash, channel
    """
    try:
        if channel == "beta":
            release = get_latest_beta_release() or get_latest_stable_release()
        else:
            release = get_latest_stable_release()

        if not release:
            return {"update_available": False, "error": "no_release"}

        remote_v = release.get("tag_name", "0.0.0").lstrip("v")
        d_url, e_hash, changelog = _extract_release_info(release)

        v_current = _parse_version("0.0.0" if current_version == "TEST" else current_version)
        v_remote = _parse_version(remote_v)

        if v_remote > v_current:
            return {
                "update_available": True,
                "version": remote_v,
                "changelog": changelog,
                "download_url": d_url,
                "hash": e_hash,
                "channel": channel,
                "is_prerelease": release.get("prerelease", False),
            }
        return {"update_available": False}

    except Exception as err:  # pylint: disable=broad-exception-caught
        print(f"[Updater] Update-Check Fehler: {err}")
        return {"update_available": False, "error": str(err)}


def check_for_updates_async(
    current_version: str,
    channel: str = "stable",
    on_result: Optional[Callable[[dict], None]] = None
) -> threading.Thread:
    """
    Asynchroner Update-Check – blockiert das Spiel nicht.

    Args:
        current_version: Aktuelle Spielversion.
        channel: 'stable' oder 'beta'.
        on_result: Callback-Funktion, die mit dem Ergebnis aufgerufen wird.

    Returns:
        Das Thread-Objekt (bereits gestartet).
    """
    def _worker():
        result = check_for_updates(current_version, channel)
        if on_result:
            on_result(result)

    t = threading.Thread(target=_worker, daemon=True, name="AST-UpdateCheck")
    t.start()
    return t


def verify_file_hash(f_path: str, expected: str) -> bool:
    """Validiert SHA-256-Hash einer Datei."""
    sha = hashlib.sha256()
    try:
        with open(f_path, "rb") as f_in:
            for chunk in iter(lambda: f_in.read(8192), b""):
                sha.update(chunk)
        return sha.hexdigest().lower() == expected.lower()
    except Exception:  # pylint: disable=broad-exception-caught
        return False


def download_and_apply_update(
    url: str,
    expected_hash: Optional[str] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None
) -> bool:
    """
    Lädt das Update-ZIP herunter, validiert es und startet das Batch-Install-Skript.

    Args:
        url: Download-URL des ZIPs.
        expected_hash: Erwarteter SHA-256-Hash (oder None um Überprüfung zu überspringen).
        progress_callback: Optional fn(bytes_done, bytes_total) für Fortschrittsanzeige.

    Returns:
        True wenn erfolgreich gestartet, False bei Fehler.
    """
    zip_path = "update.zip"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AST-Updater/3.2"})
        with urllib.request.urlopen(req, timeout=120) as res:
            total = int(res.headers.get("Content-Length", 0))
            downloaded = 0
            with open(zip_path, "wb") as f_out:
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
        _cleanup(zip_path)
        return False

    # SHA-256-Validierung
    if expected_hash:
        if not verify_file_hash(zip_path, expected_hash):
            print("[Updater] FEHLER: Hash-Verifizierung fehlgeschlagen!")
            _cleanup(zip_path)
            return False
        print("[Updater] Hash-Verifikation erfolgreich.")
    else:
        print("[Updater] Warnung: Keine Checksum verfügbar – Verifizierung übersprungen.")

    # Batch-Skript schreiben und starten
    bat_content = r"""@echo off
setlocal enabledelayedexpansion
title Audio Studio Tycoon - Update
echo =============================================
echo   Audio Studio Tycoon - Automatisches Update
echo =============================================
echo.
echo Warte auf Spielende...
timeout /t 3 /nobreak >nul

if exist "temp_update" rmdir /s /q "temp_update"
mkdir "temp_update"

echo Entpacke Update...
powershell -Command "Expand-Archive -Force -Path 'update.zip' -DestinationPath 'temp_update'"
if errorlevel 1 (
    echo FEHLER: Entpacken fehlgeschlagen!
    pause
    exit /b 1
)
del "update.zip"

echo Installiere Dateien...
set "SOURCE_DIR=temp_update"
for /d %%D in ("temp_update\*") do (
    if exist "%%D\main.py" set "SOURCE_DIR=%%D"
    if exist "%%D\Audio_Studio_Tycoon.exe" set "SOURCE_DIR=%%D"
)

xcopy /s /e /y /c "!SOURCE_DIR!\*" "."
rmdir /s /q "temp_update"

echo.
echo Update abgeschlossen! Starte Spiel...
set "NEW_EXE=main.py"
for /f "delims=" %%I in ('dir /b Audio_Studio_Tycoon_v*.exe 2^>nul') do (
    set "NEW_EXE=%%I"
)

if "!NEW_EXE!" == "main.py" (
    start "" python main.py
) else (
    start "" "!NEW_EXE!"
)
del "%~f0"
"""
    try:
        with open("apply_update.bat", "w", encoding="cp1252") as f_bat:
            f_bat.write(bat_content)
        subprocess.Popen(
            ["cmd.exe", "/c", "apply_update.bat"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        os._exit(0)  # Sofortiger Spielabbruch für den Update-Prozess
    except Exception as err:
        print(f"[Updater] Fehler beim Starten des Update-Skripts: {err}")
        return False
    return True


def _cleanup(path: str):
    """Löscht eine Datei falls vorhanden."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:  # pylint: disable=broad-exception-caught
        pass
