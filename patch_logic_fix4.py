import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('elif update_type == "Language":', 'elif update.update_type == "Language":')

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
