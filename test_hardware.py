import unittest
from logic import GameState

class TestHardwareSystem(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 200000000 # 200 Mio
        self.state.week = 52 * 15 # Jahr 2005
        
    def test_console_creation_and_sales(self):
        from models import CustomConsole
        self.state.current_console_draft = CustomConsole(
            name="SuperStation",
            architecture="RISC",
            performance=5,
            marketing_budget=10000000,
            dev_cost=100000000,
            release_week=0
        )
        
        self.state.is_developing_console = True
        self.state.console_progress = 0
        self.state.console_total_weeks = 15
        
        # Simuliere Entwicklung
        self.state.week += 150
        for _ in range(150):
            self.state._on_new_week()
            
        self.assertFalse(self.state.is_developing_console)
        self.assertTrue(hasattr(self.state, 'custom_consoles'))
        self.assertEqual(len(self.state.custom_consoles), 1)
        
        console = self.state.custom_consoles[0]
        self.assertEqual(console.name, "SuperStation")
        self.assertEqual(console.performance, 5)
        
        # Teste Verkaufs-Generierung
        initial_money = self.state.money
        self.state._on_new_week() # Trigger sales
        
        self.assertGreater(self.state.money, initial_money) # Hardware generates money!
        self.assertGreater(console.units_sold, 0)
        self.assertGreater(console.market_share, 0.05)
        
    def test_exclusive_game_boost(self):
        self.test_console_creation_and_sales()
        console = self.state.custom_consoles[0]
        console.hype = 0 # Disable hype decay interference
        
        # Verkaeufe vor Exklusivspiel
        units_sold_before = console.units_sold
        self.state._on_new_week()
        base_sales = console.units_sold - units_sold_before
        
        # Erstelle ein erfolgreiches Exklusivspiel
        from models import GameProject, ReviewScore
        game = GameProject(name="Halo", topic="FPS", genre="Action", platform="SuperStation", size="AAA")
        game.sales = 5000000
        game.review = ReviewScore([95, 90, 92, 98]) # Very good review
        self.state.game_history.append(game)
        
        # Verkaeufe NACH Exklusivspiel
        units_sold_mid = console.units_sold
        self.state._on_new_week()
        boosted_sales = console.units_sold - units_sold_mid
        
        print(f"Base: {base_sales}, Boosted: {boosted_sales}")
        
        # Verkaeufe sollten signifikant gestiegen sein (exclusives_bonus)
        self.assertGreater(boosted_sales, base_sales * 2)

if __name__ == '__main__':
    unittest.main()
