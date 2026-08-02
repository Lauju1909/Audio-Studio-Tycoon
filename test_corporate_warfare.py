import pytest
from logic import GameState
from models import RivalStudio
from managers.corporate_warfare import EspionageMission, SabotageMission, execute_hostile_takeover

# Mocking audio module to prevent pygame issues during testing
class MockAudio:
    def play_sound(self, sound): pass
    def play_music(self, music): pass
    def speak(self, text, interrupt=True): pass
    def update(self): pass
    def add_to_queue(self, text): pass
    def pause(self): pass
    def resume(self): pass
    def get_setting(self, key): return 100

@pytest.fixture
def game_state():
    gs = GameState()
    gs.audio = MockAudio()
    # Setup some base variables
    gs.money = 1000000
    gs.fans = 10000
    gs.week = 1
    
    # Add a rival
    rival = RivalStudio("Test Rival")
    rival.planned_project = {"topic": "Sci-Fi", "genre": "RPG"}
    rival.next_release_week = 50
    
    # Add fake games to rival to give them value
    from models import RivalGame
    rival.games.append(RivalGame("Test Game 1", "Fantasy", "Action", 7.0, 10))
    gs.rivals = [rival]
    
    return gs

def test_espionage_mission(game_state):
    initial_money = game_state.money
    mission = EspionageMission("Test Rival")
    
    # Force risk_level to 0.0 to guarantee success, or patch random
    mission.risk_level = 0.0 
    
    success = game_state.corporate_warfare.start_mission(mission, game_state)
    assert success == True
    assert game_state.money == initial_money - 50000
    assert len(game_state.corporate_warfare.active_missions) == 1
    
    # Tick forward until finished
    for _ in range(mission.duration_weeks):
        game_state.corporate_warfare.tick(game_state)
        
    assert len(game_state.corporate_warfare.active_missions) == 0
    assert len(game_state.emails) == 1
    body = game_state.emails[0].body
    assert "Sci-Fi" in body or "warfare_espionage_success" in body

def test_sabotage_mission(game_state):
    initial_money = game_state.money
    mission = SabotageMission("Test Rival")
    mission.risk_level = 0.0
    
    initial_release_week = game_state.rivals[0].next_release_week
    
    success = game_state.corporate_warfare.start_mission(mission, game_state)
    assert success == True
    assert game_state.money == initial_money - 150000
    
    for _ in range(mission.duration_weeks):
        game_state.corporate_warfare.tick(game_state)
        
    assert len(game_state.emails) == 1
    body = game_state.emails[0].body
    assert "verzögert" in body or "delayed" in body or "warfare_sabotage_success" in body
    assert game_state.rivals[0].next_release_week > initial_release_week

def test_espionage_failure(game_state):
    initial_fans = game_state.fans
    mission = EspionageMission("Test Rival")
    mission.risk_level = 1.0 # Guarantee failure (random.random() > 1.0 is False)
    
    game_state.corporate_warfare.start_mission(mission, game_state)
    for _ in range(mission.duration_weeks):
        game_state.corporate_warfare.tick(game_state)
        
    assert game_state.fans == initial_fans - 5000
    body = game_state.emails[0].body
    assert "PR-Desaster" in body or "PR disaster" in body or "warfare_espionage_fail" in body

def test_hostile_takeover_success(game_state):
    target = game_state.rivals[0]
    initial_money = game_state.money
    
    # Value is 500k + (1 game * 100k) = 600k. Since avg is 7.0, base_value = 600k.
    success, msg = execute_hostile_takeover(target, 700000, game_state)
    
    assert success == True
    assert target not in game_state.rivals
    assert target in getattr(game_state, "subsidiaries", [])
    assert game_state.money == initial_money - 700000

def test_hostile_takeover_fail(game_state):
    target = game_state.rivals[0]
    initial_money = game_state.money
    
    # Bid too low
    success, msg = execute_hostile_takeover(target, 10000, game_state)
    
    assert success == False
    assert target in game_state.rivals
    assert game_state.money == initial_money
