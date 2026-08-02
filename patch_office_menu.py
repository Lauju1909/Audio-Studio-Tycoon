
filepath = 'menus/office.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Darknet menu button to OfficeMenu
if 'menu_darknet_title' not in content:
    content = content.replace(
        "self.options.append({'text': self.game_state.get_text('office_upgrades_menu_title'), 'action': lambda: \"office_upgrades_menu\"})",
        "self.options.append({'text': self.game_state.get_text('office_upgrades_menu_title'), 'action': lambda: \"office_upgrades_menu\"})\n        self.options.append({'text': self.game_state.get_text('menu_darknet_title', default=\"Darknet Terminal\"), 'action': lambda: \"darknet_menu\"})"
    )

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('OfficeMenu patched.')
