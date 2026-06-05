import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_crossplay = """
    "RES_CROSSPLAY": "Crossplay",
    "RES_CROSSPLAY_DESC": "Ermögliche Crossplay, damit Spieler plattformübergreifend zusammen spielen können.",
"""

en_crossplay = """
    "RES_CROSSPLAY": "Crossplay",
    "RES_CROSSPLAY_DESC": "Enable crossplay so players can play together across different platforms.",
"""

if '"RES_CROSSPLAY"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_crossplay)
    content = content.replace('"EN": {', '"EN": {\n' + en_crossplay)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Crossplay Translations added.")
else:
    print("Crossplay Translations already exist.")
