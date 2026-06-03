import codecs

lines = []
with codecs.open('menus/business.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_classes = """class ESportsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('esports_menu_title', default='E-Sports Zentrale'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        if self.game_state.get_calendar_year() < 2010:
            self.options.append({'text': self.game_state.get_text('esports_locked', default='E-Sports (Gesperrt bis 2010)'), 'action': lambda: None})
        else:
            self.options.append({'text': self.game_state.get_text('esports_create_league', default='Neue Liga gruenden (5.000.000 EUR)'), 'action': lambda: "esports_create_league_menu"})
            
            leagues = getattr(self.game_state, 'esports_leagues', [])
            if leagues:
                self.options.append({'text': self.game_state.get_text('esports_manage_leagues', default='Ligen & World Championships'), 'action': lambda: "esports_manage_league_menu"})
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

class ESportsCreateLeagueMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('esports_create_title', default='Waehle ein Spiel fuer die Liga'), [], audio, game_state)
        self._update_options()
        
    def _update_options(self):
        self.options = []
        # Filter games that are good for e-sports
        eligible = []
        existing_leagues = [l.game_name for l in getattr(self.game_state, 'esports_leagues', [])]
        
        for g in self.game_state.game_history:
            if g.name in existing_leagues:
                continue
            if g.sales > 500000 or g.genre in ["Action", "Strategie", "Simulation"]:
                eligible.append(g)
                
        for g in eligible[-20:]: # Show max 20 recent eligible games
            self.options.append({
                'text': g.name,
                'action': lambda game=g: self._create_league(game)
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "esports_menu"})
        
    def _create_league(self, game):
        if self.game_state.money < 5000000:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'), interrupt=True)
            return None
            
        self.game_state.track_expense("marketing", 5000000)
        from models import EsportsLeague
        league = EsportsLeague(game.name, self.game_state.week)
        
        if not hasattr(self.game_state, 'esports_leagues'):
            self.game_state.esports_leagues = []
        self.game_state.esports_leagues.append(league)
        
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('esports_league_created', game=game.name, default=f"E-Sports Liga fuer {game.name} gegruendet!"), interrupt=True)
        return "esports_menu"

class ESportsManageLeagueMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('esports_manage_title', default='Ligen verwalten'), [], audio, game_state)
        self._update_options()
        
    def _update_options(self):
        self.options = []
        leagues = getattr(self.game_state, 'esports_leagues', [])
        for i, l in enumerate(leagues):
            self.options.append({
                'text': f"{l.game_name} (Hype: {l.hype:.0f})",
                'action': lambda idx=i: self._manage(idx)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "esports_menu"})
        
    def _manage(self, idx):
        self.game_state.ui_context['selected_league_idx'] = idx
        return "esports_championship_menu"

class ESportsChampionshipMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        idx = self.game_state.ui_context.get('selected_league_idx', 0)
        self.league = self.game_state.esports_leagues[idx]
        
        title = self.game_state.get_text('esports_champ_title', game=self.league.game_name, default=f"World Championship: {self.league.game_name}")
        super().__init__(title, [], audio, game_state)
        self._update_options()
        
    def _update_options(self):
        self.options = []
        year = self.game_state.get_calendar_year()
        
        if self.league.last_championship_year == year:
            self.options.append({'text': self.game_state.get_text('esports_champ_done', default='Championship in diesem Jahr bereits abgehalten.'), 'action': lambda: None})
        else:
            self.options.append({'text': self.game_state.get_text('esports_champ_small', default='Kleines Event (1 Mio EUR)'), 'action': lambda: self._host_champ(1000000, 1.0)})
            self.options.append({'text': self.game_state.get_text('esports_champ_med', default='Mittleres Event im Stadion (5 Mio EUR)'), 'action': lambda: self._host_champ(5000000, 2.0)})
            self.options.append({'text': self.game_state.get_text('esports_champ_huge', default='Gigantisches Mega-Event (20 Mio EUR)'), 'action': lambda: self._host_champ(20000000, 5.0)})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "esports_manage_league_menu"})

    def _host_champ(self, cost, multiplier):
        if self.game_state.money < cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'), interrupt=True)
            return None
            
        self.game_state.track_expense("marketing", cost)
        
        # Calculate revenue based on Fans + League Hype
        import random
        base_viewers = self.game_state.fans * 0.1 * (self.league.hype / 100.0) * multiplier
        viewers = int(base_viewers * random.uniform(0.8, 1.2))
        
        sponsorship = int(viewers * 5) # 5 EUR per viewer from sponsors/streaming
        
        self.game_state.money += sponsorship
        self.game_state.track_income("esports", sponsorship)
        
        self.league.hype += 50 * multiplier
        self.league.championships_held += 1
        self.league.last_championship_year = self.game_state.get_calendar_year()
        
        # Re-activate the game's sales!
        for g in self.game_state.game_history:
            if g.name == self.league.game_name:
                g.week_developed = self.game_state.week # Reset aging to generate sales again
                
        self.audio.play_sound("cash")
        msg = self.game_state.get_text('esports_champ_result', viewers=viewers, revenue=sponsorship, default=f"Das Event war ein Erfolg! {viewers:,} Zuschauer brachten {sponsorship:,} EUR durch Sponsoren ein!")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return None
"""

start = -1
end = -1
for i, line in enumerate(lines):
    if 'class ESportsMenu(Menu):' in line:
        start = i
    if start != -1 and 'class AcquisitionMenu(Menu):' in line:
        end = i
        break

if start != -1 and end != -1:
    lines = lines[:start] + [new_classes + '\n'] + lines[end:]

with codecs.open('menus/business.py', 'w', 'utf-8') as f:
    f.writelines(lines)
