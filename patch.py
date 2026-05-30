import re

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add __init__ vars
content = content.replace('self.office_level = 0  # Index in OFFICE_LEVELS',
    'self.office_level = 0  # Index in OFFICE_LEVELS\n        self.office_perks = []\n        self.stress_level = 0.0\n        self.strike_weeks_left = 0')

# 2. Add Office Perks, Stress, and Headhunting
insert_str = '''
        # Office Perks Overhead
        if getattr(self, 'office_perks', []):
            perk_cost = len(self.office_perks) * 500
            self.money -= perk_cost
            self.track_expense("other", perk_cost)

        # Stress and Strikes
        is_crunching_any = any(ap.get('crunch') for ap in self.active_projects)
        if is_crunching_any:
            self.stress_level = min(100.0, getattr(self, 'stress_level', 0.0) + 5.0)
        else:
            perk_relief = len(getattr(self, 'office_perks', [])) * 2.0
            self.stress_level = max(0.0, getattr(self, 'stress_level', 0.0) - (2.0 + perk_relief))

        if getattr(self, 'stress_level', 0.0) > 80.0 and getattr(self, 'strike_weeks_left', 0) == 0:
            import random
            if random.random() < 0.1: # 10% chance per week
                self.strike_weeks_left = random.randint(1, 4)
                strike_cost = self.strike_weeks_left * 5000
                self.money -= strike_cost
                self.track_expense("other", strike_cost)
                self.stress_level = 0.0
                from models import Email
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_union'),
                    subject=self.get_text('subject_strike'),
                    body=self.get_text('body_strike', weeks=self.strike_weeks_left, cost=strike_cost),
                    date_week=self.week
                ))
                if hasattr(self, 'audio'):
                    self.audio.play_sound('error')

        # Headhunting event
        if not getattr(self, "pending_headhunt_event", None) and self.employees:
            import random
            for emp in self.employees:
                avg_skill = sum(emp.skills.values()) / len(emp.skills) if emp.skills else 0
                if avg_skill >= 80 and random.random() < 0.005:
                    rival_offer = int(emp.salary * random.uniform(1.2, 2.0))
                    self.pending_headhunt_event = {
                        "employee": emp,
                        "rival_offer": rival_offer
                    }
                    self.time_speed = 0
                    break

        # Strike Countdown
        if getattr(self, 'strike_weeks_left', 0) > 0:
            self.strike_weeks_left -= 1
            if self.strike_weeks_left == 0:
                from models import Email
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_union'),
                    subject=self.get_text('subject_strike_ended'),
                    body=self.get_text('body_strike_ended'),
                    date_week=self.week
                ))
'''

target = '        if is_new_month and self.week > 1:'
content = content.replace(target, insert_str + '\n' + target, 1) # ONLY FIRST OCCURRENCE!

target_loop = '''        for ap in self.active_projects:
            proj = ap["project"]'''
replace_loop = '''        for ap in self.active_projects:
            if getattr(self, 'strike_weeks_left', 0) > 0:
                continue
            proj = ap["project"]'''
content = content.replace(target_loop, replace_loop)

target_boost = 'boost *= self.dev_speed_multiplier'
replace_boost = '''boost *= self.dev_speed_multiplier
            if getattr(self, 'office_perks', []):
                boost *= (1.0 + len(self.office_perks) * 0.02)'''
content = content.replace(target_boost, replace_boost)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('logic.py updated.')
