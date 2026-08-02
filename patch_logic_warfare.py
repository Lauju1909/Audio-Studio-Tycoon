
filepath = 'logic.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if 'from managers.corporate_warfare import CorporateWarfareManager' not in content:
    content = content.replace('from models import ', 'from managers.corporate_warfare import CorporateWarfareManager\nfrom models import ')

# Init
if 'self.corporate_warfare =' not in content:
    content = content.replace('self.is_researching = False', 'self.is_researching = False\n        self.corporate_warfare = CorporateWarfareManager()')

# Tick
if 'self.corporate_warfare.tick(self)' not in content:
    content = content.replace('self.hardware_manager.tick()', 'self.hardware_manager.tick()\n        self.corporate_warfare.tick(self)')

# Save game
if '"corporate_warfare": self.corporate_warfare.to_dict()' not in content:
    content = content.replace('"console_total_weeks": getattr(self, "console_total_weeks", 48)', '"console_total_weeks": getattr(self, "console_total_weeks", 48),\n            "corporate_warfare": self.corporate_warfare.to_dict()')

# Load game
if 'if "corporate_warfare" in data:' not in content:
    content = content.replace('if "console_progress" in data:', 'if "corporate_warfare" in data:\n            self.corporate_warfare.from_dict(data["corporate_warfare"])\n        if "console_progress" in data:')

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Logic patched.')
