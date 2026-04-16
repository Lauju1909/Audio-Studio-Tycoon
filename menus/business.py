from .base import Menu, TextInputMenu
import random

class ServiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('service_menu')
        options = [
            {'text': self.game_state.get_text('game_service_options'), 'action': lambda: "game_service_options"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]
        super().__init__(title, options, audio, game_state)

class GameServiceOptionsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('game_service_options'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"}
        ]

class BankMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('bank_menu')
        options = [
            {'text': self.game_state.get_text('loans'), 'action': lambda: "loan_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]
        super().__init__(title, options, audio, game_state)

class LoanMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('loan_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        from models import BankLoan
        self.options = [
            {'text': self.game_state.get_text('loan_50k'), 'action': lambda: self._take(50000, 0.05)},
            {'text': self.game_state.get_text('loan_100k'), 'action': lambda: self._take(100000, 0.07)},
            {'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"}
        ]

    def _take(self, amount, rate):
        from models import BankLoan
        if self.game_state.bank_loan:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('loan_already_active'))
            return None
        self.game_state.bank_loan = BankLoan(amount, rate, 52) # 1 Jahr Laufzeit
        self.game_state.money += amount
        self.audio.play_sound("confirm")
        return "game_menu"

class StockMarketMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('stock_market_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for idx, rival in enumerate(self.game_state.rivals):
             shares = getattr(rival, 'owned_shares', 0)
             price = self.game_state.get_share_price(rival)
             text = self.game_state.get_text('stock_share_info', name=rival.name, shares=shares, price=price)
             self.options.append({'text': text, 'action': lambda i=idx: self._select_rival(i)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})

    def _select_rival(self, idx):
        self.game_state._pending_rival_idx = idx
        return "stock_rival_detail"

class StockRivalDetailMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        idx = getattr(self.game_state, '_pending_rival_idx', 0)
        rival = self.game_state.rivals[idx]
        title = f"{rival.name} - {self.game_state.get_text('stock_market_menu')}"
        options = [
            {'text': self.game_state.get_text('stock_buy_10'), 'action': lambda: self._buy(idx)},
            {'text': self.game_state.get_text('stock_sell_10'), 'action': lambda: self._sell(idx)},
            {'text': self.game_state.get_text('back'), 'action': lambda: "stock_market_menu"}
        ]
        super().__init__(title, options, audio, game_state)

    def _buy(self, idx):
        success, msg = self.game_state.buy_shares(idx)
        if success:
            self.audio.play_sound("confirm")
            return "stock_market_menu"
        else:
            if msg == "max_shares":
                self.audio.speak(self.game_state.get_text('stock_max_shares'))
            elif msg == "no_money":
                self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

    def _sell(self, idx):
        success, msg = self.game_state.sell_shares(idx)
        if success:
            self.audio.play_sound("confirm")
            return "stock_market_menu"
        else:
            if msg == "no_shares":
                self.audio.speak(self.game_state.get_text('stock_no_shares'))
            return None

class LicenseShopMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('license_shop_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        available = self.game_state.get_available_licenses()
        for idx, lic in enumerate(available):
            text = self.game_state.get_text('license_info', name=lic['name'], bonus=lic['hype_bonus'], cost=lic['base_cost'])
            self.options.append({'text': text, 'action': lambda i=idx: self._buy(i)})
        
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_licenses_available'), 'action': lambda: "game_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _buy(self, idx):
        available = self.game_state.get_available_licenses()
        if 0 <= idx < len(available):
            lic = available[idx]
            if self.game_state.buy_license(lic):
                self.audio.play_sound("confirm")
                self.audio.speak(self.game_state.get_text('license_buy_confirm', name=lic['name'], cost=lic['base_cost']))
                return "license_shop_menu"
            else:
                self.audio.speak(self.game_state.get_text('not_enough_money'))
        return None

class LicenseSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('license_select_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [{'text': self.game_state.get_text('no_license'), 'action': lambda: "genre_menu"}]
        
        unused = self.game_state.get_unused_licenses()
        for lic in unused:
             self.options.append({
                 'text': f"{lic['name']} (+{lic['hype_bonus']} Hype)", 
                 'action': lambda name=lic['name']: self._select(name)
             })
             
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select(self, name):
        if self.game_state.use_license(name):
             self.audio.play_sound("confirm")
             return "genre_menu"
        return None

class AddonMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('addon_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        # Nur Spiele, die bereits veröffentlicht sind
        for idx, game in enumerate(self.game_state.game_history):
             self.options.append({
                 'text': game.name, 
                 'action': lambda i=idx: self._select_base(i)
             })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select_base(self, idx):
        self.game_state._pending_addon_base_idx = idx
        return "addon_name_input"

class AddonNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('addon_name_title', 'addon_name_prompt', audio, game_state,
                         on_confirm=self._confirm, on_cancel=lambda: "addon_menu")

    def _confirm(self, name):
        idx = getattr(self.game_state, '_pending_addon_base_idx', 0)
        base_game = self.game_state.game_history[idx]
        if self.game_state.create_addon(idx, name, base_game.topic, base_game.genre):
             self.audio.play_sound("confirm")
             return "game_menu"
        else:
             self.audio.speak(self.game_state.get_text('not_enough_money'))
             return None

class BundleMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('bundle_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        # Bundle Logic: Wähle 3 Spiele
        if not hasattr(self.game_state, '_pending_bundle_indices'):
            self.game_state._pending_bundle_indices = []
            
        for idx, game in enumerate(self.game_state.game_history):
             prefix = "[X] " if idx in self.game_state._pending_bundle_indices else "[ ] "
             self.options.append({
                 'text': prefix + game.name, 
                 'action': lambda i=idx: self._toggle_game(i)
             })
             
        if len(self.game_state._pending_bundle_indices) >= 2:
            self.options.insert(0, {'text': self.game_state.get_text('bundle_create_confirm'), 'action': lambda: "bundle_name_input"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': self._cancel})

    def _toggle_game(self, idx):
        if idx in self.game_state._pending_bundle_indices:
            self.game_state._pending_bundle_indices.remove(idx)
        else:
            if len(self.game_state._pending_bundle_indices) < 3:
                self.game_state._pending_bundle_indices.append(idx)
            else:
                self.audio.speak(self.game_state.get_text('bundle_max_reached'))
        return "bundle_menu"

    def _cancel(self):
        self.game_state._pending_bundle_indices = []
        return "game_menu"

class BundleNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('bundle_name_title', 'bundle_name_prompt', audio, game_state,
                         on_confirm=self._confirm, on_cancel=lambda: "bundle_menu")

    def _confirm(self, name):
        indices = getattr(self.game_state, '_pending_bundle_indices', [])
        if self.game_state.create_bundle(name, indices):
             self.audio.play_sound("confirm")
             self.game_state._pending_bundle_indices = []
             return "game_menu"
        else:
             self.audio.speak(self.game_state.get_text('not_enough_money'))
             return None

class ProductionMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('production_menu_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        # Check for games that can be produced
        active_games = [g for g in self.game_state.game_history if getattr(g, 'is_active', True)]
        for idx, game in enumerate(active_games):
             self.options.append({
                 'text': self.game_state.get_text('production_prompt_short', name=game.name),
                 'action': lambda g=game: self.select_game(g)
             })
        
        self.options.append({'text': self.game_state.get_text('build_presswerk_option'), 'action': self._build_presswerk})
        self.options.append({'text': self.game_state.get_text('expand_storage_option'), 'action': self._expand_storage})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        super().announce_entry()

    def select_game(self, game):
        self.game_state._pending_production_game = game
        return "production_amount_menu"

    def _build_presswerk(self):
        success, msg = self.game_state.build_presswerk()
        if success:
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('presswerk_success'))
            return "production_menu"
        else:
            if msg == "office_too_small":
                self.audio.speak(self.game_state.get_text('presswerk_fail_office_small'))
            elif msg == "no_money":
                self.audio.speak(self.game_state.get_text('presswerk_fail_no_money'))
            return None

    def _expand_storage(self):
        success, msg = self.game_state.expand_storage()
        if success:
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('storage_expand_success'))
            return "production_menu"
        else:
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

class ProductionAmountMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('production_amount_title', 'production_amount_prompt', audio, game_state,
                         on_confirm=self._confirm, on_cancel=lambda: "production_menu")
        self.is_numeric = True

    def _confirm(self, amount_str):
        try:
            amount = int(amount_str)
            if amount <= 0: raise ValueError
        except ValueError:
            self.audio.speak(self.game_state.get_text('invalid_amount'))
            return None

        game = getattr(self.game_state, '_pending_production_game', None)
        if not game: return "production_menu"

        try:
            idx = self.game_state.game_history.index(game)
        except ValueError:
            return "production_menu"

        success, msg = self.game_state.produce_copies(idx, amount)
        
        if success:
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('production_success', amount=amount))
            return "production_menu"
        else:
            if msg == "no_money":
                self.audio.speak(self.game_state.get_text('production_fail_no_money'))
            elif msg == "no_storage":
                self.audio.speak(self.game_state.get_text('production_fail_no_storage'))
            elif msg == "no_presswerk":
                self.audio.speak(self.game_state.get_text('production_fail_no_presswerk'))
            return None

class MMOPaymentMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('mmo_payment_menu'), [], audio, game_state)

class MMOManagementMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('mmo_management_menu'), [], audio, game_state)

class MMOOptionsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('mmo_options_menu'), [], audio, game_state)

class PublisherDealsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('publisher_deals_menu'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        deals = getattr(self.game_state, 'publishing_offers', [])
        for idx, deal in enumerate(deals):
            self.options.append({
                'text': f"{deal.studio_name}: {deal.game_name} ({deal.genre})",
                'action': lambda i=idx: self.select_deal(i)
            })
            
        if not self.options:
            self.options.append({'text': self.game_state.get_text('publisher_deals_empty'), 'action': lambda: "game_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        super().announce_entry()

    def select_deal(self, idx):
        self.game_state._pending_deal_idx = idx
        return "publisher_deal_details"

class PublisherDealDetailsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('publisher_deal_details_menu'), [], audio, game_state)

    def announce_entry(self):
        idx = getattr(self.game_state, '_pending_deal_idx', -1)
        deals = getattr(self.game_state, 'publishing_offers', [])
        if 0 <= idx < len(deals):
            offer = deals[idx]
            self.title = self.game_state.get_text('publisher_deal_info', 
                studio=offer.studio_name, game=offer.game_name, genre=offer.genre, 
                quality=offer.quality, cost=offer.marketing_cost, share=int(offer.player_share * 100))
            
            self.options = [
                {'text': self.game_state.get_text('publisher_deal_accept'), 'action': lambda: self.accept_deal(idx)},
                {'text': self.game_state.get_text('publisher_deal_reject'), 'action': lambda: self.reject_deal(idx)},
                {'text': self.game_state.get_text('back'), 'action': lambda: "publisher_deals_menu"}
            ]
        super().announce_entry()

    def accept_deal(self, idx):
        success, msg = self.game_state.accept_publishing_offer(idx)
        if success:
            self.audio.play_sound("confirm")
            return "game_menu"
        else:
            if msg == "not_enough_money":
                self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

    def reject_deal(self, idx):
        self.game_state.reject_publishing_offer(idx)
        return "publisher_deals_menu"

class MerchMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('merch_menu_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        from game_data import MERCH_TYPES
        for idx, merch in enumerate(MERCH_TYPES):
            self.options.append({
                'text': self.game_state.get_text('merch_produce_option', name=merch['name'], cost=merch['production_cost']),
                'action': lambda i=idx: self.select_merch(i)
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        super().announce_entry()
        
    def select_merch(self, idx):
        self.game_state._pending_merch_idx = idx
        return "merch_amount_menu"

class MerchAmountMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('merch_menu_title', 'merch_produce_prompt', audio, game_state,
                         on_confirm=self._confirm, on_cancel=lambda: "merch_menu")
        self.is_numeric = True
        
    def announce_entry(self):
        idx = getattr(self.game_state, '_pending_merch_idx', -1)
        if idx != -1:
            from game_data import MERCH_TYPES
            merch = MERCH_TYPES[idx]
            stock = 0
            for m in self.game_state.active_merch:
                if m["name"] == merch["name"]:
                    stock = m["stock"]
                    break
            
            self.prompt_text = self.game_state.get_text(
                'merch_produce_prompt', 
                name=merch['name'], 
                stock=f"{stock:,}",
                cost=merch['production_cost'],
                storage=f"{self.game_state.storage_capacity - self.game_state.used_storage:,}"
            )
        super().announce_entry()

    def _confirm(self, amount_str):
        try:
            amount = int(amount_str)
            if amount <= 0: raise ValueError
        except ValueError:
            self.audio.speak(self.game_state.get_text('invalid_amount'))
            return None
            
        idx = getattr(self.game_state, '_pending_merch_idx', -1)
        if idx != -1:
            from game_data import MERCH_TYPES
            merch = MERCH_TYPES[idx]
            total_cost = amount * merch['production_cost']
            
            if self.game_state.money < total_cost:
                self.audio.speak(self.game_state.get_text('merch_fail_money'))
                return None
                
            if self.game_state.used_storage + amount > self.game_state.storage_capacity:
                self.audio.speak(self.game_state.get_text('merch_fail_storage', storage=f"{self.game_state.storage_capacity - self.game_state.used_storage:,}"))
                return None
                 
            self.game_state.money -= total_cost
            self.game_state.used_storage += amount
            
            found = False
            for m in self.game_state.active_merch:
                if m["name"] == merch["name"]:
                    m["stock"] += amount
                    found = True
                    break
            
            if not found:
                new_merch = dict(merch)
                new_merch["stock"] = amount
                new_merch["sales"] = 0
                new_merch["revenue"] = 0
                self.game_state.active_merch.append(new_merch)
                
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('merch_success', amount=amount, name=merch['name']))
            
        return "merch_menu"

class ESportsMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('esports_menu_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        from game_data import ESPORTS_TOURNAMENTS
        for idx, t in enumerate(ESPORTS_TOURNAMENTS):
            self.options.append({
                'text': self.game_state.get_text('esports_host_option', name=t['name'], cost=t['cost']),
                'action': lambda i=idx: self.host_tournament(i)
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        super().announce_entry()
        
    def host_tournament(self, idx):
        from game_data import ESPORTS_TOURNAMENTS
        t = ESPORTS_TOURNAMENTS[idx]
        
        if self.game_state.money < t['cost']:
            self.audio.speak(self.game_state.get_text('esports_fail_money', cost=t['cost']))
            return None
            
        best_sales = 0
        for g in self.game_state.game_history:
            if getattr(g, 'sales', 0) > best_sales:
                best_sales = g.sales
        for m in getattr(self.game_state, 'active_mmos', []):
            if m.game.sales > best_sales:
                best_sales = m.game.sales
                
        if best_sales < t['min_game_sales']:
             self.audio.speak(self.game_state.get_text('esports_fail_sales', sales=t['min_game_sales']))
             return None
             
        self.game_state.money -= t['cost']
        self.game_state.hype = min(250, self.game_state.hype + t['hype_bonus'])
        self.game_state.fans += t['fan_bonus']
        
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('esports_success', name=t['name'], hype=t['hype_bonus'], fans=t['fan_bonus']))
        return "esports_menu"

class AcquisitionMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('acquisition_menu_title'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        for idx, rival in enumerate(self.game_state.rivals):
            if getattr(rival, 'is_owned_by_player', False):
                continue
                
            buyout_cost = (100 - getattr(rival, 'owned_shares', 0)) * 50000 
            
            self.options.append({
                'text': self.game_state.get_text('acquisition_option', name=rival.name, cost=buyout_cost, shares=getattr(rival, 'owned_shares', 0)),
                'action': lambda i=idx, cost=buyout_cost: self.acquire_studio(i, cost)
            })
            
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_studios_available'), 'action': lambda: "bank_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})
        super().announce_entry()
        
    def acquire_studio(self, idx, cost):
        rival = self.game_state.rivals[idx]
        shares = getattr(rival, 'owned_shares', 0)
        
        if shares < 50:
            self.audio.speak(self.game_state.get_text('acquisition_need_shares'))
            return None
            
        if self.game_state.money < cost:
            self.audio.speak(self.game_state.get_text('acquisition_fail_money', cost=cost))
            return None
            
        self.game_state.money -= cost
        rival.is_owned_by_player = True
        rival.owned_shares = 100
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('acquisition_success', name=rival.name))
        return "bank_menu"
