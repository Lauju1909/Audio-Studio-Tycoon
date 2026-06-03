import codecs

lines = []
with codecs.open('menus/research.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_classes = """class HardwareDevMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hardware_dev')
        options = []
        if self.game_state.get_calendar_year() >= 2001 and self.game_state.money >= 100000000:
            options.append({'text': self.game_state.get_text('create_console'), 'action': lambda: "console_name_input"})
        else:
            options.append({'text': self.game_state.get_text('console_reqs_not_met', default="Konsole (Benoetigt Jahr 2001 & 100 Mio EUR)"), 'action': lambda: None})
        options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})
        super().__init__(title, options, audio, game_state)

class ConsoleNameInput(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('create_console_title'), 'console_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "hardware_dev_menu")

    def _on_confirm(self, name):
        self.game_state.current_console_draft = {
            "name": name, 
            "performance": 1, 
            "architecture": "RISC", 
            "marketing_budget": 0, 
            "cost": 50000000 # 50 Mio Base Cost!
        }
        return "console_specs_menu"

class ConsoleSpecsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('console_specs'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        draft = getattr(self.game_state, 'current_console_draft', None)
        if not draft:
            self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "hardware_dev_menu"}]
            return
            
        archs = ["RISC", "x86", "Cell", "ARM"]
        
        self.options = [
            {'text': f"{self.game_state.get_text('console_arch', default='Architektur')}: {draft['architecture']}", 'action': self._cycle_arch},
            {'text': f"{self.game_state.get_text('console_perf', default='Leistung (1-10)')}: {draft['performance']} (+10 Mio EUR)", 'action': self._inc_perf},
            {'text': f"{self.game_state.get_text('console_marketing', default='Marketing-Budget')}: {draft['marketing_budget'] // 1000000} Mio (+5 Mio EUR)", 'action': self._inc_marketing},
            {'text': self.game_state.get_text('start_development_cost', cost=draft['cost']), 'action': self._start},
            {'text': self.game_state.get_text('back'), 'action': lambda: "hardware_dev_menu"}
        ]

    def _cycle_arch(self):
        archs = ["RISC", "x86", "Cell", "ARM"]
        draft = self.game_state.current_console_draft
        idx = archs.index(draft['architecture'])
        draft['architecture'] = archs[(idx + 1) % len(archs)]
        self.audio.play_sound("click")
        self._update_options()
        return None

    def _inc_perf(self):
        draft = self.game_state.current_console_draft
        if draft['performance'] < 10:
            draft['performance'] += 1
            draft['cost'] += 10000000
            self.audio.play_sound("click")
        else:
            self.audio.play_sound("error")
        self._update_options()
        return None

    def _inc_marketing(self):
        draft = self.game_state.current_console_draft
        draft['marketing_budget'] += 5000000
        draft['cost'] += 5000000
        self.audio.play_sound("click")
        self._update_options()
        return None

    def _start(self):
        draft = self.game_state.current_console_draft
        if self.game_state.money >= draft['cost']:
            self.game_state.track_expense("research", draft['cost'])
            self.game_state.is_developing_console = True
            self.game_state.console_progress = 0
            self.game_state.console_total_weeks = 100 + (draft['performance'] * 10) # Takes years!
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('console_dev_started', default="Entwicklung gestartet! Dies wird Jahre dauern."), interrupt=True)
            return "game_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
        return None
"""

start = -1
end = -1
for i, line in enumerate(lines):
    if 'class HardwareDevMenu(Menu):' in line:
        start = i
    if start != -1 and 'def _start(self):' in line:
        pass
    if start != -1 and 'return None' in line and i > start + 50:
        end = i + 1
        break

if start != -1 and end != -1:
    lines = lines[:start] + [new_classes + '\n'] + lines[end:]

with codecs.open('menus/research.py', 'w', 'utf-8') as f:
    f.writelines(lines)
