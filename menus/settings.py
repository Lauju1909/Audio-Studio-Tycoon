import pygame
from .base import Menu

class SettingsMenu:
    def __init__(self, audio, game_state, on_back):
        self.audio = audio
        self.game_state = game_state
        self.title = self.game_state.get_text('settings_menu', default="Einstellungen")
        self.on_back = on_back
        self.current_index = 0
        self.options = []
        self._update_options()

    def _update_options(self):
        s = self.game_state.settings
        lang_name = "Deutsch" if s['language'] == 'de' else "English"
        music_status = self.game_state.get_text('on') if s['music_enabled'] else self.game_state.get_text('off')

        tts_mode = s.get('tts_engine', 'auto')
        if tts_mode == 'nvda':
            tts_name = "NVDA / Screen Reader"
        elif tts_mode == 'sapi':
            tts_name = "SAPI (MS David)"
        else:
            tts_name = "Auto"

        auto_update_st = self.game_state.get_text('on') if s.get('auto_update', True) else self.game_state.get_text('off')

        # Release-Kanal: stable = nur stabile Versionen, beta = neuste (kann Fehler haben)
        channel = s.get('update_channel', 'stable')
        channel_name = "Stable" if channel == 'stable' else "Beta"

        self.options = [
            {'text': self.game_state.get_text('volume_settings', default="Lautstärkeeinstellungen"), 'action': self._goto_volume_settings},
            {'text': f"{self.game_state.get_text('music')}: {music_status}", 'action': self._toggle_music},
            {'text': f"{self.game_state.get_text('language')}: {lang_name}", 'action': self._toggle_language},
            {'text': f"{self.game_state.get_text('tts_mode')}: {tts_name}", 'action': self._toggle_tts},
            {'text': self.game_state.get_text('auto_update_toggle', status=auto_update_st), 'action': self._toggle_auto_update},
            {'text': self.game_state.get_text('release_channel', default=f"Release-Kanal: {channel_name}") + f": {channel_name}", 'action': self._toggle_channel},
            {'text': self.game_state.get_text('keybindings'), 'action': self._goto_keybindings},
            {'text': self.game_state.get_text('check_update'), 'action': self._check_update},
            {'text': self.game_state.get_text('back'), 'action': self.on_back}
        ]

    def _goto_volume_settings(self):
        return "volume_settings_menu"

    def _goto_keybindings(self):
        return "keybinding_menu"

    def _toggle_auto_update(self):
        self.game_state.settings['auto_update'] = not self.game_state.settings.get('auto_update', True)
        self.game_state.save_global_settings()
        self._update_options()
        self.speak_current(interrupt=False)

    def _toggle_channel(self):
        """Wechselt zwischen Stable und Beta Release-Kanal."""
        current = self.game_state.settings.get('update_channel', 'stable')
        new_channel = 'beta' if current == 'stable' else 'stable'
        self.game_state.settings['update_channel'] = new_channel
        self.game_state.save_global_settings()
        channel_name = "Beta" if new_channel == 'beta' else "Stable"
        if new_channel == 'beta':
            self.audio.speak(
                self.game_state.get_text(
                    'channel_beta_warning',
                    default="Beta-Kanal aktiviert. Beta-Versionen können Fehler enthalten!"
                )
            )
        else:
            self.audio.speak(
                self.game_state.get_text(
                    'channel_stable_info',
                    default="Stable-Kanal aktiviert. Nur getestete Versionen."
                )
            )
        self._update_options()
        
    def _check_update(self):
        from updater import check_for_updates
        import json
        import os

        self.audio.speak(self.game_state.get_text('checking_update'))

        current_version = "1.0.0"
        if os.path.exists("version.json"):
            try:
                with open("version.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    current_version = data.get("version", "1.0.0")
            except Exception:
                pass

        # Kanal aus Settings lesen – Standard ist immer 'stable'
        channel = self.game_state.settings.get('update_channel', 'stable')
        result = check_for_updates(current_version, channel=channel)

        if result and result.get("update_available"):
            # Beta-Warnung im Menü anzeigen
            if result.get('is_prerelease'):
                result['changelog'] = "[BETA] " + result.get('changelog', '')
            self.game_state.pending_update = result
            return "update_confirm_menu"
        else:
            self.audio.speak(self.game_state.get_text('no_update'))
            return None

    def _toggle_tts(self):
        modes = ["auto", "nvda", "sapi"]
        current = self.game_state.settings.get('tts_engine', 'auto')
        try:
            idx = modes.index(current)
        except ValueError:
            idx = 0
        new_mode = modes[(idx + 1) % len(modes)]
        self.game_state.settings['tts_engine'] = new_mode
        self.game_state.save_global_settings()
        
        if hasattr(self.audio, 'update_tts_engine'):
            self.audio.update_tts_engine(new_mode)
            
        tts_name = "NVDA / Screen Reader" if new_mode == 'nvda' else ("SAPI" if new_mode == 'sapi' else "Auto")
        self.audio.speak(self.game_state.get_text('tts_mode') + " " + tts_name)
        self._update_options()
        self.speak_current(interrupt=False)

    def _toggle_music(self):
        self.game_state.settings['music_enabled'] = not self.game_state.settings['music_enabled']
        self.game_state.save_global_settings()
        self.audio.set_music_enabled(self.game_state.settings['music_enabled'])
        if self.game_state.settings['music_enabled']:
            self.audio.play_music("music_back")
        self._update_options()
        self.speak_current()

    def _toggle_language(self):
        import translations
        new_lang = 'en' if self.game_state.settings['language'] == 'de' else 'de'
        self.game_state.settings['language'] = new_lang
        self.game_state.save_global_settings()
        translations.set_language(new_lang)
        
        self.audio.speak(self.game_state.get_text('language') + " " + ("English" if new_lang == 'en' else "Deutsch"))
        self._update_options()
        self.speak_current(interrupt=False)

    def speak_current(self, interrupt=True):
        text = self.options[self.current_index]['text']
        self.audio.speak(text, interrupt=interrupt)

    def announce_entry(self):
        self.current_index = 0
        self.audio.speak(self.game_state.get_text('settings_menu'))
        self.speak_current(interrupt=False)

    def handle_input(self, event):
        gs = self.game_state
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
        elif event.key == gs.key_confirm:
            self.audio.play_sound("confirm")
            return self.options[self.current_index]['action']()
        elif event.key == gs.key_back or event.key == pygame.K_ESCAPE:
            return self.on_back()
        return None

    def update(self):
        pass

class KeybindingMenu(Menu):
    def __init__(self, audio, game_state):
        self.game_state = game_state
        self.audio = audio
        self.waiting_for_key = None
        super().__init__(self.game_state.get_text('keybindings_menu'), [], audio, game_state)

    def _update_options(self):
        gs = self.game_state
        def _get_key_name(k):
            return pygame.key.name(k) if k else "Unknown"
            
        self.options = [
            {'text': f"{self.game_state.get_text('key_up')} ({_get_key_name(gs.key_up)})", 'action': lambda: self._start_bind('key_up')},
            {'text': f"{self.game_state.get_text('key_down')} ({_get_key_name(gs.key_down)})", 'action': lambda: self._start_bind('key_down')},
            {'text': f"{self.game_state.get_text('key_confirm')} ({_get_key_name(gs.key_confirm)})", 'action': lambda: self._start_bind('key_confirm')},
            {'text': f"{self.game_state.get_text('key_back')} ({_get_key_name(gs.key_back)})", 'action': lambda: self._start_bind('key_back')},
            {'text': f"{self.game_state.get_text('key_home')} ({_get_key_name(gs.key_home)})", 'action': lambda: self._start_bind('key_home')},
            {'text': f"{self.game_state.get_text('key_end')} ({_get_key_name(gs.key_end)})", 'action': lambda: self._start_bind('key_end')},
            {'text': self.game_state.get_text('back'), 'action': self._back}
        ]
        
    def _back(self):
        return "settings_menu"

    def _start_bind(self, key_name):
        self.waiting_for_key = key_name
        self.trigger_key = self.game_state.key_confirm
        self.bind_start_time = pygame.time.get_ticks()
        self.audio.speak(self.game_state.get_text('press_new_key', action=self.game_state.get_text(key_name)))
        return None

    def handle_input(self, event):
        if self.waiting_for_key:
            if pygame.time.get_ticks() - getattr(self, 'bind_start_time', 0) < 1000:
                return None
            if event.key == getattr(self, 'trigger_key', None):
                return None
            setattr(self.game_state, self.waiting_for_key, event.key)
            self.game_state.save_global_settings()
            key_mapped = pygame.key.name(event.key)
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('key_bound', action=self.game_state.get_text(self.waiting_for_key), key=key_mapped))
            self.waiting_for_key = None
            self._update_options()
            return None
        return super().handle_input(event)

    def announce_entry(self):
        self._update_options()
        super().announce_entry()

class VolumeSettingsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('volume_settings', default="Lautstärkeeinstellungen"), [], audio, game_state)
        
    def _update_options(self):
        s = self.game_state.settings
        self.options = [
            {'text': f"Musiklautstärke: {s.get('music_volume', 50)}%", 'action': lambda: self._adjust_volume('music_volume', 10)},
            {'text': f"Sprachausgabe (Tolk/TTS): {s.get('speech_volume', 100)}%", 'action': lambda: self._adjust_volume('speech_volume', 10)},
            {'text': f"Geräuschelautstärke: {s.get('sfx_volume', 100)}%", 'action': lambda: self._adjust_volume('sfx_volume', 10)},
            {'text': self.game_state.get_text('back', default="Zurück"), 'action': self._back}
        ]
        
    def _adjust_volume(self, key, amount, loop=True):
        val = self.game_state.settings.get(key, 100)
        val += amount
        if val > 100:
            val = 0 if loop else 100
        elif val < 0:
            val = 100 if loop else 0
            
        self.game_state.settings[key] = val
        self.game_state.save_global_settings()
        
        if hasattr(self.audio, 'apply_volumes'):
            self.audio.apply_volumes(self.game_state.settings)
            
        self._update_options()
        # self.speak_current(interrupt=True)
        
        if key == 'music_volume':
            text = f"Musik {val} Prozent"
        elif key == 'speech_volume':
            text = f"Sprachausgabe {val} Prozent"
        else:
            text = f"Geräusche {val} Prozent"
            
        self.audio.speak(text, interrupt=True)
        
        if key == 'sfx_volume':
            self.audio.play_sound("click")
            
        return None

    def handle_input(self, event):
        gs = self.game_state
        if event.key == pygame.K_LEFT:
            if self.current_index < 3:
                keys = ['music_volume', 'speech_volume', 'sfx_volume']
                return self._adjust_volume(keys[self.current_index], -10, loop=False)
        elif event.key == pygame.K_RIGHT:
            if self.current_index < 3:
                keys = ['music_volume', 'speech_volume', 'sfx_volume']
                return self._adjust_volume(keys[self.current_index], 10, loop=False)
        
        return super().handle_input(event)
        
    def _back(self):
        return "settings_menu"
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
