import codecs

lines = []
with codecs.open('menus/research.py', 'r', 'utf-8') as f:
    lines = f.readlines()

overview_classes = """class ConsoleOverviewMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('my_consoles', default='Meine Konsolen'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        consoles = getattr(self.game_state, 'custom_consoles', [])
        for i, c in enumerate(consoles):
            self.options.append({
                'text': c.name,
                'action': lambda idx=i: self._view_console(idx)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hardware_dev_menu"})

    def _view_console(self, idx):
        self.game_state.ui_context['selected_console_idx'] = idx
        return "console_detail_menu"

class ConsoleDetailMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        idx = self.game_state.ui_context.get('selected_console_idx', 0)
        c = self.game_state.custom_consoles[idx]
        
        info = f"{c.name} - Architektur: {getattr(c, 'architecture', 'RISC')}, Leistung: {getattr(c, 'performance', getattr(c, 'tech_level', 1))}. "
        info += f"Verkaufte Einheiten: {getattr(c, 'units_sold', 0):,}. Marktanteil: {getattr(c, 'market_share', 0)*100:.1f}%."
        
        super().__init__(info, [{'text': self.game_state.get_text('back'), 'action': lambda: "console_overview_menu"}], audio, game_state)
        self.audio.speak(info, interrupt=False)
"""

# Modify HardwareDevMenu to have "Meine Konsolen"
new_hw_init = """    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hardware_dev')
        options = []
        if self.game_state.get_calendar_year() >= 2001 and self.game_state.money >= 100000000:
            options.append({'text': self.game_state.get_text('create_console'), 'action': lambda: "console_name_input"})
        else:
            options.append({'text': self.game_state.get_text('console_reqs_not_met', default="Konsole (Benoetigt Jahr 2001 & 100 Mio EUR)"), 'action': lambda: None})
            
        if getattr(self.game_state, 'custom_consoles', []):
            options.append({'text': self.game_state.get_text('my_consoles', default='Meine Konsolen'), 'action': lambda: "console_overview_menu"})
            
        options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})
        super().__init__(title, options, audio, game_state)
"""

start = -1
end = -1
for i, line in enumerate(lines):
    if 'def __init__(self, audio, game_state):' in line and 'title = self.game_state.get_text(\'hardware_dev\')' in lines[i+3]:
        start = i
    if start != -1 and 'super().__init__(title, options, audio, game_state)' in line:
        end = i + 1
        break

if start != -1 and end != -1:
    lines = lines[:start] + [new_hw_init] + lines[end:]

lines.append('\n' + overview_classes)

with codecs.open('menus/research.py', 'w', 'utf-8') as f:
    f.writelines(lines)
