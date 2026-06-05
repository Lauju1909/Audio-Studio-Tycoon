import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_hw = """
    "RES_HARDWARE_DEV": "Hardware-Entwicklung",
    "RES_HARDWARE_DEV_DESC": "Erforsche eigene Spielekonsolen und Controller, um Marktanteile von Plattformbetreibern zu erobern.",
"""

en_hw = """
    "RES_HARDWARE_DEV": "Hardware Development",
    "RES_HARDWARE_DEV_DESC": "Research proprietary game consoles and controllers to capture market share from platform holders.",
"""

if '"RES_HARDWARE_DEV"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_hw)
    content = content.replace('"EN": {', '"EN": {\n' + en_hw)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Hardware Translations added.")
else:
    print("Hardware Translations already exist.")
