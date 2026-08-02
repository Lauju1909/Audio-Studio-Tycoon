import unittest
import random
from logic import GameState
from models import Employee
from menus.gameplay import UnionEventMenu

class MockAudio:
    def speak(self, text, interrupt=False):
        pass
    def play_sound(self, sound):
        pass

class TestUnionSystem(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.fans = 100000
        self.state.money = 1000000
        self.state.employees.clear()
        
        # Add employees
        for _ in range(5):
            emp = Employee(name="Test")
            emp.salary = 2000
            emp.morale = 20
            self.state.employees.append(emp)

    def test_raise_salaries(self):
        self.state.pending_union_event = {"type": "formation"}
        menu = UnionEventMenu(MockAudio(), self.state)
        menu._raise_salaries()
        
        self.assertTrue(self.state.has_union)
        self.assertIsNone(self.state.pending_union_event)
        self.assertEqual(self.state.employees[0].salary, 2600) # 2000 * 1.3
        self.assertEqual(self.state.employees[0].morale, 100)

    def test_pay_bonus(self):
        self.state.pending_union_event = {"type": "strike_threat"}
        menu = UnionEventMenu(MockAudio(), self.state)
        menu._pay_bonus()
        
        self.assertTrue(self.state.has_union)
        self.assertIsNone(self.state.pending_union_event)
        # Cost is 5 * 10k = 50k (plus track_expense 50k if not init)
        self.assertTrue(self.state.money <= 950000)
        self.assertEqual(self.state.employees[0].morale, 50) # 20 + 30

    def test_union_busting_success(self):
        original_random = random.random
        random.random = lambda: 0.1 # Forces success (< 0.5)
        
        self.state.pending_union_event = {"type": "strike_threat"}
        menu = UnionEventMenu(MockAudio(), self.state)
        menu._union_busting()
        
        random.random = original_random
        
        self.assertFalse(self.state.has_union)
        self.assertTrue(len(self.state.employees) < 5) # 1-2 fired
        self.assertEqual(self.state.fans, 50000) # 100k - 50k

    def test_union_busting_fail(self):
        original_random = random.random
        random.random = lambda: 0.9 # Forces fail (>= 0.5)
        
        self.state.pending_union_event = {"type": "strike_threat"}
        menu = UnionEventMenu(MockAudio(), self.state)
        menu._union_busting()
        
        random.random = original_random
        
        self.assertTrue(self.state.has_union)
        self.assertTrue(self.state.money <= 500000) # 500k penalty + track_expense

    def test_ignore(self):
        self.state.pending_union_event = {"type": "strike_threat"}
        menu = UnionEventMenu(MockAudio(), self.state)
        menu._ignore()
        
        self.assertTrue(self.state.has_union)
        self.assertTrue(self.state.strike_weeks_left >= 3)
        self.assertIsNone(self.state.pending_union_event)

if __name__ == '__main__':
    unittest.main()
