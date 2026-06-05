import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('game.dlc_count += 1', 'print(f"Old dlc_count: {game.dlc_count}"); game.dlc_count += 1; print(f"New dlc_count: {game.dlc_count}")')

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
