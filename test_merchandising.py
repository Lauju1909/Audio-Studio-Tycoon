from logic import GameState
from models import GameProject

def test_merchandising_campaign():
    state = GameState()
    state.time_speed = 1
    state.money = 200000
    
    # Mock Game
    game = GameProject("Test Game", "Action", "RPG", {}, "PC", "Jeder", None, "Mittel", "Kein Marketing")
    game.sales = 100000
    game.ip_rating = 80
    state.game_history.append(game)
    
    # Start T-Shirt Campaign
    assert state.start_merch_campaign("Test Game", "T-Shirts", 12, 10000)
    assert len(state.active_merch_campaigns) == 1
    assert state.active_merch_campaigns[0].game_name == "Test Game"
    
    initial_money = state.money
    # Advance one week
    state.update_tick(15000)
    
    # Should generate income
    assert state.money > initial_money
    assert state.active_merch_campaigns[0].weeks_active == 1
    
    # Advance until completion
    for _ in range(12):
        state.update_tick(15000)
        
    assert len(state.active_merch_campaigns) == 0
