import pygame
import time
from models import GameProject
from game_data import (
    get_compatibility, get_compatibility_text,
)

class Menu:
    def __init__(self, title, options, audio, game_state):
        self.title = title
        self.options = options
        self.audio = audio
        self.game_state = game_state
        self.current_index = 0

    def speak_current(self, interrupt=True):
        if self.options:
            text = self.options[self.current_index]['text']
            if self.game_state.settings.get('menu_numbering_enabled', True):
                pos = f"{self.current_index + 1} {self.game_state.get_text('of_label')} {len(self.options)}"
                self.audio.speak(f"{text}. {pos}", interrupt=interrupt)
            else:
                self.audio.speak(text, interrupt=interrupt)

    def announce_entry(self):
        self.current_index = 0
        self.audio.speak(self.title)
        if self.options:
            self.speak_current(interrupt=False)

    def handle_input(self, event):
        gs = self.game_state
        if not self.options:
            if event.key in [gs.key_up, gs.key_down, gs.key_confirm, gs.key_back, gs.key_home, gs.key_end, pygame.K_LEFT, pygame.K_RIGHT]:
                self.audio.play_sound("error")
            return None
            
        if event.key == gs.key_up:
            if self.current_index > 0:
                self.current_index -= 1
                self.audio.play_sound("click")
                self.speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == gs.key_down:
            if self.current_index < len(self.options) - 1:
                self.current_index += 1
                self.audio.play_sound("click")
                self.speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == gs.key_home:
            if self.current_index > 0:
                self.current_index = 0
                self.audio.play_sound("click")
                self.speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == gs.key_end:
            if self.current_index < len(self.options) - 1:
                self.current_index = len(self.options) - 1
                self.audio.play_sound("click")
                self.speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == gs.key_back or event.key == pygame.K_LEFT:
            back_action = None
            for opt in self.options:
                text_lower = opt['text'].strip().lower()
                back_text = self.game_state.get_text('back').strip().lower()
                if text_lower == back_text:
                    back_action = opt.get('action')
                    break
            
            if not back_action and len(self.options) > 0:
                 last_opt = self.options[-1]
                 back_text = self.game_state.get_text('back').strip().lower()
                 if back_text in last_opt['text'].strip().lower():
                      back_action = last_opt.get('action')
                     
            if back_action:
                self.audio.play_sound("click")
                return back_action()
            else:
                self.audio.play_sound("error")
                
        elif event.key == gs.key_confirm:
            self.audio.play_sound("confirm")
            action = self.options[self.current_index].get('action')
            if action:
                return action()
        return None

    def update(self):
        pass

class TextInputMenu:
    def __init__(self, title, prompt, audio, game_state, on_confirm, on_cancel):
        self.title = title
        self.prompt = prompt
        self.audio = audio
        self.game_state = game_state
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.text = ""
        self.is_text_input = True

    def sanitize_input(self, text):
        forbidden = ["\"", "'", "\\", ";", "&", "<", ">", "|"]
        for char in forbidden:
            text = text.replace(char, "")
        return text.strip()

    def announce_entry(self):
        self.text = ""
        self.game_state.pause_for_menu = True
        self.audio.speak(self.game_state.get_text('input_prompt', title=self.game_state.get_text(self.title), prompt=self.game_state.get_text(self.prompt)))

    def handle_input(self, event):
        gs = self.game_state
        mods = pygame.key.get_mods()

        # Zufallsname per STRG + R oder F2
        if (event.key == pygame.K_r and (mods & pygame.KMOD_CTRL)) or event.key == pygame.K_F2:
            if hasattr(self, 'generate_random_name'):
                self.text = self.generate_random_name()
                self.audio.play_sound("click")
                self.audio.speak(self.game_state.get_text('random_name_generated', default="Zufälliger Name: ") + self.text)
                return None

        if event.key == gs.key_confirm:
            sanitized = self.sanitize_input(self.text)
            if sanitized:
                self.audio.play_sound("confirm")
                # self.audio.speak(self.game_state.get_text('input_confirmed', text=sanitized))
                self.game_state.pause_for_menu = False
                return self.on_confirm(sanitized)
            else:
                self.audio.speak(self.game_state.get_text('input_empty_warn'))
        elif event.key == pygame.K_BACKSPACE:
            if self.text:
                removed = self.text[-1]
                self.text = self.text[:-1]
                remaining = self.text if self.text else self.game_state.get_text('input_empty')
                self.audio.speak(self.game_state.get_text('input_deleted', removed=removed, remaining=remaining))
            else:
                self.audio.speak(self.game_state.get_text('input_already_empty'))
        elif event.key == gs.key_back or event.key == pygame.K_ESCAPE:
            self.game_state.pause_for_menu = False
            return self.on_cancel()
        
        unicode_char = getattr(event, 'unicode', None)
        if unicode_char and unicode_char.isprintable() and len(unicode_char) == 1:
            self.text += unicode_char
            self.audio.speak(unicode_char)
        return None

    def update(self):
        pass

