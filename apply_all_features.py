import os
import re

def update_models():
    with open("models.py", "r", encoding="utf-8") as f:
        content = f.read()

    if "drm_level" not in content:
        content = content.replace('self.is_remake = False', 'self.is_remake = False\n        self.drm_level = 0\n        self.pirated_copies = 0')
        content = content.replace('"is_remake": getattr(self, "is_remake", False),', '"is_remake": getattr(self, "is_remake", False),\n            "drm_level": getattr(self, "drm_level", 0),\n            "pirated_copies": getattr(self, "pirated_copies", 0),')
        content = content.replace('proj.is_remake = gd.get("is_remake", False)', 'proj.is_remake = gd.get("is_remake", False)\n        proj.drm_level = gd.get("drm_level", 0)\n        proj.pirated_copies = gd.get("pirated_copies", 0)')

    if "is_crunching" not in content:
        content = content.replace('self.is_sick = False', 'self.is_sick = False\n        self.is_crunching = False\n        self.crunch_weeks = 0')
        content = content.replace('"is_sick": getattr(self, "is_sick", False),', '"is_sick": getattr(self, "is_sick", False),\n            "is_crunching": getattr(self, "is_crunching", False),\n            "crunch_weeks": getattr(self, "crunch_weeks", 0),')
        content = content.replace('emp.is_sick = ed.get("is_sick", False)', 'emp.is_sick = ed.get("is_sick", False)\n        emp.is_crunching = ed.get("is_crunching", False)\n        emp.crunch_weeks = ed.get("crunch_weeks", 0)')

    with open("models.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated models.py")

def update_logic():
    with open("logic.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    if "is_public_company" not in content:
        content = content.replace('self.is_bankrupt = False', 'self.is_bankrupt = False\n        self.is_public_company = False\n        self.shareholder_target = 0\n        self.share_value = 100')
        content = content.replace('"is_bankrupt": getattr(self, "is_bankrupt", False),', '"is_bankrupt": getattr(self, "is_bankrupt", False),\n            "is_public_company": getattr(self, "is_public_company", False),\n            "shareholder_target": getattr(self, "shareholder_target", 0),\n            "share_value": getattr(self, "share_value", 100),')
        content = content.replace('state.is_bankrupt = saved_data.get("is_bankrupt", False)', 'state.is_bankrupt = saved_data.get("is_bankrupt", False)\n        state.is_public_company = saved_data.get("is_public_company", False)\n        state.shareholder_target = saved_data.get("shareholder_target", 0)\n        state.share_value = saved_data.get("share_value", 100)')
    
    if "crunch" not in content:
        # Inject crunch logic into get_team_speed_modifier and _on_new_week
        # Speed modifier
        speed_mod_injection = """
        for emp in self.employees:
            if getattr(emp, 'is_crunching', False):
                base += 0.5
"""
        content = content.replace('base = 1.0', 'base = 1.0' + speed_mod_injection)
        
        # New week crunch effects
        new_week_injection = """
        for emp in self.employees:
            if getattr(emp, 'is_crunching', False):
                emp.crunch_weeks += 1
                emp.morale -= max(1, emp.crunch_weeks * 2)
                import random
                if random.randint(1, 100) < emp.crunch_weeks * 5:
                    emp.is_sick = True
                    emp.sick_weeks_left = random.randint(1, 3)
                    emp.is_crunching = False
                    emp.crunch_weeks = 0
            else:
                emp.crunch_weeks = max(0, emp.crunch_weeks - 1)
"""
        content = content.replace('def _on_new_week(self):', 'def _on_new_week(self):\n' + new_week_injection)

    if "_check_shareholder_meeting" not in content:
        meeting_logic = """
    def _check_shareholder_meeting(self):
        year = self.get_calendar_year()
        if not hasattr(self, 'last_shareholder_year'):
            self.last_shareholder_year = year - 1
        if self.is_public_company and year > self.last_shareholder_year:
            self.last_shareholder_year = year
            if self.money < self.shareholder_target:
                self.share_value = max(10, self.share_value - 20)
            else:
                self.share_value += 10
            self.shareholder_target = self.money + 50000
            self.pending_shareholder_meeting = True
"""
        content = content.replace('def _check_goty(self):', meeting_logic + '\n    def _check_goty(self):')
        content = content.replace('self._check_goty()', 'self._check_goty()\n        self._check_shareholder_meeting()')

    with open("logic.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated logic.py")

def update_menus():
    # gameplay.py has GOTYMenu, we can add ShareholderMenu, DRM options, Crunch toggle
    with open("menus/gameplay.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    if "ShareholderMenu" not in content:
        menu_inj = """
class ShareholderMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__("Shareholder Meeting", [
            {'text': "Acknowledge", 'action': lambda: "game_menu"}
        ], audio, game_state)
        game_state.pending_shareholder_meeting = False
        target_met = game_state.money >= getattr(game_state, 'shareholder_target', 0)
        self.audio.speak(f"Shareholder Meeting! Target met: {target_met}. Share value is now {game_state.share_value}.", interrupt=True)
"""
        content += menu_inj
        
        # Add to state machine or handle pending
        # in MainGameMenu update()
        main_menu_update = """
        if getattr(self.game_state, "pending_shareholder_meeting", False):
            return "shareholder_meeting"
"""
        content = content.replace('if getattr(self.game_state, "pending_goty_results", None):', main_menu_update + '        if getattr(self.game_state, "pending_goty_results", None):')
        
    with open("menus/gameplay.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated menus/gameplay.py")

def update_translations():
    with open("translations.py", "r", encoding="utf-8") as f:
        content = f.read()
    if "drm_none" not in content:
        # just append a few to TRANSLATIONS dictionary
        # we will use regex to find the end of TRANSLATIONS
        content = content.replace('"easygoing": "Entspannt",', '"easygoing": "Entspannt",\n    "drm_none": "Kein DRM",\n    "drm_standard": "Standard DRM",\n    "drm_aggressive": "Aggressives DRM",\n    "crunch_enable": "Crunch aktivieren",\n    "crunch_disable": "Crunch beenden",\n    "shareholder_meeting": "Aktionärsversammlung",')
        content = content.replace('"easygoing": "Easygoing",', '"easygoing": "Easygoing",\n    "drm_none": "No DRM",\n    "drm_standard": "Standard DRM",\n    "drm_aggressive": "Aggressive DRM",\n    "crunch_enable": "Enable Crunch",\n    "crunch_disable": "Disable Crunch",\n    "shareholder_meeting": "Shareholder Meeting",')
    with open("translations.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated translations.py")

if __name__ == "__main__":
    update_models()
    update_logic()
    update_menus()
    update_translations()
