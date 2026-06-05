import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_soundtrack = """
    "RES_SOUNDTRACK": "Soundtrack-Vertrieb",
    "RES_SOUNDTRACK_DESC": "Verkaufe die Musik deiner Spiele separat, um zusätzliche Einnahmen zu generieren.",
"""

en_soundtrack = """
    "RES_SOUNDTRACK": "Soundtrack Distribution",
    "RES_SOUNDTRACK_DESC": "Sell your game music separately to generate additional revenue.",
"""

if '"RES_SOUNDTRACK"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_soundtrack)
    content = content.replace('"EN": {', '"EN": {\n' + en_soundtrack)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Soundtrack Translations added.")
else:
    print("Soundtrack Translations already exist.")
