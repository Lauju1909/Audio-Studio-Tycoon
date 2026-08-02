import unittest
from logic import GameState
from managers.monetization_manager import MonetizationManager

class TestCryptoManager(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 20000000
        self.state.fans = 1000000
        self.state.monetization_manager = MonetizationManager()
        self.cm = self.state.crypto_manager
        
    def test_launch_ico(self):
        initial_money = self.state.money
        success, _ = self.cm.launch_ico(self.state)
        
        self.assertTrue(success)
        self.assertTrue(self.cm.ico_launched)
        self.assertTrue(self.state.money > initial_money) # Earned from ICO
        
    def test_pump_coin(self):
        self.cm.launch_ico(self.state)
        initial_money = self.state.money
        initial_hype = self.cm.hype_level
        initial_price = self.cm.coin_price
        
        success, _ = self.cm.pump_coin(self.state)
        self.assertTrue(success)
        self.assertEqual(self.cm.hype_level, min(100.0, initial_hype + 30.0))
        self.assertTrue(self.cm.coin_price > initial_price)
        self.assertEqual(self.state.money, initial_money - 1000000)
        
    def test_trigger_crash(self):
        self.cm.launch_ico(self.state)
        initial_fans = self.state.fans
        initial_money = self.state.money
        
        self.cm.trigger_crash(self.state)
        
        self.assertTrue(self.cm.crashed)
        self.assertEqual(self.state.monetization_manager.fan_trust, 0.0)
        self.assertEqual(self.state.monetization_manager.government_heat, 100.0)
        self.assertTrue(self.state.fans < initial_fans)
        self.assertTrue(self.state.money < initial_money) # Lawsuit
        
if __name__ == '__main__':
    unittest.main()
