import re

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken Crunch-Survivor replacements
content = re.sub(
    r"(\s*)if 'Crunch-Survivor' in getattr\(emp, 'talents', \[\]\):\s*emp\.morale = 100\s*else:\s*emp\.morale = max\(0, emp\.morale - morale_loss\)",
    r"\1if 'Crunch-Survivor' in getattr(emp, 'talents', []):\n\1    emp.morale = 100\n\1else:\n\1    emp.morale = max(0, emp.morale - morale_loss)",
    content
)

content = re.sub(
    r"(\s*)if 'Crunch-Survivor' in getattr\(emp, 'talents', \[\]\):\s*emp\.morale = 100\s*else:\s*emp\.morale = max\(0, emp\.morale - 1\)",
    r"\1if 'Crunch-Survivor' in getattr(emp, 'talents', []):\n\1    emp.morale = 100\n\1else:\n\1    emp.morale = max(0, emp.morale - 1)",
    content
)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed Crunch-Survivor indentations")
