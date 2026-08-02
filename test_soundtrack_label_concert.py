from logic import GameState
from models import SoundtrackLabel

def test_concert_success():
    state = GameState()
    state.money = 200000
    state.soundtrack_label = SoundtrackLabel("Epic Music")
    
    # Add 5 games
    for i in range(5):
        state.soundtrack_label.catalogued_games.append(f"Game {i}")
        
    initial_money = state.money
    initial_prestige = state.soundtrack_label.prestige_bonus
    
    # Emulate concert action
    from menus.events import SoundtrackLabelMenu
    
    class DummyAudio:
        def speak(self, text): pass
        def play_sound(self, sfx): pass
        def say(self, t): pass
        def say_interrupt(self, t): pass

    class DummyEvent:
        def __init__(self, key):
            self.key = key

    menu = SoundtrackLabelMenu(DummyAudio(), state)
    
    # Force action execution
    # Wait, SoundtrackLabelMenu is built with options. Let's find the index for 'label_concert'
    concert_index = -1
    for i, opt in enumerate(menu.options):
        if opt.get('action') == 'label_concert':
            concert_index = i
            break
            
    assert concert_index != -1, "Concert option not found in menu"
    
    menu.current_index = concert_index
    menu.handle_input(DummyEvent(state.key_confirm))
    
    assert state.money > (initial_money - 100000), "Should have earned money from concert"
    assert state.soundtrack_label.prestige_bonus == initial_prestige + 5, "Prestige should increase by 5"

