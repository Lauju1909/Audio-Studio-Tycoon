import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_union = """
    "RES_PLAYER_UNIONS": "Spieler-Gewerkschaften",
    "RES_PLAYER_UNIONS_DESC": "Verhandle mit Spieler-Gewerkschaften, um Streiks zu vermeiden.",
"""

en_union = """
    "RES_PLAYER_UNIONS": "Player Unions",
    "RES_PLAYER_UNIONS_DESC": "Negotiate with player unions to prevent strikes.",
"""

if '"RES_PLAYER_UNIONS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_union)
    content = content.replace('"EN": {', '"EN": {\n' + en_union)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Player Unions Translations added.")
else:
    print("Player Unions Translations already exist.")
