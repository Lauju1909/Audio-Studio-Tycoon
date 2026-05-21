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
        if self.download_url:
            return "update_progress_menu"
        return "main_menu"

    def _cancel(self):
        self.game_state.pending_update = None
        return "main_menu"

class UpdateProgressMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.download_percent = 0
        self.download_error = None
        self.download_finished = False
        self.last_announced_percent = -20
        self.last_ticker_time = 0
        self.ticker_interval = 1000
        self._announced_verifying = False

        update_info = self.game_state.pending_update
        self.download_url = update_info.get("download_url") if update_info else None
        self.expected_hash = update_info.get("hash") if update_info else None

        title = self.game_state.get_text('update_title')
        super().__init__(title, [], audio, game_state)

        import threading
        self.download_thread = threading.Thread(target=self._run_download, daemon=True)
        self.download_thread.start()

    def _run_download(self):
        from updater import download_and_apply_update
        try:
            if not self.download_url:
                self.download_error = "no_url"
                self.download_finished = True
                return

            success = download_and_apply_update(
                self.download_url,
                self.expected_hash,
                progress_callback=self._on_progress
            )
            if not success:
                self.download_error = "download_failed"
                self.download_finished = True
        except Exception as e:
            self.download_error = str(e)
            self.download_finished = True

    def _on_progress(self, downloaded, total):
        if total > 0:
            percent = int((downloaded / total) * 100)
            self.download_percent = percent

    def update(self):
        import pygame
        super().update()

        if self.download_finished:
            self.audio.play_sound("error")
            err_text = self.game_state.get_text('update_failed')
            self.audio.speak(err_text, interrupt=True)
            self.game_state.pending_update = None
            return "main_menu"

        now = pygame.time.get_ticks()
        if now - self.last_ticker_time >= self.ticker_interval:
            self.audio.play_sound("click")
            self.last_ticker_time = now

        percent = self.download_percent
        rounded_percent = (percent // 20) * 20
        if rounded_percent > self.last_announced_percent:
            self.last_announced_percent = rounded_percent
            progress_text = self.game_state.get_text('update_progress', percent=rounded_percent)
            self.audio.speak(progress_text, interrupt=True)

        if percent == 100 and not self._announced_verifying:
            self._announced_verifying = True
            self.audio.speak(self.game_state.get_text('update_verifying'), interrupt=True)

        return None

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
            {'text': t('wiki_chapter_tutorial'),   'action': lambda: self._read('wiki_tutorial_text')},
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
