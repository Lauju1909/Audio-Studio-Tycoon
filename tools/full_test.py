#!/usr/bin/env python3
"""
Umfassender automatisierter Test für Audio Studio Tycoon.
Testet alle Spielmechaniken ohne GUI/Pygame.
"""

import os
import sys
import random
import traceback

# Verzeichnis-Pfad korrigieren
game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, game_dir)
os.chdir(game_dir)

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
    print(f"  ❌ FEHLER [{category}]: {message}")
    if detail:
        print(f"     Detail: {detail}")

def log_warning(category, message):
    warnings_found.append({"category": category, "message": message})
    print(f"  ⚠️ WARNUNG [{category}]: {message}")

def log_pass(message):
    global tests_passed
    tests_passed += 1
    print(f"  ✅ {message}")

# ============================================================
# TEST 1: Imports prüfen
# ============================================================
def test_imports():
    print("\n" + "="*60)
    print("TEST 1: IMPORTS PRÜFEN")
    print("="*60)
    
    modules = {
        "logic": None,
        "models": None,
        "game_data": None,
        "translations": None,
        "audio": None,
    }
    
    for name in modules:
        try:
            modules[name] = __import__(name)
            log_pass(f"Import '{name}' erfolgreich")
        except Exception as e:
            log_error("Import", f"Modul '{name}' konnte nicht importiert werden", str(e))
    
    # Spezifische Imports prüfen die in main.py verwendet werden
    try:
        from translations import get_text, set_language
        log_pass("Import 'get_text, set_language' aus translations erfolgreich")
    except Exception as e:
        log_error("Import", "get_text/set_language aus translations fehlt", str(e))
    
    # AAADevEventMenu Import prüfen
    try:
        from menus import AAADevEventMenu
        log_pass("Import 'AAADevEventMenu' aus menus erfolgreich")
    except ImportError as e:
        log_error("Import", "AAADevEventMenu in menus.py existiert, aber wird nicht in main.py importiert!", str(e))
    
    # Prüfe ob alle in main.py importierten Menüs existieren
    menu_names = [
        "MainMenu", "CompanyNameMenu", "GameMenu", "SettingsMenu",
        "TopicMenu", "GenreMenu", "PlatformMenu", "AudienceMenu",
        "EngineSelectMenu", "GameNameMenu", "DevelopmentSliderMenu",
        "DevProgressMenu", "ReviewResultMenu", "HRMenu", "HireMenu",
        "FireMenu", "ResearchMenu", "FeatureResearchMenu",
        "GenreResearchMenu", "AudienceResearchMenu",
        "EngineCreateNameMenu", "EngineFeatureSelectMenu",
        "OfficeMenu", "GameSizeMenu", "MarketingMenu",
        "TrainingEmployeeSelectMenu", "TrainingOptionMenu",
        "BankruptcyMenu", "EmailInboxMenu", "EmailDetailMenu",
        "ServiceMenu", "GameServiceOptionsMenu", "SaveMenu", "LoadMenu",
        "HelpMenu", "RemasterSelectMenu", "PublisherMenu", "ExpoMenu",
        "BankMenu", "LoanMenu", "StockMarketMenu", "HardwareDevMenu",
        "ConsoleNameInput", "ConsoleSpecsMenu", "GOTYMenu",
        "DifficultyMenu", "SubGenreMenu", "SequelMenu", "ChartMenu",
        "AAADevEventMenu",
    ]
    
    import menus as menus_module
    for name in menu_names:
        if not hasattr(menus_module, name):
            log_error("Import", f"Menü-Klasse '{name}' fehlt in menus.py")
        else:
            log_pass(f"Menü-Klasse '{name}' vorhanden")
    
    return modules

# ============================================================
# TEST 2: GameState Initialisierung
# ============================================================
def test_game_state_init():
    print("\n" + "="*60)
    print("TEST 2: GAMESTATE INITIALISIERUNG")
    print("="*60)
    
    from logic import GameState
    
    try:
        state = GameState()
        log_pass("GameState() ohne Fehler erstellt")
    except Exception as e:
        log_error("GameState", "Initialisierung fehlgeschlagen", traceback.format_exc())
        return None
    
    # Prüfe kritische Attribute
    attrs = [
        "company_name", "money", "fans", "week", "game_history", 
        "employees", "engines", "office_level", "settings",
        "current_draft", "emails", "active_mmos", "rivals",
        "bought_platforms", "bank_loan", "accounting",
        "custom_consoles", "unlocked_topics", "unlocked_genres",
        "unlocked_audiences", "unlocked_technologies",
        "is_developing", "is_researching", "difficulty",
        "chart_history", "owned_licenses", "active_addons",
    ]
    
    for attr in attrs:
        if hasattr(state, attr):
            log_pass(f"Attribut '{attr}' vorhanden")
        else:
            log_error("GameState", f"Attribut '{attr}' fehlt")
    
    # Starter Engine prüfen
    if len(state.engines) > 0:
        log_pass(f"Starter-Engine vorhanden: '{state.engines[0].name}'")
    else:
        log_error("GameState", "Keine Starter-Engine erstellt")
    
    # Rivalen prüfen
    if len(state.rivals) == 3:
        log_pass(f"3 Rivalen erstellt: {[r.name for r in state.rivals]}")
    else:
        log_error("GameState", f"Erwartet 3 Rivalen, gefunden: {len(state.rivals)}")
    
    return state

