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
import threading
import urllib.request
import hashlib
from typing import Callable, Optional

GITHUB_API = "https://api.github.com/repos/Lauju1909/Audio-Studio-Tycoon/releases"
UPDATE_TIMEOUT = 10  # Sekunden für den Update-Check


def _parse_version(v_str: str) -> tuple:
    """Wandelt '3.2.0-beta.1' in ([3, 2, 0], tuple) um für korrekten Vergleich."""
    try:
        v_str = v_str.strip().lstrip("v")
        if "-" in v_str:
            core, suffix = v_str.split("-", 1)
        else:
            core = v_str
            suffix = "z_stable"  # Stable ist neuer als beta
            
        parts = [int(x) for x in core.split(".") if x.isdigit()]
        while len(parts) < 3:
            parts.append(0)
            
        suffix_parts = []
        if suffix != "z_stable":
            for part in suffix.split("."):
                if part.isdigit():
                    suffix_parts.append((0, int(part)))
                else:
                    suffix_parts.append((1, part))
        else:
            suffix_parts = [(2, "z_stable")]

        return (tuple(parts), tuple(suffix_parts))
    except Exception:  # pylint: disable=broad-exception-caught
        return ((0, 0, 0), ())


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
    stable = [r for r in releases if not r.get("prerelease", False) and not r.get("draft", False)]
    if not stable:
        return None
    stable.sort(key=lambda r: _parse_version(r.get("tag_name", "0.0.0")), reverse=True)
    return stable[0]


def get_latest_beta_release() -> Optional[dict]:
    """Holt das neueste Beta-Release (prerelease=True, draft=False)."""
    releases = _fetch_releases()
    if not releases:
        return None
    betas = [r for r in releases if r.get("prerelease", False) and not r.get("draft", False)]
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
        if name.endswith(".exe"):
            d_url = asset.get("browser_download_url")
        elif "checksum" in name or "sha256" in name:
            try:
                with urllib.request.urlopen(
                    asset.get("browser_download_url"), timeout=5
                ) as h_res:
                    lines = h_res.read().decode("utf-8").split("\n")
                    e_hash = next(
                        (line.split()[0] for line in lines if ".exe" in line.lower()), None
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
        if channel == "stable":
            release = get_latest_stable_release()
        elif channel == "beta":
            release = get_latest_beta_release()
        else:
            release = None

        if not release:
            return {"update_available": False, "error": "no_release"}

        remote_v = release.get("tag_name", "0.0.0").lstrip("v")
        d_url, e_hash, changelog = _extract_release_info(release)

        v_current = _parse_version("0.0.0" if current_version == "TEST" else current_version)
        v_remote = _parse_version(remote_v)

        if v_remote > v_current and d_url is not None:
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
    Lädt die neue .exe herunter, wendet den .old Trick an und startet neu.
    Kein Entpacken mehr nötig!
    """
    import os, sys, subprocess

    new_exe_name = "update_new.exe"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AST-Updater/3.2"})
        with urllib.request.urlopen(req, timeout=120) as res:
            total = int(res.headers.get("Content-Length", 0))
            downloaded = 0
            last_reported_pct = 0
            with open(new_exe_name, "wb") as f_out:
                while True:
                    chunk = res.read(65536)  # 64 KB Chunks
                    if not chunk:
                        break
                    f_out.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = int((downloaded / total) * 100)
                        if pct >= last_reported_pct + 25:
                            last_reported_pct = (pct // 25) * 25
                            print(f"[Updater] Download-Fortschritt: {last_reported_pct}%")
                        if progress_callback:
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


def _cleanup(path: str):
    """Löscht eine Datei falls vorhanden."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:  # pylint: disable=broad-exception-caught
        pass
