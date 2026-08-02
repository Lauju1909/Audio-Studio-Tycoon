import unittest
from logic import GameState
from models import Employee, ContractWorkProject

class TestContractWork(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.gs.money = 100000
        self.gs.prestige = 10
        # Give an employee with high skill to progress fast
        emp = Employee("Test Worker")
        emp.skills = {"Programmierung": 100, "Sound": 100, "Grafik": 100, "Design": 100}
        
        self.gs.employees.append(emp)

    def test_generate_and_start_contract_work(self):
        options = self.gs.generate_contract_work_options()
        self.assertEqual(len(options), 3)
        self.assertIn("target_points", options[0])
        
        # Start the first one
        self.gs.start_contract_work(options[0])
        self.assertEqual(len(self.gs.active_projects), 1)
        ap = self.gs.active_projects[0]
        self.assertIsInstance(ap["project"], ContractWorkProject)
        self.assertFalse(ap["ready_to_finish"])
        
    def test_contract_work_progress(self):
        options = self.gs.generate_contract_work_options()
        # Create a small contract to finish it quickly
        options[0]["target_points"] = 10 
        self.gs.start_contract_work(options[0])
        
        # Tick time to advance a week
        self.gs.update_tick(15000) # One week at normal speed
        
        ap = self.gs.active_projects[0]
        # Should have progressed
        self.assertTrue(ap["project"].current_points > 0)
        
        # Force progress to complete
        ap["project"].current_points = ap["project"].target_points
        self.gs.update_tick(15000)
        self.assertTrue(ap["ready_to_finish"])
        
        # Finish it
        initial_money = self.gs.money
        self.gs.finish_contract_work(ap)
        self.assertTrue(self.gs.money > initial_money)
        self.assertEqual(len(self.gs.active_projects), 0)

if __name__ == "__main__":
    unittest.main()
