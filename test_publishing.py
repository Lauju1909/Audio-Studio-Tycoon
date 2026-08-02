import unittest
from logic import GameState

class TestPublishingManager(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 20000000
        self.pm = self.state.publishing_manager
        
    def test_launch_label(self):
        success, _ = self.pm.launch_label(self.state)
        self.assertTrue(success)
        self.assertTrue(self.pm.is_active)
        self.assertEqual(self.state.money, 10000000)
        
    def test_generate_and_fund_pitch(self):
        self.pm.is_active = True
        
        # Force a pitch
        self.pm._generate_pitch(self.state)
        self.assertEqual(len(self.pm.active_pitches), 1)
        
        pitch_id = self.pm.active_pitches[0]["id"]
        budget = self.pm.active_pitches[0]["budget"]
        initial_money = self.state.money
        
        # Fund the pitch
        success, _ = self.pm.fund_pitch(self.state, pitch_id)
        self.assertTrue(success)
        self.assertEqual(len(self.pm.active_pitches), 0)
        self.assertEqual(len(self.pm.funded_projects), 1)
        self.assertEqual(self.state.money, initial_money - budget)
        
    def test_release_project(self):
        self.pm.is_active = True
        project = {
            "name": "Test Game",
            "studio": "Test Studio",
            "budget": 1000000,
            "revenue_share": 70,
            "weeks_left": 1,
            "base_quality": 80
        }
        self.pm.funded_projects.append(project)
        
        self.state.money
        self.pm.tick(self.state)
        
        # Project should be released (weeks_left went from 1 to 0)
        self.assertEqual(len(self.pm.funded_projects), 0)
        # We should have received an email about the release
        self.assertTrue(any("Release: Test Game" in email.subject for email in self.state.emails))
        
if __name__ == '__main__':
    unittest.main()
