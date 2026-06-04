import sys

with open('menus/gameplay.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add merch_menu and creator_menu to GameMenu
game_menu_code = '''
            {'text': self.game_state.get_text('esports_menu_title', default='E-Sports Zentrale'), 'action': lambda: "esports_menu"},
'''
new_game_menu_code = game_menu_code + '''
            {'text': self.game_state.get_text('merch_menu_title', default='Merchandising'), 'action': lambda: "merch_menu"},
            {'text': self.game_state.get_text('creator_menu_title', default='Content Creators Sponsern'), 'action': lambda: "creator_menu"},
'''
content = content.replace(game_menu_code, new_game_menu_code)

with open('menus/gameplay.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched GameMenu with Merch and Creators")
