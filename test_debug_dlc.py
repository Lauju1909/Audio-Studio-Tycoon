from logic import GameState
from models import Employee, GameProject

def test_game_dlc():
    state = GameState()
    state.time_speed = 1
    # Mock game
    game = GameProject("Test Game", "Action", "RPG", {}, "PC", "Jeder", None, "Mittel", "Kein Marketing")
    game.sales = 100000
    game.weeks_on_market = 20
    game.is_active = False
    state.game_history.append(game)
    
    # 5 employees so they work fast
    role_data = {"role": "Programmierer", "primary": "Programmierung", "secondary": "Design"}
    for _ in range(5):
        state.employees.append(Employee("Test", role_data, 5, None))
        
    state.money = 1000000
    # Start DLC
    assert state.start_update_project("Test Game", "DLC", "My DLC")
    
    # Assign employees to the update project
    update_proj = state.active_projects[0]["project"]
    for e in state.employees:
        e.assigned_project = update_proj
    
    for _ in range(50):
        for e in state.employees:
            e.fatigue = 0
            e.morale = 100
        
        # If there's a blocking event, clear it
        if getattr(state, "active_events", None) or state.time_speed == 0:
            state.time_speed = 1
            if hasattr(state, "pending_dev_event"):
                state.pending_dev_event = None
                
        state.update_tick(15000)
        if len(state.active_projects) == 0:
            print(f"Finished at iteration {_}")
            break
            
    if state.active_projects:
        print("Active projects after 50 iterations:", state.active_projects)
        print("Progress:", state.active_projects[0]["progress"])
    
    print("Updates:", game.updates)
    print("dlc_count:", game.dlc_count)
    # DLC should be applied
    assert game.dlc_count == 1

if __name__ == '__main__':
    test_game_dlc()
