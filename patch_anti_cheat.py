import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_cheat = """
    "RES_ANTI_CHEAT": "Anti-Cheat Systeme",
    "RES_ANTI_CHEAT_DESC": "Entwickle starke Anti-Cheat Software für faire Multiplayer-Umgebungen.",
"""

en_cheat = """
    "RES_ANTI_CHEAT": "Anti-Cheat Systems",
    "RES_ANTI_CHEAT_DESC": "Develop strong anti-cheat software for fair multiplayer environments.",
"""

if '"RES_ANTI_CHEAT"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_cheat)
    content = content.replace('"EN": {', '"EN": {\n' + en_cheat)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Anti-Cheat Translations added.")
else:
    print("Anti-Cheat Translations already exist.")
