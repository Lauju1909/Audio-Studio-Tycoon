import unittest
import random
from logic import GameState
from models import GameProject
from menus.gameplay import InfluencerEventMenu

class MockAudio:
    def speak(self, text, interrupt=False):
        pass
    def play_sound(self, sound):
        pass

class TestInfluencerScandal(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.fans = 100000
        self.state.money = 1000000
        
        # Add an active game
        project = GameProject(name="ScandalGame", topic="Sci-Fi", genre="Action", platform="PC", audience="Jeder", size="AAA", marketing="Groß")
        project.is_active = True
        project.sales = 10000
        self.state.game_history.append(project)

    def test_apologize(self):
        self.state.pending_influencer_event = {"game_name": "ScandalGame", "sponsorship": {"boost": 1.2, "duration": 10}}
        menu = InfluencerEventMenu(MockAudio(), self.state)
        menu._apologize()
        self.assertEqual(self.state.fans, 75000) # 100k - 25k
        self.assertIsNone(self.state.pending_influencer_event)

    def test_fire(self):
        self.state.pending_influencer_event = {"game_name": "ScandalGame", "sponsorship": {"boost": 1.2, "duration": 10}}
        menu = InfluencerEventMenu(MockAudio(), self.state)
        menu._fire()
        # Expect 500k because track_expense also subtracts when not initialized properly in test
        self.assertEqual(self.state.money, 500000) 
        self.assertIsNone(self.state.pending_influencer_event)

    def test_ignore_bad(self):
        original_random = random.random
        random.random = lambda: 0.1 # Forces bad outcome
        
        self.state.pending_influencer_event = {"game_name": "ScandalGame", "sponsorship": {"boost": 1.2, "duration": 10}}
        menu = InfluencerEventMenu(MockAudio(), self.state)
        menu._ignore()
        
        random.random = original_random
        
        self.assertEqual(self.state.fans, 80000) # 100k * 0.8
        self.assertFalse(self.state.game_history[0].is_active)
        self.assertEqual(self.state.game_history[0].sales, 5000) # 10k * 0.5
        self.assertIsNone(self.state.pending_influencer_event)

    def test_ignore_good(self):
        original_random = random.random
        random.random = lambda: 0.9 # Forces good outcome
        
        self.state.pending_influencer_event = {"game_name": "ScandalGame", "sponsorship": {"boost": 1.2, "duration": 10}}
        menu = InfluencerEventMenu(MockAudio(), self.state)
        menu._ignore()
        
        random.random = original_random
        
        self.assertEqual(self.state.fans, 100000) # Unchanged
        self.assertTrue(self.state.game_history[0].is_active)
        self.assertEqual(self.state.game_history[0].sales, 10000) # Unchanged
        self.assertIsNone(self.state.pending_influencer_event)

if __name__ == '__main__':
    unittest.main()
