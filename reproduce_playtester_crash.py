
import sys
import os
import json

# Add current dir to path
sys.path.append(os.getcwd())

try:
    from logic import GameState
    import translations
    # Mock translations
    translations.TRANSLATIONS = {'de': {}, 'en': {}}
    
    state = GameState()
    path = 'save_slot_test_save_playtester.json.json'
    print(f"Loading {path}...")
    
    # Manually load the file since load_game is slot-based
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # We can't easily call load_game with a path if it's hardcoded to save_slot_{slot}.json
    # So we'll temporarily rename the file or mock the method
    import shutil
    shutil.copy(path, "save_slot_999.json")
    
    if state.load_game(slot=999):
        print("Load successful. Calling _on_new_week...")
        state._on_new_week()
        print("Success! No crash.")
    else:
        print("Failed to load.")
    
    if os.path.exists("save_slot_999.json"):
        os.remove("save_slot_999.json")

except Exception as e:
    print(f"CRASH DETECTED: {e}")
    import traceback
    traceback.print_exc()
    if os.path.exists("save_slot_999.json"):
        os.remove("save_slot_999.json")
