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
from models import GameProject
from game_data import (
    GENRES, SLIDER_NAMES, AUDIENCES,
    OFFICE_LEVELS, GAME_SIZES,
    TRAINING_OPTIONS,
    get_compatibility, get_compatibility_text,
    get_available_platforms,
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
        return "difficulty_menu"

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
            title='company_creation_title',
            prompt='company_name_prompt',
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
        ]
        # Sequel-Option nur zeigen wenn es bereits Spiele gibt
        if game_state.game_history:
            options.append({'text': game_state.get_text('sequel_label'), 'action': self.goto_sequel})
        options.append({'text': game_state.get_text('hr_department'), 'action': self.goto_hr})
        
        # Audio Expo Spezial-Option
        week_in_year = (self.game_state.week - 1) % 52 + 1
        if week_in_year == 26:
            options.append({'text': self.game_state.get_text('expo_title'), 'action': self.goto_expo})

        # NEU: Phase C - Produktion
        if getattr(self.game_state, 'has_presswerk', False):
            options.append({'text': self.game_state.get_text('production_menu_title'), 'action': self.goto_production})

        # NEU: Phase D - MMO Verwaltung
        if getattr(self.game_state, 'active_mmos', []):
            options.append({'text': self.game_state.get_text('mmo_management_title'), 'action': self.goto_mmo_management})

        # NEU: Phase E - Publisher Angebote
        if getattr(self.game_state, 'publishing_offers', []):
             options.append({'text': self.game_state.get_text('publisher_deals_title'), 'action': self.goto_publisher_deals})

        options.extend([
            {'text': game_state.get_text('research_engines'), 'action': self.goto_research},
            {'text': game_state.get_text('service_support'), 'action': self.goto_service},
            {'text': game_state.get_text('inbox'), 'action': self.goto_inbox},
            {'text': game_state.get_text('finances_and_bank'), 'action': self.goto_bank},
            {'text': game_state.get_text('menu_licenses'), 'action': self.goto_licenses},
            {'text': game_state.get_text('menu_addons'), 'action': self.goto_addons},
            {'text': game_state.get_text('menu_bundles'), 'action': self.goto_bundles},
            {'text': game_state.get_text('chart_option'), 'action': self.goto_charts},
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
            # Events können 'title'/'text' ODER nur 'id' haben
            title = event.get('title', self.game_state.get_text('event_' + event.get('id', 'unknown')))
            text = event.get('text', '')
            self.audio.speak(self.game_state.get_text('random_event_alert', title=title, text=text))
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

    def goto_charts(self):
        return "chart_menu"

    def goto_production(self):
        return "production_menu"

    def goto_mmo_management(self):
        return "mmo_management_menu"

    def goto_publisher_deals(self):
        return "publisher_deals_menu"

    def goto_sequel(self):
        self.game_state.reset_draft()
        return "sequel_menu"

    def show_status(self):
        self.audio.speak(self.game_state.get_status_text())
        return None

    def new_game(self):
        self.game_state.reset_draft()
        return "license_select_menu"

    def goto_licenses(self):
        return "license_shop_menu"

    def goto_addons(self):
        return "addon_menu"

    def goto_bundles(self):
        return "bundle_menu"

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
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('select_topic'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        for topic in self.game_state.unlocked_topics:
            self.options.append({'text': topic, 'action': lambda t=topic: self._select(t)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})
        self.audio.speak(self.title)
        self.speak_current(interrupt=False)

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

        # Aktienmarkt nur verfügbar, wenn Technologie erforscht
        if "Investment & M&A" in getattr(self.game_state, 'unlocked_technologies', []):
            self.options.append({'text': self.game_state.get_text('stock_market_option'), 'action': self.goto_stock_market})

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

    def goto_stock_market(self):
        return "stock_market_menu"

    def _cancel(self):
        return "game_menu"


class LoanMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('loan_offers_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        
        loans = [
            {"name": self.game_state.get_text('loan_small'), "amount": 50000, "interest": 0.10, "weeks": 52},
            {"name": self.game_state.get_text('loan_medium'), "amount": 250000, "interest": 0.15, "weeks": 104},
            {"name": self.game_state.get_text('loan_large'), "amount": 1000000, "interest": 0.20, "weeks": 208},
        ]
        
        self.options = []
        for loan_item in loans:
            l_num = int(str(loan_item['amount']))
            i_num = float(str(loan_item['interest']))
            w_num = int(str(loan_item['weeks']))
            repay = int(l_num * (1.0 + i_num))
            self.options.append({
                'text': self.game_state.get_text('loan_option_desc', name=loan_item['name'], amount=l_num, repay=repay, weeks=w_num),
                'action': lambda loan=loan_item: self._take_loan(loan)
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


class StockMarketMenu(Menu):
    """Aktienmarkt: Anteile an Rivalen-Studios kaufen und verkaufen."""

    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('stock_market_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self._build_options()
        self.audio.speak(self.game_state.get_text('stock_market_intro'))
        self.speak_current(interrupt=False)

    def _build_options(self):
        self.options = []
        for i, rival in enumerate(self.game_state.rivals):
            shares = rival.owned_shares
            buy_price = self.game_state.get_share_price(rival)
            sell_price = int(buy_price * 0.8)

            # Info-Zeile
            self.options.append({
                'text': self.game_state.get_text('stock_buy_desc', name=rival.name, shares=shares, price=buy_price),
                'action': lambda: None
            })

            # Kauf-Option (max 50%)
            if shares < 50:
                self.options.append({
                    'text': self.game_state.get_text('stock_buy_option', name=rival.name, price=buy_price),
                    'action': lambda idx=i: self._buy(idx)
                })

            # Verkauf-Option
            if shares > 0:
                self.options.append({
                    'text': self.game_state.get_text('stock_sell_option', name=rival.name, price=sell_price),
                    'action': lambda idx=i: self._sell(idx)
                })

        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

    def _buy(self, rival_index):
        rival = self.game_state.rivals[rival_index]
        price = self.game_state.get_share_price(rival)

        if rival.owned_shares >= 50:
            self.audio.speak(self.game_state.get_text('stock_max_shares', name=rival.name))
            return None
        if self.game_state.money < price:
            self.audio.speak(self.game_state.get_text('stock_not_enough_money', price=price))
            return None

        success, new_shares = self.game_state.buy_shares(rival_index)
        if success:
            self.audio.speak(self.game_state.get_text('stock_buy_success', name=rival.name, shares=new_shares, money=self.game_state.money))
            self._build_options()
            self.current_index = 0
        return None

    def _sell(self, rival_index):
        rival = self.game_state.rivals[rival_index]

        if rival.owned_shares <= 0:
            self.audio.speak(self.game_state.get_text('stock_no_shares', name=rival.name))
            return None

        success, new_shares = self.game_state.sell_shares(rival_index)
        if success:
            self.audio.speak(self.game_state.get_text('stock_sell_success', name=rival.name, shares=new_shares, money=self.game_state.money))
            self._build_options()
            self.current_index = 0
        return None

    def _cancel(self):
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
        return "sub_genre_menu"

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
        
        # Check min tech level
        if 'min_tech_level' in size_data:
            has_engine = any(e.tech_level >= size_data['min_tech_level'] for e in self.game_state.engines)
            if not has_engine:
                self.audio.speak(self.game_state.get_text('size_min_tech_level', size=size_data['name'], tech=size_data['min_tech_level']))
                return None
                
        # Check req tech
        if 'req_tech' in size_data:
            if size_data['req_tech'] not in self.game_state.unlocked_technologies:
                self.audio.speak(self.game_state.get_text('size_req_tech', size=size_data['name'], tech=size_data['req_tech']))
                return None
        
        self.game_state.current_draft['size'] = size_data['name']
        self.audio.speak(self.game_state.get_text('size_selected', size=size_data['name']))
        
        if size_data['name'] == 'MMO':
            return "mmo_payment_menu"
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
            title='game_name',
            prompt='game_name_prompt_short',
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
            self.game_state.get_text('dev_started_info', name=self.game_state.current_draft['name'], weeks=0) # Weeks will be updated in next menu
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
        # Zeit zuerst berechnen
        from game_data import GAME_SIZES, DEV_PHASES
        size_data = next((s for s in GAME_SIZES if s["name"] == self.game_state.current_draft["size"]), GAME_SIZES[1])
        self.game_state.dev_total_weeks = max(1, int(sum(p["duration_weeks"] for p in DEV_PHASES) * size_data["time_multi"]))
        
        self.game_state.is_developing = True
        self.game_state.dev_progress = 0
        self.game_state.current_bugs = 0
        
        self.audio.speak(self.game_state.get_text('dev_progress_start_info', name=self.game_state.current_draft['name'], weeks=self.game_state.dev_total_weeks))
        self.options = []
        self.last_announced_percent = -1

    def update(self):
        if not self.game_state.is_developing:
            return

        total = max(1, self.game_state.dev_total_weeks)
        percent = int((self.game_state.dev_progress / total) * 100)
        
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
        if 'license' in self.game_state.current_draft:
            project.license_bonus = self.game_state.current_draft['license']['review_bonus']

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
# AAA EVENT MENU
# ============================================================

class AAADevEventMenu(Menu):
    """Menü für zufällige Marketing-Events während der AAA-Entwicklung."""

    def __init__(self, audio, game_state):
        super().__init__("", [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        event = self.game_state.pending_dev_event
        if not event:
            return "dev_progress_menu"

        title = self.game_state.get_text(f"event_{event['id']}_title")
        text = self.game_state.get_text(f"event_{event['id']}_text")
        
        self.title_text = title
        self.audio.speak(f"Event: {title}! {text}")
        
        self.options = []
        for opt in event["options"]:
            label = self.game_state.get_text(f"event_{event['id']}_opt_{opt['id']}")
            self.options.append({
                'text': label,
                'action': lambda o=opt: self._apply_option(o)
            })
            
        self.speak_current(interrupt=False)

    def _apply_option(self, option):
        if option["cost"] > 0 and self.game_state.money < option["cost"]:
            self.audio.speak(self.game_state.get_text('research_not_enough_money'))
            return None
            
        self.game_state.money -= option["cost"]
        self.game_state.hype += option.get("hype", 0)
        self.game_state.current_bugs += option.get("bugs", 0)
        
        if option.get("morale", 0) != 0:
            for emp in self.game_state.employees:
                emp.morale = max(0, min(100, emp.morale + option["morale"]))

        self.audio.speak(self.game_state.get_text('event_aaa_resolved'))
        
        # Event zurücksetzen und wieder zurück zur Entwicklung
        self.game_state.pending_dev_event = None
        self.game_state.time_speed = 1.0 # Pause beenden
        return "dev_progress_menu"



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
            {'text': game_state.get_text('research_category_feature'), 'action': self.research_feature},
            {'text': game_state.get_text('research_category_topic'), 'action': self.research_topic},
            {'text': game_state.get_text('research_category_genre'), 'action': self.research_genre},
            {'text': game_state.get_text('research_category_audience'), 'action': self.research_audience},
            {'text': game_state.get_text('research_category_technology'), 'action': self.research_technology},
            {'text': game_state.get_text('create_engine_option'), 'action': self.create_engine},
            {'text': game_state.get_text('show_engines_option'), 'action': self.show_engines},
            {'text': game_state.get_text('hardware_dev_option'), 'action': self.goto_hardware},
            {'text': game_state.get_text('back'), 'action': self.back},
        ]
        super().__init__(game_state.get_text('research_engines'), options, audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        researchable_feat = len(self.game_state.get_researchable_features())
        researchable_top = len(self.game_state.get_researchable_topics())
        researchable_gen = len(self.game_state.get_researchable_genres())
        researchable_aud = len(self.game_state.get_researchable_audiences())
        researchable_tech = len(self.game_state.get_researchable_technologies())
        total_new = researchable_feat + researchable_top + researchable_gen + researchable_aud + researchable_tech
        
        self.audio.speak(self.game_state.get_text('research_menu_status', features=len(self.game_state.unlocked_features), new=total_new, engines=len(self.game_state.engines)))
        self.speak_current(interrupt=False)

    def research_feature(self): return "feature_research_menu"
    def research_topic(self): return "topic_research_menu"
    def research_genre(self): return "genre_research_menu"
    def research_audience(self): return "audience_research_menu"
    def research_technology(self): return "technology_research_menu"

    def create_engine(self): return "engine_create_name"
    
    def show_engines(self):
        for eng in self.game_state.engines:
            self.audio.speak(eng.summary(), interrupt=False)
        return None

    def goto_hardware(self): return "hardware_dev_menu"
    def back(self): return "game_menu"


class FeatureResearchMenu(Menu):
    """Zeigt erforschbare Features."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('research_category_feature'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        researchable = self.game_state.get_researchable_features()
        self.options = []
        for f in researchable:
            self.options.append({
                'text': f"{f['name']} ({f['category']}). {f.get('research_weeks', 4)} Wochen. Kosten: {f['cost']:,} Euro.",
                'action': lambda fd=f: self._research(fd),
            })
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_features_available'), 'action': lambda: None})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

        self.audio.speak(self.game_state.get_text('research_features_available', count=len(researchable)))
        self.speak_current(interrupt=False)

    def _research(self, feature_data):
        if self.game_state.start_research(feature_data, "feature"):
            self.audio.speak(self.game_state.get_text('research_started', name=feature_data['name'], weeks=feature_data.get('research_weeks', 4)))
            return "game_menu" # Zurück ins Hauptmenü
        else:
            if getattr(self.game_state, 'is_researching', False) or getattr(self.game_state, 'is_developing', False):
                self.audio.speak(self.game_state.get_text('research_already_active'))
            else:
                self.audio.speak(self.game_state.get_text('research_not_enough_money'))
            return None

    def _cancel(self):
        return "research_menu"


class GenreResearchMenu(Menu):
    """Zeigt erforschbare Genres."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('research_category_genre'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        researchable = self.game_state.get_researchable_genres()
        self.options = []
        for g in researchable:
            self.options.append({
                'text': f"{g['name']}. {g.get('research_weeks', 4)} Wochen. Kosten: {g['cost']:,} Euro.",
                'action': lambda gd=g: self._research(gd),
            })
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_features_available'), 'action': lambda: None})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

        self.audio.speak(self.game_state.get_text('research_features_available', count=len(researchable)))
        self.speak_current(interrupt=False)

    def _research(self, genre_data):
        if self.game_state.start_research(genre_data, "genre"):
            self.audio.speak(self.game_state.get_text('research_started', name=genre_data['name'], weeks=genre_data.get('research_weeks', 4)))
            return "game_menu"
        else:
            if getattr(self.game_state, 'is_researching', False) or getattr(self.game_state, 'is_developing', False):
                self.audio.speak(self.game_state.get_text('research_already_active'))
            else:
                self.audio.speak(self.game_state.get_text('research_not_enough_money'))
            return None

    def _cancel(self):
        return "research_menu"


class TopicResearchMenu(Menu):
    """Zeigt erforschbare Themen."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('research_category_topic'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        researchable = self.game_state.get_researchable_topics()
        self.options = []
        for t in researchable:
            self.options.append({
                'text': f"{t['name']}. {t.get('research_weeks', 4)} Wochen. Kosten: {t['cost']:,} Euro.",
                'action': lambda td=t: self._research(td),
            })
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_features_available'), 'action': lambda: None})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

        self.audio.speak(self.game_state.get_text('research_features_available', count=len(researchable)))
        self.speak_current(interrupt=False)

    def _research(self, topic_data):
        if self.game_state.start_research(topic_data, "topic"):
            self.audio.speak(self.game_state.get_text('research_started', name=topic_data['name'], weeks=topic_data.get('research_weeks', 4)))
            return "game_menu"
        else:
            if getattr(self.game_state, 'is_researching', False) or getattr(self.game_state, 'is_developing', False):
                self.audio.speak(self.game_state.get_text('research_already_active'))
            else:
                self.audio.speak(self.game_state.get_text('research_not_enough_money'))
            return None

    def _cancel(self):
        return "research_menu"

class AudienceResearchMenu(Menu):
    """Zeigt erforschbare Zielgruppen."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('research_category_audience'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        researchable = self.game_state.get_researchable_audiences()
        self.options = []
        for a in researchable:
            self.options.append({
                'text': f"{a['name']}. {a.get('research_weeks', 4)} Wochen. Kosten: {a['cost']:,} Euro.",
                'action': lambda ad=a: self._research(ad),
            })
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_features_available'), 'action': lambda: None})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

        self.audio.speak(self.game_state.get_text('research_features_available', count=len(researchable)))
        self.speak_current(interrupt=False)

    def _research(self, aud_data):
        if self.game_state.start_research(aud_data, "audience"):
            self.audio.speak(self.game_state.get_text('research_started', name=aud_data['name'], weeks=aud_data.get('research_weeks', 4)))
            return "game_menu"
        else:
            if getattr(self.game_state, 'is_researching', False) or getattr(self.game_state, 'is_developing', False):
                self.audio.speak(self.game_state.get_text('research_already_active'))
            else:
                self.audio.speak(self.game_state.get_text('research_not_enough_money'))
            return None

    def _cancel(self):
        return "research_menu"

class TechnologyResearchMenu(Menu):
    """Zeigt erforschbare Technologien für das Endgame."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('research_category_technology'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        researchable = self.game_state.get_researchable_technologies()
        self.options = []
        for t in researchable:
            self.options.append({
                'text': f"{t['name']} - {t['description']}. {t.get('research_weeks', 4)} Wochen. Kosten: {t['cost']:,} Euro.",
                'action': lambda td=t: self._research(td),
            })
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_features_available'), 'action': lambda: None})
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

        self.audio.speak(self.game_state.get_text('research_features_available', count=len(researchable)))
        self.speak_current(interrupt=False)

    def _research(self, tech_data):
        if self.game_state.start_research(tech_data, "technology"):
            self.audio.speak(self.game_state.get_text('research_started', name=tech_data['name'], weeks=tech_data.get('research_weeks', 4)))
            return "game_menu"
        else:
            if getattr(self.game_state, 'is_researching', False) or getattr(self.game_state, 'is_developing', False):
                self.audio.speak(self.game_state.get_text('research_already_active'))
            else:
                self.audio.speak(self.game_state.get_text('research_not_enough_money'))
            return None
    def _cancel(self):
        return "research_menu"


class EngineCreateNameMenu(TextInputMenu):
    """Name für neue Engine eingeben."""

    def __init__(self, audio, game_state):
        super().__init__(
            title='create_engine_option',
            prompt='engine_name_prompt',
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
        super().__init__(game_state.get_text('office_management'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        office = self.game_state.get_office_info()
        from game_data import OFFICE_LEVELS

        if self.game_state.office_level < len(OFFICE_LEVELS) - 1:
            next_office = OFFICE_LEVELS[self.game_state.office_level + 1]
            self.options.append({'text': self.game_state.get_text('upgrade_office_to', name=next_office['name'], cost=next_office['cost']), 'action': self.upgrade})

        if not getattr(self.game_state, 'has_presswerk', False) and self.game_state.office_level >= 2:
            self.options.append({'text': self.game_state.get_text('build_presswerk_option', cost=500000), 'action': self.build_presswerk})

        if getattr(self.game_state, 'has_presswerk', False):
            self.options.append({'text': self.game_state.get_text('expand_storage_option', cost=100000, current=self.game_state.storage_capacity), 'action': self.expand_storage})

        if not getattr(self.game_state, 'has_server_room', False) and self.game_state.office_level >= 3:
            self.options.append({'text': self.game_state.get_text('build_server_room_option', cost=1000000), 'action': self.build_server_room})

        if getattr(self.game_state, 'has_server_room', False):
            self.options.append({'text': self.game_state.get_text('expand_server_option', cost=250000, current=self.game_state.server_capacity), 'action': self.expand_server_capacity})

        self.options.append({'text': self.game_state.get_text('back'), 'action': self.back})

        self.audio.speak(self.game_state.get_text('office_status', name=office['name'], max=office['max_employees']))
        if self.game_state.office_level >= len(OFFICE_LEVELS) - 1:
            self.audio.speak(self.game_state.get_text('office_max_reached'), interrupt=False)
            
        self.speak_current(interrupt=False)

    def upgrade(self):
        from game_data import OFFICE_LEVELS
        if self.game_state.upgrade_office():
            office = self.game_state.get_office_info()
            self.audio.speak(self.game_state.get_text('office_upgrade_success', name=office['name'], max=office['max_employees'], money=self.game_state.money))
        elif self.game_state.office_level >= len(OFFICE_LEVELS) - 1:
            self.audio.speak(self.game_state.get_text('office_max_reached'))
        else:
            next_cost = OFFICE_LEVELS[self.game_state.office_level + 1]['cost']
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=next_cost))
        return "office_menu"

    def build_presswerk(self):
        if self.game_state.build_presswerk():
            self.audio.speak(self.game_state.get_text('presswerk_built_success'))
            return "office_menu"
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=500000))
            return None

    def expand_storage(self):
        if self.game_state.expand_storage():
            self.audio.speak(self.game_state.get_text('storage_expanded_success', current=self.game_state.storage_capacity))
            return "office_menu"
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=100000))
            return None

    def build_server_room(self):
        if self.game_state.build_server_room():
            self.audio.speak(self.game_state.get_text('server_room_built_success'))
            return "office_menu"
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=1000000))
            return None

    def expand_server_capacity(self):
        try:
            if self.game_state.expand_server_capacity():
                self.audio.speak(self.game_state.get_text('server_expanded_success', current=self.game_state.server_capacity))
                return "office_menu"
            else:
                self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=250000))
                return None
        except ValueError:
             self.audio.speak(self.game_state.get_text('invalid_amount'))
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
        # Nur aktive oder verbuggte Spiele, oder aktive MMOs
        for i, game in enumerate(self.game_state.game_history):
            if game.is_active or game.bugs > 0 or game.size == "MMO":
                
                # Finde heraus ob es ein aktives MMO ist
                is_active_mmo = False
                if game.size == "MMO":
                    for mmo in self.game_state.active_mmos:
                        if mmo.game == game and mmo.game.is_active:
                            is_active_mmo = True
                            break
                            
                # Nur anzeigen wenn patchbar, dlc fähig, oder aktives MMO
                if game.is_active or game.bugs > 0 or is_active_mmo:
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
        
        self.options = []
        
        # Patches and DLCs for non-MMOs or MMOs?
        # Let's say MMOs also get patches, but DLC is replaced by Content Update
        self.options.append({'text': self.game_state.get_text('free_patch', bugs=game.bugs), 'action': lambda: self._patch(idx)})
        
        if game.size == "MMO":
            self.options.append({'text': self.game_state.get_text('mmo_update_option'), 'action': lambda: self._mmo_options(idx)})
        else:
            self.options.append({'text': self.game_state.get_text('release_dlc_option'), 'action': lambda: self._dlc(idx)})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})
        
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

    def _mmo_update(self, idx):
        game = self.game_state.game_history[idx]
        mmo_idx = -1
        for i, m in enumerate(self.game_state.active_mmos):
            if m.game == game:
                mmo_idx = i
                break
                
        if mmo_idx != -1 and self.game_state.release_mmo_update(mmo_idx):
            self.audio.speak(self.game_state.get_text('mmo_update_success'))
        else:
            self.audio.speak(self.game_state.get_text('mmo_update_fail'))
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
        super().__init__('hardware_name', 'hardware_prompt', audio, game_state, self._confirm, self._cancel)
        
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
        time.sleep(1.0)
        self.speak_current(interrupt=False)

    def _cancel(self):
        self.game_state.pending_goty_results = None
        return "game_menu"


# ==============================================================
# SCHWIERIGKEITSGRAD-MENÜ
# ==============================================================
class DifficultyMenu(Menu):
    """Schwierigkeitsgrad-Auswahl beim Spielstart."""

    def __init__(self, audio, game_state):
        from game_data import DIFFICULTY_LEVELS
        options = []
        for i, diff in enumerate(DIFFICULTY_LEVELS):
            diff_key = 'difficulty_' + diff['name'].lower().replace('ä','ae')
            options.append({
                'text': f"{game_state.get_text(diff_key)} - {diff['description']}",
                'action': lambda idx=i: self._select(idx)
            })
        super().__init__(game_state.get_text('difficulty_title'), options, audio, game_state)

    def _select(self, idx):
        from game_data import DIFFICULTY_LEVELS
        diff = DIFFICULTY_LEVELS[idx]
        self.game_state.difficulty = idx
        self.game_state.money = diff["start_money"]
        self.audio.speak(self.game_state.get_text('difficulty_selected', name=diff["name"], desc=diff["description"]))
        return "company_name_input"


# ==============================================================
# SUB-GENRE-MENÜ
# ==============================================================
class SubGenreMenu(Menu):
    """Sub-Genre-Auswahl nach Genre-Auswahl."""

    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('sub_genre_title'), [], audio, game_state)

    def announce_entry(self):
        from game_data import SUB_GENRES
        genre = self.game_state.current_draft.get("genre")
        self.options = []

        # Option: Kein Sub-Genre
        self.options.append({
            'text': self.game_state.get_text('sub_genre_none'),
            'action': lambda: self._select(None)
        })

        if genre and genre in SUB_GENRES:
            for sg in SUB_GENRES[genre]:
                name = sg["name"]
                self.options.append({
                    'text': self.game_state.get_text(name),
                    'action': lambda n=name: self._select(n)
                })

        super().announce_entry()

    def _select(self, sub_genre_name):
        self.game_state.current_draft["sub_genre"] = sub_genre_name
        if sub_genre_name:
            self.audio.speak(self.game_state.get_text('sub_genre_selected', name=self.game_state.get_text(sub_genre_name)))
        return "platform_menu"


# ==============================================================
# SEQUEL-MENÜ
# ==============================================================
class SequelMenu(Menu):
    """Auswahl eines früheren Spiels als Basis für ein Sequel."""

    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('sequel_title'), [], audio, game_state)

    def announce_entry(self):
        self.options = []
        games = self.game_state.game_history

        if not games:
            self.audio.speak(self.game_state.get_text('sequel_no_games'))
            self.options.append({
                'text': self.game_state.get_text('back'),
                'action': lambda: "game_menu"
            })
        else:
            for g in games:
                ip = getattr(g, 'ip_rating', 0)
                seq_num = getattr(g, 'sequel_number', 0)
                next_num = seq_num + 1 if seq_num > 0 else 2
                self.options.append({
                    'text': self.game_state.get_text('sequel_option', name=g.name, ip=ip, num=next_num),
                    'action': lambda game=g, num=next_num: self._select_sequel(game, num)
                })
            self.options.append({
                'text': self.game_state.get_text('back'),
                'action': lambda: "game_menu"
            })

        super().announce_entry()

    def _select_sequel(self, original_game, sequel_num):
        # Sequel-Name generieren
        base_name = original_game.name
        # Entferne vorherige Nummern
        for i in range(10, 1, -1):
            if base_name.endswith(f" {i}"):
                base_name = base_name[:-len(f" {i}")]
                break
        sequel_name = f"{base_name} {sequel_num}"

        # Draft vorbereiten
        self.game_state.current_draft["name"] = sequel_name
        self.game_state.current_draft["topic"] = original_game.topic
        self.game_state.current_draft["genre"] = original_game.genre
        self.game_state.current_draft["sequel_number"] = sequel_num
        self.game_state.current_draft["sub_genre"] = getattr(original_game, 'sub_genre', None)

        self.audio.speak(self.game_state.get_text('sequel_started', name=original_game.name, sequel_name=sequel_name))
        return "platform_menu"  # Springe direkt zur Plattformwahl


# ==============================================================
# VERKAUFSCHARTS-MENÜ
# ==============================================================
class ChartMenu(Menu):
    """Zeigt die aktuellen Verkaufscharts und Marktanteile."""

    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('chart_title'), [], audio, game_state)

    def announce_entry(self):
        self.options = []

        # Alle Spiele sammeln (eigene + Rival-Spiele)
        all_sales = []
        for g in self.game_state.game_history:
            if g.sales > 0:
                all_sales.append({
                    'name': g.name,
                    'studio': self.game_state.company_name,
                    'sales': g.sales
                })

        for rival in self.game_state.rivals:
            for rg in getattr(rival, 'released_games', []):
                all_sales.append({
                    'name': rg.get('name', 'Unbekannt'),
                    'studio': rival.name,
                    'sales': rg.get('sales', 0)
                })

        # Sortieren nach Sales (absteigend)
        all_sales.sort(key=lambda x: x['sales'], reverse=True)

        if not all_sales:
            self.options.append({
                'text': self.game_state.get_text('chart_no_data'),
                'action': lambda: "game_menu"
            })
        else:
            # Top 10
            for i, entry in enumerate(all_sales[:10]):
                self.options.append({
                    'text': self.game_state.get_text('chart_entry',
                        rank=i+1, name=entry['name'], studio=entry['studio'], sales=entry['sales']),
                    'action': lambda: "game_menu"
                })

            # Marktanteil berechnen
            total_sales = sum(e['sales'] for e in all_sales) or 1
            player_sales = sum(e['sales'] for e in all_sales if e['studio'] == self.game_state.company_name)
            share = round(player_sales / total_sales * 100, 1)
            self.options.append({
                'text': self.game_state.get_text('chart_player_share', share=share),
                'action': lambda: "game_menu"
            })

        self.options.append({
            'text': self.game_state.get_text('back'),
            'action': lambda: "game_menu"
        })

        super().announce_entry()


# ==============================================================
# PHASE B: LIZENZEN, ADDONS, BUNDLES
# ==============================================================

class LicenseShopMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('menu_licenses'), [], audio, game_state)

    def announce_entry(self):
        self.options = []
        from game_data import LICENSES
        
        owned_names = [lic['name'] for lic in self.game_state.owned_licenses]
        available = []
        for i, lic in enumerate(LICENSES):
            if lic['name'] not in owned_names:
                available.append((i, lic))
                
        if not available:
            self.options.append({
                'text': self.game_state.get_text('no_licenses_available'),
                'action': lambda: "game_menu"
            })
        else:
            for i, lic in available:
                self.options.append({
                    'text': self.game_state.get_text('buy_license_prompt', name=lic['name'], cost=lic['cost']),
                    'action': lambda idx=i: self._buy(idx)
                })
        self.options.append({
            'text': self.game_state.get_text('back'),
            'action': lambda: "game_menu"
        })
        super().announce_entry()

    def _buy(self, idx):
        from game_data import LICENSES
        lic = LICENSES[idx]
        if self.game_state.buy_license(idx):
            self.audio.speak(self.game_state.get_text('license_bought', name=lic['name'], money=self.game_state.money))
        else:
            self.audio.play_sound('bump')
        return "game_menu"

class LicenseSelectMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('license_select_title'), [], audio, game_state)

    def announce_entry(self):
        self.options = []
        
        # Option: Keine Lizenz
        self.options.append({
            'text': self.game_state.get_text('license_select_none'),
            'action': self._select_none
        })
        
        # Aktive Lizenzen
        active_licenses = self.game_state.get_active_licenses()
        for lic in active_licenses:
            self.options.append({
                'text': lic['name'],
                'action': lambda l_name=lic['name']: self._select_license(l_name)
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        super().announce_entry()

    def _select_none(self):
        return "topic_menu"
        
    def _select_license(self, license_name):
        res = self.game_state.use_license(license_name)
        if res:
            self.game_state.current_draft['license'] = {
                'name': license_name,
                'review_bonus': res['review_bonus']
            }
            self.audio.speak(self.game_state.get_text('license_selected', name=license_name))
        return "topic_menu"


class AddonMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('addon_title'), [], audio, game_state)

    def announce_entry(self):
        self.options = []
        
        if not self.game_state.game_history:
            self.options.append({
                'text': self.game_state.get_text('addon_no_games'),
                'action': lambda: "game_menu"
            })
        else:
            for i, game in enumerate(self.game_state.game_history):
                self.options.append({
                    'text': game.name,
                    'action': lambda idx=i: self._create_addon(idx)
                })
        
        self.options.append({
            'text': self.game_state.get_text('back'),
            'action': lambda: "game_menu"
        })
        super().announce_entry()

    def _create_addon(self, base_game_idx):
        res = self.game_state.create_addon(base_game_idx)
        if res:
            self.audio.speak(self.game_state.get_text('addon_created', 
                name=res['name'], sales=res['sales'], rev=res['revenue'], cost=res['cost'], profit=(res['revenue']-res['cost'])))
        else:
            # might be not enough money or invalid index
            self.audio.play_sound('bump')
        return "game_menu"


class BundleMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('bundle_title'), [], audio, game_state)
        self.selected_indices = set()

    def announce_entry(self):
        self.options = []
        
        from game_data import BUNDLE_DATA
        
        if len(self.game_state.game_history) < BUNDLE_DATA["min_games"]:
            self.options.append({
                'text': self.game_state.get_text('bundle_no_games'),
                'action': lambda: "game_menu"
            })
            self.options.append({
                'text': self.game_state.get_text('back'),
                'action': lambda: "game_menu"
            })
            super().announce_entry()
            return

        # Option zum Erstellen (nur sichtbar, wenn genug gewählt)
        if BUNDLE_DATA["min_games"] <= len(self.selected_indices) <= BUNDLE_DATA["max_games"]:
            self.options.append({
                'text': self.game_state.get_text('bundle_create_btn'),
                'action': self._create_bundle
            })
            
        # Spiele toggeln
        for i, game in enumerate(self.game_state.game_history):
            status = self.game_state.get_text('selected') if i in self.selected_indices else self.game_state.get_text('unselected')
            self.options.append({
                'text': f"{game.name} ({status})",
                'action': lambda idx=i: self._toggle_game(idx)
            })

        self.options.append({
            'text': self.game_state.get_text('back'),
            'action': lambda: "game_menu"
        })
        super().announce_entry()

    def _toggle_game(self, idx):
        if idx in self.selected_indices:
            self.selected_indices.remove(idx)
        else:
            self.selected_indices.add(idx)
        
        self.audio.speak(self.game_state.get_text('bundle_games_selected', count=len(self.selected_indices)))
        self.announce_entry()
        self.speak_current(interrupt=False)
        return None

    def _create_bundle(self):
        res = self.game_state.create_bundle(list(self.selected_indices))
        if res:
            self.audio.speak(self.game_state.get_text('bundle_created', 
                name=res['name'], sales=res['sales'], rev=res['revenue']))
            self.selected_indices.clear()
        else:
            self.audio.play_sound('bump')
            
        return "game_menu"

# ============================================================
# PHASE D: MMO & GaaS
# ============================================================

class MMOPaymentMenu(Menu):
    """Auswahl des Payment-Modells für MMOs."""
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('mmo_payment_title'), [], audio, game_state)
        
    def announce_entry(self):
        self.current_index = 0
        self.options = [
            {'text': self.game_state.get_text('mmo_payment_abo'), 'action': lambda: self._select("Abo")},
            {'text': self.game_state.get_text('mmo_payment_f2p'), 'action': lambda: self._select("F2P")}
        ]
        self.options.append({'text': self.game_state.get_text('back'), 'action': self.back})
        self.speak_current()
        
    def _select(self, model):
        self.game_state.current_draft['payment_model'] = model
        self.audio.speak(self.game_state.get_text('mmo_payment_selected', model=model))
        return "marketing_menu"
        
    def back(self):
        return "game_size_menu"


class MMOManagementMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('mmo_management_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        for idx, mmo in enumerate(getattr(self.game_state, 'active_mmos', [])):
            if mmo.game.is_active:
                 self.options.append({
                     'text': f"{mmo.game.name} - Spieler: {mmo.players:,} - Modell: {mmo.payment_model} - Gewinn/W: {mmo.weekly_profit:,} Euro",
                     'action': lambda i=idx: self.select_mmo(i)
                 })
                 
        self.options.append({'text': self.game_state.get_text('back'), 'action': self.back})
        
        self.audio.speak(self.game_state.get_text('mmo_management_status', current=sum(m.players for m in self.game_state.active_mmos if m.game.is_active), max=getattr(self.game_state, 'server_capacity', 0)))
        self.speak_current(interrupt=False)
        
    def select_mmo(self, idx):
        self.game_state._pending_mmo_idx = idx
        return "mmo_options_menu"

    def back(self):
        return "game_menu"


class MMOOptionsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('mmo_options_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = [
            {'text': self.game_state.get_text('mmo_release_content_update', cost=500000), 'action': self.content_update},
            {'text': self.game_state.get_text('back'), 'action': self.back}
        ]
        self.speak_current()

    def content_update(self):
        idx = getattr(self.game_state, '_pending_mmo_idx', -1)
        success, reason = self.game_state.apply_mmo_update(idx, cost=500000, player_boost=0.3)
        if success:
            self.audio.speak(self.game_state.get_text('mmo_content_update_success'))
        else:
            self.audio.speak(self.game_state.get_text('mmo_content_update_fail_' + reason))
        return "mmo_management_menu"

    def back(self):
        return "mmo_management_menu"


# ============================================================
# PHASE E: PUBLISHING OFFERS
# ============================================================

class PublisherDealsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('publisher_deals_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        offers = getattr(self.game_state, 'publishing_offers', [])
        
        if not offers:
            self.audio.speak(self.game_state.get_text('publisher_deals_empty'))
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        else:
            for idx, offer in enumerate(offers):
                self.options.append({
                    'text': f"{offer.game_name} (von {offer.studio_name})",
                    'action': lambda i=idx: self.select_offer(i)
                })
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        
        self.speak_current()
        
    def select_offer(self, idx):
        self.game_state._pending_offer_idx = idx
        return "publisher_deal_details_menu"

class PublisherDealDetailsMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('publisher_deal_details_title'), [], audio, game_state)
        
    def announce_entry(self):
        self.current_index = 0
        idx = getattr(self.game_state, '_pending_offer_idx', -1)
        offers = getattr(self.game_state, 'publishing_offers', [])
        
        if idx < 0 or idx >= len(offers):
            self.audio.speak(self.game_state.get_text('invalid_game'))
            self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "publisher_deals_menu"}]
            self.speak_current()
            return

        offer = offers[idx]
        self.options = [
            {'text': self.game_state.get_text('publisher_deal_accept'), 'action': self.accept},
            {'text': self.game_state.get_text('publisher_deal_reject'), 'action': self.reject},
            {'text': self.game_state.get_text('back'), 'action': lambda: "publisher_deals_menu"}
        ]
        
        info = self.game_state.get_text('publisher_deal_info', 
            studio=offer.studio_name, game=offer.game_name, genre=offer.genre, 
            quality=offer.quality, cost=offer.marketing_cost, share=int(offer.player_share*100)
        )
        self.audio.speak(info)
        self.speak_current(interrupt=False)
        
    def accept(self):
        idx = getattr(self.game_state, '_pending_offer_idx', -1)
        success, reason = self.game_state.accept_publishing_offer(idx)
        if success:
            self.audio.speak(self.game_state.get_text('publisher_deal_accepted'))
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=0))
        return "publisher_deals_menu"
        
    def reject(self):
        idx = getattr(self.game_state, '_pending_offer_idx', -1)
        if self.game_state.reject_publishing_offer(idx):
            self.audio.speak(self.game_state.get_text('publisher_deal_rejected'))
        return "publisher_deals_menu"


