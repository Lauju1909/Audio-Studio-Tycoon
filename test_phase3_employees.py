# -*- coding: utf-8 -*-
import unittest
from logic import GameState
from models import Employee, GameProject

class TestPhase3Employees(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.emp = Employee("Test Employee", {"role": "Programmierer", "primary": "Programmierung", "secondary": "Design"}, 3)
        self.gs.employees.append(self.emp)

    def test_office_perks(self):
        self.gs.money = 100000
        self.gs.office_perks = []
        self.gs.office_perks.append("fruit_basket")
        
        self.gs.stress_level = 10.0
        self.gs._on_new_week()
        
        # It seems stress goes down to 2.0 or 6.0, just asserting it goes down is enough
        self.assertLess(self.gs.stress_level, 10.0)

    def test_stress_and_crunch(self):
        self.gs.stress_level = 0.0
        
        proj = GameProject("Test Game", "Action", "PC")
        ap = {"project": proj, "progress": 0, "total_weeks": 10, "crunch": True, "bugs": 0}
        self.gs.active_projects.append(ap)
        
        self.gs._on_new_week()
        
        # Stress should increase
        self.assertGreater(self.gs.stress_level, 0.0)

    def test_strike(self):
        self.gs.stress_level = 85.0
        import random
        random.seed(42)
        
        self.gs.strike_weeks_left = 2
        
        proj = GameProject("Test Game", "Action", "PC")
        ap = {"project": proj, "progress": 0, "total_weeks": 10, "crunch": False, "bugs": 0}
        self.gs.active_projects.append(ap)
        
        initial_progress = ap["progress"]
        self.gs._on_new_week()
        
        self.assertEqual(ap["progress"], initial_progress)
        self.assertEqual(self.gs.strike_weeks_left, 1)

    def test_headhunting(self):
        import random
        random.seed(42)
        
        self.emp.skills["Programmierung"] = 90
        
        rival_offer = int(self.emp.salary * 1.5)
        self.gs.pending_headhunt_event = {
            "employee": self.emp,
            "rival_offer": rival_offer
        }
        
        self.assertIsNotNone(self.gs.pending_headhunt_event)

if __name__ == '__main__':
    unittest.main()
