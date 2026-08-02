import logic
import models

gs = logic.GameState()
gs.money = 1000000000
gs.fans = 10000
gs.company_name = "TestCorp"
cc = models.CustomConsoleProject(name="MyPlayConsole", tech_level=50, dev_cost=50000000, price=499)
gs.active_custom_console = cc
cc.is_released = True
cc.progress = 1.0
gs.save_game(99)

gs2 = logic.GameState()
gs2.load_game(99)
print("Loaded cc:", gs2.active_custom_console)
