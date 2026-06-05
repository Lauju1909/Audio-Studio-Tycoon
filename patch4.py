import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('base_game.hype = min(100, base_game.hype + 1)', 'self.hype = min(100, getattr(self, "hype", 0) + 1)')

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
