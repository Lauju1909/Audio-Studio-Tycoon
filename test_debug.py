from logic import GameState
from models import Employee, GameProject

def test_vacation_debug():
    state = GameState()
    state.time_speed = 1
    role_data = {"role": "Programmierer", "primary": "Programmierung", "secondary": "Design"}
    emp = Employee("Test", role_data, 1, None)
    state.employees.append(emp)
    
    state.active_projects.append({"project": GameProject("Mock", "Action", "RPG", {}, "PC", "Jeder", None, "Mittel", "Kein Marketing"), "progress": 0, "total_weeks": 100, "bugs": 0})
    
    # 35 weeks crunch
    emp.is_crunching = True
    for _ in range(35):
        state.update_tick(15000)
        
    print(f"After crunch: fatigue={emp.fatigue}, morale={emp.morale}, in_list={emp in state.employees}")
    emp.vacation_weeks_left = 4
    for _ in range(4):
        state.update_tick(15000)
        
    print(f"After vacation: vacation={emp.vacation_weeks_left}, fatigue={emp.fatigue}, morale={emp.morale}, in_list={emp in state.employees}")

if __name__ == '__main__':
    test_vacation_debug()
