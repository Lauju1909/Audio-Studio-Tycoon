from logic import GameState
from models import GameProject

class DummyAudio:
    def speak(self, text, interrupt=False): pass
    def play_sound(self, name): pass

def test_convention_manager():
    gs = GameState()
    gs.audio = DummyAudio()
    gs.money = 1500000
    gs.is_feature_unlocked = lambda f: True
    gs.week = 20 # 4 weeks before convention week (24)
    
    # Tick should trigger announcement
    gs._on_new_week()
    assert len(gs.emails) > 0
    assert any("Global Audio Expo" in e.subject or "Global Audio Expo" in e.body for e in gs.emails)
    
    # Book a mega booth
    g = GameProject("Test Game", "RPG", "Fantasy", "PC", "AAA")
    g.progress = 80.0
    g.hype = 10
    
    assert gs.convention_manager.book_booth(gs, "mega", g)
    assert gs.money == 1500000 - 1000000
    assert gs.current_convention_booking["tier"] == "mega"
    
    # Fast forward to convention week
    gs.week = 24
    gs._on_new_week() # Week 24 now
    
    # Check if convention ran
    assert gs.current_convention_booking is None # Resets after running
    assert g.hype > 10 # Hype should have increased significantly
    
    # Check emails for report
    assert any("Global Audio Expo" in e.subject for e in gs.emails)
