import sys

with open('models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to __init__
old_init = '''        self.is_sick = False
        self.is_crunching = False'''

new_init = '''        self.is_sick = False
        self.is_crunching = False
        self.fatigue = 0           # 0-100, steigt bei Arbeit
        self.vacation_weeks_left = 0 # Wenn > 0, ist der Mitarbeiter im Urlaub'''

content = content.replace(old_init, new_init)

# Add to to_dict
old_dict = '''            "is_crunching": getattr(self, "is_crunching", False)
        }'''
new_dict = '''            "is_crunching": getattr(self, "is_crunching", False),
            "fatigue": getattr(self, "fatigue", 0),
            "vacation_weeks_left": getattr(self, "vacation_weeks_left", 0)
        }'''
content = content.replace(old_dict, new_dict)

# Add to from_dict
old_from = '''        emp.is_crunching = ed.get("is_crunching", False)
        return emp'''
new_from = '''        emp.is_crunching = ed.get("is_crunching", False)
        emp.fatigue = ed.get("fatigue", 0)
        emp.vacation_weeks_left = ed.get("vacation_weeks_left", 0)
        return emp'''
content = content.replace(old_from, new_from)

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched Employee models for vacation")
