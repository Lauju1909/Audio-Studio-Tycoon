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
from systems.simulation import SimulationMixin
from systems.hr import HRMixin
from systems.business import BusinessMixin
from systems.team import TeamMixin
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


class GameState(SimulationMixin, HRMixin, SoundconMixin, RivalsMixin, DevMixin, ScoringMixin, EventsMixin, PersistenceMixin, FinanceMixin, ResearchMixin, HardwareMixin, TeamMixin, BusinessMixin):
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



def handle_input(*args, **kwargs): pass
def update_game_state(*args, **kwargs): pass
