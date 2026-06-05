import json
import os

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_cloud = """
    "RES_CLOUD_GAMING": "Cloud-Gaming Infrastruktur",
    "RES_CLOUD_GAMING_DESC": "Erforsche Cloud-Gaming, um eigene Spiele per Stream anzubieten und die Reichweite zu erhoehen.",
    "CLOUD_GAMING_MENU": "Cloud-Gaming Portal",
    "CLOUD_GAMING_ACTIVE": "Cloud-Gaming ist aktiv!",
"""

en_cloud = """
    "RES_CLOUD_GAMING": "Cloud Gaming Infrastructure",
    "RES_CLOUD_GAMING_DESC": "Research cloud gaming to stream your games and increase reach.",
    "CLOUD_GAMING_MENU": "Cloud Gaming Portal",
    "CLOUD_GAMING_ACTIVE": "Cloud Gaming is active!",
"""

if '"RES_CLOUD_GAMING"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_cloud)
    content = content.replace('"EN": {', '"EN": {\n' + en_cloud)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Translations added.")
else:
    print("Translations already exist.")
