
with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_code = """
        # --- NEW: Mitarbeiter-Wochenupdate & Headhunting ---
        for emp in self.employees:
            emp.weeks_employed = getattr(emp, "weeks_employed", 0) + 1
            
            # Alle 48 Wochen (1 Jahr) einen Talent-Punkt geben, wenn Level > 1
            if emp.weeks_employed % 48 == 0 and emp.skill_level > 1:
                emp.talent_points = getattr(emp, "talent_points", 0) + 1

            # Headhunting Event (Zufall, ca. 1x pro 2-3 Jahre pro Studio wenn gute Leute da sind)
            if getattr(self, "pending_headhunt_event", None) is None:
                if emp.skill_level >= 3 and not emp.is_ceo:
                    import random
                    if random.random() < 0.005:  # 0.5% chance per week per senior employee
                        rival_offer = int(emp.salary * random.uniform(1.3, 2.0))
                        self.pending_headhunt_event = {
                            "employee": emp,
                            "rival_offer": rival_offer
                        }
                        if hasattr(self.audio, "play_sound"):
                            self.audio.play_sound("error")
                        if hasattr(self.audio, "speak"):
                            self.audio.speak(f"Achtung! Ein Rivale versucht {emp.name} abzuwerben!")
"""

if "emp.weeks_employed = getattr(emp, \"weeks_employed\", 0) + 1" not in content:
    # Insert at the beginning of _on_new_week
    target = "def _on_new_week(self):"
    content = content.replace(target, target + new_code)
    with open('logic.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched logic.py with employee weekly update & headhunting")
else:
    print("Already patched logic.py")
