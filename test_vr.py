import unittest
from logic import GameState
from models import Employee, GameProject

class TestVRSystem(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 10000000
        self.state.fans = 100000
        self.state.employees.clear()
        
        # Add high-level employees
        for _ in range(5):
            emp = Employee(name="Pro")
            emp.salary = 5000
            emp.skill_level = 5
            self.state.employees.append(emp)

    def test_vr_dev_cost_and_price(self):
        project = GameProject(name="VR Game", topic="Sci-Fi", genre="Action", platform="Oculus Rift (VR)")
        project.assigned_employee_ids = [0, 1, 2, 3, 4]
        
        # Test Cost
        dev_cost = self.state.calculate_dev_cost(project)
        # base_cost = 10000 * 1.0 * 2.5 = 25000
        # salary_cost = 5 * 5000 * 6 * 2.0 = 300000
        self.assertEqual(dev_cost, 325000)

        # Test finalize Price and Fan Gain
        class MockReview:
            average = 80
            scores = [80, 80, 80, 80]
        project.review = MockReview()
        project.sales = 0
        
        self.state.active_projects.append({
            "project": project,
            "progress": 0,
            "total_weeks": 8,
            "duration_weeks": 8, "bugs": 0
        })
        
        old_fans = self.state.fans
        self.state.finalize_game(self.state.active_projects[0])
        print("OLD FANS:", old_fans, "NEW FANS:", self.state.fans, "NEW REVENUE:", project.revenue)
        
        # Since price is 1.5x, and fan_gain is 3x for VR if review >= 75
        self.assertTrue(self.state.fans > old_fans)

    def test_vr_dev_speed_penalty(self):
        project = GameProject(name="VR Bad Game", topic="Sci-Fi", genre="Action", platform="Oculus Rift (VR)")
        # Make employees bad
        for emp in self.state.employees:
            emp.skill_level = 2
            emp.assigned_project = project
            
        self.state.active_projects.append({
            "project": project,
            "progress": 0,
            "total_weeks": 8,
            "duration_weeks": 8, "bugs": 0
        })
        
        # Mock logic.update_tick internal behavior
        old_progress = self.state.active_projects[0]["progress"]
        
        # We manually step `_on_new_week` but we can't easily because progress is done every tick.
        # Let's just run update_tick for 1 week (15000 ms)
        self.state.update_tick(15000)
        new_progress = self.state.active_projects[0]["progress"]
        
        # 0.4 penalty for low skill!
        self.assertTrue(new_progress < 1.0) # Should be significantly slow!

if __name__ == '__main__':
    unittest.main()
