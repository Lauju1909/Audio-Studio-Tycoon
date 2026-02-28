#!/usr/bin/env python3
"""
Tiefgehender End-to-End-Test fuer Audio Studio Tycoon.
Simuliert den kompletten Spielablauf durch alle Menues mit echten Tasteneingaben.
Testet Randfaelle, Fehlerzustaende und Edge Cases.
"""

import pygame
pygame.init()
screen = pygame.display.set_mode((100, 100))

import os
import sys
import traceback
import random

game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, game_dir)
os.chdir(game_dir)

from logic import GameState
from audio import AudioManager
import translations
from translations import get_text, set_language
from models import GameProject, Employee, Engine

# ============================================================
# DUMMY AUDIO (kein Sound, kein TTS)
# ============================================================
class DummyAudio:
    def speak(self, text, interrupt=True): pass
    def play_sound(self, name): pass
    def play_music(self, name): pass
    def stop_music(self): pass
    def cleanup(self): pass
    def set_music_enabled(self, enabled): pass
    def update_tts_engine(self, engine): pass
    def is_speaking(self): return False

# ============================================================
# FEHLER-SAMMLER
# ============================================================
errors_found = []
warnings_found = []
tests_passed = 0
tests_failed = 0

def log_error(category, message, detail=""):
    global tests_failed
    tests_failed += 1
    errors_found.append({"category": category, "message": message, "detail": detail})
    print(f"  [X] FEHLER [{category}]: {message}")
    if detail:
        # Nur letzte 3 Zeilen des Tracebacks
        lines = detail.strip().split('\n')
        for line in lines[-3:]:
            print(f"      {line}")

def log_warning(category, message):
    warnings_found.append({"category": category, "message": message})
    print(f"  [!] WARNUNG [{category}]: {message}")

def log_pass(message):
    global tests_passed
    tests_passed += 1
    print(f"  [OK] {message}")

def make_key_event(key, unicode_char=""):
    return pygame.event.Event(pygame.KEYDOWN, key=key, unicode=unicode_char, mod=0, scancode=0)

