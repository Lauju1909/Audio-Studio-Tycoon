import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('elif update_type == "Content":', 'elif update.update_type == "Content":')
content = content.replace('elif update_type == "DLC":', 'elif update.update_type == "DLC":')

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)

