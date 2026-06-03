import codecs

lines = []
with codecs.open('models.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_class = """class EsportsLeague:
    def __init__(self, game_name, start_week):
        self.game_name = game_name
        self.start_week = start_week
        self.hype = 100
        self.championships_held = 0
        self.last_championship_year = 0

    def to_dict(self):
        return {
            "game_name": self.game_name,
            "start_week": self.start_week,
            "hype": self.hype,
            "championships_held": self.championships_held,
            "last_championship_year": self.last_championship_year
        }
"""

start = -1
for i, line in enumerate(lines):
    if 'class CustomConsole:' in line:
        start = i
        break

if start != -1:
    lines = lines[:start] + [new_class + '\n'] + lines[start:]

with codecs.open('models.py', 'w', 'utf-8') as f:
    f.writelines(lines)
