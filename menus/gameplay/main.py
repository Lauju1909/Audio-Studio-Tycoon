from ..base import Menu, TextInputMenu, SliderMenu
from game_data import (
    SLIDER_NAMES, GAME_SIZES,
)
import random


class MainMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('main_title')
        options = [
            {'text': self.game_state.get_text('menu_new_game'), 'action': lambda: "company_name_input"},
            {'text': self.game_state.get_text('menu_load_game'), 'action': lambda: "load_menu"},
            {'text': self.game_state.get_text('multiplayer_menu_title', default="Multiplayer"), 'action': lambda: "multiplayer_main"},
            {'text': self.game_state.get_text('menu_mod_portal'), 'action': lambda: "mod_portal"},
            {'text': self.game_state.get_text('menu_support_dev'), 'action': lambda: "monetization_menu_main"},
            {'text': self.game_state.get_text('menu_settings'), 'action': lambda: "settings_menu"},
            {'text': self.game_state.get_text('menu_help'), 'action': lambda: "help_menu"},
            {'text': self.game_state.get_text('menu_credits'), 'action': self.show_credits},
            {'text': self.game_state.get_text('menu_quit'), 'action': lambda: "quit"}
        ]
        super().__init__(title, options, audio, game_state)

    def show_credits(self):
        return "credits_menu"


class CompanyNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('company_name_title'), 'company_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "main_menu")

    def _on_confirm(self, name):
        self.game_state.company_name = name
        return "difficulty_menu"

    def generate_random_name(self):
        names = [
            "Pixel Studios", "Audio Vision", "Red Barrels", "Lauju Games", 
            "Blind Box", "Sound Wave Games", "Next Gen Studios", "Echo Games", 
            "Visionary Devs", "Gamer Forge", "Creative Minds", "Virtual Dynamics"
        ]
        return random.choice(names)


class GameMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('game_menu')
        total_emails = len(self.game_state.emails)
        unread_emails = len([e for e in self.game_state.emails if not getattr(e, 'is_read', True)])
        options = [
            {'text': self.game_state.get_text('menu_develop_game'), 'action': lambda: self._start_dev(False)},
            {'text': self.game_state.get_text('menu_co_dev_start'), 'action': lambda: self._start_dev(True)}
        ]
        if self.game_state.is_developing:
             options.insert(0, {'text': self.game_state.get_text('menu_current_dev', default="Aktuelle Entwicklungen anzeigen"), 'action': lambda: "dev_progress_menu"})

        options.extend([
            {'text': self.game_state.get_text('hr_menu'), 'action': lambda: "hr_menu"},
            {'text': self.game_state.get_text('research_menu'), 'action': lambda: "research_menu"},
            {'text': self.game_state.get_text('office_menu'), 'action': lambda: "office_menu"},
            {'text': self.game_state.get_text('email_inbox_status', total=total_emails, unread=unread_emails), 'action': lambda: "email_inbox"},
            {'text': self.game_state.get_text('community_menu_title'), 'action': lambda: "community_menu"},
            {'text': self.game_state.get_text('hardware_menu_title'), 'action': lambda: "hardware_menu"}
        ])
        
        # Locked features
        def add_locked_feature(feature_id, text, action):
            if self.game_state.is_feature_unlocked(feature_id):
                options.append({'text': text, 'action': action})
            else:
                from game_data import FEATURE_UNLOCKS
                if feature_id in FEATURE_UNLOCKS:
                    options.append({'text': f"{text} (Ab {FEATURE_UNLOCKS[feature_id].get('year', '???')})", 'action': lambda: None})
                
        add_locked_feature("esports", self.game_state.get_text('esports_menu_title', default='E-Sports Zentrale'), lambda: "esports_menu")
        add_locked_feature("soundcon", self.game_state.get_text('soundcon_menu_title', default='SoundCon Messe'), lambda: "soundcon_menu")
        add_locked_feature("soundtrack_label", self.game_state.get_text('label_menu_title', default='Soundtrack-Label'), lambda: "label_menu")
        add_locked_feature("merch", self.game_state.get_text('merch_menu_title', default='Merchandising'), lambda: "merch_menu")
        add_locked_feature("creator_sponsorship", self.game_state.get_text('creator_menu_title', default='Content Creators Sponsern'), lambda: "creator_menu")
        add_locked_feature("streaming_platform", self.game_state.get_text('streaming_platform_menu_title', default='Streaming-Plattform'), lambda: "streaming_platform_menu")
        
        options.extend([
            {'text': self.game_state.get_text('jingle_menu_title'), 'action': lambda: "jingle_name_input"},
            {'text': self.game_state.get_text('bank_menu'), 'action': lambda: "bank_menu"},
            {'text': self.game_state.get_text('service_menu'), 'action': lambda: "service_menu"},
            {'text': self.game_state.get_text('game_porting_title', default='Spiel Portieren'), 'action': lambda: "game_porting_menu"},
            {'text': self.game_state.get_text('active_games_menu_title', default="Aktive Spiele & Einnahmen"), 'action': lambda: "active_games_menu"},
            {'text': self.game_state.get_text('save_menu'), 'action': lambda: "save_menu"},
            {'text': self.game_state.get_text('menu_settings'), 'action': lambda: "settings_menu_ingame"},
            {'text': self.game_state.get_text('menu_quit'), 'action': lambda: "main_menu"}
        ])
        super().__init__(title, options, audio, game_state)

    def _start_dev(self, is_co_dev):
        if is_co_dev:
            return "co_dev_partner_menu"
        else:
            self.game_state.co_dev_partner = None
            return "project_type_menu"