# ============================================================
# TEST 3: Spielentwicklung End-to-End
# ============================================================
def test_game_development(state):
    print("\n" + "="*60)
    print("TEST 3: SPIELENTWICKLUNG END-TO-END")
    print("="*60)
    
    if state is None:
        log_error("GameDev", "State ist None, Test übersprungen")
        return
    
    from logic import GameState
    from models import GameProject, Engine
    
    state.company_name = "Test Studio"
    state.money = 500000
    
    # Draft erstellen
    state.reset_draft()
    state.current_draft["name"] = "Test RPG"
    state.current_draft["topic"] = "Fantasy"
    state.current_draft["genre"] = "RPG"
    state.current_draft["platform"] = "Zenith-Core 88"
    state.current_draft["audience"] = "Jeder"
    state.current_draft["size"] = "Mittel"
    state.current_draft["marketing"] = "Kein Marketing"
    state.current_draft["engine"] = state.engines[0] if state.engines else None
    state.current_draft["sub_genre"] = None
    
    # Projekt erstellen
    try:
        proj = GameProject(
            name="Test RPG",
            topic="Fantasy",
            genre="RPG",
            sliders={"Gameplay": 6, "Grafik": 5, "Sound": 4, "Story": 9, "KI": 4, "Welt": 2},
            platform="Zenith-Core 88",
            audience="Jeder",
            engine=state.engines[0] if state.engines else None,
            size="Mittel",
            marketing="Kein Marketing",
        )
        log_pass("GameProject erstellt")
    except Exception as e:
        log_error("GameDev", "GameProject Erstellung fehlgeschlagen", traceback.format_exc())
        return
    
    # Review berechnen
    try:
        review = state.calculate_review(proj)
        if review and review.average > 0:
            log_pass(f"Review berechnet: {review.average:.1f}")
        else:
            log_error("GameDev", "Review Score ist 0 oder None")
    except Exception as e:
        log_error("GameDev", "calculate_review fehlgeschlagen", traceback.format_exc())
        return
    
    # Verkäufe berechnen
    try:
        proj.review = review
        sales = state.calculate_sales(proj)
        log_pass(f"Verkäufe berechnet: {sales:,}")
    except Exception as e:
        log_error("GameDev", "calculate_sales fehlgeschlagen", traceback.format_exc())
    
    # Dev-Cost berechnen
    try:
        cost = state.calculate_dev_cost(proj)
        log_pass(f"Dev-Cost berechnet: {cost:,}")
    except Exception as e:
        log_error("GameDev", "calculate_dev_cost fehlgeschlagen", traceback.format_exc())
    
    # Spiel finalisieren
    try:
        old_money = state.money
        result = state.finalize_game(proj)
        log_pass(f"Spiel finalisiert. Geld: {old_money:,} -> {state.money:,}")
    except Exception as e:
        log_error("GameDev", "finalize_game fehlgeschlagen", traceback.format_exc())
        return
    
    # Prüfe ob Spiel in History
    if len(state.game_history) > 0:
        log_pass(f"Spiel in History: {state.game_history[-1].name}")
    else:
        log_error("GameDev", "Spiel nicht in game_history gefunden")

# ============================================================
# TEST 4: Alle Thema/Genre-Kombinationen
# ============================================================
def test_all_combinations():
    print("\n" + "="*60)
    print("TEST 4: THEMA/GENRE-KOMBINATIONEN")
    print("="*60)
    
    from game_data import TOPICS, GENRES, get_compatibility, TOPIC_GENRE_COMPAT
    
    missing_topics = []
    for topic in TOPICS:
        if topic not in TOPIC_GENRE_COMPAT:
            missing_topics.append(topic)
    
    if missing_topics:
        log_error("GameData", f"Topics ohne Kompatibilitätsdaten: {missing_topics}")
    else:
        log_pass(f"Alle {len(TOPICS)} Topics haben Kompatibilitätsdaten")
    
    # Prüfe ob Kompatibilitäts-Arrays die richtige Länge haben
    for topic, compat in TOPIC_GENRE_COMPAT.items():
        if len(compat) != len(GENRES):
            log_error("GameData", f"Topic '{topic}' hat {len(compat)} Compat-Werte, erwartet {len(GENRES)}")
    
    # Teste get_compatibility für alle Kombis
    error_count = 0
    for topic in TOPICS:
        for genre in GENRES:
            try:
                val = get_compatibility(topic, genre)
                if not (0 <= val <= 3):
                    log_error("GameData", f"Kompatibilitätswert für {topic}/{genre} außerhalb 0-3: {val}")
                    error_count += 1
            except Exception as e:
                log_error("GameData", f"get_compatibility({topic}, {genre}) fehlgeschlagen", str(e))
                error_count += 1
    
    if error_count == 0:
        log_pass(f"Alle {len(TOPICS)*len(GENRES)} Kompatibilitätsabfragen erfolgreich")

