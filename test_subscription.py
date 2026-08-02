import unittest
from logic import GameState
from models import GameProject, RivalGame

class TestSubscriptionManager(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 10000000 # 10 Mio
        self.state.fans = 1000000
        self.sm = self.state.subscription_manager
        
    def test_launch_service(self):
        self.assertFalse(self.sm.is_active)
        success, msg = self.sm.launch_service(self.state)
        self.assertTrue(success)
        self.assertTrue(self.sm.is_active)
        self.assertEqual(self.state.money, 5000000)
        self.assertEqual(self.sm.subscribers, 50000) # 5% of 1M
        
    def test_launch_service_no_money(self):
        self.state.money = 1000
        success, msg = self.sm.launch_service(self.state)
        self.assertFalse(success)
        self.assertFalse(self.sm.is_active)
        
    def test_add_own_game(self):
        self.sm.launch_service(self.state)
        initial_subs = self.sm.subscribers
        
        game = GameProject("Test Game", "RPG", "Fantasy", "PC")
        game.review = type('obj', (object,), {'average': 80})()
        
        success, msg = self.sm.add_own_game(self.state, game)
        self.assertTrue(success)
        self.assertIn("Test Game", self.sm.catalog)
        self.assertTrue(self.sm.subscribers > initial_subs)
        self.assertEqual(self.sm.weeks_since_last_release, 0)
        
    def test_buy_third_party_game(self):
        self.sm.launch_service(self.state)
        initial_subs = self.sm.subscribers
        
        rival_game = RivalGame("Rival RPG", "RPG", 80, 50000)
        rival_game.total_sales = 500000
        
        success, msg = self.sm.buy_third_party_game(self.state, rival_game)
        self.assertTrue(success)
        self.assertIn("Rival RPG", self.sm.catalog)
        self.assertEqual(self.sm.weeks_since_last_release, 0)
        
        # 500,000 sales -> cost is 5,000,000
        self.assertEqual(self.state.money, 0)
        self.assertEqual(self.sm.subscribers, initial_subs + int(500000 * 0.2))

    def test_tick_churn_and_income(self):
        self.sm.launch_service(self.state)
        initial_money = self.state.money
        initial_subs = self.sm.subscribers
        
        self.sm.tick(self.state)
        
        # Base churn is 0.5% per week -> 50,000 * 0.005 = 250 churn
        self.assertEqual(self.sm.subscribers, initial_subs - 250)
        
        # Income = 49,750 * 9.99 / 4 = 124,250
        # Server cost = 49,750 * 0.5 / 4 = 6,218
        # Net = 118,032
        self.assertTrue(self.state.money > initial_money)

if __name__ == '__main__':
    unittest.main()
