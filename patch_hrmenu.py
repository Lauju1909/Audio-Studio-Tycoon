import sys
import re

with open('menus/office.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to HRMenu
old_hr = '''        self.options = [
            {'text': self.game_state.get_text('hr_hire'), 'action': lambda: "hire_menu"},
            {'text': self.game_state.get_text('hr_fire'), 'action': lambda: "fire_menu"},
            {'text': self.game_state.get_text('hr_training', default="Mitarbeiter fortbilden"), 'action': lambda: "training_employee_select"},
            {'text': self.game_state.get_text('teambuilding_menu_title', default='Teambuilding-Event starten'), 'action': lambda: "teambuilding_menu"},
            {'text': self.game_state.get_text('headhunting_menu_title', default='Headhunting-Event starten'), 'action': lambda: "headhunting_event_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]'''

new_hr = '''        self.options = [
            {'text': self.game_state.get_text('hr_hire'), 'action': lambda: "hire_menu"},
            {'text': self.game_state.get_text('hr_fire'), 'action': lambda: "fire_menu"},
            {'text': self.game_state.get_text('hr_training', default="Mitarbeiter fortbilden"), 'action': lambda: "training_employee_select"},
            {'text': self.game_state.get_text('vacation_menu_title', default='Mitarbeiter in Urlaub schicken'), 'action': lambda: "vacation_menu"},
            {'text': self.game_state.get_text('teambuilding_menu_title', default='Teambuilding-Event starten'), 'action': lambda: "teambuilding_menu"},
            {'text': self.game_state.get_text('headhunting_menu_title', default='Headhunting-Event starten'), 'action': lambda: "headhunting_event_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]'''

content = content.replace(old_hr, new_hr)

with open('menus/office.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '"vacation_menu"' not in content:
    content = content.replace('"hr_menu": lambda: HRMenu(audio, state),', '"hr_menu": lambda: HRMenu(audio, state),\n        "vacation_menu": lambda: __import__(\'menus.office\', fromlist=[\'\']).VacationMenu(audio, state),')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched HRMenu and main.py")
