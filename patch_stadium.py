import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_stadium = """
    "RES_ESPORTS_STADIUMS": "Esports-Stadien",
    "RES_ESPORTS_STADIUMS_DESC": "Errichte gigantische Arenen für internationale Esports-Turniere.",
"""

en_stadium = """
    "RES_ESPORTS_STADIUMS": "Esports Stadiums",
    "RES_ESPORTS_STADIUMS_DESC": "Build gigantic arenas for international esports tournaments.",
"""

if '"RES_ESPORTS_STADIUMS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_stadium)
    content = content.replace('"EN": {', '"EN": {\n' + en_stadium)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Esports Stadiums Translations added.")
else:
    print("Esports Stadiums Translations already exist.")
