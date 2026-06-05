import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_engine = """
    "RES_ENGINE_RESEARCH": "Engine-Forschung",
    "RES_ENGINE_RESEARCH_DESC": "Erforsche eigene Spiele-Engines, um die Qualität deiner Spiele zu steigern und Lizenzkosten zu sparen.",
"""

en_engine = """
    "RES_ENGINE_RESEARCH": "Engine Research",
    "RES_ENGINE_RESEARCH_DESC": "Research proprietary game engines to increase game quality and save licensing costs.",
"""

if '"RES_ENGINE_RESEARCH"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_engine)
    content = content.replace('"EN": {', '"EN": {\n' + en_engine)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Engine Translations added.")
else:
    print("Engine Translations already exist.")
