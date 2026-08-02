import unittest
from logic import GameState
from models import GameProject

class TestDRMSystem(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 1000000

    def test_drm_0_pc(self):
        p = GameProject(name="Test", size="Indie", topic="Sci-Fi", genre="Action", platform="PC")
        p.drm_level = 0
        p.review = lambda: None
        p.review.average = 8.0
        
        sales = self.state.calculate_sales(p)
        
        self.assertTrue(p.pirated_copies > 0)
        self.assertTrue(p.pirated_copies > sales * 0.4) # roughly 35% of total => 35/(100-35) ~ 53% of sales

    def test_drm_2_pc(self):
        p = GameProject(name="Test", size="Indie", topic="Sci-Fi", genre="Action", platform="PC")
        p.drm_level = 2
        p.review = lambda: None
        p.review.average = 8.0
        
        sales = self.state.calculate_sales(p)
        
        self.assertTrue(p.pirated_copies < sales * 0.05)

if __name__ == '__main__':
    unittest.main()
