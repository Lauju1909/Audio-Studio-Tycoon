import sys

with open('menus/hardware.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to _update_options
update_code = '''
        # 3. Option: Ver?ffentlichte Soundkarten & Tantiemen
        self.options.append({'text': gs.get_text('hardware_opt_overview'), 'action': lambda: "hardware_overview"})
        
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "game_menu"})
'''
new_update_code = '''
        # 3. Option: Ver?ffentlichte Soundkarten & Tantiemen
        self.options.append({'text': gs.get_text('hardware_opt_overview'), 'action': lambda: "hardware_overview"})
        
        # 4. Option: Eigene Konsole
        if not getattr(gs, "active_custom_console", None):
            self.options.append({'text': gs.get_text('console_opt_develop'), 'action': lambda: "console_create"})
        else:
            cc = gs.active_custom_console
            if cc.is_released:
                self.options.append({'text': gs.get_text('console_active_stats', name=cc.name, users=cc.active_users, revenue=cc.revenue), 'action': None})
            else:
                self.options.append({'text': gs.get_text('console_in_dev', name=cc.name, progress=int(cc.progress*100)), 'action': None})

        self.options.append({'text': gs.get_text('back'), 'action': lambda: "game_menu"})
'''
content = content.replace(update_code, new_update_code)

# Add new Menus at the bottom
new_menus = '''
from menus.base import TextInputMenu

class ConsoleCreateMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('hardware_menu_title', 'console_name_prompt', audio, game_state,
                         on_confirm=self._confirm, on_cancel=lambda: "hardware_menu")

    def _confirm(self, name):
        if not name:
            self.audio.speak(self.game_state.get_text('invalid_name'))
            return "console_create"
            
        self.game_state._pending_console_name = name
        return "console_components"

class ConsoleComponentsMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('console_comp_title'), [], audio, game_state)
        
    def announce_entry(self):
        self.options = []
        gs = self.game_state
        
        tiers = [
            ("Budget", 20000000, 199, 10),
            ("Standard", 50000000, 299, 20),
            ("High-End", 100000000, 499, 40)
        ]
        
        for t, cost, price, tech in tiers:
            self.options.append({
                'text': gs.get_text('console_tier_opt', tier=t, cost=cost, price=price, tech=tech),
                'action': lambda t=t, c=cost, p=price, tc=tech: self._start_console(t, c, p, tc)
            })
            
        self.options.append({'text': gs.get_text('cancel'), 'action': lambda: "hardware_menu"})
        super().announce_entry()

    def _start_console(self, tier, cost, price, tech):
        gs = self.game_state
        if gs.money < cost:
            self.audio.speak(gs.get_text('not_enough_money_hardware'))
            return None
            
        gs.track_expense("other", cost)
        name = getattr(gs, '_pending_console_name', "MyConsole")
        
        from models import CustomConsoleProject
        cc = CustomConsoleProject(name=name, tech_level=tech, dev_cost=cost, price=price)
        cc.total_weeks = 50 if tier == "Budget" else 100 if tier == "Standard" else 150
        gs.active_custom_console = cc
        
        self.audio.play_sound("confirm")
        self.audio.speak(gs.get_text('console_started', name=name))
        return "hardware_menu"
'''
content += new_menus

with open('menus/hardware.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched hardware.py")
