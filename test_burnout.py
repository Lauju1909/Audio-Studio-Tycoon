import unittest
from logic import GameState
from models import Employee, GameProject

class TestBurnoutSystem(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.money = 1000000
        self.state.employees.clear()
        
        # Add test employee
        self.emp = Employee(name="Test Employee")
        self.emp.morale = 100
        import random
        random.seed(42)
        self.emp.crunch_weeks = 0
        self.state.employees.append(self.emp)

    def test_crunch_weeks_increment(self):
        # Create an active project with crunch
        proj = GameProject(name="Crunchy", size="Indie", topic="Action", genre="RPG")
        proj.assigned_employee_ids = [0]
        ap = {
            "project": proj,
            "progress": 0,
            "total_weeks": 10,
            "crunch": True,
            "bugs": 0
        }
        self.state.active_projects.append(ap)
        
        # Simuliere Woche
        self.state._on_new_week()
        self.assertEqual(self.emp.crunch_weeks, 1)
        
        self.state._on_new_week()
        self.assertEqual(self.emp.crunch_weeks, 2)
        
        # Crunch aus
        ap["crunch"] = False
        self.state._on_new_week()
        self.assertEqual(self.emp.crunch_weeks, 1)

    def test_burnout_quit(self):
        # Force high crunch weeks and low morale
        self.emp.crunch_weeks = 9
        self.emp.morale = 0
        self.state.crunch_active = True # Verhindert morale-regeneration
        
        # Create an active project with crunch so crunch_weeks stays high
        proj = GameProject(name="Crunchy", size="Indie", topic="Action", genre="RPG")
        proj.assigned_employee_ids = [0]
        ap = {
            "project": proj,
            "crunch": True,
            "progress": 0,
            "total_weeks": 10,
            "bugs": 0
        }
        self.state.active_projects.append(ap)
        
        # Simuliere viele Wochen um Quit zu erzwingen (Chance 0.15)
        quit_happened = False
        import unittest.mock as mock
        def fake_random():
            fake_random.count += 1
            # 1st call per loop is usually sick_chance, 2nd is quit_chance
            if fake_random.count % 2 == 1:
                return 0.99 # Don't get sick
            return 0.01 # Quit

        fake_random.count = 0

        with mock.patch('random.random', side_effect=fake_random):
            for _ in range(50):
                if not self.state.employees:
                    quit_happened = True
                    break
                self.state._on_new_week()
                self.emp.morale = 0
            
        self.assertTrue(quit_happened)

if __name__ == '__main__':
    unittest.main()

