"""
Audio Studio Tycoon - Audio Edition
Hauptprogramm & Spielschleife

100% Screenreader-optimiert (NVDA).
Steuerung: Pfeiltasten + Enter + Buchstaben für Texteingabe.
"""

import pygame
import time
import os
import sys
import io
import json
import ctypes

# Fix for Windows console encoding issues
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

from audio import AudioManager
from logic import GameState
from tutorial import TutorialManager
from translations import get_text, set_language
from menus import (
    OfficePerksMenu, HeadhuntingEventMenu,
    MainMenu, UpdateConfirmMenu, UpdateProgressMenu, CompanyNameMenu, GameMenu, TopicMenu,
    GenreMenu, PlatformMenu, AudienceMenu, GameSizeMenu, MarketingMenu,
    EngineSelectMenu, RemasterSelectMenu, PublisherMenu, SettingsMenu,
    VolumeSettingsMenu, KeybindingMenu, LanguageMenu, ExpoMenu, GameNameMenu,
    DevelopmentSliderMenu, DevProgressMenu, ReviewResultMenu,
    HRMenu, HireMenu, EmployeeOverviewMenu, FireMenu, TrainingEmployeeSelectMenu,
    TrainingOptionMenu, ResearchMenu, FeatureResearchMenu,
    GenreResearchMenu, TopicResearchMenu, AudienceResearchMenu,
    TechnologyResearchMenu, EngineCreateNameMenu, EngineFeatureSelectMenu,
    HardwareDevMenu, ConsoleNameInput, ConsoleSpecsMenu, OfficeMenu,
    BankruptcyMenu, EmailInboxMenu, EmailDetailMenu, ServiceMenu,
    GameServiceOptionsMenu, AddMtxMenu, MovieDealMenu, AntiCheatMenu, BankMenu, LoanMenu, StockMarketMenu,
    DonationMenu, MonetizationMenu,
    DifficultyMenu, SubGenreMenu, SequelMenu, ProjectTypeMenu, RemakeSelectMenu, ChartMenu,
    LicenseShopMenu, LicenseSelectMenu, AddonMenu, AddonNameMenu,
    BundleMenu, BundleNameMenu, ProductionMenu, ProductionAmountMenu,
    ActiveGamesMenu, GameDetailsMenu,
    MMOPaymentMenu, MMOManagementMenu, MMOOptionsMenu,
    PublisherDealsMenu, PublisherDealDetailsMenu, MerchMenu, MerchAmountMenu, SubscriptionVaultMenu, CreatorSponsorshipMenu,
    ESportsMenu, AcquisitionMenu, StockRivalDetailMenu,
    SaveMenu, LoadMenu, HelpMenu, GOTYMenu, ShareholderMenu, AAADevEventMenu, InfluencerEventMenu, UnionEventMenu, CreditsMenu,
    BuildMenu, TeambuildingMenu, ModPortalMenu, ModBrowserListMenu,
    ProjectTeamSelectMenu, DeveloperMenu,
    SoundConMenu, SoundConFinishMenu, SoundConResultMenu, SoundConHistoryMenu,
    SoundtrackLabelMenu, LabelNameInputMenu, LabelStatusMenu,
    LabelRadioMenu, LabelAddGameMenu,
    MultiplayerMainMenu, MultiplayerRoomIdInput, MultiplayerLobbyMenu,
    CommunityMenu, AccessibilityLabMenu, FanMailInboxMenu, FanMailDetailMenu, OfficeEventMenu,
    HardwareLabMenu, HardwareLicensingMenu, SoundCardCreateMenu, SoundCardFeaturesMenu, SoundCardOverviewMenu,
    JingleNameInputMenu, JingleGeneratorMenu, JingleMusicMenu, JingleVoiceMenu, JingleSFXMenu
)

