import codecs

lines = []
with codecs.open('logic.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_block = """            # -----------------------------------------------
            # Krankheitsausfaelle & Burnout
            # -----------------------------------------------
            is_emp_crunching = False
            for ap in self.active_projects:
                if ap.get("crunch") and emp in self._active_employees(ap["project"]):
                    is_emp_crunching = True
                    break
                    
            if is_emp_crunching:
                emp.crunch_weeks = getattr(emp, "crunch_weeks", 0) + 1
            else:
                emp.crunch_weeks = max(0, getattr(emp, "crunch_weeks", 0) - 1)

            if getattr(emp, 'is_sick', False):
                emp.sick_weeks_left -= 1
                if emp.sick_weeks_left <= 0:
                    emp.is_sick = False
                    self.emails.insert(0, Email(
                        sender=self.get_text('sender_hr'),
                        subject=self.get_text('subject_sick_recovered', name=emp.name),
                        body=self.get_text('body_sick_recovered', name=emp.name),
                        date_week=self.week
                    ))
                continue  # Kranke nicht kuendigen / keine Gehaltsanfragen
                
            if not emp.is_sick and not emp.is_training:
                sick_chance = 0.01
                if emp.morale < 30:
                    sick_chance = 0.08
                elif emp.morale < 60:
                    sick_chance = 0.03
                    
                # Burnout Modifier
                if getattr(emp, "crunch_weeks", 0) > 4:
                    sick_chance += 0.10 * (emp.crunch_weeks - 4)
                    
                # HR Perks reduction
                perks = getattr(self, "office_perks", [])
                if "hr_department" in perks: sick_chance -= 0.05
                if "wellness_benefits" in perks: sick_chance -= 0.05
                if "therapist" in perks: sick_chance -= 0.08
                
                sick_chance = max(0.01, sick_chance)

                if random.random() < sick_chance:
                    emp.is_sick = True
                    emp.sick_weeks_left = random.randint(1, 3)
                    if getattr(emp, "crunch_weeks", 0) > 4:
                        emp.sick_weeks_left += 2 # Burnout dauert laenger
                    self.emails.insert(0, Email(
                        sender=self.get_text('sender_hr'),
                        subject=self.get_text('subject_sick', name=emp.name),
                        body=self.get_text('body_sick', name=emp.name, weeks=emp.sick_weeks_left),
                        date_week=self.week
                    ))
                    continue

                # Kuendigung wegen Burnout
                quit_chance = 0.0
                if emp.morale == 0: quit_chance += 0.05
                if getattr(emp, "crunch_weeks", 0) > 8: quit_chance += 0.15
                
                if "hr_department" in perks: quit_chance -= 0.05
                if "therapist" in perks: quit_chance -= 0.10
                
                if quit_chance > 0 and random.random() < quit_chance:
                    quitting_employees.append(emp)
                    if getattr(emp, "crunch_weeks", 0) > 8:
                        self.emails.insert(0, Email(
                            sender=self.get_text('sender_hr'),
                            subject=self.get_text('subject_burnout_quit'),
                            body=self.get_text('body_burnout_quit', name=emp.name),
                            date_week=self.week
                        ))
                    continue
"""

# Find the broken block
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '# Krankheitsausflle & Burnout' in line:
        start_idx = i - 1
    if '            # Gehaltsforderung (E-Mail)' in line and start_idx != -1:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + [new_block + '\n'] + lines[end_idx:]

with codecs.open('logic.py', 'w', 'utf-8') as f:
    f.writelines(lines)
