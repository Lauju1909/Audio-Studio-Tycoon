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
    MainMenu, UpdateConfirmMenu, CompanyNameMenu, GameMenu, TopicMenu,
    GenreMenu, PlatformMenu, AudienceMenu, GameSizeMenu, MarketingMenu,
    EngineSelectMenu, RemasterSelectMenu, PublisherMenu, SettingsMenu,
    VolumeSettingsMenu, KeybindingMenu, ExpoMenu, GameNameMenu,
    DevelopmentSliderMenu, DevProgressMenu, ReviewResultMenu,
    HRMenu, HireMenu, FireMenu, TrainingEmployeeSelectMenu,
    TrainingOptionMenu, ResearchMenu, FeatureResearchMenu,
    GenreResearchMenu, TopicResearchMenu, AudienceResearchMenu,
    TechnologyResearchMenu, EngineCreateNameMenu, EngineFeatureSelectMenu,
    HardwareDevMenu, ConsoleNameInput, ConsoleSpecsMenu, OfficeMenu,
    BankruptcyMenu, EmailInboxMenu, EmailDetailMenu, ServiceMenu,
    GameServiceOptionsMenu, BankMenu, LoanMenu, StockMarketMenu,
    DifficultyMenu, SubGenreMenu, SequelMenu, ChartMenu,
    LicenseShopMenu, LicenseSelectMenu, AddonMenu, AddonNameMenu,
    BundleMenu, BundleNameMenu, ProductionMenu, ProductionAmountMenu,
    MMOPaymentMenu, MMOManagementMenu, MMOOptionsMenu,
    PublisherDealsMenu, PublisherDealDetailsMenu, MerchMenu, MerchAmountMenu,
    ESportsMenu, AcquisitionMenu, StockRivalDetailMenu,
    SaveMenu, LoadMenu, HelpMenu, GOTYMenu, AAADevEventMenu, CreditsMenu,
    BuildMenu, TeambuildingMenu, ModPortalMenu, ModBrowserListMenu
)

def get_menu_factories(audio, state):
    """Gibt Factory-Funktionen für alle Menüs zurück."""
    return {
        "main_menu": lambda: MainMenu(audio, state),
        "update_confirm_menu": lambda: UpdateConfirmMenu(audio, state),
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
        "settings_menu": lambda: SettingsMenu(audio, state, lambda: "main_menu"),
        "volume_settings_menu": lambda: VolumeSettingsMenu(audio, state),
        "keybinding_menu": lambda: KeybindingMenu(audio, state),
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
        "topic_research_menu": lambda: TopicResearchMenu(audio, state),
        "audience_research_menu": lambda: AudienceResearchMenu(audio, state),
        "technology_research_menu": lambda: TechnologyResearchMenu(audio, state),
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
        "license_shop_menu": lambda: LicenseShopMenu(audio, state),
        "license_select_menu": lambda: LicenseSelectMenu(audio, state),
        "addon_menu": lambda: AddonMenu(audio, state),
        "bundle_menu": lambda: BundleMenu(audio, state),
        "production_menu": lambda: ProductionMenu(audio, state),
        "production_amount_menu": lambda: ProductionAmountMenu(audio, state),
        "mmo_payment_menu": lambda: MMOPaymentMenu(audio, state),
        "mmo_management_menu": lambda: MMOManagementMenu(audio, state),
        "mmo_options_menu": lambda: MMOOptionsMenu(audio, state),
        "publisher_deals_menu": lambda: PublisherDealsMenu(audio, state),
        "publisher_deal_details_menu": lambda: PublisherDealDetailsMenu(audio, state),
        "merch_menu": lambda: MerchMenu(audio, state),
        "merch_amount_menu": lambda: MerchAmountMenu(audio, state),
        "esports_menu": lambda: ESportsMenu(audio, state),
        "acquisition_menu": lambda: AcquisitionMenu(audio, state),
        "stock_rival_detail": lambda: StockRivalDetailMenu(audio, state),
        "addon_name_input": lambda: AddonNameMenu(audio, state),
        "bundle_name_input": lambda: BundleNameMenu(audio, state),
        "settings_menu_ingame": lambda: SettingsMenu(audio, state, lambda: "game_menu"),
        "save_menu": lambda: SaveMenu(audio, state),
        "load_menu": lambda: LoadMenu(audio, state),
        "help_menu": lambda: HelpMenu(audio, state),
        "goty_menu": lambda: GOTYMenu(audio, state),
        "aaa_dev_event_menu": lambda: AAADevEventMenu(audio, state),
        "credits_menu": lambda: CreditsMenu(audio, state),
        "build_menu": lambda: BuildMenu(audio, state),
        "teambuilding_menu": lambda: TeambuildingMenu(audio, state),
        "mod_portal": lambda: ModPortalMenu(audio, state),
        "mod_browser_list": lambda: ModBrowserListMenu(audio, state),
    }

