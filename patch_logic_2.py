import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# GameState.__init__
init_code = '''
        self.sound_card_projects = []
'''
new_init_code = init_code + '''
        self.custom_consoles = []
        self.active_custom_console = None
'''
content = content.replace(init_code, new_init_code)

# to_dict
to_dict_code = '''
            "sound_card_projects": [p.to_dict() for p in getattr(self, "sound_card_projects", [])],
'''
new_to_dict_code = to_dict_code + '''
            "custom_consoles": [c.to_dict() for c in getattr(self, "custom_consoles", [])],
            "active_custom_console": getattr(self, "active_custom_console").to_dict() if getattr(self, "active_custom_console", None) else None,
'''
content = content.replace(to_dict_code, new_to_dict_code)

# from_dict
from_dict_code = '''
        self.sound_card_projects = []
        for pd in data.get("sound_card_projects", []):
            self.sound_card_projects.append(SoundCardProject.from_dict(pd))
'''
new_from_dict_code = from_dict_code + '''
        from models import CustomConsoleProject
        self.custom_consoles = []
        for c in data.get("custom_consoles", []):
            self.custom_consoles.append(CustomConsoleProject.from_dict(c))
        if data.get("active_custom_console"):
            self.active_custom_console = CustomConsoleProject.from_dict(data["active_custom_console"])
'''
content = content.replace(from_dict_code, new_from_dict_code)

# hardware logic inside _on_new_week
hardware_code = '''
        self.update_hardware_development()
'''
new_hardware_code = hardware_code + '''
        # Eigene Konsolen
        if getattr(self, "active_custom_console", None):
            cc = self.active_custom_console
            if not getattr(cc, "is_released", False):
                progress_gain = 0
                for emp in self.employees:
                    if not emp.is_training and not emp.is_sick and emp.morale > 0:
                        progress_gain += emp.skills.get("Programmierung", 50) / 100.0
                
                total_weeks = getattr(cc, "total_weeks", 50)
                weekly_progress = (progress_gain / total_weeks) * 0.5
                cc.progress += weekly_progress
                if cc.progress >= 1.0:
                    cc.progress = 1.0
                    cc.is_released = True
                    cc.weeks_on_market = 0
                    if hasattr(self.audio, "play_sound"):
                        self.audio.play_sound("success")
                    if hasattr(self.audio, "speak"):
                        self.audio.speak(self.get_text('console_finished', name=cc.name))
                    
                    from game_data import PLATFORMS
                    PLATFORMS.append({
                        "name": cc.name,
                        "license_fee": 0,
                        "market_multi": 1.0 + (cc.tech_level / 100.0),
                        "unlock_year": self.get_calendar_year(),
                        "end_year": self.get_calendar_year() + 10,
                        "type": "Konsole"
                    })
            else:
                cc.weeks_on_market += 1
                base_sales = int(cc.tech_level * 500 * (1.0 + (self.fans / 10000.0)))
                decay = max(0.1, 1.0 - (cc.weeks_on_market / 100.0))
                weekly_sales = int(base_sales * decay)
                cc.units_sold += weekly_sales
                
                revenue = weekly_sales * cc.price
                cc.revenue += revenue
                self.money += revenue
                if revenue > 0:
                    self.track_income("hardware", revenue)
                
                cc.active_users += weekly_sales
                if cc.active_users > 0:
                    cc.active_users = int(cc.active_users * 0.99)
'''
content = content.replace(hardware_code, new_hardware_code)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched logic.py properly")
