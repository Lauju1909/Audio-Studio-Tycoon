import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_exchange = """
    "RES_VIRTUAL_EXCHANGE": "Virtuelle Spielwährungs-Börse",
    "RES_VIRTUAL_EXCHANGE_DESC": "Etabliere einen Handelsplatz für verschiedene virtuelle In-Game-Währungen.",
"""

en_exchange = """
    "RES_VIRTUAL_EXCHANGE": "Virtual Currency Exchange",
    "RES_VIRTUAL_EXCHANGE_DESC": "Establish a trading platform for various virtual in-game currencies.",
"""

if '"RES_VIRTUAL_EXCHANGE"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_exchange)
    content = content.replace('"EN": {', '"EN": {\n' + en_exchange)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Virtual Exchange Translations added.")
else:
    print("Virtual Exchange Translations already exist.")
