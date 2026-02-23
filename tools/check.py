import pygame
pygame.init()
pygame.display.set_mode((100,100))
from logic import GameState
from audio import AudioManager
from menus import *
import translations

state = GameState()
audio = AudioManager()

def get_menu_factories():
    return {
        "main_menu": lambda: MainMenu(audio, state),
        "hr_menu": lambda: HRMenu(audio, state),
        "research_menu": lambda: ResearchMenu(audio, state),
        "console_specs_menu": lambda: ConsoleSpecsMenu(audio, state),
    }

for lang in ["de", "en"]:
    state.settings['language'] = lang
    translations.set_language(lang)
    print(f"--- TESTING LANGUAGE: {lang} ---")
    factories = get_menu_factories()
    for name, factory in factories.items():
        menu = factory()
        try:
            menu.announce_entry()
        except Exception as e:
            print(f"ERROR IN {name}: {e}")

print("DONE")
