import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_key = '''        new_active = {
            "update": update,'''

new_key = '''        new_active = {
            "project": update,'''

content = content.replace(old_key, new_key)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched start_update_project to use project key.")
