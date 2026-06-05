import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_mocap = """
    "RES_MOCAP": "Motion Capturing Studio",
    "RES_MOCAP_DESC": "Erforsche MoCap-Technologien, um lebensechte Animationen für deine AAA-Titel zu erstellen.",
"""

en_mocap = """
    "RES_MOCAP": "Motion Capturing Studio",
    "RES_MOCAP_DESC": "Research MoCap technologies to create lifelike animations for your AAA titles.",
"""

if '"RES_MOCAP"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_mocap)
    content = content.replace('"EN": {', '"EN": {\n' + en_mocap)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("MoCap Translations added.")
else:
    print("MoCap Translations already exist.")
