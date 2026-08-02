
with open('menus/business.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        if not getattr(self.game_state, 'is_public_company', False) and self.game_state.money >= 10000000 and self.game_state.fans >= 1000000:
            options.insert(1, {'text': self.game_state.get_text('ipo_option', default='Boersengang (IPO) planen'), 'action': lambda: "ipo_menu"})"""

replacement = """        if not getattr(self.game_state, 'is_public_company', False) and self.game_state.money >= 10000000 and self.game_state.fans >= 1000000:
            if self.game_state.is_feature_unlocked("ipo"):
                options.insert(1, {'text': self.game_state.get_text('ipo_option', default='Boersengang (IPO) planen'), 'action': lambda: "ipo_menu"})
            else:
                from game_data import FEATURE_UNLOCKS
                if "ipo" in FEATURE_UNLOCKS:
                    options.insert(1, {'text': f"{self.game_state.get_text('ipo_option', default='Boersengang (IPO) planen')} (Ab {FEATURE_UNLOCKS['ipo'].get('year', '???')}, Level {FEATURE_UNLOCKS['ipo'].get('office_level', '?')})", 'action': lambda: None})"""

if target in content:
    content = content.replace(target, replacement)
    with open('menus/business.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched BankMenu in menus/business.py!")
else:
    print("Could not find BankMenu ipo_option in menus/business.py!")
