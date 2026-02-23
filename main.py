"""
Audio Studio Tycoon - Audio Edition
Hauptprogramm & Spielschleife

100% Screenreader-optimiert (NVDA).
Steuerung: Pfeiltasten + Enter + Buchstaben für Texteingabe.
"""

import pygame
import time
import os
from audio import AudioManager
from logic import GameState
from translations import get_text, set_language
from menus import (
    MainMenu,
    CompanyNameMenu,
    GameMenu,
    SettingsMenu,
    TopicMenu,
    GenreMenu,
    PlatformMenu,
    AudienceMenu,
    EngineSelectMenu,
    GameNameMenu,
    DevelopmentSliderMenu,
    DevProgressMenu,
    ReviewResultMenu,
    HRMenu,
    HireMenu,
    FireMenu,
    ResearchMenu,
    FeatureResearchMenu,
    EngineCreateNameMenu,
    EngineFeatureSelectMenu,
    OfficeMenu,
    GameSizeMenu,
    MarketingMenu,
    TrainingEmployeeSelectMenu,
    TrainingOptionMenu,
    BankruptcyMenu,
    EmailInboxMenu,
    EmailDetailMenu,
    ServiceMenu,
    GameServiceOptionsMenu,
    SaveMenu,
    LoadMenu,
    HelpMenu,
    RemasterSelectMenu,
    PublisherMenu,
    ExpoMenu,
    BankMenu,
    LoanMenu,
    HardwareDevMenu,
    ConsoleNameInput,
    ConsoleSpecsMenu,
    GOTYMenu,
)


