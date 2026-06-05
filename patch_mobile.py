import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_mobile = """
    "RES_MOBILE_PORTS": "Mobile-Portierungen",
    "RES_MOBILE_PORTS_DESC": "Erschließe den lukrativen Mobile-Markt durch Portierungen deiner Hits.",
"""

en_mobile = """
    "RES_MOBILE_PORTS": "Mobile Ports",
    "RES_MOBILE_PORTS_DESC": "Tap into the lucrative mobile market by porting your hits.",
"""

if '"RES_MOBILE_PORTS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_mobile)
    content = content.replace('"EN": {', '"EN": {\n' + en_mobile)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Mobile Ports Translations added.")
else:
    print("Mobile Ports Translations already exist.")
