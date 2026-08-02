from .base import Menu

class UnionMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('union_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        union_mgr = self.game_state.union_manager
        
        anger_txt = self.game_state.get_text('union_anger', anger=int(union_mgr.union_anger))
        strike_status = self.game_state.get_text('union_striking') if union_mgr.is_striking else self.game_state.get_text('union_not_striking')
        
        if union_mgr.union_busted:
            self.title = self.game_state.get_text('union_busted_title')
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})
            return

        self.title = f"{self.game_state.get_text('union_menu')} - {anger_txt} | {strike_status}"

        # Automatisierung aktivieren/deaktivieren
        if union_mgr.ai_tools_active:
            self.options.append({'text': self.game_state.get_text('disable_ai_tools'), 'action': lambda: self._toggle_ai(False)})
        else:
            self.options.append({'text': self.game_state.get_text('enable_ai_tools'), 'action': lambda: self._toggle_ai(True)})
            
        # Verhandeln (nur möglich wenn Streik)
        if union_mgr.is_striking and union_mgr.negotiation_cooldown == 0:
            self.options.append({'text': self.game_state.get_text('union_accept_demands'), 'action': lambda: self._negotiate("accept_demands")})
            self.options.append({'text': self.game_state.get_text('union_compromise'), 'action': lambda: self._negotiate("compromise")})
            self.options.append({'text': self.game_state.get_text('union_bust'), 'action': lambda: self._negotiate("union_busting")})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _toggle_ai(self, state):
        self.game_state.union_manager.ai_tools_active = state
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('ai_tools_status', status=state))
        self._update_options()
        return None

    def _negotiate(self, option):
        success, msg = self.game_state.union_manager.negotiate(option, self.game_state)
        if success:
            self.audio.play_sound("confirm")
            self.audio.speak(msg)
            return "hr_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(msg)
            self._update_options()
            return None