def get_menu_factories(audio, state):
    """Gibt Factory-Funktionen für alle Menüs zurück."""
    return {
        "main_menu": lambda: MainMenu(audio, state),
        "update_confirm_menu": lambda: UpdateConfirmMenu(audio, state),
        "update_progress_menu": lambda: UpdateProgressMenu(audio, state),
        "company_name_input": lambda: CompanyNameMenu(audio, state),
        "game_menu": lambda: GameMenu(audio, state),
        "topic_menu": lambda: TopicMenu(audio, state),
        "genre_menu": lambda: GenreMenu(audio, state),
        "platform_menu": lambda: PlatformMenu(audio, state),
        "audience_menu": lambda: AudienceMenu(audio, state),
        "game_size_menu": lambda: GameSizeMenu(audio, state),
        "marketing_menu": lambda: MarketingMenu(audio, state),
        "team_select_menu": lambda: ProjectTeamSelectMenu(audio, state),
        "engine_select_menu": lambda: EngineSelectMenu(audio, state),
        "remaster_select": lambda: RemasterSelectMenu(audio, state),
        "publisher_menu": lambda: PublisherMenu(audio, state),
        "settings_menu": lambda: SettingsMenu(audio, state, lambda: "main_menu"),
        "language_menu": lambda: LanguageMenu(audio, state),
        "volume_settings_menu": lambda: VolumeSettingsMenu(audio, state),
        "keybinding_menu": lambda: KeybindingMenu(audio, state),
        "expo_menu": lambda: ExpoMenu(audio, state),
        "game_name_input": lambda: GameNameMenu(audio, state),
        "slider_menu": lambda: DevelopmentSliderMenu(audio, state),
        "dev_progress_menu": lambda: DevProgressMenu(audio, state),
        "review_result": lambda: ReviewResultMenu(audio, state),
        "hr_menu": lambda: HRMenu(audio, state),
        "office_perks_menu": lambda: OfficePerksMenu(audio, state),
        "headhunting_event_menu": lambda: HeadhuntingEventMenu(audio, state),
        "hire_menu": lambda: HireMenu(audio, state),
        "employee_overview_menu": lambda: EmployeeOverviewMenu(audio, state),
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
        "contract_work_menu": lambda: ContractWorkMenu(audio, state),
        "game_service_options": lambda: GameServiceOptionsMenu(audio, state),
        "add_mtx_menu": lambda: AddMtxMenu(audio, state),
        "movie_deal_menu": lambda: MovieDealMenu(audio, state),
        "anti_cheat_menu": lambda: AntiCheatMenu(audio, state),
        "bank_menu": lambda: BankMenu(audio, state),
        "loan_menu": lambda: LoanMenu(audio, state),
        "donation_menu": lambda: DonationMenu(audio, state),
        "monetization_menu": lambda: MonetizationMenu(audio, state),
        "monetization_menu_main": lambda: MonetizationMenu(audio, state, back_target="main_menu", show_ads=False),
        "stock_market_menu": lambda: StockMarketMenu(audio, state),
        "difficulty_menu": lambda: DifficultyMenu(audio, state),
        "sub_genre_menu": lambda: SubGenreMenu(audio, state),
        "sequel_menu": lambda: SequelMenu(audio, state),
        "project_type_menu": lambda: ProjectTypeMenu(audio, state),
        "remake_select_menu": lambda: RemakeSelectMenu(audio, state),
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
        "subscription_add_game_menu": lambda: SubscriptionVaultMenu(audio, state),
        "creator_menu": lambda: CreatorSponsorshipMenu(audio, state),
        "merch_amount_menu": lambda: MerchAmountMenu(audio, state),
        "esports_menu": lambda: ESportsMenu(audio, state),
        "acquisition_menu": lambda: AcquisitionMenu(audio, state),
        "engine_licensing_menu": lambda: __import__('menus', fromlist=['']).EngineLicensingMenu(audio, state),
        "engine_license_fee_menu": lambda: __import__('menus', fromlist=['']).EngineLicenseFeeMenu(audio, state),
        "game_porting_menu": lambda: __import__('menus', fromlist=['']).GamePortingMenu(audio, state),
        "port_platform_menu": lambda: __import__('menus', fromlist=['']).PortPlatformMenu(audio, state),
        "stock_rival_detail": lambda: StockRivalDetailMenu(audio, state),
        "addon_name_input": lambda: AddonNameMenu(audio, state),
        "bundle_name_input": lambda: BundleNameMenu(audio, state),
        "co_dev_partner_menu": lambda: __import__('menus.gameplay', fromlist=['']).CoDevPartnerMenu(audio, state),
        "subscription_service_menu": lambda: __import__('menus.business', fromlist=['']).SubscriptionServiceMenu(audio, state),
        "support_gift_card_type_menu": lambda: __import__('menus.business', fromlist=['']).SupportGiftCardTypeMenu(audio, state),
        "espionage_menu": lambda: __import__('menus.business', fromlist=['']).EspionageMenu(audio, state),
        "office_upgrades_menu": lambda: __import__('menus.office', fromlist=['']).OfficeUpgradeMenu(audio, state),
        "settings_menu_ingame": lambda: SettingsMenu(audio, state, lambda: "game_menu"),
        "save_menu": lambda: SaveMenu(audio, state),
        "load_menu": lambda: LoadMenu(audio, state),
        "help_menu": lambda: HelpMenu(audio, state),
        "goty_menu": lambda: GOTYMenu(audio, state),
        "shareholder_meeting": lambda: ShareholderMenu(audio, state),
        "aaa_dev_event_menu": lambda: AAADevEventMenu(audio, state),
        "influencer_event_menu": lambda: InfluencerEventMenu(audio, state),
        "union_event_menu": lambda: UnionEventMenu(audio, state),
        "credits_menu": lambda: CreditsMenu(audio, state),
        "build_menu": lambda: BuildMenu(audio, state),
        "teambuilding_menu": lambda: TeambuildingMenu(audio, state),
        "mod_portal": lambda: ModPortalMenu(audio, state),
        "mod_browser_list": lambda: ModBrowserListMenu(audio, state),
        "multiplayer_main": lambda: MultiplayerMainMenu(audio, state),
        "multiplayer_room_id_input": lambda: MultiplayerRoomIdInput(audio, state),
        "multiplayer_create_id_input": lambda: MultiplayerRoomIdInput(audio, state), # Reuse for now
        "multiplayer_lobby": lambda: MultiplayerLobbyMenu(audio, state),
        "active_games_menu": lambda: ActiveGamesMenu(audio, state),
        "game_details_menu": lambda: GameDetailsMenu(audio, state),
        "current_monetization_menu": lambda: MonetizationMenu(audio, state, show_ads=state.monetization_back_target != "main_menu"),
        "developer_menu": lambda: DeveloperMenu(audio, state),
        # NEU: SoundCon & Soundtrack-Label
        "soundcon_menu": lambda: SoundConMenu(audio, state),
        "soundcon_finish_confirm": lambda: SoundConFinishMenu(audio, state),
        "soundcon_result_menu": lambda: SoundConResultMenu(audio, state),
        "soundcon_history_menu": lambda: SoundConHistoryMenu(audio, state),
        "label_menu": lambda: SoundtrackLabelMenu(audio, state),
        "label_name_input": lambda: LabelNameInputMenu(audio, state),
        "label_status_menu": lambda: LabelStatusMenu(audio, state),
        "soundcon_radio_menu": lambda: LabelRadioMenu(audio, state), # alias if needed
        "label_radio_menu": lambda: LabelRadioMenu(audio, state),
        "label_add_game_menu": lambda: LabelAddGameMenu(audio, state),
        # NEU: Expansion v3.11.0 Menüs
        "community_menu": lambda: CommunityMenu(audio, state),
        "accessibility_lab": lambda: AccessibilityLabMenu(audio, state),
        "fan_mail_inbox": lambda: FanMailInboxMenu(audio, state),
        "fan_mail_detail": lambda: FanMailDetailMenu(audio, state),
        "office_event_menu": lambda: OfficeEventMenu(audio, state),
        "hardware_menu": lambda: HardwareLabMenu(audio, state),
        "hardware_licensing": lambda: HardwareLicensingMenu(audio, state),
        "hardware_create_name": lambda: SoundCardCreateMenu(audio, state),
        "hardware_project_features": lambda: SoundCardFeaturesMenu(audio, state),
        "hardware_overview": lambda: SoundCardOverviewMenu(audio, state),
        "jingle_name_input": lambda: JingleNameInputMenu(audio, state),
        "jingle_generator": lambda: JingleGeneratorMenu(audio, state),
        "jingle_select_music": lambda: JingleMusicMenu(audio, state),
        "jingle_select_voice": lambda: JingleVoiceMenu(audio, state),
        "jingle_select_sfx": lambda: JingleSFXMenu(audio, state),
    }

