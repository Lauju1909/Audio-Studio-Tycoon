"""
Spielzustand für Audio Studio Tycoon - Audio Edition.

Verwaltet Firmendaten, Geld, Fans, Mitarbeiter, Engines,
Spielhistorie, Ereignisse und die Bewertungslogik.
"""

import random
import json
import os
from models import GameProject, ReviewScore, Employee, Engine, EngineFeature, RivalStudio, RivalGame
from translations import TRANSLATIONS
from game_data import (
    get_compatibility, get_ideal_sliders, SLIDER_NAMES, PLATFORMS, AUDIENCE_MULTI, AUDIENCE_PRICE,
    RANDOM_EVENTS, OFFICE_LEVELS, ENGINE_FEATURES,
    EMPLOYEE_ROLES, DEV_PHASES, GAME_SIZES,
    TREND_TOPICS, TREND_GENRES, START_TOPICS, RESEARCHABLE_TOPICS,
    START_GENRES, START_AUDIENCES, RESEARCHABLE_GENRES, RESEARCHABLE_AUDIENCES,
    RESEARCHABLE_TECHNOLOGIES,
    get_available_platforms, START_YEAR, WEEKS_PER_YEAR,
)


class GameState:
    def __init__(self):
        self.company_name = ""
        self.money = 100000
        self.fans = 0
        self.week = 1
        self.game_history = []    # Liste aller GameProject
        self.high_score = 0.0
        self.games_made = 0
        self.total_revenue = 0

        # Trends
        self.current_trend = {}  # {'topic': '...', 'genre': '...', 'week_started': X}
        self.last_trend_week = 0

        # Mitarbeiter
        self.employees = []

        # Engines
        self.engines = []
        self.unlocked_features = []  # Liste von EngineFeature (freigeschaltet)
        self._init_starter_engine()

        # Büro
        self.office_level = 0  # Index in OFFICE_LEVELS

        # Ereignisse
        self.last_event_week = 0
        self.active_events = []

        # Forschungs-System
        self.is_researching = False
        self.research_progress = 0
        self.research_total_weeks = 0
        self.current_research_draft = None
        
        self.unlocked_topics = list(START_TOPICS)
        # Historische Themen für 1930 direkt beim Start hinzufügen
        from game_data import get_historical_topics_for_year
        for ht in get_historical_topics_for_year(START_YEAR):
            if ht["name"] not in self.unlocked_topics:
                self.unlocked_topics.append(ht["name"])
        self.unlocked_genres = list(START_GENRES)
        self.unlocked_audiences = list(START_AUDIENCES)
        self.unlocked_technologies = []

        # Aktuelles Projekt
        self.current_draft = {
            "name": "",
            "topic": None,
            "genre": None,
            "platform": None,
            "audience": None,
            "engine": None,
            "sliders": {},
            "size": "Mittel",
            "marketing": "Kein Marketing",
        }
        
        # Posteingang
        self.emails = []
        # Willkommensnachricht: Die 1930er Ära
        from models import Email
        self.emails.append(Email(
            sender="Historiker",
            subject="Willkommen in der Pionierzeit!",
            body="Das Jahr ist 1930. Du bist ein Visionär mit einer großen Idee: Man kann Maschinen beibringen, Spiele zu spielen und zu entwickeln! Mit bescheidenen Mitteln in einer Garage beginnst du dein Studio. Verfügbare Themen: Abakus, Mathematik, Schach und Logistik. Kämpfe dich durch die Geschichte – von der Weltwirtschaftskrise bis zur KI-Revolution 2023!",
            date_week=1
        ))
        
        # Aktive MMOs
        self.active_mmos = []

        # Einstellungen
        self.settings = {
            "language": "de",
            "music_enabled": True,
            "tts_engine": "auto", # mgl: auto, nvda, sapi
            "auto_update": True
        }

        # Echtzeit-Zeitsteuerung
        self.time_speed = 1.0  # 0=Pause, 1=Normal, 2=Schnell, 4=Sehr Schnell
        self.pause_for_menu = False # Flag für Menüs (z.B. Texteingabe)
        self.week_progress = 0.0
        self.is_developing = False
        self.dev_progress = 0.0
        self.dev_total_weeks = 0
        self.active_project = None
        self.crunch_active = False
        self.current_bugs = 0
        self.hype = 0.0
        self.active_expo_hype = 0
        
        # NEU: Phase 7 - Konkurrenz & GOTY
        self.rivals = self._init_rivals()
        self.last_goty_year = 0
        self.goty_history = {}
        
        # NEU: Phase 7 - DevKits & Hardware Markt
        self.bought_platforms = ["PC (MS-DOS)"]
        self.active_platforms = [p['name'] for p in get_available_platforms(1)]
        
        # NEU: Phase 7 - Finanzen & Buchhaltung
        self.bank_loan = None
        self.accounting = {"income": 0, "expenses": 0, "loan_paid": 0}
        
        # NEU: Phase 7 - Eigene Konsole
        self.custom_consoles = []
        self.is_developing_console = False
        self.console_progress = 0
        self.console_total_weeks = 50
        self.current_console_draft = None

        # NEU: Phase A - Schwierigkeitsgrad
        self.difficulty = 1  # Index in DIFFICULTY_LEVELS (0=Einfach, 1=Normal, 2=Schwer, 3=Legendär)

        # NEU: Phase A - Verkaufscharts
        self.chart_history = []  # [{'week': X, 'entries': [{'name':..., 'studio':..., 'sales':...}]}]
        self.my_goty_wins = 0

        # ACHIEVEMENTS
        self.unlocked_achievements = []

        # NEU: Phase B - Lizenzen
        self.owned_licenses = []  # [{'name': str, 'purchased_week': int, 'expires_week': int, 'used': bool}]
        self.active_licenses = self.owned_licenses  # Alias für Kompatibilität

        # NEU: Phase B - Addons
        self.active_addons = []  # Addon-Projekte die verkaufen

        # NEU: Phase B - Bundles
        self.active_bundles = [] # Bundle-Projekte die stetig verkaufen

        # Pending Events (dynamisch gesetzt, hier initialisiert für Stabilität)
        self.pending_goty_results = None
        self.pending_dev_event = None

        # NEU: Phase C - Produktion & Retail
        self.has_presswerk = False
        self.storage_capacity = 0
        self.used_storage = 0
        self.current_production_draft = None

        # NEU: Phase D - MMO & Server
        self.has_server_room = False
        self.server_capacity = 0
        
        # NEU: Phase E - Publisher Rolle
        self.publishing_offers = []
        self.published_third_party_games = []

        # Keybindings initialisieren (Standardwerte)
        import pygame
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN
        self.key_confirm = pygame.K_RETURN
        self.key_back = pygame.K_BACKSPACE
        self.key_home = pygame.K_HOME
        self.key_end = pygame.K_END

        # NEU: Phase F - Merch und Turniere
        self.active_merch = []
        self.active_tournaments = []

        # NEU: Phase G - Büro-Bau (Grid)
        self.office_grid = [[None for _ in range(10)] for _ in range(10)] # 10x10 Raster
        self.office_items = [] # [{'type': 'wall', 'x': 0, 'y': 0}, ...]
        
        # NEU: Phase G - Multitasking
        self.background_dev_active = True # Erlaubt das Verlassen des Dev-Check Screens

        # NEU: Lokales Mod-System
        try:
            from mod_manager import ModManager
            self.mod_manager = ModManager()
            self.mod_manager.apply_active_mods()
        except Exception as e:
            print(f"Fehler beim Laden des ModManagers: {e}")

    def get_market_platforms(self):
        from game_data import get_available_platforms
        base = get_available_platforms(self.week)
        out = list(base)
        for cc in getattr(self, "custom_consoles", []):
            if self.week >= cc.release_week:
                # Für spielereigene Konsole zahlt man 0 Lizenzgebühr
                out.append({
                    "name": cc.name,
                    "market_multi": cc.market_share,
                    "license_fee": 0
                })
        return out

    def load_global_settings(self):
        """Lädt systemweite Einstellungen inkl. Keybindings."""
        sets = {}
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r", encoding="utf-8") as f:
                    sets = json.load(f)
            except Exception:
                pass
                
        self.settings = sets
        
        # Tasten auslesen (falls vorhanden), ansonsten Standard lassen
        import pygame
        self.key_up = sets.get("key_up", pygame.K_UP)
        self.key_down = sets.get("key_down", pygame.K_DOWN)
        self.key_confirm = sets.get("key_confirm", pygame.K_RETURN)
        self.key_back = sets.get("key_back", pygame.K_BACKSPACE)
        self.key_home = sets.get("key_home", pygame.K_HOME)
        self.key_end = sets.get("key_end", pygame.K_END)
        
        # ... abwärtskompatibilität ...
        return sets

    def save_global_settings(self):
        """Speichert globale Einstellungen ab."""
        self.settings["key_up"] = self.key_up
        self.settings["key_down"] = self.key_down
        self.settings["key_confirm"] = self.key_confirm
        self.settings["key_back"] = self.key_back
        self.settings["key_home"] = self.key_home
        self.settings["key_end"] = self.key_end
        
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def _init_rivals(self):
        """Erstellt 3 Konkurrenz-Studios."""
        return [
            RivalStudio("MicroHard", target_market_share=30, next_release_week=random.randint(10, 30)),
            RivalStudio("Electric Farts", target_market_share=25, next_release_week=random.randint(20, 45)),
            RivalStudio("Nintengo", target_market_share=20, next_release_week=random.randint(35, 60))
        ]

    def _init_starter_engine(self):
        """Erstellt die Starter-Engine mit Basis-Features."""
        starter_features = []
        for f_data in ENGINE_FEATURES:
            if f_data["cost"] == 0:
                feat = EngineFeature(f_data["category"], f_data["name"], f_data["tech_bonus"])
                starter_features.append(feat)
                self.unlocked_features.append(feat)

        starter = Engine("Basis-Engine", starter_features)
        self.engines.append(starter)

    def reset_draft(self):
        """Setzt den aktuellen Entwurf zurück."""
        self.current_draft = {
            "name": "",
            "topic": None,
            "genre": None,
            "platform": None,
            "audience": None,
            "engine": None,
            "sliders": {},
            "size": "Mittel",
            "marketing": "Kein Marketing",
            "sub_genre": None,
            "publisher": None,
        }
        self.aaa_event_triggered = False

    def start_development(self):
        """Startet die Entwicklung des konfigurierten Spiels."""
        name = self.current_draft.get("name", "Untitled") or "Untitled"
        topic = self.current_draft.get("topic", "Abakus")
        genre = self.current_draft.get("genre", "Action")
        platform = self.current_draft.get("platform", {"name": "PC"})
        audience = self.current_draft.get("audience", "Jeder")
        engine = self.current_draft.get("engine", None)
        size = self.current_draft.get("size", "Mittel")
        marketing = self.current_draft.get("marketing", "Kein Marketing")
        sliders = self.current_draft.get("sliders", {})
        
        plat_name = platform['name'] if isinstance(platform, dict) else platform
        
        from models import GameProject
        self.active_project = GameProject(
            name=name, topic=topic, genre=genre, sliders=sliders,
            platform=plat_name, audience=audience, engine=engine,
            size=size, marketing=marketing
        )
        
        self.active_project.sequel_number = self.current_draft.get("sequel_number", 0)
        self.active_project.sub_genre = self.current_draft.get("sub_genre", None)
        self.active_project.license_bonus = 0.0
        
        self.is_developing = True
        self.dev_progress = 0
        
        base_weeks = 10
        if size == "Klein": base_weeks = 5
        elif size == "Mittel": base_weeks = 15
        elif size == "Groß": base_weeks = 30
        elif size == "AAA": base_weeks = 60
        self.dev_total_weeks = base_weeks
        
        self.current_bugs = getattr(self, "current_bugs", 0)
        self.dev_ready_to_finish = False

    def get_text(self, key, **kwargs):
        """Holt einen übersetzten Text basierend auf dem aktuellen Sprach-Setting."""
        lang = self.settings.get("language", "de")
        text = TRANSLATIONS.get(lang, TRANSLATIONS['de']).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def get_calendar_year(self):
        """Gibt das aktuelle Kalenderjahr zurück (Start: START_YEAR)."""
        return START_YEAR + (self.week - 1) // WEEKS_PER_YEAR

    def get_calendar_text(self):
        """Gibt Kalenderjahr und Woche zurück (48 Wochen pro Jahr, Start 1930)."""
        year = self.get_calendar_year()
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        lang = self.settings.get("language", "de")
        if lang == "de":
            return f"{year}, KW {week_in_year}"
        else:
            return f"{year}, Week {week_in_year}"

    def get_speed_text(self):
        """Gibt Text für aktuelle Geschwindigkeit zurück."""
        if self.time_speed == 0: 
            return self.get_text('paused')
        if self.time_speed == 0.5:
            return self.get_text('speed_slow')  
        if self.time_speed == 1: 
            return self.get_text('speed_normal')
        if self.time_speed == 2: 
            return self.get_text('speed_fast')
        return self.get_text('speed_ultra')

    def update_tick(self, dt_ms):
        """Aktualisiert Spielzeit basierend auf Millisekunden."""
        if self.time_speed == 0 or self.pause_for_menu:
            return

        ms_per_week = 15000 / self.time_speed
        self.week_progress += dt_ms / ms_per_week
        
        # Hype Decay (ca. 10% pro Woche)
        if self.hype > 0:
            decay_sec = 0.1 * (dt_ms / ms_per_week)
            self.hype = max(0.0, self.hype - decay_sec)

        if self.week_progress >= 1.0:
            self.week_progress -= 1.0
            self.week += 1
            self._on_new_week()

    def _on_new_week(self):
        """Logik die jede Woche passiert (Gehalt, Zufallsereignisse)."""
        # Jahres-Reset für Buchhaltung
        if (self.week - 1) % WEEKS_PER_YEAR == 0:
            self.accounting = {"income": 0, "expenses": 0, "loan_paid": 0}
            
        # Gehälter abziehen
        total_salary = sum(e.salary for e in self.employees)
        self.money -= total_salary
        self.accounting["expenses"] += total_salary
        
        # NEU Phase H: Erweiterte Mitarbeiter-Logik (Moral, Kündigungen, Gehalt)
        quitting_employees = []
        for i, emp in enumerate(self.employees):
            emp.weeks_employed += 1
            if not getattr(self, 'crunch_active', False):
                emp.morale = min(100, emp.morale + 2)
                
            # Kündigung wegen Burnout
            if emp.morale == 0 and random.random() < 0.05:
                quitting_employees.append(emp)
                continue
                
            # Gehaltsforderung (E-Mail)
            if not getattr(emp, 'pending_raise_request', False) and (self.week - getattr(emp, 'last_raise_week', 0)) > 20:
                expected_salary = sum(emp.skills.values()) * 5 + 500
                # Will eine Erhöhung, wenn sein Skill 30% mehr wert ist als er verdient
                if expected_salary > emp.salary * 1.3 and random.random() < 0.1:
                    emp.pending_raise_request = True
                    from models import Email
                    new_salary = int(emp.salary * 1.25)
                    mail_subj = self.get_text('subject_salary_raise')
                    mail_body = self.get_text('body_salary_raise', name=emp.name, current=emp.salary, expected=new_salary)
                    
                    mail = Email(sender=emp.name, subject=mail_subj, body=mail_body, date_week=self.week)
                    mail.is_salary_request = True
                    mail.employee_idx = i
                    mail.requested_salary = new_salary
                    self.emails.insert(0, mail)
                    
        for e in quitting_employees:
            if e in self.employees:
                self.employees.remove(e)
            from models import Email
            self.emails.insert(0, Email(
                sender=e.name,
                subject=self.get_text('subject_quit'),
                body=self.get_text('body_quit', name=e.name),
                date_week=self.week
            ))

        
        # Kreditabzahlung
        if getattr(self, "bank_loan", None):
            payment = self.bank_loan.weekly_payment
            self.money -= payment
            self.accounting["loan_paid"] += payment
            self.bank_loan.amount_remaining -= payment
            self.bank_loan.weeks_remaining -= 1
            if self.bank_loan.weeks_remaining <= 0 or self.bank_loan.amount_remaining <= 0:
                self.bank_loan = None
                from models import Email
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_bank'),
                    subject=self.get_text('subject_loan_paid'),
                    body=self.get_text('body_loan_paid'),
                    date_week=self.week
                ))
        
        # Trend check (alle 20-40 Wochen)
        if self.week - self.last_trend_week >= random.randint(20, 40):
            if self.week % 8 == 0:
                self.generate_trend()
                
        # Zufallsereignisse prüfen
        self.check_random_event()
        
        # Abgelaufene Events entfernen
        new_active = []
        for e in self.active_events:
            if "duration" in e:
                e["duration"] -= 1
                if e["duration"] > 0:
                    new_active.append(e)
            else:
                new_active.append(e) # Wenn keine Dauer, bleibt es aktiv (oder sollte gelöscht werden? Sicherer: Wir setzen default duration auf 0 beim Event erstellen)
        self.active_events = new_active
        
        # Neu: Historische Themen und Events ab neuem Spieljahr
        if (self.week - 1) % WEEKS_PER_YEAR == 0 and self.week > 1:
            self._unlock_historical_topics()
            from game_data import get_year_event
            year = self.get_calendar_year()
            y_event = get_year_event(year)
            if y_event:
                self.apply_event({
                    "id": f"hist_{year}",
                    "effect": y_event.get("effect"),
                    "value": y_event.get("value", 0),
                    "text": y_event["text"],
                    "title": f"Historisches Ereignis {year}"
                })
                
        # Marktanteil der eigenen Konsole erhöhen
        if hasattr(self, "custom_consoles"):
            for cc in self.custom_consoles:
                cc.market_share = min(0.5, cc.market_share + (cc.tech_level * 0.0005))
            
        # Projektfortschritt falls aktiv
        if self.is_developing:
            boost = 2 if self.crunch_active else 1
            # Remaster-Bonus: 1.5x schneller
            if self.current_draft.get("is_remaster"):
                boost *= 1.5
                
            # Burnout-Event Malus / Talent-Boom Bonus
            for e in self.active_events:
                if e["effect"] == "dev_speed_drop":
                    boost *= e["multiplier"]
                elif e["effect"] == "dev_speed_boost":
                    boost *= e["multiplier"]
            
            # Team Speed Modifier durch Eigenschaften
            boost *= self.get_team_speed_modifier()
            
            self.dev_progress += boost
            
            if self.crunch_active:
                has_break = self.has_office_bonus("morale_room")
                break_mod = 0.5 if has_break else 1.0
                # Moral-Malus
                for emp in self.employees:
                    morale_loss = int(random.randint(2, 5) * break_mod)
                    if emp.trait and emp.trait["effect"] == "morale_loss":
                        morale_loss = int(morale_loss * emp.trait["value"])
                    emp.morale = max(0, emp.morale - morale_loss)
                    
                # Bug-Zuwachs
                base_bugs = random.randint(1, 3)
                self.current_bugs += int(base_bugs * self.get_team_bug_modifier())
            
            # Zufällige Bugs auch ohne Crunch (seltener)
            if random.random() < 0.1:
                self.current_bugs += int(1 * self.get_team_bug_modifier())
                
            # Supporter fixen aktiv Bugs jede Woche während der Entwicklung
            supporter_count = sum(1 for e in self.employees if e.role == "Supporter")
            if supporter_count > 0 and self.current_bugs > 0:
                self.current_bugs = max(0, self.current_bugs - supporter_count)

            # AAA Events (Max 1x pro Projekt)
            if self.current_draft.get("size") == "AAA" and not getattr(self, "aaa_event_triggered", False):
                if 0.2 < (self.dev_progress / max(1, getattr(self, "dev_total_weeks", 1))) < 0.8:
                    if random.random() < 0.05:  # 5% Chance pro Woche
                        from game_data import AAA_DEV_EVENTS
                        self.pending_dev_event = random.choice(AAA_DEV_EVENTS)
                        self.aaa_event_triggered = True
                        self.time_speed = 0 # Pause game

        # Forschungsfortschritt
        elif self.is_researching:
            self.research_progress += 1
            if self.research_progress >= self.research_total_weeks:
                self.complete_research()

        # Konsolenentwicklung
        if getattr(self, "is_developing_console", False):
            self.console_progress += 1
            if self.console_progress >= self.console_total_weeks:
                self.is_developing_console = False
                c = self.current_console_draft
                from models import CustomConsole, Email
                new_console = CustomConsole(c['name'], c['tech_level'], c['cost'], self.week)
                if not hasattr(self, "custom_consoles"): 
                    self.custom_consoles = []
                self.custom_consoles.append(new_console)
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_hardware'),
                    subject=self.get_text('subject_console_done'),
                    body=self.get_text('body_console_done', name=c['name']),
                    date_week=self.week
                ))
                self.current_console_draft = None

        # Zufällige Branchen-News (5% Chance pro Woche)
        if random.random() < 0.05:
            self._generate_industry_news()

        # Expo Trigger (Woche 26 jedes Jahr)
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        if week_in_year == 24:  # Expo in Woche 24 jedes Spieljahres
            from models import Email
            self.emails.append(Email(
                sender=self.get_text('sender_assistant'),
                subject=self.get_text('subject_expo'),
                body=self.get_text('body_expo'),
                date_week=self.week
            ))
            
        # NEU: Phase B - Lizenzen ablaufen lassen
        # Wird in advance_week direkt verarbeitet

        # NEU: Phase 7 - Rivalen und GOTY evaluieren
        self._process_rivals()
        if week_in_year == WEEKS_PER_YEAR:
            self._check_goty()

    def calculate_hype(self, project):
        """Berechnet den Hype für ein Spiel basierend auf Marketing, Lizenzen und Events."""
        hype = 0
        # Marketing
        if project.marketing == self.get_text('marketing_small'):
            hype += 10
        elif project.marketing == self.get_text('marketing_medium'):
            hype += 25
        elif project.marketing == self.get_text('marketing_large'):
            hype += 50
        elif project.marketing == self.get_text('marketing_viral'):
            hype += 75
        
        # Publisher Marketing
        if getattr(project, 'marketing', None) == self.get_text('marketing_publisher_deal'):
            hype += 40
            
        # Lizenzen
        if getattr(project, 'license_bonus', 0) > 0:
            hype += project.license_bonus

        # Zufallsereignis Bonus
        for event in self.active_events:
            if event["effect"] == "hype_boost":
                hype += event["amount"]

        return min(250, int(hype))

    def _process_rivals(self):
        """Lässt Rivalen Spiele veröffentlichen und Marktanteile beeinflussen."""
        from game_data import TREND_TOPICS, TREND_GENRES
        from models import Email
        
        for rival in self.rivals:
            if self.week >= rival.next_release_week:
                # Rivale veröffentlicht ein Spiel!
                topic = random.choice(TREND_TOPICS)["topic"]
                genre = random.choice(TREND_GENRES)["genre"]
                
                # Konkurrenz wird im Laufe der Jahre etwas besser
                base_score = random.uniform(5.5, 8.5)
                year = self.get_calendar_year()
                # Boost: 0.1 pro Jahr seit START_YEAR, max +2.5
                score_boost = min(2.5, (year - START_YEAR) * 0.1)
                base_score += score_boost
                score = round(min(10.0, base_score), 1)
                
                r_game = RivalGame(f"{rival.name} {genre}", topic, genre, score, week_developed=self.week)
                rival.games.append(r_game)
                rival.next_release_week = self.week + random.randint(30, 70)
                
                # Benachrichtigung
                if score >= 8.5:
                    self.emails.append(Email(
                        sender=self.get_text('sender_industry_news'),
                        subject=self.get_text('subject_rival_hit', name=rival.name),
                        body=self.get_text('body_rival_hit', name=rival.name, game=r_game.name, score=score, genre=self.get_text(genre)),
                        date_week=self.week
                    ))

                # Dividende ausschütten, falls Anteile besessen werden
                if getattr(rival, 'is_owned_by_player', False):
                    # 100% Einnahmen!
                    income = int(score * 100000)
                    self.money += income
                    self.accounting["income"] += income
                    self.emails.append(Email(
                        sender=self.get_text('sender_bank'),
                        subject=self.get_text('subject_studio_income'),
                        body=self.get_text('body_studio_income', name=rival.name, amount=income),
                        date_week=self.week
                    ))
                elif getattr(rival, 'owned_shares', 0) > 0:
                    dividend = int((score * 10000) * (rival.owned_shares / 100))
                    self.money += dividend
                    self.accounting["income"] += dividend
                    self.emails.append(Email(
                        sender=self.get_text('sender_bank'),
                        subject=self.get_text('subject_dividend'),
                        body=self.get_text('body_dividend', name=rival.name, amount=dividend),
                        date_week=self.week
                    ))
                
                # Marktauswirkung: Zieht Hype und Verkäufe ab, wenn wir auch ein Spiel im gleichen Genre haben
                for my_game in self.game_history:
                    if my_game.is_active and my_game.genre == genre:
                        # Unser Spiel verliert Hype
                        self.hype = max(0, self.hype - 10)
                        # Verkäufe sinken für diese Woche (implizit verringert, da Hype sinkt)

    def _unlock_historical_topics(self):
        """Schaltet neue historische Themen basierend auf dem aktuellen Spieljahr frei und verarbeitet Jahresevents."""
        from game_data import get_newly_unlocked_topics, get_year_event
        from models import Email
        
        current_year = self.get_calendar_year()
        new_topics = get_newly_unlocked_topics(current_year)
        
        newly_added = []
        for t in new_topics:
            if t["name"] not in self.unlocked_topics:
                self.unlocked_topics.append(t["name"])
                newly_added.append(t)
        
        if newly_added:
            hype_texts = {1: "gering", 2: "mittel", 3: "hoch", 4: "extrem", 5: "gigantisch"}
            lines = []
            for t in newly_added:
                hype_str = hype_texts.get(t["hype_level"], "?")
                lines.append(f"• {t['name']} (passt zu: {t['synergy']}, Hype: {hype_str})")
            topic_list = "\n".join(lines)
            self.emails.insert(0, Email(
                sender="Historiker",
                subject=f"{current_year}: Neue Themen verfügbar!",
                body=f"Das Jahr {current_year} bringt neue Themen, die der Zeitgeist inspiriert:\n\n{topic_list}\n\nNutze sie für dein nächstes Spiel!",
                date_week=self.week
            ))

        # Historisches Jahresevent prüfen und anwenden
        year_event = get_year_event(current_year)
        if year_event:
            effect = year_event["effect"]
            value = year_event["value"]
            event_text = year_event["text"]
            
            if effect == "money":
                self.money += value
                self.accounting["income" if value > 0 else "expenses"] += abs(value)
            elif effect == "fans":
                self.fans += value
            elif effect == "hype":
                self.hype = min(250, self.hype + value)

            # E-Mail mit historischem Event
            self.emails.insert(0, Email(
                sender="Weltgeschehen",
                subject=f"{current_year}: Aktuelles Ereignis",
                body=f"{event_text}\n\nAuswirkung auf dein Studio: "
                     + (f"+{value:,} €" if effect == "money" and value > 0
                        else f"{value:,} €" if effect == "money"
                        else f"+{value:,} Fans" if effect == "fans"
                        else f"+{value} Hype"),
                date_week=self.week
            ))


    def _check_goty(self):
        """Ermittelt das Spiel des Jahres."""
        year = self.get_calendar_year()
        
        # Bereits vergeben?
        if year == self.last_goty_year: 
            return
        self.last_goty_year = year
        
        # Alle Spiele dieses Jahres (Spieler)
        my_games_this_year = [g for g in self.game_history if (START_YEAR + (g.week_developed - 1) // WEEKS_PER_YEAR) == year]
        my_best = max(my_games_this_year, key=lambda g: getattr(g.review, 'average', 0)) if my_games_this_year else None
        
        # Alle Spiele dieses Jahres (Rivalen)
        rival_games_this_year = []
        for r in self.rivals:
            # Finde das beste Spiel dieses Rivalen, das in DIESEM Jahr erschienen ist
            yearly_rival_games = [rg for rg in r.games if (START_YEAR + (rg.week_developed - 1) // WEEKS_PER_YEAR) == year]
            if yearly_rival_games:
                best_rg = max(yearly_rival_games, key=lambda g: g.score)
                rival_games_this_year.append((r.name, best_rg))
                
        rival_best_tuple = max(rival_games_this_year, key=lambda t: t[1].score) if rival_games_this_year else None
        
        my_score = my_best.review.average if my_best and my_best.review else 0
        rival_score = rival_best_tuple[1].score if rival_best_tuple else 0
        
        if my_score == 0 and rival_score == 0:
            return # Kein Spiel erschienen
            
        goty_data = {
            "year": year,
            "my_score": my_score,
            "my_game": my_best.name if my_best else None,
            "rival_score": rival_score,
            "rival_name": rival_best_tuple[0] if rival_best_tuple else None,
            "rival_game": rival_best_tuple[1].name if rival_best_tuple else None,
        }
        
        # Track wins for achievements
        if my_score > rival_score and my_score > 0:
            if not hasattr(self, "my_goty_wins"):
                self.my_goty_wins = 0
            self.my_goty_wins += 1
        
        self.pending_goty_results = goty_data

    def _generate_industry_news(self):
        """Erzeugt zufällige Markt-Ereignisse."""
        from models import Email
        news_types = [
            {"text": self.get_text('news_hardware_boom'), "multi": 1.2},
            {"text": self.get_text('news_recession'), "multi": 0.85},
            {"text": self.get_text('news_rival_bankrupt'), "multi": 1.0},
        ]
        news = random.choice(news_types)
        # Email-Objekt erstellen
        mail = Email(
            sender=self.get_text('sender_industry_news'),
            subject=self.get_text('news_title'),
            body=news["text"],
            date_week=self.week
        )
        self.emails.append(mail)

    # ==========================================================
    # MITARBEITER
    # ==========================================================

    def get_max_employees(self):
        """Maximale Mitarbeiter basierend auf Bauräumen."""
        max_emp = 1 # Start in Garage
        for item in getattr(self, "office_items", []):
            if "employees" in item:
                max_emp += item["employees"]
        return max_emp

    def can_hire(self):
        return len(self.employees) < self.get_max_employees()

    def generate_candidate(self):
        """Generiert einen zufälligen Bewerber."""
        from game_data import EMPLOYEE_SPECIALIZATIONS
        role_data = random.choice(EMPLOYEE_ROLES)
        level = random.randint(1, min(3, 1 + self.games_made // 3))
        
        spec = None
        if random.random() < 0.3: # 30% Chance auf Spezialisierung
            spec = random.choice(EMPLOYEE_SPECIALIZATIONS)
            
        return Employee(role_data=role_data, skill_level=level, specialization=spec)

    def hire_employee(self, employee):
        """Stellt einen Mitarbeiter ein."""
        if not self.can_hire():
            return False
        # Einstellungsgebühr = 2 Wochen Gehalt
        hire_cost = employee.salary * 2
        if self.money < hire_cost:
            return False
        self.money -= hire_cost
        self.employees.append(employee)
        return True

    def fire_employee(self, index):
        """Entlässt einen Mitarbeiter."""
        if 0 <= index < len(self.employees):
            emp = self.employees.pop(index)
            # Abfindung = 4 Wochen Gehalt
            self.money -= emp.salary * 4
            return emp
        return None

    def pay_salaries(self):
        """Bezahlt alle Gehälter (wöchentlich)."""
        total = sum(e.salary for e in self.employees)
        self.money -= total
        return total

    def advance_week(self, weeks=1):
        """Rückt die Zeit vor und verarbeitet wöchentliche Ereignisse."""
        for _ in range(weeks):
            self.week += 1
            self.pay_salaries()
            
            # Trends und Zufallsereignisse
            self.check_random_event()
            
            # Saisonale Modifikatoren berechnen
            week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
            season_mod = 1.0
            if 48 <= week_in_year <= 52:
                season_mod = 1.5  # Weihnachtsgeschäft
            elif 28 <= week_in_year <= 32:
                season_mod = 0.8  # Sommerloch
                
            # Achievements prüfen
            self._check_achievements()
            
            # Verkäufe für aktive Spiele
            for g in self.game_history:
                if g.is_active:
                    g.weeks_on_market += 1
                    # Verkäufe sinken mit der Zeit, plus saisonale Effekte
                    new_sales = int((self.calculate_sales(g) * season_mod) / (1 + g.weeks_on_market * 0.2))
                    if g.bugs > 0:
                        new_sales = int(new_sales * 0.5) # Bugs halbieren Verkäufe
                        
                    # Hacker-Event Malus
                    for e in self.active_events:
                        if e["effect"] == "sales_drop":
                            new_sales = int(new_sales * e["multiplier"])
                        elif e["effect"] == "sales_boost":
                            new_sales = int(new_sales * e["multiplier"])
                    
                    price = AUDIENCE_PRICE.get(g.audience, 30)
                    
                    # Physikalischer Verkauf zuerst
                    physical_sold = 0
                    if getattr(g, "physical_copies", 0) > 0:
                        physical_sold = min(new_sales, g.physical_copies)
                        g.physical_copies -= physical_sold
                        self.used_storage -= physical_sold
                        g.lifetime_physical_sales = getattr(g, "lifetime_physical_sales", 0) + physical_sold
                        
                    digital_sold = new_sales - physical_sold
                    
                    # Physischer Retailpreis ist fix oder via Modell (hier: default 45)
                    physical_rev = physical_sold * getattr(g, "physical_price", 45)
                    digital_rev = digital_sold * price
                    
                    g.sales += new_sales
                    # Optional: Addons pushen die Verkäufe
                    for addon in self.active_addons:
                        if addon.base_game_name == g.name:
                            new_sales = int(new_sales * 1.5) # 50% Boost durch aktives Addon

                    if g.weeks_on_market > 20 or new_sales < 100:
                        g.is_active = False

            # Einnahmen durch Addons generieren
            for addon in self.active_addons:
                base_game = next((g for g in self.game_history if g.name == addon.base_game_name), None)
                if base_game and base_game.is_active:
                    # Addon Verkäufe basieren auf den Basis-Spiel-Verkäufen
                    sales = int(base_game.sales * 0.05 / (1 + (self.week - addon.week_developed) * 0.1))
                    if sales > 0:
                        revenue = sales * 15 # Addons kosten fix 15
                        addon.sales += sales
                        addon.revenue += revenue
                        self.money += revenue
                        if hasattr(self, "accounting"):
                            self.accounting["income"] += revenue

            # Einnahmen durch Bundles generieren
            for bundle in self.active_bundles:
                from game_data import BUNDLE_DATA
                # Bundles verkaufen sich langsam aber stetig für lange Zeit.
                sales = max(10, int(500 * (bundle.average_score / 10) * BUNDLE_DATA["revenue_mod"]))
                revenue = sales * bundle.base_price
                bundle.sales += sales
                bundle.revenue += revenue
                self.money += revenue
                if hasattr(self, "accounting"):
                    self.accounting["income"] += revenue

            # Lizenzen verwalten (werden in Wochen heruntergezählt oder durch Kauf fixiert)
            # Eine Nutzung wird beim Release eines Spiels markiert (used=True)
            licenses_to_remove = []
            for license in self.active_licenses:
                if license.duration > 0:
                    license.duration -= 1
                if license.duration <= 0 and not license.used: # Only expire if not used for a game
                    licenses_to_remove.append(license)
            
            from models import Email
            for license in licenses_to_remove:
                self.active_licenses.remove(license)
                self.emails.append(Email(
                    sender=self.get_text('sender_system'),
                    subject=self.get_text('subject_license_expired'),
                    body=self.get_text('body_license_expired', name=license.name),
                    date_week=self.week
                ))

            # MMOs verarbeiten (Einnahmen, Kosten, Spielerschwund)
            total_mmo_players = sum(m.players for m in self.active_mmos if m.game.is_active)
            server_capacity = getattr(self, 'server_capacity', 0)
            server_overloaded = total_mmo_players > server_capacity
            
            for mmo in self.active_mmos:
                if mmo.game.is_active:
                    mmo.weeks_active += 1
                    # Einnahmen und Kosten
                    self.money += mmo.weekly_revenue
                    self.money -= mmo.weekly_cost
                    mmo.game.revenue += mmo.weekly_revenue
                    
                    # Spielerschwund
                    if server_overloaded:
                        mmo.players = int(mmo.players * 0.85) # 15% Schwund bei Server-Last!
                    else:
                        mmo.players = int(mmo.players * 0.98) # Normaler Schwund 2%
                    
                    if mmo.players < 1000:
                        mmo.game.is_active = False # Server shut down

            if server_overloaded and total_mmo_players > 0:
                if self.week % 4 == 0:
                    from models import Email
                    self.emails.append(Email("System", "SERVER ÜBERLASTET", "Die Serverkapazität ist aufgebraucht! Spieler können sich nicht einloggen und kündigen massig ihre Accounts. Bitte baue sofort Server aus!", self.week, is_bug=True))

            # Fan-Mails & Bugs generieren
            self.process_emails()
            
            # NEU: Phase C - Lagerkosten
            if self.used_storage > 0:
                storage_cost = int(self.used_storage * 0.1)  # 10 Cent pro gelagerte Einheit
                self.money -= storage_cost
                if hasattr(self, "accounting"):
                    self.accounting["expenses"] += storage_cost

            # NEU: Phase F - Merchandising Verkäufe
            for merch in self.active_merch:
                if merch["stock"] > 0:
                    import random
                    base_sales = random.randint(5, 40)
                    sales = int(base_sales * merch["hype_multi"] * (1 + self.hype / 100))
                    sales = min(sales, merch["stock"])
                    
                    if sales > 0:
                        revenue = sales * merch["sell_price"]
                        self.money += revenue
                        if hasattr(self, "accounting"):
                            self.accounting["income"] += revenue
                        
                        merch["stock"] -= sales
                        merch["sales"] += sales
                        merch["revenue"] += revenue
                        self.used_storage -= sales
                        
                    if merch["stock"] <= 0:
                        from models import Email
                        self.emails.append(Email(
                            sender=self.get_text("sender_logistics"),
                            subject=self.get_text("subject_merch_sold_out"),
                            body=self.get_text("body_merch_sold_out", name=merch["name"]),
                            date_week=self.week
                        ))
            
            # Ausverkaufte Merch-Artikel entfernen
            self.active_merch = [m for m in self.active_merch if m["stock"] > 0]

            # NEU: Phase E - Zufällige Publishing Angebote generieren
            if self.office_level >= 2 and random.random() < 0.05:
                self._generate_publishing_offer()

            # NEU: Phase E - Third-Party Spiele verwalten
            for published_game in self.published_third_party_games:
                if published_game.is_active:
                    published_game.weeks_on_market += 1
                    # Vereinfachte Verkaufslogik für Third-Party
                    base_sales = published_game.quality * 1000
                    sales_this_week = int(base_sales / (1 + published_game.weeks_on_market * 0.1))
                    
                    published_game.total_sales += sales_this_week
                    
                    # Einnahmen und Aufteilung
                    gross_revenue = sales_this_week * 30 # Annahme: 30 Euro pro Spiel
                    player_cut = int(gross_revenue * published_game.player_share)
                    our_cut = gross_revenue - player_cut
                    
                    self.money += our_cut
                    self.accounting["income"] += our_cut
                    published_game.total_revenue += gross_revenue
                    published_game.player_profit += player_cut
                    
                    if sales_this_week < 50 or published_game.weeks_on_market > 30:
                        published_game.is_active = False

    def process_emails(self):
        """Generiert zufällige E-Mails."""
        from models import Email
        
        if not self.game_history:
            return
            
        # Chance auf Mail
        if random.random() < 0.2:
            game = random.choice(self.game_history)
            if random.random() < 0.5:
                # Bug Report
                game.bugs += random.randint(1, 5)
                mail = Email(
                    sender=self.get_text('sender_disappointed'),
                    subject=self.get_text('subject_bug_report', game=game.name),
                    body=self.get_text('body_bug_report', game=game.name),
                    date_week=self.week,
                    game_name=game.name,
                    is_bug=True
                )
            else:
                # Fan Mail
                mail = Email(
                    sender=self.get_text('sender_fan'),
                    subject=self.get_text('subject_fan_praise', game=game.name),
                    body=self.get_text('body_fan_praise', game=game.name, topic=self.get_text(game.topic)),
                    date_week=self.week,
                    game_name=game.name
                )
            self.emails.insert(0, mail)
            
    def release_patch(self, game_index):
        """Veröffentlicht einen kostenlosen Patch."""
        game = self.game_history[game_index]
        if game.bugs > 0:
            game.bugs = 0
            self.fans += 100
            return True
        return False

    def release_dlc(self, game_index):
        """Veröffentlicht einen kostenpflichtigen DLC."""
        game = self.game_history[game_index]
        cost = 20000
        if self.money < cost:
            return False
        self.money -= cost
        game.dlc_count += 1
        game.is_active = True # Bringt Spiel zurück in die Charts
        game.weeks_on_market = max(0, game.weeks_on_market - 5)
        self.fans += 500
        return True

    def release_mmo_update(self, mmo_index):
        """Programmiert ein Content-Update für ein MMO, um Spieler zurückzugewinnen."""
        mmo = self.active_mmos[mmo_index]
        cost = 50000
        if self.money < cost:
            return False
        self.money -= cost
        # Füge Spieler hinzu basierend auf Basis-Spielerzahl (z.B. +10% max)
        new_players = int(mmo.game.sales * 0.05)
        mmo.players += new_players
        self.fans += 1000
        return True

    def get_team_bonus(self):
        """Gesamtbonus des Teams auf Spielqualität."""
        if not self.employees:
            return 0.0
        base_bonus = sum(e.quality_contribution for e in self.employees)
        return base_bonus * self.get_team_quality_modifier()

    def get_team_slider_bonus(self, slider_name):
        """Durchschnittlicher Skill-Bonus des Teams für einen Slider."""
        if not self.employees:
            return 0.0
        bonuses = [e.get_slider_bonus(slider_name) for e in self.employees]
        return sum(bonuses) / len(bonuses)

    def get_team_speed_modifier(self):
        if not self.employees: 
            return 1.0
        mods = [e.trait["value"] if e.trait and e.trait["effect"] == "speed" else 1.0 for e in self.employees]
        return sum(mods) / len(mods)

    def get_team_bug_modifier(self):
        has_qa = self.has_office_bonus("qa")
        qa_mod = 0.8 if has_qa else 1.0
        if not self.employees: 
            return 1.0 * qa_mod
        mods = [e.trait["value"] if e.trait and e.trait["effect"] == "bugs" else 1.0 for e in self.employees]
        return (sum(mods) / len(mods)) * qa_mod

    def get_team_quality_modifier(self):
        if not self.employees: 
            return 1.0
        mods = [e.trait["value"] if e.trait and e.trait["effect"] == "quality" else 1.0 for e in self.employees]
        return sum(mods) / len(mods)

    def get_status_text(self):
        """Gibt einen vollständigen Statustext für den Screenreader aus."""
        lang = self.settings.get("language", "de")
        cal = self.get_calendar_text()
        
        # Aktive Projekte prüfen
        dev_info = ""
        if self.is_developing and self.active_project:
            proj_name = self.active_project.name if hasattr(self.active_project, 'name') else self.get_text('current_project_short')
            progress_pct = int((self.dev_progress / max(1, self.dev_total_weeks)) * 100)
            dev_info = f" | {self.get_text('developing')}: {proj_name} {progress_pct}%"
        elif self.is_researching and self.current_research_draft:
            r_name = self.current_research_draft['data']['name']
            progress_pct = int((self.research_progress / max(1, self.research_total_weeks)) * 100)
            dev_info = f" | {self.get_text('researching')}: {r_name} {progress_pct}%"
        
        # Mitarbeiter-Info
        emp_count = len(self.employees)
        max_emp = self.get_max_employees()
        
        # Ungelesene Emails
        unread = sum(1 for e in self.emails if not e.is_read)
        
        office_name = "Eigenes Studio" if getattr(self, "office_items", []) else "Garage"
        
        if lang == "de":
            status = (
                f"{self.company_name} | {cal}{dev_info} | "
                f"Kontostand: {self.money:,.0f} € | "
                f"Fans: {self.fans:,} | "
                f"Büro: {office_name} ({emp_count}/{max_emp} MA) | "
                f"Spiele: {self.games_made} | "
                f"Hype: {int(self.hype)}"
            )
            if unread > 0:
                status += f" | {unread} ungelesene E-Mails"
        else:
            status = (
                f"{self.company_name} | {cal}{dev_info} | "
                f"Balance: {self.money:,.0f} € | "
                f"Fans: {self.fans:,} | "
                f"Office: {office_name} ({emp_count}/{max_emp} staff) | "
                f"Games: {self.games_made} | "
                f"Hype: {int(self.hype)}"
            )
            if unread > 0:
                status += f" | {unread} unread emails"
        return status





    # ==========================================================
    # FORSCHUNG & ENGINES
    # ==========================================================

    def start_research(self, res_data, res_type):
        """Startet ein neues Forschungsprojekt."""
        if self.money < res_data["cost"] or self.is_researching or self.is_developing:
            return False
            
        self.money -= res_data["cost"]
        self.is_researching = True
        self.research_progress = 0
        self.research_total_weeks = res_data.get("research_weeks", 4)
        self.current_research_draft = {
            "data": res_data,
            "type": res_type
        }
        return True

    def complete_research(self):
        """Schließt die aktuelle Forschung ab."""
        self.is_researching = False
        if not self.current_research_draft:
            return
            
        res_type = self.current_research_draft["type"]
        res_data = self.current_research_draft["data"]
        
        if res_type == "feature":
            feat = EngineFeature(res_data["category"], res_data["name"], res_data["tech_bonus"])
            self.unlocked_features.append(feat)
        elif res_type == "genre":
            self.unlocked_genres.append(res_data["name"])
        elif res_type == "audience":
            self.unlocked_audiences.append(res_data["name"])
        elif res_type == "topic":
            self.unlocked_topics.append(res_data["name"])
        elif res_type == "technology":
            self.unlocked_technologies.append(res_data["name"])
            
        from models import Email
        self.emails.insert(0, Email(
            sender=self.get_text('sender_assistant'),
            subject=self.get_text('subject_research_done'),
            body=self.get_text('body_research_done', name=res_data["name"]),
            date_week=self.week
        ))
        
        # Audio Warnung für abgeschlossene Forschung
        if hasattr(self, 'audio'):
            self.audio.play_sound('success')
            self.audio.speak(self.get_text('body_research_done', name=res_data["name"]), interrupt=False)
            
        self.current_research_draft = None

    def create_engine(self, name, feature_list):
        """Erstellt eine neue Engine aus freigeschalteten Features."""
        engine = Engine(name, feature_list)
        self.engines.append(engine)
        return engine

    def get_researchable_features(self):
        """Features die erforschbar, aber noch nicht freigeschaltet sind."""
        unlocked_names = {f.name for f in self.unlocked_features}
        return [f for f in ENGINE_FEATURES if f["name"] not in unlocked_names and self.week >= f.get("week", 1)]

    def get_researchable_topics(self):
        """Themen die erforschbar, aber noch nicht freigeschaltet sind."""
        return [t for t in RESEARCHABLE_TOPICS if t["name"] not in self.unlocked_topics and self.week >= t.get("week", 1)]

    def get_researchable_genres(self):
        """Genres die erforschbar, aber noch nicht freigeschaltet sind."""
        return [g for g in RESEARCHABLE_GENRES if g["name"] not in self.unlocked_genres and self.week >= g.get("week", 1)]

    def get_researchable_audiences(self):
        """Zielgruppen die erforschbar, aber noch nicht freigeschaltet sind."""
        return [a for a in RESEARCHABLE_AUDIENCES if a["name"] not in self.unlocked_audiences and self.week >= a.get("week", 1)]

    def get_researchable_technologies(self):
        """Endgame-Technologien, die noch nicht freigeschaltet sind."""
        return [t for t in RESEARCHABLE_TECHNOLOGIES if t["name"] not in self.unlocked_technologies and self.week >= t.get("week", 1)]

    # ==========================================================
    # AKTIENMARKT / INVESTMENTS
    # ==========================================================

    def get_share_price(self, rival):
        """Berechnet den Kaufpreis für 10% Anteile an einem Rivalen."""
        return 50000 + int(rival.owned_shares / 10) * 5000

    def buy_shares(self, rival_index):
        """Kauft 10% Anteile an einem Rivalen-Studio."""
        if rival_index < 0 or rival_index >= len(self.rivals):
            return False, "invalid"
        rival = self.rivals[rival_index]
        if rival.owned_shares >= 50:
            return False, "max_shares"
        price = self.get_share_price(rival)
        if self.money < price:
            return False, "no_money"
        self.money -= price
        self.accounting["expenses"] += price
        rival.owned_shares += 10
        return True, rival.owned_shares

    def sell_shares(self, rival_index):
        """Verkauft 10% Anteile an einem Rivalen-Studio."""
        if rival_index < 0 or rival_index >= len(self.rivals):
            return False, "invalid"
        rival = self.rivals[rival_index]
        if rival.owned_shares <= 0:
            return False, "no_shares"
        # Verkaufspreis = 80% des aktuellen Kaufpreises
        sell_price = int(self.get_share_price(rival) * 0.8)
        self.money += sell_price
        self.accounting["income"] += sell_price
        rival.owned_shares -= 10
        return True, rival.owned_shares

    # ==========================================================
    # BÜRO
    # ==========================================================

    def can_upgrade_office(self):
        return False

    def upgrade_office(self):
        return False

    def get_office_info(self):
        """Info über aktuelles Büro."""
        return {"name": "Eigenes Studio", "cost": 0, "max_employees": self.get_max_employees()}

    # ==========================================================
    # TRENDS
    # ==========================================================

    def update_trends(self):
        """Aktualisiert Markttrends alle 12-20 Wochen."""
        if self.week - self.last_trend_week < random.randint(12, 20):
            return None
        
        # Trend auswählen
        topic_trend = random.choice(TREND_TOPICS)
        genre_trend = random.choice(TREND_GENRES)
        
        self.current_trend = {
            "topic": topic_trend["topic"],
            "genre": genre_trend["genre"],
            "text": f"{topic_trend['text']} Und: {genre_trend['text']}",
            "week_started": self.week
        }
        self.last_trend_week = self.week
        return self.current_trend

    # ==========================================================
    # ZUFALLSEREIGNISSE
    # ==========================================================

    def check_random_event(self):
        """Prüft ob ein Zufallsereignis oder Trendwechsel ausgelöst wird."""
        # Trend prüfen
        trend = self.update_trends()
        if trend:
            return {"title": "Markttrend-Wechsel", "text": trend["text"], "effect": "trend"}

        if self.week - self.last_event_week < 8:
            return None
        if random.random() < 0.25:
            event = random.choice(RANDOM_EVENTS)
            self.last_event_week = self.week
            self.apply_event(event)
            return event
        return None

    def apply_event(self, event):
        """Wendet ein Ereignis an."""
        if event["effect"] == "money":
            self.money += event["value"]
        elif event["effect"] == "fans":
            self.fans = max(0, self.fans + event["value"])
        elif event["effect"] == "hype_boost":
            self.hype += event["hype_amount"]
        else:
            # Dauerhafte Events zur Liste hinzufügen (Kopie)
            ev_copy = dict(event)
            self.active_events.append(ev_copy)
            
        # Spieler benachrichtigen
        from models import Email
        body = self.get_text("event_" + event["id"], weeks=event.get("duration", 0), hype=event.get("hype_amount", 0))
        self.emails.insert(0, Email(
            sender="News Reader",
            subject="Markt-Ereignis",
            body=body,
            date_week=self.week
        ))
        
        # Audio Warnung
        if hasattr(self, 'audio'):
            self.audio.play_sound('warn') # Fallback wenn Datei fehlt
            self.audio.speak(body, interrupt=True)


    # ==========================================================
    # LIZENZEN (PHASE B)
    # ==========================================================
    
    def get_available_licenses(self):
        """Gibt eine Liste von Lizenzen zurück, die man kaufen kann (abhängig von Studio-Level)."""
        from game_data import LICENSES
        available = []
        for lic in LICENSES:
            # Man kann Lizenzen nur kaufen, wenn man sie noch nicht ungenutzt besitzt
            already_owned = any(owned['name'] == lic['name'] and not owned['used'] for owned in self.owned_licenses)
            if not already_owned:
                available.append(lic)
        return available
        
    def buy_license(self, license_arg):
        """Kauft eine Lizenz für das Studio (Akzeptiert Index oder Lizenz-Dict)."""
        available = self.get_available_licenses()
        license_data = None
        
        if isinstance(license_arg, int):
            if 0 <= license_arg < len(available):
                license_data = available[license_arg]
        elif isinstance(license_arg, dict):
            license_data = license_arg
            
        if not license_data:
            return False
            
        cost = license_data["base_cost"]
        if self.money >= cost:
            self.money -= cost
            self.owned_licenses.append({
                "name": license_data["name"],
                "purchased_week": self.week,
                "expires_week": self.week + 52, # Verfällt nach 1 Jahr
                "used": False,
                "hype_bonus": license_data["hype_bonus"]
            })
            return True
        return False



    def generate_publisher_deals(self):
        """Generiert eine Liste von Publisher-Deals für das aktuelle Projekt."""
        deals = []
        if not self.current_draft.get("name"):
            return deals

        # 3 Publisher Deals
        for i in range(3):
            name = f"Publisher {chr(65+i)}"
            upfront = random.randint(10000, 50000) * self.office_level
            royalty = random.randint(10, 40)
            marketing = random.choice(["Kein Marketing", "Wenig Marketing", "Großes Marketing"])
            target_score = random.randint(6, 9)
            penalty = random.randint(5000, 20000) * self.office_level
            
            deals.append({
                "name": name,
                "upfront": upfront,
                "royalty": royalty,
                "marketing": marketing,
                "target_score": target_score,
                "penalty": penalty
            })
            
        return deals

    def get_unused_licenses(self):
        """Gibt alle gekauften Lizenzen zurück, die noch nicht verfallen und unbenutzt sind."""
        valid_licenses = []
        for lic in self.owned_licenses:
            if not lic['used'] and self.week <= lic['expires_week']:
                valid_licenses.append(lic)
        return valid_licenses
        
    def get_active_licenses(self):
        """Alternativer Name für get_unused_licenses, oft genutzt in playtest."""
        return self.get_unused_licenses()

    def use_license(self, license_name):
        """Markiert eine Lizenz als genutzt und wendet sie auf den aktuellen Entwurf an."""
        for lic in self.owned_licenses:
            if lic['name'] == license_name and not lic['used'] and self.week <= lic['expires_week']:
                lic['used'] = True
                self.current_draft["license"] = lic
                return True
        return False

    # ==========================================================
    # ADDONS & BUNDLES (PHASE B)
    # ==========================================================

    def create_addon(self, base_game_idx):
        """Erstellt ein Addon für ein Basisspiel."""
        from models import AddonProject
        from game_data import ADDON_DATA
        
        base_game = self.game_history[base_game_idx]
        if not base_game.is_active:
            return None # Nur für aktive Spiele
            
        # Überprüfe ob schon ein Addon dafür existiert
        if any(a.base_game_name == base_game.name for a in self.active_addons):
            return None
            
        cost = int(base_game.dev_cost * ADDON_DATA["cost_multi"])
        if self.money < cost:
            return None
            
        self.money -= cost
        addon = AddonProject(
            base_game_name=base_game.name,
            name=f"{base_game.name}: Expansion",
            topic=base_game.topic,
            genre=base_game.genre,
            dev_cost=cost
        )
        addon.week_developed = self.week
        self.active_addons.append(addon)
        
        return {
            'name': addon.name,
            'sales': 0,
            'revenue': 0, # Wird in den nächsten Wochen generiert
            'cost': cost
        }

    def create_bundle(self, game_indices):
        """Kombiniert mehrere inaktive Spiele zu einem Bundle."""
        from models import BundleProject
        from game_data import BUNDLE_DATA
        
        if len(game_indices) < BUNDLE_DATA["min_games"] or len(game_indices) > BUNDLE_DATA["max_games"]:
            return None
            
        games = []
        for idx in game_indices:
            game = self.game_history[idx]
            if game.is_active:
                return None # Spiele müssen vom Markt sein
            games.append(game.to_dict())
            
        # Name des Bundles generieren
        topics = list(set([g['topic'] for g in games]))
        bundle_name = f"{self.company_name} {topics[0]} Collection" if topics else f"{self.company_name} Mega Bundle"
        
        bundle = BundleProject(name=bundle_name, games=games, base_price=BUNDLE_DATA["base_price"])
        self.active_bundles.append(bundle)
        
        # Initialer Boost durch Bundle-Ankündigung
        initial_sales = int(1000 * bundle.average_score)
        initial_revenue = initial_sales * bundle.base_price
        
        bundle.sales += initial_sales
        bundle.revenue += initial_revenue
        self.money += initial_revenue
        if hasattr(self, "accounting"):
            self.accounting["income"] += initial_revenue
        
        return {
            'name': bundle.name,
            'sales': bundle.sales,
            'revenue': bundle.revenue
        }

    # ==========================================================
    # BEWERTUNG
    # ==========================================================

    def calculate_review(self, project):
        """
        Berechnet die Bewertung eines Spiels.
        Inklusive Trend-Bonus.
        """
        topic = project.topic
        genre = project.genre
        sliders = project.sliders

        # 1. Synergiewert (0.0 - 1.0)
        compat_raw = get_compatibility(topic, genre)
        synergy = compat_raw / 3.0

        # 2. Slider-Match (0.0 - 1.0)
        ideal = get_ideal_sliders(genre)
        total_diff = 0
        max_diff = 0
        for sname in SLIDER_NAMES:
            player_val = sliders.get(sname, 5)
            ideal_val = ideal.get(sname, 5)
            team_bonus = self.get_team_slider_bonus(sname)
            effective_val = player_val + team_bonus
            total_diff += abs(effective_val - ideal_val)
            max_diff += 10
        slider_match = 1.0 - (total_diff / max_diff) if max_diff > 0 else 0.5

        # 3. Team-Bonus (0.0 - 1.0)
        team_quality = min(1.0, self.get_team_bonus() * 5)

        # 4. Engine-Bonus (0.0 - 1.0)
        engine_quality = 0.3
        if project.engine:
            engine_quality = min(1.0, 0.3 + project.engine.quality_bonus)

        # 5. Trend-Bonus
        trend_bonus = 1.0
        if self.current_trend:
            if topic == self.current_trend["topic"]:
                trend_bonus += 0.2
            if genre == self.current_trend["genre"]:
                trend_bonus += 0.2

        # 6. Zufallsfaktor
        random_factor = random.uniform(0.9, 1.1)

        # Basis-Score
        base_score = (
            (synergy * 0.35) +
            (slider_match * 0.35) +
            (team_quality * 0.15) +
            (engine_quality * 0.10) +
            (0.5 * 0.05)
        )
        base_score *= random_factor * trend_bonus

        # Massive Bonus for perfect synergy and slider configuration
        if synergy >= 0.8 and slider_match >= 0.8:
            base_score += 1.5

        # Sequel Bonus/Malus (IP-Rating basiert)
        sequel_num = getattr(project, 'sequel_number', 0)
        if sequel_num > 0:
            # Finde das Originalspiel oder Vorgänger in der Historie
            ip_bonus = 0
            for past in reversed(self.game_history):
                if past.topic == topic and past.genre == genre:
                    ip = getattr(past, 'ip_rating', 0)
                    if ip >= 70:
                        ip_bonus = 0.15  # Starker Hype-Bonus
                    elif ip >= 40:
                        ip_bonus = 0.05
                    elif ip < 20:
                        ip_bonus = -0.10  # Schlechte IP enttäuscht
                    break
            base_score *= (1.0 + ip_bonus)
            # Sequel-Fatigue: jedes weitere Sequel wird schwieriger
            if sequel_num >= 4:
                base_score *= 0.90
            elif sequel_num >= 3:
                base_score *= 0.95
        elif len(self.game_history) > 0:
            # Gleiche Topic+Genre Wiederholung ohne Sequel-Flag
            last = self.game_history[-1]
            if last.topic == topic and last.genre == genre:
                base_score *= 0.8

        if self.high_score > 0:
            ratio = (base_score * 10) / self.high_score
            if ratio < 0.8:
                base_score *= 0.9

        prestige = sum(item.get("cost", 0) for item in getattr(self, "office_items", [])) // 2000
        base_score *= (1.0 + prestige * 0.03)

        # Schwierigkeitsgrad-Bonus auf Review
        from game_data import DIFFICULTY_LEVELS
        diff = DIFFICULTY_LEVELS[self.difficulty]
        base_score += diff["review_bonus"] * 0.1  # Normalisiert (max ±0.1 auf 0-1 Skala)

        # Lizenz-Bonus
        base_score += getattr(project, 'license_bonus', 0.0)

        base_review = max(1.0, min(10.0, float(base_score * 10)))

        scores = []
        for _ in range(4):
            variance = random.uniform(-1.2, 1.2)
            s = int(round(max(1.0, min(10.0, base_review + variance))))
            scores.append(s)

        # NEU: Review-Texte generieren
        comments = []
        
        # Intro
        intro_key = random.choice(['review_intro_1', 'review_intro_2', 'review_intro_3'])
        intro = self.get_text(intro_key, company=self.company_name, game=project.name)
        comments.append(intro)
        
        # Story Text
        story_key = f"story_{project.topic}"
        story_text = self.get_text(story_key)
        if story_text != story_key:
            comments.append(story_text)
        
        # Positiv/Negativ basierend auf Slidern/Synergie
        if synergy >= 0.8:
            key = random.choice(['review_pos_1', 'review_pos_2', 'review_pos_3'])
            comments.append(self.get_text(key, genre=self.get_text(project.genre), topic=self.get_text(project.topic)))
        elif synergy < 0.5:
            key = random.choice(['review_neg_1', 'review_neg_2', 'review_neg_3'])
            comments.append(self.get_text(key, genre=self.get_text(project.genre), topic=self.get_text(project.topic)))
            
        if slider_match < 0.6:
            comments.append(self.get_text('review_bad_gameplay'))
        elif slider_match >= 0.9:
            comments.append(self.get_text('review_good_gameplay'))

        # Fazit
        if base_review >= 8.0:
            concl_key = 'review_concl_1'
        elif base_review >= 5.0:
            concl_key = 'review_concl_2'
        else:
            concl_key = 'review_concl_3'
        comments.append(self.get_text(concl_key))

        review = ReviewScore(scores, comments=comments)
        if review.average > self.high_score:
            self.high_score = review.average

        return review

    def calculate_sales(self, project):
        """Berechnet Verkäufe inkl. Marketing und Größe."""
        if not project.review:
            return 0

        avg = project.review.average
        # Basis-Verkäufe skalieren mit Größe
        size_data = next((s for s in GAME_SIZES if s["name"] == project.size), GAME_SIZES[1])
        base_sales = 5000 * size_data["revenue_multi"]

        if avg >= 9: 
            score_m = 6.0
        elif avg >= 8: 
            score_m = 4.0
        elif avg >= 7: 
            score_m = 2.5
        elif avg >= 6: 
            score_m = 1.8
        elif avg >= 5: 
            score_m = 1.2
        elif avg >= 4: 
            score_m = 0.8
        else: 
            score_m = 0.3

        fan_bonus = 1.0 + (self.fans / 100000)

        plat_multi = 1.0
        for p in PLATFORMS:
            if p["name"] == project.platform:
                plat_multi = p["market_multi"]
                break

        audience_multi = AUDIENCE_MULTI.get(project.audience, 1.0)
        rand_m = random.uniform(0.8, 1.2)

        # Schwierigkeitsgrad Markt-Multiplikator
        from game_data import DIFFICULTY_LEVELS
        diff_market = DIFFICULTY_LEVELS[self.difficulty]["market_multi"]

        sales = int(base_sales * score_m * fan_bonus * plat_multi * audience_multi * rand_m * diff_market)
        return sales

    def calculate_dev_cost(self, project):
        """Berechnet Entwicklungskosten inkl. Größe und Marketing."""
        # Basis-Kosten basierend auf Größe
        size_data = next((s for s in GAME_SIZES if s["name"] == project.size), GAME_SIZES[1])
        base_cost = 10000 * size_data["cost_multi"]

        # Team-Kosten
        dev_weeks = sum(p["duration_weeks"] for p in DEV_PHASES) * size_data["time_multi"]
        salary_cost = sum(e.salary for e in self.employees) * dev_weeks

        # Marketing-Kosten
        from game_data import MARKETING_OPTIONS_PH5
        mark_data = next((m for m in MARKETING_OPTIONS_PH5 if m["name"] == project.marketing), {"cost": 0})
        marketing_cost = mark_data["cost"]

        return int(base_cost + salary_cost + marketing_cost)

    def finalize_game(self, project):
        """Schließt die Spielentwicklung ab."""
        project.week_developed = self.week

        # Kosten und Marketing abziehen
        project.dev_cost = self.calculate_dev_cost(project)
        self.money -= project.dev_cost
        if hasattr(self, "accounting"):
            self.accounting["expenses"] += project.dev_cost

        project.review = self.calculate_review(project)
        # Hype-Bonus für Verkäufe
        hype_multi = 1.0 + (self.hype / 100.0)
        project.sales = int(self.calculate_sales(project) * hype_multi)

        # Reset Crunch & Bugs & Hype
        self.crunch_active = False
        self.current_bugs = 0
        self.hype = 0 # Hype wird beim Release verbraucht

        price = AUDIENCE_PRICE.get(project.audience, 30)
        total_revenue = project.sales * price
        
        # Publisher Royalties
        publisher = self.current_draft.get("publisher")
        if publisher:
            royalty_cut = int(total_revenue * publisher["royalty"])
            project.revenue = total_revenue - royalty_cut
            # Einmaliger Bonus bei Vertragsabschluss (Advance)
            self.money += publisher["advance"]
        else:
            # Self-Publishing -> Vertriebskosten
            if "Digitaler Vertrieb & Logistik" in self.unlocked_technologies:
                distribution_margin = 0.15 # 15% mit Technologie
            else:
                distribution_margin = 0.30 # 30% ohne Technologie
                
            dist_cost = int(total_revenue * distribution_margin)
            project.revenue = total_revenue - dist_cost
            project.distribution_cost = dist_cost

        self.money += project.revenue
        if hasattr(self, "accounting"):
            self.accounting["income"] += project.revenue
           # Fan-Gain durch Spiel und Lizenz
        fan_base_gain = int(project.revenue * 0.005 * (project.review.average / 10)) # Base on revenue and review score
        if getattr(project, 'license_bonus', 0) > 0:
            # Finde die Lizenz um den Fan-Bonus zu approximieren
            # Assuming license_bonus is the hype_bonus from the license data
            fan_base_gain += int(project.license_bonus * 50) # Grobe Annäherung
        self.fans += fan_base_gain
        self.games_made += 1
        self.total_revenue += project.revenue

        # Zeit vorrücken (simuliert jede Woche einzeln für Gehälter/Events)
        size_data = next((s for s in GAME_SIZES if s["name"] == project.size), GAME_SIZES[1])
        dev_weeks = int(sum(p["duration_weeks"] for p in DEV_PHASES) * size_data["time_multi"])
        
        for _ in range(dev_weeks):
            self.week += 1
            self._on_new_week()

        for emp in self.employees:
            emp.weeks_employed += dev_weeks
            if project.review and project.review.average >= 7:
                emp.morale = min(100, emp.morale + 5)
            elif project.review and project.review.average < 4:
                emp.morale = max(0, emp.morale - 10)

        # Wenn es ein MMO ist, erstelle ActiveMMO Objekt
        if project.size == "MMO":
            from models import ActiveMMO
            # Initiale Spielerzahl basierend auf Hype und Review
            initial_players = int((project.review.average * 10000) * (1 + self.hype * 0.05))
            mmo = ActiveMMO(game_project=project, initial_players=initial_players)
            self.active_mmos.append(mmo)
        # IP-Rating berechnen (0-100 basierend auf Review)
        if project.review:
            avg = project.review.average
            project.ip_rating = int(min(100, max(0, (avg - 3) * 14.3)))  # 3→0, 10→100
        
        # Sub-Genre aus Draft übernehmen
        project.sub_genre = self.current_draft.get("sub_genre", None)

        self.game_history.append(project)
        return project

    # ==========================================================
    # TRAINING
    # ==========================================================

    def train_employee(self, emp_index, train_data):
        """Verbessert Skills eines Mitarbeiters."""
        if self.money < train_data["cost"]:
            return False
        
        emp = self.employees[emp_index]
        self.money -= train_data["cost"]
        
        if train_data.get("is_specialization"):
            import random
            from game_data import EMPLOYEE_TRAITS
            # Nur gute Traits raussuchen (z.B. Speed-Booster oder Quality)
            good_traits = [t for t in EMPLOYEE_TRAITS if t["effect"] in ["speed", "quality"] and t["value"] > 1.0]
            if not good_traits:
                good_traits = EMPLOYEE_TRAITS
            emp.trait = random.choice(good_traits)
            emp.trait_learned = True
        else:
            # Skill-Boost auf Primärskill
            sname = emp.primary_skill
            emp.skills[sname] = min(100, emp.skills.get(sname, 0) + train_data["skill_boost"])
            # Kleiner Boost auf Sekundärskill
            s2 = emp.secondary_skill
            emp.skills[s2] = min(100, emp.skills.get(s2, 0) + train_data["skill_boost"] // 2)
        
        # Gehalt steigt leicht
        emp.salary = emp._calculate_salary()
        return True

    # ==========================================================
    # PLEITE CHECK
    # ==========================================================

    def is_bankrupt(self):
        """Prüft ob die Firma pleite ist."""
        return self.money < -50000  # Kreditrahmen von 50k


    # ==========================================================
    # STATUS
    # ==========================================================

    def generate_trend(self):
        """Erzeugt einen neuen Markttrend (Thema und Genre)."""
        from game_data import TREND_TOPICS, TREND_GENRES
        topic = random.choice(TREND_TOPICS)
        genre = random.choice(TREND_GENRES)
        self.current_trend = {
            "topic": topic["topic"],
            "genre": genre["genre"],
            "text": f"{topic['text']} {genre['text']}"
        }
        # Benachrichtigung via Email
        from models import Email
        self.emails.append(Email(
            sender="Marktforschung",
            subject="Marktanalyse veröffentlicht",
            body=f"Unsere Daten zeigen: {self.current_trend['text']}",
            date_week=self.week
        ))

    # ==========================================================
    # SPEICHERN / LADEN
    # ==========================================================

    def save_game(self, slot=1):
        """Speichert den Spielstand in einem Slot."""
        filepath = f"save_slot_{slot}.json"
        data = {
            "company_name": self.company_name,
            "money": self.money,
            "fans": self.fans,
            "week": self.week,
            "high_score": self.high_score,
            "games_made": self.games_made,
            "total_revenue": self.total_revenue,
            "office_level": self.office_level,
            "last_event_week": self.last_event_week,
            "last_trend_week": self.last_trend_week,
            "current_trend": self.current_trend,
            "active_events": getattr(self, "active_events", []),
            "settings": self.settings,
            "game_history": [g.to_dict() for g in self.game_history],
            "active_mmos": [m.to_dict() for m in getattr(self, "active_mmos", [])],
            "employees": [e.to_dict() for e in self.employees],
            "engines": [
                {"name": eng.name, "features": [
                    {"category": f.category, "name": f.name, "tech_bonus": f.tech_bonus}
                    for f in eng.features
                ]} for eng in self.engines
            ],
            "unlocked_features": [
                {"category": f.category, "name": f.name, "tech_bonus": f.tech_bonus}
                for f in self.unlocked_features
            ],
            "unlocked_topics": self.unlocked_topics,
            "unlocked_genres": self.unlocked_genres,
            "unlocked_audiences": self.unlocked_audiences,
            "unlocked_technologies": self.unlocked_technologies,
            "bought_platforms": getattr(self, "bought_platforms", []),
            "active_platforms": getattr(self, "active_platforms", []),
            "rivals": [r.to_dict() for r in getattr(self, "rivals", [])],
            "last_goty_year": getattr(self, "last_goty_year", 0),
            "bank_loan": self.bank_loan.to_dict() if getattr(self, "bank_loan", None) else None,
            "accounting": getattr(self, "accounting", {"income": 0, "expenses": 0, "loan_paid": 0}),
            "custom_consoles": [c.to_dict() for c in getattr(self, "custom_consoles", [])],
            "emails": [
                {
                    "sender": m.sender, "subject": m.subject, "body": m.body,
                    "date_week": m.date_week, "game_name": m.game_name,
                    "is_bug": m.is_bug, "is_read": m.is_read
                } for m in self.emails
            ],
            "has_presswerk": getattr(self, "has_presswerk", False),
            "storage_capacity": getattr(self, "storage_capacity", 0),
            "used_storage": getattr(self, "used_storage", 0),
            "has_server_room": getattr(self, "has_server_room", False),
            "server_capacity": getattr(self, "server_capacity", 0),
            "publishing_offers": [o.to_dict() for o in getattr(self, "publishing_offers", [])],
            "published_third_party_games": [g.to_dict() for g in getattr(self, "published_third_party_games", [])],
            "office_items": getattr(self, "office_items", [])
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True

    def get_save_slots_info(self):
        """Gibt Infos über die 3 verfügbaren Slots zurück."""
        slots = {}
        for i in range(1, 4):
            path = f"save_slot_{i}.json"
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    slots[i] = f"Slot {i}: {data['company_name']} (Woche {data['week']}, {data['money']:,} Euro)"
                except Exception:
                    slots[i] = f"Slot {i}: [FEHLERHAFT]"
            else:
                slots[i] = f"Slot {i}: [LEER]"
        return slots

    def load_game(self, slot=1):
        """Lädt einen Spielstand aus einem Slot."""
        filepath = f"save_slot_{slot}.json"
        if not os.path.exists(filepath):
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.company_name = data["company_name"]
        self.money = data["money"]
        self.fans = data["fans"]
        self.week = data["week"]
        self.high_score = data["high_score"]
        self.games_made = data["games_made"]
        self.total_revenue = data["total_revenue"]
        self.office_level = data["office_level"]
        self.last_event_week = data.get("last_event_week", 0)
        self.last_trend_week = data.get("last_trend_week", 0)
        self.current_trend = data.get("current_trend")
        self.active_events = data.get("active_events", [])
        self.has_presswerk = data.get("has_presswerk", False)
        self.storage_capacity = data.get("storage_capacity", 0)
        self.used_storage = data.get("used_storage", 0)
        self.has_server_room = data.get("has_server_room", False)
        self.server_capacity = data.get("server_capacity", 0)

        # Publisher Rolle laden
        self.publishing_offers = []
        if "publishing_offers" in data:
            from models import PublishingOffer
            for od in data["publishing_offers"]:
                self.publishing_offers.append(PublishingOffer(
                    od["studio_name"], od["game_name"], od["genre"], od["quality"], od["marketing_cost"], od["player_share"]
                ))

        self.published_third_party_games = []
        if "published_third_party_games" in data:
            from models import PublishedThirdPartyGame, PublishingOffer
            for gd in data["published_third_party_games"]:
                dummy_offer = PublishingOffer(gd["studio_name"], gd["game_name"], gd["genre"], gd["quality"], 0, gd["player_share"])
                g = PublishedThirdPartyGame(dummy_offer)
                g.weeks_on_market = gd.get("weeks_on_market", 0)
                g.is_active = gd.get("is_active", True)
                g.total_sales = gd.get("total_sales", 0)
                g.total_revenue = gd.get("total_revenue", 0)
                g.player_profit = gd.get("player_profit", 0)
                self.published_third_party_games.append(g)

        # Engines laden
        self.unlocked_features = []
        for fd in data.get("unlocked_features", []):
            self.unlocked_features.append(
                EngineFeature(fd["category"], fd["name"], fd["tech_bonus"])
            )
        self.unlocked_topics = data.get("unlocked_topics", list(START_TOPICS))
        self.unlocked_genres = data.get("unlocked_genres", list(START_GENRES))
        self.unlocked_audiences = data.get("unlocked_audiences", list(START_AUDIENCES))
        self.unlocked_technologies = data.get("unlocked_technologies", [])

        self.engines = []
        for ed in data.get("engines", []):
            features = [
                EngineFeature(fd["category"], fd["name"], fd["tech_bonus"])
                for fd in ed["features"]
            ]
            self.engines.append(Engine(ed["name"], features))

        # Spielhistorie laden
        self.game_history = []
        for gd in data.get("game_history", []):
            proj = GameProject(
                gd["name"], gd["topic"], gd["genre"],
                gd.get("sliders"), gd.get("platform"), gd.get("audience"),
                size=gd.get("size", "Mittel"), marketing=gd.get("marketing", "Kein Marketing")
            )
            if gd.get("review_scores"):
                proj.review = ReviewScore(gd["review_scores"])
            proj.sales = gd.get("sales", 0)
            proj.revenue = gd.get("revenue", 0)
            proj.dev_cost = gd.get("dev_cost", 0)
            proj.week_developed = gd.get("week_developed", 0)
            proj.license_bonus = gd.get("license_bonus", 0.0)
            proj.physical_copies = gd.get("physical_copies", 0)
            proj.physical_price = gd.get("physical_price", 45)
            proj.lifetime_physical_sales = gd.get("lifetime_physical_sales", 0)
            proj.is_active = gd.get("is_active", True)
            self.game_history.append(proj)

        # Aktive MMOs laden
        self.active_mmos = []
        if "active_mmos" in data:
            from models import ActiveMMO
            for md in data["active_mmos"]:
                match_game = next((g for g in self.game_history if g.name == md.get("game_dict", {}).get("name")), None)
                if match_game:
                    m = ActiveMMO(match_game, md.get("players", 0), md.get("payment_model", "Abo"))
                    m.subscription_fee = md.get("subscription_fee", 15)
                    m.server_cost_per_10k = md.get("server_cost_per_10k", 5000)
                    m.weeks_active = md.get("weeks_active", 0)
                    self.active_mmos.append(m)

        # Mitarbeiter laden
        self.employees = []
        for ed in data.get("employees", []):
            emp = Employee.__new__(Employee)
            emp.name = ed["name"]
            emp.role = ed["role"]
            emp.primary_skill = ed["primary_skill"]
            emp.secondary_skill = ed["secondary_skill"]
            emp.skill_level = ed["skill_level"]
            emp.skills = ed["skills"]
            emp.salary = ed["salary"]
            emp.morale = ed["morale"]
            emp.weeks_employed = ed["weeks_employed"]
            emp.specialization = ed.get("specialization")
            import random
            from game_data import EMPLOYEE_TRAITS
            emp.trait = ed.get("trait") if ed.get("trait") else random.choice(EMPLOYEE_TRAITS)
            self.employees.append(emp)

        # E-Mails laden
        self.emails = []
        from models import Email
        for md in data.get("emails", []):
            mail = Email(md["sender"], md["subject"], md["body"], md["date_week"], md.get("game_name"), md.get("is_bug", False))
            mail.is_read = md.get("is_read", False)
            self.emails.append(mail)

        self.settings = data.get("settings", {"language": "de", "music_enabled": True})

        # Rivalen laden
        self.rivals = []
        for r_data in data.get("rivals", []):
            games = []
            for g_data in r_data.get("games", []):
                rg = RivalGame(g_data["name"], g_data["topic"], g_data["genre"], g_data["score"], g_data["weeks_on_market"])
                rg.is_active = g_data.get("is_active", True)
                games.append(rg)
            rival = RivalStudio(r_data["name"], r_data.get("target_market_share", 10), games, r_data.get("next_release_week"))
            self.rivals.append(rival)
            
        if not self.rivals:
            self.rivals = self._init_rivals()
            
        self.last_goty_year = data.get("last_goty_year", 0)
        self.bought_platforms = data.get("bought_platforms", ["PC (MS-DOS)"])
        self.active_platforms = data.get("active_platforms", [p['name'] for p in get_available_platforms(self.week)])
        
        # Finanzen laden
        self.accounting = data.get("accounting", {"income": 0, "expenses": 0, "loan_paid": 0})
        loan_data = data.get("bank_loan")
        if loan_data:
            from models import BankLoan
            self.bank_loan = BankLoan(
                loan_data["amount_borrowed"], 0, loan_data["weeks_remaining"], 
                amount_remaining=loan_data["amount_remaining"], 
                weeks_remaining=loan_data["weeks_remaining"]
            )
            self.bank_loan.weekly_payment = loan_data["weekly_payment"]
        else:
            self.bank_loan = None
            
        self.custom_consoles = []
        if "custom_consoles" in data:
            from models import CustomConsole
            for c_data in data["custom_consoles"]:
                cc = CustomConsole(c_data["name"], c_data["tech_level"], c_data["dev_cost"], c_data["release_week"])
                cc.market_share = c_data.get("market_share", 0.05)
                self.custom_consoles.append(cc)

        # Büro laden & Migrieren
        self.office_items = data.get("office_items", [])
        self.office_grid = [[None for _ in range(10)] for _ in range(10)]
        for item in self.office_items:
            # Migration: Falls item nur ein String war (altes Format)
            if isinstance(item, str):
                # Wir können hier nur raten oder ignorieren, da Position fehlt.
                # Besser: Wir ignorieren veraltete Strings in office_items.
                continue
            
            # Migration: Falls item ein Dict ist, aber office_grid noch Strings hielt
            # In unserem neuen System hält office_grid Referenzen auf das Dict.
            y, x = item.get("y", 0), item.get("x", 0)
            if 0 <= y < 10 and 0 <= x < 10:
                self.office_grid[y][x] = item

        self.reset_draft()
        return True


    def produce_physical_copies(self, game_idx, amount, cost_per_unit=1.5):
        """Gibt physikalische Einheiten in Auftrag."""
        if not getattr(self, "has_presswerk", False):
            return False, "no_presswerk"

        if 0 <= game_idx < len(self.game_history):
            g = self.game_history[game_idx]
            if not getattr(g, "is_active", False):
                return False, "game_inactive"

            total_cost = int(amount * cost_per_unit)
            if self.money < total_cost:
                return False, "not_enough_money"

            available_storage = getattr(self, "storage_capacity", 0) - getattr(self, "used_storage", 0)
            if amount > available_storage:
                return False, "storage_full"

            self.money -= total_cost
            self.used_storage += amount
            g.physical_copies = getattr(g, "physical_copies", 0) + amount
            return True, total_cost
        
        return False, "invalid_game"

    # ==========================================================
    # PHASE D: MMO & SERVER INFRASTRUKTUR
    # ==========================================================

    def build_server_room(self):
        """Baut den ersten Serverraum."""
        cost = 1000000
        if self.money >= cost and getattr(self, "office_level", 0) >= 3 and not getattr(self, "has_server_room", False):
            self.money -= cost
            self.has_server_room = True
            self.server_capacity = 50000
            return True
        return False
        
    def expand_server_capacity(self):
        """Erweitert Serverkapazität um 50.000 Spieler."""
        cost = 250000
        if self.money >= cost and getattr(self, "has_server_room", False):
            self.money -= cost
            self.server_capacity += 50000
            return True
        return False
        
    def apply_mmo_update(self, active_mmo_idx, cost=500000, player_boost=0.2):
        """Veröffentlicht ein Content-Update für ein aktives MMO."""
        if 0 <= active_mmo_idx < len(getattr(self, "active_mmos", [])):
            if self.money >= cost:
                self.money -= cost
                mmo = self.active_mmos[active_mmo_idx]
                mmo.players = int(mmo.players * (1 + player_boost))
                mmo.game.hype = min(100, getattr(mmo.game, "hype", 0) + 20)
                return True, "success"
            return False, "not_enough_money"
        return False, "not_found"

    # ==========================================================
    # PHASE E: PUBLISHING & OFFERS
    # ==========================================================

    def _generate_publishing_offer(self):
        """Generiert ein zufälliges Publishing-Angebot für den Spieler."""
        from models import PublishingOffer, Email
        from game_data import START_TOPICS, START_GENRES
        
        studios = ["Pixel Wizards", "Neon Interactive", "Bitforge Studios", "Quantum Games", "Hyperion Soft"]
        words = ["Quest", "Saga", "Chronicles", "World", "Strike", "Legends", "Simulator", "Manager"]
        
        studio = random.choice(studios)
        game_topic = random.choice(list(START_TOPICS.keys()))
        game_genre = random.choice(list(START_GENRES.keys()))
        game_name = f"{game_topic} {random.choice(words)}"
        
        quality = random.randint(30, 95)
        # Marketingkosten skalieren mit Qualität
        marketing_cost = int((quality ** 2) * 50) 
        
        # Player Share (wie viel % der Einnahmen wir bekommen)
        player_share = random.uniform(0.3, 0.7)
        
        offer = PublishingOffer(studio, game_name, game_genre, quality, marketing_cost, player_share)
        
        if not hasattr(self, "publishing_offers"):
            self.publishing_offers = []
        self.publishing_offers.append(offer)
        
        # Email Notification
        msg = f"{studio} sucht einen Publisher für ihr neues Spiel '{game_name}'.\n" \
              f"Sie schätzen die Qualität auf {quality}% und benötigen ein Marketing-Budget von {marketing_cost:,} Euro.\n" \
              f"Als Publisher erhältst du {int(player_share*100)}% der Umsätze.\n" \
              f"Schau in dein Publishing-Menü, um das Angebot zu prüfen!"
        self.emails.append(Email("Indie Dev", "Publishing Angebot", msg, self.week, is_bug=False))

    def accept_publishing_offer(self, idx):
        """Akzeptiert ein Angebot und startet den Verkauf."""
        if not hasattr(self, "publishing_offers") or idx < 0 or idx >= len(self.publishing_offers):
            return False, "invalid_offer"
            
        offer = self.publishing_offers[idx]
        if self.money < offer.marketing_cost:
            return False, "not_enough_money"
            
        self.money -= offer.marketing_cost
        if hasattr(self, "accounting"):
             self.accounting["expenses"] += offer.marketing_cost
             
        from models import PublishedThirdPartyGame
        game = PublishedThirdPartyGame(offer)
        
        if not hasattr(self, "published_third_party_games"):
            self.published_third_party_games = []
        self.published_third_party_games.append(game)
        
        self.publishing_offers.pop(idx)
        return True, "success"

    def reject_publishing_offer(self, idx):
        """Lehnt ein Angebot ab und löscht es."""
        if hasattr(self, "publishing_offers") and 0 <= idx < len(self.publishing_offers):
            self.publishing_offers.pop(idx)
            return True
        return False

    # ==========================================================
    # PHASE C: PRODUKTION & LAGER
    # ==========================================================

    def build_presswerk(self):
        """Baut ein eigenes Presswerk. Voraussetzung: Studio-Level 2 und 500k Euro."""
        cost = 500000
        if self.office_level < 2:
            return False, "office_too_small"
        if self.has_presswerk:
            return False, "already_built"
        if self.money < cost:
            return False, "no_money"
            
        self.money -= cost
        self.has_presswerk = True
        self.storage_capacity = 50000 # Startkapazität
        if hasattr(self, "accounting"):
            self.accounting["expenses"] += cost
        return True, "success"

    def expand_storage(self):
        """Erweitert das Lager um 100.000 Einheiten für 100.000 Euro."""
        cost = 100000
        if not self.has_presswerk:
            return False, "no_presswerk"
        if self.money < cost:
            return False, "no_money"
            
        self.money -= cost
        self.storage_capacity += 100000
        if hasattr(self, "accounting"):
            self.accounting["expenses"] += cost
        return True, "success"

    def produce_copies(self, game_index, amount):
        """Produziert physische Kopien eines Spiels."""
        if not self.has_presswerk:
            return False, "no_presswerk"
        if game_index < 0 or game_index >= len(self.game_history):
            return False, "invalid_game"
            
        game = self.game_history[game_index]
        if not game.is_active:
            return False, "game_inactive"
            
        # Kosten pro Kopie: 1.50 Euro
        unit_cost = 1.5
        total_cost = int(amount * unit_cost)
        
        if self.money < total_cost:
            return False, "no_money"
        if self.used_storage + amount > self.storage_capacity:
            return False, "no_storage"
            
        self.money -= total_cost
        game.physical_copies = getattr(game, "physical_copies", 0) + amount
        # Wir setzen den Retail-Preis auf 45 Euro, falls nicht vorhanden
        if not hasattr(game, "physical_price"):
            game.physical_price = 45
            
        self.used_storage += amount
        if hasattr(self, "accounting"):
            self.accounting["expenses"] += total_cost
            
        return True, "success"

    def perform_teambuilding(self, action_type="Pizza"):
        """Führt eine Team-Building Maßnahme durch."""
        costs = {"Pizza": 500, "Ausflug": 5000, "Party": 2000}
        morale_boost = {"Pizza": 5, "Ausflug": 25, "Party": 15}
        
        cost = costs.get(action_type, 1000)
        if self.money >= cost:
            self.money -= cost
            boost = morale_boost.get(action_type, 10)
            for emp in self.employees:
                emp.morale = min(100, emp.morale + boost)
            return True
        return False

    def has_office_bonus(self, bonus_name):
        """Prüft ob ein bestimmter Bonus (z.B. 'research', 'mmo') durch Einrichtung aktiv ist."""
        for item in self.office_items:
            # Suche in game_data.BUILD_OBJECTS nach dem Bonus
            from game_data import BUILD_OBJECTS
            obj_def = BUILD_OBJECTS.get(item["type"], {})
            if obj_def.get("bonus") == bonus_name:
                return True
        return False

    def place_office_item(self, item_type, x, y):
        """Platziert ein Objekt im Büro-Grid (Ebenen-basiert)."""
        from game_data import BUILD_OBJECTS
        obj_def = BUILD_OBJECTS.get(item_type)
        if not obj_def:
            return False, "invalid_item"
            
        cost = obj_def.get("cost", 0)
        if self.money < cost:
            return False, "no_money"

        # Check adjacence requirement (e.g. door needs wall)
        if obj_def.get("requires_adjacent_wall"):
            adjacent_wall = False
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    neighbor = self.office_grid[ny][nx]
                    if neighbor and neighbor["type"] == "wall":
                        adjacent_wall = True
                        break
            if not adjacent_wall:
                return False, "needs_wall"
        
        # Grid collision check
        if self.office_grid[y][x] is not None:
            return False, "collision"
            
        # Pay
        self.money -= cost
        if hasattr(self, "accounting"):
            self.accounting["expenses"] += cost
            
        # Place
        item = {
            "type": item_type,
            "x": x,
            "y": y,
            "width": 1,
            "height": 1,
            "employees": obj_def.get("employees", 0)
        }
        self.office_items.append(item)
        self.office_grid[y][x] = item
                
        return True, "success"

    def remove_office_item(self, x, y):
        """Entfernt ein Objekt und erstattet 50% der Kosten."""
        item = getattr(self, "office_grid", [[None]*10]*10)[y][x]
        if not item: return False
        
        # Mitarbeiter Limit check if it's a desk
        if item.get("employees", 0) > 0:
            current = len(self.employees)
            future_max = self.get_max_employees() - item.get("employees", 0)
            if current > future_max:
                return False 
            
        # Remove
        self.office_items.remove(item)
        self.office_grid[y][x] = None
        
        # Refund 50%
        from game_data import BUILD_OBJECTS
        obj_def = BUILD_OBJECTS.get(item["type"], {})
        self.money += obj_def.get("cost", 0) * 0.5
        
        return True

    def get_office_item(self, x, y):
        return self.office_grid[y][x]

    def _check_achievements(self):
        """Prüft ob neue Meilensteine erreicht wurden."""
        from game_data import ACHIEVEMENTS
        from models import Email
        
        if not hasattr(self, "unlocked_achievements"):
            self.unlocked_achievements = []
        if not hasattr(self, "my_goty_wins"):
            self.my_goty_wins = 0
            
        for ach in ACHIEVEMENTS:
            if ach["id"] in self.unlocked_achievements:
                continue
                
            unlocked = False
            
            if ach["type"] == "money":
                if self.money >= ach["threshold"]:
                    unlocked = True
            elif ach["type"] == "fans":
                if self.fans >= ach["threshold"]:
                    unlocked = True
            elif ach["type"] == "game_size":
                if any(g.size == ach["threshold"] for g in self.game_history):
                    unlocked = True
            elif ach["type"] == "score":
                if any(getattr(g.review, 'average', 0) >= ach["threshold"] for g in self.game_history if hasattr(g, 'review')):
                    unlocked = True
            elif ach["type"] == "goty":
                if self.my_goty_wins >= ach["threshold"]:
                    unlocked = True
                    
            if unlocked:
                self.unlocked_achievements.append(ach["id"])
                
                # Bonus anwenden
                bonus_str = ""
                if ach["bonus_type"] == "fans":
                    self.fans += ach["bonus_value"]
                    bonus_str = f"+{ach['bonus_value']:,} Fans"
                elif ach["bonus_type"] == "money":
                    self.money += ach["bonus_value"]
                    if hasattr(self, "accounting"):
                        self.accounting["income"] += ach["bonus_value"]
                    bonus_str = f"+{ach['bonus_value']:,} €"
                elif ach["bonus_type"] == "hype":
                    self.hype = min(250, self.hype + ach["bonus_value"])
                    bonus_str = f"+{ach['bonus_value']:,} Hype"
                    
                # E-Mail generieren
                title = self.get_text(f"ach_{ach['id']}_name")
                desc = self.get_text(f"ach_{ach['id']}_desc")
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_system'),
                    subject=self.get_text('subject_achievement', title=title),
                    body=self.get_text('body_achievement', desc=desc, bonus=bonus_str),
                    date_week=self.week
                ))

    def get_current_charts(self, top_n=10):
        """Gibt die aktuellen Verkaufscharts zurueck (Spieler + Rivalen)."""
        entries = []
        for g in self.game_history:
            entries.append({
                'name': g.name,
                'studio': self.company_name,
                'sales': getattr(g, 'sales', 0),
                'is_active': getattr(g, 'is_active', False)
            })
        for rival in self.rivals:
            for rg in rival.games:
                entries.append({
                    'name': rg.name,
                    'studio': rival.name,
                    'sales': int(rg.score * 10000),
                    'is_active': (self.week - rg.week_developed) < 20
                })
        entries.sort(key=lambda e: e['sales'], reverse=True)
        return entries[:top_n]

