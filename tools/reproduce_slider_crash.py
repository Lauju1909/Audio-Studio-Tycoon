import pygame
pygame.init()
pygame.display.set_mode((100,100))

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import GameState
from audio import AudioManager
import translations
from menus import DevelopmentSliderMenu, DevProgressMenu

class DummyAudio(AudioManager):
    def __init__(self):
        super().__init__()
        self.spoken = []
    def speak(self, text, interrupt=True):
        self.spoken.append(text)
    def play_sound(self, name): pass
    def play_music(self, name): pass

def test_repro():
    print("Starting reproduction test...")
    audio = DummyAudio()
    state = GameState()
    state.audio = audio
    
    # Setup draft
    state.current_draft = {
        "name": "Test Game",
        "topic": "Vampire",
        "genre": "RPG",
        "platform": "PC",
        "audience": "Jeder",
        "size": "Mittel",
        "marketing": "Kein Marketing",
        "engine": None
    }
    
    translations.set_language("de")
    
    print("Testing DevelopmentSliderMenu confirm...")
    slider_menu = DevelopmentSliderMenu(audio, state)
    slider_menu.announce_entry()
    
    # Simulate distributing points (budget is 30)
    for name in slider_menu.slider_names:
        slider_menu.values[name] = 5 # 6 * 5 = 30
    
    try:
        result = slider_menu._confirm(slider_menu.values)
        print(f"Slider confirm result: {result}")
        
        if result == "dev_progress_menu":
            print("Creating DevProgressMenu...")
            progress_menu = DevProgressMenu(audio, state)
            print("Calling announce_entry...")
            progress_menu.announce_entry()
            print("Calling update...")
            progress_menu.update()
            
    except Exception as e:
        print(f"\nCRASH DETECTED: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\nReproduction test finished without crash in DE.")
    
    translations.set_language("en")
    print("\nTesting in EN...")
    try:
        progress_menu = DevProgressMenu(audio, state)
        progress_menu.announce_entry()
        progress_menu.update()
    except Exception as e:
        print(f"\nCRASH DETECTED IN EN: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    print("Reproduction test finished without crash in EN.")
    return True

if __name__ == "__main__":
    test_repro()
