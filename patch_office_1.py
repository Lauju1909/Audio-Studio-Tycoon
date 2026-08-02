
with open('menus/office.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        self.options.append({'text': self.game_state.get_text('hr_menu'), 'action': lambda: "hr_menu"})
        self.options.append({'text': self.game_state.get_text('office_upgrades_menu_title'), 'action': lambda: "office_upgrades_menu"})
        self.options.append({'text': self.game_state.get_text('menu_darknet_title', default="Darknet Terminal"), 'action': lambda: "darknet_menu"})"""

replacement = """        self.options.append({'text': self.game_state.get_text('hr_menu'), 'action': lambda: "hr_menu"})
        self.options.append({'text': self.game_state.get_text('office_upgrades_menu_title'), 'action': lambda: "office_upgrades_menu"})
        
        if self.game_state.is_feature_unlocked("darknet"):
            self.options.append({'text': self.game_state.get_text('menu_darknet_title', default="Darknet Terminal"), 'action': lambda: "darknet_menu"})
        else:
            from game_data import FEATURE_UNLOCKS
            if "darknet" in FEATURE_UNLOCKS:
                self.options.append({'text': f"{self.game_state.get_text('menu_darknet_title', default='Darknet Terminal')} (Ab {FEATURE_UNLOCKS['darknet'].get('year', '???')})", 'action': lambda: None})"""

if target in content:
    content = content.replace(target, replacement)
    with open('menus/office.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched Darknet in menus/office.py!")
else:
    print("Could not find Darknet option in menus/office.py!")
