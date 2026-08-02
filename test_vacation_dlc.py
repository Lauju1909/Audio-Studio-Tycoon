from logic import GameState
from models import Employee, GameProject

def test_employee_vacation_and_burnout():
    state = GameState()
    state.time_speed = 1
    role_data = {"role": "Programmierer", "primary": "Programmierung", "secondary": "Design"}
    emp = Employee("Test", role_data, 1, None)
    state.employees.append(emp)
    
    state.active_projects.append({"project": GameProject("Mock", "Action", "RPG", {}, "PC", "Jeder", None, "Mittel", "Kein Marketing"), "progress": 0, "total_weeks": 100, "bugs": 0})
    
    emp.fatigue = 50
    emp.vacation_weeks_left = 4
    
    for _ in range(5):
        state.update_tick(15000)
        
    assert emp.vacation_weeks_left <= 0
    assert emp.fatigue < 50
    
def test_game_dlc():
    state = GameState()
    state.time_speed = 1
    # Mock game
    game = GameProject("Test Game", "Action", "RPG", {}, "PC", "Jeder", None, "Mittel", "Kein Marketing")
    game.sales = 100000
    game.weeks_on_market = 5
    game.is_active = False
    state.game_history.append(game)
    
    # 5 employees so they work fast
    role_data = {"role": "Programmierer", "primary": "Programmierung", "secondary": "Design"}
    for _ in range(5):
        state.employees.append(Employee("Test", role_data, 5, None))
        
    state.money = 1000000
    # Start DLC
    assert state.start_update_project("Test Game", "DLC", "My DLC")
    
    for _ in range(50):
        for e in state.employees:
            e.fatigue = 0
            e.morale = 100
        state.update_tick(15000)
        if state.time_speed == 0:
            state.time_speed = 1
            if getattr(state, 'pending_dev_event', None):
                state.pending_dev_event = None
        if len(state.active_projects) == 0:
            break
            
    # DLC should be applied
    print("ACTIVE PROJECTS:", state.active_projects)
    print("DLC COUNT:", game.dlc_count)
    print("UPDATES:", game.updates)
    print("GAME IN HISTORY:", state.game_history[0].name)
    assert game.dlc_count == 1
    assert len(state.active_projects) == 0
