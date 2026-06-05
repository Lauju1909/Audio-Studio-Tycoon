import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_mod = """
    "RES_MOD_SUPPORT": "Mod-Support",
    "RES_MOD_SUPPORT_DESC": "Erlaube Spielern, deine Spiele mit eigenen Mods zu erweitern.",
"""

en_mod = """
    "RES_MOD_SUPPORT": "Mod Support",
    "RES_MOD_SUPPORT_DESC": "Allow players to expand your games with their own mods.",
"""

if '"RES_MOD_SUPPORT"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_mod)
    content = content.replace('"EN": {', '"EN": {\n' + en_mod)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Mod-Support Translations added.")
else:
    print("Mod-Support Translations already exist.")
