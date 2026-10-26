"""Personal-System (HR): Einstellen, Entlassen, Gehaelter. Mixin fuer GameState."""
import random

from models import Employee
from game_data import EMPLOYEE_ROLES, WEEKS_PER_YEAR


class HRMixin:
    def get_max_employees(self):
        """Maximale Mitarbeiter basierend auf Bauräumen."""
        max_emp = 1 # Start in Garage
        for item in getattr(self, "office_items", []):
            if "employees" in item:
                max_emp += item["employees"]
        return max_emp

    def can_hire(self):
        return len(self.employees) < self.get_max_employees()

    def generate_candidate(self):
        """Generiert einen zufälligen Bewerber."""
        from game_data import EMPLOYEE_SPECIALIZATIONS
        role_data = random.choice(EMPLOYEE_ROLES)
        level = random.randint(1, min(3, 1 + self.games_made // 3))
        
        spec = None
        if random.random() < 0.3: # 30% Chance auf Spezialisierung
            spec = random.choice(EMPLOYEE_SPECIALIZATIONS)
            
        return Employee(role_data=role_data, skill_level=level, specialization=spec)

    def hire_employee(self, employee):
        """Stellt einen Mitarbeiter ein."""
        if not self.can_hire():
            return False
        # Einstellungsgebühr = 2 Wochen Gehalt
        hire_cost = employee.salary * 2
        if self.money < hire_cost:
            if hasattr(self, 'audio'):
                self.audio.play_sound('error')
            return False
            
        self.track_expense("staff", hire_cost)
        if hasattr(self, 'audio'):
            self.audio.play_sound('buy')
            self.audio.speak(self.get_text('employee_hired', name=employee.name), interrupt=True)
        self.employees.append(employee)
        return True

    def fire_employee(self, index):
        """Entlässt einen Mitarbeiter."""
        if 0 <= index < len(self.employees):
            emp = self.employees[index]
            if getattr(emp, "is_ceo", False):
                return None # Chef kann nicht gefeuert werden
            self.employees.pop(index)
            # Abfindung = 1 Monat Gehalt (entspricht ca. 4 Wochen)
            self.track_expense("salaries", emp.salary)
            return emp
        return None

    def pay_salaries(self):
        """Bezahlt alle Gehälter (monatlich aufgestaut)."""
        total = sum(e.salary for e in self.employees)
        # Wir stauen sie wöchentlich auf (salary / weeks_per_month) und zahlen bei Monatswechsel.
        weeks_per_month = WEEKS_PER_YEAR / 12.0
        weekly_share = total / weeks_per_month
        self.accrued_salaries += weekly_share
        return weekly_share
