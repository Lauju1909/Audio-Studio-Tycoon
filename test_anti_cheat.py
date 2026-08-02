import unittest
from logic import GameState
from models import GameProject

class TestAntiCheatFeature(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.fans = 100000
        self.state.money = 200000

    def test_buy_anti_cheat_f2p(self):
        project = GameProject(
            name="FreeGame",
            topic="Sci-Fi",
            genre="Action",
            platform="PC",
            audience="Jeder",
            size="AAA",
            marketing="Groß"
        )
        project.is_f2p = True
        project.active_players = 50000
        project.is_active = True
        self.state.game_history.append(project)

        # Initial has no anti-cheat
        self.assertFalse(getattr(project, 'has_anti_cheat', False))
        
        # Buy Anti-Cheat
        success = self.state.buy_anti_cheat("FreeGame")
        
        self.assertTrue(success)
        self.assertTrue(project.has_anti_cheat)
        self.assertEqual(self.state.money, 100000) # Costs 100k

        # Try buying again
        success2 = self.state.buy_anti_cheat("FreeGame")
        self.assertFalse(success2)

    def test_buy_anti_cheat_no_money(self):
        self.state.money = 50000
        project = GameProject(
            name="PoorGame",
            topic="Sci-Fi",
            genre="Action",
            platform="PC",
            audience="Jeder",
            size="AAA",
            marketing="Groß"
        )
        project.is_f2p = True
        project.active_players = 50000
        project.is_active = True
        self.state.game_history.append(project)

        success = self.state.buy_anti_cheat("PoorGame")
        self.assertFalse(success)
        self.assertFalse(getattr(project, 'has_anti_cheat', False))

if __name__ == '__main__':
    unittest.main()
