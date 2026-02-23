"""
Menüsystem für Audio Studio Tycoon - Audio Edition.

Alle Menüs sind vollständig über Tastatur bedienbar und
kommunizieren per NVDA mit dem Spieler.

Menü-Typen:
- Menu: Standard-Auswahl (Auf/Ab + Enter)
- TextInputMenu: Texteingabe (Buchstaben tippen, Backspace, Enter)
- SliderMenu: Slider-Verteilung (Auf/Ab = Slider, Links/Rechts = Wert)
"""

import pygame
import time
from models import GameProject, ReviewScore
from game_data import (
    TOPICS, GENRES, SLIDER_NAMES, PLATFORMS, AUDIENCES,
    OFFICE_LEVELS, ENGINE_FEATURES, GAME_SIZES,
    TRAINING_OPTIONS,
    get_compatibility, get_compatibility_text,
    get_available_platforms, get_available_features,
)
# logic.py: Spielzustand


# ============================================================
# BASIS-MENÜ
# ============================================================

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
            # Fallback for "von" / "of" depending on language
            try:
                von_word = "von" if self.game_state.settings['language'] == 'de' else "of"
            except AttributeError:
                von_word = "von"
            pos = f"{self.current_index + 1} {von_word} {len(self.options)}"
            self.audio.speak(f"{text}. {pos}", interrupt=interrupt)

    def announce_entry(self):
        self.current_index = 0
        self.audio.speak(self.title)
        if self.options:
            self.speak_current(interrupt=False)

    def handle_input(self, event):
        if not self.options:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN, pygame.K_LEFT, pygame.K_RIGHT]:
                self.audio.play_sound("error")
            return None
        if event.key == pygame.K_UP:
            if self.current_index > 0:
                self.current_index -= 1
                self.audio.play_sound("click")
                self.speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == pygame.K_DOWN:
            if self.current_index < len(self.options) - 1:
                self.current_index += 1
                self.audio.play_sound("click")
                self.speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == pygame.K_RETURN:
            self.audio.play_sound("confirm")
            action = self.options[self.current_index].get('action')
            if action:
                return action()
        return None

    def update(self):
        pass


# ============================================================
# TEXTEINGABE-MENÜ
# ============================================================

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

    def announce_entry(self):
        self.text = ""
        self.game_state.pause_for_menu = True
        self.audio.speak(self.game_state.get_text('input_prompt', title=self.game_state.get_text(self.title), prompt=self.game_state.get_text(self.prompt)))

    def handle_input(self, event):
        if event.key == pygame.K_RETURN:
            if self.text.strip():
                self.audio.play_sound("confirm")
                self.audio.speak(self.game_state.get_text('input_confirmed', text=self.text))
                self.game_state.pause_for_menu = False
                return self.on_confirm(self.text.strip())
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
        elif event.key == pygame.K_ESCAPE:
            self.game_state.pause_for_menu = False
            return self.on_cancel()
        elif event.unicode and event.unicode.isprintable() and len(event.unicode) == 1:
            self.text += event.unicode
            self.audio.speak(event.unicode)
        return None

    def update(self):
        pass


# ============================================================
# EINSTELLUNGEN-MENÜ
# ============================================================

class SettingsMenu:
    def __init__(self, audio, game_state, on_back):
        self.audio = audio
        self.game_state = game_state
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

        self.options = [
            {'text': f"{self.game_state.get_text('music')}: {music_status}", 'action': self._toggle_music},
            {'text': f"{self.game_state.get_text('language')}: {lang_name}", 'action': self._toggle_language},
            {'text': f"{self.game_state.get_text('tts_mode')}: {tts_name}", 'action': self._toggle_tts},
            {'text': self.game_state.get_text('back'), 'action': self.on_back}
        ]

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
        
        # Audio Engine anweisen, den Modus zu wechseln
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
        
        # Immediate text update for title and layout
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
        if event.key == pygame.K_UP:
            if self.current_index > 0:
                self.current_index -= 1
                self.audio.play_sound("click")
                self.speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == pygame.K_DOWN:
            if self.current_index < len(self.options) - 1:
                self.current_index += 1
                self.audio.play_sound("click")
                self.speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == pygame.K_RETURN:
            self.audio.play_sound("confirm")
            return self.options[self.current_index]['action']()
        elif event.key == pygame.K_ESCAPE:
            return self.on_back()
        return None

    def update(self):
        pass


# ============================================================
# SLIDER-MENÜ
# ============================================================

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
        if event.key == pygame.K_UP:
            if self.current_index > 0:
                self.current_index -= 1
                self._speak_current()
            else:
                self.audio.play_sound("error")
        elif event.key == pygame.K_DOWN:
            if self.current_index < len(self.slider_names) - 1:
                self.current_index += 1
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
        elif event.key == pygame.K_RETURN:
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
        elif event.key == pygame.K_ESCAPE:
            self.game_state.pause_for_menu = False
            return self.on_cancel()

        if event.key != pygame.K_RETURN:
            self._enter_warned = False
        return None

    def update(self):
        pass


# ============================================================
# HAUPTMENÜ
# ============================================================

class MainMenu(Menu):
    def __init__(self, audio, game_state):
        self.game_state = game_state
        options = [
            {'text': game_state.get_text('start_new_game'), 'action': self.new_game},
            {'text': game_state.get_text('load_game'), 'action': self.load_game},
            {'text': game_state.get_text('settings'), 'action': self.goto_settings},
            {'text': game_state.get_text('menu_credits'), 'action': self.show_credits},
            {'text': game_state.get_text('quit'), 'action': self.quit_game},
        ]
        super().__init__(game_state.get_text('main_menu'), options, audio, game_state)

    def goto_settings(self):
        return "settings_menu"

    def new_game(self):
        self.audio.speak(self.game_state.get_text('game_start_new'))
        return "company_name_input"

    def load_game(self):
        return "load_menu"

    def show_credits(self):
        # Speak the credits text and return None to stay in the menu
        # but re-announce the main menu so the user isn't lost
        self.audio.speak(self.game_state.get_text('credits_text'))
        return "main_menu"

    def quit_game(self):
        self.audio.speak(self.game_state.get_text('goodbye'))
        return "quit"


# ============================================================
# FIRMENGRÜNDUNG
# ============================================================

class CompanyNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(
            title=game_state.get_text('company_creation_title'),
            prompt=game_state.get_text('company_name_prompt'),
            audio=audio,
            game_state=game_state,
            on_confirm=self._confirm,
            on_cancel=self._cancel,
        )

    def _confirm(self, name):
        self.game_state.company_name = name
        self.audio.speak(self.game_state.get_text('game_welcome', name=name, money=self.game_state.money))
        return "game_menu"

    def _cancel(self):
        return "main_menu"