class SliderMenu:
    def __init__(self, title, audio, game_state, slider_names, budget, on_confirm, on_cancel):
        self.title = title
        self.audio = audio
        self.game_state = game_state
        self.slider_names = slider_names
        self.budget = budget
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.values = {name: 0 for name in slider_names}
        self.current_index = 0
        self._enter_warned = False

    @property
    def remaining(self):
        return self.budget - sum(self.values.values())

    def announce_entry(self):
        self.values = {name: 0 for name in self.slider_names}
        self.current_index = 0
        self._enter_warned = False
        self.game_state.pause_for_menu = True
        self.audio.speak(
            self.game_state.get_text('slider_intro', title=self.title, budget=self.budget, length=len(self.slider_names))
        )
        self._speak_current()

    def _speak_current(self):
        name = self.slider_names[self.current_index]
        val = self.values[name]
        msg = self.game_state.get_text('slider_status', 
                                       name=name, 
                                       val=val, 
                                       remaining=self.remaining, 
                                       current=self.current_index + 1, 
                                       total=len(self.slider_names))
        self.audio.speak(msg, interrupt=True)

    def handle_input(self, event):
        gs = self.game_state
        if event.key == gs.key_up:
            if self.current_index > 0:
                self.current_index -= 1
                self._speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == gs.key_down:
            if self.current_index < len(self.slider_names) - 1:
                self.current_index += 1
                self._speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == gs.key_home:
            if self.current_index > 0:
                self.current_index = 0
                self._speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == gs.key_end:
            if self.current_index < len(self.slider_names) - 1:
                self.current_index = len(self.slider_names) - 1
                self._speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == pygame.K_RIGHT:
            name = self.slider_names[self.current_index]
            if self.values[name] < 10 and self.remaining > 0:
                self.values[name] += 1
                self.audio.play_sound("click")
                self._speak_current()
            elif self.remaining <= 0:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('slider_no_points'))
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('slider_max'))
        elif event.key == pygame.K_LEFT:
            name = self.slider_names[self.current_index]
            if self.values[name] > 0:
                self.values[name] -= 1
                self.audio.play_sound("click")
                self._speak_current()
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('slider_min'))
        elif event.key == gs.key_confirm:
            if self.remaining > 0:
                if hasattr(self, '_enter_warned') and self._enter_warned:
                    self.audio.play_sound("confirm")
                    self.game_state.pause_for_menu = False
                    return self.on_confirm(dict(self.values))
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('slider_warn_remaining', remaining=self.remaining))
                self._enter_warned = True
            else:
                self.audio.play_sound("confirm")
                self.game_state.pause_for_menu = False
                return self.on_confirm(dict(self.values))
        elif event.key == gs.key_back or event.key == pygame.K_ESCAPE:
            self.game_state.pause_for_menu = False
            return self.on_cancel()

        if event.key != gs.key_confirm:
            self._enter_warned = False
        return None

    def update(self):
        pass
