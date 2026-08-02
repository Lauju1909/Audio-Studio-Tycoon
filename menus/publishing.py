from .base import Menu

class PublishingMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Publishing Label (Indie-Fund)", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        pm = self.game_state.publishing_manager
        
        if not pm.is_active:
            if not self.game_state.is_feature_unlocked("publishing_label"):
                from game_data import FEATURE_UNLOCKS
                year = FEATURE_UNLOCKS["publishing_label"].get("year", "???") if "publishing_label" in FEATURE_UNLOCKS else 2005
                self.options.append({'text': f'Publishing Label (Gesperrt bis {year})', 'action': lambda: None})
            else:
                self.options.append({'text': 'Publishing Label gruenden (10.000.000 EUR)', 'action': self._launch_label})
        else:
            self.options.append({'text': f"Prestige: {pm.prestige} | Finanzierte Projekte: {len(pm.funded_projects)}", 'action': lambda: None})
            self.options.append({'text': 'Aktive Pitches ansehen', 'action': lambda: "publishing_pitches_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})
        
    def _launch_label(self):
        pm = self.game_state.publishing_manager
        success, msg = pm.launch_label(self.game_state)
        if success:
            self.audio.play_sound("cheer")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return "publishing_menu"

class PublishingPitchesMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Aktive Indie-Pitches", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        pm = self.game_state.publishing_manager
        
        if not pm.active_pitches:
            self.options.append({'text': 'Aktuell keine neuen Pitches. Warte ein paar Wochen.', 'action': lambda: None})
        else:
            for pitch in pm.active_pitches:
                text = f"{pitch['game_name']} von {pitch['studio']} | Budget: {pitch['budget']:,} EUR | Share: {pitch['revenue_share']}% | Dauer: {pitch['dev_time']} W"
                self.options.append({
                    'text': text,
                    'action': lambda p=pitch: self._fund_pitch(p['id'])
                })
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "publishing_menu"})
        
    def _fund_pitch(self, pitch_id):
        pm = self.game_state.publishing_manager
        success, msg = pm.fund_pitch(self.game_state, pitch_id)
        if success:
            self.audio.play_sound("cash")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        return "publishing_menu"
