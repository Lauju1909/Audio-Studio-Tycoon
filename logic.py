"""
Spielzustand für Audio Studio Tycoon - Audio Edition.

Verwaltet Firmendaten, Geld, Fans, Mitarbeiter, Engines,
Spielhistorie, Ereignisse und die Bewertungslogik.
"""

import random

import json
import os
from models import (
    GameProject, ReviewScore, Employee, Engine, EngineFeature, 
    RivalStudio, RivalGame, Email, AddonProject, BundleProject, 
    ActiveMMO, BankLoan, CustomConsole, PublishingOffer, 
    PublishedThirdPartyGame, BankStatement,
    SoundConEvent, SoundtrackLabel, RadioContract, ManufacturingJob
)
from translations import TRANSLATIONS, get_system_language
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
        self.developer_mode = False # Versteckter Entwickler-Modus
        self.pending_update = None

        # Trends
        self.current_trend = {}  # {'topic': '...', 'genre': '...', 'week_started': X}
        self.last_trend_week = 0

        # Mitarbeiter
        self.employees = []
        self._init_ceo()

        # Engines
        self.engines = []
        self.unlocked_features = []  # Liste von EngineFeature (freigeschaltet)
        self.current_engine_draft = None
        self._init_starter_engine()

        # Büro
        self.office_level = 0  # Index in OFFICE_LEVELS
        self.office_perks = []
        self.stress_level = 0.0
        self.strike_weeks_left = 0

        # Ereignisse
        self.last_event_week = 0
        self.active_events = []

        # Forschungs-System
        self.is_researching = False
        self.research_progress = 0
        self.research_total_weeks = 0
        self.current_research_draft = None
        
        self.unlocked_topics = list(START_TOPICS)
        self.unlocked_genres = list(START_GENRES)
        self.unlocked_audiences = list(START_AUDIENCES)
        self.unlocked_technologies = []

        # Aktuelles Projekt
        self.current_draft = {
            "name": "",
            "topic": "Fantasy",
            "genre": "Action",
            "platform": "PC",
            "audience": "Jeder",
            "engine": None,
            "sliders": {},
            "size": "Mittel",
            "marketing": "none",
        }
        
        # Posteingang
        self.emails = []
        # NEU Phase II: Sabotage-Cooldown
        self.last_sabotage_week = -100
        # NEU: Monetarisierungs-Cooldown
        self.last_ad_week = -10
        self.monetization_back_target = "bank_menu" # Default target for back button

        # Aktive MMOs
        self.active_mmos = []

        # Bankwesen & Finanzen
        self.bank_statements = []
        self.accrued_income = {}
        self.accounting = {"income": 0, "expenses": 0, "loan_paid": 0}
        self.accrued_expenses = {}

        self.subscription_active = False
        self.subscription_price = 9.99
        self.subscription_subscribers = 0
        self.subscription_games = [] # Liste von GameProject Objekten
        self.subscription_hype = 0.0
        self.subscription_multi = 1.0

        # NEU: Finanzhistorie
        self.financial_history = []    # Liste von Dicts {week, year, profit}
        self.accrued_salaries = 0
        self.financial_history = []
        self.office_grid = [[None for _ in range(10)] for _ in range(10)]
        self.office_objects = []

        # Einstellungen
        self.settings = {
            "language": get_system_language(),
            "music_enabled": True,
            "music_volume": 50,
            "speech_volume": 100,
            "sfx_volume": 100,
            "tts_engine": "auto", # mgl: auto, nvda, sapi
            "auto_update": True,
            "update_channel": "stable"
        }

        # Echtzeit-Zeitsteuerung
        self.time_speed = 1.0  # 0=Pause, 1=Normal, 2=Schnell, 4=Sehr Schnell
        self.pause_for_menu = False # Flag für Menüs (z.B. Texteingabe)
        self.week_progress = 0.0
        self.active_projects = [] # Liste von Dicts: {project, progress, total_weeks, bugs, crunch, ready_to_finish, event_count, aaa_event_done, co_dev}
        self.hype = 0.0
        self.active_expo_hype = 0
        
        # Initialisierung wichtiger Subsysteme
        self.bank_loan = None
        self.financial_history = []
        self.current_week_balance = {
            "income": {"sales": 0, "mmo": 0, "merch": 0, "publishing": 0, "shares": 0, "other": 0},
            "expenses": {"salaries": 0, "rent": 0, "marketing": 0, "research": 0, "production": 0, "training": 0, "loan_repayment": 0, "shares": 0, "taxes": 0, "subscription": 0, "server_costs": 0, "other": 0}
        }
        self.accounting = {"income": 0, "expenses": 0, "loan_paid": 0}
        self.rivals = [] # Wird später via _init_rivals gefüllt
        self._pending_rival_idx = None
        self.bought_platforms = ["PC (MS-DOS)"]
        self.active_platforms = []
        self.unlocked_platforms = [] # Manuell freigeschaltete Plattformen (via Events)
        self.last_goty_year = 0
        self.goty_history = {}
        
        # NEU: Phase 7 - Eigene Konsole
        self.custom_consoles = []
        self.is_developing_console = False
        self.console_progress = 0
        self.console_total_weeks = WEEKS_PER_YEAR
        self.current_console_draft = None

        # NEU: Phase A - Schwierigkeitsgrad
        self.difficulty = 1  # Index in DIFFICULTY_LEVELS (0=Einfach, 1=Normal, 2=Schwer, 3=Legendär)

        # Historische Effekte / Statuswerte
        self.research_points = 0  # rp
        self.prestige = 0
        self.tax_rate = 0.15 # Standard 15%
        self.sales_multiplier = 1.0
        self.profit_multiplier = 1.0
        self.logic_multiplier = 1.0
        self.hype_multiplier = 1.0
        self.dev_speed_multiplier = 1.0
        self.interest_rate = 0.05 # Basis-Zins 5%
        self.marketing_efficiency = 1.0
        self.streamer_hype_multi = 1.0
        self.quality_standard_multi = 1.0
        self.subscription_multi = 1.0

        # NEU: Phase A - Verkaufscharts
        self.chart_history = []  # [{'week': X, 'entries': [{'name':..., 'studio':..., 'sales':...}]}]
        self.my_goty_wins = 0

        # ACHIEVEMENTS
        self.unlocked_achievements = []


        # NEU: Phase I - Co-Entwicklung
        self.co_dev_partner = None # Name des Partners, wenn aktiv

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
        
        # NEU: Phase D2 - Server Infrastructure & Office Departments
        self.support_level = 0
        self.qa_level = 0
        
        # NEU: Phase E - Publisher Rolle
        self.publishing_offers = []
        self.published_third_party_games = []
        self.manufacturing_jobs = [] # NEU: Laufende Produktionsaufträge

        # Keybindings initialisieren (Standardwerte)
        import pygame
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN
        self.key_confirm = pygame.K_RETURN
        self.key_cancel = pygame.K_ESCAPE

        # Historische Themen für das Startjahr freischalten
        self._unlock_historical_topics(silent=True)
        self.key_back = pygame.K_BACKSPACE
        self.key_home = pygame.K_HOME
        self.key_end = pygame.K_END

        # NEU: Phase F - Merch und Turniere
        self.active_merch = []
        self.active_tournaments = []
        self.active_sponsorships = []

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
        
        # NEU: Multiplayer
        self.multiplayer = None

        # NEU: Tutorial-System
        self.completed_tutorials = [] # Liste der abgeschlossenen Tutorial-IDs
        self.active_tutorial = None # Aktuelles Tutorial-Objekt
        self.tutorial_step_index = 0

        # NEU: SoundCon – Spielemesse
        self.soundcon_history = []         # Liste aller SoundConEvent-Objekte
        self.active_soundcon = None        # Aktuelles SoundConEvent (während der Messe)
        self.soundcon_last_year = 0        # Letztes Jahr mit Messe-Teilnahme
        self.pending_soundcon_result = None # Messe-Ergebnisse warten auf Anzeige

        # NEU: Soundtrack-Label
        self.soundtrack_label = None       # SoundtrackLabel oder None (wenn nicht gegründet)

        # ============================================================
        # NEU: v3.11.0-beta.1 Expansion Variables (Community & Hardware)
        # ============================================================
        self.fan_mail_inbox = []
        self.sound_card_projects = []
        self.active_jingles = []
        self.unlocked_hardware_tech = []
        self.active_personality_event = None
        self.active_personality_employee = None
        self.temp_dev_speed_penalty = 1.0
        self.temp_dev_speed_weeks = 0
        self.temp_quality_boost = 0.0
        self.temp_quality_weeks = 0
        self.accessibility_reputation = 0
        self.accessibility_lab_history = []
        self.last_accessibility_grant_year = 0

    def add_welcome_emails(self):
        """Erstellt die Willkommens-E-Mails in der aktuell gesetzten Sprache."""
        # Willkommensnachricht: Die 1930er Ära
        self.emails.append(Email(
            sender=self.get_text('sender_historian'),
            subject=self.get_text('subject_pioneer_times'),
            body=self.get_text('body_pioneer_times'),
            date_week=1
        ))
        
        # Initialisierung von Inhalten, die Sprach-Keys benötigen
        self.rivals = self._init_rivals()
        from game_data import get_available_platforms
        self.active_platforms = [p['name'] for p in get_available_platforms(1)]

    def get_market_platforms(self):
        from game_data import get_available_platforms, PLATFORMS
        base = get_available_platforms(self.week)
        out = list(base)
        
        # Manuell freigeschaltete Plattformen hinzufügen (falls noch nicht drin)
        base_names = [p['name'] for p in base]
        for p_name in getattr(self, "unlocked_platforms", []):
            if p_name not in base_names:
                # Suche die Plattform-Daten in der Master-Liste
                p_data = next((p for p in PLATFORMS if p['name'] == p_name), None)
                if p_data:
                    out.append(p_data)

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
                
        # Bestehende Settings aktualisieren statt komplett zu ersetzen (erhält Defaults)
        self.settings.update(sets)
        self.completed_tutorials = self.settings.get("completed_tutorials", [])
        
        # Tasten auslesen (falls vorhanden), ansonsten Standard lassen
        import pygame
        self.key_up = self.settings.get("key_up", pygame.K_UP)
        self.key_down = self.settings.get("key_down", pygame.K_DOWN)
        self.key_confirm = self.settings.get("key_confirm", pygame.K_RETURN)
        self.key_back = self.settings.get("key_back", pygame.K_BACKSPACE)
        self.key_home = self.settings.get("key_home", pygame.K_HOME)
        self.key_end = self.settings.get("key_end", pygame.K_END)
        
        return self.settings

    def save_global_settings(self):
        """Speichert globale Einstellungen ab."""
        self.settings["key_up"] = self.key_up
        self.settings["key_down"] = self.key_down
        self.settings["key_confirm"] = self.key_confirm
        self.settings["key_back"] = self.key_back
        self.settings["key_home"] = self.key_home
        self.settings["key_end"] = self.key_end
        self.settings["completed_tutorials"] = self.completed_tutorials
        
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def _init_rivals(self):
        """Erstellt 3 Konkurrenz-Studios."""
        return [
            RivalStudio("MicroHard", target_market_share=30, next_release_week=random.randint(10, 30), ai_personality="Trendchaser"),
            RivalStudio("Electric Farts", target_market_share=25, next_release_week=random.randint(20, 45), ai_personality="Aggressive"),
            RivalStudio("Nintengo", target_market_share=20, next_release_week=random.randint(35, 60), ai_personality="Perfectionist")
        ]

    def _init_ceo(self):
        """Erstellt den Chef als ersten permanenten Mitarbeiter."""
        found = False
        for e in self.employees:
            if getattr(e, 'is_ceo', False) or e.name == "Chef":
                e.is_ceo = True
                e.salary = 0 # Sicherstellen
                found = True
                break
        if found:
            return
            
        # Der Chef hat feste Daten
        ceo = Employee(name="Chef", role_data={"role": "Chef", "primary": "Gameplay", "secondary": "Design"}, skill_level=3)
        ceo.is_ceo = True
        ceo.salary = 0
        self.employees.insert(0, ceo)

    def _init_starter_engine(self):
        """Erstellt die Starter-Engine mit Basis-Features."""
        from game_data import ENGINE_FEATURES
        starter_features = []
        for f_data in ENGINE_FEATURES:
            if f_data["cost"] == 0:
                feat = EngineFeature(f_data["category"], f_data["name"], f_data["tech_bonus"])
                starter_features.append(feat)
                self.unlocked_features.append(feat)

        starter = Engine("Basis-Engine", starter_features)
        self.engines.append(starter)

    def _unlock_historical_topics(self, silent=False):
        """Prüft das aktuelle Jahr und schaltet neue historische Themen und Ereignisse frei."""
        from game_data import get_newly_unlocked_topics, YEAR_EVENTS, START_YEAR
        
        calendar_year = START_YEAR + (self.week - 1) // WEEKS_PER_YEAR
        new_topics = get_newly_unlocked_topics(calendar_year)
        
        # 1. Themen freischalten
        for topic in new_topics:
            name = topic["name"]
            if name not in self.unlocked_topics:
                self.unlocked_topics.append(name)
                if not silent:
                    # E-Mail Benachrichtigung
                    self.emails.insert(0, Email(
                        sender=self.get_text("sender_historian"),
                        subject=self.get_text("subject_new_topic"),
                        body=self.get_text("body_new_topic", topic=self.get_text(name)),
                        date_week=self.week
                    ))

        # 2. Historisches Ereignis verarbeiten
        if calendar_year in YEAR_EVENTS:
            event = YEAR_EVENTS[calendar_year]
            effect_type = event.get("effect")
            val = event.get("value")
            
            if not silent:
                # E-Mail senden
                event_text = self.get_text(event["text"])
                impact_desc = f"{effect_type} -> {val}"
                self.emails.insert(0, Email(
                    sender=self.get_text("sender_world_events"),
                    subject=self.get_text("subject_historical_event", year=calendar_year),
                    body=f"{event_text}\n\n{self.get_text('event_impact')}: {impact_desc}",
                    date_week=self.week
                ))

            # Effekt anwenden
            if effect_type == "money":
                if val > 0: self.track_income("other", val)
                else: self.track_expense("other", abs(val))
            elif effect_type == "money_multi":
                diff = self.money * (val - 1)
                if diff > 0:
                    self.track_income("other", diff)
                elif diff < 0:
                    self.track_expense("other", abs(diff))
            elif effect_type == "fans":
                self.fans += val
            elif effect_type == "hype":
                self.hype = min(250, self.hype + val)
            elif effect_type == "hype_multi":
                self.hype_multiplier *= val
            elif effect_type == "rp":
                self.research_points += val
            elif effect_type == "prestige":
                self.prestige += val
            elif effect_type == "tax_increase":
                self.tax_rate += val
            elif effect_type == "sales_multi":
                self.sales_multiplier *= val
            elif effect_type == "logic_boost":
                self.logic_multiplier *= val
            elif effect_type == "dev_speed":
                self.dev_speed_multiplier *= val
            elif effect_type == "interest_increase":
                self.interest_rate += val
            elif effect_type == "marketing_rev":
                self.marketing_efficiency *= val
            elif effect_type == "streamer_impact":
                self.streamer_hype_multi *= val
            elif effect_type == "subscription_boom" or effect_type == "subscription_standard":
                self.subscription_multi *= val
            elif effect_type == "quality_standard" or effect_type == "story_standard" or effect_type == "graphics_standard":
                self.quality_standard_multi *= val
            elif effect_type == "trend_topic":
                self.current_trend = {
                    'topic': val,
                    'genre': self.current_trend.get('genre', 'Action'),
                    'week_started': self.week
                }
            elif effect_type == "trend_genre":
                self.current_trend = {
                    'topic': self.current_trend.get('topic', 'Fantasy'),
                    'genre': val,
                    'week_started': self.week
                }
            elif effect_type == "trend_difficulty":
                # Schwierigkeit als Trend ist ein neues Konzept, wir merken es uns
                self.difficulty_trend = val 
            elif effect_type == "unlock_tech":
                if val not in self.unlocked_technologies:
                    self.unlocked_technologies.append(val)
            elif effect_type == "unlock_platform":
                from game_data import PLATFORMS
                p_name_part = str(event.get("value", ""))
                # Finde die Plattform, die den Namen enthält
                for p in PLATFORMS:
                    if p_name_part.lower() in p["name"].lower():
                        if p["name"] not in self.unlocked_platforms:
                            self.unlocked_platforms.append(p["name"])
                            # Benachrichtigung via Email
                            self.emails.insert(0, Email(
                                sender=self.get_text('sender_historical'),
                                subject=self.get_text('subject_platform_unlocked', name=p["name"]),
                                body=self.get_text('body_platform_unlocked', name=p["name"]),
                                date_week=self.week
                            ))
                            if hasattr(self, 'audio'):
                                self.audio.play_sound('confirm')
                                self.audio.speak(self.get_text('announce_platform_unlocked', name=p["name"]), interrupt=False)
                        break
            elif effect_type == "game_end":
                self.game_over = True
                self.game_over_reason = "historical_end"

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

    def estimate_dev_time(self):
        """Schätzt die Entwicklungszeit für den aktuellen Draft (in Wochen, ca.-Angabe)."""
        size = self.current_draft.get("size", "Mittel")
        base_weeks = {"Klein": 5, "Mittel": 15, "Groß": 30, "AAA": 60}.get(size, 15)
        # Teamgröße und Speed-Modifier einrechnen
        speed = self.get_team_speed_modifier()
        if getattr(self, "co_dev_partner", None):
            speed *= 1.8
        # Geschätzte Kalenderwochen (ca.)
        estimated = max(1, int(base_weeks / max(0.5, speed)))
        return estimated

    def start_development(self):
        """Startet die Entwicklung eines neuen Spiels."""
        try:
            name = self.current_draft.get("name", "Untitled") or "Untitled"
            topic = self.current_draft.get("topic", "Fantasy")
            genre = self.current_draft.get("genre", "Action")
            platform = self.current_draft.get("platform", {"name": "PC"})
            audience = self.current_draft.get("audience", "Jeder")
            engine = self.current_draft.get("engine", None)
            size = self.current_draft.get("size", "Mittel")
            marketing = self.current_draft.get("marketing", "Kein Marketing")
            sliders = self.current_draft.get("sliders", {})
            
            plat_name = platform['name'] if isinstance(platform, dict) else platform
            
            project = GameProject(
                name=name, topic=topic, genre=genre, sliders=sliders,
                platform=plat_name, audience=audience, engine=engine,
                size=size, marketing=marketing
            )
            
            # Team-Zuweisung
            if "assigned_employee_ids" in self.current_draft:
                project.assigned_employee_ids = self.current_draft["assigned_employee_ids"]
            else:
                project.assigned_employee_ids = [i for i, e in enumerate(self.employees) if not getattr(e, 'is_sick', False) and not getattr(e, 'is_training', False)]
            
            project.sequel_number = self.current_draft.get("sequel_number", 0)
            project.sub_genre = self.current_draft.get("sub_genre", None)
            project.is_remaster = self.current_draft.get("is_remaster", False)
            
            base_weeks = {"Klein": 5, "Mittel": 15, "Groß": 30, "AAA": 60}.get(size, 15)
            
            new_active = {
                "project": project,
                "progress": 0.0,
                "total_weeks": base_weeks,
                "bugs": 0,
                "crunch": False,
                "ready_to_finish": False,
                "event_count": 0,
                "aaa_event_done": False,
                "co_dev": getattr(self, "co_dev_partner", None),
                "publisher": self.current_draft.get("publisher")
            }
            self.active_projects.append(new_active)
            self.reset_draft()
            self.co_dev_partner = None # Reset für nächstes Spiel
        except Exception as e:
            with open("crash_log.txt", "a", encoding="utf-8") as f:
                import traceback
                f.write(f"\nSTART_DEV CRASH: {str(e)}\n")
                f.write(traceback.format_exc())
            raise e

    # ------------------------------------------------------------------ #
    #  SoundCon – Spielemesse                                              #
    # ------------------------------------------------------------------ #

    def can_attend_soundcon(self) -> tuple:
        """Prüft ob der Spieler an der aktuellen SoundCon teilnehmen kann.

        Returns:
            (bool, str): True/False und Grund bei Ablehnung.
        """
        current_year = self.get_calendar_year()
        if self.soundcon_last_year >= current_year:
            return False, "soundcon_already_attended"
        if self.active_soundcon is not None:
            return False, "soundcon_already_booked"
        return True, ""

    def book_soundcon_booth(self, booth_tier: str) -> bool:
        """Bucht einen Messestand für die SoundCon.

        Args:
            booth_tier: Standgröße ('klein', 'mittel', 'groß', 'keynote').

        Returns:
            True bei Erfolg, False bei zu wenig Geld.
        """
        can, _ = self.can_attend_soundcon()
        if not can:
            return False

        tier_data = SoundConEvent.BOOTH_TIERS.get(booth_tier)
        if not tier_data:
            return False

        cost = tier_data["cost"]
        if self.money < cost:
            return False

        self.track_expense("other", cost)
        event = SoundConEvent(year=self.get_calendar_year(), booth_tier=booth_tier)
        self.active_soundcon = event
        return True

    def conduct_soundcon_qa(self) -> dict:
        """Führt eine Q&A-Runde auf der SoundCon durch (max. 3 Runden).

        Returns:
            Dict mit 'success', 'qa_round', 'message'.
        """
        if not self.active_soundcon:
            return {"success": False, "message": "soundcon_not_booked"}
        if self.active_soundcon.qa_rounds >= 3:
            return {"success": False, "message": "soundcon_qa_max"}

        self.active_soundcon.qa_rounds += 1
        qa_num = self.active_soundcon.qa_rounds
        if hasattr(self, 'audio'):
            self.audio.play_sound('confirm')
            self.audio.speak(
                self.get_text('soundcon_qa_done', round=qa_num), interrupt=False
            )
        return {"success": True, "qa_round": qa_num, "message": "soundcon_qa_success"}

    def finish_soundcon(self) -> dict:
        """Schließt die SoundCon ab und berechnet die Ergebnisse.

        Returns:
            Ergebnis-Dict mit hype, fans, prestige, qa, tier.
        """
        if not self.active_soundcon:
            return {}

        result = self.active_soundcon.calculate_results(self)

        # Effekte anwenden
        self.hype   = min(250, self.hype + result["hype"])
        self.fans  += result["fans"]
        self.prestige += result["prestige"]

        # Archivieren
        self.soundcon_history.append(self.active_soundcon)
        self.soundcon_last_year = self.active_soundcon.year
        self.pending_soundcon_result = result
        self.active_soundcon = None

        # E-Mail mit Zusammenfassung
        self.emails.insert(0, Email(
            sender=self.get_text('soundcon_sender'),
            subject=self.get_text('soundcon_result_subject', year=self.get_calendar_year()),
            body=self.get_text(
                'soundcon_result_body',
                hype=result["hype"], fans=result["fans"],
                prestige=result["prestige"], qa=result["qa"],
                tier=self.get_text(f'soundcon_tier_{result["tier"]}')
            ),
            date_week=self.week
        ))
        if hasattr(self, 'audio'):
            self.audio.play_sound('success')
            self.audio.speak(
                self.get_text('soundcon_result_announce', fans=result["fans"]), interrupt=False
            )
        return result

    # ------------------------------------------------------------------ #
    #  Soundtrack-Label                                                    #
    # ------------------------------------------------------------------ #

    def found_soundtrack_label(self, label_name: str) -> bool:
        """Gründet ein Soundtrack-Label.

        Kostet 30.000 €. Scheitert wenn Label bereits existiert oder kein Geld.

        Args:
            label_name: Name des neuen Labels.

        Returns:
            True bei Erfolg, False bei Misserfolg.
        """
        FOUNDING_COST = 30_000
        if self.soundtrack_label is not None:
            return False  # Bereits gegründet
        if self.money < FOUNDING_COST:
            return False

        self.track_expense("other", FOUNDING_COST)
        label = SoundtrackLabel(label_name)
        label.founding_week = self.week
        self.soundtrack_label = label

        # Alle bisherigen Spiele retroaktiv hinzufügen
        for g in self.game_history:
            label.add_game(g.name)

        self.emails.insert(0, Email(
            sender=self.get_text('label_sender'),
            subject=self.get_text('label_founded_subject', name=label_name),
            body=self.get_text('label_founded_body', name=label_name, cost=FOUNDING_COST,
                               games=len(label.catalogued_games)),
            date_week=self.week
        ))
        if hasattr(self, 'audio'):
            self.audio.play_sound('success')
            self.audio.speak(self.get_text('label_founded_announce', name=label_name), interrupt=False)
        return True

    def sign_radio_contract(self, station_data: dict) -> bool:
        """Unterzeichnet einen Radiovertrag für das Soundtrack-Label.

        Args:
            station_data: Dict aus SoundtrackLabel.RADIO_STATIONS.

        Returns:
            True bei Erfolg.
        """
        if not self.soundtrack_label:
            return False
        cost = station_data.get("cost", 0)
        if self.money < cost:
            return False

        self.track_expense("other", cost)
        contract = RadioContract(
            station_name=station_data["name"],
            weekly_royalties=station_data["royalties"],
            duration_weeks=station_data["weeks"],
            hype_per_week=station_data["hype"]
        )
        self.soundtrack_label.radio_contracts.append(contract)

        self.emails.insert(0, Email(
            sender=self.get_text('label_sender'),
            subject=self.get_text('label_radio_subject', station=station_data["name"]),
            body=self.get_text('label_radio_body',
                               station=station_data["name"],
                               royalties=station_data["royalties"],
                               weeks=station_data["weeks"]),
            date_week=self.week
        ))
        if hasattr(self, 'audio'):
            self.audio.play_sound('confirm')
            self.audio.speak(
                self.get_text('label_radio_announce', station=station_data["name"]), interrupt=False
            )
        return True


    def can_start_development(self, size):
        """Prüft ob alle Voraussetzungen für den Entwicklungsstart erfüllt sind."""
        # 1. Genug Mitarbeiter?
        if not self.employees:
            return False, "no_employees"
            
        # 2. Genug Geld? (Wird beim Start abgezogen, hier nur Vorab-Check)
        # 3. Genug Arbeitsplätze?
        workplaces = sum(1 for obj in self.office_objects if obj.object_type == "Desk" or obj.object_type == "workplace")
        if workplaces < len(self.employees):
            return False, "not_enough_workplaces"
            
        # 4. Spezielle Anforderungen für AAA (z.B. 1980+)
        if size == "AAA" and self.get_calendar_year() < 1980:
            return False, "aaa_too_early"
            
        return True, ""

    def start_update_project(self, game_name, update_type, name="Update", selected_languages=None):
        """Startet ein Update- oder DLC-Projekt für ein existierendes Spiel."""
        # Suche das Basisspiel
        game = next((g for g in self.game_history if g.name == game_name), None)
        if not game:
            return False
            
        dev_cost = 0
        total_weeks = 0
        
        if update_type == "Patch":
            # Repariert 50% der Bugs
            dev_cost = 5000
            total_weeks = 2
        elif update_type == "Content":
            # Erhöht Hype und Fans
            dev_cost = 20000
            total_weeks = 4
        elif update_type == "DLC":
            # Kostet mehr, bringt aber Einnahmen
            dev_cost = 50000
            total_weeks = 8
        elif update_type == "Language":
            # Fügt neue Sprachen hinzu
            langs = selected_languages or []
            dev_cost = len(langs) * 10000
            # Mindestens 1 Woche, um ZeroDivisionError zu vermeiden
            total_weeks = max(1, len(langs))
            
        update = UpdateProject(
            base_game_name=game_name,
            name=name,
            update_type=update_type,
            dev_cost=dev_cost,
            total_weeks=total_weeks,
            languages=selected_languages
        )
        
        new_active = {
            "update": update,
            "progress": 0.0,
            "total_weeks": total_weeks
        }
        self.active_projects.append(new_active)
        return True

    def start_manufacturing_job(self, game_name, amount, cost_per_unit, weeks):
        """Startet einen Auftrag zur Produktion physischer Kopien."""
        if self.money < amount * cost_per_unit:
            return False
            
        self.track_expense("production", amount * cost_per_unit)
        
        job = ManufacturingJob(game_name, amount, cost_per_unit, weeks)
        self.manufacturing_jobs.append(job)
        return True

    def get_text(self, text_key, **kwargs):
        """Holt einen übersetzten Text basierend auf dem aktuellen Sprach-Setting."""
        from translations import get_text as t_get_text, set_language
        
        # Synchronisiere Sprache in translations.py
        lang = self.settings.get("language", "de")
        set_language(lang)
        
        return t_get_text(text_key, **kwargs)

    def get_calendar_year(self):
        """Gibt das aktuelle Kalenderjahr zurück (Start: START_YEAR)."""
        return START_YEAR + (self.week - 1) // WEEKS_PER_YEAR

    def get_calendar_text(self):
        """Gibt Kalenderjahr, Monat und Woche zurück (dynamisch basierend auf WEEKS_PER_YEAR)."""
        year = self.get_calendar_year()
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        
        # Dynamische Monatsberechnung (12 Monate pro Jahr)
        month_idx = int((week_in_year - 1) * 12 / WEEKS_PER_YEAR)
        
        lang = self.settings.get("language", "de")
        month_key = [
            "month_jan", "month_feb", "month_mar", "month_apr", "month_may", "month_jun",
            "month_jul", "month_aug", "month_sep", "month_oct", "month_nov", "month_dec"
        ][min(month_idx, 11)]
        
        month_name = self.get_text(month_key)
        
        # Wochen innerhalb des Monats (angenähert)
        weeks_per_month = WEEKS_PER_YEAR / 12
        week_in_month = int(((week_in_year - 1) % weeks_per_month) + 1)
        
        return f"{month_name} {year}, {self.get_text('calendar_week')} {week_in_month}"

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

    @property
    def is_developing(self):
        return len(self.active_projects) > 0

    def update_subscription_service(self):
        """Berechnet wöchentliche Abonnentenzahlen, Einnahmen und Hype für den Abo-Dienst."""
        if not getattr(self, 'subscription_active', False):
            return

        # 1. Bibliothek bewerten (Library Quality)
        # Wir berechnen einen Qualitäts-Faktor basierend auf Anzahl und Qualität der Spiele
        if not hasattr(self, 'subscription_games'):
            self.subscription_games = []
            
        num_games = len(self.subscription_games)
        if num_games == 0:
            # Ohne Spiele verliert man schnell Abonnenten
            self.subscription_hype = max(0.0, self.subscription_hype - 2.0)
            avg_score = 0
        else:
            total_score = sum(getattr(g, 'review_score', 50.0) for g in self.subscription_games)
            avg_score = total_score / num_games
            
            # Genre-Vielfalt Bonus
            genres = set(getattr(g, 'genre', 'Unknown') for g in self.subscription_games)
            diversity_bonus = len(genres) * 2.0
            
            # Hype-Zuwachs durch Bibliothek
            # Basis: Mehr Spiele = mehr Hype, gute Spiele = mehr Hype
            library_hype_gain = (num_games * 0.1) + (avg_score / 20.0) + (diversity_bonus / 10.0)
            self.subscription_hype = min(100.0, self.subscription_hype + library_hype_gain)

        # 2. Hype-Zerfall (Hype decay)
        self.subscription_hype = max(0.0, self.subscription_hype - 0.3)

        # 3. Finanzen
        weeks_per_month = WEEKS_PER_YEAR / 12.0
        weekly_income = (self.subscription_subscribers * self.subscription_price) / weeks_per_month
        # Serverkosten steigen mit Abonnentenzahl
        server_costs_weekly = max(500, self.subscription_subscribers * 0.05) / weeks_per_month
        
        self.track_income("subscription", weekly_income)
        self.track_expense("server_costs", server_costs_weekly)

        # 4. Abonnenten-Wachstum
        # Ziel-Abonnenten basierend auf Hype, Preis und Bibliotheksqualität
        # Ein Preis von 10€ ist "normal". Höhere Preise schrecken ab, niedrigere locken an.
        price_factor = 15.0 / max(1.0, self.subscription_price)
        # Qualitätsfaktor (avg_score 70+ ist gut)
        quality_factor = max(0.1, (avg_score - 40) / 40.0) if avg_score > 40 else 0.1
        
        target_subs = (self.subscription_hype * 2000) * price_factor * quality_factor * self.subscription_multi
        
        # Annäherung an Target
        diff = target_subs - self.subscription_subscribers
        growth_rate = 0.02 if diff > 0 else 0.05 # Verluste gehen schneller als Gewinne
        self.subscription_subscribers += diff * growth_rate
        
        if self.subscription_subscribers < 0:
            self.subscription_subscribers = 0

    def _on_new_week(self):
        """Logik die jede Woche passiert (Gehalt, Zufallsereignisse)."""
        # Abo-Dienst aktualisieren
        self.update_subscription_service()
        self._process_engine_licensing()
        self._process_port_projects()
        
        # Feature 1.2: Support Department
        support_level = getattr(self, "support_level", 0)
        if support_level > 0:
            self.track_expense("other", support_level * 500)
            
        # Feature 1.3: QA Lab
        qa_level = getattr(self, "qa_level", 0)
        if qa_level > 0:
            for proj in getattr(self, "active_projects", []):
                current_bugs = proj.get("bugs", 0)
                if current_bugs > 0:
                    removed = min(current_bugs, qa_level * 2)
                    proj["bugs"] = current_bugs - removed

        # Monatsankündigung (dynamisch basierend auf WEEKS_PER_YEAR)
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        prev_week_in_year = (self.week - 2) % WEEKS_PER_YEAR + 1 if self.week > 1 else 0
        
        current_month = int((week_in_year - 1) * 12 / WEEKS_PER_YEAR)
        prev_month = int((prev_week_in_year - 1) * 12 / WEEKS_PER_YEAR) if self.week > 1 else -1
        
        is_new_month = (current_month != prev_month)

        # Passive income from acquired studios
        for rival in self.rivals:
            if getattr(rival, 'is_owned_by_player', False):
                passive_income = random.randint(10000, 50000)
                self.money += passive_income
                self.track_income("other", passive_income)


        # Office Perks Overhead
        if getattr(self, 'office_perks', []):
            perk_cost = len(self.office_perks) * 500
            self.money -= perk_cost
            self.track_expense("other", perk_cost)

        # Stress and Strikes
        is_crunching_any = any(ap.get('crunch') for ap in self.active_projects)
        if is_crunching_any:
            self.stress_level = min(100.0, getattr(self, 'stress_level', 0.0) + 5.0)
        else:
            perk_relief = len(getattr(self, 'office_perks', [])) * 2.0
            self.stress_level = max(0.0, getattr(self, 'stress_level', 0.0) - (2.0 + perk_relief))

        if getattr(self, 'stress_level', 0.0) > 80.0 and getattr(self, 'strike_weeks_left', 0) == 0:

            if random.random() < 0.1: # 10% chance per week
                self.strike_weeks_left = random.randint(1, 4)
                strike_cost = self.strike_weeks_left * 5000
                self.money -= strike_cost
                self.track_expense("other", strike_cost)
                self.stress_level = 0.0
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_union'),
                    subject=self.get_text('subject_strike'),
                    body=self.get_text('body_strike', weeks=self.strike_weeks_left, cost=strike_cost),
                    date_week=self.week
                ))
                if hasattr(self, 'audio'):
                    self.audio.play_sound('error')

        # Headhunting event
        if not getattr(self, "pending_headhunt_event", None) and self.employees:

            for emp in self.employees:
                avg_skill = sum(emp.skills.values()) / len(emp.skills) if emp.skills else 0
                if avg_skill >= 80 and random.random() < 0.005:
                    rival_offer = int(emp.salary * random.uniform(1.2, 2.0))
                    self.pending_headhunt_event = {
                        "employee": emp,
                        "rival_offer": rival_offer
                    }
                    self.time_speed = 0
                    break

        # Strike Countdown
        if getattr(self, 'strike_weeks_left', 0) > 0:
            self.strike_weeks_left -= 1
            if self.strike_weeks_left == 0:
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_union'),
                    subject=self.get_text('subject_strike_ended'),
                    body=self.get_text('body_strike_ended'),
                    date_week=self.week
                ))

        if is_new_month and self.week > 1:
            cal = self.get_calendar_text()
            self.emails.insert(0, Email(
                sender=self.get_text('sender_calendar'),
                subject=self.get_text('subject_new_month', date=cal),
                body=self.get_text('body_new_month', date=cal,
                                   money=self.money, fans=int(self.fans)),
                date_week=self.week
            ))
            if hasattr(self, 'audio'):
                self.audio.speak(self.get_text('announce_new_month', date=cal), interrupt=False)

        # Monatlicher Kontoauszug
        if (self.week == 1) or (is_new_month and self.week > 4):
            self._send_monthly_bank_statement()

        # Jahres-Reset für Buchhaltung und Jahresbilanz
        if (self.week - 1) % WEEKS_PER_YEAR == 0:
            if self.week > 1 and hasattr(self, "accounting"):
                inc = self.accounting.get("income", 0)
                exp = self.accounting.get("expenses", 0)
                prof = inc - exp
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_accounting'),
                    subject=self.get_text('subject_yearly_report', year=self.get_calendar_year() - 1),
                    body=self.get_text('body_yearly_report', income=inc, expenses=exp, profit=prof),
                    date_week=self.week
                ))
            self.accounting = {"income": 0, "expenses": 0, "loan_paid": 0}
            # Neue Themen freischalten
            self._unlock_historical_topics()
            
        # --- Pleite-Check (Bankruptcy Check) ---
        if self.is_bankrupt() and not getattr(self, "pending_bankrupt", False):
            self.pending_bankrupt = True
            self.time_speed = 0  # Pause das Spiel bei Bankrott
            if hasattr(self, 'audio'):
                self.audio.play_sound('warn')
                self.audio.speak(self.get_text('bankruptcy_warning'), interrupt=True)
            
        # --- AUDIO FEEDBACK: Warnung bei wenig Geld ---
        if self.money < 5000 and self.week > 10:
            if hasattr(self, 'audio'):
                self.audio.play_sound('warn')
                self.audio.speak(self.get_text('low_money_warning', amount=self.money), interrupt=False)
            
        # Gehälter berechnen (monatlich aufgeteilt auf Wochen)
        self.pay_salaries()
        
        # Gehälter abziehen (jetzt monatlich bei Monatswechsel)
        if is_new_month and self.week > 1:
            total_salary = self.accrued_salaries
            self.track_expense("salaries", total_salary)
            self.accrued_salaries = 0 # Reset nach Zahlung
        
        
        # NEU Phase H: Erweiterte Mitarbeiter-Logik (Moral, Kündigungen, Gehalt)
        
        # Büro-Moralbonus berechnen (Summe aller morale_bonus der platzierten Objekte)
        office_morale_bonus = 0
        for obj in getattr(self, 'office_objects', []):
            m_bonus = 0
            if hasattr(obj, 'get'):
                m_bonus = obj.get("morale_bonus", 0)
            elif isinstance(obj, dict):
                from game_data import BUILD_OBJECTS
                obj_type = obj.get("type", obj.get("object_type"))
                obj_def = BUILD_OBJECTS.get(obj_type)
                if obj_def:
                    m_bonus = obj_def.get("morale_bonus", 0)
            office_morale_bonus += m_bonus

        # NEU: Team-Persönlichkeit easygoing
        has_easygoing = any(getattr(e, "personality", None) == "easygoing" for e in self.employees)

        quitting_employees = []
        for i, emp in enumerate(self.employees):
            emp.weeks_employed += 1
            if not getattr(self, 'crunch_active', False):
                # Standard-Basis (2) + Büro-Bonus
                reg_bonus = 2 + office_morale_bonus
                if has_easygoing:
                    reg_bonus *= 1.10
                if getattr(emp, "personality", None) == "perfectionist":
                    reg_bonus *= 0.90
                emp.morale = min(100, emp.morale + max(1, int(reg_bonus)))

            # -----------------------------------------------
            # NEU Phase 2: Training-Countdown
            # -----------------------------------------------
            if getattr(emp, 'is_training', False):
                emp.training_weeks_left -= 1
                if emp.training_weeks_left <= 0:
                    emp.is_training = False
                    # Skill vergeben
                    boost = getattr(emp, 'training_skill_boost', 0)
                    if boost > 0:
                        emp.skills[emp.primary_skill] = min(100, emp.skills[emp.primary_skill] + boost)
                    emp.training_skill_boost = 0
                    self.emails.insert(0, Email(
                        sender=self.get_text('sender_hr'),
                        subject=self.get_text('subject_training_done', name=emp.name),
                        body=self.get_text('body_training_done', name=emp.name, skill=emp.primary_skill, value=emp.skills[emp.primary_skill]),
                        date_week=self.week
                    ))
                continue  # Trainierende Mitarbeiter kündigen nicht / bekommen keine Gehaltsanfragen

            # -----------------------------------------------
            # NEU Phase 2: Krankheitsausfälle
            # -----------------------------------------------
            if getattr(emp, 'is_sick', False):
                emp.sick_weeks_left -= 1
                if emp.sick_weeks_left <= 0:
                    emp.is_sick = False
                    self.emails.insert(0, Email(
                        sender=self.get_text('sender_hr'),
                        subject=self.get_text('subject_sick_recovered', name=emp.name),
                        body=self.get_text('body_sick_recovered', name=emp.name),
                        date_week=self.week
                    ))
                continue  # Kranke nicht kündigen / keine Gehaltsanfragen

            # Krankheits-Zufallsevent (basierend auf Burnout / Moral)
            # Bei Moral < 30: 8% Chance, bei Moral < 60: 3% Chance, sonst 1%
            if not emp.is_sick and not emp.is_training:
                sick_chance = 0.01
                if emp.morale < 30:
                    sick_chance = 0.08
                elif emp.morale < 60:
                    sick_chance = 0.03
                if random.random() < sick_chance:
                    emp.is_sick = True
                    emp.sick_weeks_left = random.randint(1, 3)
                    self.emails.insert(0, Email(
                        sender=self.get_text('sender_hr'),
                        subject=self.get_text('subject_sick', name=emp.name),
                        body=self.get_text('body_sick', name=emp.name, weeks=emp.sick_weeks_left),
                        date_week=self.week
                    ))
                    continue

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
                self.emails.insert(0, Email(
                sender=e.name,
                subject=self.get_text('subject_quit'),
                body=self.get_text('body_quit', name=e.name),
                date_week=self.week
            ))


        
        # Kreditabzahlung
        if getattr(self, "bank_loan", None):
            payment = min(self.bank_loan.weekly_payment, self.bank_loan.amount_remaining)
            # NEU: Wenn nicht genug Geld für die Rate → Bankrott-Warnung
            if self.money < payment:
                if not getattr(self, "pending_bankrupt", False):
                    self.pending_bankrupt = True
                    self.time_speed = 0
                    if hasattr(self, 'audio'):
                        self.audio.play_sound('warn')
                        self.audio.speak(self.get_text('loan_default_warning'), interrupt=True)
            else:
                self.track_expense("loan_repayment", payment)
                self.accounting["loan_paid"] += payment
                self.bank_loan.amount_remaining -= payment
                self.bank_loan.weeks_remaining -= 1
                if self.bank_loan.amount_remaining <= 0 or self.bank_loan.weeks_remaining <= 0:
                    self.bank_loan = None
                    self.emails.insert(0, Email(
                        sender=self.get_text('sender_bank'),
                        subject=self.get_text('subject_loan_paid'),
                        body=self.get_text('body_loan_paid'),
                        date_week=self.week
                    ))
                    if hasattr(self, 'audio'):
                        self.audio.play_sound('success')
                        self.audio.speak(self.get_text('subject_loan_paid'), interrupt=False)
        
        # NEU Phase I/II: Industriespionage / Headhunting
        if self.week % 8 == 0 and self.employees and self.rivals:
            rival = random.choice(self.rivals)
            
            # Check für Sicherheits-Zentrale & Rechtsabteilung
            security_bonus = 1.0
            legal_bonus = 1.0
            has_legal = False
            for obj in getattr(self, 'office_objects', []):
                if obj.get('bonus') == 'security':
                    security_bonus = 0.5 # Chance halbiert
                if obj.get('bonus') == 'legal_protection':
                    legal_bonus = 0.7 # Weitere 30% Reduktion
                    has_legal = True
            
            # Basis-Chance skaliert mit Schwierigkeit
            diff_multi = {0: 0.2, 1: 0.5, 2: 1.0, 3: 1.8}.get(self.difficulty, 1.0)
            chance = 0.06 * diff_multi * security_bonus * legal_bonus
            
            if getattr(rival, 'ai_personality', '') == "Aggressive": chance *= 1.5
            
            if random.random() < chance:
                target_emp = random.choice(self.employees)
                
                # Schutz-Logik Phase II: Rechtsabteilung schützt Top-Leute
                if has_legal and getattr(target_emp, 'level', 1) >= 8:
                    # Der Versuch scheitert stillschweigend (Vertrag ist zu gut)
                    pass
                elif not getattr(target_emp, 'pending_poach_offer', False):
                    target_emp.pending_poach_offer = True
                    offer_salary = int(target_emp.salary * 1.5)
                    mail = Email(
                        sender="Headhunter",
                        subject=self.get_text('subject_poach_offer', name=target_emp.name),
                        body=self.get_text('body_poach_offer', name=target_emp.name, rival=rival.name, salary=offer_salary),
                        date_week=self.week
                    )
                    mail.is_poach_offer = True
                    mail.employee_idx = self.employees.index(target_emp)
                    mail.offered_salary = offer_salary
                    self.emails.insert(0, mail)

        # Mitarbeiter verlässt Studio bei ignoriertem Abwerbeangebot
        for emp in list(self.employees):
            if getattr(emp, 'pending_poach_offer', False):
                # Wir nutzen ein einfaches 'timer' Attribut oder prüfen ob das Angebot alt ist
                # Da wir kein Zeitstempel im Employee für das Angebot haben, nutzen wir eine Chance
                if random.random() < 0.3: # 30% Chance pro Woche zu gehen
                    self.employees.remove(emp)
                    self.emails.insert(0, Email(
                        sender="System",
                        subject=self.get_text('subject_employee_left', name=emp.name),
                        body=self.get_text('body_employee_left_poach', name=emp.name),
                        date_week=self.week
                    ))
                    self.audio.speak(self.get_text('employee_left_poach', name=emp.name))

        # NEU Phase II: Marktforschung / KI-Spionage
        has_intel = False
        for obj in getattr(self, 'office_objects', []):
            if obj.get('bonus') == 'competitor_intel':
                has_intel = True
                break
        
        if has_intel and is_new_month:
            potential_targets = [r for r in self.rivals if getattr(r, 'planned_project', None)]
            if potential_targets:
                target = random.choice(potential_targets)
                plan = target.planned_project
                self.emails.append(Email(
                    sender=self.get_text('sender_intel'),
                    subject=self.get_text('subject_intel_report', name=target.name),
                    body=self.get_text('body_intel_report', name=target.name, genre=self.get_text(plan['genre'])),
                    date_week=self.week
                ))

        # Trend check (ca. alle 4-8 Monate)
        trend_interval = random.randint(int(WEEKS_PER_YEAR * 0.4), int(WEEKS_PER_YEAR * 0.8))
        if self.week - self.last_trend_week >= trend_interval:
            if self.week % 8 == 0:
                self.generate_trend()

        # --- SoundCon: Jahresereignis (jedes Jahr Woche 2 = Messe-Zeit) ---
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        current_year = self.get_calendar_year()
        if week_in_year == 2 and current_year > self.soundcon_last_year:
            # Messe steht an – Spieler via E-Mail informieren
            self.emails.insert(0, Email(
                sender=self.get_text('soundcon_sender'),
                subject=self.get_text('soundcon_email_subject', year=current_year),
                body=self.get_text('soundcon_email_body'),
                date_week=self.week
            ))
            if hasattr(self, 'audio'):
                self.audio.play_sound('confirm')
                self.audio.speak(self.get_text('soundcon_announcement', year=current_year), interrupt=False)

        # --- Soundtrack-Label: Wöchentliche Tantiemen ---
        if getattr(self, 'soundtrack_label', None):
            label_income = self.soundtrack_label.tick_week()
            label_hype   = self.soundtrack_label.tick_hype()
            if label_income > 0:
                self.track_income('other', label_income)
            if label_hype > 0:
                self.hype = min(250, self.hype + label_hype)

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
        
        # Marktanteil der eigenen Konsole erhöhen
        if hasattr(self, "custom_consoles"):
            for cc in self.custom_consoles:
                cc.market_share = min(0.5, cc.market_share + (cc.tech_level * 0.0005))
            
        # Projektfortschritt für alle aktiven Projekte
        for ap in self.active_projects:
            if getattr(self, 'strike_weeks_left', 0) > 0:
                continue
            proj = ap["project"]
            
            # NEU: Auftragsarbeiten
            if getattr(proj, "target_points", None) is not None:
                points_added = 0.0
                skill_map = {"Code": "Programmierung", "Audio": "Sound", "Grafik": "Grafik", "Design": "Design"}
                skill_name = skill_map.get(proj.type, "Programmierung")
                
                active_emps = self._active_employees(proj)
                for emp in active_emps:
                    points_added += emp.skills.get(skill_name, 50) / 10.0
                
                if not active_emps:
                    points_added = 5.0
                    
                points_added *= getattr(self, "dev_speed_multiplier", 1.0)
                proj.current_points = min(proj.target_points, proj.current_points + points_added)
                
                if proj.current_points >= proj.target_points:
                    ap["ready_to_finish"] = True
                
                # Moral-Malus
                if ap.get("crunch"):
                    has_break = self.has_office_bonus("morale_room")
                    break_mod = 0.5 if has_break else 1.0
                    for emp in active_emps:
                        morale_loss = int(random.randint(2, 5) * break_mod)
                        if getattr(emp, "personality", None) == "workaholic":
                            morale_loss = int(morale_loss * 1.5)
                        emp.morale = max(0, emp.morale - morale_loss)
                else:
                    for emp in active_emps:
                        if getattr(emp, "personality", None) == "workaholic":
                            emp.morale = max(0, emp.morale - 1)
                            
                continue

            boost = 2 if ap.get("crunch") else 1
            if getattr(proj, 'is_remaster', False):
                boost *= 1.5
                
            # Burnout-Event Malus / Talent-Boom Bonus
            for e in self.active_events:
                if e["effect"] == "dev_speed_drop":
                    boost *= e["multiplier"]
                elif e["effect"] == "dev_speed_boost":
                    boost *= e["multiplier"]
            
            # Team Speed Modifier durch Eigenschaften
            boost *= self.get_team_speed_modifier(proj)
            
            # NEU Phase I: Co-Dev Boost
            if ap.get("co_dev"):
                boost *= 1.8 # Fast doppelte Geschwindigkeit
            
            boost *= self.dev_speed_multiplier
            if getattr(self, 'office_perks', []):
                boost *= (1.0 + len(self.office_perks) * 0.02)
            
            ap["progress"] += boost
            
            if ap.get("crunch"):
                has_break = self.has_office_bonus("morale_room")
                break_mod = 0.5 if has_break else 1.0
                # Moral-Malus nur für das Team des Projekts
                active_emps = self._active_employees(proj)
                for emp in active_emps:
                    morale_loss = int(random.randint(2, 5) * break_mod)
                    if getattr(emp, "personality", None) == "workaholic":
                        morale_loss = int(morale_loss * 1.5)
                    emp.morale = max(0, emp.morale - morale_loss)
            else:
                # Kein Crunch: Workaholics verlieren wöchentlich 1 Moralpunkt durch harte Arbeit
                active_emps = self._active_employees(proj)
                for emp in active_emps:
                    if getattr(emp, "personality", None) == "workaholic":
                        emp.morale = max(0, emp.morale - 1)
                    
                # Bug-Zuwachs
                base_bugs = random.randint(1, 3)
                ap["bugs"] += int(base_bugs * self.get_team_bug_modifier(proj))
            
            # Zufällige Bugs auch ohne Crunch (seltener)
            if random.random() < 0.1:
                ap["bugs"] += int(1 * self.get_team_bug_modifier(proj))
                
            # Supporter fixen aktiv Bugs jede Woche während der Entwicklung
            active_supps = [e for e in self._active_employees(proj) if e.role == "Supporter"]
            if active_supps and ap["bugs"] > 0:
                ap["bugs"] = max(0, ap["bugs"] - len(active_supps))

            # AAA Events (Max 1x pro Projekt)
            # Fertigstellung-Check
            if ap["progress"] >= ap["total_weeks"]:
                ap["ready_to_finish"] = True
                
            # AAA Events (Max 1x pro Projekt)
            if proj.size == "AAA" and not ap.get("aaa_event_done"):
                prog_pct = ap["progress"] / ap["total_weeks"]
                if 0.2 < prog_pct < 0.8 and random.random() < 0.05:
                    from game_data import AAA_DEV_EVENTS
                    self.pending_dev_event = {
                        "data": random.choice(AAA_DEV_EVENTS),
                        "ap": ap
                    }
                    ap["aaa_event_done"] = True
                    self.time_speed = 0

            # Allgemeine Events
            max_ev = {"Klein": 1, "Mittel": 1, "Groß": 2, "AAA": 0}.get(proj.size, 1)
            if ap.get("event_count", 0) < max_ev:
                prog_pct = ap["progress"] / ap["total_weeks"]
                if 0.15 < prog_pct < 0.85:
                    chance = {"Klein": 0.04, "Mittel": 0.05, "Groß": 0.06}.get(proj.size, 0.05)
                    if random.random() < chance:
                        from game_data import GENERAL_DEV_EVENTS
                        self.pending_dev_event = {
                            "data": random.choice(GENERAL_DEV_EVENTS),
                            "ap": ap
                        }
                        ap["event_count"] = ap.get("event_count", 0) + 1
                        self.time_speed = 0

        # Forschungsfortschritt
        if self.is_researching:
            self.research_progress += 1
            if self.research_progress >= self.research_total_weeks:
                self.complete_research()

        # Konsolenentwicklung
        if getattr(self, "is_developing_console", False):
            self.console_progress += 1
            if self.console_progress >= self.console_total_weeks:
                self.is_developing_console = False
                c = self.current_console_draft
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
        # Expo Trigger (Mitte des Jahres)
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        if week_in_year == (WEEKS_PER_YEAR // 2): 
            self.emails.append(Email(
                sender=self.get_text('sender_assistant'),
                subject=self.get_text('subject_expo', default="Spiele-Messe: Ausstellung!"),
                body=self.get_text('body_expo', default="Die jährliche Spiele-Messe steht vor der Tür. Wir können dort ausstellen!"),
                date_week=self.week,
                is_bug=False
            ))
            self.emails[-1].is_expo_invite = True

        # --- Saisonale Modifikatoren (dynamisch) ---
        season_mod = 1.0
        # Weihnachtsgeschäft (letzte 4 Wochen des Jahres)
        winter_start = WEEKS_PER_YEAR - 3
        if winter_start <= week_in_year <= WEEKS_PER_YEAR:
            season_mod = 1.5
        # Sommerloch (ca. 60% bis 75% des Jahres)
        summer_start = int(WEEKS_PER_YEAR * 0.6)
        summer_end = int(WEEKS_PER_YEAR * 0.75)
        if summer_start <= week_in_year <= summer_end:
            season_mod = 0.8

        # Achievements prüfen
        if hasattr(self, "_check_achievements"):
            self._check_achievements()

        # Verkäufe für aktive Spiele
        for g in self.game_history:
            if g.is_active:
                g.weeks_on_market += 1
                
                # In-Game Werbung (Feature 1)
                if getattr(g, "has_ads", False):
                    ad_rev = int((g.sales * 0.05) + (g.revenue * 0.01))
                    if ad_rev > 0:
                        self.track_income("other", ad_rev)
                        g.revenue += ad_rev
                        self.hype = max(0.0, self.hype - 0.5) # Hype loss due to ads

                # Modding-Support (Feature 2)
                decay_factor = 0.1 if getattr(g, "has_mod_support", False) else 0.2

                # Verkäufe sinken mit der Zeit, plus saisonale Effekte
                new_sales = int((self.calculate_sales(g) * season_mod) / (1 + g.weeks_on_market * decay_factor))
                if getattr(g, "bugs", 0) > 0:
                    new_sales = int(new_sales * 0.5) # Bugs halbieren Verkäufe
                    fan_loss = int(g.bugs * 2.0)
                    fan_loss = max(0, fan_loss - (getattr(self, "support_level", 0) * 5))
                    self.fans = max(0, self.fans - fan_loss)
                    
                # Event-Modifikatoren
                for e in self.active_events:
                    if e["effect"] == "sales_drop":
                        new_sales = int(new_sales * e["multiplier"])
                    elif e["effect"] == "sales_boost":
                        new_sales = int(new_sales * e["multiplier"])

                if getattr(g, "is_f2p", False):
                    g.active_players = int(getattr(g, "active_players", 0) * 0.95) + new_sales
                    f2p_revenue = int(g.active_players * 0.2 * self.profit_multiplier)
                    g.sales += new_sales
                    g.revenue += f2p_revenue
                    self.track_income("sales", f2p_revenue)
                    if g.weeks_on_market > int(WEEKS_PER_YEAR * 0.4) or new_sales < 100:
                        g.is_active = False
                    continue
                
                price = AUDIENCE_PRICE.get(g.audience, 30)
                
                # Physikalischer Verkauf zuerst
                physical_sold = 0
                if getattr(g, "physical_copies", 0) > 0:
                    physical_sold = min(new_sales, g.physical_copies)
                    g.physical_copies -= physical_sold
                    self.used_storage -= physical_sold
                    g.lifetime_physical_sales = getattr(g, "lifetime_physical_sales", 0) + physical_sold
                    
                digital_sold = new_sales - physical_sold
                
                physical_rev = physical_sold * getattr(g, "physical_price", 45)
                digital_rev = digital_sold * price
                
                g.sales += new_sales
                total_rev = int((digital_rev + physical_rev) * self.profit_multiplier)
                g.revenue += total_rev
                
                self.track_income("sales", total_rev)

                # Optional: Addons pushen die Verkäufe
                for addon in self.active_addons:
                    if addon.base_game_name == g.name:
                        new_sales = int(new_sales * 1.5) # 50% Boost durch aktives Addon

                if g.weeks_on_market > int(WEEKS_PER_YEAR * 0.4) or new_sales < 100:
                    g.is_active = False

        # Einnahmen durch Addons
        for addon in self.active_addons:
            base_game = next((g for g in self.game_history if g.name == addon.base_game_name), None)
            if base_game and base_game.is_active:
                elapsed = max(1, self.week - addon.week_developed)
                sales = int(base_game.sales * 0.05 / (1 + elapsed * 0.1))
                if sales > 0:
                    revenue = int(sales * 15 * self.profit_multiplier)
                    addon.sales += sales
                    addon.revenue += revenue
                    self.track_income("sales", revenue)

        # Einnahmen durch Bundles
        for bundle in self.active_bundles:
            from game_data import BUNDLE_DATA
            sales = max(10, int(500 * (bundle.average_score / 10) * BUNDLE_DATA["revenue_mod"]))
            revenue = int(sales * bundle.base_price * self.profit_multiplier)
            bundle.sales += sales
            bundle.revenue += revenue
            self.track_income("sales", revenue)

        # Lizenzen verwalten
        licenses_to_remove = []
        for lic in self.active_licenses:
            if hasattr(lic, "duration"):
                lic.duration -= 1
                if lic.duration <= 0 and not getattr(lic, "used", False):
                    licenses_to_remove.append(lic)
        
        for lic in licenses_to_remove:
            self.active_licenses.remove(lic)
            self.emails.append(Email(
                sender=self.get_text('sender_system'),
                subject=self.get_text('subject_license_expired'),
                body=self.get_text('body_license_expired', name=lic.name),
                date_week=self.week
            ))

        # MMOs & Server Usage verarbeiten
        total_mmo_players = sum(m.players for m in self.active_mmos if m.game.is_active)
        total_subs = getattr(self, "subscription_subscribers", 0)
        ad_games_traffic = sum(g.sales for g in self.game_history if g.is_active and getattr(g, "has_ads", False)) // 10
        server_usage = total_mmo_players + total_subs + ad_games_traffic
        
        server_capacity = getattr(self, 'server_capacity', 0)
        server_overloaded = server_usage > server_capacity
        
        if server_overloaded:
            self.hype = max(0.0, self.hype - 2.0)
        
        for mmo in self.active_mmos:
            if mmo.game.is_active:
                mmo.weeks_active += 1
                rev = int(mmo.weekly_revenue * self.profit_multiplier)
                self.track_income("mmo", rev)
                self.track_expense("mmo", mmo.weekly_cost)
                mmo.game.revenue += rev
                
                if server_overloaded:
                    mmo.players = int(mmo.players * 0.85)
                else:
                    mmo.players = int(mmo.players * 0.98)
                
                if mmo.players < 1000:
                    mmo.game.is_active = False

        if server_overloaded and server_usage > 0 and is_new_month:
                self.emails.append(Email(
                sender=self.get_text('sender_system'),
                subject=self.get_text('subject_server_overload'),
                body=self.get_text('body_server_overload'),
                date_week=self.week,
                is_bug=True
            ))

        # Fan-Mails & Bugs
        self.process_emails()
        
        # Lagerkosten
        if self.used_storage > 0:
            storage_cost = int(self.used_storage * 0.1)
            self.track_expense("other", storage_cost)

        # Merchandising
        for merch in self.active_merch:
            if merch["stock"] > 0:
                sales = int(random.randint(5, 40) * merch["hype_multi"] * (1 + self.hype / 100))
                sales = min(sales, merch["stock"])
                if sales > 0:
                    rev = int(sales * merch["sell_price"] * self.profit_multiplier)
                    self.track_income("merch", rev)
                    merch["stock"] -= sales
                    merch["sales"] += sales
                    merch["revenue"] += rev
                    self.used_storage -= sales
                    if merch["stock"] <= 0:
                                        self.emails.append(Email(
                            sender=self.get_text("sender_logistics"),
                            subject=self.get_text("subject_merch_sold_out"),
                            body=self.get_text("body_merch_sold_out", name=merch["name"]),
                            date_week=self.week
                        ))
        self.active_merch = [m for m in self.active_merch if m["stock"] > 0]

        # Publishing Angebote
        if self.office_level >= 2 and random.random() < 0.05:
            self._generate_publishing_offer()

        # Third-Party Spiele
        for published_game in self.published_third_party_games:
            if published_game.is_active:
                published_game.weeks_on_market += 1
                base_sales = published_game.quality * 1000
                sales_this_week = int(base_sales / (1 + published_game.weeks_on_market * 0.1))
                published_game.total_sales += sales_this_week
                gross_revenue = int(sales_this_week * 30 * self.profit_multiplier)
                player_cut = int(gross_revenue * published_game.player_share)
                our_cut = gross_revenue - player_cut
                self.track_income("sales", our_cut)
                published_game.total_revenue += gross_revenue
                published_game.player_profit += player_cut
                if sales_this_week < 50 or published_game.weeks_on_market > int(WEEKS_PER_YEAR * 0.6):
                    published_game.is_active = False

        # ============================================================
        # NEU: v3.11.0-beta.1 Expansion Weekly Updates
        # ============================================================
        
        # 1. Temporäre Modifikatoren abbauen
        if getattr(self, "temp_dev_speed_weeks", 0) > 0:
            self.temp_dev_speed_weeks -= 1
            if self.temp_dev_speed_weeks <= 0:
                self.temp_dev_speed_penalty = 1.0
                
        if getattr(self, "temp_quality_weeks", 0) > 0:
            self.temp_quality_weeks -= 1
            if self.temp_quality_weeks <= 0:
                self.temp_quality_boost = 0.0

        # 2. Jingles aktualisieren
        active_jingles = []
        for jingle in getattr(self, "active_jingles", []):
            if hasattr(jingle, "weeks_left"):
                jingle.weeks_left -= 1
                if jingle.weeks_left > 0:
                    active_jingles.append(jingle)
            else:
                jingle.weeks_left = 3
                active_jingles.append(jingle)
        self.active_jingles = active_jingles

        # 3. Soundkarten wöchentliche Updates
        self.update_hardware_development()
        
        for card in getattr(self, "sound_card_projects", []):
            if card.is_released:
                card.weeks_on_market += 1
                
                # Marktanteil-Berechnung mit Decay
                from game_data import HARDWARE_TECH_LIST
                features_bonus = sum(f["sound_bonus"] for f in HARDWARE_TECH_LIST if f["id"] in card.features)
                base_market_share = 0.05 + features_bonus
                card.market_share = max(0.005, base_market_share / (1.0 + card.weeks_on_market * 0.04))
                
                # Passive wöchentliche Tantiemen generieren
                royalties = int(card.market_share * random.randint(4000, 12000))
                card.royalties_gained = royalties
                card.lifetime_royalties += royalties
                self.track_income("hardware", royalties)

        # 4. Fanpost wöchentlich generieren
        self.receive_fan_mail()

        # 4b. Barrierefreiheits-Reputation sorgt fuer langsames Community-Wachstum
        self.update_accessibility_reputation()

        # 5. Büro-Events wöchentlich prüfen & triggern
        self.trigger_personality_event()

        # WÖCHENTLICHE BILANZ ABSPEICHERN
        self.finalize_weekly_balance()

        # NEU: Phase 7 - Rivalen und GOTY evaluieren
        self._process_rivals()
        self._process_tournaments()
        self._process_sponsorships()
        if week_in_year == WEEKS_PER_YEAR:
            self._check_goty()
        self._check_shareholder_meeting()

    def calculate_hype(self, project):
        """Berechnet den Hype für ein Spiel basierend auf Marketing, Lizenzen und Events."""
        hype = 0
        # Marketing - Jetzt dynamisch aus game_data.py
        from game_data import MARKETING_OPTIONS_PH5
        m_option = next((m for m in MARKETING_OPTIONS_PH5 if m["name"] == project.marketing), None)
        
        if m_option:
            hype += m_option.get("hype", 0)
        elif project.marketing == 'publisher_deal':
            hype += 40
        elif project.marketing == 'small': # Legacy Support
            hype += 10
        elif project.marketing == 'medium':
            hype += 25
        elif project.marketing == 'large':
            hype += 50
            
        # Marketing-Effizienz anwenden
        hype *= self.marketing_efficiency

        # Lizenzen
        if getattr(project, 'license_bonus', 0) > 0:
            hype += project.license_bonus

        # Projektbezogener Hype aus Fanpost, Jingles und Community-Aktionen
        hype += getattr(project, 'hype', 0.0)

        # Zufallsereignis Bonus
        for event in self.active_events:
            if event["effect"] == "hype_boost":
                hype += event.get("hype_amount", event.get("amount", 0))

        # Globaler Hype-Multiplikator
        hype *= self.hype_multiplier

        return min(250, int(hype))

    def _process_rivals(self):
        """Lsst Rivalen Spiele verffentlichen und Marktanteile beeinflussen."""
        import competitor_ai
        
        for rival in self.rivals:
            if getattr(rival, 'is_owned_by_player', False):
                # Phase 2 M&A: Passive Einnahmen durch den Backkatalog
                back_catalog_income = int(sum(getattr(g, 'score', 0) * 100 for g in getattr(rival, 'games', [])))
                if back_catalog_income > 0:
                    self.track_income("other", back_catalog_income)
                continue

            r_game = competitor_ai.evaluate_turn(rival, self)
            
            if r_game:
                # Sabotage-Check: Wenn der Spieler gerade das gleiche Genre entwickelt
                sabotage_msg = ""
                can_sabotage = (self.week - self.last_sabotage_week) >= 4
                
                if can_sabotage and self.is_developing and any(ap["project"].genre == r_game.genre for ap in self.active_projects):
                    # Hype-Verlust skaliert mit Schwierigkeit
                    diff_multi = {0: 0.3, 1: 0.6, 2: 1.0, 3: 1.5}.get(self.difficulty, 1.0)
                    base_loss = random.randint(10, 25)
                    loss = int(base_loss * diff_multi)
                    
                    # PR Defense Check (Phase II)
                    pr_bonus = 1.0
                    for obj in getattr(self, 'office_objects', []):
                        if obj.get('bonus') == 'pr_defense':
                            pr_bonus = 0.5
                    
                    loss = int(loss * pr_bonus)
                    
                    self.hype = max(0, self.hype - loss)
                    self.last_sabotage_week = self.week
                    sabotage_msg = f"\n\n{self.get_text('sabotage_warning', name=rival.name, genre=self.get_text(r_game.genre))}"
                
                # Benachrichtigung
                if r_game.score >= 8.5 or sabotage_msg:
                    self.emails.append(Email(
                        sender=self.get_text('sender_industry_news'),
                        subject=self.get_text('subject_rival_hit', name=rival.name),
                        body=self.get_text('body_rival_hit', name=rival.name, game=r_game.name, score=r_game.score, genre=self.get_text(r_game.genre)) + sabotage_msg,
                        date_week=self.week
                    ))

                # Dividende ausschütten, falls Anteile besessen werden
                if getattr(rival, 'owned_shares', 0) > 0:
                    dividend = int((r_game.score * 10000) * (rival.owned_shares / 100))
                    self.track_income("other", dividend)
                    self.emails.append(Email(
                        sender=self.get_text('sender_bank'),
                        subject=self.get_text('subject_dividend'),
                        body=self.get_text('body_dividend', name=rival.name, amount=dividend),
                        date_week=self.week
                    ))
                
                # Marktauswirkung: Zieht Hype und Verkäufe ab, wenn wir auch ein Spiel im gleichen Genre haben
                for my_game in self.game_history:
                    if my_game.is_active and my_game.genre == r_game.genre:
                        # Unser Spiel verliert Hype (passiv über Zeit)
                        self.hype = max(0, self.hype - 10)



    
    def _process_sponsorships(self):
        if not hasattr(self, "active_sponsorships"):
            self.active_sponsorships = []
        for s in list(self.active_sponsorships):
            s["duration"] -= 1
            if s["duration"] <= 0:
                self.streamer_hype_multi /= s["boost"]
                self.active_sponsorships.remove(s)
                
    def add_sponsorship(self, boost, duration):
        if not hasattr(self, "active_sponsorships"):
            self.active_sponsorships = []
        self.active_sponsorships.append({"boost": boost, "duration": duration})
        self.streamer_hype_multi *= boost

    def _process_tournaments(self):
        """Verarbeitet aktive E-Sport-Turniere: liefert Einnahmen, Hype und Fans."""
        if not getattr(self, "active_tournaments", []):
            return
        finished = []
        for tournament in self.active_tournaments:
            tournament["weeks_left"] = tournament.get("weeks_left", 4) - 1
            if tournament["weeks_left"] <= 0:
                finished.append(tournament)
        for t in finished:
            self.active_tournaments.remove(t)
            prize = t.get("prize_pool", 50000)
            hype_gain = t.get("hype_bonus", 20)
            fan_gain = t.get("fan_bonus", 10000)
            self.track_income("other", prize)
            self.hype = min(250, self.hype + hype_gain)
            self.fans += fan_gain
            self.emails.insert(0, Email(
                sender=self.get_text('sender_industry_news'),
                subject=self.get_text('esports_result_subject', name=t.get("name", "Turnier")),
                body=self.get_text(
                    'esports_result_body',
                    name=t.get("name", "Turnier"),
                    prize=prize,
                    fans=fan_gain,
                    hype=hype_gain
                ),
                date_week=self.week
            ))
            if hasattr(self, 'audio'):
                self.audio.play_sound('cheer')
                self.audio.speak(self.get_text(
                    'esports_result_subject',
                    name=t.get("name", "Turnier")
                ), interrupt=False)

    
    def _check_shareholder_meeting(self):
        year = self.get_calendar_year()
        if not hasattr(self, 'last_shareholder_year'):
            self.last_shareholder_year = year - 1
        if getattr(self, 'is_public_company', False) and year > self.last_shareholder_year:
            self.last_shareholder_year = year
            if self.money < self.shareholder_target:
                self.share_value = max(10, getattr(self, 'share_value', 100) - 20)
            else:
                self.share_value = getattr(self, 'share_value', 100) + 10
            self.shareholder_target = self.money + 50000
            self.pending_shareholder_meeting = True

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
        if hasattr(self, 'audio'):
            self.audio.play_sound('drumroll')
            self.audio.speak(self.get_text('goty_ceremony_start'), interrupt=True)
 
    def _generate_industry_news(self):
        """Erzeugt zufällige Markt-Ereignisse."""
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
            if hasattr(self, 'audio'):
                self.audio.play_sound('error')
            return False
            
        self.track_expense("staff", hire_cost)
        if hasattr(self, 'audio'):
            self.audio.play_sound('buy')
            self.audio.speak(self.get_text('employee_hired', name=employee.name), interrupt=True)
        self.employees.append(employee)
        return True

    def fire_employee(self, index):
        """Entlässt einen Mitarbeiter."""
        if 0 <= index < len(self.employees):
            emp = self.employees[index]
            if getattr(emp, "is_ceo", False):
                return None # Chef kann nicht gefeuert werden
            self.employees.pop(index)
            # Abfindung = 1 Monat Gehalt (entspricht ca. 4 Wochen)
            self.track_expense("salaries", emp.salary)
            return emp
        return None

    def pay_salaries(self):
        """Bezahlt alle Gehälter (monatlich aufgestaut)."""
        total = sum(e.salary for e in self.employees)
        # Wir stauen sie wöchentlich auf (salary / weeks_per_month) und zahlen bei Monatswechsel.
        weeks_per_month = WEEKS_PER_YEAR / 12.0
        weekly_share = total / weeks_per_month
        self.accrued_salaries += weekly_share
        return weekly_share

    def process_emails(self):
        """Generiert zufällige E-Mails."""
        
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
        self.track_expense("production", cost)
        game.dlc_count += 1
        game.is_active = True # Bringt Spiel zurück in die Charts
        # Markt-Reset: Ca. 1 Monat (dynamisch)
        reset_weeks = max(4, int(WEEKS_PER_YEAR / 10))
        game.weeks_on_market = max(0, game.weeks_on_market - reset_weeks)
        self.fans += 500
        return True

    def release_mmo_update(self, mmo_index):
        """Programmiert ein Content-Update für ein MMO, um Spieler zurückzugewinnen."""
        mmo = self.active_mmos[mmo_index]
        cost = 50000
        if self.money < cost:
            return False
        self.track_expense("mmo", cost)
        # Füge Spieler hinzu basierend auf Basis-Spielerzahl (z.B. +10% max)
        new_players = int(mmo.game.sales * 0.05)
        mmo.players += new_players
        self.fans += 1000
        return True

    def _active_employees(self, project=None):
        """Liefert nur Mitarbeiter, die nicht krank und nicht in Training sind. Filtert nach Projekt-Team wenn angegeben."""
        base = [e for e in self.employees if not getattr(e, 'is_sick', False) and not getattr(e, 'is_training', False)]
        if project and hasattr(project, 'assigned_employee_ids') and project.assigned_employee_ids:
            # Nur Mitarbeiter, deren Index in der Liste ist
            return [e for i, e in enumerate(self.employees) if i in project.assigned_employee_ids and e in base]
        return base

    def get_team_bonus(self, project=None):
        """Gesamtbonus des Teams auf Spielqualität (nur aktive Mitarbeiter)."""
        active = self._active_employees(project)
        if not active:
            return 0.0
        
        total_bonus = 0.0
        for e in active:
            eb = e.quality_contribution
            # Spezialisierungs-Bonus einrechnen
            if project and e.specialization:
                spec = e.specialization
                btype = spec.get("bonus_type")
                target = spec.get("target")
                val = spec.get("bonus_value", 0)
                
                if btype == "Genre" and (project.genre == target or project.sub_genre == target):
                    eb *= (1.0 + val)
                elif btype == "Topic" and project.topic == target:
                    eb *= (1.0 + val)
            total_bonus += eb
            
        return total_bonus * self.get_team_quality_modifier(project)

    def get_team_slider_bonus(self, slider_name, project=None):
        """Durchschnittlicher Skill-Bonus des Teams für einen Slider (nur aktive Mitarbeiter)."""
        active = self._active_employees(project)
        if not active:
            return 0.0
        
        bonuses = []
        for e in active:
            b = e.get_slider_bonus(slider_name)
            # Spezialisierungen für bestimmte Kategorien (Code, Sound, Design, Story)
            if e.specialization:
                spec = e.specialization
                btype = spec.get("bonus_type")
                val = spec.get("bonus_value", 0)
                
                # Mapping Slider -> Spezialisierung
                mapping = {
                    "Sound": "Sound",
                    "KI": "KI",
                    "Gameplay": "KI", # Code-Maschine hilft auch bei Gameplay
                    "Grafik": "Grafik",
                    "Welt": "Grafik", # Design-Gott hilft auch bei Welt
                    "Story": "Story"
                }
                if mapping.get(slider_name) == btype:
                    b *= (1.0 + val)
            bonuses.append(b)
            
        return sum(bonuses) / len(bonuses)

    def get_team_speed_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
        
        # Durchschnittlicher Speed-Skill (50 = 1.0)
        avg_speed = sum(e.speed for e in active) / len(active)
        
        # Trait-Modifikatoren (Robust gegen alte Strings oder fehlende Keys)
        trait_mods = []
        for e in active:
            val = 1.0
            if hasattr(e, 'trait') and isinstance(e.trait, dict):
                if e.trait.get("effect") == "speed":
                    val = e.trait.get("value", 1.0)
            trait_mods.append(val)
        trait_avg = sum(trait_mods) / len(trait_mods)
        
        # NEU: Persönlichkeits-Modifikatoren (workaholic: +20% Speed)
        pers_mods = [1.20 if getattr(e, 'personality', None) == 'workaholic' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods)
        
        # NEU: Temporäre Event-Mali
        temp_penalty = getattr(self, "temp_dev_speed_penalty", 1.0)
        
        base_multi = (avg_speed / 50.0) * trait_avg * pers_avg
        return base_multi * self.dev_speed_multiplier * self.logic_multiplier * temp_penalty

    def get_team_bug_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
            
        # Durchschnittlicher Bug-Modifier der Mitarbeiter
        avg_mod = sum(e.bug_modifier for e in active) / len(active)
        
        # Trait-Modifikatoren
        trait_mods = []
        for e in active:
            val = 1.0
            if hasattr(e, 'trait') and isinstance(e.trait, dict):
                if e.trait.get("effect") == "bugs":
                    val = e.trait.get("value", 1.0)
            trait_mods.append(val)
        trait_avg = sum(trait_mods) / len(trait_mods)
        
        # NEU: Persönlichkeits-Modifikatoren (chaotic: +15% Bugs)
        pers_mods = [1.15 if getattr(e, 'personality', None) == 'chaotic' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods)
        
        # QA Bonus
        qa_bonus = 0.7 if self.has_office_bonus("qa_tools") else 1.0
        
        return avg_mod * trait_avg * qa_bonus * pers_avg

    def get_team_quality_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
        mods = [e.trait["value"] if e.trait and e.trait["effect"] == "quality" else 1.0 for e in active]
        
        # NEU: Persönlichkeits-Modifikatoren (perfectionist: +15% Qualität)
        pers_mods = [1.15 if getattr(e, 'personality', None) == 'perfectionist' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods)
        
        # NEU: Temporärer Event-Bonus
        temp_boost = getattr(self, "temp_quality_boost", 0.0)
        
        return (sum(mods) / len(mods)) * pers_avg * (1.0 + temp_boost)

    def get_status_text(self):
        """Gibt einen vollständigen Statustext für den Screenreader aus."""
        lang = self.settings.get("language", "de")
        cal = self.get_calendar_text()
        
        # Aktive Projekte prüfen
        dev_info = ""
        if self.active_projects:
            # Zeige die ersten zwei Projekte namentlich, den Rest als Anzahl
            names = [ap["project"].name for ap in self.active_projects[:2]]
            if len(self.active_projects) > 2:
                names.append(f"+{len(self.active_projects)-2}")
            dev_info = f" | {self.get_text('developing')}: {', '.join(names)}"
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
                f"{self.get_text('money_label')}: {self.money:,.0f} € | "
                f"{self.get_text('fans')}: {self.fans:,} | "
                f"{self.get_text('office')}: {office_name} ({emp_count}/{max_emp} MA) | "
                f"{self.get_text('menu_history_count').replace('{count}.', str(self.games_made))} | "
                f"Hype: {int(self.hype)}"
            )
            if unread > 0:
                status += f" | {unread} ungelesene E-Mails"
        else:
            status = (
                f"{self.company_name} | {cal}{dev_info} | "
                f"{self.get_text('money_label')}: {self.money:,.0f} € | "
                f"{self.get_text('fans')}: {self.fans:,} | "
                f"{self.get_text('office')}: {office_name} ({emp_count}/{max_emp} staff) | "
                f"{self.get_text('menu_history_count').replace('{count}.', str(self.games_made))} | "
                f"Hype: {int(self.hype)}"
            )
            if unread > 0:
                status += f" | {unread} unread emails"
        return status





    # ==========================================================
    # FORSCHUNG & ENGINES
    # ==========================================================

    def get_research_block_reason(self):
        """Gibt den Grund zurück, warum Forschung gerade nicht möglich ist (oder None)."""
        if self.is_researching:
            name = self.current_research_draft['data']['name'] if self.current_research_draft else '?'
            return self.get_text('research_blocked_already_researching', name=name)
        if self.is_developing:
            proj_name = self.active_projects[0]["project"].name if self.active_projects else '?'
            return self.get_text('research_blocked_developing', name=proj_name)
        return None

    def start_research(self, res_data, res_type):
        """Startet ein neues Forschungsprojekt."""
        if self.money < res_data["cost"]:
            return False
        if self.is_researching or self.is_developing:
            return False
            
        self.track_expense("research", res_data["cost"])
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
        return [f for f in ENGINE_FEATURES if f["name"] not in unlocked_names and self.week >= ((f.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

    def get_researchable_topics(self):
        """Themen die erforschbar, aber noch nicht freigeschaltet sind."""
        return [t for t in RESEARCHABLE_TOPICS if t["name"] not in self.unlocked_topics and self.week >= ((t.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

    def get_researchable_genres(self):
        """Genres die erforschbar, aber noch nicht freigeschaltet sind."""
        return [g for g in RESEARCHABLE_GENRES if g["name"] not in self.unlocked_genres and self.week >= ((g.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

    def get_researchable_audiences(self):
        """Zielgruppen die erforschbar, aber noch nicht freigeschaltet sind."""
        return [a for a in RESEARCHABLE_AUDIENCES if a["name"] not in self.unlocked_audiences and self.week >= ((a.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

    def get_researchable_technologies(self):
        """Endgame-Technologien, die noch nicht freigeschaltet sind."""
        return [t for t in RESEARCHABLE_TECHNOLOGIES if t["name"] not in self.unlocked_technologies and self.week >= ((t.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

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
        self.track_expense("shares", price)
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
        self.track_income("shares", sell_price)
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
        # Aktualisiert Markttrends alle 1/4 bis fast 1/2 Jahr
        min_w = WEEKS_PER_YEAR // 4
        max_w = int(WEEKS_PER_YEAR * 0.4) + 1
        if self.week - self.last_trend_week < random.randint(min_w, max_w):
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
        if "duration" in event:
            # Dauerhafte Events zur Liste hinzufügen (Kopie)
            ev_copy = dict(event)
            self.active_events.append(ev_copy)
        elif event["effect"] == "money":
            self.track_income("other", event["value"])
        elif event["effect"] == "fans":
            self.fans = max(0, self.fans + event["value"])
        elif event["effect"] == "hype_boost":
            self.hype += event["hype_amount"]
            
        body = self.get_text("event_" + event["id"], weeks=event.get("duration", 0), hype=event.get("hype_amount", 0))
        self.emails.insert(0, Email(
            sender=self.get_text('sender_industry_news'),
            subject=self.get_text('news_title'),
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
            self.track_expense("other", cost)
            self.owned_licenses.append({
                "name": license_data["name"],
                "purchased_week": self.week,
                "expires_week": self.week + WEEKS_PER_YEAR, # Verfällt nach 1 Jahr
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
            
        self.track_expense("production", cost)
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
        self.track_income("sales", initial_revenue)
        
        return {
            'name': bundle.name,
            'sales': bundle.sales,
            'revenue': bundle.revenue
        }

    # ==========================================================
    # BEWERTUNG
    # ==========================================================

    def calculate_review(self, project, bugs=0):
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
            team_bonus = self.get_team_slider_bonus(sname, project=project)
            effective_val = player_val + team_bonus
            total_diff += abs(effective_val - ideal_val)
            max_diff += 10
        slider_match = 1.0 - (total_diff / max_diff) if max_diff > 0 else 0.5

        # 3. Team-Bonus (0.0 - 1.0)
        team_quality = min(1.0, self.get_team_bonus(project) * 5)

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
        # Schwierigkeits-Standard (steigt über die Jahre)
        base_score *= random_factor * trend_bonus

        # Bug-Malus (Massiv wenn viele Bugs)
        bug_penalty = (bugs * 0.02) # 50 Bugs = -1.0 (10 Punkte auf 10er Skala)
        base_score = max(0.1, base_score - bug_penalty)

        # Massive Bonus for perfect synergy and slider configuration
        if synergy >= 0.8 and slider_match >= 0.8:
            base_score += 0.15

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

        # Barrierefreiheits-Reputation: saubere Screenreader-UX hilft Reviews leicht.
        accessibility_bonus = min(0.05, getattr(self, "accessibility_reputation", 0) / 2000.0)
        base_score += accessibility_bonus

        # Qualitätsstandard-Multiplikator anwenden (macht es über die Jahre schwerer)
        base_review = max(1.0, min(10.0, float(base_score * 10 / self.quality_standard_multi)))

        scores = []
        for _ in range(4):
            variance = random.uniform(-1.2, 1.2)
            s = int(round(max(1.0, min(10.0, base_review + variance))))
            scores.append(s)

        # NEU: Review-Texte generieren
        comments = []
        
        # Intro
        intro_key = random.choice(['review_intro_1', 'review_intro_2', 'review_intro_3', 'review_intro_4', 'review_intro_5'])
        prefix = self.get_text('review_prefix')
        intro = self.get_text(intro_key, company=self.company_name, game=project.name)
        comments.append(f"{prefix}{intro}")
        
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

        if getattr(self, "accessibility_reputation", 0) >= 50:
            comments.append(self.get_text('review_accessibility_praise'))

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

        sales = int(base_sales * score_m * fan_bonus * plat_multi * audience_multi * rand_m * diff_market * self.sales_multiplier)
        if getattr(project, "is_f2p", False):
            sales *= 10
        if getattr(project, "is_remake", False):
            sales = int(sales * 2.0)
        return sales

    def calculate_dev_cost(self, project):
        """Berechnet Entwicklungskosten inkl. Größe und Marketing."""
        # Basis-Kosten basierend auf Größe
        size_data = next((s for s in GAME_SIZES if s["name"] == project.size), GAME_SIZES[1])
        base_cost = 10000 * size_data["cost_multi"]

        # Team-Kosten (nur zugewiesene MA)
        dev_weeks = sum(p["duration_weeks"] for p in DEV_PHASES) * size_data["time_multi"]
        assigned_emps = [self.employees[i] for i in getattr(project, 'assigned_employee_ids', []) if i < len(self.employees)]
        if not assigned_emps: assigned_emps = self.employees # Fallback
        salary_cost = sum(e.salary for e in assigned_emps) * dev_weeks

        # Marketing-Kosten
        from game_data import MARKETING_OPTIONS_PH5
        mark_data = next((m for m in MARKETING_OPTIONS_PH5 if m["name"] == project.marketing), {"cost": 0})
        marketing_cost = mark_data["cost"]

        return int(base_cost + salary_cost + marketing_cost)

    def finalize_game(self, ap_dict, early_access=False):
        """Schließt die Spielentwicklung ab."""
        project = ap_dict["project"]
        bugs = ap_dict["bugs"]
        
        was_early_access = project in self.game_history
        
        project.week_developed = self.week

        # Kosten und Marketing abziehen
        new_dev_cost = self.calculate_dev_cost(project)
        cost_diff = new_dev_cost - getattr(project, "dev_cost", 0)
        project.dev_cost = new_dev_cost
        if cost_diff > 0:
            self.track_expense("production", cost_diff)

        project.review = self.calculate_review(project, bugs=bugs)
        
        # Hype-Bonus berechnen und anwenden
        self.hype += self.calculate_hype(project)
        hype_multi = 1.0 + (self.hype / 100.0)
        new_sales = int(self.calculate_sales(project) * hype_multi)
        project.sales = getattr(project, "sales", 0) + new_sales

        if getattr(project, "is_f2p", False):
            project.active_players = getattr(project, "active_players", 0) + new_sales
            price = 0
        else:
            price = AUDIENCE_PRICE.get(project.audience, 30)
            
        total_revenue_new = int(new_sales * price * self.profit_multiplier)
        
        # Publisher Royalties
        publisher = ap_dict.get("publisher")
        
        if publisher:
            royalty_cut = int(total_revenue_new * publisher["royalty"])
            new_revenue = total_revenue_new - royalty_cut
            if not was_early_access:
                self.track_income("publishing", publisher["advance"])
        else:
            if "Digitaler Vertrieb & Logistik" in self.unlocked_technologies:
                distribution_margin = 0.15 
            else:
                distribution_margin = 0.30 
                
            dist_cost = int(total_revenue_new * distribution_margin)
            new_revenue = total_revenue_new - dist_cost
            if hasattr(project, "distribution_cost"):
                project.distribution_cost += dist_cost
            else:
                project.distribution_cost = dist_cost

        project.revenue = getattr(project, "revenue", 0) + new_revenue

        # Co-Dev aus dem AP-Dict
        if ap_dict.get("co_dev") and not was_early_access:
            partner = ap_dict["co_dev"]
            refund = int(new_dev_cost * 0.5)
            self.track_income("other", refund)
            project.revenue = int(project.revenue * 0.5)
            self.emails.insert(0, Email(
                sender=partner,
                subject=self.get_text('subject_co_dev', name=project.name),
                body=self.get_text('body_co_dev', refund=refund, revenue=project.revenue),
                date_week=self.week
            ))
            
        # Projekt aus Liste entfernen
        if not early_access:
            if ap_dict in self.active_projects:
                self.active_projects.remove(ap_dict)
            
        # Post-Game Logic
        self.co_dev_partner = None

        self.track_income("sales", new_revenue)
            
        # Fan-Gain durch Spiel und Lizenz
        fan_base_gain = int(new_revenue * 0.005 * (project.review.average / 10))
        if getattr(project, 'license_bonus', 0) > 0 and not was_early_access:
            fan_base_gain += int(project.license_bonus * 50)
        self.fans += fan_base_gain
        if not was_early_access:
            self.games_made += 1
        self.total_revenue += new_revenue

        # Moral-Anpassung nach Release
        for emp in self.employees:
            if project.review and project.review.average >= 7:
                emp.morale = min(100, emp.morale + 5)
            elif project.review and project.review.average < 4:
                emp.morale = max(0, emp.morale - 10)

        # Wenn es ein MMO ist, erstelle ActiveMMO Objekt
        if project.size == "MMO" and not was_early_access:
            # Initiale Spielerzahl basierend auf Hype und Review
            initial_players = int((project.review.average * 10000) * (1 + self.hype * 0.05))
            mmo = ActiveMMO(game_project=project, initial_players=initial_players)
            self.active_mmos.append(mmo)
        
        # Hype wird erst JETZT verbraucht, damit MMOs den Bonus noch mitnehmen
        self.hype = 0
        # IP-Rating berechnen (0-100 basierend auf Review)
        if project.review:
            avg = project.review.average
            project.ip_rating = int(min(100, max(0, (avg - 3) * 14.3)))  # 3→0, 10→100
        
        # Sub-Genre aus Draft übernehmen
        project.sub_genre = self.current_draft.get("sub_genre", None)

        if project not in self.game_history:
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
        self.track_expense("staff", train_data["cost"])
        
        if train_data.get("is_specialization"):

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

    def donate(self, amount):
        """Spendet einen Betrag an die Community/Wohltätigkeit."""
        if self.money >= amount:
            self.track_expense("other", amount)
            
            # Fan-Bonus: 1 Fan pro 100 EUR Spende, plus Bonus bei großen Beträgen
            fans_gained = int(amount / 100)
            if amount >= 10000: fans_gained = int(fans_gained * 1.2)
            if amount >= 100000: fans_gained = int(fans_gained * 1.5)
            
            self.fans += fans_gained
            return True, fans_gained
        return False, 0


    def watch_ad(self):
        """Simuliert das Ansehen einer Werbung gegen Belohnung."""
        # Cooldown: Nur einmal pro Woche möglich
        if self.week > self.last_ad_week:
            reward = 5000
            self.track_income("other", reward)
            self.last_ad_week = self.week
            return True, reward
        return False, 0


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
        self.emails.append(Email(
            sender=self.get_text('sender_intel'),
            subject=self.get_text('sender_intel'),
            body=f"{self.get_text('main_trend')} {self.current_trend['text']}",
            date_week=self.week
        ))

    # ==========================================================
    # NEU: v3.11.0-beta.1 Expansion Methods (Community & Hardware)
    # ==========================================================

    def get_accessibility_lab_actions(self):
        """Liefert die verfuegbaren Aktionen fuer das Barrierefreiheits-Labor."""
        return [
            {
                "id": "screenreader_test",
                "name_key": "access_lab_action_screenreader",
                "cost": 4000,
                "reputation": 5,
                "fans": 120,
                "hype": 1.0,
                "bug_reduction": 2,
                "quality_boost": 0.0,
                "quality_weeks": 0,
            },
            {
                "id": "audio_description",
                "name_key": "access_lab_action_audio_description",
                "cost": 9000,
                "reputation": 8,
                "fans": 260,
                "hype": 2.0,
                "bug_reduction": 1,
                "quality_boost": 0.03,
                "quality_weeks": 6,
            },
            {
                "id": "community_beta",
                "name_key": "access_lab_action_community_beta",
                "cost": 15000,
                "reputation": 12,
                "fans": 500,
                "hype": 4.0,
                "bug_reduction": 5,
                "quality_boost": 0.04,
                "quality_weeks": 4,
            },
        ]

    def get_accessibility_weekly_fans(self):
        """Berechnet den passiven woechentlichen Fan-Zuwachs."""
        rep = getattr(self, "accessibility_reputation", 0)
        if rep <= 0:
            return 0
        return min(800, max(1, int(rep * 1.5)))

    def update_accessibility_reputation(self):
        """Wendet den passiven Community-Effekt des Barrierefreiheits-Labors an."""
        weekly_fans = self.get_accessibility_weekly_fans()
        if weekly_fans > 0:
            self.fans += weekly_fans
        if self.active_projects and getattr(self, "accessibility_reputation", 0) >= 50:
            self.hype = min(250, self.hype + 0.1)

        rep = getattr(self, "accessibility_reputation", 0)
        current_year = self.get_calendar_year()
        if rep >= 40 and current_year > getattr(self, "last_accessibility_grant_year", 0):
            grant_amount = int(10000 + rep * 500)
            self.track_income("other", grant_amount)
            self.last_accessibility_grant_year = current_year
            self.emails.insert(0, Email(
                sender=self.get_text('sender_system'),
                subject=self.get_text('subject_access_grant'),
                body=self.get_text('body_access_grant', amount=grant_amount, score=rep),
                date_week=self.week
            ))
        return weekly_fans

    def run_accessibility_lab_action(self, action_id):
        """Fuehrt eine Aktion im Barrierefreiheits-Labor aus."""
        action = next((a for a in self.get_accessibility_lab_actions() if a["id"] == action_id), None)
        if not action:
            return False, "invalid"
        if self.money < action["cost"]:
            return False, "no_money"

        self.track_expense("research", action["cost"])
        self.accessibility_reputation = min(
            100,
            getattr(self, "accessibility_reputation", 0) + action["reputation"]
        )
        self.fans = max(0, self.fans + action["fans"])
        self.hype = min(250, self.hype + action["hype"])

        bug_reduction = action.get("bug_reduction", 0)
        if bug_reduction:
            for ap in self.active_projects:
                ap["bugs"] = max(0, ap.get("bugs", 0) - bug_reduction)

        if action.get("quality_boost", 0) > 0:
            self.temp_quality_boost = max(
                getattr(self, "temp_quality_boost", 0.0),
                action["quality_boost"]
            )
            self.temp_quality_weeks = max(
                getattr(self, "temp_quality_weeks", 0),
                action["quality_weeks"]
            )

        self.accessibility_lab_history.append({
            "week": self.week,
            "action_id": action["id"],
            "cost": action["cost"],
            "reputation": action["reputation"],
        })
        if hasattr(self, "_check_achievements"):
            self._check_achievements()
        return True, action

    def receive_fan_mail(self):
        """Generiert eine neue Fanpost mit Antwortoptionen."""

        from models import FanMail
        from game_data import FAN_MAIL_TEMPLATES
        
        # Chance basierend auf Fans und Hype
        chance = 0.10 + min(0.30, self.fans / 200000.0)
        if random.random() > chance:
            return False
            
        template = random.choice(FAN_MAIL_TEMPLATES)
        
        # Eindeutige ID vergeben
        mail_id = f"fanmail_{self.week}_{random.randint(1000, 9999)}"
        
        # Zufälliger Fan-Name
        fan_firstnames = ["Thomas", "Michael", "Andreas", "Christian", "Stefan", "Lukas", "Julia", "Sarah", "Laura", "Katharina"]
        fan_lastnames = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"]
        sender_name = f"{random.choice(fan_firstnames)} {random.choice(fan_lastnames)}"
        
        # FanMail erstellen
        mail = FanMail(
            mail_id=mail_id,
            sender=sender_name,
            subject_key=template["subject_key"],
            text_key=template["text_key"],
            options=template["options"]
        )
        self.fan_mail_inbox.append(mail)
        
        # E-Mail-Benachrichtigung an den Spieler
        self.emails.insert(0, Email(
            sender=sender_name,
            subject=self.get_text(template["subject_key"]),
            body=self.get_text(template["text_key"]),
            date_week=self.week
        ))
        
        # Audio-Feedback
        if hasattr(self, 'audio'):
            self.audio.play_sound('click')
            
        return True

    def answer_fan_mail(self, mail_id: str, option_idx: int) -> bool:
        """Beantwortet eine Fanpost und wendet die entsprechenden Effekte an."""
        mail = next((m for m in self.fan_mail_inbox if m.mail_id == mail_id), None)
        if not mail or mail.is_answered:
            return False
            
        if option_idx < 0 or option_idx >= len(mail.options):
            return False
            
        mail.is_answered = True
        mail.selected_option = option_idx
        mail.is_read = True
        
        option = mail.options[option_idx]
        effects = option.get("effects", option.get("value", {}))
        
        # Effekte anwenden
        # 1. Fans
        fans_diff = effects.get("fans", 0)
        self.fans = max(0, self.fans + fans_diff)
        
        # 2. Hype (auf alle aktiven Projekte addieren)
        hype_diff = effects.get("hype", 0.0)
        for ap in self.active_projects:
            if getattr(self, 'strike_weeks_left', 0) > 0:
                continue
            proj = ap["project"]
            proj.hype = max(0.0, proj.hype + hype_diff)
            
        # 3. Geld
        money_diff = effects.get("money", 0)
        if money_diff != 0:
            if money_diff > 0:
                self.track_income("other", money_diff)
            else:
                self.track_expense("other", abs(money_diff))
                
        return True

    def start_sound_card_project(self, name: str, features: list) -> bool:
        """Startet ein neues Soundkarten-Entwicklungsprojekt."""
        if self.get_calendar_year() < 1980:
            return False
            
        # Entwicklungskosten berechnen
        from game_data import HARDWARE_TECH_LIST
        dev_cost = 20000 # Grundkosten
        for tech_id in features:
            tech = next((t for t in HARDWARE_TECH_LIST if t["id"] == tech_id), None)
            if tech:
                dev_cost += tech["cost"]
                
        if self.money < dev_cost:
            return False
            
        self.track_expense("hardware", dev_cost)
        
        from models import SoundCardProject
        project = SoundCardProject(
            name=name,
            features=features,
            dev_cost=dev_cost,
            progress=0.0
        )
        self.sound_card_projects.append(project)
        return True

    def unlock_hardware_technology(self, tech_id: str) -> bool:
        """Schaltet eine Soundkarten-Technologie frei (Lizenzkauf)."""
        from game_data import HARDWARE_TECH_LIST
        tech = next((t for t in HARDWARE_TECH_LIST if t["id"] == tech_id), None)
        if not tech:
            return False
            
        if tech_id in self.unlocked_hardware_tech:
            return False
            
        # Jahr prüfen
        if self.get_calendar_year() < tech["year"]:
            return False
            
        if self.money < tech["cost"]:
            return False
            
        self.track_expense("hardware", tech["cost"])
        self.unlocked_hardware_tech.append(tech_id)
        return True

    def update_hardware_development(self):
        """Aktualisiert wöchentlich den Entwicklungsfortschritt von Soundkarten."""
        # Nur ein unfertiges Projekt kann gleichzeitig entwickelt werden
        active_proj = next((p for p in self.sound_card_projects if not p.is_released), None)
        if not active_proj:
            return
            
        # Fortschrittsgeschwindigkeit
        active_emps = self._active_employees()
        if active_emps:
            avg_speed = sum(e.speed for e in active_emps) / len(active_emps)
        else:
            avg_speed = 30.0 # Standard
            
        # Jede Woche ca. 8% bis 15% Fortschritt basierend auf Mitarbeitern
        prog_inc = 5.0 + (avg_speed / 10.0)
        active_proj.progress = min(100.0, active_proj.progress + prog_inc)

    def release_sound_card(self, card_name: str) -> bool:
        """Veröffentlicht eine fertig entwickelte Soundkarte."""
        card = next((p for p in self.sound_card_projects if p.name == card_name and not p.is_released), None)
        if not card or card.progress < 100.0:
            return False
            
        card.is_released = True
        card.weeks_on_market = 0
        
        # Vorherige Karten verlieren an Marktanteil, wenn eine neue veröffentlicht wird
        for other_card in self.sound_card_projects:
            if other_card.is_released and other_card.name != card_name:
                other_card.market_share *= 0.5
                
        return True

    def create_radio_jingle(self, name: str, music_track: str, voice_style: str, sfx: str) -> bool:
        """Produziert ein neues Radio-Jingle zur Marketing-Unterstützung."""
        # Kosten berechnen
        cost = 5000 # Basiskosten
        if music_track != "none": cost += 2000
        if voice_style != "none": cost += 1500
        if sfx != "none": cost += 1000
        
        if self.money < cost:
            return False
            
        self.track_expense("marketing", cost)
        
        # Hype Bonus berechnen
        hype_bonus = 5.0
        if music_track != "none": hype_bonus += 3.0
        if voice_style != "none": hype_bonus += 2.0
        if sfx != "none": hype_bonus += 2.0
        
        from models import RadioJingle
        jingle = RadioJingle(
            name=name,
            music_track=music_track,
            voice_style=voice_style,
            sfx=sfx,
            hype_bonus=hype_bonus,
            cost=cost
        )
        jingle.weeks_left = 4
        self.active_jingles.append(jingle)
        
        # Hype auf alle aktiven Spiele anwenden
        for ap in self.active_projects:
            if getattr(self, 'strike_weeks_left', 0) > 0:
                continue
            proj = ap["project"]
            proj.hype = max(0.0, proj.hype + hype_bonus)
            
        return True

    def trigger_personality_event(self) -> bool:
        """Prüft und triggert wöchentlich Büro-Events basierend auf Mitarbeiter-Persönlichkeiten."""
        if getattr(self, "active_personality_event", None) is not None:
            return False
            
        # 10% Chance pro Woche

        if random.random() > 0.10:
            return False
            
        if not self.employees:
            return False
            
        # Vorhandene Persönlichkeiten im Team ermitteln
        team_personalities = [e.personality for e in self.employees if getattr(e, "personality", None)]
        if not team_personalities:
            return False
            
        from game_data import OFFICE_PERSONALITY_EVENTS
        eligible_events = []
        for event in OFFICE_PERSONALITY_EVENTS:
            req = event["personality_required"]
            if req in team_personalities:
                eligible_events.append(event)
                
        if not eligible_events:
            return False
            
        chosen_event = random.choice(eligible_events)
        
        # Finde einen passenden Mitarbeiter als Hauptakteur des Events
        protagonist = next((e for e in self.employees if getattr(e, "personality", None) == chosen_event["personality_required"]), self.employees[0])
        
        self.active_personality_event = chosen_event
        self.active_personality_employee = protagonist
        
        # Benachrichtigungs-Email senden
        self.emails.insert(0, Email(
            sender=protagonist.name,
            subject=self.get_text("subject_office_event"),
            body=self.get_text("body_office_event", name=protagonist.name),
            date_week=self.week
        ))
        
        if hasattr(self, 'audio'):
            self.audio.play_sound('warn')
            
        return True

    def answer_personality_event(self, option_idx: int) -> bool:
        """Beantwortet das aktive Büro-Event und wendet Effekte an."""
        event = getattr(self, "active_personality_event", None)
        if not event:
            return False
            
        if option_idx < 0 or option_idx >= len(event["options"]):
            return False
            
        option = event["options"][option_idx]
        effects = option.get("effects", {})
        
        # 1. Moral der Mitarbeiter
        morale_diff = effects.get("morale", 0)
        if morale_diff != 0:
            protagonist = getattr(self, "active_personality_employee", None)
            if protagonist:
                protagonist.morale = max(0, min(100, protagonist.morale + morale_diff))
            else:
                for emp in self.employees:
                    emp.morale = max(0, min(100, emp.morale + morale_diff))
                    
        # 2. Geld
        money_diff = effects.get("money", 0)
        if money_diff != 0:
            if money_diff > 0:
                self.track_income("other", money_diff)
            else:
                self.track_expense("other", abs(money_diff))
                
        # 3. Hype
        hype_diff = effects.get("hype", 0.0)
        if hype_diff != 0.0:
            for ap in self.active_projects:
                ap["project"].hype = max(0.0, ap["project"].hype + hype_diff)
                
        # 4. Fans
        fans_diff = effects.get("fans", 0)
        if fans_diff != 0:
            self.fans = max(0, self.fans + fans_diff)
            
        # 5. Spezielle temporäre Modifikatoren
        if "dev_speed_penalty" in effects:
            self.temp_dev_speed_penalty = effects["dev_speed_penalty"]
            self.temp_dev_speed_weeks = 4
            
        if "quality_boost" in effects:
            self.temp_quality_boost = effects["quality_boost"]
            self.temp_quality_weeks = 4
            
        # Event zurücksetzen
        self.active_personality_event = None
        self.active_personality_employee = None
        return True

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
            "port_projects": [p.to_dict() for p in getattr(self, "port_projects", [])],
            "employees": [e.to_dict() for e in self.employees],
            "engines": [
                {"name": eng.name, "is_licensed": eng.is_licensed, "license_fee": eng.license_fee, "features": [
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
            "unlocked_platforms": getattr(self, "unlocked_platforms", []),
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
            "office_items": getattr(self, "office_items", []),
            "office_objects": [(obj.to_dict() if hasattr(obj, 'to_dict') else obj) for obj in getattr(self, "office_objects", [])],
            "active_projects": [
                {
                    "project": ap["project"].to_dict(),
                    "progress": ap["progress"],
                    "total_weeks": ap["total_weeks"],
                    "bugs": ap["bugs"],
                    "crunch": ap.get("crunch", False),
                    "ready_to_finish": ap.get("ready_to_finish", False),
                    "event_count": ap.get("event_count", 0),
                    "aaa_event_done": ap.get("aaa_event_done", False),
                    "co_dev": ap.get("co_dev")
                } for ap in self.active_projects
            ],
            "soundcon_history": [s.to_dict() for s in getattr(self, "soundcon_history", [])],
            "soundcon_last_year": getattr(self, "soundcon_last_year", 0),
            "active_soundcon": self.active_soundcon.to_dict() if getattr(self, "active_soundcon", None) else None,
            "pending_soundcon_result": getattr(self, "pending_soundcon_result", None),
            "soundtrack_label": self.soundtrack_label.to_dict() if getattr(self, "soundtrack_label", None) else None,
            "fan_mail_inbox": [m.to_dict() for m in getattr(self, "fan_mail_inbox", [])],
            "sound_card_projects": [p.to_dict() for p in getattr(self, "sound_card_projects", [])],
            "active_jingles": [{"jingle": j.to_dict(), "weeks_left": getattr(j, "weeks_left", 4)} for j in getattr(self, "active_jingles", [])],
            "unlocked_hardware_tech": getattr(self, "unlocked_hardware_tech", []),
            "active_personality_event": getattr(self, "active_personality_event", None),
            "active_personality_employee_name": self.active_personality_employee.name if getattr(self, "active_personality_employee", None) else None,
            "temp_dev_speed_penalty": getattr(self, "temp_dev_speed_penalty", 1.0),
            "temp_dev_speed_weeks": getattr(self, "temp_dev_speed_weeks", 0),
            "temp_quality_boost": getattr(self, "temp_quality_boost", 0.0),
            "temp_quality_weeks": getattr(self, "temp_quality_weeks", 0),
            "accessibility_reputation": getattr(self, "accessibility_reputation", 0),
            "accessibility_lab_history": getattr(self, "accessibility_lab_history", []),
            "last_accessibility_grant_year": getattr(self, "last_accessibility_grant_year", 0),
            "unlocked_achievements": getattr(self, "unlocked_achievements", []),
            "my_goty_wins": getattr(self, "my_goty_wins", 0)
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
            for od in data["publishing_offers"]:
                self.publishing_offers.append(PublishingOffer(
                    od["studio_name"], od["game_name"], od["genre"], od["quality"], od["marketing_cost"], od["player_share"]
                ))

        self.published_third_party_games = []
        if "published_third_party_games" in data:
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
            eng = Engine(ed["name"], features)
            eng.is_licensed = ed.get("is_licensed", False)
            eng.license_fee = ed.get("license_fee", 0)
            self.engines.append(eng)

        # Spielhistorie laden
        self.game_history = []
        for gd in data.get("game_history", []):
            self.game_history.append(GameProject.from_dict(gd))

        # Aktive MMOs laden
        self.active_mmos = []
        if "active_mmos" in data:
            for md in data["active_mmos"]:
                match_game = next((g for g in self.game_history if g.name == md.get("game_dict", {}).get("name")), None)
                if match_game:
                    m = ActiveMMO(match_game, md.get("players", 0), md.get("payment_model", "Abo"))
                    m.subscription_fee = md.get("subscription_fee", 15)
                    m.server_cost_per_10k = md.get("server_cost_per_10k", 5000)
                    m.weeks_active = md.get("weeks_active", 0)
                    self.active_mmos.append(m)

        self.port_projects = []
        if "port_projects" in data:
            from models import PortProject
            for pd in data["port_projects"]:
                port = PortProject(pd["original_game_name"], pd["new_platform"], pd["dev_cost"], pd["total_weeks"])
                port.progress = pd.get("progress", 0.0)
                port.is_finished = pd.get("is_finished", False)
                self.port_projects.append(port)

        # Mitarbeiter laden
        self.employees = []
        for ed in data.get("employees", []):
            emp = Employee.from_dict(ed)
            # Falls Trait fehlt (Migration), zufällig zuweisen
            if not emp.trait:

                from game_data import EMPLOYEE_TRAITS
                emp.trait = random.choice(EMPLOYEE_TRAITS)
            self.employees.append(emp)

        # E-Mails laden
        self.emails = []
        for md in data.get("emails", []):
            mail = Email(md["sender"], md["subject"], md["body"], md["date_week"], md.get("game_name"), md.get("is_bug", False))
            mail.is_read = md.get("is_read", False)
            self.emails.append(mail)

        self.settings = data.get("settings", {"language": "de", "music_enabled": True})

        # Rivalen laden
        # Aktive Projekte laden
        self.active_projects = []
        for ad in data.get("active_projects", []):
            if ad.get("is_contract"):
                from models import ContractWorkProject
                proj = ContractWorkProject.from_dict(ad["project"])
            else:
                from models import GameProject
                proj = GameProject.from_dict(ad["project"])
            
            self.active_projects.append({
                "project": proj,
                "progress": ad["progress"],
                "total_weeks": ad["total_weeks"],
                "bugs": ad.get("bugs", 0),
                "crunch": ad.get("crunch", False),
                "ready_to_finish": ad.get("ready_to_finish", False),
                "event_count": ad.get("event_count", 0),
                "aaa_event_done": ad.get("aaa_event_done", False),
                "co_dev": ad.get("co_dev")
            })
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
        self.unlocked_platforms = data.get("unlocked_platforms", [])
        
        # Finanzen laden
        self.accounting = data.get("accounting", {"income": 0, "expenses": 0, "loan_paid": 0})
        loan_data = data.get("bank_loan")
        if loan_data:
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
            for c_data in data["custom_consoles"]:
                cc = CustomConsole(c_data["name"], c_data["tech_level"], c_data["dev_cost"], c_data["release_week"])
                cc.market_share = c_data.get("market_share", 0.05)
                self.custom_consoles.append(cc)

        # Büro laden & Migrieren
        self.office_items = data.get("office_items", [])
        self.office_objects = []
        
        # Versuche office_objects direkt zu laden
        objects_data = data.get("office_objects")
        if objects_data:
            from models import OfficeObject
            for od in objects_data:
                if isinstance(od, dict) and "object_type" in od:
                    self.office_objects.append(OfficeObject.from_dict(od))
                else:
                    self.office_objects.append(od)
        
        self.office_grid = [[None for _ in range(10)] for _ in range(10)]
        
        # Falls office_objects leer war aber office_items existiert (Migration)
        if not self.office_objects and self.office_items:
            from models import OfficeObject
            for item in self.office_items:
                if isinstance(item, dict):
                    y, x = item.get("y", 0), item.get("x", 0)
                    new_obj = OfficeObject(item.get("type", "Desk"), x, y, level=item.get("level", 1))
                    self.office_objects.append(new_obj)
        
        # Grid aus office_objects aufbauen
        for obj in self.office_objects:
            if not hasattr(obj, 'y') or not hasattr(obj, 'x'):
                continue
            y, x = obj.y, obj.x
            if 0 <= y < len(self.office_grid) and 0 <= x < len(self.office_grid[0]):
                self.office_grid[y][x] = obj

        # NEU: SoundCon & Soundtrack-Label laden
        self.soundcon_history = []
        if "soundcon_history" in data:
            for sd in data["soundcon_history"]:
                self.soundcon_history.append(SoundConEvent.from_dict(sd))
        self.soundcon_last_year = data.get("soundcon_last_year", 0)
        
        active_sc = data.get("active_soundcon")
        self.active_soundcon = SoundConEvent.from_dict(active_sc) if active_sc else None
        self.pending_soundcon_result = data.get("pending_soundcon_result")

        label_data = data.get("soundtrack_label")
        self.soundtrack_label = SoundtrackLabel.from_dict(label_data) if label_data else None

        # NEU: v3.11.0-beta.1 Expansion Variables laden
        from models import FanMail, SoundCardProject, RadioJingle
        
        self.fan_mail_inbox = []
        for md in data.get("fan_mail_inbox", []):
            self.fan_mail_inbox.append(FanMail.from_dict(md))
            
        self.sound_card_projects = []
        for pd in data.get("sound_card_projects", []):
            self.sound_card_projects.append(SoundCardProject.from_dict(pd))
            
        self.active_jingles = []
        for jd in data.get("active_jingles", []):
            j = RadioJingle.from_dict(jd["jingle"])
            j.weeks_left = jd.get("weeks_left", 4)
            self.active_jingles.append(j)
            
        self.unlocked_hardware_tech = data.get("unlocked_hardware_tech", [])
        self.active_personality_event = data.get("active_personality_event", None)
        
        emp_name = data.get("active_personality_employee_name")
        if emp_name:
            self.active_personality_employee = next((e for e in self.employees if e.name == emp_name), None)
            if not self.active_personality_employee and self.employees:
                self.active_personality_employee = self.employees[0]
        else:
            self.active_personality_employee = None
            
        self.temp_dev_speed_penalty = data.get("temp_dev_speed_penalty", 1.0)
        self.temp_dev_speed_weeks = data.get("temp_dev_speed_weeks", 0)
        self.temp_quality_boost = data.get("temp_quality_boost", 0.0)
        self.temp_quality_weeks = data.get("temp_quality_weeks", 0)
        self.accessibility_reputation = data.get("accessibility_reputation", 0)
        self.accessibility_lab_history = data.get("accessibility_lab_history", [])
        self.last_accessibility_grant_year = data.get("last_accessibility_grant_year", 0)
        self.unlocked_achievements = data.get("unlocked_achievements", [])
        self.my_goty_wins = data.get("my_goty_wins", 0)

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

            self.track_expense("production", total_cost)
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
            self.track_expense("mmo", cost)
            self.has_server_room = True
            self.server_capacity = 50000
            return True
        return False
        
    def expand_server_capacity(self):
        """Erweitert Serverkapazität um 50.000 Spieler."""
        cost = 250000
        if self.money >= cost and getattr(self, "has_server_room", False):
            self.track_expense("mmo", cost)
            self.server_capacity += 50000
            return True
        return False
        
    def apply_mmo_update(self, active_mmo_idx, cost=500000, player_boost=0.2):
        """Veröffentlicht ein Content-Update für ein aktives MMO."""
        if 0 <= active_mmo_idx < len(getattr(self, "active_mmos", [])):
            if self.money >= cost:
                self.track_expense("mmo", cost)
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
        from game_data import START_TOPICS, START_GENRES
        
        studios = ["Pixel Wizards", "Neon Interactive", "Bitforge Studios", "Quantum Games", "Hyperion Soft"]
        words = ["Quest", "Saga", "Chronicles", "World", "Strike", "Legends", "Simulator", "Manager"]
        
        studio = random.choice(studios)
        game_topic = random.choice(list(START_TOPICS))
        game_genre = random.choice(list(START_GENRES))
        game_name = f"{self.get_text(game_topic)} {random.choice(words)}"
        
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
        msg = self.get_text('publisher_deal_info_email', studio=studio, game=game_name, quality=quality, cost=marketing_cost, share=int(player_share*100))
        self.emails.append(Email(
            sender=self.get_text('sender_headhunter'), 
            subject=self.get_text('publisher_deals_title'), 
            body=msg, 
            date_week=self.week, 
            is_bug=False
        ))

    def accept_publishing_offer(self, idx):
        """Akzeptiert ein Angebot und startet den Verkauf."""
        if not hasattr(self, "publishing_offers") or idx < 0 or idx >= len(self.publishing_offers):
            return False, "invalid_offer"
            
        offer = self.publishing_offers[idx]
        if self.money < offer.marketing_cost:
            return False, "not_enough_money"
            
        self.track_expense("marketing", offer.marketing_cost)
             
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
            
        self.track_expense("production", cost)
        self.has_presswerk = True
        self.storage_capacity = 50000 # Startkapazität
        return True, "success"

    def expand_storage(self):
        """Erweitert das Lager um 100.000 Einheiten für 100.000 Euro."""
        cost = 100000
        if not self.has_presswerk:
            return False, "no_presswerk"
        if self.money < cost:
            return False, "no_money"
            
        self.track_expense("production", cost)
        self.storage_capacity += 100000
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
            
        self.track_expense("production", total_cost)
        game.physical_copies = getattr(game, "physical_copies", 0) + amount
        # Wir setzen den Retail-Preis auf 45 Euro, falls nicht vorhanden
        if not hasattr(game, "physical_price"):
            game.physical_price = 45
            
        self.used_storage += amount
        return True, "success"
            
        return True, "success"

    def perform_teambuilding(self, action_type="Pizza"):
        """Führt eine Team-Building Maßnahme durch."""
        costs = {"Pizza": 500, "Ausflug": 5000, "Party": 2000}
        morale_boost = {"Pizza": 5, "Ausflug": 25, "Party": 15}
        
        cost = costs.get(action_type, 1000)
        if self.money >= cost:
            self.track_expense("staff", cost)
            boost = morale_boost.get(action_type, 10)
            for emp in self.employees:
                emp.morale = min(100, emp.morale + boost)
            return True
        return False

    def start_training(self, emp_idx, training_option):
        """Startet eine Fortbildung für einen Mitarbeiter (Phase 2)."""
        if not (0 <= emp_idx < len(self.employees)):
            return False, "invalid_employee"
        
        emp = self.employees[emp_idx]
        
        if getattr(emp, 'is_training', False):
            return False, "already_training"
        if getattr(emp, 'is_sick', False):
            return False, "is_sick"
        
        cost = training_option.get("cost", 0)
        if self.money < cost:
            return False, "no_money"
        
        self.track_expense("staff", cost)
        
        lock_weeks = training_option.get("lock_weeks", 1)
        skill_boost = training_option.get("skill_boost", 0)
        is_spec = training_option.get("is_specialization", False)
        
        emp.is_training = True
        emp.training_weeks_left = lock_weeks
        emp.training_skill_boost = skill_boost
        
        # Spezialisierungskurs: Sofort eine zufällige freie Spezialisierung vergeben
        if is_spec:
            from game_data import EMPLOYEE_SPECIALIZATIONS

            current_spec = getattr(emp, 'specialization', None)
            if current_spec:
                spec_name = current_spec.get("name")
            else:
                spec_name = None
            free_specs = [s for s in EMPLOYEE_SPECIALIZATIONS if s["name"] != spec_name]
            if free_specs:
                emp.specialization = random.choice(free_specs)
        
        return True, lock_weeks



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
        self.track_expense("other", cost)
            
        # Place
        item_data = {
            "type": item_type,
            "x": x,
            "y": y,
            "width": 1,
            "height": 1,
            "employees": obj_def.get("employees", 0)
        }
        from models import OfficeObject
        obj = OfficeObject.from_dict({"object_type": item_type, "x": x, "y": y, "level": 1})
        
        if not hasattr(self, "office_items"): self.office_items = []
        if not hasattr(self, "office_objects"): self.office_objects = []
        
        self.office_items.append(item_data)
        self.office_objects.append(obj)
        self.office_grid[y][x] = obj
                
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
        if item in self.office_items:
            self.office_items.remove(item)
        
        # Also remove from office_objects if it's an OfficeObject or find the matching one
        if hasattr(self, "office_objects"):
            to_remove = None
            for obj in self.office_objects:
                if obj.x == x and obj.y == y:
                    to_remove = obj
                    break
            if to_remove:
                self.office_objects.remove(to_remove)
                
        self.office_grid[y][x] = None
        
        # Refund 50%
        from game_data import BUILD_OBJECTS
        obj_def = BUILD_OBJECTS.get(item.get("type"), {})
        self.track_income("other", obj_def.get("cost", 0) * 0.5)
        
        return True

    def get_office_item(self, x, y):
        return self.office_grid[y][x]

    def _check_achievements(self):
        """Prüft ob neue Meilensteine erreicht wurden."""
        from game_data import ACHIEVEMENTS
        
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
            elif ach["type"] == "accessibility":
                if getattr(self, "accessibility_reputation", 0) >= ach["threshold"]:
                    unlocked = True
                    
            if unlocked:
                self.unlocked_achievements.append(ach["id"])
                
                # Bonus anwenden
                bonus_str = ""
                if ach["bonus_type"] == "fans":
                    self.fans += ach["bonus_value"]
                    bonus_str = f"+{ach['bonus_value']:,} Fans"
                elif ach["bonus_type"] == "money":
                    self.track_income("other", ach["bonus_value"])
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
                
                # Audio-Feedback
                if hasattr(self, "audio") and self.audio:
                    self.audio.play_sound("achievement.wav") # Sound falls vorhanden
                    self.audio.speak(f"Meilenstein erreicht: {title}. {desc}", interrupt=False)

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

    def track_income(self, category, amount):
        """Trackt Einnahmen in einer Kategorie."""
        if not hasattr(self, "current_week_balance"):
            self.money += amount
            return
        if category in self.current_week_balance["income"]:
            self.current_week_balance["income"][category] += amount
        else:
            self.current_week_balance["income"]["other"] += amount
        self.money += amount
        if hasattr(self, "accounting"):
            self.accounting["income"] += amount
        
        # NEU: Monatliche Verfolgung
        self.accrued_income[category] = self.accrued_income.get(category, 0) + amount

    def track_expense(self, category, amount):
        """Trackt Ausgaben in einer Kategorie."""
        if not hasattr(self, "current_week_balance"):
            self.money -= amount
            return
        if category in self.current_week_balance["expenses"]:
            self.current_week_balance["expenses"][category] += amount
        else:
            self.current_week_balance["expenses"]["other"] += amount
        self.money -= amount
        if hasattr(self, "accounting"):
            self.accounting["expenses"] += amount

        # NEU: Monatliche Verfolgung
        self.accrued_expenses[category] = self.accrued_expenses.get(category, 0) + amount

    def finalize_weekly_balance(self):
        """Speichert die aktuelle Wochenbilanz in die Historie und setzt sie zurück."""
        if not hasattr(self, "current_week_balance"): return
        
        total_income = sum(self.current_week_balance["income"].values())
        total_expenses = sum(self.current_week_balance["expenses"].values())
        
        balance_entry = {
            "week": self.week,
            "income": self.current_week_balance["income"].copy(),
            "expenses": self.current_week_balance["expenses"].copy(),
            "total_income": total_income,
            "total_expenses": total_expenses,
            "profit": total_income - total_expenses
        }
        if not hasattr(self, "financial_history"): self.financial_history = []
        self.financial_history.append(balance_entry)
        
        if len(self.financial_history) > 200:
            self.financial_history.pop(0)
            
        # Reset für neue Woche
        self.current_week_balance = {
            "income": {k: 0 for k in self.current_week_balance["income"]},
            "expenses": {k: 0 for k in self.current_week_balance["expenses"]}
        }

    def _process_engine_licensing(self):
        """Berechnet wöchentliche Lizenzeinnahmen aus lizenzierten Engines."""
        for eng in getattr(self, "engines", []):
            if getattr(eng, "is_licensed", False):
                fee = getattr(eng, "license_fee", 0)
                if fee > 0:
                    optimal_fee = max(1, eng.tech_level * 10)
                    demand = max(0, 100 - ((fee / optimal_fee) * 50))
                    income = int(demand * fee)
                    if income > 0:
                        self.track_income("engine_license", income)

    def _process_port_projects(self):
        """Verarbeitet aktive Portierungs-Projekte."""
        if not hasattr(self, "port_projects"):
            self.port_projects = []
            
        for port in list(self.port_projects):
            if not port.is_finished:
                # Calculate progress based on employees
                progress_gain = 0.0
                for emp in self.employees:
                    if emp.morale > 0 and not getattr(emp, "is_training", False) and not getattr(emp, "is_sick", False):
                        progress_gain += emp.speed / 1000.0  # arbitrary scale
                
                port.progress += progress_gain
                
                if port.progress >= 1.0:
                    port.progress = 1.0
                    port.is_finished = True
                    self.port_projects.remove(port)
                    # Create new game project based on original game
                    orig = next((g for g in self.game_history if g.name == port.original_game_name), None)
                    if orig:
                        from models import GameProject, ReviewScore
                        new_name = f"{orig.name} ({port.new_platform})"
                        new_game = GameProject(new_name, orig.topic, orig.genre, orig.sliders, port.new_platform, orig.audience, orig.engine, orig.size, orig.marketing)
                        new_game.review = ReviewScore([min(10, s + random.randint(-1, 1)) for s in orig.review.scores])
                        new_game.sales = 0
                        new_game.revenue = 0
                        new_game.dev_cost = port.dev_cost
                        new_game.week_developed = self.week
                        self.game_history.append(new_game)
                        self.emails.insert(0, Email(
                            sender="System",
                            subject="Portierung abgeschlossen",
                            body=f"Das Spiel {port.original_game_name} wurde erfolgreich auf {port.new_platform} portiert und veröffentlicht!",
                            date_week=self.week
                        ))
                        if hasattr(self, "audio"):
                            self.audio.speak(f"Portierung von {port.original_game_name} auf {port.new_platform} abgeschlossen.")

    def update_subscription_service(self):
        """Aktualisiert den Abo-Dienst (Abonnenten-Wachstum, Einnahmen, Kosten)."""
        if not getattr(self, "subscription_active", False):
            if hasattr(self, "subscription_subscribers"):
                self.subscription_subscribers = 0
            return

        # 1. Wachstum berechnen
        # Basis-Interesse (Hype hilft extrem)
        growth_base = (self.hype * 50) + 100
        
        # Preis-Effekt: 9.99 ist Standard. 
        price_factor = 1.0
        if self.subscription_price > 15.0:
            price_factor = 0.5
        if self.subscription_price > 20.0:
            price_factor = -0.05 # Leichter Verlust bei Wucherpreisen
        if self.subscription_price < 7.0:
            price_factor = 1.5
            
        # Bibliotheks-Effekt (Anzahl der Spiele im Abo)
        game_count = len(getattr(self, "subscription_games", []))
        library_factor = 0.5 + (game_count * 0.1) # 5 Spiele = 1.0 (normal)
        
        # Zufällige Fluktuation

        drift = random.uniform(0.95, 1.05)
        
        # Abonnenten-Änderung (Wachstum oder Schrumpfen)
        change = int(growth_base * price_factor * library_factor * drift)
        
        # Falls keine Spiele im Abo sind, verliert man massiv Leute
        if game_count == 0:
            change = -int(self.subscription_subscribers * 0.2) - 50
            
        self.subscription_subscribers = max(0, self.subscription_subscribers + change)
        
        # 2. Finanzen
        # Einnahmen (wöchentlich ca. 1/4 des Monatspreises)
        income = int(self.subscription_subscribers * (self.subscription_price / 4))
        if income > 0:
            self.track_income("subscription", income)
            
        # Serverkosten (0.05€ pro Abonnent pro Woche + Grundgebühr pro Spiel)
        server_costs = int(self.subscription_subscribers * 0.05) + (game_count * 200)
        if server_costs > 0:
            self.track_expense("server_costs", server_costs)

    def get_financial_report(self):
        """Gibt einen Bericht über die Finanzen der letzten Woche aus."""
        if not self.financial_history:
            return self.get_text('no_finances_yet')
            
        last = self.financial_history[-1]
        
        # Einnahmen Details
        inc_parts = []
        for cat, val in last["income"].items():
            if val > 0:
                inc_parts.append(f"{self.get_text('finance_' + cat)}: {val:,.0f} €")
        
        # Ausgaben Details
        exp_parts = []
        for cat, val in last["expenses"].items():
            if val > 0:
                exp_parts.append(f"{self.get_text('finance_' + cat)}: {val:,.0f} €")
                
        report = [
            f"--- {self.get_text('finance_report_title')} ({self.get_text('calendar_week')} {last['week']}) ---",
            f"{self.get_text('finance_total_income')}: {last['total_income']:,.0f} €",
            ". ".join(inc_parts) if inc_parts else self.get_text('none'),
            f"{self.get_text('finance_total_expenses')}: {last['total_expenses']:,.0f} €",
            ". ".join(exp_parts) if exp_parts else self.get_text('none'),
            f"{self.get_text('finance_net_profit')}: {last['profit']:,.0f} €",
            f"--- {self.get_text('current_balance')}: {self.money:,.0f} € ---"
        ]
        return "\n".join(report)

    def get_yearly_report(self):
        """Generiert eine Zusammenfassung des vergangenen Spieljahres."""
        from game_data import WEEKS_PER_YEAR, START_YEAR
        if not hasattr(self, "financial_history") or not self.financial_history:
            return self.get_text('no_finances_yet')
            
        if len(self.financial_history) < WEEKS_PER_YEAR:
            history = self.financial_history
        else:
            history = self.financial_history[-WEEKS_PER_YEAR:]
            
        total_inc = sum(w["total_income"] for w in history)
        total_exp = sum(w["total_expenses"] for w in history)
        profit = total_inc - total_exp
        
        # Meistverkauftes Spiel in diesem Jahr
        year_start_week = self.week - WEEKS_PER_YEAR
        year_games = [g for g in self.game_history if g.week_developed >= year_start_week]
        best_game = max(year_games, key=lambda g: g.sales) if year_games else None
        
        report = [
            f"--- {self.get_text('yearly_report_title', year=self.week // WEEKS_PER_YEAR + START_YEAR - 1)} ---",
            f"{self.get_text('finance_total_income')}: {total_inc:,.0f} €",
            f"{self.get_text('finance_total_expenses')}: {total_exp:,.0f} €",
            f"{self.get_text('finance_net_profit')}: {profit:,.0f} €",
        ]
        
        if best_game:
            report.append(f"{self.get_text('yearly_best_game')}: {best_game.name} ({best_game.sales:,} {self.get_text('sales')})")
        
        return "\n".join(report)


    def _send_monthly_bank_statement(self):
        """Generiert und speichert einen monatlichen Kontoauszug."""
        import game_data
        year = (self.week - 1) // game_data.WEEKS_PER_YEAR + game_data.START_YEAR
        # Dynamische Monatsberechnung (1 bis 12)
        month_index = int(((self.week - 1) % game_data.WEEKS_PER_YEAR) * 12 / game_data.WEEKS_PER_YEAR) + 1
        
        # NEU: Steuern berechnen (vom monatlichen Gewinn)
        taxes = 0
        total_income = sum(self.accrued_income.values())
        total_expense = sum(self.accrued_expenses.values())
        profit = total_income - total_expense
        if profit > 0:
            taxes = int(profit * self.tax_rate)
            self.track_expense("taxes", taxes)
            
        statement = BankStatement(
            week=self.week,
            year=year,
            income_items=self.accrued_income.copy(),
            expense_items=self.accrued_expenses.copy(),
            final_balance=self.money
        )
        
        self.bank_statements.insert(0, statement)
        
        # Reset accrued data for next month
        self.accrued_income = {}
        self.accrued_expenses = {}
        
        # Email senden
        cal = self.get_calendar_text()
        body_lines = [
            f"{self.get_text('monthly_statement_period')}: {cal}",
            "",
            f"{self.get_text('finance_total_income')}: {statement.total_income:,.0f} EUR",
        ]
        for cat, val in statement.income_items.items():
            if val > 0:
                body_lines.append(f"  + {self.get_text('finance_' + cat)}: {val:,.0f} EUR")
        
        body_lines.append("")
        body_lines.append(f"{self.get_text('finance_total_expenses')}: {statement.total_expense:,.0f} EUR")
        for cat, val in statement.expense_items.items():
            if val > 0:
                body_lines.append(f"  - {self.get_text('finance_' + cat)}: {val:,.0f} EUR")
                
        profit = statement.total_income - statement.total_expense
        sign = "+" if profit >= 0 else ""
        body_lines.extend([
            "",
            f"{self.get_text('finance_net_profit')}: {sign}{profit:,.0f} EUR",
            f"{self.get_text('current_balance')}: {self.money:,.0f} EUR",
        ])
        
        self.emails.insert(0, Email(
            sender=self.get_text("sender_bank"),
            subject=self.get_text("subject_monthly_statement", date=cal),
            body="\n".join(body_lines),
            date_week=self.week
        ))

    def _finish_update_project(self, update):
        """Wendet die Effekte eines fertigen Updates/DLCs an."""
        game = next((g for g in self.game_history if g.name == update.base_game_name), None)
        if not game: return
        
        game.updates.append(update)
        
        if update.update_type == "Patch":
            bugs_to_fix = int(game.bugs * 0.5) + 1
            game.bugs = max(0, game.bugs - bugs_to_fix)
            game.total_bugs_fixed += bugs_to_fix
        elif update_type == "Content":
            self.fans += 500
            self.hype = min(100, self.hype + 20)
        elif update_type == "Language":
            for l in update.languages:
                if l not in game.languages:
                    game.languages.append(l)
                    
        self.emails.insert(0, Email(
            sender=self.get_text('sender_dev'),
            subject=self.get_text('subject_update_finished', name=update.name),
            body=self.get_text('body_update_finished', game=game.name, type=update.update_type),
            date_week=self.week
        ))

    def place_office_room(self, x1, y1, x2, y2, room_type):
        """Platziert einen Raum im Büro-Raster."""
        from game_data import OFFICE_ROOM_TYPES
        room_data = next((r for r in OFFICE_ROOM_TYPES if r["id"] == room_type), None)
        if not room_data: return False
        
        width = x2 - x1 + 1
        height = y2 - y1 + 1
        cost = width * height * room_data["cost_per_tile"]
        
        if self.money < cost: return False
        
        # Check if area is within grid
        if x1 < 0 or y1 < 0 or x2 >= len(self.office_grid) or y2 >= len(self.office_grid[0]):
            return False
            
        self.track_expense("other", cost)
        
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.office_grid[x][y] = room_type
        return True

    def buy_office_furniture(self, x, y, item_id):
        """Kauft ein Möbelstück und platziert es."""
        from game_data import FURNITURE_DATA
        item_data = next((f for f in FURNITURE_DATA if f["id"] == item_id), None)
        if not item_data: return False
        
        if self.money < item_data["cost"]: return False
        
        # Check grid
        if x < 0 or x >= len(self.office_grid) or y < 0 or y >= len(self.office_grid[0]):
            return False
            
        # Nur in Räumen platzierbar? (Optional: Desk nur in 'dev' Raum)
        # room = self.office_grid[x][y]
        
        self.track_expense("other", item_data["cost"])
        
        new_obj = OfficeObject(item_data["type"], x, y, level=1)
        self.office_objects.append(new_obj)
        return True

    def expand_office_grid(self):
        """Vergrößert das Büro-Raster."""
        cost = 50000 * (len(self.office_grid) // 10)
        if self.money < cost: return False
        
        self.track_expense("other", cost)
        
        new_size = len(self.office_grid) + 5
        new_grid = [[None for _ in range(new_size)] for _ in range(new_size)]
        
        # Copy old grid
        for x in range(len(self.office_grid)):
            for y in range(len(self.office_grid[0])):
                new_grid[x][y] = self.office_grid[x][y]
        
        self.office_grid = new_grid
        return True

    def delete_bank_statement(self, idx):
        """Löscht einen Kontoauszug aus der Liste."""
        if 0 <= idx < len(self.bank_statements):
            self.bank_statements.pop(idx)
            return True
        return False

    def get_financial_summary(self):
        """Gibt eine kurze akustische Zusammenfassung der Finanzen zurück."""
        # Suche nach financial_history falls vorhanden
        profit = 0
        if hasattr(self, "financial_history") and self.financial_history:
            # Profit der letzten 4 Wochen
            last_4 = self.financial_history[-4:]
            inc = sum(w["total_income"] for w in last_4)
            exp = sum(w["total_expenses"] for w in last_4)
            profit = inc - exp
        
        summary = self.get_text('finance_summary_hotkey', 
                                money=self.money, 
                                profit=profit, 
                                fans=self.fans)
        return summary



    def generate_contract_work_options(self):
        """Generiert 3 zufaellige Auftragsarbeiten."""

        from models import ContractWorkProject
        options = []
        types = ["Code", "Audio", "Grafik", "Design"]
        
        base_points = 50 + (self.prestige * 5)
        base_payout = 2000 + (self.prestige * 200)
        
        for i in range(3):
            ctype = random.choice(types)
            diff = random.randint(1, 3)
            
            target_points = base_points * diff * random.uniform(0.8, 1.2)
            payout = base_payout * diff * random.uniform(0.9, 1.3)
            
            titles = []
            if ctype == "Code":
                titles = ["Datenbank-Optimierung", "Netzwerk-Code", "KI-Routinen", "Bugfixing extern"]
            elif ctype == "Audio":
                titles = ["Soundeffekte", "Podcast-Jingle", "Hintergrundmusik", "Voice-Over"]
            elif ctype == "Grafik":
                titles = ["Logo-Design", "3D-Modellierung", "Sprite-Animationen", "UI-Mockups"]
            else:
                titles = ["Level-Design", "Gamedesign-Dokument", "Balancing-Tabelle", "Quest-Schreiben"]
                
            name = f"{random.choice(titles)} ({ctype})"
            
            options.append({
                "name": name,
                "type": ctype,
                "target_points": int(target_points),
                "payout": int(payout)
            })
            
        return options

    def start_contract_work(self, option_data):
        """Startet einen ausgewaehlten Auftrag."""
        from models import ContractWorkProject
        cw = ContractWorkProject(
            name=option_data["name"],
            work_type=option_data["type"],
            target_points=option_data["target_points"],
            payout=option_data["payout"]
        )
        self.active_projects.append({
            "project": cw,
            "progress": 0.0,
            "total_weeks": 9999,
            "bugs": 0,
            "crunch": False,
            "ready_to_finish": False,
            "assigned_employee_ids": []
        })
        return True

    def finish_contract_work(self, ap_dict):
        """Schliesst eine Auftragsarbeit ab und zahlt aus."""
        proj = ap_dict["project"]
        self.track_income("other", proj.payout)
        if ap_dict in self.active_projects:
            self.active_projects.remove(ap_dict)
        return True

    def get_status_summary(self):
        """Gibt eine Zusammenfassung der Statuswerte (Datum, Geld, Forschungspunkte, Mitarbeiter, Fans) zurück."""
        # Skill-Punkte der Mitarbeiter summieren (Level)
        total_level = sum(emp.level for emp in self.employees)
        cal = self.get_calendar_text()
        
        summary = self.get_text('status_summary_hotkey',
                                date=cal,
                                money=self.money,
                                rp=self.research_points,
                                employees=len(self.employees),
                                total_level=total_level,
                                fans=self.fans,
                                prestige=self.prestige,
                                accessibility=getattr(self, "accessibility_reputation", 0),
                                accessibility_weekly=self.get_accessibility_weekly_fans())
        return summary

