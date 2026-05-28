from .base import Menu, TextInputMenu, SliderMenu
from game_data import (
    GENRES, SLIDER_NAMES, AUDIENCES,
    OFFICE_LEVELS, GAME_SIZES,
    get_compatibility, get_compatibility_text,
    get_available_platforms,
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
        import random
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
            return "topic_menu"

class CoDevPartnerMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_co_dev_partner_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for rival in self.game_state.rivals:
            self.options.append({'text': self.game_state.get_text('co_dev_partner_option', name=rival.name), 'action': lambda r=rival.name: self._select(r)})
        
        # Falls es keine Konkurrenten gibt:
        if not self.options:
            self.options.append({'text': self.game_state.get_text('co_dev_no_partners'), 'action': lambda: "game_menu"})
        else:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select(self, partner_name):
        self.game_state.co_dev_partner = partner_name
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('co_dev_started', name=partner_name))
        return "topic_menu"

class TopicMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('topic_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for topic in self.game_state.unlocked_topics:
            self.options.append({'text': self.game_state.get_text(topic), 'action': lambda t=topic: self._select(t)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select(self, topic):
        self.game_state.current_draft['topic'] = topic
        return "genre_menu"

class GenreMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('genre_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for genre in self.game_state.unlocked_genres:
            self.options.append({'text': self.game_state.get_text(genre), 'action': lambda g=genre: self._select(g)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "topic_menu"})

    def _select(self, genre):
        self.game_state.current_draft['genre'] = genre
        return "platform_menu"

class PlatformMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('platform_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        platforms = self.game_state.get_market_platforms()
        for p in platforms:
            self.options.append({'text': f"{p['name']} ({p['license_fee']} EUR)", 'action': lambda plat=p: self._select(plat)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "genre_menu"})

    def _select(self, plat):
        self.game_state.current_draft['platform'] = plat
        return "audience_menu"

class AudienceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('audience_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for aud in self.game_state.unlocked_audiences:
            self.options.append({'text': self.game_state.get_text(aud), 'action': lambda a=aud: self._select(a)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "platform_menu"})

    def _select(self, aud):
        self.game_state.current_draft['audience'] = aud
        return "game_size_menu"

class GameSizeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('game_size_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for size in GAME_SIZES:
            name = size['name'] if isinstance(size, dict) else size
            self.options.append({'text': self.game_state.get_text(name), 'action': lambda s=name: self._select(s)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "audience_menu"})

    def _select(self, size):
        self.game_state.current_draft['size'] = size
        return "engine_select_menu"

class EngineSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('engine_select_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for engine in self.game_state.engines:
            self.options.append({'text': engine.name, 'action': lambda e=engine: self._select(e)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_size_menu"})

    def _select(self, engine):
        self.game_state.current_draft['engine'] = engine
        return "marketing_menu"

class MarketingMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('marketing_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('marketing_none'), 'action': lambda: self._select('none')},
            {'text': self.game_state.get_text('marketing_small'), 'action': lambda: self._select('small')},
            {'text': self.game_state.get_text('marketing_medium'), 'action': lambda: self._select('medium')},
            {'text': self.game_state.get_text('marketing_large'), 'action': lambda: self._select('large')},
            {'text': self.game_state.get_text('back'), 'action': lambda: "engine_select_menu"}
        ]

    def _select(self, level):
        self.game_state.current_draft['marketing'] = level
        return "team_select_menu"

class ProjectTeamSelectMenu(Menu):
    """Menü zur Auswahl der Mitarbeiter für ein Projekt."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        # Standard: Alle verfügbaren Mitarbeiter sind ausgewählt
        if "assigned_employee_ids" not in self.game_state.current_draft:
             self.game_state.current_draft["assigned_employee_ids"] = [i for i, e in enumerate(self.game_state.employees) if not getattr(e, 'is_sick', False) and not getattr(e, 'is_training', False)]
        
        super().__init__(self.game_state.get_text('menu_team_select'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        assigned_ids = self.game_state.current_draft.get("assigned_employee_ids", [])
        
        # IDs der Mitarbeiter, die bereits in anderen Projekten arbeiten
        busy_ids = []
        for ap in self.game_state.active_projects:
            busy_ids.extend(getattr(ap["project"], 'assigned_employee_ids', []))

        for i, emp in enumerate(self.game_state.employees):
            # Kranke/Trainierende MA können nicht gewählt werden
            if getattr(emp, 'is_sick', False) or getattr(emp, 'is_training', False):
                continue
            
            # Bereits beschäftigte MA (außer sie sind bereits diesem Projekt zugewiesen)
            if i in busy_ids and i not in assigned_ids:
                continue
                
            is_assigned = i in assigned_ids
            status_text = self.game_state.get_text('team_status_assigned' if is_assigned else 'team_status_not_assigned')
            text = self.game_state.get_text('team_member_status', name=emp.name, role=self.game_state.get_text(emp.role), status=status_text)
            
            # Spezialisierungs-Indikator
            if emp.specialization:
                spec = emp.specialization
                # BUG-FIX v3.3.9: Sicherer .get()-Zugriff statt [] um KeyError/TypeError bei None-Werten nach reset_draft zu vermeiden
                draft_genre = self.game_state.current_draft.get('genre')
                draft_topic = self.game_state.current_draft.get('topic')
                draft_sub_genre = self.game_state.current_draft.get('sub_genre')
                if spec.get("bonus_type") == "Genre" and (draft_genre == spec.get("target") or draft_sub_genre == spec.get("target")):
                    text += " [BONUS!]"
                elif spec.get("bonus_type") == "Topic" and draft_topic == spec.get("target"):
                    text += " [BONUS!]"
            
            # WICHTIG: idx=i fixiert den aktuellen Wert von i für die Lambda-Funktion
            self.options.append({'text': text, 'action': lambda idx=i: self._toggle(idx)})

        # Bestätigen Option
        count = len(assigned_ids)
        self.options.append({'text': self.game_state.get_text('team_confirm', count=count), 'action': self._confirm})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "marketing_menu"})

    def _toggle(self, real_idx):
        assigned_ids = self.game_state.current_draft.get("assigned_employee_ids", [])
        
        if real_idx in assigned_ids:
            assigned_ids.remove(real_idx)
        else:
            assigned_ids.append(real_idx)
            
        self.game_state.current_draft["assigned_employee_ids"] = assigned_ids
        self._update_options()
        return None

    def _confirm(self):
        if not self.game_state.current_draft.get("assigned_employee_ids"):
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('team_none_selected_error'))
            return None
        
        # Zeitschätzung ansagen
        weeks = self.game_state.estimate_dev_time()
        self.audio.speak(self.game_state.get_text('dev_time_estimate', weeks=weeks))
        
        return "game_name_input"

class GameNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('game_name_title', 'game_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "marketing_menu")

    def _on_confirm(self, name):
        self.game_state.current_draft['name'] = name
        return "slider_menu"

    def generate_random_name(self):
        import random
        prefixes = ["Project", "The Last", "Super", "Mega", "Blind", "Dark", "Crazy", "Epic", "Legend of", "Call of", "Return to"]
        suffixes = ["Adventure", "Strike", "Hero", "Tycoon", "Quest", "Legends", "Warriors", "Audio", "World", "Chronicles"]
        
        draft = getattr(self.game_state, 'current_draft', {})
        topic = draft.get('topic', '')
        genre = draft.get('genre', '')
        
        choices = [
            f"{random.choice(prefixes)} {random.choice(suffixes)}",
            f"{random.choice(prefixes)} {topic}" if topic else f"{random.choice(prefixes)} Game"
        ]
        
        if topic:
            choices.append(f"{topic} {random.choice(suffixes)}")
        if genre and topic:
            choices.append(f"{topic} {genre}")
            
        return random.choice(choices)

class DevelopmentSliderMenu(SliderMenu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('dev_sliders_title'), audio, game_state,
                         SLIDER_NAMES, budget=15, 
                         on_confirm=self._on_confirm, on_cancel=lambda: "game_name_input")

    def _on_confirm(self, values):
        self.game_state.current_draft['sliders'] = values
        est = self.game_state.estimate_dev_time()
        self.game_state.start_development()
        self.audio.speak(
            self.game_state.get_text('dev_time_estimate', weeks=est),
            interrupt=False
        )
        return "dev_progress_menu"

class DevProgressMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('dev_progress_menu'), [], audio, game_state)
        self.selected_project_idx = -1
        self._update_options()

    def _update_options(self):
        self.options = []
        if self.selected_project_idx == -1:
            for i, ap in enumerate(self.game_state.active_projects):
                prog = int((ap["progress"] / ap["total_weeks"]) * 100)
                name = ap["project"].name
                # Closure für idx
                def make_select(idx):
                    return lambda: self._select_project(idx)
                self.options.append({'text': f"{name} ({prog}%)", 'action': make_select(i)})
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        else:
            self.options = [
                {'text': self.game_state.get_text('get_progress_label', default="Fortschritt abfragen"), 'action': self._speak_progress},
                {'text': self.game_state.get_text('finish_game'), 'action': self._finish},
                {'text': self.game_state.get_text('back'), 'action': self._back_to_list}
            ]

    def _select_project(self, idx):
        self.selected_project_idx = idx
        self._update_options()
        self.current_index = 0
        return None

    def _back_to_list(self):
        self.selected_project_idx = -1
        self._update_options()
        self.current_index = 0
        return None

    def _speak_progress(self):
        if self.selected_project_idx < 0 or self.selected_project_idx >= len(self.game_state.active_projects):
            return self._back_to_list()
        ap = self.game_state.active_projects[self.selected_project_idx]
        progress = int((ap["progress"] / ap["total_weeks"]) * 100)
        progress = min(100, progress)
        status = f"{progress}% {self.game_state.get_text('completed_label')}. Bugs: {ap['bugs']}"
        self.audio.speak(status)
        return None

    def _finish(self):
        if self.selected_project_idx < 0 or self.selected_project_idx >= len(self.game_state.active_projects):
            return self._back_to_list()
        ap = self.game_state.active_projects[self.selected_project_idx]
        if ap["progress"] >= ap["total_weeks"]:
            self.game_state.finalize_game(ap)
            return "review_result"
        else:
            self.audio.speak(self.game_state.get_text('dev_not_finished'))
            return None

    def speak_current(self, interrupt=True):
        text = self.options[self.current_index]['text']
        self.audio.speak(text, interrupt=interrupt)

class DeveloperMenu(Menu):
    """Geheimes Menü für Tests."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Developer Mode", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': "Geld hinzufügen (1 Mio)", 'action': self._add_money},
            {'text': "Entwicklung sofort beenden", 'action': self._instant_dev},
            {'text': "Forschungspunkte hinzufügen", 'action': self._add_rp},
            {'text': "Alle Themen/Genres freischalten", 'action': self._unlock_all},
            {'text': "Moral auf 100", 'action': self._fix_morale},
            {'text': "Fans hinzufügen (100k)", 'action': self._add_fans},
            {'text': "Zurück", 'action': lambda: "game_menu"}
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
        self.audio.speak("500 Forschungspunkte hinzugefügt.")
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
        self.audio.speak("100.000 Fans hinzugefügt.")
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
        except Exception as e:
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
        game = self.game_state.game_history[-1]
        score = game.review.average if game.review else 0
        self.audio.speak(self.game_state.get_text('reviews_for', name=game.name, score=score), interrupt=False)
        if self.review_text:
            self.audio.speak(self.game_state.get_text('review_prefix') + self.review_text, interrupt=False)

class RemasterSelectMenu(Menu):
    def __init__(self, audio, game_state):
         super().__init__(game_state.get_text('remaster_title'), [], audio, game_state)

class PublisherMenu(Menu):
    def __init__(self, audio, game_state):
         super().__init__(game_state.get_text('publisher_title'), [], audio, game_state)

class GOTYMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        
        # Verarbeite anstehende Ergebnisse
        if getattr(self.game_state, "pending_goty_results", None):
            res = self.game_state.pending_goty_results
            winner_text = "Niemand"
            if res["my_score"] > res["rival_score"] and res["my_score"] > 0:
                winner_text = f"{self.game_state.company_name} ({res['my_game']})"
            elif res["rival_score"] > 0:
                winner_text = f"{res['rival_name']} ({res['rival_game']})"
            
            # In Historie speichern
            self.game_state.goty_history[res["year"]] = winner_text
            # WICHTIG: Ergebnis löschen, damit wir nicht im Loop hängen bleiben!
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

class DifficultyMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('difficulty_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        from game_data import DIFFICULTY_LEVELS
        self.options = []
        for idx, diff in enumerate(DIFFICULTY_LEVELS):
             self.options.append({
                 'text': f"{diff['name']}: {diff['description']}", 
                 'action': lambda i=idx: self._select(i)
             })
             
    def _select(self, idx):
        self.game_state.difficulty = idx
        # Startgeld etc. setzen
        from game_data import DIFFICULTY_LEVELS
        self.game_state.money = DIFFICULTY_LEVELS[idx]['start_money']
        return "game_menu"

class SubGenreMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('subgenre_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [{'text': self.game_state.get_text('no_subgenre'), 'action': lambda: "platform_menu"}]
        
        genre = self.game_state.current_draft.get('genre')
        from game_data import SUB_GENRES
        if genre in SUB_GENRES:
             for sub in SUB_GENRES[genre]:
                  self.options.append({
                      'text': sub['name'], 
                      'action': lambda s=sub['name']: self._select(s)
                  })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "genre_menu"})

    def _select(self, name):
        self.game_state.current_draft['sub_genre'] = name
        return "platform_menu"

class SequelMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('sequel_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [{'text': self.game_state.get_text('new_ip'), 'action': lambda: "topic_menu"}]
        
        # Nur Spiele mit IP-Rating > 20
        for game in self.game_state.game_history:
             if game.ip_rating > 20:
                  self.options.append({
                      'text': f"{game.name} (IP: {game.ip_rating})", 
                      'action': lambda g=game: self._select(g)
                  })
                  
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select(self, game):
        self.game_state.current_draft['topic'] = game.topic
        self.game_state.current_draft['genre'] = game.genre
        self.game_state.current_draft['sequel_to'] = game.name
        self.game_state.current_draft['sequel_number'] = game.sequel_number + 1
        return "sub_genre_menu"

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
            self.options.append({'text': text, 'action': lambda: None})
            
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_active_games', default="Momentan keine aktiven Spiele auf dem Markt."), 'action': lambda: "game_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

class AAADevEventMenu(Menu):
    """Zeigt Entwicklungs-Events (AAA und allgemein) mit Entscheidungsoptionen."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.event_ctx = getattr(game_state, 'pending_dev_event', None)
        
        if self.event_ctx:
            event = self.event_ctx["data"]
            proj_name = self.event_ctx["ap"]["project"].name
            title = f"{proj_name}: " + game_state.get_text('dev_event_' + event['id'] + '_title',
                                         default=game_state.get_text('aaa_event_title'))
        else:
            title = game_state.get_text('aaa_event_title')
            
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        if not self.event_ctx:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
            return
            
        event = self.event_ctx["data"]
        for opt in event.get('options', []):
            opt_text = self.game_state.get_text(
                'dev_event_opt_' + event['id'] + '_' + opt['id'],
                default=self.game_state.get_text('dev_event_opt_' + opt['id'], default=opt['id'])
            )
            # Konsequenz-Zusammenfassung
            effects = []
            if opt.get('cost', 0) > 0:
                effects.append(f"-{opt['cost']:,} EUR")
            if opt.get('delay', 0) > 0:
                effects.append(f"+{opt['delay']} {self.game_state.get_text('weeks')}")
            if opt.get('speed', 0) > 0:
                effects.append(f"-{opt['speed']} {self.game_state.get_text('weeks')}")
            if opt.get('hype', 0) != 0:
                sign = '+' if opt['hype'] > 0 else ''
                effects.append(f"{sign}{opt['hype']} Hype")
            if opt.get('bugs', 0) > 0:
                effects.append(f"+{opt['bugs']} Bugs")
            if opt.get('morale', 0) != 0:
                sign = '+' if opt['morale'] > 0 else ''
                effects.append(f"{sign}{opt['morale']} {self.game_state.get_text('morale')}")
            suffix = f" [{', '.join(effects)}]" if effects else ""
            full_text = opt_text + suffix
            self.options.append({'text': full_text, 'action': lambda o=opt: self._choose(o)})

    def announce_entry(self):
        self.current_index = 0
        if self.event_ctx:
            event = self.event_ctx["data"]
            desc = self.game_state.get_text(
                'dev_event_' + event['id'] + '_desc',
                default=self.game_state.get_text('aaa_event_title')
            )
            self.audio.speak(self.title)
            self.audio.speak(desc, interrupt=False)
        else:
            self.audio.speak(self.title)
        if self.options:
            self.speak_current(interrupt=False)

    def _choose(self, opt):
        gs = self.game_state
        ap = self.event_ctx["ap"]
        
        # Kosten abziehen
        cost = opt.get('cost', 0)
        if cost > 0:
            if gs.money < cost:
                self.audio.play_sound("error")
                self.audio.speak(gs.get_text('not_enough_money'))
                return None
            gs.track_expense("dev_event", cost)
            
        # Zeitverzögerung
        delay = opt.get('delay', 0)
        if delay > 0:
            ap["total_weeks"] += delay
            
        # Beschleunigung
        speed = opt.get('speed', 0)
        if speed > 0:
            ap["progress"] = min(ap["total_weeks"], ap["progress"] + speed)
            
        # Hype (global)
        hype = opt.get('hype', 0)
        if hype != 0:
            gs.hype = max(0, gs.hype + hype)
            
        # Bugs
        bugs = opt.get('bugs', 0)
        if bugs > 0:
            ap["bugs"] += bugs
            
        # Moral (Team des Projekts)
        morale = opt.get('morale', 0)
        if morale != 0:
            active_emps = gs._active_employees(ap["project"])
            for emp in active_emps:
                emp.morale = max(0, min(100, emp.morale + morale))
                
        # Event abschliessen
        gs.pending_dev_event = None
        self.audio.play_sound("confirm")
        return "game_menu"

class ExpoMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Spiele-Messe veranstalten", [], audio, game_state)
        self.state = "size"
        self.cost = 0
        self.base_hype = 0
        self._update_options()

    def _update_options(self):
        self.options = []
        if self.state == "size":
            self.title = "Spiele-Messe: Standgröße wählen"
            self.options.append({'text': self.game_state.get_text('expo_small_stand'), 'action': lambda: self._select_size(50000, 5)})
            self.options.append({'text': self.game_state.get_text('expo_medium_stand'), 'action': lambda: self._select_size(250000, 15)})
            self.options.append({'text': self.game_state.get_text('expo_large_stand'), 'action': lambda: self._select_size(1000000, 40)})
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})
        elif self.state == "demo":
            self.title = "Spiele-Messe: Demo zeigen?"
            # BUG-FIX v3.3.9: active_projects statt veraltetes dev_progress-Attribut nutzen
            first_prog = self.game_state.active_projects[0]["progress"] if self.game_state.active_projects else 0
            if self.game_state.is_developing and first_prog > 10:
                self.options.append({'text': self.game_state.get_text('expo_demo_current'), 'action': lambda: self._select_demo(10000, 5)})
            self.options.append({'text': self.game_state.get_text('expo_demo_none'), 'action': lambda: self._select_demo(0, 0)})
        elif self.state == "influencer":
            self.title = "Spiele-Messe: Influencer einladen?"
            self.options.append({'text': self.game_state.get_text('expo_influencer_hire'), 'action': lambda: self._select_influencer(100000, 10)})
            self.options.append({'text': self.game_state.get_text('expo_influencer_none'), 'action': lambda: self._select_influencer(0, 0)})
        elif self.state == "event":
            self.title = self.game_state.get_text('expo_event_overcrowded_title')
            self.options.append({'text': self.game_state.get_text('expo_event_overcrowded_opt1'), 'action': lambda: self._resolve_event("security")})
            self.options.append({'text': self.game_state.get_text('expo_event_overcrowded_opt2'), 'action': lambda: self._resolve_event("chaos")})

    def _select_size(self, cost, hype):
        if self.game_state.money < cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None
        self.cost += cost
        self.base_hype += hype
        self.state = "demo"
        self._update_options()
        self.announce_entry()
        return None

    def _select_demo(self, cost, hype):
        if self.game_state.money < self.cost + cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None
        self.cost += cost
        self.base_hype += hype
        self.state = "influencer"
        self._update_options()
        self.announce_entry()
        return None

    def _select_influencer(self, cost, hype):
        if self.game_state.money < self.cost + cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None
        self.cost += cost
        self.base_hype += hype
        
        import random
        if random.random() < 0.4:
            self.state = "event"
            self._update_options()
            self.announce_entry()
            return None
        else:
            return self._finish_expo()

    def _resolve_event(self, choice):
        import random
        if choice == "security":
            if self.game_state.money < self.cost + 50000:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('not_enough_money'))
                self._apply_chaos()
            else:
                self.cost += 50000
                self.audio.play_sound("cash")
                self.audio.speak(self.game_state.get_text('expo_event_security_safe'))
        elif choice == "chaos":
            if random.random() < 0.5:
                self.audio.play_sound("cheer")
                self.audio.speak(self.game_state.get_text('expo_event_success_mega'))
                self.base_hype *= 2
            else:
                self._apply_chaos()
        return self._finish_expo()

    def _apply_chaos(self):
        self.audio.play_sound("error")
        self.audio.speak(self.game_state.get_text('expo_event_fail_damage'))
        self.game_state.fans = max(0, self.game_state.fans - 10000)
        self.base_hype = max(0, self.base_hype - 10)

    def _finish_expo(self):
        self.game_state.track_expense("marketing", self.cost)
        self.game_state.hype += self.base_hype
        self.audio.play_sound("cheer")
        self.audio.speak(self.game_state.get_text('expo_finished', cost=self.cost, hype=self.base_hype))
        return "game_menu"

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
