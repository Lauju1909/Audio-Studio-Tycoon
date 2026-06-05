import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_neuro = """
    "RES_NEURO": "Neuro-Gaming",
    "RES_NEURO_DESC": "Entwickle revolutionäre Interfaces für die direkte Verbindung zwischen Gehirn und Spiel.",
"""

en_neuro = """
    "RES_NEURO": "Neuro Gaming",
    "RES_NEURO_DESC": "Develop revolutionary interfaces for direct brain-to-game connection.",
"""

if '"RES_NEURO"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_neuro)
    content = content.replace('"EN": {', '"EN": {\n' + en_neuro)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Neuro Translations added.")
else:
    print("Neuro Translations already exist.")
