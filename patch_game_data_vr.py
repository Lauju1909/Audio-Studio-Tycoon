
with open('game_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '"vr_headset":' not in content:
    content = content.replace('"transmedia": {', '"vr_headset": {"year": 2016, "name": "VR Hardware Labor"},\n    "metaverse": {"year": 2018, "name": "Das AudioVerse (Metaverse)"},\n    "transmedia": {')
    with open('game_data.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched game_data.py for VR & Metaverse")
else:
    print("Already patched game_data.py")
