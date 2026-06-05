import sys

with open('menus/office.py', 'r', encoding='utf-8') as f:
    content = f.read()

merch_menu = '''
class MerchandisingMenu(Menu):
    def __init__(self, state):
        super().__init__(state)
        self.title = state.get_text("menu_merchandising")
        
        # Lade alle Spiele als verfÃ¼gbare Marken
        self.games = [g for g in state.game_history]
        self.selected_game_idx = 0
        
        self.merch_types = [
            {"name": state.get_text("merch_type_tshirt"), "cost": 10000, "duration": 12},
            {"name": state.get_text("merch_type_soundtrack"), "cost": 25000, "duration": 24},
            {"name": state.get_text("merch_type_figures"), "cost": 50000, "duration": 48}
        ]
        self.selected_type_idx = 0
        
        self._update_options()
        
    def _update_options(self):
        self.options = []
        if not self.games:
            self.options.append(("Keine IPs verfÃ¼gbar", lambda: None))
            self.options.append(("ZurÃ¼ck", lambda: self.state.close_menu()))
            return
            
        game = self.games[self.selected_game_idx]
        mtype = self.merch_types[self.selected_type_idx]
        
        self.options.append((f"Marke: {game.name} (IP: {game.ip_rating})", self.next_game))
        self.options.append((f"Typ: {mtype['name']} ({mtype['cost']}â‚¬, {mtype['duration']}W)", self.next_type))
        self.options.append((self.state.get_text("start_merch"), self.start_merch))
        self.options.append(("", lambda: None))
        
        # Zeige aktive Kampagnen
        active = getattr(self.state, "active_merch", [])
        if active:
            self.options.append((f"--- {self.state.get_text('merch_campaigns')} ---", lambda: None))
            for m in active:
                self.options.append((f"{m.merch_type} ({m.game_name}) - {m.weeks_active}/{m.duration_weeks}W", lambda: None))
                
        self.options.append(("", lambda: None))
        self.options.append(("ZurÃ¼ck", lambda: self.state.close_menu()))
        
    def next_game(self):
        if self.games:
            self.selected_game_idx = (self.selected_game_idx + 1) % len(self.games)
            self._update_options()
            
    def next_type(self):
        self.selected_type_idx = (self.selected_type_idx + 1) % len(self.merch_types)
        self._update_options()
        
    def start_merch(self):
        if not self.games: return
        game = self.games[self.selected_game_idx]
        mtype = self.merch_types[self.selected_type_idx]
        
        if self.state.start_merch_campaign(game.name, mtype["name"], mtype["duration"], mtype["cost"]):
            tolk.output("Kampagne gestartet!")
        else:
            tolk.output("Nicht genug Geld!")
        self._update_options()
'''

if 'class MerchandisingMenu' not in content:
    content += '\n' + merch_menu
    with open('menus/office.py', 'w', encoding='utf-8') as f:
        f.write(content)
