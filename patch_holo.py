import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_holo = """
    "RES_HOLO": "Hologramm-Technologie",
    "RES_HOLO_DESC": "Erforsche Projektionen im echten Raum, um physische und virtuelle Realität zu verschmelzen.",
"""

en_holo = """
    "RES_HOLO": "Hologram Technology",
    "RES_HOLO_DESC": "Research real-space projections to merge physical and virtual reality.",
"""

if '"RES_HOLO"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_holo)
    content = content.replace('"EN": {', '"EN": {\n' + en_holo)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Holo Translations added.")
else:
    print("Holo Translations already exist.")
