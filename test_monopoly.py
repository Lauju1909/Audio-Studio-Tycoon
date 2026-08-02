import unittest
from logic import GameState
from models import RivalStudio
from managers.monopoly_manager import MonopolyManager

class TestMonopolyManager(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 50000000
        self.mm = MonopolyManager()
        
        # Add some dummy rivals
        for i in range(5):
            rival = RivalStudio(f"Rival {i}", 50)
            self.state.rivals.append(rival)
            
    def test_market_share(self):
        # 0 subsidiaries -> 5%
        self.assertEqual(self.mm.get_market_share(self.state), 5.0)
        
        # Own 2 rivals -> 5% + 16% = 21%
        self.state.rivals[0].is_owned_by_player = True
        self.state.rivals[1].is_owned_by_player = True
        
        self.assertEqual(self.mm.get_market_share(self.state), 21.0)
        
    def test_anti_trust_fines(self):
        # Own 5 rivals -> 5% + 40% = 45% (triggers fine)
        for r in self.state.rivals:
            r.is_owned_by_player = True
            
        self.state.money
        self.mm.tick(self.state)
        
        # Fine should be max(2000000, 5% of money). 5% of 50M = 2.5M
        # But wait, subsidiaries also give passive income. 
        # So we check if anti_trust_fines_paid increases.
        self.assertTrue(self.mm.anti_trust_fines_paid > 0)
        
    def test_bribe_politicians(self):
        success, _ = self.mm.bribe_politicians(self.state)
        self.assertTrue(success)
        self.assertEqual(self.mm.lobbying_weeks_left, 26)
        
        # Test immunity
        for r in self.state.rivals:
            r.is_owned_by_player = True
            
        self.mm.anti_trust_fines_paid = 0
        self.mm.tick(self.state)
        
        # No fines because lobbying_weeks_left > 0
        self.assertEqual(self.mm.anti_trust_fines_paid, 0)
        self.assertEqual(self.mm.lobbying_weeks_left, 25)
        
    def test_sell_subsidiary(self):
        self.state.rivals[0].is_owned_by_player = True
        initial_money = self.state.money
        
        success, _ = self.mm.sell_subsidiary(self.state, 0)
        self.assertTrue(success)
        self.assertFalse(self.state.rivals[0].is_owned_by_player)
        self.assertEqual(self.state.rivals[0].owned_shares, 0)
        self.assertTrue(self.state.money > initial_money) # Sold it
        
if __name__ == '__main__':
    unittest.main()
