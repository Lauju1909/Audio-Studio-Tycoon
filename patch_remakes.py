import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_remake = """
    "RES_REMAKES": "Remakes & Remasters",
    "RES_REMAKES_DESC": "Bringe alte Klassiker mit modernisierter Grafik und Engine erneut auf den Markt.",
"""

en_remake = """
    "RES_REMAKES": "Remakes & Remasters",
    "RES_REMAKES_DESC": "Re-release old classics with modernized graphics and engine.",
"""

if '"RES_REMAKES"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_remake)
    content = content.replace('"EN": {', '"EN": {\n' + en_remake)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Remakes Translations added.")
else:
    print("Remakes Translations already exist.")
