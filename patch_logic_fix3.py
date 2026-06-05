import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if 'def start_update_project' in line:
        start_idx = i
        break

for i in range(start_idx, start_idx + 20):
    if 'elif update.update_type == "Content":' in lines[i]:
        lines[i] = lines[i].replace('update.update_type', 'update_type')
    if 'elif update.update_type == "DLC":' in lines[i]:
        lines[i] = lines[i].replace('update.update_type', 'update_type')

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