class DeveloperMenu(Menu):
    """Geheimes MenÃ¼ fÃ¼r Tests."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Developer Mode", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': "Geld hinzufÃ¼gen (1 Mio)", 'action': self._add_money},
            {'text': "Entwicklung sofort beenden", 'action': self._instant_dev},
            {'text': "Forschungspunkte hinzufÃ¼gen", 'action': self._add_rp},
            {'text': "Alle Themen/Genres freischalten", 'action': self._unlock_all},
            {'text': "Moral auf 100", 'action': self._fix_morale},
            {'text': "Fans hinzufÃ¼gen (100k)", 'action': self._add_fans},
            {'text': "ZurÃ¼ck", 'action': lambda: "game_menu"}
        ]

    def _add_money(self):
        self.game_state.track_income("other", 1000000)
        self.audio.play_sound("cash")
        return None

    def _instant_dev(self):
        # BUG-FIX v3.3.9: active_projects statt veralteter dev_progress/dev_total_weeks nutzen
        if self.game_state.is_developing:
            for ap in self.game_state.active_projects:
                ap["progress"] = ap["total_weeks"]
            self.audio.speak("Entwicklung abgeschlossen.")
        return None

    def _add_rp(self):
        self.game_state.research_points += 500
        self.audio.speak("500 Forschungspunkte hinzugefÃ¼gt.")
        return None

    def _unlock_all(self):
        from game_data import HISTORICAL_TOPICS, RESEARCHABLE_GENRES
        for t in HISTORICAL_TOPICS:
            if t["name"] not in self.game_state.unlocked_topics:
                self.game_state.unlocked_topics.append(t["name"])
        for g in RESEARCHABLE_GENRES:
            if g not in self.game_state.unlocked_genres:
                self.game_state.unlocked_genres.append(g)
        self.audio.speak("Alles freigeschaltet.")
        return None

    def _fix_morale(self):
        for emp in self.game_state.employees:
            emp.morale = 100
        self.audio.speak("Moral wiederhergestellt.")
        return None
    
    def _add_fans(self):
        self.game_state.fans += 100000
        self.audio.speak("100.000 Fans hinzugefÃ¼gt.")
        return None


class ReviewResultMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.review_text = ""
        super().__init__(self.game_state.get_text('review_result'), [], audio, game_state)
        self._generate_review_text()
        self._update_options()

    def _generate_review_text(self):
        if not self.game_state.game_history:
            return
        game = self.game_state.game_history[-1]
        score = game.review.average if game.review else 0
        try:
            from ai_reviewer import ai_reviewer
            self.review_text = ai_reviewer.generate_review(self.game_state, game, score)
        except Exception:
            self.review_text = f"Wertung: {score}/10."

    def _update_options(self):
        if not self.game_state.game_history:
            self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "main_menu"}]
            return
        game = self.game_state.game_history[-1]
        score = game.review.average if game.review else 0
        
        self.options = []
        # Show full review text as a menu option for readability
        if self.review_text:
            # We split the long text into chunks if it's too long, but for screen readers, one long string is usually fine.
            self.options.append({'text': self.review_text, 'action': lambda: None})
            
        self.options.append({'text': self.game_state.get_text('score_label', score=score), 'action': lambda: None})
        self.options.append({'text': self.game_state.get_text('review_listen_again'), 'action': self._repeat_review})
        self.options.append({'text': self.game_state.get_text('continue'), 'action': lambda: "game_menu"})


    def _repeat_review(self):
        self.audio.speak(self.review_text)
        return None

    def announce_entry(self):
        super().announce_entry()
        if not self.game_state.game_history:
            self.audio.speak(self.game_state.get_text('no_reviews_available', default="Keine Reviews verfügbar."), interrupt=False)
            return
        game = self.game_state.game_history[-1]
        score = game.review.average if game.review else 0
        self.audio.speak(self.game_state.get_text('reviews_for', name=game.name, score=score), interrupt=False)
        if self.review_text:
            self.audio.speak(self.game_state.get_text('review_prefix') + self.review_text, interrupt=False)


class GOTYMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        
        # Verarbeite anstehende Ergebnisse
        
        if getattr(self.game_state, "pending_shareholder_meeting", False):
            pass
        if getattr(self.game_state, "pending_goty_results", None):
            res = self.game_state.pending_goty_results
            winner_text = "Niemand"
            if res["my_score"] > res["rival_score"] and res["my_score"] > 0:
                winner_text = f"{self.game_state.company_name} ({res['my_game']})"
            elif res["rival_score"] > 0:
                winner_text = f"{res['rival_name']} ({res['rival_game']})"
            
            # In Historie speichern
            self.game_state.goty_history[res["year"]] = winner_text
            # WICHTIG: Ergebnis lÃ¶schen, damit wir nicht im Loop hÃ¤ngen bleiben!
            self.game_state.pending_goty_results = None
            
        super().__init__(self.game_state.get_text('goty_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        # Zeige GOTY Historie (neueste zuerst)
        years = sorted(self.game_state.goty_history.keys(), reverse=True)
        for y in years:
             winner = self.game_state.goty_history[y]
             self.options.append({'text': f"{self.game_state.get_text('year_label', default='Jahr')} {y}: {winner}", 'action': lambda: None})
        
        if not self.options:
             self.options.append({'text': self.game_state.get_text('goty_no_awards'), 'action': lambda: "game_menu"})
             
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def announce_entry(self):
        super().announce_entry()
        if self.game_state.goty_history:
            latest_year = max(self.game_state.goty_history.keys())
            winner = self.game_state.goty_history[latest_year]
            self.audio.speak(f"{self.game_state.get_text('goty_winner_announcement', default='Der Gewinner des Jahres')} {latest_year} {self.game_state.get_text('is_label', default='ist')}: {winner}", interrupt=False)


class ChartMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('charts_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        # Charts berechnen
        charts = self.game_state.get_current_charts()
        for idx, entry in enumerate(charts):
             text = f"{idx+1}. {entry['name']} ({entry['studio']}) - {entry['sales']:,} Sales"
             self.options.append({'text': text, 'action': lambda: None})
             
        if not self.options:
             self.options.append({'text': self.game_state.get_text('charts_empty'), 'action': lambda: "game_menu"})
             
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})


class ActiveGamesMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('active_games_menu_title', default="Aktive Spiele & Einnahmen"), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        active_games = [g for g in self.game_state.game_history if g.is_active]
        for g in active_games:
            woche = g.weeks_on_market
            text = f"{g.name}: Woche {woche}, {g.sales:,} Sales, {g.revenue:,} EUR Einnahmen bisher."
            self.options.append({'text': text, 'action': lambda game=g: self._select_game(game)})
            
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_active_games', default="Momentan keine aktiven Spiele auf dem Markt."), 'action': lambda: "game_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select_game(self, game):
        self.game_state._pending_game_details = game
        return "game_details_menu"


class GameDetailsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        game = getattr(self.game_state, '_pending_game_details', None)
        title = self.game_state.get_text('game_details_title', default="Spieldetails")
        if game:
            title = f"{title}: {game.name}"
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        game = getattr(self.game_state, '_pending_game_details', None)
        if game and game.is_active:
            # Mod Support feature
            if not getattr(game, 'has_mod_support', False):
                self.options.append({'text': self.game_state.get_text('activate_mod_support', default="Mod-Support hinzufÃ¼gen (10.000 EUR)"), 'action': self._add_mod_support})
            else:
                self.options.append({'text': self.game_state.get_text('has_mod_support_active', default="Mod-Support: Aktiviert"), 'action': lambda: None})
                
            # Ads feature
            if not getattr(game, 'has_ads', False):
                self.options.append({'text': self.game_state.get_text('activate_ads', default="In-Game Werbung aktivieren"), 'action': self._activate_ads})
            else:
                self.options.append({'text': self.game_state.get_text('has_ads_active', default="In-Game Werbung: Aktiviert"), 'action': lambda: None})
        
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "active_games_menu"})

    def _add_mod_support(self):
        game = getattr(self.game_state, '_pending_game_details', None)
        if game:
            if self.game_state.money >= 10000:
                self.game_state.track_expense("other", 10000)
                game.has_mod_support = True
                self.audio.play_sound("cash")
                self._update_options()
                self.current_index = 0
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('not_enough_money'))
        return None

    def _activate_ads(self):
        game = getattr(self.game_state, '_pending_game_details', None)
        if game:
            game.has_ads = True
            self.audio.play_sound("confirm")
            self._update_options()
            self.current_index = 0
        return None


class CreditsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_credits'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.audio.speak(self.title)
        self.audio.speak(self.game_state.get_text('credits_text'), interrupt=False)
        self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "main_menu"}]
        self.speak_current(interrupt=False)


class ShareholderMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        game_state.pending_shareholder_meeting = False
        
        target_met = getattr(game_state, 'shareholder_target_met', False)
        
        if target_met:
            game_state.shareholder_trust = min(100, getattr(game_state, 'shareholder_trust', 100) + 10)
            msg = game_state.get_text('shareholder_happy', default="Aktionaere sind gluecklich! Umsatzziele erreicht.")
            audio.play_sound("cheer")
        else:
            game_state.shareholder_trust = getattr(game_state, 'shareholder_trust', 100) - 25
            msg = game_state.get_text('shareholder_angry', default="Aktionaere sind unzufrieden! Ziele verfehlt.")
            audio.play_sound("error")
            
        game_state.shareholder_target = game_state.money * 1.10 # Neues Ziel
        
        if game_state.shareholder_trust <= 0:
            msg += " " + game_state.get_text('shareholder_fired', default="Du wurdest als CEO entlassen! GAME OVER.")
            options = [{'text': "Game Over", 'action': lambda: "main_menu"}]
        else:
            msg += " " + game_state.get_text('shareholder_trust_msg', trust=game_state.shareholder_trust, default=f"Vertrauen liegt bei {game_state.shareholder_trust}%.")
            options = [{'text': "Verstanden", 'action': lambda: "game_menu"}]
            
        super().__init__(game_state.get_text('shareholder_title', default='Jahreshauptversammlung'), options, audio, game_state)
        self.audio.speak(msg, interrupt=True)
