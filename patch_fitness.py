import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_fitness = """
    "RES_FITNESS_GAMING": "Fitness-Gaming Integration",
    "RES_FITNESS_GAMING_DESC": "Kombiniere Gaming mit körperlicher Betätigung, um neue Zielgruppen zu erschließen.",
"""

en_fitness = """
    "RES_FITNESS_GAMING": "Fitness Gaming Integration",
    "RES_FITNESS_GAMING_DESC": "Combine gaming with physical exercise to reach new target audiences.",
"""

if '"RES_FITNESS_GAMING"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_fitness)
    content = content.replace('"EN": {', '"EN": {\n' + en_fitness)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fitness Gaming Translations added.")
else:
    print("Fitness Gaming Translations already exist.")
