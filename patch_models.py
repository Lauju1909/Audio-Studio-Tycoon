import re
import json

# 1. Update models.py
with open("models.py", "r", encoding="utf-8") as f:
    content = f.read()

# adding DRM and piracy, expansions, crunch
if "drm_level" not in content:
    content = content.replace('self.is_remake = False', 'self.is_remake = False\n        self.drm_level = 0\n        self.pirated_copies = 0')
    content = content.replace('"is_remake": getattr(self, "is_remake", False),', '"is_remake": getattr(self, "is_remake", False),\n            "drm_level": getattr(self, "drm_level", 0),\n            "pirated_copies": getattr(self, "pirated_copies", 0),')
    content = content.replace('proj.is_remake = gd.get("is_remake", False)', 'proj.is_remake = gd.get("is_remake", False)\n        proj.drm_level = gd.get("drm_level", 0)\n        proj.pirated_copies = gd.get("pirated_copies", 0)')

if "is_crunching" not in content:
    content = content.replace('self.is_sick = False', 'self.is_sick = False\n        self.is_crunching = False\n        self.crunch_weeks = 0')
    content = content.replace('"is_sick": getattr(self, "is_sick", False),', '"is_sick": getattr(self, "is_sick", False),\n            "is_crunching": getattr(self, "is_crunching", False),\n            "crunch_weeks": getattr(self, "crunch_weeks", 0),')
    content = content.replace('emp.is_sick = ed.get("is_sick", False)', 'emp.is_sick = ed.get("is_sick", False)\n        emp.is_crunching = ed.get("is_crunching", False)\n        emp.crunch_weeks = ed.get("crunch_weeks", 0)')

with open("models.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched models.py")
