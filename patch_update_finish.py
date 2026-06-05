import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_finish = '''            if ap["progress"] >= ap["total_weeks"]:
                ap["ready_to_finish"] = True
                if proj.__class__.__name__ == "EngineProject":
                    self.finalize_engine(ap)
                    continue'''

new_finish = '''            if ap["progress"] >= ap["total_weeks"]:
                ap["ready_to_finish"] = True
                if proj.__class__.__name__ == "EngineProject":
                    self.finalize_engine(ap)
                    continue
                elif proj.__class__.__name__ in ["UpdateProject", "DLCProject"]:
                    self._finish_update_project(proj)
                    if ap in self.active_projects:
                        self.active_projects.remove(ap)
                    continue'''

content = content.replace(old_finish, new_finish)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched finish logic for updates/DLCs")
