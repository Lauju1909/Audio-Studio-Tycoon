import json

translation_file = "translations.py"

with open(translation_file, "r", encoding="utf-8") as f:
    content = f.read()

de_stream = """
    "RES_STREAM_INTEGRATION": "Streaming-Integration",
    "RES_STREAM_INTEGRATION_DESC": "Erlaube es Streamern, ihre Communities direkt ins Spiel einzubinden.",
"""

en_stream = """
    "RES_STREAM_INTEGRATION": "Streaming Integration",
    "RES_STREAM_INTEGRATION_DESC": "Allow streamers to integrate their communities directly into the game.",
"""

if '"RES_STREAM_INTEGRATION"' not in content:
    content = content.replace('"DE": {', '"DE": {\n' + de_stream)
    content = content.replace('"EN": {', '"EN": {\n' + en_stream)
    with open(translation_file, "w", encoding="utf-8") as f:
        f.write(content)
    print("Stream Translations added.")
else:
    print("Stream Translations already exist.")
