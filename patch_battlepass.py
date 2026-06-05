import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_battlepass = """
    "RES_BATTLE_PASS": "Battle Pass System",
    "RES_BATTLE_PASS_DESC": "Implementiere ein Season-Pass-Modell, um langfristiges Spieler-Engagement zu fördern.",
"""

en_battlepass = """
    "RES_BATTLE_PASS": "Battle Pass System",
    "RES_BATTLE_PASS_DESC": "Implement a season pass model to encourage long-term player engagement.",
"""

if '"RES_BATTLE_PASS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_battlepass)
    content = content.replace('"EN": {', '"EN": {\n' + en_battlepass)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Battle Pass Translations added.")
else:
    print("Battle Pass Translations already exist.")
