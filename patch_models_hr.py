
with open('models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to __init__
if "self.talents = []" not in content:
    content = content.replace('self.personality = personality or random.choice(["perfectionist", "chaotic", "showman", "workaholic", "easygoing"])',
                              'self.personality = personality or random.choice(["perfectionist", "chaotic", "showman", "workaholic", "easygoing"])\n        self.talents = []\n        self.talent_points = 0')

# Add to to_dict
if '"talents": getattr(self, "talents", []),' not in content:
    content = content.replace('"personality": getattr(self, "personality", "easygoing"),',
                              '"personality": getattr(self, "personality", "easygoing"),\n            "talents": getattr(self, "talents", []),\n            "talent_points": getattr(self, "talent_points", 0),')

# Add to from_dict
if 'emp.talents = ed.get("talents", [])' not in content:
    content = content.replace('emp.personality = ed.get("personality", "easygoing")',
                              'emp.personality = ed.get("personality", "easygoing")\n        emp.talents = ed.get("talents", [])\n        emp.talent_points = ed.get("talent_points", 0)')

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched Employee in models.py")