# ============================================================
# TEST 1: Kompletter Spielstart-Flow  
# ============================================================
def test_game_start_flow():
    print("\n" + "="*60)
    print("TEST 1: KOMPLETTER SPIELSTART-FLOW")
    print("="*60)
    
    from menus import MainMenu, DifficultyMenu, CompanyNameMenu, GameMenu
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    
    # 1. Hauptmenue -> Neues Spiel
    try:
        menu = MainMenu(audio, state)
        menu.announce_entry()
        # Navigiere zu "Neues Spiel starten" (sollte erstes Item sein)
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"MainMenu -> Enter -> {result}")
    except Exception as e:
        log_error("GameStart", "MainMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # 2. Schwierigkeitsgrad waehlen
    try:
        menu = DifficultyMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))  # Einfach
        log_pass(f"DifficultyMenu -> Enter -> {result}")
    except Exception as e:
        log_error("GameStart", "DifficultyMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # 3. Firmenname eingeben
    try:
        menu = CompanyNameMenu(audio, state)
        menu.announce_entry()
        # Buchstaben eingeben
        for char in "TestCo":
            menu.handle_input(make_key_event(ord(char.upper()), char))
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        if state.company_name:
            log_pass(f"CompanyNameMenu -> Firmenname: '{state.company_name}' -> {result}")
        else:
            log_error("GameStart", "Firmenname wurde nicht gesetzt")
    except Exception as e:
        log_error("GameStart", "CompanyNameMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # 4. Game Menu
    try:
        menu = GameMenu(audio, state)
        menu.announce_entry()
        # Navigiere durch alle Optionen
        for i in range(15):
            menu.handle_input(make_key_event(pygame.K_DOWN))
        for i in range(15):
            menu.handle_input(make_key_event(pygame.K_UP))
        log_pass("GameMenu Navigation funktioniert")
    except Exception as e:
        log_error("GameStart", "GameMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 2: Komplette Spielentwicklungs-Pipeline via Menues
# ============================================================
def test_dev_pipeline():
    print("\n" + "="*60)
    print("TEST 2: SPIELENTWICKLUNGS-PIPELINE VIA MENUES")
    print("="*60)
    
    from menus import (TopicMenu, GenreMenu, SubGenreMenu, PlatformMenu, 
                       AudienceMenu, GameSizeMenu, MarketingMenu, EngineSelectMenu,
                       GameNameMenu, DevelopmentSliderMenu, DevProgressMenu,
                       ReviewResultMenu, SequelMenu, RemasterSelectMenu,
                       PublisherMenu, ExpoMenu)
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Pipeline Test GmbH"
    state.money = 500000
    
    # Topic waehlen
    try:
        menu = TopicMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"TopicMenu -> {state.current_draft.get('topic', '???')} -> {result}")
    except Exception as e:
        log_error("DevPipeline", "TopicMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # Genre waehlen
    try:
        menu = GenreMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"GenreMenu -> {state.current_draft.get('genre', '???')} -> {result}")
    except Exception as e:
        log_error("DevPipeline", "GenreMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # SubGenre waehlen
    try:
        menu = SubGenreMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"SubGenreMenu -> {result}")
    except Exception as e:
        log_error("DevPipeline", "SubGenreMenu fehlgeschlagen", traceback.format_exc())
    
    # Platform waehlen
    try:
        menu = PlatformMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"PlatformMenu -> {state.current_draft.get('platform', '???')} -> {result}")
    except Exception as e:
        log_error("DevPipeline", "PlatformMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # Publisher waehlen
    try:
        menu = PublisherMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"PublisherMenu -> {result}")
    except Exception as e:
        log_error("DevPipeline", "PublisherMenu fehlgeschlagen", traceback.format_exc())
    
    # Audience
    try:
        menu = AudienceMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"AudienceMenu -> {state.current_draft.get('audience', '???')} -> {result}")
    except Exception as e:
        log_error("DevPipeline", "AudienceMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # GameSize
    try:
        menu = GameSizeMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"GameSizeMenu -> {state.current_draft.get('size', '???')} -> {result}")
    except Exception as e:
        log_error("DevPipeline", "GameSizeMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # Marketing
    try:
        menu = MarketingMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"MarketingMenu -> {result}")
    except Exception as e:
        log_error("DevPipeline", "MarketingMenu fehlgeschlagen", traceback.format_exc())
    
    # Engine
    try:
        menu = EngineSelectMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"EngineSelectMenu -> {result}")
    except Exception as e:
        log_error("DevPipeline", "EngineSelectMenu fehlgeschlagen", traceback.format_exc())
    
    # Spielname eingeben
    try:
        menu = GameNameMenu(audio, state)
        menu.announce_entry()
        for char in "MeinSpiel":
            menu.handle_input(make_key_event(ord(char.upper()), char))
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"GameNameMenu -> '{state.current_draft.get('name', '???')}' -> {result}")
    except Exception as e:
        log_error("DevPipeline", "GameNameMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # Slider verteilen
    try:
        menu = DevelopmentSliderMenu(audio, state)
        menu.announce_entry()
        # Rechts druecken um Punkte zu verteilen (6 Slider * 5 Punkte = 30)
        for _ in range(5):
            menu.handle_input(make_key_event(pygame.K_RIGHT))
        menu.handle_input(make_key_event(pygame.K_DOWN))
        for _ in range(5):
            menu.handle_input(make_key_event(pygame.K_RIGHT))
        menu.handle_input(make_key_event(pygame.K_DOWN))
        for _ in range(5):
            menu.handle_input(make_key_event(pygame.K_RIGHT))
        menu.handle_input(make_key_event(pygame.K_DOWN))
        for _ in range(5):
            menu.handle_input(make_key_event(pygame.K_RIGHT))
        menu.handle_input(make_key_event(pygame.K_DOWN))
        for _ in range(5):
            menu.handle_input(make_key_event(pygame.K_RIGHT))
        menu.handle_input(make_key_event(pygame.K_DOWN))
        for _ in range(5):
            menu.handle_input(make_key_event(pygame.K_RIGHT))
        # Enter zum Bestaetigen
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"DevelopmentSliderMenu -> Punkte verteilt -> {result}")
    except Exception as e:
        log_error("DevPipeline", "DevelopmentSliderMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # Dev Progress - Spielentwicklung simulieren
    try:
        menu = DevProgressMenu(audio, state)
        menu.announce_entry()
        # Wochen vorspielen bis fertig
        state.time_speed = 4.0
        for _ in range(200):
            state.update_tick(1000)  # 1 Sekunde pro Tick
            if hasattr(menu, 'update'):
                menu.update()
        # Fertiges Spiel
        if state.is_developing:
            # Noch nicht fertig - mehr Ticks
            for _ in range(500):
                state.update_tick(1000)
                if hasattr(menu, 'update'):
                    menu.update()
        
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"DevProgressMenu -> Entwicklung {'fertig' if not state.is_developing else 'laeuft noch'} -> {result}")
    except Exception as e:
        log_error("DevPipeline", "DevProgressMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # Review-Ergebnis anzeigen
    try:
        if len(state.game_history) > 0:
            menu = ReviewResultMenu(audio, state)
            menu.announce_entry()
            result = menu.handle_input(make_key_event(pygame.K_RETURN))
            log_pass(f"ReviewResultMenu -> Score: {state.game_history[-1].review.average if state.game_history[-1].review else 'N/A'} -> {result}")
        else:
            log_warning("DevPipeline", "Kein Spiel in History nach Entwicklung")
    except Exception as e:
        log_error("DevPipeline", "ReviewResultMenu fehlgeschlagen", traceback.format_exc())
    
    # Sequel testen
    try:
        menu = SequelMenu(audio, state)
        menu.announce_entry()
        log_pass("SequelMenu erstellt und geoeffnet")
    except Exception as e:
        log_error("DevPipeline", "SequelMenu fehlgeschlagen", traceback.format_exc())
    
    # Remaster testen
    try:
        menu = RemasterSelectMenu(audio, state)
        menu.announce_entry()
        log_pass("RemasterSelectMenu erstellt und geoeffnet")
    except Exception as e:
        log_error("DevPipeline", "RemasterSelectMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 3: HR-Pipeline via Menues
# ============================================================
def test_hr_pipeline():
    print("\n" + "="*60)
    print("TEST 3: HR-PIPELINE VIA MENUES")
    print("="*60)
    
    from menus import (HRMenu, HireMenu, FireMenu, 
                       TrainingEmployeeSelectMenu, TrainingOptionMenu)
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "HR Test GmbH"
    state.money = 500000
    state.office_level = 2  # Mittleres Buero
    
    # HR Menu oeffnen
    try:
        menu = HRMenu(audio, state)
        menu.announce_entry()
        log_pass("HRMenu geoeffnet")
    except Exception as e:
        log_error("HR", "HRMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # Hire Menu - Bewerber anzeigen und ersten einstellen
    try:
        menu = HireMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        if len(state.employees) > 0:
            log_pass(f"HireMenu -> Mitarbeiter eingestellt: {state.employees[0].name}")
        else:
            log_warning("HR", "Kein Mitarbeiter eingestellt nach Enter")
    except Exception as e:
        log_error("HR", "HireMenu fehlgeschlagen", traceback.format_exc())
    
    # Noch 2 einstellen
    for i in range(2):
        try:
            menu = HireMenu(audio, state)
            menu.announce_entry()
            menu.handle_input(make_key_event(pygame.K_RETURN))
        except Exception as e:
            log_error("HR", f"HireMenu Runde {i+2} fehlgeschlagen", traceback.format_exc())
    
    log_pass(f"{len(state.employees)} Mitarbeiter eingestellt")
    
    # Fire Menu
    try:
        menu = FireMenu(audio, state)
        menu.announce_entry()
        before = len(state.employees)
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"FireMenu -> Vor: {before}, Nach: {len(state.employees)} -> {result}")
    except Exception as e:
        log_error("HR", "FireMenu fehlgeschlagen", traceback.format_exc())
    
    # Training
    if len(state.employees) > 0:
        try:
            menu = TrainingEmployeeSelectMenu(audio, state)
            menu.announce_entry()
            result = menu.handle_input(make_key_event(pygame.K_RETURN))
            log_pass(f"TrainingEmployeeSelectMenu -> {result}")
        except Exception as e:
            log_error("HR", "TrainingEmployeeSelectMenu fehlgeschlagen", traceback.format_exc())
        
        try:
            menu = TrainingOptionMenu(audio, state)
            menu.announce_entry()
            result = menu.handle_input(make_key_event(pygame.K_RETURN))
            log_pass(f"TrainingOptionMenu -> {result}")
        except Exception as e:
            log_error("HR", "TrainingOptionMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 4: Forschung via Menues
# ============================================================
def test_research_pipeline():
    print("\n" + "="*60)
    print("TEST 4: FORSCHUNG VIA MENUES")
    print("="*60)
    
    from menus import (ResearchMenu, FeatureResearchMenu, GenreResearchMenu,
                       AudienceResearchMenu, EngineCreateNameMenu, 
                       EngineFeatureSelectMenu)
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Research Test GmbH"
    state.money = 5000000
    state.week = 100
    
    # Research Menu
    try:
        menu = ResearchMenu(audio, state)
        menu.announce_entry()
        log_pass("ResearchMenu geoeffnet")
    except Exception as e:
        log_error("Research", "ResearchMenu fehlgeschlagen", traceback.format_exc())
        return
    
    # Feature Research
    try:
        menu = FeatureResearchMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"FeatureResearchMenu -> {result}")
    except Exception as e:
        log_error("Research", "FeatureResearchMenu fehlgeschlagen", traceback.format_exc())
    
    # Genre Research
    try:
        menu = GenreResearchMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"GenreResearchMenu -> {result}")
    except Exception as e:
        log_error("Research", "GenreResearchMenu fehlgeschlagen", traceback.format_exc())
    
    # Audience Research
    try:
        menu = AudienceResearchMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"AudienceResearchMenu -> {result}")
    except Exception as e:
        log_error("Research", "AudienceResearchMenu fehlgeschlagen", traceback.format_exc())
    
    # Engine erstellen
    try:
        state.is_researching = False
        menu = EngineCreateNameMenu(audio, state)
        menu.announce_entry()
        for char in "SuperEngine":
            menu.handle_input(make_key_event(ord(char.upper()), char))
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"EngineCreateNameMenu -> {result}")
    except Exception as e:
        log_error("Research", "EngineCreateNameMenu fehlgeschlagen", traceback.format_exc())
    
    try:
        menu = EngineFeatureSelectMenu(audio, state)
        menu.announce_entry()
        # Feature auswaehlen
        menu.handle_input(make_key_event(pygame.K_RETURN))
        # Runter und dann erstellen
        for _ in range(20):
            menu.handle_input(make_key_event(pygame.K_DOWN))
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"EngineFeatureSelectMenu -> {result}")
    except Exception as e:
        log_error("Research", "EngineFeatureSelectMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 5: Bank/Finance Menues
# ============================================================
def test_finance_menus():
    print("\n" + "="*60)
    print("TEST 5: BANK/FINANZ MENUES")
    print("="*60)
    
    from menus import BankMenu, LoanMenu, StockMarketMenu, ChartMenu
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Finance Test GmbH"
    state.money = 1000000
    
    # Bank Menu
    try:
        menu = BankMenu(audio, state)
        menu.announce_entry()
        # Navigieren
        for i in range(5):
            menu.handle_input(make_key_event(pygame.K_DOWN))
        menu.handle_input(make_key_event(pygame.K_UP))
        log_pass("BankMenu Navigation funktioniert")
    except Exception as e:
        log_error("Finance", "BankMenu fehlgeschlagen", traceback.format_exc())
    
    # Loan Menu
    try:
        menu = LoanMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"LoanMenu -> {result}")
    except Exception as e:
        log_error("Finance", "LoanMenu fehlgeschlagen", traceback.format_exc())
    
    # Stock Market
    try:
        state.unlocked_technologies.append("Investment & M&A")
        menu = StockMarketMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"StockMarketMenu -> {result}")
    except Exception as e:
        log_error("Finance", "StockMarketMenu fehlgeschlagen", traceback.format_exc())
    
    # Chart Menu
    try:
        menu = ChartMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"ChartMenu -> {result}")
    except Exception as e:
        log_error("Finance", "ChartMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 6: Office & Settings
# ============================================================
def test_office_settings():
    print("\n" + "="*60)
    print("TEST 6: BUERO & EINSTELLUNGEN")
    print("="*60)
    
    from menus import OfficeMenu, SettingsMenu, HelpMenu, SaveMenu, LoadMenu
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Office Test"
    state.money = 5000000
    
    # Office
    try:
        menu = OfficeMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"OfficeMenu -> {result}")
    except Exception as e:
        log_error("Office", "OfficeMenu fehlgeschlagen", traceback.format_exc())
    
    # Settings
    try:
        menu = SettingsMenu(audio, state, lambda: "game_menu")
        menu.announce_entry()
        for i in range(5):
            menu.handle_input(make_key_event(pygame.K_DOWN))
        menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass("SettingsMenu Navigation funktioniert")
    except Exception as e:
        log_error("Settings", "SettingsMenu fehlgeschlagen", traceback.format_exc())
    
    # Help
    try:
        menu = HelpMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"HelpMenu -> {result}")
    except Exception as e:
        log_error("Help", "HelpMenu fehlgeschlagen", traceback.format_exc())
    
    # Save
    try:
        menu = SaveMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"SaveMenu -> {result}")
    except Exception as e:
        log_error("Save", "SaveMenu fehlgeschlagen", traceback.format_exc())
    
    # Load
    try:
        menu = LoadMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"LoadMenu -> {result}")
    except Exception as e:
        log_error("Load", "LoadMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 7: Email & Service
# ============================================================
def test_email_service():
    print("\n" + "="*60)
    print("TEST 7: EMAIL & SERVICE")
    print("="*60)
    
    from menus import EmailInboxMenu, EmailDetailMenu, ServiceMenu, GameServiceOptionsMenu
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Email Test"
    state.money = 500000
    
    # Emails hinzufuegen (als Email-Objekte, nicht Dicts!)
    from models import Email
    state.emails = [
        Email(sender="Fan", subject="Tolles Spiel!", body="Ich liebe euer Spiel!", date_week=1),
        Email(sender="Bank", subject="Kredit Info", body="Ihre Kreditinformationen.", date_week=2),
    ]
    state.emails[1].is_read = True
    
    # Inbox
    try:
        menu = EmailInboxMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"EmailInboxMenu -> {result}")
    except Exception as e:
        log_error("Email", "EmailInboxMenu fehlgeschlagen", traceback.format_exc())
    
    # Detail
    try:
        state.selected_email_index = 0
        menu = EmailDetailMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"EmailDetailMenu -> {result}")
    except Exception as e:
        log_error("Email", "EmailDetailMenu fehlgeschlagen", traceback.format_exc())
    
    # Service (mit einem Spiel in History)
    proj = GameProject("TestService", "Fantasy", "RPG",
                       sliders={"Gameplay": 5, "Grafik": 5, "Sound": 5, "Story": 5, "KI": 5, "Welt": 5},
                       platform="Zenith-Core 88", audience="Jeder",
                       engine=state.engines[0] if state.engines else None)
    state.finalize_game(proj)
    
    try:
        menu = ServiceMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"ServiceMenu -> {result}")
    except Exception as e:
        log_error("Service", "ServiceMenu fehlgeschlagen", traceback.format_exc())
    
    # GameServiceOptions
    try:
        state.selected_service_game_index = 0
        menu = GameServiceOptionsMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"GameServiceOptionsMenu -> {result}")
    except Exception as e:
        log_error("Service", "GameServiceOptionsMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 8: Hardware/Console Menus
# ============================================================
def test_hardware_menus():
    print("\n" + "="*60)
    print("TEST 8: HARDWARE/KONSOLE MENUES")
    print("="*60)
    
    from menus import HardwareDevMenu, ConsoleNameInput, ConsoleSpecsMenu
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Hardware Test"
    state.money = 50000000
    state.unlocked_technologies.append("Hardware Labor")
    
    try:
        menu = HardwareDevMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"HardwareDevMenu -> {result}")
    except Exception as e:
        log_error("Hardware", "HardwareDevMenu fehlgeschlagen", traceback.format_exc())
    
    try:
        menu = ConsoleNameInput(audio, state)
        menu.announce_entry()
        for char in "MeineBox":
            menu.handle_input(make_key_event(ord(char.upper()), char))
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"ConsoleNameInput -> {result}")
    except Exception as e:
        log_error("Hardware", "ConsoleNameInput fehlgeschlagen", traceback.format_exc())
    
    try:
        menu = ConsoleSpecsMenu(audio, state)
        menu.announce_entry()
        menu.handle_input(make_key_event(pygame.K_RETURN))
        menu.handle_input(make_key_event(pygame.K_DOWN))
        menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass("ConsoleSpecsMenu Navigation funktioniert")
    except Exception as e:
        log_error("Hardware", "ConsoleSpecsMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 9: Bankruptcy & GOTY & AAA Events
# ============================================================
def test_special_menus():
    print("\n" + "="*60)
    print("TEST 9: SPEZIAL-MENUES (Bankrott, GOTY, AAA)")
    print("="*60)
    
    from menus import BankruptcyMenu, GOTYMenu, AAADevEventMenu
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Special Test"
    
    # Bankruptcy
    try:
        menu = BankruptcyMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"BankruptcyMenu -> {result}")
    except Exception as e:
        log_error("Special", "BankruptcyMenu fehlgeschlagen", traceback.format_exc())
    
    # GOTY
    try:
        state.pending_goty_results = {
            "year": 1,
            "my_score": 0,
            "my_game": None,
            "rival_score": 9.5,
            "rival_name": "TestStudio",
            "rival_game": "TestSpiel",
        }
        menu = GOTYMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"GOTYMenu (Verlust) -> {result}")
    except Exception as e:
        log_error("Special", "GOTYMenu fehlgeschlagen", traceback.format_exc())
    
    # GOTY - Spieler gewinnt
    try:
        state.pending_goty_results = {
            "year": 1,
            "my_score": 9.8,
            "my_game": "MeinSpiel",
            "rival_score": 7.0,
            "rival_name": "TestStudio",
            "rival_game": "RivalGame",
        }
        menu = GOTYMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"GOTYMenu (Sieg) -> {result}")
    except Exception as e:
        log_error("Special", "GOTYMenu Sieg fehlgeschlagen", traceback.format_exc())
    
    # AAA Dev Event
    try:
        state.pending_dev_event = {
            "id": "aaa_cgi_leak",
            "options": [
                {
                    "id": "finish",
                    "cost": 2000000,
                    "hype": 100
                },
                {
                    "id": "ignore",
                    "cost": 0,
                    "hype": -50
                }
            ]
        }
        state.money = 5000000
        menu = AAADevEventMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"AAADevEventMenu -> {result}")
    except Exception as e:
        log_error("Special", "AAADevEventMenu fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 10: Edge Cases & Grenzwerte
# ============================================================
def test_edge_cases():
    print("\n" + "="*60)
    print("TEST 10: EDGE CASES & GRENZWERTE")
    print("="*60)
    
    from menus import (GameMenu, TopicMenu, HireMenu, FireMenu, 
                       ServiceMenu, EmailInboxMenu, SequelMenu)
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Edge Test"
    
    # Spiel mit 0 Geld
    state.money = 0
    try:
        menu = GameMenu(audio, state)
        menu.announce_entry()
        log_pass("GameMenu mit 0 Geld funktioniert")
    except Exception as e:
        log_error("EdgeCase", "GameMenu mit 0 Geld crasht", traceback.format_exc())
    
    # Negativem Geld
    state.money = -50000
    try:
        menu = GameMenu(audio, state)
        menu.announce_entry()
        log_pass("GameMenu mit negativem Geld funktioniert")
    except Exception as e:
        log_error("EdgeCase", "GameMenu mit negativem Geld crasht", traceback.format_exc())
    
    state.money = 500000
    
    # Leere Mitarbeiterliste -> Fire
    try:
        state.employees = []
        menu = FireMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"FireMenu mit leerer Liste -> {result}")
    except Exception as e:
        log_error("EdgeCase", "FireMenu mit leerer Mitarbeiterliste crasht", traceback.format_exc())
    
    # Service ohne Spiele
    try:
        state.game_history = []
        menu = ServiceMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"ServiceMenu ohne Spiele -> {result}")
    except Exception as e:
        log_error("EdgeCase", "ServiceMenu ohne Spiele crasht", traceback.format_exc())
    
    # Email inbox leer
    try:
        state.emails = []
        menu = EmailInboxMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"EmailInboxMenu leer -> {result}")
    except Exception as e:
        log_error("EdgeCase", "EmailInboxMenu leer crasht", traceback.format_exc())
    
    # Sequel ohne Spiele
    try:
        state.game_history = []
        menu = SequelMenu(audio, state)
        menu.announce_entry()
        result = menu.handle_input(make_key_event(pygame.K_RETURN))
        log_pass(f"SequelMenu ohne Spiele -> {result}")
    except Exception as e:
        log_error("EdgeCase", "SequelMenu ohne Spiele crasht", traceback.format_exc())
    
    # Extremer Stress-Test: Viele schnelle Eingaben
    try:
        state.money = 500000
        menu = GameMenu(audio, state)
        menu.announce_entry()
        for _ in range(100):
            key = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, 
                                 pygame.K_RETURN, pygame.K_ESCAPE])
            menu.handle_input(make_key_event(key))
        log_pass("GameMenu ueberlebt 100 zufaellige Eingaben")
    except Exception as e:
        log_error("EdgeCase", "GameMenu crasht bei Stress-Test", traceback.format_exc())

