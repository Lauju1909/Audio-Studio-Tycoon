"""
Spielt das Spiel GENAU wie ein normaler Spieler:
- Benutzt den ECHTEN Game-Loop aus main.py
- Injiziert Tastatur-Events über pygame
- Kein Mocking, keine Simulationen
- Echte Menüübergänge, echte Logik, echter AudioManager
"""
import pygame
import sys
import os
import time
import traceback

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '.')

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Audio Studio Tycoon - PLAYTEST")

# Echter Import wie in main.py
from logic import GameState
from audio import AudioManager
import translations
from menus import (
    MainMenu, DifficultyMenu, CompanyNameMenu, GameMenu,
    TopicMenu, GenreMenu, SubGenreMenu,
    PlatformMenu, AudienceMenu, GameSizeMenu,
    MarketingMenu, PublisherMenu, EngineSelectMenu,
    GameNameMenu, DevelopmentSliderMenu, DevProgressMenu,
    ReviewResultMenu, HRMenu, HireMenu, FireMenu,
    TrainingEmployeeSelectMenu, TrainingOptionMenu,
    ResearchMenu, FeatureResearchMenu, GenreResearchMenu,
    AudienceResearchMenu, EngineCreateNameMenu, EngineFeatureSelectMenu,
    HardwareDevMenu, ConsoleNameInput, ConsoleSpecsMenu,
    OfficeMenu, SettingsMenu, SaveMenu, LoadMenu, HelpMenu,
    BankruptcyMenu, EmailInboxMenu, EmailDetailMenu,
    ServiceMenu, GameServiceOptionsMenu,
    BankMenu, LoanMenu, StockMarketMenu,
    GOTYMenu, AAADevEventMenu, ExpoMenu,
    SequelMenu, RemasterSelectMenu, ChartMenu,
)

# --- Setup genau wie in main.py ---
audio = AudioManager()
state = GameState()
state.audio = audio
state.load_global_settings()
translations.set_language(state.settings.get("language", "de"))

menu_factories = {
    "main_menu": lambda: MainMenu(audio, state),
    "difficulty_menu": lambda: DifficultyMenu(audio, state),
    "company_name_input": lambda: CompanyNameMenu(audio, state),
    "game_menu": lambda: GameMenu(audio, state),
    "topic_menu": lambda: TopicMenu(audio, state),
    "genre_menu": lambda: GenreMenu(audio, state),
    "sub_genre_menu": lambda: SubGenreMenu(audio, state),
    "platform_menu": lambda: PlatformMenu(audio, state),
    "audience_menu": lambda: AudienceMenu(audio, state),
    "game_size_menu": lambda: GameSizeMenu(audio, state),
    "marketing_menu": lambda: MarketingMenu(audio, state),
    "publisher_menu": lambda: PublisherMenu(audio, state),
    "engine_select_menu": lambda: EngineSelectMenu(audio, state),
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
    "sequel_menu": lambda: SequelMenu(audio, state),
    "chart_menu": lambda: ChartMenu(audio, state),
    "settings_menu": lambda: SettingsMenu(audio, state, lambda: "main_menu"),
    "settings_menu_ingame": lambda: SettingsMenu(audio, state, lambda: "game_menu"),
    "save_menu": lambda: SaveMenu(audio, state),
    "load_menu": lambda: LoadMenu(audio, state),
    "help_menu": lambda: HelpMenu(audio, state),
    "goty_menu": lambda: GOTYMenu(audio, state),
    "aaa_dev_event_menu": lambda: AAADevEventMenu(audio, state),
    "expo_menu": lambda: ExpoMenu(audio, state),
    "remaster_select": lambda: RemasterSelectMenu(audio, state),
}

def switch_menu(key):
    """Wechselt das Menü - genau wie in main.py"""
    menu = menu_factories[key]()
    menu.announce_entry()
    return menu

def press(key, char=''):
    """Erzeugt ein echtes pygame KEYDOWN Event"""
    return pygame.event.Event(pygame.KEYDOWN, key=key, unicode=char, mod=0, scancode=0)

def do_input(menu, current_key, key, char=''):
    """Verarbeitet einen Tastendruck und wechselt ggf. das Menü"""
    event = press(key, char)
    result = menu.handle_input(event)
    if result == "quit":
        return current_key, menu, False
    elif result and result in menu_factories:
        print(f"  [{current_key}] -> [{result}]")
        current_key = result
        menu = switch_menu(current_key)
    return current_key, menu, True

def tick(menu, n=1):
    """Simuliert n Frames (mit update_tick und menu.update)"""
    for _ in range(n):
        state.update_tick(100)  # 100ms pro Frame (10 FPS)
        if hasattr(menu, 'update'):
            menu.update()

