"""
Erstellt ein GitHub Release fuer Audio Studio Tycoon.
Benoetigt: pip install requests
Aufruf: python create_release.py v3.6.1
"""
import sys
import json
import os

try:
    import requests
except ImportError:
    print("Installiere requests...")
    os.system("pip install requests -q")
    import requests

VERSION = sys.argv[1] if len(sys.argv) > 1 else "v3.6.1"

# Token aus Umgebungsvariable oder Eingabe
token = os.environ.get("GITHUB_TOKEN", "")
if not token:
    token = input("GitHub Token eingeben: ").strip()

REPO = "Lauju1909/Audio-Studio-Tycoon"
URL = f"https://api.github.com/repos/{REPO}/releases"

data = {
    "tag_name": VERSION,
    "name": f"Audio Studio Tycoon {VERSION} - Sprachausgabe-Fix",
    "body": """## Sprachausgabe-Fix

### Behoben
- Doppelte Sprachausgabe behoben: NVDA/JAWS = nur Tolk, kein Screenreader = nur SAPI
- SAPI COM-Thread-Fehler behoben
- Robuster Fallback: Tolk -> SAPI -> pyttsx3

### Steuerung
- Pfeiltasten: Navigation
- Enter: Auswahl
- Leertaste: Pause
- 1/2/3: Spielgeschwindigkeit
- F: Finanzuebersicht""",
    "draft": False,
    "prerelease": False
}

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

resp = requests.post(URL, json=data, headers=headers)
if resp.status_code == 201:
    print(f"Release erfolgreich erstellt: {resp.json()['html_url']}")
else:
    print(f"Fehler {resp.status_code}: {resp.text}")
