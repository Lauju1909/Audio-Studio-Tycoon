import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_motion = """
    "RES_MOTION_CONTROLLER": "Motion Controller Hardware",
    "RES_MOTION_CONTROLLER_DESC": "Entwickle und verkaufe deine eigenen fortschrittlichen Motion-Controller.",
"""

en_motion = """
    "RES_MOTION_CONTROLLER": "Motion Controller Hardware",
    "RES_MOTION_CONTROLLER_DESC": "Develop and sell your own advanced motion controllers.",
"""

if '"RES_MOTION_CONTROLLER"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_motion)
    content = content.replace('"EN": {', '"EN": {\n' + en_motion)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Motion Controller Translations added.")
else:
    print("Motion Controller Translations already exist.")
