import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_retro = """
    "RES_RETRO": "Retro-Konsolen",
    "RES_RETRO_DESC": "Erforsche Retro-Gaming, um ältere Spiele als Remaster neu aufzulegen.",
"""

en_retro = """
    "RES_RETRO": "Retro Consoles",
    "RES_RETRO_DESC": "Research retro gaming to re-release older games as remasters.",
"""

if '"RES_RETRO"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_retro)
    content = content.replace('"EN": {', '"EN": {\n' + en_retro)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Retro Consoles Translations added.")
else:
    print("Retro Consoles Translations already exist.")
