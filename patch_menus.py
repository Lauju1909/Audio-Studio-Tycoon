import re

with open('menus/office.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_menus = '''
class OfficePerksMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('office_perks_menu'), [], audio, game_state)
        if not hasattr(self.game_state, 'office_perks'):
            self.game_state.office_perks = []
        self._update_options()
        
    def _update_options(self):
        self.options = []
        for perk in ["fruit_basket", "kicker_table", "company_car"]:
            active = perk in getattr(self.game_state, "office_perks", [])
            status = self.game_state.get_text('active') if active else self.game_state.get_text('inactive')
            text = f"{self.game_state.get_text('perk_'+perk)} [{status}]"
            self.options.append({'text': text, 'action': lambda p=perk: self.toggle_perk(p)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hr_menu"})

    def toggle_perk(self, perk):
        if not hasattr(self.game_state, "office_perks"):
            self.game_state.office_perks = []
        if perk in self.game_state.office_perks:
            self.game_state.office_perks.remove(perk)
            self.audio.play_sound('click')
        else:
            cost = 2000 if perk == "fruit_basket" else (5000 if perk == "kicker_table" else 20000)
            if self.game_state.money >= cost:
                self.game_state.money -= cost
                self.game_state.track_expense("other", cost)
                self.game_state.office_perks.append(perk)
                self.audio.play_sound('cash')
            else:
                self.audio.play_sound('error')
        self._update_options()
        return "stay"

class HeadhuntingEventMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('headhunting_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        event = getattr(self.game_state, "pending_headhunt_event", None)
        if not event:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
            return
            
        emp = event["employee"]
        offer = event["rival_offer"]
        
        self.title = self.game_state.get_text('headhunting_desc', name=emp.name, offer=offer)
        
        self.options.append({
            'text': self.game_state.get_text('match_offer', offer=offer),
            'action': lambda: self.match_offer()
        })
        self.options.append({
            'text': self.game_state.get_text('let_them_go'),
            'action': lambda: self.let_go()
        })
        
    def match_offer(self):
        event = getattr(self.game_state, "pending_headhunt_event", None)
        if event:
            emp = event["employee"]
            emp.salary = event["rival_offer"]
            self.audio.play_sound('success')
            self.game_state.pending_headhunt_event = None
        return "game_menu"
        
    def let_go(self):
        event = getattr(self.game_state, "pending_headhunt_event", None)
        if event:
            emp = event["employee"]
            if emp in self.game_state.employees:
                self.game_state.employees.remove(emp)
                for ap in self.game_state.active_projects:
                    proj = ap["project"]
                    if getattr(proj, "team", None) and emp in proj.team:
                        proj.team.remove(emp)
            self.audio.play_sound('error')
            self.game_state.pending_headhunt_event = None
        return "game_menu"
'''

content += "\n" + new_menus

# Also add Office Perks to HRMenu
target_hr = "{'text': self.game_state.get_text('menu_teambuilding'), 'action': lambda: \"teambuilding_menu\"},"
replace_hr = target_hr + "\n            {'text': self.game_state.get_text('office_perks_menu'), 'action': lambda: \"office_perks_menu\"},"
content = content.replace(target_hr, replace_hr)

with open('menus/office.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('menus/office.py updated')
