import unittest
import random
from logic import GameState
from models import GameProject

class TestAIAssets(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.fans = 100000
        self.state.money = 1000000

    def test_use_ai_assets(self):
        project = GameProject(name="AIGame", topic="Sci-Fi", genre="Action", platform="PC", audience="Jeder", size="AAA", marketing="Groß")
        self.state.active_projects.append({"project": project, "progress": 0, "total_weeks": 10})
        
        # initial state
        self.assertFalse(project.used_ai_assets)
        self.assertEqual(self.state.active_projects[0]["progress"], 0)
        
        # Use AI assets
        success = self.state.use_ai_assets(0)
        self.assertTrue(success)
        self.assertTrue(project.used_ai_assets)
        self.assertEqual(self.state.active_projects[0]["progress"], 3.0) # 30% of 10 weeks
        
        # Test emails
        self.assertTrue(any(e.subject == "KI-Assets integriert" for e in self.state.emails))

    def test_lawsuit_chance(self):
        # We monkey-patch random.random to force lawsuit
        original_random = random.random
        random.random = lambda: 0.1 # Forces lawsuit (< 0.3)
        
        project = GameProject(name="LawsuitGame", topic="Sci-Fi", genre="Action", platform="PC", audience="Jeder", size="AAA", marketing="Groß")
        project.used_ai_assets = True
        self.state.active_projects.append({"project": project, "progress": 10, "total_weeks": 10, "bugs": 0})
        
        # Finishes the game
        self.state.finalize_game(self.state.active_projects[0])
        
        # Restore random
        random.random = original_random
        
        # Check penalties
        self.assertTrue(any("URHEBERRECHTSVERLETZUNG" in e.subject for e in self.state.emails))

if __name__ == '__main__':
    unittest.main()
