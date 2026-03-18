# ruff: noqa: F405, F403
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic import GameState
from audio import AudioManager
import translations

class ConsoleAudio(AudioManager):
    def __init__(self):
        super().__init__()
    def speak(self, text, interrupt=True):
        print(f"\n[AUDIO] {text}")
    def play_sound(self, name):
        print(f"*[SOUND: {name}]*")
    def play_music(self, name):
        pass

audio = ConsoleAudio()
state = GameState()
state.audio = audio
state.settings['language'] = 'de'
translations.set_language('de')

from menus import *

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
    "topic_research_menu": lambda: TopicResearchMenu(audio, state),
    "genre_research_menu": lambda: GenreResearchMenu(audio, state),
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
    "settings_menu": lambda: SettingsMenu(audio, state, lambda: "main_menu"),
    "save_menu": lambda: SaveMenu(audio, state),
    "load_menu": lambda: LoadMenu(audio, state),
    "help_menu": lambda: HelpMenu(audio, state),
    "aaa_dev_event_menu": lambda: AAADevEventMenu(audio, state),
}

current_key = "main_menu"
current_menu = menu_factories[current_key]()
current_menu.announce_entry()

class MockEvent:
    def __init__(self, key, unicode=""):
        self.type = pygame.KEYDOWN
        self.key = key
        self.unicode = unicode

print("\n--- CONSOLE MODE: 'w'=UP, 's'=DOWN, 'a'=LEFT, 'd'=RIGHT, 'enter'=SELECT, 'q'=QUIT ---")

while True:
    cmd = input("\n> ").strip().lower()
    
    if cmd == 'q':
        break
        
    event = None
    if cmd == 'w':
        event = MockEvent(pygame.K_UP)
    elif cmd == 's':
        event = MockEvent(pygame.K_DOWN)
    elif cmd == 'a':
        event = MockEvent(pygame.K_LEFT)
    elif cmd == 'd':
        event = MockEvent(pygame.K_RIGHT)
    elif cmd == 'enter' or cmd == '':
        event = MockEvent(pygame.K_RETURN)
    else:
        # Check text input
        if hasattr(current_menu, 'is_text_input') and current_menu.is_text_input:
            if cmd == 'backspace' or cmd == '-':
                event = MockEvent(pygame.K_BACKSPACE)
            else:
                for char in cmd:
                    evt = MockEvent(pygame.K_a, unicode=char)
                    res = current_menu.handle_input(evt)
                event = None # handled
        else:
            print("Unknown command. Use: w/s/a/d/enter/q/backspace")
            continue
            
    if event:
        res = current_menu.handle_input(event)
        if res == "quit":
            break
        elif res:
            current_key = res
            current_menu = menu_factories[current_key]()
            current_menu.announce_entry()
