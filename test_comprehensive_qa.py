import pytest
from logic import GameState
from models import GameProject

def test_100_weeks_stability():
    logic = GameState()
    logic.money = 10000000
    
    # Run 100 weeks
    for _ in range(100):
        logic.update_tick(15000) # One week in ms
        
    assert logic.week >= 100
    
    logic.current_draft = {
        "name": "Test Game",
        "topic": "Fantasy",
        "genre": "RPG",
        "platform": {"name": "PC"},
        "audience": "Jeder",
        "engine": None,
        "size": "Mittel",
        "marketing": "Kein Marketing",
        "sliders": {}
    }
    logic.start_development()
    
    # Run another 20 weeks to finish project
    for _ in range(20):
        logic.update_tick(15000)
