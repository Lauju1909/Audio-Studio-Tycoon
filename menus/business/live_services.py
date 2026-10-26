from ..base import Menu, TextInputMenu
import random
import webbrowser
import urllib.parse


class ServiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('service_menu')
        options = []
        
        def add_locked_feature(feature_id, text, action):
            if self.game_state.is_feature_unlocked(feature_id):
                options.append({'text': text, 'action': action})
            else:
                from game_data import FEATURE_UNLOCKS
                if feature_id in FEATURE_UNLOCKS:
                    options.append({'text': f"{text} (Ab {FEATURE_UNLOCKS[feature_id].get('year', '???')})", 'action': lambda: None})
        
        add_locked_feature("subscription_vault", self.game_state.get_text('service_manage_subscription'), lambda: "subscription_service_menu")
        add_locked_feature("cloud_gaming", self.game_state.get_text('cloud_gaming_title', default="Cloud Gaming Service"), lambda: "cloud_gaming_menu")
        
        options.extend([
            {'text': self.game_state.get_text('game_service_options'), 'action': lambda: "game_service_options"},
            {'text': self.game_state.get_text('contract_work_menu_title', default="Auftragsarbeiten"), 'action': lambda: "contract_work_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ])
        super().__init__(title, options, audio, game_state)


class ContractWorkMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('contract_work_menu_title', default="Auftragsarbeiten"), [], audio, game_state)
        self.contract_options = []
        self._update_options()

    def _update_options(self):
        self.options = []
        if not self.contract_options:
            self.contract_options = self.game_state.generate_contract_work_options()
        
        for idx, cw in enumerate(self.contract_options):
            txt = f"{cw['name']} ({cw['type']}) - Ziel: {int(cw['target_points'])} Pkt - {cw['payout']} EUR"
            self.options.append({'text': txt, 'action': lambda i=idx: self._select_contract(i)})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})

    def _select_contract(self, idx):
        cw = self.contract_options[idx]
        if self.game_state.start_contract_work(cw):
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('contract_started', default=f"Auftrag {cw['name']} angenommen!"))
            self.contract_options.pop(idx)
            self._update_options()
            self.current_index = 0
            return "dev_progress_menu"
        return None


class GameServiceOptionsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('game_service_options'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        if self.game_state.get_calendar_year() >= 2010:
            self.options.append({'text': self.game_state.get_text('menu_add_mtx', default="Mikrotransaktionen integrieren"), 'action': lambda: "add_mtx_menu"})
        self.options.extend([
            {'text': self.game_state.get_text('menu_movie_deal', default="Filmlizenzen verkaufen"), 'action': lambda: "movie_deal_menu"},
            {'text': self.game_state.get_text('menu_anti_cheat', default="Anti-Cheat System kaufen (100.000 â‚¬)"), 'action': lambda: "anti_cheat_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"}
        ])


class AddMtxMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_add_mtx', default="Mikrotransaktionen integrieren"), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        valid_games = [g for g in self.game_state.game_history if getattr(g, "is_active", False) and not getattr(g, "has_mtx", False)]
        for g in valid_games:
            self.options.append({
                'text': g.name,
                'action': lambda name=g.name: self._add_mtx(name)
            })
        if not valid_games:
            self.options.append({
                'text': self.game_state.get_text('no_games_available'),
                'action': None
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_service_options"})

    def _add_mtx(self, game_name):
        if self.game_state.add_mtx_to_game(game_name):
            if hasattr(self.audio, 'play_sound'):
                self.audio.play_sound('cash')
            if hasattr(self.audio, 'speak'):
                self.audio.speak(self.game_state.get_text('mtx_added_success', game=game_name, default=f"Lootboxen in {game_name} integriert! Fans sind sauer."))
        return "game_service_options"


class MovieDealMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_movie_deal', default="Filmlizenzen verkaufen"), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        valid_games = [g for g in self.game_state.game_history if not getattr(g, "has_movie_deal", False) and g.review and g.review.average >= 8.0 and g.sales >= 500000]
        for g in valid_games:
            self.options.append({
                'text': g.name,
                'action': lambda name=g.name: self._sell_deal(name)
            })
        if not valid_games:
            self.options.append({
                'text': self.game_state.get_text('no_games_available'),
                'action': None
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_service_options"})

    def _sell_deal(self, game_name):
        if self.game_state.sell_movie_license(game_name):
            if hasattr(self.audio, 'play_sound'):
                self.audio.play_sound('cash')
            if hasattr(self.audio, 'speak'):
                self.audio.speak(self.game_state.get_text('movie_deal_success', game=game_name, default=f"Filmdeal fur {game_name} erfolgreich abgeschlossen!"))
        return "game_service_options"


class AntiCheatMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_anti_cheat', default="Anti-Cheat System kaufen (100.000 â‚¬)"), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        valid_games = [g for g in self.game_state.game_history if not getattr(g, "has_anti_cheat", False) and (getattr(g, "is_f2p", False) or any(m.game.name == g.name for m in getattr(self.game_state, 'active_mmos', [])))]
        for g in valid_games:
            self.options.append({
                'text': g.name,
                'action': lambda name=g.name: self._buy_anti_cheat(name)
            })
        if not valid_games:
            self.options.append({
                'text': self.game_state.get_text('no_games_available'),
                'action': None
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_service_options"})

    def _buy_anti_cheat(self, game_name):
        if self.game_state.buy_anti_cheat(game_name):
            if hasattr(self.audio, 'play_sound'):
                self.audio.play_sound('cash')
            if hasattr(self.audio, 'speak'):
                self.audio.speak(self.game_state.get_text('anti_cheat_success', game=game_name, default=f"Anti-Cheat fÃ¼r {game_name} erfolgreich installiert!"))
        else:
            if hasattr(self.audio, 'play_sound'):
                self.audio.play_sound('error')
            if hasattr(self.audio, 'speak'):
                self.audio.speak(self.game_state.get_text('not_enough_money', default="Nicht genug Geld!"))
        return "game_service_options"


class MMOPaymentMenu(Menu):
    """Wahl des Zahlungsmodells fÃ¼r ein MMO/Live-Service-Spiel."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        options = [
            {'text': game_state.get_text('mmo_model_abo'),  'action': lambda: self._select('Abo')},
            {'text': game_state.get_text('mmo_model_f2p'),  'action': lambda: self._select('F2P')},
        ]
        if self.game_state.get_calendar_year() >= 2010:
            options.append({'text': game_state.get_text('mmo_model_loot'), 'action': lambda: self._select('Lootboxen')})
        options.append({'text': game_state.get_text('back'), 'action': lambda: 'game_menu'})
        super().__init__(self.game_state.get_text('mmo_payment_menu'), options, audio, game_state)

    def _select(self, model):
        from models import ActiveMMO
        gs = self.game_state
        proj = getattr(gs, '_pending_mmo_game', None)
        if proj is None:
            self.audio.speak(gs.get_text('mmo_no_game'))
            return 'game_menu'
        initial = max(10000, int(gs.fans * 0.05))
        mmo = ActiveMMO(proj, initial_players=initial, payment_model=model)
        if not hasattr(gs, 'active_mmos'):
            gs.active_mmos = []
        gs.active_mmos.append(mmo)
        gs._pending_mmo_game = None
        self.audio.play_sound('confirm')
        self.audio.speak(gs.get_text('mmo_launched', name=proj.name, model=model, players=initial))
        return 'mmo_management_menu'


class MMOManagementMenu(Menu):
    """Ãœbersicht und Verwaltung aktiver MMOs."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('mmo_management_menu'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        gs = self.game_state
        mmos = getattr(gs, 'active_mmos', [])
        if not mmos:
            self.options.append({'text': gs.get_text('mmo_none_active'), 'action': lambda: 'game_menu'})
        else:
            for idx, mmo in enumerate(mmos):
                label = gs.get_text(
                    'mmo_status_entry',
                    name=mmo.game.name,
                    players=f"{mmo.players:,}",
                    profit=f"{mmo.weekly_profit:,}",
                    model=mmo.payment_model,
                )
                self.options.append({'text': label, 'action': lambda i=idx: self._select(i)})
        self.options.append({'text': gs.get_text('back'), 'action': lambda: 'game_menu'})
        super().announce_entry()

    def _select(self, idx):
        self.game_state._pending_mmo_idx = idx
        return 'mmo_options_menu'


class MMOOptionsMenu(Menu):
    """Optionen fÃ¼r ein einzelnes aktives MMO (Preisanpassung, Abschalten)."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('mmo_options_menu'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        gs = self.game_state
        idx = getattr(gs, '_pending_mmo_idx', -1)
        mmos = getattr(gs, 'active_mmos', [])
        if 0 <= idx < len(mmos):
            mmo = mmos[idx]
            self.title = mmo.game.name + " - Optionen"
            status_txt = gs.get_text(
                'mmo_detail_status',
                players=f"{mmo.players:,}",
                weekly_profit=f"{mmo.weekly_profit:,}",
                weeks=mmo.weeks_active,
            )
            self.options = [
                {'text': status_txt,                    'action': lambda: None},
                {'text': gs.get_text('mmo_raise_price'),  'action': lambda i=idx: self._price(i, +1)},
                {'text': gs.get_text('mmo_lower_price'),  'action': lambda i=idx: self._price(i, -1)},
                {'text': gs.get_text('mmo_shutdown'),     'action': lambda i=idx: self._shutdown(i)},
                {'text': gs.get_text('back'),             'action': lambda: 'mmo_management_menu'},
            ]
        else:
            self.options = [{'text': gs.get_text('back'), 'action': lambda: 'mmo_management_menu'}]
        super().announce_entry()

    def _price(self, idx, direction):
        gs = self.game_state
        mmos = getattr(gs, 'active_mmos', [])
        if 0 <= idx < len(mmos):
            mmo = mmos[idx]
            change = 1 * direction
            mmo.subscription_fee = max(1, mmo.subscription_fee + change)
            # PreisÃ¤nderung beeinflusst Spieler-Zahl
            if direction > 0:
                mmo.players = int(mmo.players * 0.95)
                gs.audio.speak(gs.get_text('mmo_price_raised', fee=mmo.subscription_fee))
            else:
                mmo.players = int(mmo.players * 1.05)
                gs.audio.speak(gs.get_text('mmo_price_lowered', fee=mmo.subscription_fee))
            gs.audio.play_sound('click')
        return 'mmo_options_menu'

    def _shutdown(self, idx):
        gs = self.game_state
        mmos = getattr(gs, 'active_mmos', [])
        if 0 <= idx < len(mmos):
            mmo = mmos.pop(idx)
            gs.audio.play_sound('error')
            gs.audio.speak(gs.get_text('mmo_shutdown_done', name=mmo.game.name))
        return 'mmo_management_menu'


class StreamingPlatformMenu(Menu):
    def __init__(self, audio, state):
        super().__init__(state.get_text('streaming_platform_menu_title'), [], audio, state)
        self.title = state.get_text('streaming_platform_menu_title')
        self.options = []

    def on_enter(self):
        self.options = []
        if not self.state.streaming_platform:
            self.options.append(self.state.get_text('streaming_found_platform'))
        else:
            sp = self.state.streaming_platform
            self.options.append(self.state.get_text('streaming_platform_info', subs=sp.subscribers, level=sp.server_level, cost=sp.get_maintenance_cost(), rev=sp.get_monthly_revenue()))
            self.options.append(self.state.get_text('streaming_upgrade_server', cost=sp.server_level * 5000000))
            status = self.state.get_text('streaming_status_yes') if sp.exclusive_esports else self.state.get_text('streaming_status_no')
            self.options.append(self.state.get_text('streaming_assign_exclusive', status=status))
            
        self.options.append(self.state.get_text('back'))
        super().on_enter()

    def on_select(self, index):
        if not self.state.streaming_platform:
            if index == 0:
                if self.state.found_streaming_platform():
                    self.app.audio.speak(self.state.get_text('streaming_found_success'))
                else:
                    self.app.audio.speak(self.state.get_text('streaming_found_error'))
                self.on_enter()
            else:
                self.app.change_menu('business_menu')
        else:
            if index == 0:
                # Just info
                self.app.audio.speak(self.options[index])
            elif index == 1:
                # Upgrade
                cost = self.state.streaming_platform.server_level * 5000000
                if self.state.upgrade_streaming_server():
                    self.app.audio.speak(self.state.get_text('streaming_upgrade_success', level=self.state.streaming_platform.server_level))
                else:
                    self.app.audio.speak(self.state.get_text('not_enough_money', required=cost))
                self.on_enter()
            elif index == 2:
                # Toggle
                self.state.toggle_exclusive_esports()
                self.app.audio.speak(self.state.get_text('esports_sponsor_changed', tier="")) # Or something else
                self.on_enter()
            else:
                self.app.change_menu('business_menu')


class StreamingPlatformMenu(Menu):
    def __init__(self, audio, state):
        self.audio = audio
        self.game_state = state
        super().__init__(state.get_text('streaming_platform_menu_title'), [], audio, state)
        
    def _update_options(self):
        self.options = []
        if not self.game_state.streaming_platform:
            self.options.append({'text': self.game_state.get_text('streaming_found_platform'), 'action': self._found})
        else:
            sp = self.game_state.streaming_platform
            self.options.append({'text': self.game_state.get_text('streaming_platform_info', subs=sp.subscribers, level=sp.server_level, cost=sp.get_maintenance_cost(), rev=sp.get_monthly_revenue()), 'action': self._info})
            self.options.append({'text': self.game_state.get_text('streaming_upgrade_server', cost=sp.server_level * 5000000), 'action': self._upgrade})
            status = self.game_state.get_text('streaming_status_yes') if sp.exclusive_esports else self.game_state.get_text('streaming_status_no')
            self.options.append({'text': self.game_state.get_text('streaming_assign_exclusive', status=status), 'action': self._toggle})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def on_enter(self):
        self._update_options()
        super().on_enter()

    def _found(self):
        if self.game_state.found_streaming_platform():
            self.audio.speak(self.game_state.get_text('streaming_found_success'))
        else:
            self.audio.speak(self.game_state.get_text('streaming_found_error'))
        self._update_options()
        return "streaming_platform_menu"
        
    def _info(self):
        return "streaming_platform_menu"
        
    def _upgrade(self):
        if self.game_state.upgrade_streaming_server():
            self.audio.speak(self.game_state.get_text('streaming_upgrade_success', level=self.game_state.streaming_platform.server_level))
        else:
            cost = self.game_state.streaming_platform.server_level * 5000000
            self.audio.speak(self.game_state.get_text('not_enough_money', required=cost))
        self._update_options()
        return "streaming_platform_menu"
        
    def _toggle(self):
        self.game_state.toggle_exclusive_esports()
        self.audio.speak(self.game_state.get_text('esports_sponsor_changed', tier="Toggle"))
        self._update_options()
        return "streaming_platform_menu"


class CloudGamingMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('cloud_gaming_title', default='Cloud Gaming Service'), [], audio, game_state)
        self.options = []

    def on_enter(self):
        self.options.clear()
        gs = self.game_state
        cg = getattr(gs, "cloud_gaming", None)
        if not cg:
            self.options.append({'text': gs.get_text('back'), 'action': lambda: "business_menu"})
            return

        if not cg.active:
            self.options.append({
                'text': gs.get_text('cloud_gaming_start', default='Dienst starten (10.000.000 $)'),
                'action': self._start
            })
        else:
            self.options.append({
                'text': gs.get_text('cloud_gaming_stop', default='Dienst stoppen') + f" ({cg.subscribers:,} Subs)",
                'action': self._toggle
            })
            self.options.append({
                'text': gs.get_text('cloud_gaming_price_up', default='Preis erhoehen (Aktuell: {}$)', price=cg.price),
                'action': self._price_up
            })
            self.options.append({
                'text': gs.get_text('cloud_gaming_price_down', default='Preis senken (Aktuell: {}$)', price=cg.price),
                'action': self._price_down
            })
            upgrade_cost = cg.tech_level * 5000000
            self.options.append({
                'text': gs.get_text('cloud_gaming_upgrade', default='Server ausbauen (Stufe {}, Kosten: {:,}$)', level=cg.tech_level, cost=upgrade_cost),
                'action': self._upgrade
            })
            
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "business_menu"})

    def _start(self):
        cg = self.game_state.cloud_gaming
        if self.game_state.money >= 10000000:
            self.game_state.money -= 10000000
            cg.active = True
            cg.tech_level = 1
            self.audio.speak(self.game_state.get_text('cloud_gaming_started', default='Cloud Gaming Service gestartet.'))
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money'))
        return "cloud_gaming_menu"

    def _toggle(self):
        cg = self.game_state.cloud_gaming
        cg.active = not cg.active
        self.audio.speak(self.game_state.get_text('cloud_gaming_stopped', default='Dienst gestoppt.'))
        return "cloud_gaming_menu"

    def _price_up(self):
        cg = self.game_state.cloud_gaming
        cg.price += 1.0
        self.audio.speak(self.game_state.get_text('price_changed', default='Preis geaendert.'))
        return "cloud_gaming_menu"

    def _price_down(self):
        cg = self.game_state.cloud_gaming
        if cg.price > 1.0:
            cg.price -= 1.0
        self.audio.speak(self.game_state.get_text('price_changed', default='Preis geaendert.'))
        return "cloud_gaming_menu"

    def _upgrade(self):
        cg = self.game_state.cloud_gaming
        cost = cg.tech_level * 5000000
        if self.game_state.money >= cost:
            self.game_state.money -= cost
            cg.tech_level += 1
            cg.server_cost_per_sub = max(0.5, cg.server_cost_per_sub - 0.2)
            self.audio.speak(self.game_state.get_text('cloud_gaming_upgraded', default='Serverkapazitaet verbessert!'))
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money'))
        return "cloud_gaming_menu"


class MetaverseMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("AudioVerse", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        gs = self.game_state
        
        if getattr(gs, 'metaverse_burst', False):
            self.title = "AudioVerse (OFFLINE)"
            self.options.append({'text': "Das AudioVerse ist gecrasht. Geld ist weg.", 'action': lambda: "service_menu"})
            return
            
        self.title = f"AudioVerse (Investiert: ${gs.metaverse_investment:,.0f} | Wert: ${gs.metaverse_land_value:,.0f})"
        
        # Investieren
        if gs.money >= 500000:
            self.options.append({'text': "Investiere $500k in AudioVerse-Land", 'action': self._invest})
        
        # Verkaufen
        if gs.metaverse_land_value > 0:
            self.options.append({'text': f"Alles verkaufen (Gewinn mitnehmen)", 'action': self._sell})
            
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "service_menu"})

    def _invest(self):
        gs = self.game_state
        if gs.money >= 500000:
            gs.money -= 500000
            gs.track_expense("metaverse", 500000)
            gs.metaverse_investment += 500000
            gs.metaverse_land_value += 500000
            self.audio.play_sound("buy")
            self._update_options()
        return "metaverse_menu"

    def _sell(self):
        gs = self.game_state
        if gs.metaverse_land_value > 0:
            gs.money += gs.metaverse_land_value
            gs.metaverse_investment = 0
            gs.metaverse_land_value = 0
            gs.metaverse_weeks_active = 0
            self.audio.play_sound("money")
            self._update_options()
        return "metaverse_menu"


class TransmediaMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Transmedia Empire (Film & Serien)", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options.clear()
        
        # Only show games with IP rating > 40 and no existing movie deal
        eligible_games = [g for g in self.game_state.game_history if g.ip_rating >= 40 and not getattr(g, "has_movie_deal", False)]
        
        for g in eligible_games:
            self.options.append({
                'text': f"{g.name} (IP: {g.ip_rating})",
                'action': lambda game=g: self._select_game(game)
            })
            
        if not eligible_games:
            self.options.append({
                'text': "Keine geeigneten IPs (IP-Rating > 40 & noch keine Adaption) verfuegbar.",
                'action': lambda: None
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "business_menu"})

    def _select_game(self, game):
        # We need to set up the deal context
        self.game_state.selected_transmedia_game = game
        return "transmedia_deal_menu"


class TransmediaDealMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        game = getattr(self.game_state, "selected_transmedia_game", None)
        title = f"Transmedia Deal für {game.name}" if game else "Transmedia Deal"
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options.clear()
        game = getattr(self.game_state, "selected_transmedia_game", None)
        
        if not game:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "transmedia_menu"})
            return
            
        import random
        
        # Movie Deal
        movie_offer = 5000000 + (game.ip_rating * 100000)
        self.options.append({
            'text': f"Kino-Film Deal ({movie_offer:,} EUR Vorschuss)",
            'action': lambda: self._sign_deal(game, movie_offer, "Kino")
        })
        
        # Series Deal (Netflix style) unlocks later (2012)
        if self.game_state.get_calendar_year() >= 2012:
            series_offer = 3000000 + (game.ip_rating * 150000)
            self.options.append({
                'text': f"Streaming-Serie Deal ({series_offer:,} EUR Vorschuss)",
                'action': lambda: self._sign_deal(game, series_offer, "Streaming")
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "transmedia_menu"})

    def _sign_deal(self, game, upfront, deal_type):
        import random
        
        self.game_state.money += upfront
        game.has_movie_deal = True
        
        # Simulate massive sales boost based on deal type
        hit_chance = 0.7 if deal_type == "Streaming" else 0.5
        
        if random.random() < hit_chance:
            # Massive Hit! Reactivate game if inactive, or just boost stats massively
            bonus_sales = random.randint(500000, 2000000)
            bonus_revenue = bonus_sales * 25 # Assuming 25 per copy
            game.sales += bonus_sales
            game.revenue += bonus_revenue
            game.ip_rating += random.randint(10, 30)
            
            # Optionally reactivate the game
            game.is_active = True
            game.weeks_on_market = max(1, game.weeks_on_market)
            
            self.audio.play_sound('cash')
            self.audio.speak(f"Ein gigantischer Hit! Die {deal_type}-Adaption treibt die Verkufe von {game.name} durch die Decke! (+{bonus_sales:,} Sales)")
        else:
            # Flop, just minor boost
            bonus_sales = random.randint(10000, 50000)
            game.sales += bonus_sales
            game.revenue += bonus_sales * 25
            game.ip_rating -= random.randint(1, 5)
            self.audio.play_sound('error')
            self.audio.speak(f"Die {deal_type}-Adaption war ein Flop bei den Kritikern. Die Fans sind enttuscht. (+{bonus_sales:,} Sales)")
            
        return "transmedia_menu"
