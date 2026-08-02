
filepath = 'main.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if 'from menus.corporate import' not in content:
    content = content.replace(
        'from menus.office import',
        'from menus.corporate import DarknetMenu, DarknetTargetSelectMenu, DarknetTakeoverSelectMenu, DarknetTakeoverBidMenu\nfrom menus.office import'
    )

# Add routing
routes = '''        elif next_state == "darknet_menu":
            self.current_menu = DarknetMenu(self.audio, self.game_state)
        elif next_state == "darknet_target_select":
            self.current_menu = DarknetTargetSelectMenu(self.audio, self.game_state)
        elif next_state == "darknet_takeover_select":
            self.current_menu = DarknetTakeoverSelectMenu(self.audio, self.game_state)
        elif next_state == "darknet_takeover_bid":
            self.current_menu = DarknetTakeoverBidMenu(self.audio, self.game_state)
'''

if 'next_state == "darknet_menu"' not in content:
    content = content.replace(
        '        elif next_state == "email_detail":\n            self.current_menu = EmailDetailMenu(self.audio, self.game_state)',
        '        elif next_state == "email_detail":\n            self.current_menu = EmailDetailMenu(self.audio, self.game_state)\n' + routes
    )

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Main patched.')
