import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_merch = """
    "RES_MERCHANDISING": "Merchandising",
    "RES_MERCHANDISING_DESC": "Erforsche Merchandising, um physische Fanartikel zu deinen Spielen zu verkaufen.",
"""

en_merch = """
    "RES_MERCHANDISING": "Merchandising",
    "RES_MERCHANDISING_DESC": "Research merchandising to sell physical fan items for your games.",
"""

if '"RES_MERCHANDISING"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_merch)
    content = content.replace('"EN": {', '"EN": {\n' + en_merch)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Merch Translations added.")
else:
    print("Merch Translations already exist.")
