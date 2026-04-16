"""
Prüft ob alle get_text()-Keys aus allen Menü-Dateien in translations.py vorhanden sind.
"""
import re
import os

MENU_FILES = [
    "menus/phase_g.py",
    "menus/gameplay.py",
    "menus/business.py",
    "menus/office.py",
    "menus/research.py",
    "menus/settings.py",
    "menus/system.py",
    "menus/base.py",
    "main.py",
    "logic.py",
    "audio.py",
]

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(base, "translations.py"), encoding="utf-8") as f:
    trans_content = f.read()

all_keys = {}
for filepath in MENU_FILES:
    full = os.path.join(base, filepath)
    if not os.path.exists(full):
        continue
    with open(full, encoding="utf-8") as f:
        content = f.read()
    keys = re.findall(r"get_text\(['\"]([^'\"]+)['\"]", content)
    for k in keys:
        if k not in all_keys:
            all_keys[k] = []
        all_keys[k].append(filepath)

missing = {}
for k, files in all_keys.items():
    # Suche: key kommt in translations vor?
    if f'"{k}"' not in trans_content and f"'{k}'" not in trans_content:
        missing[k] = files

print(f"=== ÜBERSETZUNGS-KEY-CHECK ===")
print(f"Geprüfte Keys: {len(all_keys)}")
print(f"Fehlende Keys: {len(missing)}")
if missing:
    print()
    for k, files in missing.items():
        print(f"  FEHLT: '{k}' (benutzt in: {', '.join(files)})")
else:
    print("Alle Keys vorhanden!")
