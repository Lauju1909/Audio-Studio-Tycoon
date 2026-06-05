import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_esports = """
    "RES_ESPORTS": "E-Sports Ligen",
    "RES_ESPORTS_DESC": "Erforsche E-Sports, um eigene Ligen und Turniere für deine Spiele zu veranstalten.",
"""

en_esports = """
    "RES_ESPORTS": "E-Sports Leagues",
    "RES_ESPORTS_DESC": "Research e-sports to host custom leagues and tournaments for your games.",
"""

if '"RES_ESPORTS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_esports)
    content = content.replace('"EN": {', '"EN": {\n' + en_esports)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("ESports Translations added.")
else:
    print("ESports Translations already exist.")
