import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_cloud2 = """
    "RES_CLOUD2": "Cloud-Gaming 2.0",
    "RES_CLOUD2_DESC": "Erforsche die nächste Generation des Cloud-Gamings für 8K-Auflösungen und minimale Latenz.",
"""

en_cloud2 = """
    "RES_CLOUD2": "Cloud Gaming 2.0",
    "RES_CLOUD2_DESC": "Research next-gen cloud gaming for 8K resolution and minimal latency.",
"""

if '"RES_CLOUD2"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_cloud2)
    content = content.replace('"EN": {', '"EN": {\n' + en_cloud2)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Cloud 2.0 Translations added.")
else:
    print("Cloud 2.0 Translations already exist.")
