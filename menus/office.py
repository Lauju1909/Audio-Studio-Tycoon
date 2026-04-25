from .base import Menu
from game_data import TRAINING_OPTIONS, OFFICE_LEVELS, OFFICE_UPGRADES

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
            # Status-Tags: [Training] oder [Krank] anzeigen
            if getattr(emp, 'is_training', False):
                weeks_left = getattr(emp, 'training_weeks_left', 0)
                status = self.game_state.get_text('training_status_tag', weeks=weeks_left)
                txt = f"[T] {emp.name} ({emp.role}) — {status}"
            elif getattr(emp, 'is_sick', False):
                weeks_left = getattr(emp, 'sick_weeks_left', 0)
                status = self.game_state.get_text('sick_status_tag', weeks=weeks_left)
                txt = f"[K] {emp.name} ({emp.role}) — {status}"
            else:
                txt = f"{emp.name} ({emp.role})"
            self.options.append({'text': txt, 'action': lambda idx=i: self._select(idx)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _select(self, idx):
        emp = self.game_state.employees[idx]
        if getattr(emp, 'is_training', False):
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('training_already_in'))
            return None
        if getattr(emp, 'is_sick', False):
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('training_sick_blocked'))
            return None
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
        idx = getattr(self.game_state, 'selected_training_employee_idx', 0)
        emp = self.game_state.employees[idx] if 0 <= idx < len(self.game_state.employees) else None
        emp_name = emp.name if emp else "?"

        for opt in TRAINING_OPTIONS:
            lock = opt.get('lock_weeks', 1)
            boost = opt.get('skill_boost', 0)
            is_spec = opt.get('is_specialization', False)
            if is_spec:
                desc = self.game_state.get_text('training_option_spec_desc', cost=opt['cost'], weeks=lock)
            else:
                desc = self.game_state.get_text('training_option_desc', cost=opt['cost'], boost=boost, weeks=lock)
            txt = f"{opt['name']} — {desc}"
            self.options.append({'text': txt, 'action': lambda o=opt: self._train(o)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "training_employee_select"})

    def _train(self, opt):
        idx = getattr(self.game_state, 'selected_training_employee_idx', 0)
        ok, result = self.game_state.start_training(idx, opt)
        if ok:
            emp = self.game_state.employees[idx]
            self.audio.play_sound("confirm")
            is_spec = opt.get('is_specialization', False)
            if is_spec:
                spec_name = emp.specialization['name'] if emp.specialization else "?"
                self.audio.speak(self.game_state.get_text('training_started_spec', name=emp.name, spec=spec_name, weeks=result))
            else:
                self.audio.speak(self.game_state.get_text('training_started', name=emp.name, opt=opt['name'], weeks=result))
            return "hr_menu"
        else:
            self.audio.play_sound("error")
            if result == "no_money":
                self.audio.speak(self.game_state.get_text('not_enough_money'))
            elif result == "already_training":
                self.audio.speak(self.game_state.get_text('training_already_in'))
            elif result == "is_sick":
                self.audio.speak(self.game_state.get_text('training_sick_blocked'))
            else:
                self.audio.speak(self.game_state.get_text('training_error'))
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
        
        self.options.append({'text': self.game_state.get_text('office_upgrades_menu_title'), 'action': lambda: "office_upgrades_menu"})
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
        total_emails = len(self.game_state.emails)
        unread_emails = len([e for e in self.game_state.emails if not getattr(e, 'is_read', True)])
        super().__init__(self.game_state.get_text('email_inbox_status', total=total_emails, unread=unread_emails), [], audio, game_state)
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
            
            if getattr(email, 'is_salary_request', False):
                options = [
                    {'text': self.game_state.get_text('accept_raise', default="Gehaltserhöhung zustimmen"), 'action': self._accept_raise},
                    {'text': self.game_state.get_text('decline_raise', default="Ablehnen"), 'action': self._decline_raise}
                ]
            elif getattr(email, 'is_poach_offer', False):
                options = [
                    {'text': self.game_state.get_text('accept_counter_offer', default="Gegenangebot machen (Gehalt erhöhen)"), 'action': self._accept_counter_offer},
                    {'text': self.game_state.get_text('decline_poach', default="Angebot ignorieren"), 'action': self._delete}
                ]
            else:
                options = [
                    {'text': self.game_state.get_text('delete_email'), 'action': self._delete},
                    {'text': self.game_state.get_text('back'), 'action': lambda: "email_inbox"}
                ]
        else:
            title = self.game_state.get_text('email_title')
            self.email_body = ""
            options = [
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

    def _accept_raise(self):
        idx = getattr(self.game_state, 'selected_email_idx', 0)
        if 0 <= idx < len(self.game_state.emails):
            email = self.game_state.emails[idx]
            emp_idx = getattr(email, 'employee_idx', -1)
            if 0 <= emp_idx < len(self.game_state.employees):
                emp = self.game_state.employees[emp_idx]
                emp.salary = getattr(email, 'requested_salary', int(emp.salary * 1.25))
                emp.pending_raise_request = False
                emp.last_raise_week = self.game_state.week
                emp.morale = min(100, emp.morale + 50)
                self.audio.play_sound("buy")
                self.audio.speak(self.game_state.get_text('raise_accepted', default="Die Gehaltserhöhung wurde gewährt.", name=emp.name))
            self.game_state.emails.pop(idx)
        return "email_inbox"

    def _decline_raise(self):
        idx = getattr(self.game_state, 'selected_email_idx', 0)
        if 0 <= idx < len(self.game_state.emails):
            email = self.game_state.emails[idx]
            emp_idx = getattr(email, 'employee_idx', -1)
            if 0 <= emp_idx < len(self.game_state.employees):
                emp = self.game_state.employees[emp_idx]
                emp.pending_raise_request = False
                emp.morale = max(0, emp.morale - 50)  # Heftiger Dämpfer
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('raise_declined', default="Forderung abgelehnt. Die Moral ist gesunken.", name=emp.name))
            self.game_state.emails.pop(idx)
        return "email_inbox"

    def _accept_counter_offer(self):
        idx = getattr(self.game_state, 'selected_email_idx', 0)
        if 0 <= idx < len(self.game_state.emails):
            email = self.game_state.emails[idx]
            emp_idx = getattr(email, 'employee_idx', -1)
            if 0 <= emp_idx < len(self.game_state.employees):
                emp = self.game_state.employees[emp_idx]
                emp.salary = getattr(email, 'offered_salary', int(emp.salary * 1.5))
                emp.pending_poach_offer = False
                emp.morale = min(100, emp.morale + 30)
                self.audio.play_sound("buy")
                self.audio.speak(self.game_state.get_text('poach_counter_success', default="Gegenangebot angenommen! {name} bleibt im Studio.", name=emp.name))
            self.game_state.emails.pop(idx)
        return "email_inbox"

class OfficeUpgradeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('office_upgrades_menu_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        from game_data import OFFICE_UPGRADES
        self.options = []
        
        owned_upgrades = []
        for obj in getattr(self.game_state, 'office_objects', []):
            owned_upgrades.append(obj.get('bonus'))
            
        for upgrade in OFFICE_UPGRADES:
            if upgrade['bonus'] in owned_upgrades:
                txt = f"[X] {self.game_state.get_text(upgrade['name_key'])}"
                self.options.append({'text': txt, 'action': lambda: None})
            else:
                txt = f"[ ] {self.game_state.get_text(upgrade['name_key'])} ({upgrade['cost']} EUR)"
                self.options.append({'text': txt, 'action': lambda u=upgrade: self._buy_upgrade(u)})
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "office_menu"})

    def _buy_upgrade(self, upgrade):
        if self.game_state.money >= upgrade['cost']:
            self.game_state.money -= upgrade['cost']
            if not hasattr(self.game_state, 'office_objects'):
                self.game_state.office_objects = []
            self.game_state.office_objects.append({'bonus': upgrade['bonus']})
            self.audio.play_sound("buy")
            self.audio.speak(self.game_state.get_text('upgrade_bought', name=self.game_state.get_text(upgrade['name_key'])))
            self._update_options()
            return "office_upgrades_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

