import random

class HRManager:
    def __init__(self, state):
        self.state = state

    def tick(self):
        self._process_stress_and_strikes()
        self._process_headhunting_event()
        self._process_strike_countdown()
        self._process_employees()
        self._process_poaching()

    def _process_stress_and_strikes(self):
        is_crunching_any = any(ap.get('crunch') for ap in self.state.active_projects)
        if is_crunching_any:
            self.state.stress_level = min(100.0, getattr(self.state, 'stress_level', 0.0) + 5.0)
        else:
            perk_relief = len(getattr(self.state, 'office_perks', [])) * 2.0
            self.state.stress_level = max(0.0, getattr(self.state, 'stress_level', 0.0) - (2.0 + perk_relief))

        avg_morale = sum(e.morale for e in self.state.employees) / len(self.state.employees) if self.state.employees else 100
        
        if len(self.state.employees) >= 5 and (getattr(self.state, 'stress_level', 0.0) > 60.0 or avg_morale < 50):
            if not getattr(self.state, 'has_union', False):
                if random.random() < 0.2 and getattr(self.state, 'pending_union_event', None) is None:
                    self.state.pending_union_event = {"type": "formation"}
            else:
                if random.random() < 0.15 and getattr(self.state, 'strike_weeks_left', 0) == 0 and getattr(self.state, 'pending_union_event', None) is None:
                    self.state.pending_union_event = {"type": "strike_threat"}

    def _process_headhunting_event(self):
        if not getattr(self.state, "pending_headhunt_event", None) and self.state.employees:
            for emp in self.state.employees:
                avg_skill = sum(emp.skills.values()) / len(emp.skills) if emp.skills else 0
                if avg_skill >= 80 and random.random() < 0.005:
                    rival_offer = int(emp.salary * random.uniform(1.2, 2.0))
                    self.state.pending_headhunt_event = {
                        "employee": emp,
                        "rival_offer": rival_offer
                    }
                    self.state.time_speed = 0
                    break

    def _process_strike_countdown(self):
        if getattr(self.state, 'strike_weeks_left', 0) > 0:
            strike_weekly_cost = len(self.state.employees) * 10000
            self.state.money -= strike_weekly_cost
            self.state.track_expense("other", strike_weekly_cost)
            self.state.strike_weeks_left -= 1
            if self.state.strike_weeks_left == 0:
                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("strike_ended", {}))

    def _process_employees(self):
        office_morale_bonus = 0
        for obj in getattr(self.state, 'office_objects', []):
            m_bonus = 0
            if hasattr(obj, 'get'):
                m_bonus = obj.get("morale_bonus", 0)
            elif isinstance(obj, dict):
                from game_data import BUILD_OBJECTS
                obj_type = obj.get("type", obj.get("object_type"))
                obj_def = BUILD_OBJECTS.get(obj_type)
                if obj_def:
                    m_bonus = obj_def.get("morale_bonus", 0)
            office_morale_bonus += m_bonus

        has_easygoing = any(getattr(e, "personality", None) == "easygoing" for e in self.state.employees)

        quitting_employees = []
        for i, emp in enumerate(self.state.employees):
            emp.weeks_employed += 1
            if not getattr(self.state, 'crunch_active', False):
                reg_bonus = 2 + office_morale_bonus
                if has_easygoing:
                    reg_bonus *= 1.10
                if getattr(emp, "personality", None) == "perfectionist":
                    reg_bonus *= 0.90
                emp.morale = min(100, emp.morale + max(1, int(reg_bonus)))

            if getattr(emp, 'is_training', False):
                emp.training_weeks_left -= 1
                if emp.training_weeks_left <= 0:
                    emp.is_training = False
                    boost = getattr(emp, 'training_skill_boost', 0)
                    if boost > 0:
                        emp.skills[emp.primary_skill] = min(100, emp.skills[emp.primary_skill] + boost)
                    emp.training_skill_boost = 0
                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("training_done", {"emp": emp}))
                continue

            is_emp_crunching = False
            for ap in self.state.active_projects:
                if ap.get("crunch") and emp in self.state._active_employees(ap["project"]):
                    is_emp_crunching = True
                    break
                    
            if is_emp_crunching:
                emp.crunch_weeks = getattr(emp, "crunch_weeks", 0) + 1
            else:
                emp.crunch_weeks = max(0, getattr(emp, "crunch_weeks", 0) - 1)

            if getattr(emp, 'vacation_weeks_left', 0) > 0:
                emp.vacation_weeks_left -= 1
                emp.fatigue = max(0, getattr(emp, 'fatigue', 0) - 20)
                emp.morale = min(100, emp.morale + 10)
                continue

            is_working = self.state.is_developing or getattr(self.state, 'active_custom_console', None) or len(getattr(self.state, 'active_ports', [])) > 0 or len(getattr(self.state, 'active_contract_works', [])) > 0
            if is_working and not emp.is_training and not getattr(emp, 'is_sick', False):
                emp.fatigue = getattr(emp, 'fatigue', 0) + random.randint(1, 3)
                if is_emp_crunching:
                    emp.fatigue += 5
            else:
                emp.fatigue = max(0, getattr(emp, 'fatigue', 0) - 2)

            if getattr(emp, 'fatigue', 0) >= 100 and not getattr(emp, 'is_sick', False):
                emp.fatigue = 0
                emp.is_sick = True
                emp.sick_weeks_left = random.randint(3, 6)
                emp.morale = max(0, emp.morale - 30)
                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("burnout", {"emp": emp}))
                continue

            if getattr(emp, 'is_sick', False):
                emp.sick_weeks_left -= 1
                if emp.sick_weeks_left <= 0:
                    emp.is_sick = False
                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("sick_recovered", {"emp": emp}))
                continue
                
            if not emp.is_sick and not emp.is_training:
                sick_chance = 0.01
                if emp.morale < 30:
                    sick_chance = 0.08
                elif emp.morale < 60:
                    sick_chance = 0.03
                    
                if getattr(emp, "crunch_weeks", 0) > 4:
                    sick_chance += 0.10 * (emp.crunch_weeks - 4)
                    
                perks = getattr(self.state, "office_perks", [])
                if "hr_department" in perks: sick_chance -= 0.05
                if "wellness_benefits" in perks: sick_chance -= 0.05
                if "therapist" in perks: sick_chance -= 0.08
                
                sick_chance = max(0.01, sick_chance)

                if random.random() < sick_chance:
                    emp.is_sick = True
                    emp.sick_weeks_left = random.randint(1, 3)
                    if getattr(emp, "crunch_weeks", 0) > 4:
                        emp.sick_weeks_left += 2
                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("sick", {"emp": emp}))
                    continue

                quit_chance = 0.0
                if emp.morale == 0: quit_chance += 0.05
                if getattr(emp, "crunch_weeks", 0) > 8: quit_chance += 0.15
                
                if "hr_department" in perks: quit_chance -= 0.05
                if "therapist" in perks: quit_chance -= 0.10
                
                if quit_chance > 0 and random.random() < quit_chance:
                    quitting_employees.append(emp)
                    if getattr(emp, "crunch_weeks", 0) > 8:
                        from notifications import dispatcher, Event
                        dispatcher.dispatch(Event("burnout_quit", {"emp": emp}))
                    continue

            if not getattr(emp, 'pending_raise_request', False) and (self.state.week - getattr(emp, 'last_raise_week', 0)) > 20:
                expected_salary = sum(emp.skills.values()) * 5 + 500
                if expected_salary > emp.salary * 1.3 and random.random() < 0.1:
                    emp.pending_raise_request = True
                    new_salary = int(emp.salary * 1.25)
                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("salary_raise_request", {"emp_idx": i, "emp": emp, "new_salary": new_salary}))
                    
        for e in quitting_employees:
            if e in self.state.employees:
                self.state.employees.remove(e)
                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("employee_quit", {"emp": e}))

    def _process_poaching(self):
        if self.state.week % 8 == 0 and getattr(self.state, 'employees', []) and getattr(self.state, 'rivals', []):
            rival = random.choice(self.state.rivals)
            
            security_bonus = 1.0
            legal_bonus = 1.0
            has_legal = False
            for obj in getattr(self.state, 'office_objects', []):
                if obj.get('bonus') == 'security':
                    security_bonus = 0.5
                if obj.get('bonus') == 'legal_protection':
                    legal_bonus = 0.7
                    has_legal = True
            
            diff_multi = {0: 0.2, 1: 0.5, 2: 1.0, 3: 1.8}.get(getattr(self.state, 'difficulty', 1), 1.0)
            chance = 0.06 * diff_multi * security_bonus * legal_bonus
            
            if getattr(rival, 'ai_personality', '') == "Aggressive": chance *= 1.5
            
            if random.random() < chance:
                target_emp = random.choice(self.state.employees)
                
                if has_legal and getattr(target_emp, 'level', 1) >= 8:
                    pass
                elif not getattr(target_emp, 'pending_poach_offer', False):
                    target_emp.pending_poach_offer = True
                    offer_salary = int(target_emp.salary * 1.5)
                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("poach_offer", {"emp_idx": self.state.employees.index(target_emp), "emp": target_emp, "rival_name": rival.name, "offer_salary": offer_salary}))

        for emp in list(self.state.employees):
            if getattr(emp, 'pending_poach_offer', False):
                if random.random() < 0.3:
                    if emp in self.state.employees:
                        self.state.employees.remove(emp)
                        from notifications import dispatcher, Event
                        dispatcher.dispatch(Event("employee_left_poach", {"emp": emp}))
                        if hasattr(self.state, 'audio'):
                            self.state.audio.speak(self.state.get_text('employee_left_poach', name=emp.name))
