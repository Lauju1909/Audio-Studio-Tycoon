import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_loot = """
    "RES_LOOTBOXES": "Lootboxen",
    "RES_LOOTBOXES_DESC": "Erforsche Lootbox-Mechaniken, um den Profit massiv zu steigern (kann den Ruf schädigen).",
"""

en_loot = """
    "RES_LOOTBOXES": "Lootboxes",
    "RES_LOOTBOXES_DESC": "Research lootbox mechanics to massively increase profit (might damage reputation).",
"""

if '"RES_LOOTBOXES"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_loot)
    content = content.replace('"EN": {', '"EN": {\n' + en_loot)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Lootbox Translations added.")
else:
    print("Lootbox Translations already exist.")