def main():
    # ---- Initialisierung ----
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Audio Studio Tycoon - Audio Edition")
    audio = AudioManager()
    os.system("cls" if os.name == "nt" else "clear")

    state = GameState()
    state.audio = audio  # Audio-Instanz für globale Text-Ausgaben in Models
    
    # NEU: Globale Einstellungen sofort beim Start laden
    state.load_global_settings()
    set_language(state.settings.get('language', 'de'))
    audio.set_music_enabled(state.settings.get('music_enabled', True))
    audio.update_tts_engine(state.settings.get('tts_engine', 'auto'))

    # Umbau: Dynamische Menü-Generierung über Lambda-Funktionen
    menu_factories = {
        # Haupt-Flow
        "main_menu": lambda: MainMenu(audio, state),
        "company_name_input": lambda: CompanyNameMenu(audio, state),
        "game_menu": lambda: GameMenu(audio, state),

        # Spielentwicklung
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

        # Personal
        "hr_menu": lambda: HRMenu(audio, state),
        "hire_menu": lambda: HireMenu(audio, state),
        "fire_menu": lambda: FireMenu(audio, state),
        "training_employee_select": lambda: TrainingEmployeeSelectMenu(audio, state),
        "training_option_select": lambda: TrainingOptionMenu(audio, state),

        # Forschung & Engines
        "research_menu": lambda: ResearchMenu(audio, state),
        "feature_research_menu": lambda: FeatureResearchMenu(audio, state),
        "engine_create_name": lambda: EngineCreateNameMenu(audio, state),
        "engine_feature_select": lambda: EngineFeatureSelectMenu(audio, state),
        "hardware_dev_menu": lambda: HardwareDevMenu(audio, state),
        "console_name_input": lambda: ConsoleNameInput(audio, state),
        "console_specs_menu": lambda: ConsoleSpecsMenu(audio, state),

        # Büro
        "office_menu": lambda: OfficeMenu(audio, state),

        # Spezial
        "bankruptcy": lambda: BankruptcyMenu(audio, state),
        "email_inbox": lambda: EmailInboxMenu(audio, state),
        "email_detail": lambda: EmailDetailMenu(audio, state),
        "service_menu": lambda: ServiceMenu(audio, state),
        "game_service_options": lambda: GameServiceOptionsMenu(audio, state),
        "bank_menu": lambda: BankMenu(audio, state),
        "loan_menu": lambda: LoanMenu(audio, state),
        "settings_menu": lambda: SettingsMenu(audio, state, lambda: "main_menu"),
        "settings_menu_ingame": lambda: SettingsMenu(audio, state, lambda: "game_menu"),
        "save_menu": lambda: SaveMenu(audio, state),
        "load_menu": lambda: LoadMenu(audio, state),
        "help_menu": lambda: HelpMenu(audio, state),
        "goty_menu": lambda: GOTYMenu(audio, state),
    }

    current_key = "main_menu"
    current_menu = menu_factories[current_key]()

    # ---- Willkommensnachricht ----
    audio.speak(get_text("main_welcome"))
    time.sleep(0.3)
    audio.play_music("music_back")
    current_menu.announce_entry()

    # ---- Hauptschleife ----
    running = True
    clock = pygame.time.Clock()
    last_tick_time = pygame.time.get_ticks()

    while running:
        current_time_ms = pygame.time.get_ticks()
        dt = current_time_ms - last_tick_time
        last_tick_time = current_time_ms

        # Zeit-Logik im State aktualisieren
        state.update_tick(dt)

        # Update-Logik (Fortschrittsbalken etc.)
        if hasattr(current_menu, 'update'):
            current_menu.update()

        # Pleite-Check
        if state.is_bankrupt() and current_key != "bankruptcy":
            current_key = "bankruptcy"
            current_menu = menu_factories[current_key]()
            current_menu.announce_entry()
            
        # GOTY-Check
        goty = getattr(state, "pending_goty_results", None)
        if goty and current_key not in ["goty_menu", "bankruptcy"]:
            current_key = "goty_menu"
            current_menu = menu_factories[current_key]()
            current_menu.announce_entry()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                result = current_menu.handle_input(event)

                if result == "quit":
                    running = False
                elif result and result in menu_factories:
                    current_key = result
                    current_menu = menu_factories[current_key]()
                    current_menu.announce_entry()
                
                # Zeitsteuerung (Hotkeys)
                elif event.key == pygame.K_SPACE:
                    if state.time_speed > 0:
                        state.time_speed = 0
                        audio.speak(state.get_text('paused_msg'))
                    else:
                        state.time_speed = 1.0
                        audio.speak(state.get_text('start_msg'))
                elif event.key == pygame.K_1:
                    state.time_speed = 1.0
                    audio.speak(state.get_text('time_speed_speech', speed=state.get_text('speed_1')))
                elif event.key == pygame.K_2:
                    state.time_speed = 2.0
                    audio.speak(state.get_text('time_speed_speech', speed=state.get_text('speed_2')))
                elif event.key == pygame.K_3:
                    state.time_speed = 4.0
                    audio.speak(state.get_text('time_speed_speech', speed=state.get_text('speed_3')))
                elif event.key == pygame.K_s:
                    if current_key not in ["main_menu", "company_name_input", "bankruptcy"]:
                        state.save_game(slot=1)
                        # Bonus: Kurzes Speichergeräusch abspielen
                        if hasattr(audio, 'play_sound'): audio.play_sound('blip')
                        audio.speak(state.get_text('quicksave_msg'))
                elif event.key == pygame.K_l:
                    if current_key not in ["company_name_input", "bankruptcy"]:
                        if state.load_game(slot=1):
                            # Bonus: Lade-Geräusch
                            if hasattr(audio, 'play_sound'): audio.play_sound('blip')
                            audio.speak(state.get_text('quickload_msg'))
                            current_key = "game_menu"
                            current_menu = menu_factories[current_key]()
                            current_menu.announce_entry()
                        else:
                            if hasattr(audio, 'play_sound'): audio.play_sound('error')
                            audio.speak(state.get_text('quickload_fail_msg'))
                elif event.key == pygame.K_c:
                    state.crunch_active = not state.crunch_active
                    audio.speak(state.get_text('crunch_active' if state.crunch_active else 'crunch_off'))
                    if state.crunch_active:
                        audio.speak(state.get_text('crunch_info'), interrupt=False)
                elif event.key == pygame.K_j:
                    audio.speak(state.get_calendar_text())
                elif event.key == pygame.K_m:
                    if not state.is_developing:
                        audio.speak(state.get_text('marketing_simulated'))
                        # M-Taste ruft simuliertes Marketing auf
                        current_key = "marketing_menu"
                        current_menu = menu_factories[current_key]()
                        current_menu.announce_entry()
                    else:
                        audio.speak(state.get_text('marketing_blocked'))

        # Fenster aktualisieren
        screen.fill((10, 10, 20))

        try:
            font = pygame.font.SysFont("Arial", 13)

            # Header
            header = font.render(
                f"[{state.company_name or get_text('main_title')}] "
                f"{state.get_text('money', money=state.money)} | "
                f"{state.get_text('fans')}: {state.fans:,} | "
                f"{state.get_calendar_text()} ({state.get_speed_text()})",
                True, (80, 200, 80)
            )
            screen.blit(header, (10, 10))

            # Dev-Status (falls aktiv)
            if state.is_developing:
                crunch_txt = f" | {state.get_text('crunch_active')}" if state.crunch_active else ""
                dev_info = font.render(
                    f"{state.get_text('progress')}: {int(state.dev_progress)}/{state.dev_total_weeks} Ww. | "
                    f"Bugs: {state.current_bugs}{crunch_txt}",
                    True, (255, 150, 50)
                )
                screen.blit(dev_info, (10, 30))
                y_offset = 50
            else:
                y_offset = 30

            # Team-Info
            from game_data import OFFICE_LEVELS
            office = OFFICE_LEVELS[state.office_level]
            team_text = font.render(
                f"{state.get_text('office')}: {office['name']} | "
                f"Mitarbeiter: {len(state.employees)}/{office['max_employees']} | "
                f"Engines: {len(state.engines)}",
                True, (100, 150, 200)
            )
            screen.blit(team_text, (10, y_offset))

            # Menü-Info
            menu_info = font.render(f"{state.get_text('current_menu')}: {current_key}", True, (150, 150, 150))
            screen.blit(menu_info, (10, 50))

            # Trend-Info
            if state.current_trend:
                txt = f"{state.get_text('trend')}: {state.current_trend['topic']} / {state.current_trend['genre']}"
                trend_v = font.render(txt, True, (255, 100, 100))
                screen.blit(trend_v, (10, 70))

            # Screenreader-Hinweis
            hint = font.render(
                get_text('main_screenreader_hint'),
                True, (60, 60, 60)
            )
            screen.blit(hint, (10, 275))
        except Exception:
            pass

        pygame.display.flip()
        clock.tick(30)

    # ---- Aufräumen ----
    audio.cleanup()
    pygame.quit()


if __name__ == "__main__":
    main()