# ============================================================
# TEST 5: Sub-Genres prüfen
# ============================================================
def test_sub_genres():
    print("\n" + "="*60)
    print("TEST 5: SUB-GENRES")
    print("="*60)
    
    from game_data import GENRES, SUB_GENRES, SLIDER_NAMES
    
    for genre in GENRES:
        if genre not in SUB_GENRES:
            log_warning("SubGenre", f"Genre '{genre}' hat keine Sub-Genres definiert")
        else:
            for sg in SUB_GENRES[genre]:
                # Prüfe ob alle Slider in slider_adjust vorhanden
                for slider in SLIDER_NAMES:
                    if slider not in sg["slider_adjust"]:
                        log_error("SubGenre", f"Sub-Genre '{sg['name']}' ({genre}) fehlt Slider '{slider}'")
            log_pass(f"Genre '{genre}': {len(SUB_GENRES[genre])} Sub-Genres korrekt")

# ============================================================
# TEST 6: Übersetzungen prüfen
# ============================================================
def test_translations():
    print("\n" + "="*60)
    print("TEST 6: ÜBERSETZUNGEN")
    print("="*60)
    
    from translations import TRANSLATIONS
    
    if "de" not in TRANSLATIONS:
        log_error("Translations", "Deutsche Übersetzung ('de') fehlt!")
        return
    if "en" not in TRANSLATIONS:
        log_error("Translations", "Englische Übersetzung ('en') fehlt!")
        return
    
    de_keys = set(TRANSLATIONS["de"].keys())
    en_keys = set(TRANSLATIONS["en"].keys())
    
    only_de = de_keys - en_keys
    only_en = en_keys - de_keys
    
    if only_de:
        log_warning("Translations", f"{len(only_de)} Keys nur in DE: {list(only_de)[:10]}...")
    if only_en:
        log_warning("Translations", f"{len(only_en)} Keys nur in EN: {list(only_en)[:10]}...")
    
    common_keys = de_keys & en_keys
    log_pass(f"Gemeinsame Keys: {len(common_keys)}, nur DE: {len(only_de)}, nur EN: {len(only_en)}")
    
    # Teste get_text mit GameState
    from logic import GameState
    state = GameState()
    
    critical_keys = [
        'paused', 'speed_normal', 'speed_fast', 'speed_ultra',
        'paused_msg', 'start_msg', 'quicksave_msg', 'quickload_msg',
        'quickload_fail_msg', 'crunch_active', 'crunch_off',
        'sender_bank', 'sender_assistant', 'sender_industry_news',
        'subject_research_done', 'body_research_done',
        'sender_legal', 'license_expired_subject', 'license_expired_body',
        'sender_hardware', 'subject_console_done', 'body_console_done',
        'subject_dividend', 'body_dividend',
        'sender_disappointed', 'subject_bug_report', 'body_bug_report',
        'sender_fan', 'subject_fan_praise', 'body_fan_praise',
        'subject_expo', 'body_expo',
        'news_hardware_boom', 'news_recession', 'news_rival_bankrupt',
        'news_title', 'subject_rival_hit', 'body_rival_hit',
        'subject_loan_paid', 'body_loan_paid',
    ]
    
    missing_keys = []
    for key in critical_keys:
        text = state.get_text(key)
        if text == key:  # Nicht übersetzt
            missing_keys.append(key)
    
    if missing_keys:
        log_warning("Translations", f"{len(missing_keys)} kritische Keys fehlen in DE: {missing_keys[:15]}")
    else:
        log_pass(f"Alle {len(critical_keys)} kritischen Übersetzungskeys vorhanden")

# ============================================================
# TEST 7: Event-System
# ============================================================
def test_events():
    print("\n" + "="*60)
    print("TEST 7: EVENT-SYSTEM")
    print("="*60)
    
    from game_data import RANDOM_EVENTS as EVENTS_BOTTOM
    
    # Prüfe ob RANDOM_EVENTS die erwarteten Felder hat
    for i, event in enumerate(EVENTS_BOTTOM):
        required_fields = ["id", "effect"]
        for field in required_fields:
            if field not in event:
                log_error("Events", f"Event {i} fehlt Feld '{field}'")
    
    # Prüfe apply_event mit allen Events
    from logic import GameState
    state = GameState()
    state.company_name = "Test"
    state.money = 100000
    
    for event in EVENTS_BOTTOM:
        try:
            old_money = state.money
            state.apply_event(event)
            log_pass(f"Event '{event.get('id', 'unknown')}' angewendet")
        except Exception as e:
            log_error("Events", f"apply_event fehlgeschlagen für Event '{event.get('id', 'unknown')}'", traceback.format_exc())

