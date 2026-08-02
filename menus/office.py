from .base import Menu
from game_data import TRAINING_OPTIONS, OFFICE_LEVELS, OFFICE_UPGRADES

class HRMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hr_menu')
        options = [
            {'text': self.game_state.get_text('hire_employee'), 'action': lambda: "hire_menu"},
            {'text': self.game_state.get_text('menu_employee_overview'), 'action': lambda: "employee_overview_menu"},
            {'text': self.game_state.get_text('fire_employee'), 'action': lambda: "fire_menu"},
            {'text': self.game_state.get_text('training_employee'), 'action': lambda: "training_employee_select"},
            {'text': self.game_state.get_text('menu_teambuilding'), 'action': lambda: "teambuilding_menu"},
            {'text': self.game_state.get_text('office_perks_menu'), 'action': lambda: "office_perks_menu"},
            {'text': "Mitarbeiter-Talentbäume (Skill Tree)", 'action': lambda: "talent_tree_menu"},
            {'text': self.game_state.get_text('union_menu'), 'action': lambda: "union_menu"},
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
        
        # Generiere 3 zufällige Kandidaten mit echten Namen
        candidates = []
        for _ in range(3):
            role = random.choice(EMPLOYEE_ROLES)
            # Übergebe None, damit Employee.__init__ einen echten Namen aus game_data wählt
            candidates.append(Employee(name=None, role_data=role))
            
        self.options = []
        for c in candidates:
             # Rolle lokalisieren
             role_name = self.game_state.get_text(c.role)
             txt = f"{c.name} ({role_name}, {self.game_state.get_text('salary_suffix', salary=c.salary)})"
             self.options.append({'text': txt, 'action': lambda emp=c: self._hire(emp)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _hire(self, emp):
        cost = emp.salary * 2
        if self.game_state.hire_employee(emp):
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('hire_success', name=emp.name, cost=cost, money=self.game_state.money))
            return "hr_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('hire_full' if len(self.game_state.employees) >= self.game_state.get_max_employees() else 'insufficient_funds'))
            return None

class FireMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('fire_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for i, emp in enumerate(self.game_state.employees):
            if getattr(emp, 'is_ceo', False):
                continue
            role_name = self.game_state.get_text(emp.role)
            self.options.append({'text': f"{emp.name} ({role_name})", 'action': lambda idx=i: self._fire(idx)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _fire(self, idx):
        if 0 <= idx < len(self.game_state.employees):
            emp = self.game_state.employees[idx]
            name = emp.name
            if self.game_state.fire_employee(idx):
                self.audio.play_sound("confirm")
                self.audio.speak(self.game_state.get_text('fire_success', name=name, money=self.game_state.money))
        return "hr_menu"

class EmployeeOverviewMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_employee_overview'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for emp in self.game_state.employees:
            role_name = self.game_state.get_text(emp.role)
            status = ""
            if getattr(emp, 'is_training', False):
                status = self.game_state.get_text('training_status_tag', weeks=emp.training_weeks_left)
            elif getattr(emp, 'is_sick', False):
                status = self.game_state.get_text('sick_status_tag', weeks=emp.sick_weeks_left)
            else:
                status = "OK"

            txt = self.game_state.get_text('employee_detail_summary',
                                          name=emp.name,
                                          role=role_name,
                                          level=emp.skill_level,
                                          salary=emp.salary,
                                          morale=int(emp.morale),
                                          status=status)
            self.options.append({'text': txt, 'action': None})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

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
            role_name = self.game_state.get_text(emp.role)
            if getattr(emp, 'is_training', False):
                weeks_left = getattr(emp, 'training_weeks_left', 0)
                status = self.game_state.get_text('training_status_tag', weeks=weeks_left)
                txt = f"[T] {emp.name} ({role_name}) — {status}"
            elif getattr(emp, 'is_sick', False):
                weeks_left = getattr(emp, 'sick_weeks_left', 0)
                status = self.game_state.get_text('sick_status_tag', weeks=weeks_left)
                txt = f"[K] {emp.name} ({role_name}) — {status}"
            else:
                txt = f"{emp.name} ({role_name})"
            self.options.append({'text': txt, 'action': lambda idx=i: self._select(idx)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _select(self, idx):
        emp = self.game_state.employees[idx]
        if getattr(emp, 'is_training', False):
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('training_already_in', name=emp.name))
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
        emp.name if emp else "?"

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
                self.audio.speak(self.game_state.get_text('training_already_in', name=emp.name))
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
            
        qa_lvl = getattr(self.game_state, 'qa_level', 0)
        self.options.append({'text': self.game_state.get_text('upgrade_qa_lab', level=qa_lvl, cost=50000), 'action': self._upgrade_qa_lab})
        
        sup_lvl = getattr(self.game_state, 'support_level', 0)
        self.options.append({'text': self.game_state.get_text('upgrade_support', level=sup_lvl, cost=25000), 'action': self._upgrade_support})
        
        cap = getattr(self.game_state, 'server_capacity', 0)
        self.options.append({'text': self.game_state.get_text('buy_servers', capacity=cap, cost=10000), 'action': self._buy_servers})
        
        self.options.append({'text': self.game_state.get_text('hr_menu'), 'action': lambda: "hr_menu"})
        self.options.append({'text': self.game_state.get_text('office_upgrades_menu_title'), 'action': lambda: "office_upgrades_menu"})
        
        if self.game_state.is_feature_unlocked("darknet"):
            self.options.append({'text': self.game_state.get_text('menu_darknet_title', default="Darknet Terminal"), 'action': lambda: "darknet_menu"})
        else:
            from game_data import FEATURE_UNLOCKS
            if "darknet" in FEATURE_UNLOCKS:
                self.options.append({'text': f"{self.game_state.get_text('menu_darknet_title', default='Darknet Terminal')} (Ab {FEATURE_UNLOCKS['darknet'].get('year', '???')})", 'action': lambda: None})
        self.options.append({'text': self.game_state.get_text('menu_build_office'), 'action': lambda: "build_menu"})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _upgrade(self):
        if self.game_state.office_level >= len(OFFICE_LEVELS) - 1:
            self.audio.speak(self.game_state.get_text('office_max_level'))
            return None
        next_office = OFFICE_LEVELS[self.game_state.office_level + 1]
        if self.game_state.money >= next_office['cost']:
            self.game_state.track_expense("office", next_office['cost'])
            self.game_state.office_level += 1
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('office_upgrade_success', name=next_office['name'], max_emp=self.game_state.get_max_employees()))
            self._update_options()
            return "office_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

    def _upgrade_qa_lab(self):
        cost = 50000
        if self.game_state.money >= cost:
            self.game_state.track_expense("office", cost)
            self.game_state.qa_level = getattr(self.game_state, 'qa_level', 0) + 1
            self.audio.play_sound("buy")
            self.audio.speak(self.game_state.get_text('qa_lab_upgraded', level=self.game_state.qa_level))
            self._update_options()
            return "office_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

    def _upgrade_support(self):
        cost = 25000
        if self.game_state.money >= cost:
            self.game_state.track_expense("office", cost)
            self.game_state.support_level = getattr(self.game_state, 'support_level', 0) + 1
            self.audio.play_sound("buy")
            self.audio.speak(self.game_state.get_text('support_upgraded', level=self.game_state.support_level))
            self._update_options()
            return "office_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

    def _buy_servers(self):
        cost = 10000
        if self.game_state.money >= cost:
            self.game_state.track_expense("office", cost)
            self.game_state.server_capacity = getattr(self.game_state, 'server_capacity', 0) + 50000
            self.audio.play_sound("buy")
            self.audio.speak(self.game_state.get_text('servers_bought', capacity=self.game_state.server_capacity))
            self._update_options()
            return "office_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

class EmailInboxMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.filter_type = 'all'
        super().__init__("Posteingang", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        total_emails = len(self.game_state.emails)
        unread_emails = len([e for e in self.game_state.emails if not getattr(e, 'is_read', True)])
        self.title = self.game_state.get_text('email_inbox_status', total=total_emails, unread=unread_emails)
        
        self.options = []
        filter_names = {'all': "Alle", 'hr': "Personal", 'bugs': "Bugs", 'other': "Sonstige"}
        self.options.append({'text': f"Filter: {filter_names[self.filter_type]}", 'action': self._toggle_filter})
        
        for i, email in enumerate(self.game_state.emails):
            is_hr = getattr(email, 'is_salary_request', False) or getattr(email, 'is_poach_offer', False)
            is_bug = getattr(email, 'is_bug', False)
            is_other = not is_hr and not is_bug
            
            if self.filter_type == 'hr' and not is_hr: continue
            if self.filter_type == 'bugs' and not is_bug: continue
            if self.filter_type == 'other' and not is_other: continue
            
            status = self.game_state.get_text('new_label') + " " if not getattr(email, 'is_read', True) else ""
            txt = f"{status}{email.sender}: {email.subject}"
            self.options.append({'text': txt, 'action': lambda idx=i: self._read(idx), 'email_idx': i})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"} )

    def _toggle_filter(self):
        types = ['all', 'hr', 'bugs', 'other']
        idx = types.index(self.filter_type)
        self.filter_type = types[(idx + 1) % len(types)]
        self._update_options()
        self.current_index = 0
        self.speak_current(interrupt=True)
        return None

    def handle_input(self, event):
        import pygame
        if event.key == pygame.K_DELETE:
            if self.options and self.current_index < len(self.options):
                opt = self.options[self.current_index]
                if 'email_idx' in opt:
                    real_idx = opt['email_idx']
                    if 0 <= real_idx < len(self.game_state.emails):
                        self.game_state.emails.pop(real_idx)
                        self.audio.play_sound("confirm")
                        self.audio.speak(self.game_state.get_text('email_deleted', default="E-Mail gelöscht"))
                        self._update_options()
                        if self.current_index >= len(self.options):
                            self.current_index = max(0, len(self.options) - 1)
                        self.speak_current(interrupt=True)
                        return None
        return super().handle_input(event)

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
                    {'text': self.game_state.get_text('accept_counter_offer'), 'action': self._accept_counter_offer},
                    {'text': self.game_state.get_text('decline_poach'), 'action': self._delete}
                ]
            elif getattr(email, 'is_expo_invite', False):
                options = [
                    {'text': self.game_state.get_text('attend_expo', default="Messe besuchen (Menü öffnen)"), 'action': lambda: "expo_menu"},
                    {'text': self.game_state.get_text('delete_email'), 'action': self._delete},
                    {'text': self.game_state.get_text('back'), 'action': lambda: "email_inbox"}
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
        self.current_index = 0
        self.audio.speak(self.title)
        if hasattr(self, 'email_body') and self.email_body:
            self.audio.speak(self.email_body, interrupt=False)
        if self.options:
            self.speak_current(interrupt=False)

    def handle_input(self, event):
        import pygame
        if event.key == pygame.K_DELETE:
            return self._delete()
        return super().handle_input(event)

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
                self.audio.speak(self.game_state.get_text('raise_accepted', name=emp.name))
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
                self.audio.speak(self.game_state.get_text('raise_declined', name=emp.name))
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
                self.audio.speak(self.game_state.get_text('poach_counter_success', name=emp.name))
            self.game_state.emails.pop(idx)
        return "email_inbox"

class OfficeUpgradeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('office_upgrades_menu_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
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
            self.game_state.track_expense("office", upgrade['cost'])
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



class OfficePerksMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('office_perks_menu'), [], audio, game_state)
        if not hasattr(self.game_state, 'office_perks'):
            self.game_state.office_perks = []
        self._update_options()
        
    def _update_options(self):
        self.options = []
        for perk in ["fruit_basket", "kicker_table", "company_car", "wellness_benefits", "therapist", "hr_department"]:
            active = perk in getattr(self.game_state, "office_perks", [])
            status = self.game_state.get_text('active') if active else self.game_state.get_text('inactive')
            text = f"{self.game_state.get_text('perk_'+perk)} [{status}]"
            self.options.append({'text': text, 'action': lambda p=perk: self.toggle_perk(p)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def toggle_perk(self, perk):
        if not hasattr(self.game_state, "office_perks"):
            self.game_state.office_perks = []
        if perk in self.game_state.office_perks:
            self.game_state.office_perks.remove(perk)
            self.audio.play_sound('click')
        else:
            cost = 2000 if perk == "fruit_basket" else (5000 if perk == "kicker_table" else 20000)
            if self.game_state.money >= cost:
                self.game_state.money -= cost
                self.game_state.track_expense("other", cost)
                self.game_state.office_perks.append(perk)
                self.audio.play_sound('cash')
            else:
                self.audio.play_sound('error')
        self._update_options()
        return "stay"

class HeadhuntingEventMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('headhunting_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        event = getattr(self.game_state, "pending_headhunt_event", None)
        if not event:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
            return
            
        emp = event["employee"]
        offer = event["rival_offer"]
        
        self.title = self.game_state.get_text('headhunting_desc', name=emp.name, offer=offer)
        
        self.options.append({
            'text': self.game_state.get_text('match_offer', offer=offer),
            'action': lambda: self.match_offer()
        })
        self.options.append({
            'text': self.game_state.get_text('let_them_go'),
            'action': lambda: self.let_go()
        })
        
    def match_offer(self):
        event = getattr(self.game_state, "pending_headhunt_event", None)
        if event:
            emp = event["employee"]
            emp.salary = event["rival_offer"]
            self.audio.play_sound('success')
            self.game_state.pending_headhunt_event = None
        return "game_menu"
        
    def let_go(self):
        event = getattr(self.game_state, "pending_headhunt_event", None)
        if event:
            emp = event["employee"]
            if emp in self.game_state.employees:
                self.game_state.employees.remove(emp)
                for ap in self.game_state.active_projects:
                    proj = ap["project"]
                    if getattr(proj, "team", None) and emp in proj.team:
                        proj.team.remove(emp)
            self.audio.play_sound('error')
            self.game_state.pending_headhunt_event = None
        return "game_menu"


class TalentTreeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Mitarbeiter-Talentbäume", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options.clear()
        
        has_employees = False
        for i, emp in enumerate(self.game_state.employees):
            has_employees = True
            tp = getattr(emp, "talent_points", 0)
            status = f" ({tp} Punkte)" if tp > 0 else ""
            self.options.append({
                'text': f"{emp.name} - Level {emp.skill_level}{status}",
                'action': lambda idx=i: self._select_employee(idx)
            })
            
        if not has_employees:
            self.options.append({'text': "Keine Mitarbeiter vorhanden.", 'action': lambda: None})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def _select_employee(self, idx):
        self.game_state.selected_talent_emp_idx = idx
        return "employee_talent_menu"

class EmployeeTalentMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        idx = getattr(self.game_state, "selected_talent_emp_idx", -1)
        if idx >= 0 and idx < len(self.game_state.employees):
            emp = self.game_state.employees[idx]
            tp = getattr(emp, "talent_points", 0)
            title = f"Talente: {emp.name} (Punkte: {tp})"
        else:
            title = "Mitarbeiter Talente"
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options.clear()
        idx = getattr(self.game_state, "selected_talent_emp_idx", -1)
        if idx < 0 or idx >= len(self.game_state.employees):
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "talent_tree_menu"})
            return
            
        emp = self.game_state.employees[idx]
        tp = getattr(emp, "talent_points", 0)
        talents = getattr(emp, "talents", [])
        
        # Available Talents
        talent_paths = [
            ("Audio-Gott", "Erhöht die Qualität von Sound-Features bei jedem Projekt."),
            ("Agile Coach", "Erhöht die Entwicklungsgeschwindigkeit des gesamten Teams."),
            ("Crunch-Survivor", "Mitarbeiter verliert nie mehr Moral und ermüdet nicht."),
            ("Marketing-Guru", "Jedes Projekt bekommt einen passiven Hype-Boost.")
        ]
        
        for name, desc in talent_paths:
            if name in talents:
                self.options.append({
                    'text': f"[GELERNT] {name} - {desc}",
                    'action': lambda: None
                })
            else:
                if tp > 0:
                    self.options.append({
                        'text': f"[LERNEN] {name} - {desc} (Kosten: 1 Punkt)",
                        'action': lambda n=name: self._learn_talent(emp, n)
                    })
                else:
                    self.options.append({
                        'text': f"[GESPERRT] {name} - {desc} (Nicht genug Punkte)",
                        'action': lambda: None
                    })
                    
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "talent_tree_menu"})

    def _learn_talent(self, emp, talent_name):
        tp = getattr(emp, "talent_points", 0)
        if tp > 0:
            emp.talent_points -= 1
            if not hasattr(emp, "talents"):
                emp.talents = []
            emp.talents.append(talent_name)
            self.audio.play_sound("success")
            self.audio.speak(f"{emp.name} hat das Talent {talent_name} gelernt!")
            
            # Re-init menu to update title and points
            self.title = f"Talente: {emp.name} (Punkte: {emp.talent_points})"
            self._update_options()
        return None