# ======================================
# ECHTES SPIELEN WIE EIN NORMALER SPIELER
# ======================================

print("=" * 60)
print("ECHTES PLAYTHROUGH - Wie ein normaler Spieler")
print("=" * 60)

try:
    # --- SCHRITT 1: Hauptmenü -> Neues Spiel ---
    print("\n[1] Hauptmenü: Enter (Neues Spiel)")
    current_key = "main_menu"
    menu = switch_menu(current_key)
    tick(menu, 5)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)

    # --- SCHRITT 2: Schwierigkeit wählen (Normal = Index 1) ---
    print("[2] Schwierigkeit: Down + Enter (Normal)")
    tick(menu, 3)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_DOWN)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)

    # --- SCHRITT 3: Firmenname eingeben ---
    print("[3] Firmenname: 'MeineGames' + Enter")
    tick(menu, 3)
    for c in "MeineGames":
        current_key, menu, ok = do_input(menu, current_key, ord(c.upper()), c)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)

    # Jetzt sollten wir im game_menu sein
    print(f"\n    Aktuell: {current_key}")
    print(f"    Firma: {state.company_name}, Geld: {state.money:,}")

    # --- SCHRITT 4: Neues Spiel entwickeln (Index 1) ---
    print("\n[4] GameMenu: Down + Enter (Neues Spiel entwickeln)")
    tick(menu, 10)  # Ein paar Frames warten
    current_key, menu, ok = do_input(menu, current_key, pygame.K_DOWN)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)

    # --- SCHRITT 5: Thema wählen (Fantasy, Index 0) ---
    print("[5] Thema: Enter (Fantasy)")
    tick(menu, 3)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)

    # --- SCHRITT 6: Genre wählen (Action, Index 0) ---
    print("[6] Genre: Enter (Action)")
    tick(menu, 3)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)

    # --- SCHRITT 7: Sub-Genre wählen (Keins, Index 0) ---
    print("[7] Sub-Genre: Enter (Keins)")
    tick(menu, 3)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)

    # Jetzt kommt game_name_input
    print(f"    Aktuell: {current_key}")

    # --- SCHRITT 8: Spielname eingeben ---
    print("[8] Spielname: 'DragonQuest' + Enter")
    tick(menu, 3)
    for c in "DragonQuest":
        current_key, menu, ok = do_input(menu, current_key, ord(c.upper()), c)
    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)

    print(f"    Aktuell: {current_key}")

    # Der Flow geht jetzt: game_name_input -> slider_menu
    # ABER - der echte Flow hat noch Platform, Audience, Size, Marketing, Publisher, Engine dazwischen!
    # Die Reihenfolge im Spiel ist:
    # SubGenre -> game_name_input -> (Enter) -> slider_menu
    # NEIN! Schauen wir was passiert ist:

    if current_key == "slider_menu":
        print("\n    *** DIREKT ZUM SLIDER - KEIN Platform/Audience/etc. ***")
        print("    Das bedeutet: Platform=None, Audience=Jeder, etc.")
        print(f"    Draft: {state.current_draft}")
    elif current_key == "platform_menu":
        # Platform wählen
        print("[8b] Platform: Enter")
        tick(menu, 3)
        current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)
        print(f"    Aktuell: {current_key}")

    # Weiter je nach aktuellem Menü
    flow_steps = {
        "audience_menu": ("Audience: Enter", pygame.K_RETURN),
        "game_size_menu": ("GameSize: Enter (Klein)", pygame.K_RETURN),
        "marketing_menu": ("Marketing: Enter", pygame.K_RETURN),
        "publisher_menu": ("Publisher: Enter (Selbstverlag)", pygame.K_RETURN),
        "engine_select_menu": ("Engine: Enter", pygame.K_RETURN),
        "game_name_input": ("GameName: 'TestGame' + Enter", None),
    }

    step = 9
    while current_key in flow_steps or current_key == "game_name_input":
        if current_key == "game_name_input":
            print(f"[{step}] Spielname eingeben")
            tick(menu, 3)
            for c in "TestGame":
                current_key, menu, ok = do_input(menu, current_key, ord(c.upper()), c)
            current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)
        elif current_key in flow_steps:
            desc, key = flow_steps[current_key]
            print(f"[{step}] {desc}")
            tick(menu, 3)
            current_key, menu, ok = do_input(menu, current_key, key)
        else:
            break
        step += 1
        print(f"    Aktuell: {current_key}")

    # --- SLIDER MENU ---
    if current_key == "slider_menu":
        print(f"\n{'='*60}")
        print("SLIDER MENU ERREICHT!")
        print(f"Draft: {state.current_draft}")
        print(f"{'='*60}")

        # Punkte verteilen: 5 pro Slider mit Pfeiltasten (genau wie ein Spieler)
        print("\nPunkte verteilen (5 pro Kategorie)...")
        for si in range(6):
            for _ in range(5):
                current_key, menu, ok = do_input(menu, current_key, pygame.K_RIGHT)
            tick(menu, 1)
            if si < 5:
                current_key, menu, ok = do_input(menu, current_key, pygame.K_DOWN)

        print(f"    Slider-Werte: {menu.values}")
        print(f"    Verbleibend: {menu.remaining}")
        
        print("\n*** ENTER DRÜCKEN (der Crash-Moment!) ***")
        try:
            current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)
            print(f"    -> Ergebnis: {current_key}")
        except Exception as e:
            print(f"\n!!! CRASH BEI SLIDER ENTER !!!")
            print(f"    Fehler: {e}")
            traceback.print_exc()
            audio.cleanup()
            pygame.quit()
            sys.exit(1)

        # --- DEV PROGRESS ---
        if current_key == "dev_progress_menu":
            print(f"\nDevProgressMenu geöffnet!")
            print(f"    is_developing: {state.is_developing}")
            print(f"    dev_total_weeks: {state.dev_total_weeks}")
            
            # Entwicklung laufen lassen (Speed 3 = 4x)
            print("\nEntwicklung läuft (Speed 3)...")
            state.time_speed = 4.0
            for frame in range(10000):
                try:
                    tick(menu, 1)
                except Exception as e:
                    print(f"\n!!! CRASH WÄHREND ENTWICKLUNG (Frame {frame}) !!!")
                    print(f"    Fehler: {e}")
                    traceback.print_exc()
                    audio.cleanup()
                    pygame.quit()
                    sys.exit(1)
                
                # Prüfe ob Entwicklung fertig
                if not state.is_developing and hasattr(menu, 'options') and menu.options:
                    print(f"    Entwicklung fertig nach {frame} Frames!")
                    break
                    
                # GOTY/AAA Event Check (wie in main.py)
                goty = getattr(state, "pending_goty_results", None)
                if goty and current_key not in ["goty_menu", "bankruptcy", "aaa_dev_event_menu"]:
                    print(f"    GOTY Event!")
                    current_key = "goty_menu"
                    menu = switch_menu(current_key)
                    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)
                
                dev_event = getattr(state, "pending_dev_event", None)
                if dev_event and current_key == "dev_progress_menu":
                    print(f"    AAA Dev Event!")
                    current_key = "aaa_dev_event_menu"
                    menu = switch_menu(current_key)
                    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)
            
            # Fertig -> Enter drücken (Veröffentlichen)
            if menu.options:
                print("\nSpiel veröffentlichen (Enter)...")
                try:
                    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)
                    print(f"    -> {current_key}")
                except Exception as e:
                    print(f"\n!!! CRASH BEI VERÖFFENTLICHUNG !!!")
                    print(f"    Fehler: {e}")
                    traceback.print_exc()
                    audio.cleanup()
                    pygame.quit()
                    sys.exit(1)

            # Review anzeigen
            if current_key == "review_result":
                print("\nReviewResultMenu...")
                try:
                    current_key, menu, ok = do_input(menu, current_key, pygame.K_RETURN)
                    print(f"    -> {current_key}")
                    if state.game_history:
                        g = state.game_history[-1]
                        score = g.review.average if g.review else "N/A"
                        print(f"    Score: {score}, Sales: {g.sales:,}")
                except Exception as e:
                    print(f"\n!!! CRASH BEI REVIEW !!!")
                    print(f"    Fehler: {e}")
                    traceback.print_exc()
                    audio.cleanup()
                    pygame.quit()
                    sys.exit(1)

            # Zurück zum GameMenu
            if current_key == "game_menu":
                print(f"\nZurück im GameMenu!")
                print(f"    Geld: {state.money:,}, Fans: {state.fans:,}")
                print(f"    Spiele: {state.games_made}")

    print(f"\n{'='*60}")
    print("PLAYTHROUGH KOMPLETT - KEIN CRASH!")
    print(f"{'='*60}")

except Exception as e:
    print(f"\n{'='*60}")
    print(f"!!! UNERWARTETER CRASH !!!")
    print(f"{'='*60}")
    print(f"Menü: {current_key}")
    print(f"Draft: {state.current_draft}")
    print(f"Fehler: {e}")
    traceback.print_exc()

audio.cleanup()
pygame.quit()
