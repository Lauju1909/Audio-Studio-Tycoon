import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_abo = """
    "RES_SUBSCRIPTION": "Abo-Modelle",
    "RES_SUBSCRIPTION_DESC": "Erforsche Abomodelle, um Spielern monatliche Zahlungsoptionen anzubieten.",
"""

en_abo = """
    "RES_SUBSCRIPTION": "Subscription Models",
    "RES_SUBSCRIPTION_DESC": "Research subscription models to offer monthly payment options.",
"""

if '"RES_SUBSCRIPTION"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_abo)
    content = content.replace('"EN": {', '"EN": {\n' + en_abo)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Abo Translations added.")
else:
    print("Abo Translations already exist.")
