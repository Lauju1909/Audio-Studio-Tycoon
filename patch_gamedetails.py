import sys

with open('menus/gameplay.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_options = '''            if not getattr(game, 'has_ads', False):
                self.options.append({'text': self.game_state.get_text('activate_ads', default="In-Game Werbung aktivieren"), 'action': self._activate_ads})
            else:
                self.options.append({'text': self.game_state.get_text('has_ads_active', default="In-Game Werbung: Aktiviert"), 'action': lambda: None})
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "active_games_menu"})'''

new_options = '''            if not getattr(game, 'has_ads', False):
                self.options.append({'text': self.game_state.get_text('activate_ads', default="In-Game Werbung aktivieren"), 'action': self._activate_ads})
            else:
                self.options.append({'text': self.game_state.get_text('has_ads_active', default="In-Game Werbung: Aktiviert"), 'action': lambda: None})
                
            self.options.append({'text': self.game_state.get_text('start_patch', default="Patch entwickeln (Bugs beheben)"), 'action': self._start_patch})
            self.options.append({'text': self.game_state.get_text('start_content_update', default="Content-Update entwickeln (Kostenlos)"), 'action': self._start_content_update})
            self.options.append({'text': self.game_state.get_text('start_dlc', default="DLC entwickeln (Kostenpflichtig)"), 'action': self._start_dlc})
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "active_games_menu"})'''

content = content.replace(old_options, new_options)

old_funcs = '''    def _activate_ads(self):
        game = getattr(self.game_state, '_pending_game_details', None)
        if game:
            game.has_ads = True
            self.audio.play_sound("confirm")
            self._update_options()
            self.current_index = 0
        return None'''

new_funcs = '''    def _activate_ads(self):
        game = getattr(self.game_state, '_pending_game_details', None)
        if game:
            game.has_ads = True
            self.audio.play_sound("confirm")
            self._update_options()
            self.current_index = 0
        return None

    def _start_patch(self):
        game = getattr(self.game_state, '_pending_game_details', None)
        if game:
            if self.game_state.start_update_project(game.name, "Patch", name="Patch"):
                self.audio.play_sound("confirm")
                self.audio.speak(self.game_state.get_text("patch_started", default="Patch-Entwicklung gestartet."))
                return "active_games_menu"
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text("not_enough_money"))
        return None

    def _start_content_update(self):
        game = getattr(self.game_state, '_pending_game_details', None)
        if game:
            if self.game_state.start_update_project(game.name, "Content", name="Content-Update"):
                self.audio.play_sound("confirm")
                self.audio.speak(self.game_state.get_text("content_started", default="Content-Update gestartet."))
                return "active_games_menu"
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text("not_enough_money"))
        return None

    def _start_dlc(self):
        game = getattr(self.game_state, '_pending_game_details', None)
        if game:
            if self.game_state.start_update_project(game.name, "DLC", name="DLC"):
                self.audio.play_sound("confirm")
                self.audio.speak(self.game_state.get_text("dlc_started", default="DLC-Entwicklung gestartet."))
                return "active_games_menu"
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text("not_enough_money"))
        return None'''

content = content.replace(old_funcs, new_funcs)

with open('menus/gameplay.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added Updates & DLC options to GameDetailsMenu")
