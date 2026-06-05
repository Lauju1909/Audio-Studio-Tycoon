import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_weather = """
    "RES_DYNAMIC_WEATHER": "Dynamisches Wetter-System",
    "RES_DYNAMIC_WEATHER_DESC": "Implementiere ein realistisches Wettersystem für mehr Immersion in deinen Spielen.",
"""

en_weather = """
    "RES_DYNAMIC_WEATHER": "Dynamic Weather System",
    "RES_DYNAMIC_WEATHER_DESC": "Implement a realistic weather system for more immersion in your games.",
"""

if '"RES_DYNAMIC_WEATHER"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_weather)
    content = content.replace('"EN": {', '"EN": {\n' + en_weather)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Weather Translations added.")
else:
    print("Weather Translations already exist.")
