
with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agile Coach (Dev Speed)
# in _on_new_week, where progress is added (approx line 1315-1317)
# But wait, there are multiple dev loops. I can patch `points_added += emp.skills.get(skill_name, 50) / 10.0`
# or we just add a multiplier if ANY employee has "Agile Coach".
# Let's search for "points_added += emp.skills.get(skill_name, 50) / 10.0" and replace it.

if "points_added += emp.skills.get(skill_name, 50) / 10.0" in content:
    content = content.replace("points_added += emp.skills.get(skill_name, 50) / 10.0", 
        "base_points = emp.skills.get(skill_name, 50) / 10.0\n                        "
        "if 'Agile Coach' in getattr(emp, 'talents', []):\n                            base_points *= 1.2\n                        "
        "points_added += base_points")

# 2. Audio-Gott
# Let's add a bonus to review scores if team has "Audio-Gott". (Around line 3350 or where ReviewScore is generated).
# Review is generated around `review_min = max(1, quality // 10)`. Let's just find `ReviewScore(`
# Wait, `quality` is calculated around line 3317: `quality = max(10, min(100, int((p_score / p_score_target) * 100)))`
# I can patch `if "Audio-Gott" in [t for e in self.employees for t in getattr(e, "talents", [])]: quality += 5`
if "quality = max(10, min(100, int((p_score / p_score_target) * 100)))" in content:
    content = content.replace("quality = max(10, min(100, int((p_score / p_score_target) * 100)))",
        "quality = max(10, min(100, int((p_score / p_score_target) * 100)))\n        if any('Audio-Gott' in getattr(e, 'talents', []) for e in self.employees):\n            quality = min(100, quality + 5)")

# 3. Marketing-Guru
# Passive Hype generation in _on_new_week.
# Let's insert it before "if getattr(self, "pending_headhunt_event", None) is None:"
target = 'if getattr(self, "pending_headhunt_event", None) is None:'
replacement = """if 'Marketing-Guru' in getattr(emp, 'talents', []):
                self.hype = min(100.0, self.hype + 0.1)
            
            if getattr(self, "pending_headhunt_event", None) is None:"""
if target in content:
    content = content.replace(target, replacement)

# 4. Crunch-Survivor (Morale never drops)
# We can just prevent morale dropping below 100 for them.
# Let's patch _on_new_week where morale is modified.
target_morale = 'emp.morale = max(0, emp.morale - morale_loss)'
replacement_morale = """if 'Crunch-Survivor' in getattr(emp, 'talents', []):
                                emp.morale = 100
                            else:
                                emp.morale = max(0, emp.morale - morale_loss)"""
if target_morale in content:
    content = content.replace(target_morale, replacement_morale)
    
target_morale2 = 'emp.morale = max(0, emp.morale - 1)'
replacement_morale2 = """if 'Crunch-Survivor' in getattr(emp, 'talents', []):
                        emp.morale = 100
                    else:
                        emp.morale = max(0, emp.morale - 1)"""
if target_morale2 in content:
    content = content.replace(target_morale2, replacement_morale2)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched logic.py for talent effects")
