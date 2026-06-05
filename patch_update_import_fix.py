import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        update = UpdateProject(
            base_game_name=game_name,'''

new = '''        from models import UpdateProject
        update = UpdateProject(
            base_game_name=game_name,'''

content = content.replace(old, new)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed missing UpdateProject import.")
