from .base import Menu

class LeaderboardMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        
        if not getattr(self.game_state, 'leaderboard_manager', None):
            from managers.leaderboard import LeaderboardManager
            self.game_state.leaderboard_manager = LeaderboardManager(self.game_state)
            
        # We need to fetch scores
        self.scores = []
        self.is_fetching = True
        self.game_state.leaderboard_manager.get_top_scores(self._on_scores_fetched)
        
        super().__init__("Globale Online-Charts", [{"text": "Lade Daten...", "action": None}], audio, game_state)
        
    def _on_scores_fetched(self, scores):
        self.scores = scores
        self.is_fetching = False
        self._update_options()
        
    def _update_options(self):
        self.options = []
        for i, score in enumerate(self.scores):
            text = f"{i+1}. {score['name']} - Score: {score['score']} - Prestige: {score['prestige']}"
            self.options.append({"text": text, "action": None})
            
        self.options.append({"text": "Meinen Score hochladen", "action": self._upload_score})
        self.options.append({"text": "Zurück", "action": lambda: "main_menu"})
        
        # Audio Update
        self.audio.speak("Leaderboard geladen.")

    def update(self):
        # We might need to update if fetching finished
        if not self.is_fetching and len(self.options) == 1:
            self._update_options()
            
    def _upload_score(self):
        score = self.game_state.money
        prestige = getattr(self.game_state, 'prestige', 0)
        name = self.game_state.company_name or "Unknown_Studio"
        
        self.audio.speak("Score wird hochgeladen...")
        self.game_state.leaderboard_manager.submit_score(name, score, prestige, self._on_score_uploaded)
        return None
        
    def _on_score_uploaded(self, success):
        self.audio.speak("Erfolgreich in den globalen Charts gespeichert!")
        # Reload
        self.is_fetching = True
        self.options = [{"text": "Lade neue Daten...", "action": None}]
        self.game_state.leaderboard_manager.get_top_scores(self._on_scores_fetched)
