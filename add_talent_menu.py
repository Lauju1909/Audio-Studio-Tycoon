
with open('menus/office.py', 'r', encoding='utf-8') as f:
    content = f.read()

talent_tree_code = """
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
"""

if "class TalentTreeMenu(Menu):" not in content:
    content += "\n" + talent_tree_code
    with open('menus/office.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added TalentTreeMenu to office.py")
else:
    print("TalentTreeMenu already in office.py")
