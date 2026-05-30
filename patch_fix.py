import re

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The injection starts with # Office Perks Overhead
# and ends right before         if is_new_month and self.week > 1:
# Let's find all occurrences of the injection.
injection = '''        # Office Perks Overhead
        if getattr(self, 'office_perks', []):'''

parts = content.split(injection)
if len(parts) > 2:
    # It was injected twice! We want to remove the first one.
    # parts[0] is everything before the first injection.
    # parts[1] is the rest of the first injection + code before the second.
    # We need to find the end of the first injection.
    # The injection ends with             if self.strike_weeks_left == 0:\n                from models import Email\n                self.emails.insert(0, Email(\n                    sender=self.get_text('sender_union'),\n                    subject=self.get_text('subject_strike_ended'),\n                    body=self.get_text('body_strike_ended'),\n                    date_week=self.week\n                ))\n
    end_marker = "date_week=self.week\n                ))\n\n"
    
    # Just git checkout and re-patch, it's safer.
