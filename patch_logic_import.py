import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_update = '''        elif update_type == "Language":
            # Fuegt neue Sprachen hinzu
            langs = selected_languages or []
            dev_cost = len(langs) * 10000
            # Mindestens 1 Woche, um ZeroDivisionError zu vermeiden
            total_weeks = max(1, len(langs))

        update = UpdateProject(
            base_game_name=game_name,'''

new_update = '''        elif update_type == "Language":
            # Fuegt neue Sprachen hinzu
            langs = selected_languages or []
            dev_cost = len(langs) * 10000
            # Mindestens 1 Woche, um ZeroDivisionError zu vermeiden
            total_weeks = max(1, len(langs))

        from models import UpdateProject
        update = UpdateProject(
            base_game_name=game_name,'''

if "from models import UpdateProject" not in content:
    content = content.replace(old_update, new_update)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched logic.py with UpdateProject import")
