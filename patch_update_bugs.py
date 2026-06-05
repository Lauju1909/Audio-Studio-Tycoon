import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_dict = '''        new_active = {
            "project": update,
            "progress": 0.0,
            "total_weeks": total_weeks
        }'''

new_dict = '''        new_active = {
            "project": update,
            "progress": 0.0,
            "total_weeks": total_weeks,
            "bugs": 0
        }'''

content = content.replace(old_dict, new_dict)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added bugs key to start_update_project")