def main():
    """Hauptspielschleife."""
    os.environ['SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS'] = '0'
    
    # --- AUDIO PRE-INIT (WICHTIG VOR PYGAME.INIT) ---
    try:
        pygame.mixer.pre_init(44100, -16, 2, 512)
    except Exception:
        pass

    pygame.init()
    pygame.key.set_repeat(300, 50)
    # Nutze HWSURFACE, DOUBLEBUF und SCALED für maximale GPU-Beschleunigung und CPU-Effizienz
    screen = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED | pygame.RESIZABLE)
    
    # Fenster in den Vordergrund bringen (wichtig für Fokus bei automatischem Update-Neustart)
    if sys.platform == 'win32':
        try:
            hwnd = pygame.display.get_wm_info().get('window')
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                ctypes.windll.user32.SetActiveWindow(hwnd)
        except Exception:
            pass

    # --- VERSION LADEN ---
    curr_v_path = "version.json"
    current_v = "3.8.1"
    if os.path.exists(curr_v_path):
        try:
            with open(curr_v_path, "r", encoding="utf-8") as f_v:
                current_v = json.load(f_v).get("version", "3.8.1")
        except:
            pass

    pygame.display.set_caption(f"Audio Studio Tycoon v{current_v} - Stable")

    # --- PERFORMANCE & WOW CACHE ---
    # Fonts einmalig laden (Extrem CPU-schonend)
    fonts = {
        'title': pygame.font.SysFont("Arial", 32, bold=True),
        'opt': pygame.font.SysFont("Arial", 24),
        'ticker': pygame.font.SysFont("Arial", 18, bold=True),
        'footer': pygame.font.SysFont("Arial", 16)
    }

    # Hintergrund-Gradient vorrendern (Spart 600 Draw-Calls pro Frame!)
    bg_surface = pygame.Surface((800, 600))
    for i in range(600):
        color = (15 + i//40, 23 + i//50, 42 + i//30)
        pygame.draw.line(bg_surface, color, (0, i), (800, i))
    
    # Glassmorphism Box vorrendern (GPU-friendly)
    menu_box = pygame.Surface((600, 400), pygame.SRCALPHA)
    pygame.draw.rect(menu_box, (30, 41, 59, 180), (0, 0, 600, 400), border_radius=20)
    pygame.draw.rect(menu_box, (51, 65, 85), (0, 0, 600, 400), 2, border_radius=20)

    audio = AudioManager()
    state = GameState()
    state.audio = audio
    state.load_global_settings()
    tutorial_manager = TutorialManager(audio, state)
    set_language(state.settings.get('language', 'de'))
    state.add_welcome_emails()
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
    
    # Trigger Welcome Tutorial if needed
    tutorial_manager.start_tutorial("welcome")

    running = True
    clock = pygame.time.Clock()
    last_tick_time = pygame.time.get_ticks()

    while running:
        dt = pygame.time.get_ticks() - last_tick_time
        last_tick_time = pygame.time.get_ticks()
        state.update_tick(dt)

        if hasattr(current_menu, 'update'):
            result = current_menu.update()
            if result:
                if result in menu_factories:
                    current_key = result
                    current_menu = menu_factories[current_key]()
                    current_menu.announce_entry()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- TUTORIAL INPUT HANDLING ---
            if tutorial_manager.handle_input(event):
                continue

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
                
                # --- NEUE GLOBALE HOTKEYS ---
                elif event.key == pygame.K_f:
                    # Finanzen abfragen
                    audio.speak(state.get_financial_summary())
                elif event.key == pygame.K_s:
                    # Status abfragen (RP, Mitarbeiter, Fans)
                    audio.speak(state.get_status_summary())
                elif event.key == pygame.K_d and (pygame.key.get_mods() & pygame.KMOD_CTRL) and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                    # Entwickler-Modus aktivieren/deaktivieren
                    state.developer_mode = not state.developer_mode
                    if state.developer_mode:
                        audio.speak("Entwickler-Modus aktiviert. Drücke D im Hauptmenü oder Ingame-Menü für Optionen.")
                    else:
                        audio.speak("Entwickler-Modus deaktiviert.")
                elif event.key == pygame.K_d and state.developer_mode:
                    # Direkter Sprung ins Dev-Menü
                    result = "developer_menu"
                    current_key = result
                    current_menu = menu_factories[current_key]()
                    current_menu.announce_entry()
                    continue
                
                try:
                    result = current_menu.handle_input(event)
                    if result:
                        if result in menu_factories:
                            current_key = result
                            current_menu = menu_factories[current_key]()
                            current_menu.announce_entry()
                            
                            # Trigger Contextual Tutorials
                            if result == "game_menu":
                                tutorial_manager.start_tutorial("office")
                            elif result == "topic_menu":
                                tutorial_manager.start_tutorial("game_dev")
                            elif result == "research_menu":
                                tutorial_manager.start_tutorial("research")
                            elif result == "hr_menu":
                                tutorial_manager.start_tutorial("hr")
                            elif result == "marketing_menu":
                                tutorial_manager.start_tutorial("marketing")
                            elif result == "bank_menu":
                                tutorial_manager.start_tutorial("finance")
                            elif result == "multiplayer_main":
                                tutorial_manager.start_tutorial("multiplayer")
                        elif result == "quit":
                            running = False
                except Exception as e:
                    import traceback
                    err_msg = traceback.format_exc()
                    with open("crash_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"\n--- CRASH AT {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                        f.write(f"Menu: {current_key}\n")
                        f.write(err_msg)
                        f.write("-" * 40 + "\n")
                    
                    # Visuelle Fehlermeldung für den User
                    ctypes.windll.user32.MessageBoxW(0, f"Ein Fehler ist aufgetreten:\n\n{str(e)}\n\nDetails wurden in crash_log.txt gespeichert.", "Audio Studio Tycoon - Fehler", 0x10)
                    
                    # Versuche zurück zum Hauptmenü zu gehen statt abzustürzen
                    current_key = "main_menu"
                    current_menu = menu_factories[current_key]()
                    current_menu.announce_entry()
                    audio.speak("Ein interner Fehler ist aufgetreten. Rückkehr zum Hauptmenü.")

                # Automatischer Wechsel zum Ergebnis wenn Entwicklung im Hintergrund fertig ist
                any_ready = any(ap.get("ready_to_finish") for ap in state.active_projects)
                if state.is_developing and any_ready and current_key != "dev_progress_menu":
                    if not state.pause_for_menu:
                        current_key = "dev_progress_menu"
                        current_menu = menu_factories[current_key]()
                        current_menu.announce_entry()

                # --- EVENT QUEUEING ---
                # Verhindert UI Flip-Flop, wenn mehrere Events im selben Tick triggern
                active_event_menus = (
                    "aaa_dev_event_menu", 
                    "influencer_event_menu", 
                    "union_event_menu", 
                    "headhunting_event_menu", 
                    "goty_menu"
                )
                
                if current_key not in active_event_menus:
                    if getattr(state, "pending_dev_event", None):
                        current_key = "aaa_dev_event_menu"
                        current_menu = menu_factories[current_key]()
                        current_menu.announce_entry()
                    elif getattr(state, "pending_influencer_event", None):
                        current_key = "influencer_event_menu"
                        current_menu = menu_factories[current_key]()
                        current_menu.announce_entry()
                    elif getattr(state, "pending_union_event", None):
                        current_key = "union_event_menu"
                        current_menu = menu_factories[current_key]()
                        current_menu.announce_entry()
                    elif getattr(state, "pending_headhunt_event", None):
                        current_key = "headhunting_event_menu"
                        current_menu = menu_factories[current_key]()
                        current_menu.announce_entry()
                    elif getattr(state, "pending_goty_results", None) and current_key != "dev_progress_menu":
                        current_key = "goty_menu"
                        current_menu = menu_factories[current_key]()
                        current_menu.announce_entry()

        # --- VISUAL RENDERING (OPTIMIERT) ---
        screen.blit(bg_surface, (0, 0))
        
        # Menü-Box (Blitten statt Zeichnen)
        screen.blit(menu_box, (100, 100))

        # Title
        title_surf = fonts['title'].render(current_menu.title, True, (0, 242, 254))
        screen.blit(title_surf, (150, 130))

        # Options
        if hasattr(current_menu, 'options'):
            for i, opt in enumerate(current_menu.options):
                color = (255, 255, 255) if i == current_menu.current_index else (148, 163, 184)
                if i == current_menu.current_index:
                    # Cursor Highlight (pulsierend für WOW-Effekt)
                    p_alpha = int(40 + 20 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
                    h_rect = pygame.Surface((520, 35), pygame.SRCALPHA)
                    pygame.draw.rect(h_rect, (0, 242, 254, p_alpha), (0, 0, 520, 35), border_radius=5)
                    screen.blit(h_rect, (140, 180 + i*40))
                
                opt_surf = fonts['opt'].render(opt['text'], True, color)
                screen.blit(opt_surf, (150, 185 + i*40))

        # Multi-Tasking Ticker (oben rechts)
        if state.is_developing:
            # BUG-FIX v3.3.9: Nutze active_projects statt der veralteten Legacy-Attribute dev_progress / dev_total_weeks
            first_ap = state.active_projects[0]
            prog = int((first_ap["progress"] / max(1, first_ap["total_weeks"])) * 100)
            prog = min(100, prog)
            proj_name = first_ap["project"].name if hasattr(first_ap["project"], 'name') else '???'
            count_suffix = f" (+{len(state.active_projects)-1})" if len(state.active_projects) > 1 else ""
            ticker_text = f"DEV: {proj_name}{count_suffix} - {prog}%"
            # Pulsierender Effekt
            alpha = int(155 + 100 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            t_box = pygame.Surface((230, 40), pygame.SRCALPHA)
            pygame.draw.rect(t_box, (0, 242, 254, alpha // 4), (0, 0, 230, 40), border_radius=10)
            screen.blit(t_box, (550, 20))
            t_surf = fonts['ticker'].render(ticker_text, True, (0, 242, 254))
            screen.blit(t_surf, (570, 30))

        # Footer Info - jetzt mit Monat und Jahr
        cal_text = state.get_calendar_text() if state.company_name else ""
        money_txt = f"{get_text('money_label')}: {state.money:,} EUR"
        if cal_text:
            money_txt += f" | {cal_text}"
        f_surf = fonts['footer'].render(money_txt, True, (255, 255, 255))
        screen.blit(f_surf, (110, 510))

        pygame.display.flip()
        clock.tick(60)

    audio.cleanup()
    pygame.quit()

if __name__ == "__main__":
    main()
