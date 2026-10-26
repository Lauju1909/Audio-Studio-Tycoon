"""
Spielzustand für Audio Studio Tycoon - Audio Edition.

Verwaltet Firmendaten, Geld, Fans, Mitarbeiter, Engines,
Spielhistorie, Ereignisse und die Bewertungslogik.
"""

import random

import json
import os
from managers.corporate_warfare import CorporateWarfareManager
from managers.union_manager import UnionManager
from managers.it_security import ITSecurityManager
from managers.conventions import ConventionManager
from managers.real_estate import RealEstateManager
from managers.stock_manager import StockManager
from managers.subscription_manager import SubscriptionManager
from managers.monetization_manager import MonetizationManager
from managers.publishing_manager import PublishingManager
from managers.crypto_manager import CryptoManager
from managers.monopoly_manager import MonopolyManager
from managers.global_event_manager import GlobalEventManager
from models import (
    GameProject, ReviewScore, Employee, Engine, EngineFeature, 
    RivalStudio, RivalGame, Email, AddonProject, BundleProject, 
    ActiveMMO, BankLoan, CustomConsole, PublishingOffer, 
    PublishedThirdPartyGame, BankStatement,
    SoundConEvent, SoundtrackLabel, RadioContract, ManufacturingJob,
    StreamingPlatform, PodcastNetwork, AudioPass, CloudGamingService
)
from systems.hr import HRMixin
from systems.hardware import HardwareMixin
from systems.research import ResearchMixin
from systems.finance import FinanceMixin
from systems.persistence import PersistenceMixin
from systems.events import EventsMixin
from systems.scoring import ScoringMixin
from systems.dev import DevMixin
from systems.rivals import RivalsMixin
from systems.soundcon import SoundconMixin
from translations import get_system_language
from game_data import (
    get_compatibility, get_ideal_sliders, SLIDER_NAMES, PLATFORMS, AUDIENCE_MULTI, AUDIENCE_PRICE,
    RANDOM_EVENTS, ENGINE_FEATURES,
    EMPLOYEE_ROLES, DEV_PHASES, GAME_SIZES,
    TREND_TOPICS, TREND_GENRES, START_TOPICS, RESEARCHABLE_TOPICS,
    START_GENRES, START_AUDIENCES, RESEARCHABLE_GENRES, RESEARCHABLE_AUDIENCES,
    RESEARCHABLE_TECHNOLOGIES,
    get_available_platforms, START_YEAR, WEEKS_PER_YEAR,
)


