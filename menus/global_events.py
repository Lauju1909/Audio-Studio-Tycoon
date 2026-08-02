from .base import Menu

class GlobalEventsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Globale Events & Krisen-Management", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        gem = self.game_state.global_event_manager
        
        if not gem.current_event:
            self.options.append({'text': 'Aktuell gibt es keine globalen Krisen.', 'action': lambda: None})
        else:
            self.options.append({'text': f"AKTIVE KRISE: {gem.current_event.name}", 'action': lambda: None})
            self.options.append({'text': f"Dauer: {gem.current_event.duration_weeks - gem.current_event.weeks_active} Wochen verbleibend", 'action': lambda: None})
            
            if gem.current_event.effect_type == "chip_crisis":
                if gem.black_market_deal_active:
                    self.options.append({'text': 'Schwarzmarkt-Deal aktiv! (Entwicklungs-Malus umgangen)', 'action': lambda: None})
                else:
                    self.options.append({'text': 'Hardware auf dem Schwarzmarkt kaufen (5.000.000 EUR) - Stoppt Entwicklungs-Malus!', 'action': self._buy_chips})
                    
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})
        
    def _buy_chips(self):
        gem = self.game_state.global_event_manager
        success, msg = gem.buy_black_market_chips(self.game_state)
        if success:
            self.audio.play_sound("cash")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return "global_events_menu"
