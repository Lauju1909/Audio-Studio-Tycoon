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
        
        # Simuliere viele Wochen um Quit zu erzwingen (Chance 0.15)
        quit_happened = False
        for _ in range(50):
            if not self.state.employees:
                quit_happened = True
                break
            self.state._on_new_week()
            # Moral wieder auf 0 zwingen falls es durch andere Effekte hoch geht
            self.emp.morale = 0
            
        self.assertTrue(quit_happened)

if __name__ == '__main__':
    unittest.main()