# ============================================================
# TEST 11: Sprachen-Wechsel waehrend des Spiels
# ============================================================
def test_language_switch():
    print("\n" + "="*60)
    print("TEST 11: SPRACHWECHSEL")
    print("="*60)
    
    from menus import GameMenu, TopicMenu, HRMenu
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Language Test"
    state.money = 500000
    
    for lang in ['de', 'en', 'de']:
        try:
            set_language(lang)
            state.settings['language'] = lang
            
            menu = GameMenu(audio, state)
            menu.announce_entry()
            
            menu2 = TopicMenu(audio, state)
            menu2.announce_entry()
            
            menu3 = HRMenu(audio, state)
            menu3.announce_entry()
            
            log_pass(f"Alle Menues in '{lang}' funktionieren")
        except Exception as e:
            log_error("Language", f"Menues in '{lang}' fehlgeschlagen", traceback.format_exc())
    
    # Zuruecksetzen
    set_language('de')
    state.settings['language'] = 'de'

# ============================================================
# TEST 12: update_tick Randfaelle
# ============================================================
def test_update_tick_edge_cases():
    print("\n" + "="*60)
    print("TEST 12: UPDATE_TICK RANDFAELLE")
    print("="*60)
    
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    state.company_name = "Tick Test"
    state.money = 500000
    
    # Test mit dt=0
    try:
        state.update_tick(0)
        log_pass("update_tick(0) funktioniert")
    except Exception as e:
        log_error("Tick", "update_tick(0) crasht", traceback.format_exc())
    
    # Test mit sehr grossem dt
    try:
        state.update_tick(100000)
        log_pass("update_tick(100000) funktioniert")
    except Exception as e:
        log_error("Tick", "update_tick(100000) crasht", traceback.format_exc())
    
    # Test mit negativem dt
    try:
        state.update_tick(-1000)
        log_pass("update_tick(-1000) funktioniert")
    except Exception as e:
        log_error("Tick", "update_tick(-1000) crasht", traceback.format_exc())
    
    # Test state update waehrend Forschung
    try:
        state.is_researching = True
        state.research_progress = 0
        state.research_total_weeks = 4
        state.research_type = "feature"
        state.research_item = {"name": "Test Feature", "tech_bonus": 1}
        state.time_speed = 4.0
        for _ in range(200):
            state.update_tick(1000)
        log_pass("update_tick waehrend Forschung funktioniert")
    except Exception as e:
        log_error("Tick", "update_tick waehrend Forschung crasht", traceback.format_exc())

