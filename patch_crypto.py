import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_crypto = """
    "RES_CRYPTO": "Kryptowährungs-Integration",
    "RES_CRYPTO_DESC": "Erlaube In-Game-Käufe mit virtuellen Währungen und Tokens.",
"""

en_crypto = """
    "RES_CRYPTO": "Cryptocurrency Integration",
    "RES_CRYPTO_DESC": "Allow in-game purchases with virtual currencies and tokens.",
"""

if '"RES_CRYPTO"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_crypto)
    content = content.replace('"EN": {', '"EN": {\n' + en_crypto)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Crypto Translations added.")
else:
    print("Crypto Translations already exist.")