def main():
    """Hauptspielschleife."""
    os.environ['SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS'] = '0'
    pygame.init()
    pygame.key.set_repeat(300, 50)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Audio Studio Tycoon - v3.0.0 Visionary")

    audio = AudioManager()
    state = GameState()
    state.audio = audio
    state.load_global_settings()
    set_language(state.settings.get('language', 'de'))
    audio.apply_volumes(state.settings)

    current_key = "main_menu"

    # AUTO-UPDATE BEIM START (nur Stable-Kanal, sofern nicht explizit Beta gewählt)
    if state.settings.get('auto_update', True):
        try:
            from updater import check_for_updates
            import json
            curr_v_path = "version.json"
            current_v = "1.0.0"
            if os.path.exists(curr_v_path):
                with open(curr_v_path, "r", encoding="utf-8") as f_v:
                    current_v = json.load(f_v).get("version", "1.0.0")
            # Auto-Update lädt IMMER nur Stable – Beta muss manuell aktiviert werden
            channel = state.settings.get('update_channel', 'stable')
            result = check_for_updates(current_v, channel=channel)
            if result and result.get("update_available"):
                state.pending_update = result
                current_key = "update_confirm_menu"
        except Exception: # pylint: disable=broad-exception-caught
            pass


    menu_factories = get_menu_factories(audio, state)
    current_menu = menu_factories[current_key]()

    audio.speak(get_text("main_welcome"))
    audio.play_music("music_back")
    current_menu.announce_entry()

    running = True
    clock = pygame.time.Clock()
    last_tick_time = pygame.time.get_ticks()

    while running:
        dt = pygame.time.get_ticks() - last_tick_time
        last_tick_time = pygame.time.get_ticks()
        state.update_tick(dt)

        if hasattr(current_menu, 'update'):
            current_menu.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Globale Geschwindigkeitssteuerung
                if event.key == pygame.K_1:
                    state.time_speed = 1.0
                    audio.speak(get_text("speed_normal"))
                elif event.key == pygame.K_2:
                    state.time_speed = 2.0
                    audio.speak(get_text("speed_fast"))
                elif event.key == pygame.K_3:
                    state.time_speed = 4.0
                    audio.speak(get_text("speed_ultra"))
                elif event.key == pygame.K_SPACE or event.key == pygame.K_0:
                    if state.time_speed > 0:
                        state.last_speed = state.time_speed
                        state.time_speed = 0
                        audio.speak(get_text("paused"))
                    else:
                        state.time_speed = getattr(state, "last_speed", 1.0)
                        audio.speak(state.get_speed_text())
                
                result = current_menu.handle_input(event)
                if result == "quit":
                    running = False
                elif result and result in menu_factories:
                    current_key = result
                    current_menu = menu_factories[current_key]()
                    current_menu.announce_entry()

                # Automatischer Wechsel zum Ergebnis wenn Entwicklung im Hintergrund fertig ist
                if state.is_developing and getattr(state, "dev_ready_to_finish", False) and current_key != "dev_progress_menu":
                    if not state.pause_for_menu:
                        current_key = "dev_progress_menu"
                        current_menu = menu_factories[current_key]()
                        current_menu.announce_entry()

        # --- VISUAL RENDERING (WOW-FAKTOR) ---
        screen.fill((15, 23, 42)) # Slate 900
        
        # Hintergrund-Gradient Simulation
        for i in range(600):
            color = (15 + i//40, 23 + i//50, 42 + i//30)
            pygame.draw.line(screen, color, (0, i), (800, i))

        # Menü-Box (Glassmorphism)
        menu_rect = pygame.Rect(100, 100, 600, 400)
        pygame.draw.rect(screen, (30, 41, 59, 180), menu_rect, border_radius=20) # Slate 800
        pygame.draw.rect(screen, (51, 65, 85), menu_rect, 2, border_radius=20) # Border

        # Title
        font = pygame.font.SysFont("Arial", 32, bold=True)
        title_surf = font.render(current_menu.title, True, (0, 242, 254))
        screen.blit(title_surf, (150, 130))

        # Options
        font_opt = pygame.font.SysFont("Arial", 24)
        if hasattr(current_menu, 'options'):
            for i, opt in enumerate(current_menu.options):
                color = (255, 255, 255) if i == current_menu.current_index else (148, 163, 184)
                if i == current_menu.current_index:
                    # Cursor Highlight
                    pygame.draw.rect(screen, (0, 242, 254, 50), (140, 180 + i*40, 520, 35), border_radius=5)
                
                opt_surf = font_opt.render(opt['text'], True, color)
                screen.blit(opt_surf, (150, 185 + i*40))

        # Multi-Tasking Ticker (oben rechts)
        if state.is_developing:
            prog = int((state.dev_progress / max(1, state.dev_total_weeks)) * 100)
            prog = min(100, prog)
            ticker_font = pygame.font.SysFont("Arial", 18, bold=True)
            ticker_text = f"DEV: {state.current_draft.get('name', '???')} - {prog}%"
            # Pulsierender Effekt
            alpha = int(155 + 100 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            pygame.draw.rect(screen, (0, 242, 254, alpha // 4), (550, 20, 230, 40), border_radius=10)
            t_surf = ticker_font.render(ticker_text, True, (0, 242, 254))
            screen.blit(t_surf, (570, 30))

        # Footer Info
        footer_font = pygame.font.SysFont("Arial", 16)
        money_txt = f"{get_text('money_label')}: {state.money:,} EUR | KW {state.week}"
        f_surf = footer_font.render(money_txt, True, (255, 255, 255))
        screen.blit(f_surf, (110, 510))

        pygame.display.flip()
        clock.tick(30)

    audio.cleanup()
    pygame.quit()

if __name__ == "__main__":
    main()
