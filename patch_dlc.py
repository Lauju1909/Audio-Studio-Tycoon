import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_dlc = """
    "RES_DLC_DEVELOPMENT": "DLC Entwicklung",
    "RES_DLC_DEVELOPMENT_DESC": "Erlaube die Entwicklung von DLCs für existierende Spiele, um deren Lebenszyklus zu verlängern.",
"""

en_dlc = """
    "RES_DLC_DEVELOPMENT": "DLC Development",
    "RES_DLC_DEVELOPMENT_DESC": "Allow development of DLCs for existing games to extend their lifecycle.",
"""

if '"RES_DLC_DEVELOPMENT"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_dlc)
    content = content.replace('"EN": {', '"EN": {\n' + en_dlc)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("DLC Translations added.")
else:
    print("DLC Translations already exist.")
