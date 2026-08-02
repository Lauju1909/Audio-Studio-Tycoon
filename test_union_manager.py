import pytest
from logic import GameState
from models import Employee

# Mocking audio module to prevent pygame issues during testing
class MockAudio:
    def play_sound(self, sound_name):
        pass
    def speak(self, text, interrupt=True):
        pass

@pytest.fixture
def game_state():
    gs = GameState()
    gs.audio = MockAudio()
    gs.money = 1000000
    gs.fans = 10000
    gs.week = 1
    
    # Add some employees
    e1 = Employee("Alice", {"role": "Programmer", "primary": "Code", "secondary": "Design"})
    e1.salary = 2000
    e1.morale = 100
    e2 = Employee("Bob", {"role": "Artist", "primary": "Grafik", "secondary": "Design"})
    e2.salary = 2000
    e2.morale = 100
    gs.employees = [e1, e2]
    return gs

def test_ai_tools_increase_anger_and_decrease_morale(game_state):
    mgr = game_state.union_manager
    mgr.ai_tools_active = True
    
    initial_morale = game_state.employees[0].morale
    mgr.tick(game_state)
    
    assert mgr.union_anger == 2.0
    assert game_state.employees[0].morale < initial_morale

def test_strike_trigger(game_state):
    mgr = game_state.union_manager
    mgr.union_anger = 99.0
    mgr.ai_tools_active = True
    
    mgr.tick(game_state)
    
    assert mgr.is_striking == True
    assert mgr.strike_weeks_left >= 3
    assert len(game_state.emails) == 1
    assert "strike" in game_state.emails[0].subject.lower() or "streik" in game_state.emails[0].subject.lower() or "schlagen" in game_state.emails[0].subject.lower()

def test_negotiation_accept_demands(game_state):
    mgr = game_state.union_manager
    mgr.is_striking = True
    mgr.strike_weeks_left = 5
    mgr.ai_tools_active = True
    
    initial_salary = game_state.employees[0].salary
    success, msg = mgr.negotiate("accept_demands", game_state)
    
    assert success == True
    assert mgr.is_striking == False
    assert mgr.ai_tools_active == False
    assert mgr.union_anger == 0.0
    assert game_state.employees[0].salary == int(initial_salary * 1.2)

def test_negotiation_compromise(game_state):
    mgr = game_state.union_manager
    mgr.is_striking = True
    mgr.union_anger = 100.0
    
    initial_money = game_state.money
    success, msg = mgr.negotiate("compromise", game_state)
    
    assert success == True
    assert mgr.is_striking == False
    assert mgr.union_anger == 70.0
    assert game_state.money == initial_money - (len(game_state.employees) * 15000)

def test_negotiation_union_busting_fail(game_state, monkeypatch):
    mgr = game_state.union_manager
    mgr.is_striking = True
    
    import random
    monkeypatch.setattr(random, "random", lambda: 0.9) # Force fail (> 0.4)
    
    initial_money = game_state.money
    initial_fans = game_state.fans
    success, msg = mgr.negotiate("union_busting", game_state)
    
    assert success == False
    assert game_state.money == initial_money - 500000 - 1000000
    assert game_state.fans == int(initial_fans * 0.8)

def test_negotiation_union_busting_success(game_state, monkeypatch):
    mgr = game_state.union_manager
    mgr.is_striking = True
    
    import random
    monkeypatch.setattr(random, "random", lambda: 0.1) # Force success (< 0.4)
    
    success, msg = mgr.negotiate("union_busting", game_state)
    
    assert success == True
    assert mgr.union_busted == True
    assert mgr.is_striking == False