class GameState(HRMixin, SoundconMixin, RivalsMixin, DevMixin, ScoringMixin, EventsMixin, PersistenceMixin, FinanceMixin, ResearchMixin, HardwareMixin):
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
        self.corporate_warfare = CorporateWarfareManager()
        self.union_manager = UnionManager()
        self.stock_manager = StockManager()
        self.subscription_manager = SubscriptionManager()
        self.monetization_manager = MonetizationManager()
        self.publishing_manager = PublishingManager()
        self.crypto_manager = CryptoManager()
        self.monopoly_manager = MonopolyManager()
        self.global_event_manager = GlobalEventManager()
        self.it_manager = ITSecurityManager()
        self.convention_manager = ConventionManager()
        self.real_estate_manager = RealEstateManager()
        self.pending_update = None
        self.ui_context = {}
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
        self.metaverse_land_value = 0.0
        self.metaverse_investment = 0.0
        self.metaverse_weeks_active = 0
        self.metaverse_burst = False
        self.metaverse_land_value = 0.0
        self.metaverse_investment = 0.0
        self.metaverse_weeks_active = 0
        self.metaverse_burst = False

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
        
        # Managers
        from managers.hr import HRManager
        from managers.finance import FinanceManager
        from managers.marketing import MarketingManager
        from managers.publisher import PublisherManager
        self.hr_manager = HRManager(self)
        self.finance_manager = FinanceManager(self)
        self.marketing_manager = MarketingManager(self)
        
        # Notifications
        from notifications import MailClient
        self.mail_client = MailClient(self)

        # Aktive MMOs
        self.active_mmos = []

        # Streaming Plattform
        self.streaming_platform = None

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

        # NEU: Crowdfunding
        self.active_crowdfundings = []  # Liste von { "project_name": str, "deadline_week": int, "target": int }
        self.failed_crowdfundings = 0

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
        self.active_merch_campaigns = []
        self.active_addons = []  # Addon-Projekte die verkaufen

        # NEU: Phase B - Bundles
        self.active_bundles = [] # Bundle-Projekte die stetig verkaufen

        # Pending Events (dynamisch gesetzt, hier initialisiert für Stabilität)
        self.pending_goty_results = None
        self.pending_dev_event = None
        self.pending_influencer_event = None
        self.pending_headhunt_event = None
        self.pending_union_event = None
        self.has_union = False

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
        self.key_left = pygame.K_LEFT
        self.key_right = pygame.K_RIGHT
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

        # NEU: E-Sports-Ligen (ab 2010)
        self.esports_leagues = []  # Liste von EsportsLeague-Objekten

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
        self.publisher_manager = PublisherManager(self)
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

        self.custom_consoles = []
        self.radio_contracts = []
        self.active_jingles = []
        self.soundtrack_label = None
        self.audio_pass = AudioPass()
        self.cloud_gaming = CloudGamingService()
        self.podcast_network = PodcastNetwork()
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


    # ------------------------------------------------------------------ #
    #  SoundCon – Spielemesse                                              #
    # ------------------------------------------------------------------ #


    # ------------------------------------------------------------------ #
    #  Soundtrack-Label                                                    #
    # ------------------------------------------------------------------ #


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

    def is_feature_unlocked(self, feature_id):
        """Prüft ob ein Feature laut FEATURE_UNLOCKS verfügbar ist."""
        from game_data import FEATURE_UNLOCKS
        
        feature = FEATURE_UNLOCKS.get(feature_id)
        if not feature:
            return True # If not specified, it's unlocked by default
            
        current_year = self.get_calendar_year()
        if "year" in feature and current_year < feature["year"]:
            return False
            
        if "office_level" in feature and self.office_level < feature["office_level"]:
            return False
            
        return True


    def get_calendar_text(self):
        """Gibt Kalenderjahr, Monat und Woche zurück (dynamisch basierend auf WEEKS_PER_YEAR)."""
        year = self.get_calendar_year()
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        
        # Dynamische Monatsberechnung (12 Monate pro Jahr)
        month_idx = int((week_in_year - 1) * 12 / WEEKS_PER_YEAR)
        
        self.settings.get("language", "de")
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

        while self.week_progress >= 1.0:
            self.week_progress -= 1.0
            self.week += 1
            self._on_new_week()

    @property
    def is_developing(self):
        return len(self.active_projects) > 0


    def _on_new_week(self):
        # --- NEW: Mitarbeiter-Wochenupdate & Headhunting ---
        for emp in self.employees:
            emp.weeks_employed = getattr(emp, "weeks_employed", 0) + 1
            
            # Alle 48 Wochen (1 Jahr) einen Talent-Punkt geben, wenn Level > 1
            if emp.weeks_employed % 48 == 0 and emp.skill_level > 1:
                emp.talent_points = getattr(emp, "talent_points", 0) + 1

            # Headhunting Event (Zufall, ca. 1x pro 2-3 Jahre pro Studio wenn gute Leute da sind)
            if 'Marketing-Guru' in getattr(emp, 'talents', []):
                self.hype = min(100.0, self.hype + 0.1)
            
            if getattr(self, "pending_headhunt_event", None) is None:
                if emp.skill_level >= 3 and not emp.is_ceo:
                    if __import__('random').random() < 0.005:  # 0.5% chance per week per senior employee
                        rival_offer = int(emp.salary * random.uniform(1.3, 2.0))
                        self.pending_headhunt_event = {
                            "employee": emp,
                            "rival_offer": rival_offer
                        }
                        if hasattr(self.audio, "play_sound"):
                            self.audio.play_sound("error")
                        if hasattr(self.audio, "speak"):
                            self.audio.speak(f"Achtung! Ein Rivale versucht {emp.name} abzuwerben!")

        """Logik die jede Woche passiert (Gehalt, Zufallsereignisse)."""
        # Abo-Dienst aktualisieren
        self.update_subscription_service()
        self._process_engine_licensing()
        self._process_port_projects()
        if hasattr(self, 'publisher_manager'):
            self.publisher_manager.update_tick()
        self._process_podcast_network()
        self._process_cloud_gaming()
        self._process_audio_pass()


        # Monatsankündigung (dynamisch basierend auf WEEKS_PER_YEAR)
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        prev_week_in_year = (self.week - 2) % WEEKS_PER_YEAR + 1 if self.week > 1 else 0
        
        current_month = int((week_in_year - 1) * 12 / WEEKS_PER_YEAR)
        prev_month = int((prev_week_in_year - 1) * 12 / WEEKS_PER_YEAR) if self.week > 1 else -1
        
        is_new_month = (current_month != prev_month)

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

        # Manager Ticks
        self.hr_manager.tick()
        self.finance_manager.tick(is_new_month)
        self.marketing_manager.tick(is_new_month)
        self.corporate_warfare.tick(self)
        self.union_manager.tick(self)
        self.stock_manager.tick(self)
        self.subscription_manager.tick(self)
        self.monetization_manager.tick(self)
        self.publishing_manager.tick(self)
        self.crypto_manager.tick(self)
        self.monopoly_manager.tick(self)
        self.global_event_manager.tick(self)
        self.it_manager.tick(self)
        self.convention_manager.tick(self)
        self.real_estate_manager.tick(self)
        
        # Eigene Konsolenverkaeufe und Marktanteil
        if hasattr(self, "custom_consoles"):
            for cc in self.custom_consoles:
                # Basis-Wachstum + Hype
                base_sales = int(5000 * cc.market_share * (1.0 + getattr(cc, 'hype', 0) / 100))
                
                # Exklusivtitel-Bonus
                exclusives_bonus = 1.0
                for game in self.game_history:
                    if game.platform == cc.name and game.sales > 0:
                        exclusives_bonus += 0.5 * (game.review.average / 10.0) # Sehr gute Exklusivtitel pushen extrem!
                        
                weekly_sales = int(base_sales * exclusives_bonus)
                
                # Saettigung: Irgendwann kauft es keiner mehr
                saturation = getattr(cc, 'units_sold', 0) / 100000000.0 # Ab 100 Mio wird es schwerer
                weekly_sales = int(weekly_sales * max(0.1, 1.0 - saturation))
                
                cc.units_sold = getattr(cc, 'units_sold', 0) + weekly_sales
                
                # Gewinn pro verkaufter Konsole (z.B. 50 EUR pro Stueck)
                profit = weekly_sales * 50
                if profit > 0:
                    self.money += profit
                    self.track_income("hardware", profit)
                
                # Marktanteil waechst langsam durch Verkaeufe
                cc.market_share = min(0.6, cc.market_share + (weekly_sales / 10000000.0))
                
                # Hype nimmt ab
                if getattr(cc, 'hype', 0) > 0:
                    cc.hype = max(0, cc.hype - 0.5)

        # Metaverse Bubble Logic
        if getattr(self, "metaverse_investment", 0) > 0 and not getattr(self, "metaverse_burst", False):
            self.metaverse_weeks_active = getattr(self, "metaverse_weeks_active", 0) + 1
            growth = random.uniform(0.01, 0.05)
            self.metaverse_land_value *= (1 + growth)
            
            if self.metaverse_weeks_active > 24:
                risk = 0.005 + (self.metaverse_weeks_active - 24) * 0.001
                if random.random() < risk:
                    self.metaverse_burst = True
                    # Bug fix: don't track expense here, because money was spent during investment
                    self.metaverse_land_value = 0
                    self.hype = max(0, self.hype - 30)
                    for e in self.employees:
                        e.morale = max(0, e.morale - 20)
                    self.active_events.append({
                        "name": "AudioVerse-Blase geplatzt!",
                        "effect": "none",
                        "multiplier": 1.0,
                        "duration": 4
                    })

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
                new_active.append(e)
        self.active_events = new_active

                # Projektfortschritt für alle aktiven Projekte
        for ap in list(self.active_projects):
            if getattr(self, 'strike_weeks_left', 0) > 0 or (hasattr(self, 'union_manager') and self.union_manager.is_striking):
                continue
            proj = ap["project"]
            
            # NEU: Auftragsarbeiten
            if getattr(proj, "target_points", None) is not None:
                points_added = 0.0
                skill_map = {"Code": "Programmierung", "Audio": "Sound", "Grafik": "Grafik", "Design": "Design"}
                skill_name = skill_map.get(proj.type, "Programmierung")
                
                active_emps = self._active_employees(proj)
                for emp in active_emps:
                    base_points = emp.skills.get(skill_name, 50) / 10.0
                    if 'Agile Coach' in getattr(emp, 'talents', []):
                        base_points *= 1.2
                    points_added += base_points
                
                if not active_emps:
                    points_added = 5.0
                    
                points_added *= getattr(self, "dev_speed_multiplier", 1.0)
                if hasattr(self, 'union_manager') and self.union_manager.ai_tools_active:
                    points_added *= 2.0
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
                        if 'Crunch-Survivor' in getattr(emp, 'talents', []):
                            emp.morale = 100
                        else:
                            emp.morale = max(0, emp.morale - morale_loss)
                else:
                    for emp in active_emps:
                        if getattr(emp, "personality", None) == "workaholic":
                            if 'Crunch-Survivor' in getattr(emp, 'talents', []):
                                emp.morale = 100
                            else:
                                emp.morale = max(0, emp.morale - 1)
                        else:
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
            if hasattr(self, 'union_manager') and self.union_manager.ai_tools_active:
                boost *= 2.0
            if getattr(self, 'office_perks', []):
                boost *= (1.0 + len(self.office_perks) * 0.02)
                
            # VR-spezifischer Malus fr ungeschultes Personal
            if "(VR)" in getattr(proj, "platform", ""):
                active_emps = self._active_employees(proj)
                if active_emps:
                    avg_skill = sum(e.skill_level for e in active_emps) / len(active_emps) if active_emps else 0
                    if avg_skill < 3.5:
                        boost *= 0.4 # Sehr langsam, wenn das Team nicht hochqualifiziert ist
                    elif avg_skill < 4.5:
                        boost *= 0.7
                        
            boost *= self.global_event_manager.get_development_speed_modifier()
                    
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
                    if 'Crunch-Survivor' in getattr(emp, 'talents', []):

                        emp.morale = 100

                    else:

                        emp.morale = max(0, emp.morale - morale_loss)
            else:
                # Kein Crunch: Workaholics verlieren wöchentlich 1 Moralpunkt durch harte Arbeit
                active_emps = self._active_employees(proj)
                for emp in active_emps:
                    if getattr(emp, "personality", None) == "workaholic":
                        if 'Crunch-Survivor' in getattr(emp, 'talents', []):

                            emp.morale = 100

                        else:

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
                if proj.__class__.__name__ == "EngineProject":
                    self.finalize_engine(ap)
                    continue
                elif proj.__class__.__name__ in ["UpdateProject", "DLCProject"]:
                    self._finish_update_project(proj)
                    if ap in self.active_projects:
                        self.active_projects.remove(ap)
                    continue
                
            # AAA Events (Max 1x pro Projekt)
            if getattr(proj, "size", None) == "AAA" and not ap.get("aaa_event_done"):
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
            max_ev = {"Klein": 1, "Mittel": 1, "Groß": 2, "AAA": 0}.get(getattr(proj, "size", None), 1)
            if ap.get("event_count", 0) < max_ev:
                prog_pct = ap["progress"] / ap["total_weeks"]
                if 0.15 < prog_pct < 0.85:
                    chance = {"Klein": 0.04, "Mittel": 0.05, "Groß": 0.06}.get(getattr(proj, "size", None), 0.05)
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
            if getattr(self, 'strike_weeks_left', 0) == 0:
                self.research_progress += 1
            if self.research_progress >= self.research_total_weeks:
                self.complete_research()

        # Konsolenentwicklung
        if getattr(self, "is_developing_console", False):
            if getattr(self, 'strike_weeks_left', 0) == 0:
                self.console_progress += 1
            if self.console_progress >= getattr(self, 'console_total_weeks', 100):
                self.is_developing_console = False
                c = self.current_console_draft
                if isinstance(c, dict):
                    new_console = CustomConsole(
                        name=c['name'],
                        architecture=c.get('architecture', 'RISC'),
                        performance=c.get('performance', 1),
                        marketing_budget=c.get('marketing_budget', 0),
                        dev_cost=c['cost'],
                        release_week=self.week
                    )
                else:
                    new_console = CustomConsole(
                        name=c.name,
                        architecture=c.architecture,
                        performance=c.performance,
                        marketing_budget=c.marketing_budget,
                        dev_cost=c.dev_cost,
                        release_week=self.week
                    )
                if not hasattr(self, "custom_consoles"):
                    self.custom_consoles = []
                self.custom_consoles.append(new_console)
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_hardware'),
                    subject=self.get_text('subject_console_done'),
                    body=self.get_text('body_console_done', name=c['name'] if isinstance(c, dict) else c.name),
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
                    current_active = g.active_players
                else:
                    current_active = new_sales * 5  # Simulate active players for non-F2P games

                # In-Game Werbung (Feature 1)
                if getattr(g, "has_ads", False):
                    ad_rev = int(current_active * 0.5)
                    if ad_rev > 0:
                        self.track_income("other", ad_rev)
                        g.revenue += ad_rev
                        self.hype = max(0.0, self.hype - 0.5) # Hype loss due to ads

                # Mikrotransaktionen (MTX)
                if getattr(g, "has_mtx", False):
                    mtx_rev = int(current_active * 1.5)
                    if mtx_rev > 0:
                        self.track_income("other", mtx_rev)
                        g.revenue += mtx_rev
                        self.fans = max(0, self.fans - 20) # stetiger Fan-Verlust

                if getattr(g, "is_f2p", False):
                    # Cheater-Welle für F2P
                    if not getattr(g, "has_anti_cheat", False):
                        if random.random() < 0.05:
                            lost_players = int(g.active_players * 0.15)
                            g.active_players -= lost_players
                            self.fans = max(0, self.fans - lost_players)
                            self.emails.insert(0, Email(
                                sender=self.get_text('cheater_email_sender', default="Community Manager"),
                                subject=self.get_text('cheater_email_subject', game=g.name, default="Cheater in {game}!"),
                                body=self.get_text('cheater_email_body', game=g.name, lost=lost_players, default="Eine massive Cheater-Welle ruiniert das Spiel! Wir verlieren Spieler!"),
                                date_week=self.week
                            ))
                            
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
                
                # DDoS Check
                is_ddos = any(e.get("type") == "ddos" for e in getattr(self, "active_cyber_effects", []))
                if is_ddos:
                    digital_sold = 0 # No digital sales during DDoS
                
                physical_rev = physical_sold * getattr(g, "physical_price", 45)
                digital_rev = digital_sold * price
                
                g.sales += physical_sold + digital_sold
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
                
                is_ddos = any(e.get("type") == "ddos" for e in getattr(self, "active_cyber_effects", []))
                
                if not is_ddos:
                    rev = int(mmo.weekly_revenue * self.profit_multiplier)
                    self.track_income("mmo", rev)
                    mmo.game.revenue += rev
                else:
                    rev = 0

                self.track_expense("mmo", mmo.weekly_cost)
                
                if getattr(mmo.game, "has_mtx", False):
                    if not is_ddos:
                        mtx_rev = int(mmo.players * 1.5)
                        self.track_income("other", mtx_rev)
                        mmo.game.revenue += mtx_rev
                    mmo.players = int(mmo.players * 0.95) # players leave faster due to MTX
                
                # Cheater-Wellen Logic
                if not getattr(mmo.game, "has_anti_cheat", False):
                    if random.random() < 0.05: # 5% Chance pro Woche auf Cheater-Welle
                        lost_players = int(mmo.players * 0.15)
                        mmo.players -= lost_players
                        self.fans = max(0, self.fans - lost_players)
                        self.emails.insert(0, Email(
                            sender=self.get_text('cheater_email_sender', default="Community Manager"),
                            subject=self.get_text('cheater_email_subject', game=mmo.game.name, default="Cheater in {game}!"),
                            body=self.get_text('cheater_email_body', game=mmo.game.name, lost=lost_players, default="Eine massive Cheater-Welle ruiniert das Spiel! Wir verlieren Spieler!"),
                            date_week=self.week
                        ))
                
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

        # Eigene Konsolen
        if getattr(self, "active_custom_console", None):
            cc = self.active_custom_console
            if not getattr(cc, "is_released", False):
                progress_gain = 0
                for emp in self.employees:
                    if not emp.is_training and not emp.is_sick and emp.morale > 0:
                        progress_gain += emp.skills.get("Programmierung", 50) / 100.0
                
                total_weeks = getattr(cc, "total_weeks", 50)
                weekly_progress = (progress_gain / total_weeks) * 0.5
                cc.progress += weekly_progress
                if cc.progress >= 1.0:
                    cc.progress = 1.0
                    cc.is_released = True
                    cc.weeks_on_market = 0
                    if hasattr(self.audio, "play_sound"):
                        self.audio.play_sound("success")
                    if hasattr(self.audio, "speak"):
                        self.audio.speak(self.get_text('console_finished', name=cc.name))
                    
                    from game_data import PLATFORMS
                    PLATFORMS.append({
                        "name": cc.name,
                        "license_fee": 0,
                        "market_multi": 1.0 + (cc.tech_level / 100.0),
                        "unlock_year": self.get_calendar_year(),
                        "end_year": self.get_calendar_year() + 10,
                        "type": "Konsole"
                    })
            else:
                cc.weeks_on_market += 1
                base_sales = int(cc.tech_level * 500 * (1.0 + (self.fans / 10000.0)))
                decay = max(0.1, 1.0 - (cc.weeks_on_market / 100.0))
                weekly_sales = int(base_sales * decay)
                cc.units_sold += weekly_sales
                
                revenue = weekly_sales * cc.price
                cc.revenue += revenue
                self.money += revenue
                if revenue > 0:
                    self.track_income("hardware", revenue)
                
                cc.active_users += weekly_sales
                if cc.active_users > 0:
                    cc.active_users = int(cc.active_users * 0.99)
        
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
        self._process_esports_leagues()
        self._process_sponsorships()
        if week_in_year == WEEKS_PER_YEAR:
            self._check_goty()


    
                


    


 

            


    def _active_employees(self, project=None):
        """Liefert nur Mitarbeiter, die nicht krank, nicht in Training und nicht im Urlaub sind. Filtert nach Projekt-Team wenn angegeben."""
        base = [e for e in self.employees if not getattr(e, 'is_sick', False) and not getattr(e, 'is_training', False) and getattr(e, 'vacation_weeks_left', 0) <= 0]
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
            
        return sum(bonuses) / len(bonuses) if bonuses else 0

    def get_team_speed_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
        
        # Durchschnittlicher Speed-Skill (50 = 1.0)
        avg_speed = sum(e.speed for e in active) / len(active) if active else 0
        
        # Trait-Modifikatoren (Robust gegen alte Strings oder fehlende Keys)
        trait_mods = []
        for e in active:
            val = 1.0
            if hasattr(e, 'trait') and isinstance(e.trait, dict):
                if e.trait.get("effect") == "speed":
                    val = e.trait.get("value", 1.0)
            trait_mods.append(val)
        trait_avg = sum(trait_mods) / len(trait_mods) if trait_mods else 0
        
        # NEU: Persönlichkeits-Modifikatoren (workaholic: +20% Speed)
        pers_mods = [1.20 if getattr(e, 'personality', None) == 'workaholic' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods) if pers_mods else 0
        
        # NEU: Temporäre Event-Mali
        temp_penalty = getattr(self, "temp_dev_speed_penalty", 1.0)
        
        base_multi = (avg_speed / 50.0) * trait_avg * pers_avg
        return base_multi * self.dev_speed_multiplier * self.logic_multiplier * temp_penalty

    def get_team_bug_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
            
        # Durchschnittlicher Bug-Modifier der Mitarbeiter
        avg_mod = sum(e.bug_modifier for e in active) / len(active) if active else 0
        
        # Trait-Modifikatoren
        trait_mods = []
        for e in active:
            val = 1.0
            if hasattr(e, 'trait') and isinstance(e.trait, dict):
                if e.trait.get("effect") == "bugs":
                    val = e.trait.get("value", 1.0)
            trait_mods.append(val)
        trait_avg = sum(trait_mods) / len(trait_mods) if trait_mods else 0
        
        # NEU: Persönlichkeits-Modifikatoren (chaotic: +15% Bugs)
        pers_mods = [1.15 if getattr(e, 'personality', None) == 'chaotic' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods) if pers_mods else 0
        
        # QA Bonus
        qa_bonus = 0.7 if self.has_office_bonus("qa_tools") else 1.0
        if "Next-Gen Testlabor & QA" in self.unlocked_technologies:
            qa_bonus *= 0.6
        if "Performance-Labor" in self.unlocked_technologies:
            qa_bonus *= 0.8
        
        return avg_mod * trait_avg * qa_bonus * pers_avg

    def get_team_quality_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
        mods = [e.trait["value"] if e.trait and e.trait["effect"] == "quality" else 1.0 for e in active]
        
        # NEU: Persönlichkeits-Modifikatoren (perfectionist: +15% Qualität)
        pers_mods = [1.15 if getattr(e, 'personality', None) == 'perfectionist' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods) if pers_mods else 0
        
        # NEU: Temporärer Event-Bonus
        temp_boost = getattr(self, "temp_quality_boost", 0.0)
        return (sum(mods) / len(mods) if mods else 0.0) * pers_avg * (1.0 + temp_boost)

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


    # ==========================================================
    # AKTIENMARKT / INVESTMENTS
    # ==========================================================


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


    # ==========================================================
    # ZUFALLSEREIGNISSE
    # ==========================================================


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


    # ==========================================================
    # BEWERTUNG
    # ==========================================================


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


    # ==========================================================
    # STATUS
    # ==========================================================


    # ==========================================================
    # NEU: v3.11.0-beta.1 Expansion Methods (Community & Hardware)
    # ==========================================================


    # ==========================================================
    # SPEICHERN / LADEN
    # ==========================================================


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


def handle_input(*args, **kwargs): pass
def update_game_state(*args, **kwargs): pass
