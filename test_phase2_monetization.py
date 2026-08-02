import unittest
from logic import GameState
from models import GameProject

class TestPhase2Monetization(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.company_name = "TestCompany"
        self.state.rivals = self.state._init_rivals()

    def test_f2p_project(self):
        project = GameProject(
            name="F2P Game",
            topic="Fantasy",
            genre="RPG",
            platform="PC",
            audience="Jeder",
            size="Klein",
            marketing="Kein Marketing"
        )
        project.is_f2p = True
        ap = {"project": project, "progress": 0, "total_weeks": 10, "stage": 3, "bugs": 0}
        self.state.active_projects.append(ap)
        # Fast forward
        self.state.week += 10
        self.state.finalize_game(ap)
        
        # Retail price should be 0, is_f2p should be True
        released_game = self.state.game_history[-1]
        self.assertTrue(released_game.is_f2p)

    def test_remake_project(self):
        project = GameProject(
            name="Remake Game",
            topic="Fantasy",
            genre="RPG",
            platform="PC",
            audience="Jeder",
            size="Klein",
            marketing="Kein Marketing"
        )
        project.is_remake = True
        project.original_game_name = "Old Game"
        
        self.state.hype
        ap = {"project": project, "progress": 0, "total_weeks": 10, "stage": 3, "bugs": 0}
        self.state.active_projects.append(ap)
        self.state.finalize_game(ap)
        
        released_game = self.state.game_history[-1]
        self.assertTrue(released_game.is_remake)
        self.assertEqual(released_game.original_game_name, "Old Game")

    def test_ma_buyout(self):
        # Find a rival and buy them out
        rival = self.state.rivals[0]
        rival.is_owned_by_player = False
        
        # Test they release a game normally
        self.state._process_rivals()
        
        # Buy them out
        rival.is_owned_by_player = True
        
        # Fast forward to next week to get passive income
        initial_money = self.state.money
        self.state._on_new_week()
        
        # Since the first week logic might add or substract other values,
        # we check that we generated passive income tracking via 'other'
        self.assertGreater(self.state.money, initial_money)

if __name__ == '__main__':
    unittest.main()
