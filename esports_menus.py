
class ESportsMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('esports_menu_title', default='E-Sports Zentrale'), [], audio, game_state)
    def announce_entry(self):
        self.options = []
        if self.game_state.get_calendar_year() < 2010:
            self.options.append({'text': self.game_state.get_text('esports_locked', default='E-Sports (Gesperrt bis 2010)'), 'action': lambda: None})
        else:
            self.options.append({'text': self.game_state.get_text('esports_create_league', default='Neue Liga gruenden (5.000.000 EUR)'), 'action': lambda: "esports_create_league_menu"})
            leagues = getattr(self.game_state, 'esports_leagues', [])
            if leagues:
                self.options.append({'text': self.game_state.get_text('esports_manage_leagues', default='Ligen & World Championships'), 'action': lambda: "esports_manage_league_menu"})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "business_menu"})
        super().announce_entry()

class ESportsCreateLeagueMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('esports_create_title', default='Waehle ein Spiel fuer die Liga'), [], audio, game_state)
    def announce_entry(self):
        self.options = []
        existing_leagues = [l.game_name for l in getattr(self.game_state, 'esports_leagues', [])]
        
        for game in self.game_state.game_history:
            # We assume multiplayer is maybe Action or Sport for now, or just let them pick any released game.
            if game.name not in existing_leagues and game.sales > 100000:
                self.options.append({
                    'text': f"{game.name} - 5.000.000 EUR",
                    'action': lambda g=game: self.create_league(g)
                })
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "esports_menu"})
        super().announce_entry()
        
    def create_league(self, game):
        cost = 5000000
        if self.game_state.money < cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'), interrupt=True)
            return None
            
        self.game_state.money -= cost
        self.game_state.track_expense("marketing", cost)
        
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
        super().__init__(game_state.get_text('esports_manage_title', default='Ligen verwalten'), [], audio, game_state)
    def announce_entry(self):
        self.options = []
        leagues = getattr(self.game_state, 'esports_leagues', [])
        for i, l in enumerate(leagues):
            self.options.append({
                'text': f"{l.game_name} (Hype: {int(l.hype)}) - {l.sponsor_tier}",
                'action': lambda idx=i: self.manage_league(idx)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "esports_menu"})
        super().announce_entry()
        
    def manage_league(self, idx):
        if not hasattr(self.game_state, 'ui_context'):
            self.game_state.ui_context = {}
        self.game_state.ui_context['selected_league_idx'] = idx
        return "esports_championship_menu"

class ESportsChampionshipMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__("Championships & Sponsoren", [], audio, game_state)
    def announce_entry(self):
        self.options = []
        idx = self.game_state.ui_context.get('selected_league_idx', 0)
        self.league = self.game_state.esports_leagues[idx]
        
        self.title = self.game_state.get_text('esports_champ_title', game=self.league.game_name, default=f"Liga: {self.league.game_name}")
        
        from models import EsportsLeague
        
        if self.league.last_championship_year >= self.game_state.get_calendar_year():
            self.options.append({'text': self.game_state.get_text('esports_champ_done', default='Championship in diesem Jahr bereits abgehalten.'), 'action': lambda: None})
        else:
            for ct in EsportsLeague.CHAMPIONSHIP_TYPES:
                cost = ct['cost']
                text = self.game_state.get_text(f"esports_champ_{ct['id']}", cost=f"{cost:,}", default=f"Event ({cost:,} EUR)")
                self.options.append({
                    'text': text,
                    'action': lambda c=ct: self._host_champ(c)
                })
        
        self.options.append({'text': self.game_state.get_text('esports_sponsors', default='Sponsoren verwalten'), 'action': lambda: "esports_sponsor_menu"})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "esports_manage_league_menu"})
        super().announce_entry()

    def _host_champ(self, ct):
        import random
        cost = ct['cost']
        if self.game_state.money < cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'), interrupt=True)
            return None
            
        self.game_state.money -= cost
        self.game_state.track_expense("marketing", cost)
        
        fan_base = self.game_state.fans
        base_viewers = int(fan_base * 0.08 * (self.league.hype / 100.0) * ct['viewer_mult'])
        viewers = max(10000, int(base_viewers * random.uniform(0.8, 1.25)))
        
        prize_pool = int(cost * 0.15)
        self.league.prize_pool_total += prize_pool
        
        streaming_bonus = 1.0 + self.league.streaming_deals * 0.2
        revenue = int(viewers * ct['rev_per_viewer'] * streaming_bonus)
        revenue = int(revenue * random.uniform(0.85, 1.15))
        
        self.game_state.money += revenue
        self.game_state.track_income("esports", revenue)
        self.league.total_championship_income += revenue
        self.league.last_championship_revenue = revenue
        self.league.last_championship_viewers = viewers
        self.league.total_viewers += viewers
        
        hype_gain = ct['hype_bonus'] * (1.0 + self.league.streaming_deals * 0.1)
        self.league.hype = min(200.0, self.league.hype + hype_gain)
        self.league.championships_held += 1
        self.league.last_championship_year = self.game_state.get_calendar_year()
        
        fan_gain = int(viewers * 0.01)
        self.game_state.fans += fan_gain
        
        self.audio.play_sound("cash")
        msg = self.game_state.get_text(
            'esports_champ_result',
            viewers=f"{viewers:,}",
            revenue=f"{revenue:,}",
            hype=int(hype_gain),
            fans=f"{fan_gain:,}",
            prize=f"{prize_pool:,}",
            default=f"Erfolg! {viewers:,} Zuschauer brachten {revenue:,} EUR. +{int(hype_gain)} Hype. +{fan_gain:,} Fans."
        )
        self.audio.speak(msg, interrupt=True)
        
        from models import Email
        self.game_state.emails.insert(0, Email(
            sender=self.game_state.get_text('esports_sender', default='E-Sports Team'),
            subject=self.game_state.get_text('esports_champ_email_subject',
                                              game=self.league.game_name,
                                              year=self.game_state.get_calendar_year(),
                                              default=f"World Championship {self.game_state.get_calendar_year()}: {self.league.game_name}"),
            body=self.game_state.get_text(
                'esports_champ_email_body',
                viewers=f"{viewers:,}",
                revenue=f"{revenue:,}",
                prize=f"{prize_pool:,}",
                fans=f"{fan_gain:,}",
                hype=int(hype_gain),
                default=(
                    f"Das World Championship für '{self.league.game_name}' ist Geschichte!\\n"
                    f"Zuschauer: {viewers:,}\\nEinnahmen: {revenue:,} EUR\\n"
                    f"Preisgeld: {prize_pool:,} EUR\\nNeue Fans: +{fan_gain:,}\\nHype: +{int(hype_gain)}"
                )
            ),
            date_week=self.game_state.week
        ))
        
        self.announce_entry()
        return None

class ESportsSponsorMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__("Sponsoren", [], audio, game_state)
    def announce_entry(self):
        self.options = []
        idx = self.game_state.ui_context.get('selected_league_idx', 0)
        league = self.game_state.esports_leagues[idx]
        
        from models import EsportsLeague
        for st in EsportsLeague.SPONSOR_TIERS:
            # Check if this tier is higher than the current one
            if st['id'] == league.sponsor_tier:
                self.options.append({'text': f"Aktuell: {st['id']} (+{st['weekly_base']} EUR/Woche)", 'action': lambda: None})
            else:
                self.options.append({'text': f"Zu {st['id']} wechseln (+{st['weekly_base']} EUR/Woche)", 'action': lambda s=st: self.change_sponsor(s, league)})
                
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "esports_championship_menu"})
        super().announce_entry()
        
    def change_sponsor(self, st, league):
        league.sponsor_tier = st['id']
        self.audio.play_sound("confirm")
        self.audio.speak(f"Sponsor auf {st['id']} geaendert!", interrupt=True)
        self.announce_entry()
        return None

