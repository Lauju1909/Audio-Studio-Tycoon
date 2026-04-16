from .base import Menu
from game_data import TRAINING_OPTIONS, OFFICE_LEVELS

class HRMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hr_menu')
        options = [
            {'text': self.game_state.get_text('hire_employee'), 'action': lambda: "hire_menu"},
            {'text': self.game_state.get_text('fire_employee'), 'action': lambda: "fire_menu"},
            {'text': self.game_state.get_text('training_employee'), 'action': lambda: "training_employee_select"},
            {'text': self.game_state.get_text('menu_teambuilding'), 'action': lambda: "teambuilding_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]
        super().__init__(title, options, audio, game_state)

class HireMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('hire_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        from models import Employee
        import random
        from game_data import EMPLOYEE_ROLES
        
        # Generiere 3 zufällige Kandidaten
        candidates = []
        for _ in range(3):
            role = random.choice(EMPLOYEE_ROLES)
            name = f"{self.game_state.get_text('profi_prefix')} {random.randint(10,99)}"
            salary = random.randint(1000, 5000)
            candidates.append(Employee(name, role, salary))
            
        self.options = []
        for c in candidates:
             txt = f"{c.name} ({c.role}, {self.game_state.get_text('salary_suffix', salary=c.salary)})"
             self.options.append({'text': txt, 'action': lambda emp=c: self._hire(emp)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _hire(self, emp):
        # Check Max Employees
        if len(self.game_state.employees) >= self.game_state.get_max_employees():
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('hire_full'))
            return None
            
        self.game_state.employees.append(emp)
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('hire_success', name=emp.name))
        return "hr_menu"

class FireMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('fire_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for i, emp in enumerate(self.game_state.employees):
            self.options.append({'text': f"{emp.name} ({emp.role})", 'action': lambda idx=i: self._fire(idx)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _fire(self, idx):
        if 0 <= idx < len(self.game_state.employees):
            emp = self.game_state.employees.pop(idx)
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('fire_success', name=emp.name))
        return "hr_menu"

class TrainingEmployeeSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('training_employee'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for i, emp in enumerate(self.game_state.employees):
            self.options.append({'text': f"{emp.name} ({emp.role})", 'action': lambda idx=i: self._select(idx)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _select(self, idx):
        self.game_state.selected_training_employee_idx = idx
        return "training_option_select"

class TrainingOptionMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('training_option'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for opt in TRAINING_OPTIONS:
            self.options.append({'text': f"{opt['name']} ({opt['cost']} EUR)", 'action': lambda o=opt: self._train(o)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "training_employee_select"})

    def _train(self, opt):
         if self.game_state.money >= opt['cost']:
             idx = getattr(self.game_state, 'selected_training_employee_idx', 0)
             if 0 <= idx < len(self.game_state.employees):
                 emp = self.game_state.employees[idx]
                 self.game_state.money -= opt['cost']
                 # Train Logic
                 skill_gain = 5
                 emp.skills[emp.primary_skill] = min(100, emp.skills[emp.primary_skill] + skill_gain)
                 self.audio.play_sound("confirm")
                 self.audio.speak(self.game_state.get_text('training_success', name=emp.name, skill=emp.skills[emp.primary_skill]))
             return "hr_menu"
         else:
             self.audio.play_sound("error")
             self.audio.speak(self.game_state.get_text('not_enough_money'))
             return None

class OfficeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('office_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        current_lvl = self.game_state.office_level
        if current_lvl < len(OFFICE_LEVELS) - 1:
            next_office = OFFICE_LEVELS[current_lvl + 1]
            txt = f"{self.game_state.get_text('upgrade_office')}: {next_office['name']} ({next_office['cost']} EUR)"
            self.options.append({'text': txt, 'action': self._upgrade})
        
        self.options.append({'text': self.game_state.get_text('menu_build_office'), 'action': lambda: "build_menu"})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _upgrade(self):
        if self.game_state.office_level >= len(OFFICE_LEVELS) - 1:
            self.audio.speak(self.game_state.get_text('office_max_level'))
            return None
        next_office = OFFICE_LEVELS[self.game_state.office_level + 1]
        if self.game_state.money >= next_office['cost']:
            self.game_state.money -= next_office['cost']
            self.game_state.office_level += 1
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('office_upgrade_success', name=next_office['name'], max_emp=self.game_state.get_max_employees()))

            return "game_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

class EmailInboxMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('email_inbox'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for i, email in enumerate(self.game_state.emails):
            status = self.game_state.get_text('new_label') + " " if not getattr(email, 'is_read', True) else ""
            txt = f"{status}{email.sender}: {email.subject}"
            self.options.append({'text': txt, 'action': lambda idx=i: self._read(idx)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"} )

    def _read(self, idx):
        self.game_state.selected_email_idx = idx
        return "email_detail"

class EmailDetailMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        idx = getattr(self.game_state, 'selected_email_idx', 0)
        if 0 <= idx < len(self.game_state.emails):
            email = self.game_state.emails[idx]
            email.is_read = True
            title = f"{email.sender}: {email.subject}"
            self.email_body = email.body
        else:
            title = self.game_state.get_text('email_title')
            self.email_body = ""

        options = [
            {'text': self.game_state.get_text('delete_email'), 'action': self._delete},
            {'text': self.game_state.get_text('back'), 'action': lambda: "email_inbox"}
        ]
        super().__init__(title, options, audio, game_state)

    def announce_entry(self):
        super().announce_entry()
        if self.email_body:
            self.audio.speak(self.email_body, interrupt=False)

    def _delete(self):
        idx = getattr(self.game_state, 'selected_email_idx', 0)
        if 0 <= idx < len(self.game_state.emails):
            self.game_state.emails.pop(idx)
            self.audio.play_sound("confirm")
        return "email_inbox"
