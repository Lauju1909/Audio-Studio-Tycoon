import codecs

lines = []
with codecs.open('models.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_class = """class CustomConsole:
    \"\"\"Vom Spieler entwickelte Konsole.\"\"\"
    def __init__(self, name, architecture, performance, marketing_budget, dev_cost, release_week):
        self.name = name
        self.architecture = architecture
        self.performance = performance  # 1-10
        self.marketing_budget = marketing_budget
        self.dev_cost = dev_cost
        self.release_week = release_week
        self.market_share = min(0.3, 0.05 + (marketing_budget / 50000000.0))
        self.units_sold = 0
        self.hype = min(100, marketing_budget / 500000.0)
        
    @property
    def tech_level(self):
        return self.performance

    def to_dict(self):
        return {
            "name": self.name,
            "architecture": getattr(self, 'architecture', 'Standard'),
            "performance": getattr(self, 'performance', getattr(self, 'tech_level', 1)),
            "marketing_budget": getattr(self, 'marketing_budget', 0),
            "dev_cost": self.dev_cost,
            "release_week": self.release_week,
            "market_share": self.market_share,
            "units_sold": getattr(self, 'units_sold', 0),
            "hype": getattr(self, 'hype', 0)
        }
"""

start = -1
end = -1
for i, line in enumerate(lines):
    if 'class CustomConsole:' in line:
        start = i
    if start != -1 and 'PHASE E: Publisher Role' in line:
        end = i - 1
        break

if start != -1 and end != -1:
    lines = lines[:start] + [new_class + '\n'] + lines[end:]

with codecs.open('models.py', 'w', 'utf-8') as f:
    f.writelines(lines)
