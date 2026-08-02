import os
from logic import GameState
from models import CustomConsoleProject

class DummyAudio:
    def speak(self, text, interrupt=False):
        pass
    def play_sound(self, name):
        pass

def test_custom_console_development():
    gs = GameState()
    gs.audio = DummyAudio()
    gs.money = 1000000000
    gs.fans = 10000
    gs.company_name = "TestCorp"
    
    # Hire some employees to program
    from models import Employee
    emp1 = Employee("Alice", {"role": "Programmierer", "primary": "Programmierung", "secondary": "Grafik"}, skill_level=5)
    emp1.skills["Programmierung"] = 100
    gs.employees.append(emp1)
    
    cc = CustomConsoleProject(name="MyPlayConsole", tech_level=50, dev_cost=50000000, price=499)
    cc.total_weeks = 5
    gs.active_custom_console = cc
    
    assert cc.progress == 0.0
    
    # advance week to develop
    for i in range(15):
        gs._on_new_week()
        
    assert getattr(cc, "is_released", False) == True
    assert cc.progress >= 1.0
    
    # Check if added to PLATFORMS
    from game_data import PLATFORMS
    found = any(p["name"] == "MyPlayConsole" for p in PLATFORMS)
    assert found == True
    
    # Check if it sells
    assert cc.units_sold > 0
    assert cc.active_users > 0
    assert cc.revenue > 0
    
    # Test save/load
    gs.save_game(99)
    gs2 = GameState()
    gs2.audio = DummyAudio()
    assert gs2.load_game(99) == True
    
    assert gs2.active_custom_console is not None
    assert gs2.active_custom_console.name == "MyPlayConsole"
    assert gs2.active_custom_console.is_released == True
    assert gs2.active_custom_console.units_sold == cc.units_sold
    
    if os.path.exists("save_slot_99.json"):
        os.remove("save_slot_99.json")
