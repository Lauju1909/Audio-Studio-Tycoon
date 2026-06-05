import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to init
if 'self.active_merch = []' not in content:
    init_loc = content.find('self.active_addons = []')
    content = content[:init_loc] + 'self.active_merch = []\n        ' + content[init_loc:]

# Add to save_game
if '"active_merch": [m.to_dict() for m in getattr(self, "active_merch", [])],' not in content:
    save_loc = content.find('"active_addons": [a.to_dict() for a in self.active_addons],')
    content = content[:save_loc] + '"active_merch": [m.to_dict() for m in getattr(self, "active_merch", [])],\n            ' + content[save_loc:]

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
