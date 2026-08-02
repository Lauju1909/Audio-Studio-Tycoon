from .base import Menu

class MonopolyMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Kartellamt & Monopol-Uebersicht", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        mm = self.game_state.monopoly_manager
        
        market_share = mm.get_market_share(self.game_state)
        subsidiaries = [r for r in self.game_state.rivals if getattr(r, 'is_owned_by_player', False)]
        
        self.options.append({'text': f"Tochtergesellschaften: {len(subsidiaries)} | Marktanteil: {market_share:.1f}%", 'action': lambda: None})
        
        if mm.lobbying_weeks_left > 0:
            self.options.append({'text': f"Kartellamt bestochen (Immunität für {mm.lobbying_weeks_left} Wochen)", 'action': lambda: None})
        else:
            if market_share >= 40.0:
                self.options.append({'text': f"WARNUNG: Kartellamt aktiv! Strafzahlungen fallen an.", 'action': lambda: None})
            self.options.append({'text': 'Politiker bestechen (15.000.000 EUR)', 'action': self._bribe})
            
        if subsidiaries:
            self.options.append({'text': 'Tochtergesellschaft abstossen (Marktanteil reduzieren)', 'action': lambda: "sell_subsidiary_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "espionage_menu"})
        
    def _bribe(self):
        mm = self.game_state.monopoly_manager
        success, msg = mm.bribe_politicians(self.game_state)
        if success:
            self.audio.play_sound("cash")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return "monopoly_menu"


class SellSubsidiaryMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Tochtergesellschaft abstossen", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        subsidiaries = [r for r in self.game_state.rivals if getattr(r, 'is_owned_by_player', False)]
        
        if not subsidiaries:
            self.options.append({'text': 'Keine Tochtergesellschaften vorhanden.', 'action': lambda: None})
        else:
            for i, sub in enumerate(subsidiaries):
                self.options.append({
                    'text': f"{sub.name} abstossen (3 - 8 Mio EUR)",
                    'action': lambda i=i: self._sell(i)
                })
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "monopoly_menu"})
        
    def _sell(self, index):
        mm = self.game_state.monopoly_manager
        success, msg = mm.sell_subsidiary(self.game_state, index)
        if success:
            self.audio.play_sound("cash")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        return "monopoly_menu"
