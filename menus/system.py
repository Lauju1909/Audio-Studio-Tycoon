import os
import json
from .base import Menu

class UpdateConfirmMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        update_info = self.game_state.pending_update
        v = update_info.get("version", "???") if update_info else "???"
        title = self.game_state.get_text('update_available').format(version=v)
        options = [
            {'text': self.game_state.get_text('yes_update'), 'action': self._apply_update},
            {'text': self.game_state.get_text('no_update_cancel'), 'action': self._cancel}
        ]
        super().__init__(title, options, audio, game_state)
        if update_info:
            self.changelog = update_info.get("changelog", "")
            self.download_url = update_info.get("download_url")
            self.expected_hash = update_info.get("hash")
        else:
            self.changelog = ""
            self.download_url = None
            self.expected_hash = None

    def announce_entry(self):
        super().announce_entry()
        if self.changelog:
            # "Changelog" ist ein universeller Begriff, wir nutzen ihn direkt
            self.audio.speak("Changelog: " + self.changelog, interrupt=False)

    def _apply_update(self):
        from updater import download_and_apply_update
        if self.download_url:
            self.audio.speak(self.game_state.get_text('downloading_update'))
            download_and_apply_update(self.download_url, self.expected_hash)
        return "main_menu"

    def _cancel(self):
        self.game_state.pending_update = None
        return "main_menu"

class BankruptcyMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('bankrupt_title')
        options = [
            {'text': self.game_state.get_text('load_last_save'), 'action': self._load_save},
            {'text': self.game_state.get_text('quit_to_main'), 'action': lambda: "main_menu"}
        ]
        super().__init__(title, options, audio, game_state)

    def _load_save(self):
        if self.game_state.load_game(slot=1):
             return "game_menu"
        return "main_menu"

class SaveMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('save_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        slots = self.game_state.get_save_slots_info()
        self.options = []
        for i in range(1, 6):
            info = slots.get(i, self.game_state.get_text('empty_slot'))
            self.options.append({
                'text': f"Slot {i}: {info}",
                'action': lambda s=i: self._save(s)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _save(self, slot):
        if self.game_state.save_game(slot):
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('save_success'))
            self._update_options()
        return None

class LoadMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('load_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        slots = self.game_state.get_save_slots_info()
        self.options = []
        for i in range(1, 6):
            info = slots.get(i, self.game_state.get_text('empty_slot'))
            self.options.append({
                'text': f"Slot {i}: {info}",
                'action': lambda s=i: self._load(s)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "main_menu"})

    def _load(self, slot):
        if self.game_state.load_game(slot):
            self.audio.play_sound("confirm")
            return "game_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('load_fail'))
        return None

class HelpMenu(Menu):
    """Erweitertes Wiki-System mit Unterkapiteln."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        t = game_state.get_text
        title = t('help_menu')
        options = [
            {'text': t('wiki_chapter_controls'),   'action': lambda: self._read('wiki_controls_text')},
            {'text': t('wiki_chapter_gameplay'),   'action': lambda: self._read('wiki_gameplay_text')},
            {'text': t('wiki_chapter_dev'),        'action': lambda: self._read('wiki_dev_text')},
            {'text': t('wiki_chapter_hr'),         'action': lambda: self._read('wiki_hr_text')},
            {'text': t('wiki_chapter_research'),   'action': lambda: self._read('wiki_research_text')},
            {'text': t('wiki_chapter_money'),      'action': lambda: self._read('wiki_money_text')},
            {'text': t('wiki_chapter_mods'),       'action': lambda: self._read('wiki_mods_text')},
            {'text': t('back'),                    'action': lambda: "main_menu"},
        ]
        super().__init__(title, options, audio, game_state)

    def announce_entry(self):
        t = self.game_state.get_text
        super().announce_entry()
        self.audio.speak(t('wiki_welcome_new'), interrupt=False)

    def _read(self, text_key):
        text = self.game_state.get_text(text_key)
        self.audio.speak(text, interrupt=True)
        return None
