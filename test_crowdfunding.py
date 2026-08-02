import unittest
from logic import GameState
from models import Employee

class TestCrowdfundingSystem(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 1000000
        self.state.fans = 10000
        self.state.hype = 10
        self.state.employees.clear()
        
        # Add high-level employees
        for _ in range(5):
            emp = Employee(name="Pro")
            emp.salary = 5000
            emp.skill_level = 5
            self.state.employees.append(emp)

    def test_start_campaign_success(self):
        self.state.current_draft = {"name": "TestCF", "topic": "Sci-Fi", "genre": "Action"}
        self.state.fans = 1000000 # Massig fans
        
        success, reason = self.state.start_crowdfunding_campaign(100000)
        
        self.assertTrue(success)
        self.assertTrue(len(self.state.active_crowdfundings) == 1)
        self.assertTrue(self.state.active_projects[-1]["project"].is_crowdfunded)

    def test_start_campaign_failure(self):
        self.state.current_draft = {"name": "TestCF", "topic": "Sci-Fi", "genre": "Action"}
        self.state.fans = 10 # Keine fans
        self.state.hype = 10
        
        success, reason = self.state.start_crowdfunding_campaign(1000000)
        
        self.assertFalse(success)
        self.assertTrue(len(self.state.active_crowdfundings) == 0)

    def test_campaign_deadline_penalty(self):
        self.state.current_draft = {"name": "TestCF", "topic": "Sci-Fi", "genre": "Action"}
        self.state.fans = 1000000
        self.state.start_crowdfunding_campaign(100000)
        
        # Simulieren Ablauf der Frist
        cf = self.state.active_crowdfundings[0]
        cf["deadline_week"] = self.state.week - 1
        
        old_fans = self.state.fans
        self.state._on_new_week()
        
        self.assertTrue(self.state.fans < old_fans)
        self.assertTrue(len(self.state.active_crowdfundings) == 0)
        self.assertTrue(len(self.state.emails) > 0)

if __name__ == '__main__':
    unittest.main()
