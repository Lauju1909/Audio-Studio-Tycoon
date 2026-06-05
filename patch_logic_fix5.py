import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('game.updates.append(update)', 'print(f"Finishing update: {update.update_type} for {game.name}"); game.updates.append(update)')

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
