
import sys
import os

# Add current dir to path
sys.path.append(os.getcwd())

try:
    from logic import GameState
    import translations
    # Mock translations to avoid missing keys
    translations.TRANSLATIONS = {'de': {}, 'en': {}}
    
    for slot in range(1, 6):
        state = GameState()
        print(f"--- Testing Slot {slot} ---")
        if state.load_game(slot=slot):
            print(f"Load successful for slot {slot}. Calling _on_new_week...")
            try:
                state._on_new_week()
                print(f"Success for slot {slot}! No crash.")
            except Exception as e:
                print(f"CRASH DETECTED in slot {slot}: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"Failed to load slot {slot} or slot empty.")
except Exception as e:
    print(f"FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
