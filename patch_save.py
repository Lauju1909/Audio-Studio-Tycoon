import sys
import re

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix save_game
save_code = '''
            "sound_card_projects": [p.to_dict() for p in getattr(self, "sound_card_projects", [])],
'''
if '"custom_consoles"' not in save_code:
    new_save_code = save_code + '''
            "custom_consoles": [c.to_dict() for c in getattr(self, "custom_consoles", [])],
            "active_custom_console": getattr(self, "active_custom_console").to_dict() if getattr(self, "active_custom_console", None) else None,
'''
    content = content.replace(save_code, new_save_code)

# Fix load_game
load_code = '''
        self.sound_card_projects = []
        for pd in data.get("sound_card_projects", []):
            self.sound_card_projects.append(SoundCardProject.from_dict(pd))
'''
new_load_code = load_code + '''
        try:
            from models import CustomConsoleProject
            self.custom_consoles = []
            for c in data.get("custom_consoles", []):
                self.custom_consoles.append(CustomConsoleProject.from_dict(c))
            if data.get("active_custom_console"):
                self.active_custom_console = CustomConsoleProject.from_dict(data["active_custom_console"])
        except Exception as e:
            print("Error loading console", e)
'''
# I should remove the old one I put in from_dict accidentally? 
# Actually, I'll just find the exact place in load_game.
content = re.sub(r'(\s*self.sound_card_projects = \[\]\s*for pd in data.get\("sound_card_projects", \[\]\):\s*self.sound_card_projects.append\(SoundCardProject.from_dict\(pd\)\))', r'\1' + new_load_code.replace(load_code, ''), content)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched save/load")
