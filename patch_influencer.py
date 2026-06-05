import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_influencer = """
    "RES_INFLUENCER": "Influencer-Marketing",
    "RES_INFLUENCER_DESC": "Arbeite mit Streamern zusammen, um deine Spiele viral zu machen.",
"""

en_influencer = """
    "RES_INFLUENCER": "Influencer Marketing",
    "RES_INFLUENCER_DESC": "Collaborate with streamers to make your games go viral.",
"""

if '"RES_INFLUENCER"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_influencer)
    content = content.replace('"EN": {', '"EN": {\n' + en_influencer)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Influencer Translations added.")
else:
    print("Influencer Translations already exist.")
