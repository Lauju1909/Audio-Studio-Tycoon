import sys
import re

with open('menus/business.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'class AcquisitionMenu\(Menu\):.*?return "acquisition_menu"', re.DOTALL)

new_acq = '''class AcquisitionMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('acquisition_menu_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        for idx, rival in enumerate(self.game_state.rivals):
            if getattr(rival, 'is_owned_by_player', False):
                self.options.append({
                    'text': self.game_state.get_text('subsidiary_manage_option', default='Tochterfirma verwalten: {name}').format(name=rival.name),
                    'action': lambda i=idx: self.manage_subsidiary(i)
                })
            else:
                buyout_cost = (100 - getattr(rival, 'owned_shares', 0)) * 50000 
                
                self.options.append({
                    'text': self.game_state.get_text('acquisition_option', name=rival.name, cost=buyout_cost, shares=getattr(rival, 'owned_shares', 0)),
                    'action': lambda i=idx, cost=buyout_cost: self.acquire_studio(i, cost)
                })
            
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_studios_available'), 'action': lambda: "bank_menu"})

        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})
        super().announce_entry()
        
    def manage_subsidiary(self, idx):
        self.game_state.selected_subsidiary_idx = idx
        return "subsidiary_manage_menu"

    def acquire_studio(self, idx, cost):
        if self.game_state.money >= cost:
            self.game_state.money -= cost
            self.game_state.track_expense("shares", cost)
            rival = self.game_state.rivals[idx]
            rival.owned_shares = 100
            rival.is_owned_by_player = True
            self.audio.speak(self.game_state.get_text('acquisition_success', name=rival.name))
        else:
            self.audio.speak(self.game_state.get_text('acquisition_fail_money', cost=cost))
        return "acquisition_menu"'''

new_content = re.sub(pattern, new_acq, content)

with open('menus/business.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Patched with regex.")
