import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_ai = """
    "RES_AI_NPCS": "KI für NPCs",
    "RES_AI_NPCS_DESC": "Erforsche fortschrittliche Künstliche Intelligenz, um extrem realistische NPCs zu erschaffen.",
"""

en_ai = """
    "RES_AI_NPCS": "AI for NPCs",
    "RES_AI_NPCS_DESC": "Research advanced Artificial Intelligence to create highly realistic NPCs.",
"""

if '"RES_AI_NPCS"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_ai)
    content = content.replace('"EN": {', '"EN": {\n' + en_ai)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("AI Translations added.")
else:
    print("AI Translations already exist.")
