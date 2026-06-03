import codecs

lines = []
with codecs.open('menus/business.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_block = """        options = [
            {'text': self.game_state.get_text('bank_statement_option'), 'action': self._show_report},
            {'text': self.game_state.get_text('loans'), 'action': lambda: "loan_menu"},
            {'text': self.game_state.get_text('donate_menu'), 'action': lambda: "donation_menu"},
            {'text': self.game_state.get_text('menu_monetization'), 'action': lambda: "monetization_menu"}
        ]
        if not getattr(self.game_state, 'is_public_company', False) and self.game_state.money >= 10000000 and self.game_state.fans >= 1000000:
            options.insert(1, {'text': self.game_state.get_text('ipo_option', default='Boersengang (IPO) planen'), 'action': lambda: "ipo_menu"})
            
        options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        super().__init__(title, options, audio, game_state)
"""

for i, line in enumerate(lines):
    if 'options = [' in line and 'bank_statement_option' in lines[i+1]:
        start = i
        end = i+7
        lines = lines[:start] + [new_block] + lines[end:]
        break

with codecs.open('menus/business.py', 'w', 'utf-8') as f:
    f.writelines(lines)
