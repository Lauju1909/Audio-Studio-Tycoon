import unittest
from logic import GameState
from models import GameProject

class TestMTXFeature(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.fans = 100000

    def test_add_mtx(self):
        project = GameProject(
            name="Test Game",
            topic="Fantasy",
            genre="RPG",
            platform="PC",
            audience="Jeder",
            size="Klein",
            marketing="Kein Marketing"
        )
        project.sales = 100000
        project.revenue = 5000000
        project.review = type('Mock', (), {'average': 8.0, 'scores': [8,8,8,8]})()
        self.state.game_history.append(project)

        # Initial hat das Spiel keine MTX
        self.assertFalse(getattr(project, 'has_mtx', False))
        
        # Fuge MTX hinzu
        success = self.state.add_mtx_to_game("Test Game")
        self.assertTrue(success)
        self.assertTrue(project.has_mtx)
        
        # Fans sollten droppen
        self.assertLess(self.state.fans, 100000)
        
        # In der naechsten Woche sollte es Extra Revenue generieren
        initial_money = self.state.money
        self.state._on_new_week()
        
        self.assertGreater(self.state.money, initial_money)

if __name__ == '__main__':
    unittest.main()
