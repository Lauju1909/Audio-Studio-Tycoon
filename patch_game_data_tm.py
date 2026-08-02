
with open('game_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '"transmedia":' not in content:
    content = content.replace('"ipo": {', '"transmedia": {"year": 2000, "name": "Filmrechte & Transmedia"},\n    "ipo": {')
    with open('game_data.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched game_data.py")
else:
    print("Already patched")
