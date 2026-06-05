import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_cloud_saves = """
    "RES_CLOUD_SAVES": "Cloud-Saves",
    "RES_CLOUD_SAVES_DESC": "Biete Cloud-Speicherung an, damit Spieler ihre Fortschritte überall abrufen können.",
"""

en_cloud_saves = """
    "RES_CLOUD_SAVES": "Cloud Saves",
    "RES_CLOUD_SAVES_DESC": "Offer cloud saves so players can access their progress anywhere.",
"""

if '"RES_CLOUD_SAVES"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_cloud_saves)
    content = content.replace('"EN": {', '"EN": {\n' + en_cloud_saves)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Cloud Saves Translations added.")
else:
    print("Cloud Saves Translations already exist.")
