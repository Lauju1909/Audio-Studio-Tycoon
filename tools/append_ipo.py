import codecs

lines = []
with codecs.open('menus/business.py', 'r', 'utf-8') as f:
    lines = f.readlines()

ipo_class = """
class IPOMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('ipo_title', default='Boersengang (IPO)'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        payout = int((self.game_state.fans * 10 + self.game_state.money) * 0.3)
        self.options.append({
            'text': self.game_state.get_text('ipo_confirm', payout=payout, default=f'An die Boerse gehen (Erloes: {payout} EUR)'),
            'action': lambda p=payout: self._go_public(p)
        })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})

    def _go_public(self, payout):
        self.game_state.is_public_company = True
        self.game_state.shareholder_trust = 100
        self.game_state.money += payout
        self.game_state.shareholder_target = self.game_state.money * 1.10
        self.game_state.track_income("other", payout)
        self.audio.play_sound('cheer')
        self.audio.speak(self.game_state.get_text('ipo_success', default="Der Boersengang war ein voller Erfolg!"), interrupt=True)
        return "bank_menu"
"""

lines.append(ipo_class)

with codecs.open('menus/business.py', 'w', 'utf-8') as f:
    f.writelines(lines)
