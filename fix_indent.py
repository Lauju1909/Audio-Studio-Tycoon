
with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """                    base_points = emp.skills.get(skill_name, 50) / 10.0
                        if 'Agile Coach' in getattr(emp, 'talents', []):
                            base_points *= 1.2
                        points_added += base_points"""

replacement = """                    base_points = emp.skills.get(skill_name, 50) / 10.0
                    if 'Agile Coach' in getattr(emp, 'talents', []):
                        base_points *= 1.2
                    points_added += base_points"""

if target in content:
    content = content.replace(target, replacement)
    with open('logic.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed indentation in logic.py")
else:
    print("Could not find target to fix")
