import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_rt = """
    "RES_REALTIME_RAYTRACING": "Echtzeit-Raytracing",
    "RES_REALTIME_RAYTRACING_DESC": "Biete hyperrealistische Beleuchtung in deinen Spielen für die neuesten Grafikkarten an.",
"""

en_rt = """
    "RES_REALTIME_RAYTRACING": "Real-Time Raytracing",
    "RES_REALTIME_RAYTRACING_DESC": "Offer hyper-realistic lighting in your games for the latest graphics cards.",
"""

if '"RES_REALTIME_RAYTRACING"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_rt)
    content = content.replace('"EN": {', '"EN": {\n' + en_rt)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Raytracing Translations added.")
else:
    print("Raytracing Translations already exist.")
