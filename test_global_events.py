import unittest
from logic import GameState

class TestGlobalEvents(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 10000000
        self.gem = self.state.global_event_manager
        
    def test_trigger_crisis(self):
        self.gem.trigger_chip_crisis(self.state)
        self.assertTrue(self.gem.current_event is not None)
        self.assertEqual(self.gem.current_event.effect_type, "chip_crisis")
        
        # Test modifiers
        self.assertEqual(self.gem.get_development_speed_modifier(), 0.8)
        self.assertEqual(self.gem.get_server_cost_modifier(), 1.5)
        self.assertEqual(self.gem.get_hardware_cost_modifier(), 2.0)
        
    def test_black_market(self):
        self.gem.trigger_chip_crisis(self.state)
        initial_money = self.state.money
        
        success, _ = self.gem.buy_black_market_chips(self.state)
        self.assertTrue(success)
        self.assertTrue(self.gem.black_market_deal_active)
        self.assertTrue(self.state.money < initial_money)
        
        # Dev speed back to normal
        self.assertEqual(self.gem.get_development_speed_modifier(), 1.0)
        # Server/Hardware still expensive
        self.assertEqual(self.gem.get_server_cost_modifier(), 1.5)
        
if __name__ == '__main__':
    unittest.main()
