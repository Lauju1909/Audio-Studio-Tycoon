import sys

with open('menus/business.py', 'r', encoding='utf-8') as f:
    content = f.read()

subsidiary_code = '''
class SubsidiaryManagementMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('subsidiary_manage_title', default='Tochterfirma verwalten'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        rival_idx = getattr(self.game_state, 'selected_subsidiary_idx', -1)
        if 0 <= rival_idx < len(self.game_state.rivals):
            rival = self.game_state.rivals[rival_idx]
            
            self.options.append({
                'text': self.game_state.get_text('subsidiary_inject_cash', default='100.000 EUR investieren (Erhöht Spielqualität)'),
                'action': lambda: self.inject_cash(rival)
            })
            
            if getattr(self.game_state, 'active_custom_console', None):
                self.options.append({
                    'text': self.game_state.get_text('subsidiary_force_console', default='Anweisen, exklusiv für unsere Konsole zu entwickeln'),
                    'action': lambda: self.force_console(rival)
                })
                
            self.options.append({
                'text': self.game_state.get_text('subsidiary_absorb', default='Studio auflösen & IPs übernehmen'),
                'action': lambda: self.absorb_studio(rival, rival_idx)
            })

        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "acquisition_menu"})
        super().announce_entry()

    def inject_cash(self, rival):
        if self.game_state.money >= 100000:
            self.game_state.money -= 100000
            self.game_state.track_expense("other", 100000)
            rival.games_quality_boost = getattr(rival, 'games_quality_boost', 0) + 10
            self.audio.speak(self.game_state.get_text('subsidiary_cash_success', default='Geld investiert. Ihre zukünftigen Spiele werden besser.'))
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money'))
        return "subsidiary_manage_menu"

    def force_console(self, rival):
        rival.develop_for_custom_console = True
        self.audio.speak(self.game_state.get_text('subsidiary_console_success', default='Das Studio entwickelt künftig exklusiv für unsere Konsole.'))
        return "subsidiary_manage_menu"

    def absorb_studio(self, rival, idx):
        # Transfer fans
        transferred_fans = int(getattr(rival, 'fans', 5000) * 0.25)
        self.game_state.fans += transferred_fans
        
        # Transfer games / IPs
        if hasattr(rival, 'games'):
            self.game_state.game_history.extend(rival.games)
            
        self.audio.speak(self.game_state.get_text('subsidiary_absorb_success', default='Studio aufgelöst. Wir haben ihre Spiele und {} Fans übernommen.').format(transferred_fans))
        self.game_state.rivals.pop(idx)
        return "acquisition_menu"
'''

content += "\n" + subsidiary_code

with open('menus/business.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added SubsidiaryManagementMenu to business.py")