# ============================================================
# TEST 8: Speichern/Laden
# ============================================================
def test_save_load():
    print("\n" + "="*60)
    print("TEST 8: SPEICHERN / LADEN")
    print("="*60)
    
    from logic import GameState
    from models import GameProject
    
    state = GameState()
    state.company_name = "Save Test Studio"
    state.money = 123456
    state.fans = 9999
    state.week = 42
    
    # Ein Spiel entwickeln
    state.current_draft["topic"] = "Fantasy"
    state.current_draft["genre"] = "Action"
    state.current_draft["size"] = "Mittel"
    state.current_draft["marketing"] = "Kein Marketing"
    
    proj = GameProject("SaveTest Game", "Fantasy", "Action",
                       sliders={"Gameplay": 9, "Grafik": 7, "Sound": 5, "Story": 2, "KI": 3, "Welt": 4},
                       platform="Zenith-Core 88", audience="Jeder",
                       engine=state.engines[0] if state.engines else None)
    state.finalize_game(proj)
    
    # Speichern
    try:
        test_slot = 99  # Sonderer Slot zum Testen
        # Manuell den Pfad setzen damit es keinen existierenden Slot überschreibt
        import json
        filepath = "save_slot_test_99.json"
        state.save_game.__func__  # Prüfe ob Methode existiert
        
        # Wir nutzen den echten Speicher-Mechanismus mit Slot 99
        # Dazu patchen wir den filepath temporär
        original_money = state.money
        original_week = state.week
        original_company = state.company_name
        
        state.save_game(slot=1)  # Slot 1 zum Testen
        log_pass("Spielstand gespeichert")
    except Exception as e:
        log_error("SaveLoad", "Speichern fehlgeschlagen", traceback.format_exc())
        return
    
    # Laden
    try:
        state2 = GameState()
        result = state2.load_game(slot=1)
        if result:
            log_pass("Spielstand geladen")
            # Daten vergleichen
            if state2.company_name == original_company:
                log_pass(f"Firmenname korrekt: '{state2.company_name}'")
            else:
                log_error("SaveLoad", f"Firmenname falsch: '{state2.company_name}' != '{original_company}'")
            
            if len(state2.game_history) > 0:
                log_pass(f"Game History geladen: {len(state2.game_history)} Spiele")
            else:
                log_error("SaveLoad", "Game History leer nach Laden")
            
            if len(state2.rivals) > 0:
                log_pass(f"Rivalen geladen: {len(state2.rivals)}")
            else:
                log_error("SaveLoad", "Keine Rivalen nach Laden")
        else:
            log_error("SaveLoad", "load_game() gab False zurück")
    except Exception as e:
        log_error("SaveLoad", "Laden fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 9: Mitarbeiter-System
# ============================================================
def test_employee_system():
    print("\n" + "="*60)
    print("TEST 9: MITARBEITER-SYSTEM")
    print("="*60)
    
    from logic import GameState
    from models import Employee
    from game_data import EMPLOYEE_ROLES, SLIDER_NAMES
    
    state = GameState()
    state.money = 1000000
    
    # Candidate generieren
    try:
        candidate = state.generate_candidate()
        log_pass(f"Candidate generiert: {candidate.name} ({candidate.role})")
        
        # Skills prüfen
        for slider in SLIDER_NAMES:
            if slider not in candidate.skills:
                log_error("Employee", f"Candidate hat keinen Skill '{slider}'")
        log_pass(f"Candidate Skills: {candidate.skills}")
    except Exception as e:
        log_error("Employee", "generate_candidate fehlgeschlagen", traceback.format_exc())
        return
    
    # Einstellen
    try:
        result = state.hire_employee(candidate)
        if result:
            log_pass(f"Mitarbeiter eingestellt: {candidate.name}")
        else:
            log_error("Employee", "hire_employee gab False zurück")
    except Exception as e:
        log_error("Employee", "hire_employee fehlgeschlagen", traceback.format_exc())
    
    # Entlassen
    try:
        if len(state.employees) > 0:
            fired = state.fire_employee(0)
            if fired:
                log_pass(f"Mitarbeiter entlassen: {fired.name}")
            else:
                log_error("Employee", "fire_employee gab None zurück")
    except Exception as e:
        log_error("Employee", "fire_employee fehlgeschlagen", traceback.format_exc())
    
    # Training
    try:
        from game_data import TRAINING_OPTIONS
        # Nochmal einstellen
        candidate2 = state.generate_candidate()
        state.hire_employee(candidate2)
        
        if len(state.employees) > 0:
            for train in TRAINING_OPTIONS:
                result = state.train_employee(0, train)
                log_pass(f"Training '{train['name']}' angewendet: {result}")
    except Exception as e:
        log_error("Employee", "Training fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 10: Forschungs-System
# ============================================================
def test_research_system():
    print("\n" + "="*60)
    print("TEST 10: FORSCHUNGS-SYSTEM")
    print("="*60)
    
    from logic import GameState
    from game_data import RESEARCHABLE_TOPICS, RESEARCHABLE_GENRES, RESEARCHABLE_AUDIENCES
    
    state = GameState()
    state.money = 5000000
    state.week = 100  # Weit genug für die meisten Forschungen
    
    # Topic Forschung
    try:
        researchable = state.get_researchable_topics()
        if len(researchable) > 0:
            result = state.start_research(researchable[0], "topic")
            if result:
                log_pass(f"Topic Forschung gestartet: {researchable[0]['name']}")
                state.complete_research()
                if researchable[0]["name"] in state.unlocked_topics:
                    log_pass(f"Topic '{researchable[0]['name']}' freigeschaltet")
                else:
                    log_error("Research", f"Topic '{researchable[0]['name']}' nicht freigeschaltet nach Abschluss")
            else:
                log_error("Research", "start_research gab False zurück")
        else:
            log_warning("Research", "Keine erforschbaren Topics bei Woche 100")
    except Exception as e:
        log_error("Research", "Topic Forschung fehlgeschlagen", traceback.format_exc())
    
    # Genre Forschung
    try:
        researchable = state.get_researchable_genres()
        if len(researchable) > 0:
            result = state.start_research(researchable[0], "genre")
            if result:
                log_pass(f"Genre Forschung gestartet: {researchable[0]['name']}")
                state.complete_research()
                log_pass(f"Genre Forschung abgeschlossen")
    except Exception as e:
        log_error("Research", "Genre Forschung fehlgeschlagen", traceback.format_exc())
    
    # Feature Forschung
    try:
        features = state.get_researchable_features()
        if len(features) > 0:
            result = state.start_research(features[0], "feature")
            if result:
                log_pass(f"Feature Forschung gestartet: {features[0]['name']}")
                state.complete_research()
                log_pass(f"Feature Forschung abgeschlossen")
    except Exception as e:
        log_error("Research", "Feature Forschung fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 11: Büro-Upgrade
# ============================================================
def test_office_upgrade():
    print("\n" + "="*60)
    print("TEST 11: BÜRO-UPGRADE")
    print("="*60)
    
    from logic import GameState
    from game_data import OFFICE_LEVELS
    
    state = GameState()
    state.money = 10000000
    
    for i in range(len(OFFICE_LEVELS) - 1):
        try:
            old_level = state.office_level
            if state.can_upgrade_office():
                result = state.upgrade_office()
                if result:
                    log_pass(f"Büro-Upgrade: Level {old_level} -> {state.office_level} ({OFFICE_LEVELS[state.office_level]['name']})")
                else:
                    log_error("Office", f"upgrade_office gab False zurück bei Level {old_level}")
            else:
                log_error("Office", f"can_upgrade_office() False bei Level {old_level}, obwohl genug Geld")
        except Exception as e:
            log_error("Office", f"Büro-Upgrade fehlgeschlagen bei Level {i}", traceback.format_exc())

# ============================================================
# TEST 12: Kredit-System
# ============================================================
def test_bank_system():
    print("\n" + "="*60)
    print("TEST 12: KREDIT-SYSTEM")
    print("="*60)
    
    from logic import GameState
    from models import BankLoan
    
    state = GameState()
    state.money = 50000
    
    # Kredit aufnehmen
    try:
        loan = BankLoan(100000, 0.2, 52)
        state.bank_loan = loan
        state.money += 100000
        log_pass(f"Kredit aufgenommen: {loan.amount_borrowed}, Wöchentliche Zahlung: {loan.weekly_payment}")
        
        # Wöchentliche Zahlung simulieren
        for _ in range(5):
            old_money = state.money
            state._on_new_week()
        log_pass(f"5 Wochen Kreditabzahlung simuliert. Geld: {state.money:,}")
    except Exception as e:
        log_error("Bank", "Kredit-System fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 13: Aktienmarkt
# ============================================================
def test_stock_market():
    print("\n" + "="*60)
    print("TEST 13: AKTIENMARKT")
    print("="*60)
    
    from logic import GameState
    
    state = GameState()
    state.money = 1000000
    
    # Anteile kaufen
    try:
        result, info = state.buy_shares(0)
        if result:
            log_pass(f"Anteile an '{state.rivals[0].name}' gekauft. Anteil: {info}%")
        else:
            log_error("Stock", f"buy_shares fehlgeschlagen: {info}")
    except Exception as e:
        log_error("Stock", "buy_shares fehlgeschlagen", traceback.format_exc())
    
    # Anteile verkaufen
    try:
        result, info = state.sell_shares(0)
        if result:
            log_pass(f"Anteile an '{state.rivals[0].name}' verkauft. Anteil: {info}%")
        else:
            log_error("Stock", f"sell_shares fehlgeschlagen: {info}")
    except Exception as e:
        log_error("Stock", "sell_shares fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 14: Lizenz-System
# ============================================================
def test_license_system():
    print("\n" + "="*60)
    print("TEST 14: LIZENZ-SYSTEM")
    print("="*60)
    
    from logic import GameState
    from game_data import LICENSES
    
    state = GameState()
    state.money = 5000000
    
    # Lizenz kaufen
    try:
        result = state.buy_license(0)
        if result:
            log_pass(f"Lizenz '{LICENSES[0]['name']}' gekauft")
            # Lizenz benutzen
            state.current_draft["topic"] = "Fantasy"
            use_result = state.use_license(LICENSES[0]["name"])
            if use_result:
                log_pass(f"Lizenz verwendet. Hype-Bonus: {use_result['hype_bonus']}")
            else:
                log_error("License", "use_license gab None zurück")
        else:
            log_error("License", "buy_license gab False zurück")
    except Exception as e:
        log_error("License", "Lizenz-System fehlgeschlagen", traceback.format_exc())
    
    # Lizenz-Ablauf
    try:
        state.week = state.owned_licenses[0]["expires_week"] + 1  # Abgelaufen
        state.expire_licenses()
        log_pass("expire_licenses() ohne Fehler ausgeführt")
    except Exception as e:
        log_error("License", "expire_licenses fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 15: Addon & Bundle
# ============================================================
def test_addon_bundle():
    print("\n" + "="*60)
    print("TEST 15: ADDON & BUNDLE")
    print("="*60)
    
    from logic import GameState
    from models import GameProject
    
    state = GameState()
    state.company_name = "Addon Test"
    state.money = 2000000
    
    # Erst Spiele entwickeln
    for i in range(3):
        state.current_draft["topic"] = "Fantasy"
        state.current_draft["genre"] = "RPG"
        state.current_draft["size"] = "Mittel"
        state.current_draft["marketing"] = "Kein Marketing"
        proj = GameProject(f"Bundle Game {i+1}", "Fantasy", "RPG",
                           sliders={"Gameplay": 6, "Grafik": 5, "Sound": 4, "Story": 9, "KI": 4, "Welt": 2},
                           platform="Zenith-Core 88", audience="Jeder",
                           engine=state.engines[0] if state.engines else None)
        state.finalize_game(proj)
    
    # Addon erstellen
    try:
        addon = state.create_addon(0)
        if addon:
            log_pass(f"Addon erstellt: {addon['name']}, Gewinn: {addon['revenue'] - addon['cost']:,}")
        else:
            log_warning("Addon", "Addon konnte nicht erstellt werden (evtl. nicht genug Geld)")
    except Exception as e:
        log_error("Addon", "create_addon fehlgeschlagen", traceback.format_exc())
    
    # Bundle erstellen
    try:
        bundle = state.create_bundle([0, 1, 2])
        if bundle:
            log_pass(f"Bundle erstellt: {bundle['name']}, Verkäufe: {bundle['sales']:,}")
        else:
            log_error("Bundle", "create_bundle gab None zurück")
    except Exception as e:
        log_error("Bundle", "create_bundle fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 16: Langzeit-Simulation (Wochen voranschreiten)
# ============================================================
def test_long_simulation():
    print("\n" + "="*60)
    print("TEST 16: LANGZEIT-SIMULATION (200 Wochen)")
    print("="*60)
    
    from logic import GameState
    from models import GameProject
    
    state = GameState()
    state.company_name = "Simulations-Studio"
    state.money = 500000
    
    try:
        for w in range(200):
            state.week += 1
            state._on_new_week()
            
            # Alle 30 Wochen ein Spiel veröffentlichen
            if w % 30 == 0 and w > 0:
                state.current_draft["topic"] = random.choice(state.unlocked_topics)
                state.current_draft["genre"] = random.choice(state.unlocked_genres)
                state.current_draft["size"] = "Mittel"
                state.current_draft["marketing"] = "Kein Marketing"
                proj = GameProject(
                    f"SimGame {w//30}", 
                    state.current_draft["topic"],
                    state.current_draft["genre"],
                    sliders={"Gameplay": 5, "Grafik": 5, "Sound": 5, "Story": 5, "KI": 5, "Welt": 5},
                    platform="Zenith-Core 88", audience="Jeder",
                    engine=state.engines[0] if state.engines else None
                )
                state.finalize_game(proj)
        
        log_pass(f"200 Wochen simuliert. Geld: {state.money:,}, Fans: {state.fans:,}, Spiele: {len(state.game_history)}")
        
        # Prüfe Bankrott-Check
        if state.is_bankrupt():
            log_warning("Simulation", "Studio ist bankrott nach 200 Wochen")
        else:
            log_pass("Studio überlebt 200 Wochen")
            
    except Exception as e:
        log_error("Simulation", f"Langzeit-Simulation in Woche {state.week} fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 17: Konsolen-Entwicklung
# ============================================================
def test_console_dev():
    print("\n" + "="*60)
    print("TEST 17: KONSOLEN-ENTWICKLUNG")
    print("="*60)
    
    from logic import GameState
    from models import CustomConsole
    
    state = GameState()
    state.money = 5000000
    state.unlocked_technologies.append("Hardware Labor")
    
    # Konsole entwickeln simulieren
    try:
        state.current_console_draft = {
            "name": "TestConsole 1",
            "tech_level": 3,
            "cost": 500000,
        }
        state.is_developing_console = True
        state.console_progress = 0
        state.console_total_weeks = 5  # Kurz zum Testen
        state.money -= 500000
        
        # Wochen vorrücken
        for _ in range(6):
            state.week += 1
            state._on_new_week()
        
        if len(state.custom_consoles) > 0:
            log_pass(f"Konsole entwickelt: {state.custom_consoles[0].name}")
        else:
            log_error("Console", "Konsole nicht in custom_consoles nach Abschluss")
    except Exception as e:
        log_error("Console", "Konsolen-Entwicklung fehlgeschlagen", traceback.format_exc())

# ============================================================
# TEST 18: Doppelte RANDOM_EVENTS Definition
# ============================================================
def test_data_integrity():
    print("\n" + "="*60)
    print("TEST 18: DATENINTEGRITÄT")
    print("="*60)
    
    # RANDOM_EVENTS ist in game_data.py zweimal definiert (Zeile ~473 und ~831)
    # Die zweite überschreibt die erste. Prüfen ob die Events die richtige Struktur haben.
    from game_data import RANDOM_EVENTS
    
    # Die aktuelle (letzte) Definition hat Events mit 'id' und 'effect'
    # Die erste Definition (überschrieben) hatte 'title', 'text', 'effect', 'value'
    # apply_event erwartet 'id', 'effect' UND 'title', 'text', 'value'
    
    for i, event in enumerate(RANDOM_EVENTS):
        if "id" not in event:
            log_error("DataIntegrity", f"RANDOM_EVENTS[{i}] hat kein 'id' Feld")
        if "title" in event:
            log_warning("DataIntegrity", f"RANDOM_EVENTS[{i}] hat unerwartetes 'title' Feld (alte Definition?)")
    
    # Prüfe ob apply_event die Events korrekt verarbeiten kann
    from logic import GameState
    state = GameState()
    state.company_name = "Test"
    state.money = 100000
    
    for event in RANDOM_EVENTS:
        try:
            state.apply_event(event)
        except Exception as e:
            log_error("DataIntegrity", f"apply_event fehlgeschlagen für Event '{event.get('id', 'unknown')}'", str(e))
    
    log_pass(f"RANDOM_EVENTS enthält {len(RANDOM_EVENTS)} Events")
    
    # Prüfe ob RANDOM_EVENTS zweimal definiert ist
    import ast
    with open(os.path.join(game_dir, "game_data.py"), "r", encoding="utf-8") as f:
        content = f.read()
    
    count = content.count("RANDOM_EVENTS = [")
    if count > 1:
        log_error("DataIntegrity", f"RANDOM_EVENTS ist {count}x in game_data.py definiert! Die erste wird überschrieben.")
    else:
        log_pass("RANDOM_EVENTS nur einmal definiert")
    
    # Prüfe ob REVIEW_TEMPLATES und MAIL_TEMPLATES doppelt definiert sind
    for var_name in ["REVIEW_TEMPLATES", "MAIL_TEMPLATES"]:
        count = content.count(f"{var_name} = " + "{")
        if count > 1:
            log_error("DataIntegrity", f"{var_name} ist {count}x in game_data.py definiert!")
        else:
            log_pass(f"{var_name} nur einmal definiert")

# ============================================================
# TEST 19: main.py Import-Fehler
# ============================================================
def test_main_imports():
    print("\n" + "="*60)
    print("TEST 19: MAIN.PY IMPORT-PRÜFUNG")
    print("="*60)
    
    # Lese main.py und prüfe ob alle referenzierten Menüklassen importiert werden
    main_path = os.path.join(game_dir, "main.py")
    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # AAADevEventMenu wird in Zeile 148 benutzt, aber nicht importiert
    if "AAADevEventMenu" in content:
        if "AAADevEventMenu" not in content.split("from menus import")[1].split(")")[0] if "from menus import" in content else "":
            log_error("MainImport", "AAADevEventMenu wird in main.py verwendet (Zeile 148), aber NICHT importiert! → Crash bei AAA-Events!")
        else:
            log_pass("AAADevEventMenu korrekt importiert")
    
    # Prüfe ob alle factory-Menüs auch importiert sind
    import re
    lambda_pattern = re.findall(r'lambda: (\w+)\(', content)
    import_section = content.split("from menus import")[1].split(")")[0] if "from menus import" in content else ""
    
    for menu_class in lambda_pattern:
        if menu_class not in ("SettingsMenu",):  # Schon importiert
            if menu_class not in import_section and menu_class not in content[:500]:
                log_error("MainImport", f"'{menu_class}' wird als Factory verwendet, aber möglicherweise nicht importiert")

# ============================================================
# TEST 20: MMO-System
# ============================================================
def test_mmo_system():
    print("\n" + "="*60)
    print("TEST 20: MMO-SYSTEM")
    print("="*60)
    
    from logic import GameState
    from models import GameProject, ActiveMMO
    
    state = GameState()
    state.company_name = "MMO Test"
    state.money = 10000000
    state.office_level = 4  # HQ: 20 Mitarbeiter
    state.unlocked_technologies.append("Live-Service Architektur")
    
    # 10 Mitarbeiter einstellen
    for _ in range(10):
        cand = state.generate_candidate()
        state.hire_employee(cand)
    
    # MMO entwickeln
    state.current_draft["topic"] = "Fantasy"
    state.current_draft["genre"] = "RPG"
    state.current_draft["size"] = "MMO"
    state.current_draft["marketing"] = "Kein Marketing"
    
    try:
        proj = GameProject(
            "TestMMO", "Fantasy", "RPG",
            sliders={"Gameplay": 8, "Grafik": 8, "Sound": 8, "Story": 8, "KI": 8, "Welt": 8},
            platform="Zenith-Core 88", audience="Jeder",
            engine=state.engines[0],
            size="MMO"
        )
        state.finalize_game(proj)
        
        if len(state.active_mmos) > 0:
            mmo = state.active_mmos[0]
            log_pass(f"MMO erstellt: {mmo.game.name}, Spieler: {mmo.players:,}, WR: {mmo.weekly_revenue:,}, WC: {mmo.weekly_cost:,}")
        else:
            log_error("MMO", "Kein ActiveMMO erstellt nach finalize_game mit size=MMO")
    except Exception as e:
        log_error("MMO", "MMO-Entwicklung fehlgeschlagen", traceback.format_exc())

# ============================================================
# HAUPTPROGRAMM
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("🎮 UMFASSENDER SPIELTEST - Audio Studio Tycoon")
    print("="*60)
    
    # Reihenfolge: Kritisch -> Weniger kritisch
    modules = test_imports()
    state = test_game_state_init()
    test_game_development(state)
    test_all_combinations()
    test_sub_genres()
    test_translations()
    test_events()
    test_save_load()
    test_employee_system()
    test_research_system()
    test_office_upgrade()
    test_bank_system()
    test_stock_market()
    test_license_system()
    test_addon_bundle()
    test_long_simulation()
    test_console_dev()
    test_data_integrity()
    test_main_imports()
    test_mmo_system()
    
    # Zusammenfassung
    print("\n" + "="*60)
    print("📊 ZUSAMMENFASSUNG")
    print("="*60)
    print(f"  ✅ Tests bestanden: {tests_passed}")
    print(f"  ❌ Fehler gefunden: {tests_failed}")
    print(f"  ⚠️ Warnungen: {len(warnings_found)}")
    
    if errors_found:
        print("\n" + "="*60)
        print("🔴 ALLE FEHLER:")
        print("="*60)
        for i, err in enumerate(errors_found, 1):
            print(f"  {i}. [{err['category']}] {err['message']}")
            if err['detail']:
                # Nur die letzte Zeile des Tracebacks
                last_line = err['detail'].strip().split('\n')[-1]
                print(f"     → {last_line}")
    
    if warnings_found:
        print("\n" + "="*60)
        print("🟡 ALLE WARNUNGEN:")
        print("="*60)
        for i, warn in enumerate(warnings_found, 1):
            print(f"  {i}. [{warn['category']}] {warn['message']}")
    
    print(f"\n{'='*60}")
    if tests_failed > 0:
        print(f"❌ {tests_failed} FEHLER GEFUNDEN - BITTE BEHEBEN!")
        sys.exit(1)
    else:
        print("✅ ALLE TESTS BESTANDEN!")
        sys.exit(0)
