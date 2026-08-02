from .base import Menu

class SubscriptionMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("AudioPass Zentrale", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        sm = self.game_state.subscription_manager
        
        if not sm.is_active:
            if not self.game_state.is_feature_unlocked("subscription_vault"):
                from game_data import FEATURE_UNLOCKS
                year = FEATURE_UNLOCKS["subscription_vault"].get("year", "???") if "subscription_vault" in FEATURE_UNLOCKS else 2015
                self.options.append({'text': f'AudioPass (Gesperrt bis {year})', 'action': lambda: None})
            else:
                self.options.append({'text': 'AudioPass starten (5.000.000 EUR)', 'action': self._launch_service})
        else:
            self.options.append({'text': f"Abonnenten: {sm.subscribers:,} | Einnahmen/Woche: {(sm.subscribers * sm.monthly_fee / 4):,.0f} EUR", 'action': lambda: None})
            self.options.append({'text': f"Wochen seit letztem Release: {sm.weeks_since_last_release}", 'action': lambda: None})
            
            self.options.append({'text': 'Eigenes Spiel zum Katalog hinzufuegen', 'action': lambda: "sub_add_own_game_menu"})
            self.options.append({'text': 'Third-Party Spiele lizenzieren', 'action': lambda: "sub_third_party_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        
    def _launch_service(self):
        sm = self.game_state.subscription_manager
        success, msg = sm.launch_service(self.game_state)
        if success:
            self.audio.play_sound("cheer")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return "subscription_menu"

class SubAddOwnGameMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Eigenes Spiel hinzufuegen", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        sm = self.game_state.subscription_manager
        
        my_games = [g for g in self.game_state.game_history if getattr(g, "type", "") != "Auftragsarbeit"]
        
        for game in my_games:
            if game.name not in sm.catalog:
                self.options.append({
                    'text': f"{game.name} (Review: {getattr(game.review, 'average', 0)}%)",
                    'action': lambda g=game: self._add_game(g)
                })
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "subscription_menu"})
        
    def _add_game(self, game):
        sm = self.game_state.subscription_manager
        success, msg = sm.add_own_game(self.game_state, game)
        if success:
            self.audio.play_sound("cash")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        return "subscription_menu"

class SubThirdPartyMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Third-Party Spiele lizenzieren", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        sm = self.game_state.subscription_manager
        
        for rival in self.game_state.rivals:
            for game in getattr(rival, "history", []):
                if game.name not in sm.catalog:
                    cost = int(game.sales * 10)
                    self.options.append({
                        'text': f"{game.name} von {rival.name} ({cost:,} EUR)",
                        'action': lambda g=game: self._buy_game(g)
                    })
                    
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "subscription_menu"})
        
    def _buy_game(self, rival_game):
        sm = self.game_state.subscription_manager
        success, msg = sm.buy_third_party_game(self.game_state, rival_game)
        if success:
            self.audio.play_sound("cash")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        return "subscription_menu"
