import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_ugc = """
    "RES_USER_GENERATED_CONTENT": "User-Generated Content",
    "RES_USER_GENERATED_CONTENT_DESC": "Erforsche Tools, um Spielern die Erstellung eigener Inhalte zu ermöglichen.",
"""

en_ugc = """
    "RES_USER_GENERATED_CONTENT": "User-Generated Content",
    "RES_USER_GENERATED_CONTENT_DESC": "Research tools to allow players to create their own content.",
"""

if '"RES_USER_GENERATED_CONTENT"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_ugc)
    content = content.replace('"EN": {', '"EN": {\n' + en_ugc)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("UGC Translations added.")
else:
    print("UGC Translations already exist.")
