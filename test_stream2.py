import unittest
from logic import GameState
from game_data import WEEKS_PER_YEAR, START_YEAR

class TestStreamingPlatform(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 20000000
        
    def test_found_streaming_platform(self):
        # Initial year is 1930
        self.assertFalse(self.state.found_streaming_platform())
        
        self.state.week = (2011 - START_YEAR) * WEEKS_PER_YEAR + 1
        self.assertTrue(self.state.found_streaming_platform())
        self.assertIsNotNone(self.state.streaming_platform)
        self.assertEqual(self.state.money, 10000000)

    def test_upgrade_server(self):
        self.state.week = (2011 - START_YEAR) * WEEKS_PER_YEAR + 1
        self.state.found_streaming_platform()
        
        self.assertTrue(self.state.upgrade_streaming_server())
        self.assertEqual(self.state.streaming_platform.server_level, 2)
        self.assertEqual(self.state.money, 5000000)

    def test_monthly_update(self):
        self.state.week = (2011 - START_YEAR) * WEEKS_PER_YEAR + 1
        self.state.found_streaming_platform()
        self.state.streaming_platform.subscribers = 1000
        
        self.state._process_streaming_platform_monthly()
        
        # 50,000 cost, revenue = 1000 * 4.5 = 4500. Growth = 1000 * 1.05 + 1000 = 2050
        self.assertEqual(self.state.streaming_platform.subscribers, 2050)
        self.assertEqual(len(self.state.emails), 1)

if __name__ == '__main__':
    unittest.main()