# ============================================================
# TEST 13: Doppelte Keys in Translations pruefen 
# ============================================================
def test_duplicate_translation_keys():
    print("\n" + "="*60)
    print("TEST 13: DOPPELTE KEYS IN TRANSLATIONS")
    print("="*60)
    
    import ast
    
    filepath = os.path.join(game_dir, "translations.py")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Parse the source and find the TRANSLATIONS dict
    # Check for duplicate keys in each language dict
    for lang in ['de', 'en']:
        # Einfacher Ansatz: Zaehle wie oft jeder Key vorkommt
        import re
        # Finde den Sprach-Block
        lang_pattern = f"'{lang}'"
        start_idx = content.find(lang_pattern + ": {")
        if start_idx == -1:
            start_idx = content.find(lang_pattern + ":")
        
        if start_idx == -1:
            log_warning("Translations", f"Sprach-Block '{lang}' nicht gefunden")
            continue
        
        # Zaehle alle Key-Vorkommen im ganzen File
        key_counts = {}
        key_pattern = re.compile(r"'([^']+)':\s*[\"f]")
        
        # Wir extrahieren nur die Keys aus dem jeweiligen Sprach-Block
        brace_count = 0
        in_lang = False
        lang_content = ""
        for i, line in enumerate(content.split('\n')):
            if lang_pattern in line and '{' in line:
                in_lang = True
                brace_count = 0
            if in_lang:
                brace_count += line.count('{') - line.count('}')
                lang_content += line + '\n'
                if brace_count <= 0 and len(lang_content) > 10:
                    break
        
        # Finde doppelte Keys
        for match in key_pattern.finditer(lang_content):
            key = match.group(1)
            key_counts[key] = key_counts.get(key, 0) + 1
        
        duplicates = {k: v for k, v in key_counts.items() if v > 1}
        if duplicates:
            log_error("Translations", f"Doppelte Keys in '{lang}': {duplicates}")
        else:
            log_pass(f"Keine doppelten Keys in '{lang}' ({len(key_counts)} Keys)")

