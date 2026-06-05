import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_vr = """
    "RES_VR": "Virtuelle Realität (VR)",
    "RES_VR_DESC": "Erforsche VR-Technologien, um immersive Spieleerlebnisse zu kreieren.",
"""

en_vr = """
    "RES_VR": "Virtual Reality (VR)",
    "RES_VR_DESC": "Research VR technologies to create immersive gaming experiences.",
"""

if '"RES_VR"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_vr)
    content = content.replace('"EN": {', '"EN": {\n' + en_vr)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("VR Translations added.")
else:
    print("VR Translations already exist.")
