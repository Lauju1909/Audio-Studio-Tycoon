from ..base import Menu, TextInputMenu
import random
import webbrowser
import urllib.parse


class EspionageMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('espionage_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        self.options = []
        for i, rival in enumerate(gs.rivals):
            self.options.append({'text': gs.get_text('espionage_steal_tech', cost=200000) + f" ({rival.name})", 'action': lambda idx=i: self._spy(idx)})
            self.options.append({'text': gs.get_text('espionage_smear_campaign', cost=100000) + f" ({rival.name})", 'action': lambda idx=i: self._sabotage(idx)})
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "stock_market_menu"})

    def _spy(self, rival_idx):
        gs = self.game_state
        if gs.money < 200000:
            self.audio.play_sound("error")
            self.audio.speak(gs.get_text('espionage_not_enough_money'))
            return None
        gs.track_expense("other", 200000)
        if random.random() < 0.3:
            self.audio.play_sound("cheer")
            self.audio.speak(gs.get_text('espionage_steal_success'))
            gs.research_progress += 50
        else:
            self.audio.play_sound("error")
            self.audio.speak(gs.get_text('espionage_steal_caught', penalty=500000))
            gs.track_expense("other", 500000)
        return "stock_market_menu"

    def _sabotage(self, rival_idx):
        gs = self.game_state
        rival = gs.rivals[rival_idx]
        if gs.money < 100000:
            self.audio.play_sound("error")
            self.audio.speak(gs.get_text('espionage_not_enough_money'))
            return None
        gs.track_expense("other", 100000)
        if random.random() < 0.6:
            self.audio.play_sound("cheer")
            self.audio.speak(gs.get_text('espionage_smear_success', name=rival.name))
            rival.hype = max(0, rival.hype - 30)
        else:
            self.audio.play_sound("error")
            self.audio.speak(gs.get_text('espionage_smear_caught', penalty=5000))
            gs.fans = max(0, gs.fans - 5000)
        return "stock_market_menu"


class ESportsMenu(Menu):
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
        self.league.total_championship_income += sponsorship
        self.league.total_viewers += viewers
        self.league.last_championship_viewers = viewers
        self.league.last_championship_revenue = sponsorship
        self.league.prize_pool_total += cost
        
        # Re-activate the game's sales!
        for g in self.game_state.game_history:
            if g.name == self.league.game_name:
                g.week_developed = self.game_state.week # Reset aging to generate sales again
                
        self.audio.play_sound("cash")
        msg = self.game_state.get_text('esports_champ_result', viewers=viewers, revenue=sponsorship, default=f"Das Event war ein Erfolg! {viewers:,} Zuschauer brachten {sponsorship:,} EUR durch Sponsoren ein!")
        self.audio.speak(msg, interrupt=True)
        
        # Jahres-Email
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
                revenue=f"{sponsorship:,}", prize=f"{cost:,}", fans=f"{int(viewers * 0.1):,}", hype=int(50 * multiplier),
                default=(
                    f"Das World Championship fÃ¼r '{self.league.game_name}' ist Geschichte!\n"
                    f"Zuschauer: {viewers:,}\nEinnahmen: {sponsorship:,} EUR\n"
                    f"Preisgeld: {cost:,} EUR\nNeue Fans: +{int(viewers * 0.1):,}\nHype: +{int(50 * multiplier)}"
                )
            ),
            date_week=self.game_state.week
        ))
        self._update_options()
        return None


class AcquisitionMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('acquisition_menu_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        for idx, rival in enumerate(self.game_state.rivals):
            if getattr(rival, 'is_owned_by_player', False):
                self.options.append({
                    'text': self.game_state.get_text('subsidiary_manage_option', default='Tochterfirma verwalten: {name}').format(name=rival.name),
                    'action': lambda i=idx: self.manage_subsidiary(i)
                })
            else:
                buyout_cost = (100 - getattr(rival, 'owned_shares', 0)) * 50000 
                
                self.options.append({
                    'text': self.game_state.get_text('acquisition_option', name=rival.name, cost=buyout_cost, shares=getattr(rival, 'owned_shares', 0)),
                    'action': lambda i=idx, cost=buyout_cost: self.acquire_studio(i, cost)
                })
            
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_studios_available'), 'action': lambda: "bank_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})
        super().announce_entry()
        
    def manage_subsidiary(self, idx):
        self.game_state.selected_subsidiary_idx = idx
        return "subsidiary_manage_menu"

    def acquire_studio(self, idx, cost):
        rival = self.game_state.rivals[idx]
        shares = getattr(rival, 'owned_shares', 0)
        
        if shares < 50:
            self.audio.speak(self.game_state.get_text('acquisition_need_shares'))
            return None
            
        if self.game_state.money < cost:
            self.audio.speak(self.game_state.get_text('acquisition_fail_money', cost=cost))
            return None
            
        self.game_state.track_expense("other", cost)
        rival.is_owned_by_player = True
        rival.owned_shares = 100
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('acquisition_success', name=rival.name))
        return "bank_menu"


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
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
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
        leagues = getattr(self.game_state, 'esports_leagues', [])
        idx = getattr(self.game_state, 'ui_context', {}).get('selected_league_idx', 0)
        if not leagues or idx < 0 or idx >= len(leagues):
            self.title = "Keine Liga gewählt"
            self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "esports_menu"}]
            super().announce_entry()
            return
        self.league = leagues[idx]
        
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
        leagues = getattr(self.game_state, 'esports_leagues', [])
        idx = getattr(self.game_state, 'ui_context', {}).get('selected_league_idx', 0)
        if not leagues or idx < 0 or idx >= len(leagues):
            self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "esports_menu"}]
            super().announce_entry()
            return
        league = leagues[idx]
        
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


class SubsidiaryManagementMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('subsidiary_manage_title', default='Tochterfirma verwalten'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        rival_idx = getattr(self.game_state, 'selected_subsidiary_idx', -1)
        if 0 <= rival_idx < len(self.game_state.rivals):
            rival = self.game_state.rivals[rival_idx]
            
            self.options.append({
                'text': self.game_state.get_text('subsidiary_inject_cash', default='100.000 EUR investieren (Erhöht Spielqualität)'),
                'action': lambda: self.inject_cash(rival)
            })
            
            if getattr(self.game_state, 'active_custom_console', None):
                self.options.append({
                    'text': self.game_state.get_text('subsidiary_force_console', default='Anweisen, exklusiv für unsere Konsole zu entwickeln'),
                    'action': lambda: self.force_console(rival)
                })
                
            self.options.append({
                'text': self.game_state.get_text('subsidiary_absorb', default='Studio auflösen & IPs übernehmen'),
                'action': lambda: self.absorb_studio(rival, rival_idx)
            })

        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "acquisition_menu"})
        super().announce_entry()

    def inject_cash(self, rival):
        if self.game_state.money >= 100000:
            self.game_state.money -= 100000
            self.game_state.track_expense("other", 100000)
            rival.games_quality_boost = getattr(rival, 'games_quality_boost', 0) + 1.0
            self.audio.speak(self.game_state.get_text('subsidiary_cash_success', default='Geld investiert. Ihre zukünftigen Spiele werden besser.'))
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money', default='Nicht genug Geld.'))
        return "subsidiary_manage_menu"

    def force_console(self, rival):
        rival.develop_for_custom_console = True
        self.audio.speak(self.game_state.get_text('subsidiary_console_success', default='Das Studio entwickelt künftig exklusiv für unsere Konsole.'))
        return "subsidiary_manage_menu"

    def absorb_studio(self, rival, idx):
        transferred_fans = int(getattr(rival, 'fans', 5000) * 0.25)
        self.game_state.fans += transferred_fans
        if hasattr(rival, 'games'):
            self.game_state.game_history.extend(rival.games)
            
        self.audio.speak(self.game_state.get_text('subsidiary_absorb_success', default='Studio aufgelöst. Wir haben ihre Spiele und {} Fans übernommen.').format(transferred_fans))
        self.game_state.rivals.pop(idx)
        return "acquisition_menu"
