import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_movie = """
    "RES_MOVIE_LICENSES": "Filmlizenzen",
    "RES_MOVIE_LICENSES_DESC": "Erwirb Lizenzen großer Blockbuster-Filme, um darauf basierende Spiele zu entwickeln.",
"""

en_movie = """
    "RES_MOVIE_LICENSES": "Movie Licenses",
    "RES_MOVIE_LICENSES_DESC": "Acquire licenses from major blockbuster movies to develop games based on them.",
"""

if '"RES_MOVIE_LICENSES"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_movie)
    content = content.replace('"EN": {', '"EN": {\n' + en_movie)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Movie License Translations added.")
else:
    print("Movie License Translations already exist.")
