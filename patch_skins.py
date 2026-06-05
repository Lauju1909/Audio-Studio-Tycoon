import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_skins = """
    "RES_BLOCKCHAIN_SKINS": "Blockchain-Skins",
    "RES_BLOCKCHAIN_SKINS_DESC": "Implementiere limitierte In-Game Gegenstände via Blockchain, extrem umstritten aber hochprofitabel.",
"""

en_skins = """
    "RES_BLOCKCHAIN_SKINS": "Blockchain Skins",
    "RES_BLOCKCHAIN_SKINS_DESC": "Implement limited in-game items via blockchain, highly controversial but extremely profitable.",
"""

if '"RES_BLOCKCHAIN_SKINS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_skins)
    content = content.replace('"EN": {', '"EN": {\n' + en_skins)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Blockchain Skins Translations added.")
else:
    print("Blockchain Skins Translations already exist.")
