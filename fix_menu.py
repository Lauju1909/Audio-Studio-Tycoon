with open('menus/business.py', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('"business_menu"', '"game_menu"')
with open('menus/business.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('menus/gameplay.py', 'r', encoding='utf-8') as f:
    gp = f.read()

insertion = "              {'text': self.game_state.get_text('esports_menu_title', default='E-Sports Zentrale'), 'action': lambda: \"esports_menu\"},\n"
if 'esports_menu' not in gp:
    gp = gp.replace("{'text': self.game_state.get_text('jingle_menu_title')", insertion + "              {'text': self.game_state.get_text('jingle_menu_title')")
    with open('menus/gameplay.py', 'w', encoding='utf-8') as f:
        f.write(gp)
