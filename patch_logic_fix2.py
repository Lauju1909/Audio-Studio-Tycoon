import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the ones in start_update_project
old1 = '''        if update_type == "Patch":
            # Repariert 50% der Bugs
            dev_cost = 5000
            total_weeks = 2
        elif update.update_type == "Content":
            # ErhÃ¶ht Hype und Fans
            dev_cost = 20000
            total_weeks = 4
        elif update.update_type == "DLC":
            # Kostet mehr, bringt aber Einnahmen
            dev_cost = 50000'''

new1 = '''        if update_type == "Patch":
            # Repariert 50% der Bugs
            dev_cost = 5000
            total_weeks = 2
        elif update_type == "Content":
            # ErhÃ¶ht Hype und Fans
            dev_cost = 20000
            total_weeks = 4
        elif update_type == "DLC":
            # Kostet mehr, bringt aber Einnahmen
            dev_cost = 50000'''

content = content.replace(old1, new1)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)

