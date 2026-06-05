import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_loop = '''            if is_emp_crunching:
                emp.crunch_weeks = getattr(emp, "crunch_weeks", 0) + 1
            else:
                emp.crunch_weeks = max(0, getattr(emp, "crunch_weeks", 0) - 1)

            if getattr(emp, 'is_sick', False):'''

new_loop = '''            if is_emp_crunching:
                emp.crunch_weeks = getattr(emp, "crunch_weeks", 0) + 1
            else:
                emp.crunch_weeks = max(0, getattr(emp, "crunch_weeks", 0) - 1)

            # Vacation Logic
            if getattr(emp, 'vacation_weeks_left', 0) > 0:
                emp.vacation_weeks_left -= 1
                emp.fatigue = max(0, getattr(emp, 'fatigue', 0) - 20)
                emp.morale = min(100, emp.morale + 10)
                continue

            # Fatigue Logic
            is_working = self.is_developing or getattr(self, 'active_custom_console', None) or len(getattr(self, 'active_ports', [])) > 0 or len(getattr(self, 'active_contract_works', [])) > 0
            if is_working and not emp.is_training and not getattr(emp, 'is_sick', False):
                emp.fatigue = getattr(emp, 'fatigue', 0) + random.randint(1, 3)
                if is_emp_crunching:
                    emp.fatigue += 5
            else:
                emp.fatigue = max(0, getattr(emp, 'fatigue', 0) - 2)

            if getattr(emp, 'fatigue', 0) >= 100 and not getattr(emp, 'is_sick', False):
                emp.fatigue = 0
                emp.is_sick = True
                emp.sick_weeks_left = random.randint(3, 6)
                emp.morale = max(0, emp.morale - 30)
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_hr'),
                    subject=self.get_text('subject_burnout', default='Mitarbeiter-Burnout!'),
                    body=self.get_text('body_burnout', name=emp.name, default=f'{emp.name} hat einen Burnout erlitten und faellt fuer {emp.sick_weeks_left} Wochen aus!'),
                    date_week=self.week
                ))
                continue

            if getattr(emp, 'is_sick', False):'''

content = content.replace(old_loop, new_loop)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched logic.py with fatigue and vacation")