# ============================================================
# MANAGEMENT-ZENTRALE (Hauptspiel-Menü)
# ============================================================

class GameMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        options = [
            {'text': game_state.get_text('company_overview'), 'action': self.show_status},
            {'text': game_state.get_text('develop_new_game'), 'action': self.new_game},
            {'text': game_state.get_text('hr_department'), 'action': self.goto_hr},
        ]
        
        # Audio Expo Spezial-Option
        week_in_year = (self.game_state.week - 1) % 52 + 1
        if week_in_year == 26:
            options.append({'text': self.game_state.get_text('expo_title'), 'action': self.goto_expo})

        options.extend([
            {'text': game_state.get_text('research_engines'), 'action': self.goto_research},
            {'text': game_state.get_text('service_support'), 'action': self.goto_service},
            {'text': game_state.get_text('inbox'), 'action': self.goto_inbox},
            {'text': self.game_state.get_text('finances_and_bank'), 'action': self.goto_bank},
            {'text': game_state.get_text('upgrade_office'), 'action': self.goto_office},
            {'text': game_state.get_text('history'), 'action': self.show_history},
            {'text': game_state.get_text('save_game'), 'action': self.goto_save},
            {'text': game_state.get_text('wiki'), 'action': self.goto_help},
            {'text': game_state.get_text('settings'), 'action': self.goto_settings},
            {'text': game_state.get_text('quit'), 'action': self.quit_game_to_main},
        ])
        super().__init__(game_state.get_text('management_center'), options, audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        # Zufallsereignis prüfen
        event = self.game_state.check_random_event()
        if event:
            self.audio.speak(self.game_state.get_text('random_event_alert', title=event['title'], text=event['text']))
        self.audio.speak(
            f"{self.game_state.get_text('management_center')} - {self.game_state.company_name}. "
            f"{self.game_state.get_text('week')} {self.game_state.week}.",
            interrupt=False
        )
        self.speak_current(interrupt=False)

    def goto_service(self):
        return "service_menu"

    def goto_expo(self):
        return "expo_menu"

    def goto_inbox(self):
        return "email_inbox"

    def goto_bank(self):
        return "bank_menu"

    def show_status(self):
        self.audio.speak(self.game_state.get_status_text())
        return None

    def new_game(self):
        self.game_state.reset_draft()
        return "topic_menu"

    def remaster_game(self):
        return "remaster_select"

    def goto_hr(self):
        return "hr_menu"

    def goto_research(self):
        return "research_menu"

    def goto_office(self):
        return "office_menu"

    def goto_settings(self):
        return "settings_menu_ingame"

    def show_history(self):
        if not self.game_state.game_history:
            self.audio.speak(self.game_state.get_text('menu_empty_history'))
            return None
        self.audio.speak(self.game_state.get_text('menu_history_count', count=len(self.game_state.game_history)))
        for i, game in enumerate(self.game_state.game_history[-5:], 1):
            self.audio.speak(f"{i}. {game.summary()}", interrupt=False)
        return None

    def goto_save(self):
        return "save_menu"

    def goto_help(self):
        return "help_menu"

    def quit_game_to_main(self):
        self.audio.speak(self.game_state.get_text('goodbye'))
        return "main_menu"


# ============================================================
# SPIELENTWICKLUNG: THEMA → GENRE → PLATTFORM → ZIELGRUPPE → ENGINE → NAME → SLIDER → REVIEW
# ============================================================

class TopicMenu(Menu):
    def __init__(self, audio, game_state):
        options = []
        for topic in TOPICS:
            options.append({'text': topic, 'action': lambda t=topic: self._select(t)})
        options.append({'text': game_state.get_text('back'), 'action': self._cancel})
        super().__init__(game_state.get_text('select_topic'), options, audio, game_state)

    def _select(self, topic):
        self.game_state.current_draft['topic'] = topic
        self.audio.speak(self.game_state.get_text('dev_topic_selected', topic=topic))
        return "genre_menu"

    def _cancel(self):
        return "game_menu"


# ============================================================
# FINANZEN & BANK
# ============================================================

class BankMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('finances_and_bank'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = [
            {'text': self.game_state.get_text('bank_statement_option'), 'action': self.show_accounting},
        ]
        if not self.game_state.bank_loan:
            self.options.append({'text': self.game_state.get_text('take_loan_option'), 'action': self.goto_loans})
        else:
            rem = self.game_state.bank_loan.amount_remaining
            self.options.append({'text': self.game_state.get_text('pay_loan_option', amount=rem), 'action': self.pay_loan})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})
        self.audio.speak(self.title)
        self.speak_current(interrupt=False)

    def show_accounting(self):
        acc = self.game_state.accounting
        income = acc['income']
        expenses = acc['expenses']
        loan_paid = acc['loan_paid']
        profit = income - expenses - loan_paid
        
        # Falls Year Text anders formatiert werden soll (hier verwenden wir f-strings per translate key)
        msg = self.game_state.get_text('bank_account_statement', year=(self.game_state.week - 1) // 52 + 1, income=income, expenses=expenses, loan_paid=loan_paid, profit=profit)
        self.audio.speak(msg)
        return None

    def goto_loans(self):
        return "loan_menu"

    def pay_loan(self):
        rem = self.game_state.bank_loan.amount_remaining
        if self.game_state.money < rem:
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=rem))
            return None
        self.game_state.money -= rem
        self.game_state.bank_loan = None
        self.audio.speak(self.game_state.get_text('loan_paid_off'))
        self.announce_entry()
        return None

    def _cancel(self):
        return "game_menu"


class LoanMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('loan_offers_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        from models import BankLoan
        
        loans = [
            {"name": self.game_state.get_text('loan_small'), "amount": 50000, "interest": 0.10, "weeks": 52},
            {"name": self.game_state.get_text('loan_medium'), "amount": 250000, "interest": 0.15, "weeks": 104},
            {"name": self.game_state.get_text('loan_large'), "amount": 1000000, "interest": 0.20, "weeks": 208},
        ]
        
        self.options = []
        for l in loans:
            l_num = int(str(l['amount']))
            i_num = float(str(l['interest']))
            w_num = int(str(l['weeks']))
            repay = int(l_num * (1.0 + i_num))
            self.options.append({
                'text': self.game_state.get_text('loan_option_desc', name=l['name'], amount=l_num, repay=repay, weeks=w_num),
                'action': lambda loan=l: self._take_loan(loan)
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})
        self.audio.speak(self.title)
        self.speak_current(interrupt=False)

    def _take_loan(self, loan_data):
        from models import BankLoan
        loan = BankLoan(loan_data['amount'], loan_data['interest'], loan_data['weeks'])
        self.game_state.bank_loan = loan
        self.game_state.money += loan_data['amount']
        self.audio.speak(self.game_state.get_text('loan_taken_success', amount=loan_data['amount']))
        return "bank_menu"


class GenreMenu(Menu):
    def __init__(self, audio, game_state):
        options = []
        for genre in GENRES:
            options.append({'text': genre, 'action': lambda g=genre: self._select(g)})
        options.append({'text': game_state.get_text('back'), 'action': self._cancel})
        super().__init__(game_state.get_text('select_genre'), options, audio, game_state)

    def announce_entry(self):
        topic = self.game_state.current_draft.get('topic', '?')
        self.current_index = 0
        self.audio.speak(self.game_state.get_text('choose_genre_for_topic', topic=topic))
        self.speak_current(interrupt=False)

    def _select(self, genre):
        topic = self.game_state.current_draft.get('topic', '?')
        self.game_state.current_draft['genre'] = genre
        compat = get_compatibility(topic, genre)
        compat_text = get_compatibility_text(compat)
        self.audio.speak(f"{topic} + {genre}: {compat_text}.")
        return "platform_menu"

    def _cancel(self):
        return "topic_menu"


class PlatformMenu(Menu):
    """Plattform-Auswahl basierend auf verfügbaren Plattformen."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        # Wird in announce_entry dynamisch befüllt
        super().__init__(self.game_state.get_text('select_platform'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        available = get_available_platforms(self.game_state.week)
        self.options = []
        for p in available:
            fee = p['license_fee']
            is_bought = p['name'] in self.game_state.bought_platforms
            fee_text = ""
            if not is_bought and fee > 0:
                fee_text = f" (DevKit: {fee:,} {self.game_state.get_text('money_unit')})"
            
            def select_action(pn=p['name'], cost=fee, bought=is_bought):
                if not bought and cost > 0:
                    if self.game_state.money < cost:
                        self.audio.speak(self.game_state.get_text('not_enough_money_platform', platform=pn, cost=cost))
                        return None
                    self.game_state.money -= cost
                    self.game_state.bought_platforms.append(pn)
                    self.audio.speak(self.game_state.get_text('platform_bought', platform=pn, cost=cost))

                return self._select(pn)

            self.options.append({
                'text': f"{p['name']}{fee_text}",
                'action': select_action,
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})
        self.audio.speak(self.game_state.get_text('select_platform'))
        self.speak_current(interrupt=False)

    def _select(self, platform_name):
        self.game_state.current_draft['platform'] = platform_name
        self.audio.speak(self.game_state.get_text('platform_selected', platform=platform_name))
        return "audience_menu"

    def _cancel(self):
        return "genre_menu"


class AudienceMenu(Menu):
    """Zielgruppen-Auswahl."""

    def __init__(self, audio, game_state):
        options = []
        for a in AUDIENCES:
            options.append({'text': a, 'action': lambda au=a: self._select(au)})
        options.append({'text': game_state.get_text('back'), 'action': self._cancel})
        super().__init__(game_state.get_text('select_audience'), options, audio, game_state)

    def _select(self, audience):
        self.game_state.current_draft['audience'] = audience
        self.audio.speak(self.game_state.get_text('audience_selected', audience=audience))
        return "game_size_menu"

    def _cancel(self):
        return "platform_menu"


class GameSizeMenu(Menu):
    """Auswahl der Spielgröße (Klein, Mittel, Groß, AAA)."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        options = []
        for size in GAME_SIZES:
            options.append({
                'text': f"{size['name']} - {size['description']}",
                'action': lambda s=size: self._select(s)
            })
        options.append({'text': game_state.get_text('back'), 'action': self._cancel})
        super().__init__(game_state.get_text('select_size'), options, audio, game_state)

    def _select(self, size_data):
        # Check min employees
        if len(self.game_state.employees) < size_data['min_employees']:
            self.audio.speak(self.game_state.get_text('size_min_employees', size=size_data['name'], min_emp=size_data['min_employees'], current_emp=len(self.game_state.employees)))
            return None
        
        self.game_state.current_draft['size'] = size_data['name']
        self.audio.speak(self.game_state.get_text('size_selected', size=size_data['name']))
        return "marketing_menu"

    def _cancel(self):
        return "audience_menu"

class RemasterSelectMenu(Menu):
    """Auswahl eines alten Spiels für ein Remaster."""

    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('select_remaster'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        classics = [g for g in self.game_state.game_history if g.review and g.review.average >= 7]
        self.options = []
        for g in classics:
            self.options.append({
                'text': f"{g.name} ({g.topic}/{g.genre}, Score: {g.review.average:.1f})",
                'action': lambda p=g: self._select(p)
            })
        
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_remasters'), 'action': lambda: "game_menu"})
        
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        self.speak_current()

    def _select(self, project):
        self.game_state.reset_draft()
        self.game_state.current_draft.update({
            "name": f"{project.name} Remastered",
            "topic": project.topic,
            "genre": project.genre,
            "audience": project.audience,
            "is_remaster": True
        })
        self.audio.speak(self.game_state.get_text('remaster_selected', name=project.name))
        return "platform_menu"

    def _cancel(self):
        return "game_menu"

class MarketingMenu(Menu):
    """Auswahl der Marketing-Kampagne."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('marketing'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        from game_data import MARKETING_OPTIONS_PH5
        self.options = []
        for mark in MARKETING_OPTIONS_PH5:
            self.options.append({
                'text': f"{mark['name']} ({mark['cost']:,} Euro, +{mark['hype']} Hype)",
                'action': lambda m=mark: self._select(m)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})
        self.audio.speak(self.game_state.get_text('marketing'))
        self.speak_current(interrupt=False)

    def _select(self, mark_data):
        if self.game_state.money < mark_data['cost']:
            self.audio.speak(self.game_state.get_text('not_enough_money_marketing', cost=mark_data['cost']))
            return None
            
        self.game_state.money -= mark_data['cost']
        self.game_state.hype += mark_data['hype']
        self.game_state.current_draft['marketing'] = mark_data['name']
        self.audio.speak(self.game_state.get_text('marketing_booked', hype=mark_data['hype'], current_hype=self.game_state.hype))
        return "publisher_menu"

    def _cancel(self):
        return "game_size_menu"


class EngineSelectMenu(Menu):
    """Engine-Auswahl aus vorhandenen Engines."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('select_engine'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        for eng in self.game_state.engines:
            self.options.append({
                'text': f"{eng.name}, Tech-Level {eng.tech_level}",
                'action': lambda e=eng: self._select(e),
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})
        self.audio.speak(self.game_state.get_text('select_engine'))
        self.speak_current(interrupt=False)

    def _select(self, engine):
        self.game_state.current_draft['engine'] = engine
        self.audio.speak(self.game_state.get_text('engine_selected', name=engine.name, tech_level=engine.tech_level))
        return "game_name_input"

    def _cancel(self):
        return "marketing_menu"


class GameNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(
            title=game_state.get_text('game_name'),
            prompt=game_state.get_text('game_name_prompt_short'), # I'll add this to translations
            audio=audio,
            game_state=game_state,
            on_confirm=self._confirm,
            on_cancel=self._cancel,
        )

    def announce_entry(self):
        self.text = ""
        d = self.game_state.current_draft
        self.audio.speak(
            self.game_state.get_text('dev_name_prompt', topic=d.get('topic','?'), genre=d.get('genre','?'), platform=d.get('platform','?'))
        )

    def _confirm(self, name):
        self.game_state.current_draft['name'] = name
        self.audio.speak(self.game_state.get_text('dev_name_success', name=name))
        return "slider_menu"

    def _cancel(self):
        return "engine_select_menu"


class DevelopmentSliderMenu(SliderMenu):
    def __init__(self, audio, game_state):
        super().__init__(
            title=game_state.get_text('dev_progress'),
            audio=audio,
            game_state=game_state,
            slider_names=SLIDER_NAMES,
            budget=30,
            on_confirm=self._confirm,
            on_cancel=self._cancel,
        )

    def announce_entry(self):
        self.values = {name: 0 for name in self.slider_names}
        self.current_index = 0
        self._enter_warned = False

        d = self.game_state.current_draft
        dummy = type('Dummy', (), {
            'platform': d.get('platform', 'PC'),
            'audience': d.get('audience', 'Jugendliche'),
            'size': d.get('size', 'Mittel'),
            'marketing': d.get('marketing', 'Kein Marketing')
        })()
        cost = self.game_state.calculate_dev_cost(dummy)

        self.audio.speak(
            self.game_state.get_text('dev_slider_explain', 
                                     name=d.get('name','?'), 
                                     topic=d.get('topic','?'), 
                                     genre=d.get('genre','?'), 
                                     platform=d.get('platform','?'), 
                                     cost=cost, 
                                     budget=self.budget)
        )
        self._speak_current()

    def _confirm(self, values):
        self.game_state.current_draft['sliders'] = values

        # Entwicklungsfortschritt anzeigen
        self.audio.speak(
            self.game_state.get_text('dev_started')
        )
        return "dev_progress_menu"

    def _cancel(self):
        return "game_name_input"


class DevProgressMenu(Menu):
    """Zeigt Entwicklungsfortschritt in Phasen."""

    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('dev_progress'), [], audio, game_state)
        self.last_announced_percent = -1
        self.is_polishing = False
        self.last_bug_count = -1

    def announce_entry(self):
        self.game_state.is_developing = True
        self.game_state.dev_progress = 0
        self.game_state.current_bugs = 0
        
        # Zeit berechnen
        from game_data import GAME_SIZES, DEV_PHASES
        size_data = next((s for s in GAME_SIZES if s["name"] == self.game_state.current_draft["size"]), GAME_SIZES[1])
        self.game_state.dev_total_weeks = int(sum(p["duration_weeks"] for p in DEV_PHASES) * size_data["time_multi"])
        
        self.audio.speak(self.game_state.get_text('dev_started', name=self.game_state.current_draft['name'], weeks=self.game_state.dev_total_weeks))
        self.options = []
        self.last_announced_percent = -1

    def update(self):
        if not self.game_state.is_developing:
            return

        percent = int((self.game_state.dev_progress / self.game_state.dev_total_weeks) * 100)
        
        if percent % 25 == 0 and percent != self.last_announced_percent and percent <= 100:
            self.audio.speak(self.game_state.get_text('dev_percent', percent=percent, bugs=self.game_state.current_bugs, hype=self.game_state.hype))
            self.last_announced_percent = percent

        if self.game_state.dev_progress >= self.game_state.dev_total_weeks:
            if not self.is_polishing and not self.options:
                self._show_finish_options()
            elif self.is_polishing:
                # Während Polishing: Ansage bei Bug-Änderung
                if self.game_state.current_bugs != self.last_bug_count:
                    self.audio.speak(self.game_state.get_text('polish_bugs', bugs=self.game_state.current_bugs))
                    self.last_bug_count = self.game_state.current_bugs
                    # Menü wieder einblenden nach jeder Woche oder per Taste?
                    # Wir lassen es über handle_input steuern.

    def _show_finish_options(self):
        self.options = [
            {'text': self.game_state.get_text('finish_dev'), 'action': self._finalize},
            {'text': self.game_state.get_text('polishing'), 'action': self._polish},
        ]
        self.current_index = 0
        self.audio.speak(self.game_state.get_text('dev_finished_prompt'))
        self.speak_current()

    def _finalize(self):
        from models import GameProject
        self.game_state.is_developing = False
        project = GameProject(
            name=self.game_state.current_draft['name'],
            topic=self.game_state.current_draft['topic'],
            genre=self.game_state.current_draft['genre'],
            sliders=self.game_state.current_draft['sliders'],
            platform=self.game_state.current_draft['platform'],
            audience=self.game_state.current_draft['audience'],
            engine=self.game_state.current_draft['engine'],
            size=self.game_state.current_draft['size'],
            marketing=self.game_state.current_draft['marketing']
        )
        project.bugs = self.game_state.current_bugs
        self.game_state.finalize_game(project)
        return "review_result"

    def _polish(self):
        self.audio.speak(self.game_state.get_text('polish_active'))
        self.is_polishing = True
        self.last_bug_count = self.game_state.current_bugs
        self.options = [] 
        return None

    def handle_input(self, event):
        if not self.options:
            # Wenn kein Menü da ist (während Entwicklung oder Polishing), 
            # öffne es bei Enter während Polishing wieder
            if self.is_polishing and event.key in [pygame.K_RETURN, pygame.K_UP, pygame.K_DOWN]:
                self._show_finish_options()
            return None
        return super().handle_input(event)


# ============================================================
# REVIEW-ERGEBNIS
# ============================================================

class ReviewResultMenu(Menu):
    def __init__(self, audio, game_state):
        options = [
            {'text': game_state.get_text('back'), 'action': self._continue},
            {'text': game_state.get_text('quit'), 'action': self._quit},
        ]
        super().__init__(game_state.get_text('review_result'), options, audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        from models import GameProject

        d = self.game_state.current_draft
        project = GameProject(
            name=d['name'], topic=d['topic'], genre=d['genre'],
            sliders=d['sliders'], platform=d.get('platform', 'PC'),
            audience=d.get('audience', 'Jugendliche'),
            engine=d.get('engine'),
            size=d.get('size', 'Mittel'),
            marketing=d.get('marketing', 'Kein Marketing')
        )

        project = self.game_state.finalize_game(project)

        self.audio.speak(self.game_state.get_text('review_intro', name=project.name))

        for i, score in enumerate(project.review.scores):
            self.audio.speak(self.game_state.get_text('review_score_reviewer', i=i+1, score=score), interrupt=False)

        self.audio.speak(
            self.game_state.get_text('review_average', avg=project.review.average),
            interrupt=False,
        )
        # NEU: Detaillierte Berichte sprechen
        for comment in project.review.comments:
            self.audio.speak(comment, interrupt=False)
        self.audio.play_sound("cash")
        self.audio.speak(
            self.game_state.get_text('dev_result_sales', sales=project.sales, revenue=project.revenue, cost=project.dev_cost, profit=project.profit),
            interrupt=False,
        )
        self.audio.speak(
            self.game_state.get_text('dev_result_money', money=self.game_state.money, fans=self.game_state.fans),
            interrupt=False,
        )
        self.speak_current(interrupt=False)

    def _continue(self):
        self.game_state.reset_draft()
        return "game_menu"

    def _quit(self):
        self.game_state.save_game()
        self.audio.speak(self.game_state.get_text('game_saved_exit'))
        return "quit"


# ============================================================
# PERSONAL-ABTEILUNG
# ============================================================

class HRMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        options = [
            {'text': game_state.get_text('hire_employee'), 'action': self.hire},
            {'text': game_state.get_text('show_employees'), 'action': self.show_employees},
            {'text': game_state.get_text('train_employee'), 'action': self.train},
            {'text': game_state.get_text('fire_employee'), 'action': self.fire},
            {'text': game_state.get_text('back'), 'action': self.back},
        ]
        super().__init__(game_state.get_text('hr_department'), options, audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        gs = self.game_state
        max_emp = gs.get_max_employees()
        self.audio.speak(self.game_state.get_text('hr_department_status', current=len(gs.employees), max_emp=max_emp))
        self.speak_current(interrupt=False)

    def hire(self):
        if not self.game_state.can_hire():
            office = OFFICE_LEVELS[self.game_state.office_level]
            self.audio.speak(self.game_state.get_text('hr_no_space', office=office['name'], max_emp=office['max_employees']))
            return None
        return "hire_menu"

    def show_employees(self):
        if not self.game_state.employees:
            self.audio.speak(self.game_state.get_text('hr_no_employees'))
            return None
        for i, emp in enumerate(self.game_state.employees, 1):
            self.audio.speak(f"{i}. {emp.detail()}", interrupt=False)
        return None

    def train(self):
        if not self.game_state.employees:
            self.audio.speak(self.game_state.get_text('hr_no_employees_train'))
            return None
        return "training_employee_select"

    def fire(self):
        if not self.game_state.employees:
            self.audio.speak(self.game_state.get_text('hr_no_employees_fire'))
            return None
        return "fire_menu"

    def back(self):
        return "game_menu"


class HireMenu(Menu):
    """Zeigt 3 zufällige Bewerber."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.candidates = []
        super().__init__(game_state.get_text('candidates'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.candidates = [self.game_state.generate_candidate() for _ in range(3)]
        self.options = []
        for c in self.candidates:
            hire_cost = c.salary * 2
            spec_text = self.game_state.get_text('hire_spec_text', spec=c.specialization['name']) if c.specialization else ""
            self.options.append({
                'text': self.game_state.get_text('hire_candidate_desc', name=c.name, role=c.role, level=c.skill_level, salary=c.salary, spec=spec_text, cost=hire_cost),
                'action': lambda emp=c: self._hire(emp),
            })
        self.options.append({'text': self.game_state.get_text('refresh_candidates'), 'action': self._refresh})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

        self.audio.speak(self.game_state.get_text('hire_candidates_available'))
        self.speak_current(interrupt=False)

    def _hire(self, emp):
        hire_cost = emp.salary * 2
        if self.game_state.money < hire_cost:
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=hire_cost))
            return None
        if self.game_state.hire_employee(emp):
            self.audio.speak(self.game_state.get_text('hire_success', name=emp.name, cost=hire_cost, money=self.game_state.money))
            return "hr_menu"
        self.audio.speak(self.game_state.get_text('hire_fail'))
        return None

    def _refresh(self):
        return "hire_menu"

    def _cancel(self):
        return "hr_menu"


class FireMenu(Menu):
    """Zeigt aktuelle Mitarbeiter zum Entlassen."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('fire_employee'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        for i, emp in enumerate(self.game_state.employees):
            abfindung = emp.salary * 4
            self.options.append({
                'text': self.game_state.get_text('fire_desc', name=emp.name, role=emp.role, cost=abfindung),
                'action': lambda idx=i: self._fire(idx),
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})
        self.audio.speak(self.game_state.get_text('fire_ask'))
        self.speak_current(interrupt=False)

    def _fire(self, index):
        emp = self.game_state.fire_employee(index)
        if emp:
            self.audio.speak(self.game_state.get_text('fire_success', name=emp.name, money=self.game_state.money))
        return "hr_menu"

    def _cancel(self):
        return "hr_menu"


# ============================================================
# FORSCHUNG & ENGINE
# ============================================================

class ResearchMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        options = [
            {'text': game_state.get_text('research_feature'), 'action': self.research},
            {'text': game_state.get_text('create_engine_option'), 'action': self.create_engine},
            {'text': game_state.get_text('show_engines_option'), 'action': self.show_engines},
            {'text': game_state.get_text('hardware_dev_option'), 'action': self.goto_hardware},
            {'text': game_state.get_text('back'), 'action': self.back},
        ]
        super().__init__(game_state.get_text('research_engines'), options, audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        researchable = self.game_state.get_researchable_features()
        self.audio.speak(self.game_state.get_text('research_menu_status', features=len(self.game_state.unlocked_features), new=len(researchable), engines=len(self.game_state.engines)))
        self.speak_current(interrupt=False)

    def research(self):
        return "feature_research_menu"

    def create_engine(self):
        return "engine_create_name"

    def show_engines(self):
        for eng in self.game_state.engines:
            self.audio.speak(eng.summary(), interrupt=False)
        return None

    def goto_hardware(self):
        return "hardware_dev_menu"

    def back(self):
        return "game_menu"


class FeatureResearchMenu(Menu):
    """Zeigt erforschbare Features."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('research_feature'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        researchable = self.game_state.get_researchable_features()
        self.options = []
        for f in researchable:
            self.options.append({
                'text': self.game_state.get_text('research_feature_desc', name=f['name'], category=f['category'], cost=f['cost'], bonus=f['tech_bonus']),
                'action': lambda fd=f: self._research(fd),
            })
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_features_available'), 'action': lambda: None})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

        self.audio.speak(self.game_state.get_text('research_features_available', count=len(researchable)))
        self.speak_current(interrupt=False)

    def _research(self, feature_data):
        if self.game_state.research_feature(feature_data):
            self.audio.speak(self.game_state.get_text('research_success', name=feature_data['name'], money=self.game_state.money))
            return "research_menu"
        else:
            self.audio.speak(self.game_state.get_text('research_fail'))
            return None

    def _cancel(self):
        return "research_menu"


class EngineCreateNameMenu(TextInputMenu):
    """Name für neue Engine eingeben."""

    def __init__(self, audio, game_state):
        super().__init__(
            title=game_state.get_text('create_engine_option'),
            prompt=game_state.get_text('engine_name_prompt'),
            audio=audio,
            game_state=game_state,
            on_confirm=self._confirm,
            on_cancel=self._cancel,
        )
        self._engine_name = ""

    def _confirm(self, name):
        self._engine_name = name
        self.game_state._pending_engine_name = name
        return "engine_feature_select"

    def _cancel(self):
        return "research_menu"


class EngineFeatureSelectMenu(Menu):
    """Features für die neue Engine auswählen (Toggle-basiert)."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.selected_features = []
        super().__init__(game_state.get_text('select_engine_features'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.selected_features = []
        self.options = []

        # Gruppieren nach Kategorie, nur freigeschaltete
        categories = {}
        for f in self.game_state.unlocked_features:
            categories.setdefault(f.category, []).append(f)

        # Bestes Feature pro Kategorie anzeigen
        for cat, features in sorted(categories.items()):
            best = max(features, key=lambda x: x.tech_bonus)
            self.options.append({
                'text': f"[  ] {best.name} ({cat}, Tech: +{best.tech_bonus})",
                'action': lambda feat=best: self._toggle(feat),
                '_feature': best,
                '_selected': False,
            })

        self.options.append({'text': self.game_state.get_text('create_engine_option'), 'action': self._create})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

        name = getattr(self.game_state, '_pending_engine_name', 'Neue Engine')
        self.audio.speak(self.game_state.get_text('engine_select_features', name=name))
        self.speak_current(interrupt=False)

    def _toggle(self, feature):
        if feature in self.selected_features:
            self.selected_features.remove(feature)
            status = "abgewählt"
        else:
            self.selected_features.append(feature)
            status = "ausgewählt"

        # Update option text
        for opt in self.options:
            if opt.get('_feature') == feature:
                mark = "[X]" if feature in self.selected_features else "[  ]"
                opt['text'] = f"{mark} {feature.name} ({feature.category}, Tech: +{feature.tech_bonus})"
                break

        self.audio.speak(
            f"{feature.name} {status}. {len(self.selected_features)} Features gewählt."
        )
        return None

    def _create(self):
        if not self.selected_features:
            self.audio.speak(self.game_state.get_text('engine_create_fail'))
            return None

        name = getattr(self.game_state, '_pending_engine_name', 'Neue Engine')
        engine = self.game_state.create_engine(name, list(self.selected_features))
        self.audio.speak(self.game_state.get_text('engine_create_success', name=engine.name, level=engine.tech_level))
        return "research_menu"

    def _cancel(self):
        return "research_menu"


# ============================================================
# BÜRO
# ============================================================

class OfficeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        options = [
            {'text': game_state.get_text('upgrade_office'), 'action': self.upgrade},
            {'text': game_state.get_text('back'), 'action': self.back},
        ]
        super().__init__(game_state.get_text('office_management'), options, audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        office = self.game_state.get_office_info()
        self.audio.speak(self.game_state.get_text('office_status', name=office['name'], max=office['max_employees']))
        if self.game_state.office_level < len(OFFICE_LEVELS) - 1:
            next_office = OFFICE_LEVELS[self.game_state.office_level + 1]
            self.audio.speak(
                self.game_state.get_text('office_upgrade_available', name=next_office['name'], cost=next_office['cost'], max=next_office['max_employees']),
                interrupt=False
            )
        else:
            self.audio.speak(self.game_state.get_text('office_max_reached'), interrupt=False)
        self.speak_current(interrupt=False)

    def upgrade(self):
        if self.game_state.upgrade_office():
            office = self.game_state.get_office_info()
            self.audio.speak(self.game_state.get_text('office_upgrade_success', name=office['name'], max=office['max_employees'], money=self.game_state.money))
        elif self.game_state.office_level >= len(OFFICE_LEVELS) - 1:
            self.audio.speak(self.game_state.get_text('office_max_reached'))
        else:
            next_cost = OFFICE_LEVELS[self.game_state.office_level + 1]['cost']
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=next_cost))
        return None

    def back(self):
        return "game_menu"


# ============================================================
# TRAINING-MENÜS
# ============================================================

class TrainingEmployeeSelectMenu(Menu):
    """Wähle einen Mitarbeiter für das Training."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('select_employee_training'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        for i, emp in enumerate(self.game_state.employees):
            self.options.append({
                'text': f"{emp.name} ({emp.role})",
                'action': lambda idx=i: self._select(idx)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})
        self.audio.speak(self.game_state.get_text('train_select'))
        self.speak_current(interrupt=False)

    def _select(self, index):
        self.game_state._pending_train_emp_index = index
        return "training_option_select"


class TrainingOptionMenu(Menu):
    """Wähle eine Trainings-Option."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('select_training'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        emp_idx = getattr(self.game_state, '_pending_train_emp_index', 0)
        if not self.game_state.employees or emp_idx >= len(self.game_state.employees):
            self.audio.speak(self.game_state.get_text('hr_show_none'))
            return
        emp = self.game_state.employees[emp_idx]
        
        self.options = []
        for train in TRAINING_OPTIONS:
            self.options.append({
                'text': self.game_state.get_text('train_option_desc', name=train['name'], desc=train['description'], cost=train['cost']),
                'action': lambda t=train: self._train(emp_idx, t)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})
        self.audio.speak(self.game_state.get_text('train_choose', name=emp.name))
        self.speak_current(interrupt=False)

    def _train(self, emp_idx, train_data):
        if self.game_state.train_employee(emp_idx, train_data):
            emp = self.game_state.employees[emp_idx]
            self.audio.speak(self.game_state.get_text('train_success', name=emp.name, salary=emp.salary, money=self.game_state.money))
            return "hr_menu"
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=train_data['cost']))
            return None


# ============================================================
# PLEITE-MENÜ
# ============================================================

class BankruptcyMenu(Menu):
    def __init__(self, audio, game_state):
        options = [
            {'text': game_state.get_text('main_menu'), 'action': lambda: "main_menu"},
            {'text': game_state.get_text('quit'), 'action': lambda: "quit"},
        ]
        super().__init__(game_state.get_text('bankruptcy'), options, audio, game_state)

    def announce_entry(self):
        self.audio.speak(self.game_state.get_text('bankruptcy_text'))


# ============================================================
# NEU: E-MAIL & SERVICE
# ============================================================

class EmailInboxMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('inbox'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        for i, mail in enumerate(self.game_state.emails):
            status = "" if mail.is_read else self.game_state.get_text('email_status_new')
            self.options.append({
                'text': f"{status}{mail.subject} ({self.game_state.get_text('week')} {mail.date_week})",
                'action': lambda idx=i: self._read_mail(idx)
            })
        self.options.append({'text': self.game_state.get_text('email_inbox_back'), 'action': lambda: "game_menu"})
        
        unread = len([m for m in self.game_state.emails if not m.is_read])
        self.audio.speak(self.game_state.get_text('email_inbox', total=len(self.game_state.emails), unread=unread))
        self.speak_current(interrupt=False)

    def _read_mail(self, index):
        self.game_state._pending_email_index = index
        return "email_detail"


class EmailDetailMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('email_details'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        idx = getattr(self.game_state, '_pending_email_index', 0)
        if not self.game_state.emails or idx >= len(self.game_state.emails):
            self.audio.speak(self.game_state.get_text('inbox_empty'))
            return
        mail = self.game_state.emails[idx]
        mail.is_read = True
        
        self.options = [
            {'text': self.game_state.get_text('reply_ok'), 'action': lambda: "email_inbox"},
            {'text': self.game_state.get_text('delete'), 'action': lambda: self._delete(idx)}
        ]
        
        self.audio.speak(self.game_state.get_text('email_detail', sender=mail.sender, subject=mail.subject))
        self.audio.speak(mail.body, interrupt=False)
        self.speak_current(interrupt=False)

    def _delete(self, index):
        self.game_state.emails.pop(index)
        return "email_inbox"


class ServiceMenu(Menu):
    """Management von Patches und DLCs."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('service_support'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        # Nur aktive oder verbuggte Spiele
        for i, game in enumerate(self.game_state.game_history):
            if game.is_active or game.bugs > 0:
                self.options.append({
                    'text': self.game_state.get_text('service_game_desc', name=game.name, bugs=game.bugs, dlcs=game.dlc_count),
                    'action': lambda idx=i: self._manage_game(idx)
                })
        
        self.options.append({'text': self.game_state.get_text('service_back'), 'action': lambda: "game_menu"})
        self.audio.speak(self.game_state.get_text('service_select'))
        self.speak_current(interrupt=False)

    def _manage_game(self, index):
        self.game_state._pending_service_game_index = index
        return "game_service_options"


class GameServiceOptionsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('update_options'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        idx = getattr(self.game_state, '_pending_service_game_index', 0)
        game = self.game_state.game_history[idx]
        
        self.options = [
            {'text': self.game_state.get_text('free_patch', bugs=game.bugs), 'action': lambda: self._patch(idx)},
            {'text': self.game_state.get_text('release_dlc_option'), 'action': lambda: self._dlc(idx)},
            {'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"}
        ]
        self.audio.speak(self.game_state.get_text('service_options', name=game.name))
        self.speak_current(interrupt=False)

    def _patch(self, idx):
        if self.game_state.release_patch(idx):
            self.audio.speak(self.game_state.get_text('patch_success'))
        else:
            self.audio.speak(self.game_state.get_text('patch_fail'))
        return "service_menu"

    def _dlc(self, idx):
        if self.game_state.release_dlc(idx):
            self.audio.speak(self.game_state.get_text('dlc_success'))
        else:
            self.audio.speak(self.game_state.get_text('dlc_fail'))
        return "service_menu"


# ============================================================
# SPEICHER- SLOTS & HILFE
# ============================================================

class LoadMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('select_slot'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        slots = self.game_state.get_save_slots_info()
        self.options = []
        for i in range(1, 4):
            self.options.append({
                'text': slots[i],
                'action': lambda s=i: self._load(s)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "main_menu"})
        self.audio.speak(self.game_state.get_text('select_slot'))
        self.speak_current(interrupt=False)

    def _load(self, slot):
        if self.game_state.load_game(slot):
            self.audio.speak(self.game_state.get_text('game_loaded'))
            return "game_menu"
        self.audio.speak(self.game_state.get_text('no_savegame'))
        return None


class SaveMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('select_slot'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        slots = self.game_state.get_save_slots_info()
        self.options = []
        for i in range(1, 4):
            self.options.append({
                'text': slots[i],
                'action': lambda s=i: self._save(s)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        self.audio.speak(self.game_state.get_text('select_slot'))
        self.speak_current(interrupt=False)

    def _save(self, slot):
        if self.game_state.save_game(slot):
            self.audio.speak(self.game_state.get_text('game_saved', slot=slot))
            return "game_menu"
        return None


class HelpMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        options = [
            {'text': game_state.get_text('wiki_concept'), 'action': lambda: self._speak_key('wiki_concept')},
            {'text': game_state.get_text('wiki_dev'), 'action': lambda: self._speak_key('wiki_dev')},
            {'text': game_state.get_text('wiki_hr'), 'action': lambda: self._speak_key('wiki_hr')},
            {'text': game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]
        super().__init__(game_state.get_text('wiki'), options, audio, game_state)

    def _speak_key(self, key):
        self.audio.speak(self.game_state.get_text(key))
        return None

class PublisherMenu(Menu):
    """Auswahl eines Publishers."""

    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('select_publisher'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        from game_data import PUBLISHERS
        self.options = [
            {'text': self.game_state.get_text('self_publish'), 'action': lambda: self._select(None)}
        ]
        for pub in PUBLISHERS:
            self.options.append({
                'text': f"{pub['name']} (Vorschuss: {pub['advance']:,}, Royalties: {int(pub['royalty']*100)}%)",
                'action': lambda p=pub: self._select(p)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "marketing_menu"})
        self.speak_current()

    def _select(self, publisher):
        self.game_state.current_draft['publisher'] = publisher
        if publisher:
            self.audio.speak(self.game_state.get_text('publisher_contract', name=publisher['name']))
        else:
            self.audio.speak(self.game_state.get_text('publisher_self'))
        return "engine_select_menu"

class ExpoMenu(Menu):
    """Die Audio Expo (Woche 26)."""
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('expo_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = [
            {'text': self.game_state.get_text('expo_small'), 'action': lambda: self._attend(5000, 20)},
            {'text': self.game_state.get_text('expo_large'), 'action': lambda: self._attend(20000, 60)},
            {'text': self.game_state.get_text('expo_none'), 'action': lambda: "game_menu"}
        ]
        self.audio.speak(self.game_state.get_text('expo_prompt'))
        self.speak_current()

    def _attend(self, cost, hype):
        if self.game_state.money < cost:
            self.audio.speak(self.game_state.get_text('expo_fail'))
            return None
        self.game_state.money -= cost
        self.game_state.hype += hype
        self.audio.speak(self.game_state.get_text('expo_success', hype=hype))
        return "game_menu"

# ============================================================
# EIGENE HARDWARE (Endgame)
# ============================================================

class HardwareDevMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('hardware_dev_option'), [], audio, game_state)

    def announce_entry(self):
        self.audio.speak(self.game_state.get_text('hardware_welcome'))
        self.options = [
            {'text': self.game_state.get_text('hardware_new'), 'action': self.goto_console_name},
            {'text': self.game_state.get_text('back'), 'action': self._cancel}
        ]
        self.speak_current(interrupt=False)

    def goto_console_name(self):
        return "console_name_input"

    def _cancel(self):
        return "research_menu"

class ConsoleNameInput(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('hardware_name'), game_state.get_text('hardware_prompt'), audio, game_state, self._confirm, self._cancel)
        
    def _confirm(self, name):
        self.game_state.current_console_draft = {"name": name, "tech_level": 1, "cost": 10000000}
        self.audio.speak(self.game_state.get_text('hardware_confirm', name=name))
        return "console_specs_menu"

    def _cancel(self):
        return "hardware_dev_menu"

class ConsoleSpecsMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('hardware_specs'), [], audio, game_state)
        self.game_state = game_state
        self.features = [
            {"name": self.game_state.get_text('hw_feat_cd_dvd'), "cost": 3000000, "tech": 1},
            {"name": self.game_state.get_text('hw_feat_3d_gfx'), "cost": 5000000, "tech": 2},
            {"name": self.game_state.get_text('hw_feat_online'), "cost": 4000000, "tech": 1},
            {"name": self.game_state.get_text('hw_feat_wireless'), "cost": 2000000, "tech": 1},
        ]
        self.selected = []

    def announce_entry(self):
        self.options = []
        for f in self.features:
            status = self.game_state.get_text('hardware_spec_chosen') if f in self.selected else self.game_state.get_text('hardware_spec_not_chosen')
            self.options.append({
                'text': self.game_state.get_text('hardware_spec_option', name=f['name'], cost=f['cost'], status=status),
                'action': lambda feat=f: self._toggle(feat)
            })
        
        draft = self.game_state.current_console_draft
        total_cost = 10000000 + sum(f['cost'] for f in self.selected)
        total_tech = 1 + sum(f['tech'] for f in self.selected)
        
        self.options.append({
            'text': self.game_state.get_text('hardware_dev_start', cost=total_cost, tech=total_tech),
            'action': self._start_dev
        })
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})
        self.audio.speak(self.game_state.get_text('hardware_choose_specs'))
        self.speak_current(interrupt=False)

    def _toggle(self, f):
        if f in self.selected:
            self.selected.remove(f)
            self.audio.speak(self.game_state.get_text('hardware_deselected', name=f['name']))
        else:
            self.selected.append(f)
            self.audio.speak(self.game_state.get_text('hardware_selected', name=f['name']))
        self.announce_entry()
        return None

    def _start_dev(self):
        total_cost = 10000000 + sum(f['cost'] for f in self.selected)
        if self.game_state.money < total_cost:
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=total_cost))
            return None
        
        self.game_state.money -= total_cost
        draft = self.game_state.current_console_draft
        draft['cost'] = total_cost
        draft['tech_level'] = 1 + sum(f['tech'] for f in self.selected)
        
        self.game_state.is_developing_console = True
        self.game_state.console_progress = 0
        self.game_state.console_total_weeks = 50
        
        self.audio.speak(self.game_state.get_text('hardware_start_dev', name=draft['name']))
        self.selected = []
        return "game_menu"

    def _cancel(self):
        return "console_name_input"

# ============================================================
# GAME OF THE YEAR CEREMONY
# ============================================================

class GOTYMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('goty_title'), [], audio, game_state)
        
    def announce_entry(self):
        self.options = []
        goty = getattr(self.game_state, "pending_goty_results", None)
        if not goty:
            self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})
            self.audio.speak(self.title)
            self.speak_current(interrupt=False)
            return

        # Trommelwirbel (wenn Datei fehlt, wird es ignoriert)
        self.audio.play_sound('drumroll') 

        year = goty["year"]
        my_score = goty["my_score"]
        my_game = goty["my_game"]
        rival_score = goty["rival_score"]
        rival_name = goty["rival_name"]
        rival_game = goty["rival_game"]

        if my_score > rival_score and my_score >= 8.0:
            msg = self.game_state.get_text('goty_ceremony_win', year=year, game=my_game)
            # Bonus sound
            self.audio.play_sound('success')
        else:
            winner = rival_name if rival_name else "Niemand"
            win_game = rival_game if rival_game else "Nichts"
            msg = self.game_state.get_text('goty_ceremony_lose', year=year, winner=winner, game=win_game)
            
        self.audio.speak(msg)
        self.options.append({'text': self.game_state.get_text('continue_btn'), 'action': self._cancel})
        # Wir warten kurz, damit der Sound wirkt
        import time
        time.sleep(1.0)
        self.speak_current(interrupt=False)

    def _cancel(self):
        self.game_state.pending_goty_results = None
        return "game_menu"
