import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_publisher = """
    "RES_PUBLISHER": "Eigene Publisher",
    "RES_PUBLISHER_DESC": "Erforsche den Eigenvertrieb, um unabhängiger von externen Publishern zu werden.",
"""

en_publisher = """
    "RES_PUBLISHER": "Own Publisher",
    "RES_PUBLISHER_DESC": "Research self-publishing to become independent from external publishers.",
"""

if '"RES_PUBLISHER"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_publisher)
    content = content.replace('"EN": {', '"EN": {\n' + en_publisher)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Publisher Translations added.")
else:
    print("Publisher Translations already exist.")
