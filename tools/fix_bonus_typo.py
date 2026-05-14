with open(r'menus\gameplay.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Suche nach der fehlerhaften Zeile (Klammer falsch gesetzt)
old = '                    text += " [BONUS!"]\n'
new = '                    text += " [BONUS!]"\n'

if old in content:
    content = content.replace(old, new, 1)
    with open(r'menus\gameplay.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("FIXED OK")
else:
    print("NOT FOUND")
    # Zeige Zeilen 272-278 zum Debugging
    lines = content.splitlines()
    for i, ln in enumerate(lines[271:278], 272):
        print(f"{i}: {repr(ln)}")
