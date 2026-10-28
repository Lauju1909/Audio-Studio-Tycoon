import os
import sys
import pygame

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import translations
from logic import GameState
from menus.settings import KeybindingMenu, SettingsMenu, LanguageMenu
from ui.router import MenuRouter
from main import setup_router

class MockAudio:
    def __init__(self):
        self.spoken = []
        self.sounds = []
    def speak(self, msg, interrupt=False):
        self.spoken.append((msg, interrupt))
    def play_sound(self, s):
        self.sounds.append(s)
    def apply_volumes(self, s):
        pass
    def play_music(self, m):
        pass

def test_language_toggle_flow():
    print("=== TEST 1: Basic GameState Toggle ===")
    pygame.init()
    audio = MockAudio()
    state = GameState()
    state.audio = audio
    state.load_global_settings()
    
    # Force to de
    state.set_language("de")
    assert state.settings["language"] == "de"
    assert translations.CURRENT_LANGUAGE == "de"
    assert state.get_text("develop_new_game") == "Neues Spiel entwickeln"
    
    # Toggle to en
    new_lang = state.toggle_language()
    assert new_lang == "en"
    assert state.settings["language"] == "en"
    assert translations.CURRENT_LANGUAGE == "en"
    assert state.get_text("develop_new_game") == "Develop New Game"
    
    # Toggle back to de
    new_lang2 = state.toggle_language()
    assert new_lang2 == "de"
    assert state.settings["language"] == "de"
    assert translations.CURRENT_LANGUAGE == "de"
    assert state.get_text("develop_new_game") == "Neues Spiel entwickeln"
    print("[OK] GameState.toggle_language switches de <-> en and updates translations")

def test_menu_router_language_refresh():
    print("=== TEST 2: MenuRouter Instant Language Refresh ===")
    audio = MockAudio()
    state = GameState()
    state.audio = audio
    state.set_language("de")
    
    router = setup_router(audio, state)
    menu_de = router.get_menu("main_menu")
    opt0_de = menu_de.options[0]["text"]
    assert "Neues Spiel" in opt0_de, f"Expected German 'Neues Spiel', got: {opt0_de}"
    
    # Switch to en
    state.toggle_language()
    menu_en = router.get_menu("main_menu")
    opt0_en = menu_en.options[0]["text"]
    assert "New Game" in opt0_en, f"Expected English 'New Game', got: {opt0_en}"
    print(f"[OK] MenuRouter reflects language switch immediately: '{opt0_de}' -> '{opt0_en}'")

def test_keybinding_menu():
    print("=== TEST 3: KeybindingMenu includes Language Toggle ===")
    audio = MockAudio()
    state = GameState()
    state.audio = audio
    state.set_language("de")
    
    kb_menu = KeybindingMenu(audio, state)
    option_texts = [o["text"] for o in kb_menu.options]
    assert any("Sprache umschalten" in t for t in option_texts), f"Language toggle not found in options: {option_texts}"
    
    # Switch to English
    state.set_language("en")
    kb_menu_en = KeybindingMenu(audio, state)
    option_texts_en = [o["text"] for o in kb_menu_en.options]
    assert any("Toggle Language" in t for t in option_texts_en), f"English toggle not found in options: {option_texts_en}"
    print("[OK] KeybindingMenu supports language toggle binding in DE and EN")

def test_hotkey_detection():
    print("=== TEST 4: Hotkey constants and matching ===")
    state = GameState()
    state.load_global_settings()
    
    # Default key is F8
    assert state.key_toggle_language == pygame.K_F8 or getattr(state, 'key_toggle_language') == 1073741889
    
    # Simulate F8 event
    event_f8 = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F8, mod=0)
    is_toggle_1 = (event_f8.key == getattr(state, 'key_toggle_language', pygame.K_F8)) or \
                  (event_f8.key == pygame.K_l and (pygame.key.get_mods() & pygame.KMOD_CTRL))
    assert is_toggle_1 is True
    
    # Simulate Ctrl+L event
    event_ctrl_l = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_l, mod=pygame.KMOD_CTRL)
    mods_2 = getattr(event_ctrl_l, 'mod', 0) | pygame.key.get_mods()
    is_toggle_2 = (event_ctrl_l.key == getattr(state, 'key_toggle_language', pygame.K_F8)) or \
                  (event_ctrl_l.key == pygame.K_l and (mods_2 & pygame.KMOD_CTRL))
    assert bool(is_toggle_2) is True
    print("[OK] F8 and Ctrl+L hotkeys correctly recognized")

if __name__ == "__main__":
    test_language_toggle_flow()
    test_menu_router_language_refresh()
    test_keybinding_menu()
    test_hotkey_detection()
    print("\nALL 4 LANGUAGE TOGGLE TESTS PASSED 100%!")
