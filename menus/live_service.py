from .base import Menu

class LiveServiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Live-Service & Monetarisierung", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        mm = self.game_state.monetization_manager
        
        if not self.game_state.is_feature_unlocked("live_services"):
            from game_data import FEATURE_UNLOCKS
            year = FEATURE_UNLOCKS["live_services"].get("year", "???") if "live_services" in FEATURE_UNLOCKS else 2012
            self.options.append({'text': f'Live-Services (Gesperrt bis {year})', 'action': lambda: None})
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})
            return
            
        self.options.append({'text': f"Fan-Vertrauen: {mm.fan_trust:.1f}% | Gov Heat: {mm.government_heat:.1f}%", 'action': lambda: None})
        
        loot_text = "[AN] Lootboxen (High Risk, Massive Income)" if mm.lootboxes_active else "[AUS] Lootboxen aktivieren"
        self.options.append({'text': loot_text, 'action': self._toggle_lootboxes})
        
        bp_text = "[AN] Battle Pass (Low Risk, Steady Income)" if mm.battle_pass_active else "[AUS] Battle Pass aktivieren"
        self.options.append({'text': bp_text, 'action': self._toggle_battle_pass})
        
        self.options.append({'text': f"PR-Manager einstellen (100.000 EUR) - Aktuell: {mm.pr_managers}", 'action': self._hire_pr})
        self.options.append({'text': f"Ethik-Manager einstellen (250.000 EUR) - Aktuell: {mm.ethics_managers}", 'action': self._hire_ethics})
        
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})
        
    def _toggle_lootboxes(self):
        mm = self.game_state.monetization_manager
        active = mm.toggle_lootboxes()
        if active:
            self.audio.play_sound("cash")
            self.audio.speak("Lootboxen aktiviert. Die Kasse klingelt, aber die Fans werden es hassen!")
        else:
            self.audio.play_sound("confirm")
            self.audio.speak("Lootboxen deaktiviert. Die Fans atmen auf.")
        self._update_options()
        return "live_service_menu"
        
    def _toggle_battle_pass(self):
        mm = self.game_state.monetization_manager
        active = mm.toggle_battle_pass()
        if active:
            self.audio.play_sound("cash")
            self.audio.speak("Battle Pass aktiviert.")
        else:
            self.audio.play_sound("confirm")
            self.audio.speak("Battle Pass deaktiviert.")
        self._update_options()
        return "live_service_menu"
        
    def _hire_pr(self):
        mm = self.game_state.monetization_manager
        success, msg = mm.hire_pr_manager(self.game_state)
        if success:
            self.audio.play_sound("confirm")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return "live_service_menu"
        
    def _hire_ethics(self):
        mm = self.game_state.monetization_manager
        success, msg = mm.hire_ethics_manager(self.game_state)
        if success:
            self.audio.play_sound("confirm")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return "live_service_menu"
