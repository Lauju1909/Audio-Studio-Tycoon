import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_smarthome = """
    "RES_SMART_HOME": "Smart Home Integration",
    "RES_SMART_HOME_DESC": "Erlaube die Verknüpfung des Spiels mit Smart Home Geräten für externe Beleuchtungs- und Soundeffekte.",
"""

en_smarthome = """
    "RES_SMART_HOME": "Smart Home Integration",
    "RES_SMART_HOME_DESC": "Allow linking the game with smart home devices for external lighting and sound effects.",
"""

if '"RES_SMART_HOME"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_smarthome)
    content = content.replace('"EN": {', '"EN": {\n' + en_smarthome)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Smart Home Translations added.")
else:
    print("Smart Home Translations already exist.")