# ============================================================
# TEST 14: main.py simulieren (ohne Pygame-Loop)
# ============================================================
def test_main_simulation():
    print("\n" + "="*60)
    print("TEST 14: MAIN.PY SIMULATION")
    print("="*60)
    
    # Simuliere den main.py Startup-Code
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    
    try:
        state.load_global_settings()
        set_language(state.settings.get('language', 'de'))
        audio.set_music_enabled(state.settings.get('music_enabled', True))
        audio.update_tts_engine(state.settings.get('tts_engine', 'auto'))
        log_pass("main.py Initialisierung simuliert")
    except Exception as e:
        log_error("Main", "Initialisierung fehlgeschlagen", traceback.format_exc())
    
    # Alle Menu-Factories aus main.py testen
    from menus import (MainMenu, CompanyNameMenu, GameMenu, SettingsMenu,
        TopicMenu, GenreMenu, PlatformMenu, AudienceMenu,
        EngineSelectMenu, GameNameMenu, DevelopmentSliderMenu,
        DevProgressMenu, ReviewResultMenu, HRMenu, HireMenu,
        FireMenu, ResearchMenu, FeatureResearchMenu,
        GenreResearchMenu, AudienceResearchMenu,
        EngineCreateNameMenu, EngineFeatureSelectMenu,
        OfficeMenu, GameSizeMenu, MarketingMenu,
        TrainingEmployeeSelectMenu, TrainingOptionMenu,
        BankruptcyMenu, EmailInboxMenu, EmailDetailMenu,
        ServiceMenu, GameServiceOptionsMenu, SaveMenu, LoadMenu,
        HelpMenu, RemasterSelectMenu, PublisherMenu, ExpoMenu,
        BankMenu, LoanMenu, StockMarketMenu, HardwareDevMenu,
        ConsoleNameInput, ConsoleSpecsMenu, GOTYMenu,
        DifficultyMenu, SubGenreMenu, SequelMenu, ChartMenu,
        AAADevEventMenu)
    
    menu_factories = {
        "main_menu": lambda: MainMenu(audio, state),
        "company_name_input": lambda: CompanyNameMenu(audio, state),
        "game_menu": lambda: GameMenu(audio, state),
        "topic_menu": lambda: TopicMenu(audio, state),
        "genre_menu": lambda: GenreMenu(audio, state),
        "platform_menu": lambda: PlatformMenu(audio, state),
        "audience_menu": lambda: AudienceMenu(audio, state),
        "game_size_menu": lambda: GameSizeMenu(audio, state),
        "marketing_menu": lambda: MarketingMenu(audio, state),
        "engine_select_menu": lambda: EngineSelectMenu(audio, state),
        "remaster_select": lambda: RemasterSelectMenu(audio, state),
        "publisher_menu": lambda: PublisherMenu(audio, state),
        "expo_menu": lambda: ExpoMenu(audio, state),
        "game_name_input": lambda: GameNameMenu(audio, state),
        "slider_menu": lambda: DevelopmentSliderMenu(audio, state),
        "dev_progress_menu": lambda: DevProgressMenu(audio, state),
        "review_result": lambda: ReviewResultMenu(audio, state),
        "hr_menu": lambda: HRMenu(audio, state),
        "hire_menu": lambda: HireMenu(audio, state),
        "fire_menu": lambda: FireMenu(audio, state),
        "training_employee_select": lambda: TrainingEmployeeSelectMenu(audio, state),
        "training_option_select": lambda: TrainingOptionMenu(audio, state),
        "research_menu": lambda: ResearchMenu(audio, state),
        "feature_research_menu": lambda: FeatureResearchMenu(audio, state),
        "genre_research_menu": lambda: GenreResearchMenu(audio, state),
        "audience_research_menu": lambda: AudienceResearchMenu(audio, state),
        "engine_create_name": lambda: EngineCreateNameMenu(audio, state),
        "engine_feature_select": lambda: EngineFeatureSelectMenu(audio, state),
        "hardware_dev_menu": lambda: HardwareDevMenu(audio, state),
        "console_name_input": lambda: ConsoleNameInput(audio, state),
        "console_specs_menu": lambda: ConsoleSpecsMenu(audio, state),
        "office_menu": lambda: OfficeMenu(audio, state),
        "bankruptcy": lambda: BankruptcyMenu(audio, state),
        "email_inbox": lambda: EmailInboxMenu(audio, state),
        "email_detail": lambda: EmailDetailMenu(audio, state),
        "service_menu": lambda: ServiceMenu(audio, state),
        "game_service_options": lambda: GameServiceOptionsMenu(audio, state),
        "bank_menu": lambda: BankMenu(audio, state),
        "loan_menu": lambda: LoanMenu(audio, state),
        "stock_market_menu": lambda: StockMarketMenu(audio, state),
        "difficulty_menu": lambda: DifficultyMenu(audio, state),
        "sub_genre_menu": lambda: SubGenreMenu(audio, state),
        "sequel_menu": lambda: SequelMenu(audio, state),
        "chart_menu": lambda: ChartMenu(audio, state),
        "settings_menu": lambda: SettingsMenu(audio, state, lambda: "main_menu"),
        "settings_menu_ingame": lambda: SettingsMenu(audio, state, lambda: "game_menu"),
        "save_menu": lambda: SaveMenu(audio, state),
        "load_menu": lambda: LoadMenu(audio, state),
        "help_menu": lambda: HelpMenu(audio, state),
        "goty_menu": lambda: GOTYMenu(audio, state),
        "aaa_dev_event_menu": lambda: AAADevEventMenu(audio, state),
    }
    
    # Alle Factories instanziieren
    failed = 0
    for key, factory in menu_factories.items():
        try:
            menu = factory()
            # announce 
            menu.announce_entry()
        except Exception as e:
            log_error("MainSim", f"Menu Factory '{key}' crasht", traceback.format_exc())
            failed += 1
    
    if failed == 0:
        log_pass(f"Alle {len(menu_factories)} Menu-Factories aus main.py funktionieren")

