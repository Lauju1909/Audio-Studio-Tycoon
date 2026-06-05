import sys

with open('menus/office.py', 'r', encoding='utf-8') as f:
    content = f.read()

vacation_code = '''
class VacationMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('vacation_menu_title', default='Mitarbeiter in Urlaub schicken'), [], audio, game_state)

    def announce_entry(self):
        self.options = []
        for idx, emp in enumerate(self.game_state.employees):
            if getattr(emp, 'is_sick', False) or getattr(emp, 'is_training', False) or getattr(emp, 'vacation_weeks_left', 0) > 0:
                continue
            
            fatigue = getattr(emp, 'fatigue', 0)
            self.options.append({
                'text': self.game_state.get_text('vacation_employee_option', name=emp.name, fatigue=fatigue, default=f'{emp.name} (Erschoepfung: {fatigue}%)'),
                'action': lambda i=idx: self.send_on_vacation(i)
            })

        if not self.options:
            self.options.append({'text': self.game_state.get_text('vacation_none_available', default='Keine verfuegbaren Mitarbeiter.'), 'action': None})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})
        super().announce_entry()

    def send_on_vacation(self, idx):
        emp = self.game_state.employees[idx]
        emp.vacation_weeks_left = 4  # 4 weeks vacation
        self.audio.speak(self.game_state.get_text('vacation_success', name=emp.name, default=f'{emp.name} ist nun fuer 4 Wochen im Urlaub.'))
        return "vacation_menu"
'''

content += vacation_code

with open('menus/office.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added VacationMenu to office.py")
