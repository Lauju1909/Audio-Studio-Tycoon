from .base import Menu

class DarknetMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_darknet_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        
        self.options.append({'text': self.game_state.get_text('menu_darknet_espionage'), 'action': lambda: self._start_espionage()})
        self.options.append({'text': self.game_state.get_text('menu_darknet_sabotage'), 'action': lambda: self._start_sabotage()})
        self.options.append({'text': self.game_state.get_text('menu_darknet_takeover'), 'action': lambda: "darknet_takeover_select"})
        self.options.append({'text': self.game_state.get_text('menu_darknet_back'), 'action': lambda: "office_menu"})

    def _start_espionage(self):
        self.game_state.darknet_mission_type = "espionage"
        return "darknet_target_select"
        
    def _start_sabotage(self):
        self.game_state.darknet_mission_type = "sabotage"
        return "darknet_target_select"


class DarknetTargetSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('warfare_select_target'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for rival in self.game_state.rivals:
            self.options.append({'text': rival.name, 'action': lambda r=rival: self._select_target(r)})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "darknet_menu"})

    def _select_target(self, rival):
        m_type = getattr(self.game_state, "darknet_mission_type", None)
        if not m_type:
            return "darknet_menu"
            
        from managers.corporate_warfare import EspionageMission, SabotageMission
        if m_type == "espionage":
            mission = EspionageMission(rival.name)
        elif m_type == "sabotage":
            mission = SabotageMission(rival.name)
        else:
            return "darknet_menu"
            
        if self.game_state.corporate_warfare.start_mission(mission, self.game_state):
            self.audio.play_sound("buy")
            self.audio.speak(self.game_state.get_text('warfare_mission_started', default="Mission gestartet. Überwache den Posteingang für Updates."))
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
        
        return "darknet_menu"


class DarknetTakeoverSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('warfare_select_target'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for rival in self.game_state.rivals:
            # Estimate base value
            base_value = 500000 + (len(rival.games) * 100000)
            txt = f"{rival.name} (Est: ~{base_value}$)"
            self.options.append({'text': txt, 'action': lambda r=rival: self._select_target(r)})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "darknet_menu"})

    def _select_target(self, rival):
        self.game_state.darknet_takeover_target = rival.name
        return "darknet_takeover_bid"


class DarknetTakeoverBidMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.input_text = ""
        super().__init__(self.game_state.get_text('warfare_input_bid'), [], audio, game_state)

    def handle_input(self, event):
        import pygame
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
            self.audio.speak(self.input_text if self.input_text else "Leer")
        elif event.key == pygame.K_RETURN:
            if self.input_text.isdigit():
                bid = int(self.input_text)
                target_name = getattr(self.game_state, "darknet_takeover_target", None)
                rival = next((r for r in self.game_state.rivals if r.name == target_name), None)
                if rival:
                    if self.game_state.money >= bid:
                        from managers.corporate_warfare import execute_hostile_takeover
                        success, msg = execute_hostile_takeover(rival, bid, self.game_state)
                        if success:
                            self.audio.play_sound("buy")
                        else:
                            self.audio.play_sound("error")
                        self.audio.speak(msg)
                    else:
                        self.audio.play_sound("error")
                        self.audio.speak(self.game_state.get_text('not_enough_money'))
                return "darknet_menu"
        elif event.unicode.isdigit():
            self.input_text += event.unicode
            self.audio.speak(self.input_text)
        elif event.key == pygame.K_ESCAPE:
            return "darknet_takeover_select"
        return None

    def get_text_display(self):
        return [self.title, self.input_text + "_"]