# ============================================================
# HAUPTPROGRAMM
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("TIEFGEHENDER END-TO-END-TEST - Audio Studio Tycoon")
    print("="*60)
    
    test_game_start_flow()
    test_dev_pipeline()
    test_hr_pipeline()
    test_research_pipeline()
    test_finance_menus()
    test_office_settings()
    test_email_service()
    test_hardware_menus()
    test_special_menus()
    test_edge_cases()
    test_language_switch()
    test_update_tick_edge_cases()
    test_duplicate_translation_keys()
    test_main_simulation()
    
    # Zusammenfassung
    print("\n" + "="*60)
    print("ZUSAMMENFASSUNG")
    print("="*60)
    print(f"  [OK] Tests bestanden: {tests_passed}")
    print(f"  [X]  Fehler gefunden: {tests_failed}")
    print(f"  [!]  Warnungen: {len(warnings_found)}")
    
    if errors_found:
        print("\n" + "="*60)
        print("ALLE FEHLER:")
        print("="*60)
        for i, err in enumerate(errors_found, 1):
            print(f"  {i}. [{err['category']}] {err['message']}")
            if err['detail']:
                last_line = err['detail'].strip().split('\n')[-1]
                print(f"     -> {last_line}")
    
    if warnings_found:
        print("\n" + "="*60)
        print("ALLE WARNUNGEN:")
        print("="*60)
        for i, warn in enumerate(warnings_found, 1):
            print(f"  {i}. [{warn['category']}] {warn['message']}")
    
    print(f"\n{'='*60}")
    if tests_failed > 0:
        print(f"[X] {tests_failed} FEHLER GEFUNDEN - BITTE BEHEBEN!")
        sys.exit(1)
    else:
        print("[OK] ALLE TESTS BESTANDEN!")
        sys.exit(0)
    
    pygame.quit()
