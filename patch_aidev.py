import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_ai_dev = """
    "RES_AI_DEV_TOOLS": "KI-DevTools",
    "RES_AI_DEV_TOOLS_DESC": "Erforsche KI-gestützte Entwicklungswerkzeuge, um die Programmierzeit massiv zu verkürzen.",
"""

en_ai_dev = """
    "RES_AI_DEV_TOOLS": "AI DevTools",
    "RES_AI_DEV_TOOLS_DESC": "Research AI-assisted development tools to massively reduce programming time.",
"""

if '"RES_AI_DEV_TOOLS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_ai_dev)
    content = content.replace('"EN": {', '"EN": {\n' + en_ai_dev)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("AI DevTools Translations added.")
else:
    print("AI DevTools Translations already exist.")
