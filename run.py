import logic
state = logic.GameState()
state.time_speed = 1
from models import GameProject, Employee
game = GameProject('Test Game', 'Action', 'RPG', {}, 'PC', 'Jeder', None, 'Mittel', 'Kein Marketing')
game.sales = 100000
state.game_history.append(game)
role_data = {'role': 'Programmierer', 'primary': 'Programmierung', 'secondary': 'Design'}
for _ in range(5): state.employees.append(Employee('Test', role_data, 5, None))
state.money = 1000000
state.start_update_project('Test Game', 'DLC', 'My DLC')
for _ in range(50):
 for e in state.employees:
  e.fatigue = 0
  e.morale = 100
 state.update_tick(15000)
 if len(state.active_projects) == 0: break
print('dlc_count:', game.dlc_count, 'updates:', len(game.updates))

