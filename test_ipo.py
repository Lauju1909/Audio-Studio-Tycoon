import unittest
from logic import GameState

class TestIPOSystem(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 20000000
        self.state.fans = 2000000
        
    def test_go_public(self):
        sm = self.state.stock_manager
        self.assertFalse(sm.is_public)
        
        # Payout calculation
        payout = int((self.state.fans * 10 + self.state.money) * 0.3)
        expected_money = self.state.money + payout
        
        # Simuliere IPO (wie im Menue)
        sm.go_public(self.state, payout)
        
        self.assertEqual(self.state.money, expected_money)
        self.assertTrue(sm.is_public)
        self.assertEqual(sm.shareholder_trust, 100)
        self.assertEqual(sm.owned_shares_percent, 51.0)
        
    def test_earnings_call_triggers(self):
        sm = self.state.stock_manager
        sm.go_public(self.state, 10000000)
        
        # Simuliere 12 Wochen (Earnings Call)
        initial_trust = sm.shareholder_trust
        
        # We don't make any money, so we miss target
        for _ in range(12):
            sm.tick(self.state)
            
        self.assertEqual(sm.earnings_call_weeks_left, 12) # Reset
        self.assertTrue(sm.shareholder_trust < initial_trust) # Trust dropped
        
    def test_pay_dividend(self):
        sm = self.state.stock_manager
        sm.go_public(self.state, 1000000)
        sm.shareholder_trust = 50.0
        
        initial_money = self.state.money
        success, msg = sm.pay_dividend(self.state, 500000)
        
        self.assertTrue(success)
        self.assertTrue(self.state.money < initial_money)
        self.assertTrue(sm.shareholder_trust > 50.0)

if __name__ == '__main__':
    unittest.main()
