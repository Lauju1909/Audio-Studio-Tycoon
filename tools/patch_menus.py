
# ============================================================
# PRODUCTION MENU
# ============================================================

class ProductionMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('production_menu_title'), [], audio, game_state)
        
    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        active_games = [g for g in self.game_state.game_history if g.state == "on_market" and (g.publisher == self.game_state.company_name or not g.publisher)]
        
        if not active_games:
            self.audio.speak(self.game_state.get_text('production_no_games'))
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        else:
            for idx, game in enumerate(active_games):
                stock = getattr(game, 'stock', 0)
                self.options.append({
                    'text': f"{game.name} - Im Lager: {stock}/{self.game_state.storage_capacity}",
                    'action': lambda i=idx: self.select_game(i)
                })
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
            
        used_storage = sum(getattr(g, 'stock', 0) for g in self.game_state.game_history)
        self.audio.speak(self.game_state.get_text('production_status', used=used_storage, max=self.game_state.storage_capacity))
        self.speak_current(interrupt=False)
        
    def select_game(self, idx):
        active_games = [g for g in self.game_state.game_history if g.state == "on_market" and (g.publisher == self.game_state.company_name or not g.publisher)]
        if 0 <= idx < len(active_games):
            self.game_state._pending_production_game_idx = self.game_state.game_history.index(active_games[idx])
            return "production_amount_menu"
        return "production_menu"

class ProductionAmountMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('production_amount_title', 'production_amount_prompt', audio, game_state, self._confirm, self._cancel, is_numeric=True)
        
    def _confirm(self, amount_str):
        try:
            amount = int(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.audio.speak(self.game_state.get_text('invalid_amount'))
            return "production_menu"
            
        idx = getattr(self.game_state, '_pending_production_game_idx', -1)
        success, info = self.game_state.produce_physical_copies(idx, amount)
        self.audio.speak(info)
        return "production_menu"
        
    def _cancel(self):
        return "production_menu"
