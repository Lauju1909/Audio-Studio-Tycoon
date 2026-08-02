from logic import GameState
from models import GameProject

class DummyAudio:
    def speak(self, text, interrupt=False):
        pass
    def play_sound(self, name):
        pass

def test_it_security_ddos_prevents_digital_sales():
    gs = GameState()
    gs.audio = DummyAudio()
    gs.week = 52 * 10 + 1 # Year 2000+
    gs.money = 1000000000
    
    # Give a released game
    g = GameProject("HackThis", "Hacking", "Sim", "PC", "B")
    g.is_released = True
    g.is_active = True
    g.weeks_on_market = 1
    g.sales = 0
    g.quality = 8.0
    gs.game_history.append(g)
    
    # First, test without DDoS
    gs.calculate_sales = lambda x: 50000
    gs._on_new_week()
    assert g.sales > 0, "Game should have digital sales"
    
    # Now simulate DDoS
    initial_sales = g.sales
    if not hasattr(gs, 'active_cyber_effects'):
        gs.active_cyber_effects = []
    gs.active_cyber_effects.append({"type": "ddos", "weeks_left": 2})
    
    gs._on_new_week()
    assert g.sales == initial_sales, "Digital sales should be 0 during DDoS"

def test_it_security_ransomware():
    gs = GameState()
    gs.audio = DummyAudio()
    gs.week = 52 * 10 + 1
    gs.money = 1000000000
    
    # Start a project
    g = GameProject("SecretProject", "Hacking", "Sim", "PC", "AAA")
    g.is_released = False
    g.progress = 50.0
    gs.current_project = g
    
    from managers.it_security import ITSecurityManager
    
    # manually reset
    g.progress = 50.0
    
    mgr = ITSecurityManager()
    
    # Ransomware attack
    import random
    orig_choice = random.choice
    random.choice = lambda x: "ransomware"
    
    if not hasattr(gs, 'it_upgrades'):
        gs.it_upgrades = []
    if not hasattr(gs, 'active_cyber_effects'):
        gs.active_cyber_effects = []
        
    mgr._trigger_random_attack(gs)
    random.choice = orig_choice
    
    assert g.progress == 37.5, f"Progress should be 25% less (50 -> 37.5), got {g.progress}"
    
    # With backup upgrade
    gs.it_upgrades.append("encrypted_backups")
    g.progress = 50.0
    random.choice = lambda x: "ransomware"
    mgr._trigger_random_attack(gs)
    random.choice = orig_choice
    
    assert g.progress == 50.0, "Progress should not drop if encrypted_backups is unlocked"
