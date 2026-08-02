import unittest
from logic import GameState
from models import GameProject

class TestMonetizationManager(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 20000000
        self.state.fans = 1000000
        self.state.week = 2000
        self.mm = self.state.monetization_manager
        
    def test_hire_managers(self):
        self.assertEqual(self.mm.pr_managers, 0)
        self.assertEqual(self.mm.ethics_managers, 0)
        
        success, _ = self.mm.hire_pr_manager(self.state)
        self.assertTrue(success)
        self.assertEqual(self.mm.pr_managers, 1)
        
        success, _ = self.mm.hire_ethics_manager(self.state)
        self.assertTrue(success)
        self.assertEqual(self.mm.ethics_managers, 1)
        
    def test_lootbox_income_and_heat(self):
        game = GameProject("Lootbox Simulator", "RPG", "Fantasy", "PC")
        game.sales = 1000000
        game.release_week = 1990
        self.state.game_history.append(game)
        
        self.mm.toggle_lootboxes()
        self.assertTrue(self.mm.lootboxes_active)
        
        initial_money = self.state.money
        initial_trust = self.mm.fan_trust
        initial_heat = self.mm.government_heat
        
        self.mm.tick(self.state)
        
        self.assertTrue(self.state.money > initial_money) # Made money
        self.assertTrue(self.mm.fan_trust < initial_trust) # Lost trust
        self.assertTrue(self.mm.government_heat > initial_heat) # Gained heat

    def test_government_fine(self):
        self.mm.government_heat = 100.0
        initial_money = self.state.money
        
        self.mm.tick(self.state)
        
        self.assertEqual(self.mm.government_heat, 0.0)
        self.assertEqual(self.state.money, initial_money // 2)
        
if __name__ == '__main__':
    unittest.main()
