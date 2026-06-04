from .base import Menu, TextInputMenu
import random
import webbrowser
import urllib.parse

class ServiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('service_menu')
        options = []
        if self.game_state.get_calendar_year() >= 2000:
            options.append({'text': self.game_state.get_text('service_manage_subscription'), 'action': lambda: "subscription_service_menu"})
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

class SubscriptionServiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('subscription_menu_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        self.options = []
        if getattr(gs, 'subscription_active', False):
            
            self.options.append({'text': gs.get_text('subscription_add_game'), 'action': lambda: "subscription_add_game_menu"})
            self.options.append({'text': gs.get_text('subscription_stop') + f" ({int(gs.subscription_subscribers):,} Abonnenten)", 'action': self._toggle})
            self.options.append({'text': gs.get_text('subscription_price_up', price=gs.subscription_price), 'action': self._change_price})
            self.options.append({'text': gs.get_text('subscription_price_down', price=gs.subscription_price), 'action': self._change_price_down})
        else:
            self.options.append({'text': gs.get_text('subscription_start', cost=50000), 'action': self._toggle})
        
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "service_menu"})

    def _toggle(self):
        gs = self.game_state
        if getattr(gs, 'subscription_active', False):
            gs.subscription_active = False
            self.audio.play_sound("error")
        else:
            if gs.money >= 50000:
                gs.track_expense("staff", 50000)
                gs.subscription_active = True
                gs.subscription_hype = 10.0
                self.audio.play_sound("cash")
            else:
                self.audio.play_sound("error")
                self.audio.speak(gs.get_text('not_enough_money'))
        self._update_options()
        return None

    def _change_price(self):
        gs = self.game_state
        gs.subscription_price += 1.0
        if gs.subscription_price > 25.0:
            gs.subscription_price = 5.0
        self.audio.play_sound("click")
        self._update_options()
        return None

    def _change_price_down(self):
        gs = self.game_state
        gs.subscription_price -= 1.0
        if gs.subscription_price < 5.0:
            gs.subscription_price = 25.0
        self.audio.play_sound("click")
        self._update_options()
        return None

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

class BankMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('bank_menu')
        options = [
            {'text': self.game_state.get_text('bank_statement_option'), 'action': self._show_report},
            {'text': self.game_state.get_text('loans'), 'action': lambda: "loan_menu"},
            {'text': self.game_state.get_text('donate_menu'), 'action': lambda: "donation_menu"},
            {'text': self.game_state.get_text('menu_monetization'), 'action': lambda: "monetization_menu"}
        ]
        if not getattr(self.game_state, 'is_public_company', False) and self.game_state.money >= 10000000 and self.game_state.fans >= 1000000:
            options.insert(1, {'text': self.game_state.get_text('ipo_option', default='Boersengang (IPO) planen'), 'action': lambda: "ipo_menu"})
            
        options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        super().__init__(title, options, audio, game_state)

    def _show_report(self):
        report = self.game_state.get_financial_report()
        self.audio.speak(report)
        return None

class LoanMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('loan_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        from models import BankLoan
        if self.game_state.bank_loan:
            loan = self.game_state.bank_loan
            self.options = [
                {
                    'text': self.game_state.get_text(
                        'active_loan_info',
                        amount_remaining=loan.amount_remaining,
                        weeks_remaining=loan.weeks_remaining,
                        weekly_payment=loan.weekly_payment
                    ),
                    'action': lambda: self.audio.speak(
                        self.game_state.get_text(
                            'active_loan_info',
                            amount_remaining=self.game_state.bank_loan.amount_remaining,
                            weeks_remaining=self.game_state.bank_loan.weeks_remaining,
                            weekly_payment=self.game_state.bank_loan.weekly_payment
                        )
                    )
                },
                {
                    'text': self.game_state.get_text('pay_loan_option', amount=loan.amount_remaining),
                    'action': self._repay_loan
                },
                {'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"}
            ]
        else:
            self.options = [
                {'text': self.game_state.get_text('loan_50k'), 'action': lambda: self._take(50000, self.game_state.interest_rate)},
                {'text': self.game_state.get_text('loan_100k'), 'action': lambda: self._take(100000, self.game_state.interest_rate + 0.02)},
                {'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"}
            ]

    def _take(self, amount, rate):
        from models import BankLoan
        if self.game_state.bank_loan:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('loan_already_active'))
            return None
        from game_data import WEEKS_PER_YEAR
        self.game_state.bank_loan = BankLoan(amount, rate, WEEKS_PER_YEAR) # 1 Jahr Laufzeit
        self.game_state.track_income("other", amount)
        self.audio.play_sound("confirm")
        self._update_options()
        self.current_index = 0
        return "game_menu"

    def _repay_loan(self):
        loan = self.game_state.bank_loan
        if not loan:
            self.audio.play_sound("error")
            return None
        amount_to_pay = loan.amount_remaining
        if self.game_state.money >= amount_to_pay:
            self.game_state.money -= amount_to_pay
            self.game_state.track_expense("loan_repayment", amount_to_pay)
            self.game_state.accounting["loan_paid"] += amount_to_pay
            self.game_state.bank_loan = None
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('loan_paid_off'))
            self._update_options()
            self.current_index = 0
            return None
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money_loan', amount=amount_to_pay))
            return None

class DonationMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('donate_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        self.options = [
            {'text': gs.get_text('donate_option', amount=1000), 'action': lambda: self._donate(1000)},
            {'text': gs.get_text('donate_option', amount=10000), 'action': lambda: self._donate(10000)},
            {'text': gs.get_text('donate_option', amount=100000), 'action': lambda: self._donate(100000)},
            {'text': gs.get_text('back'), 'action': lambda: "bank_menu"}
        ]

    def _donate(self, amount):
        success, fans = self.game_state.donate(amount)
        if success:
            self.audio.play_sound("cash")
            self.audio.speak(self.game_state.get_text('donate_success', amount=amount, fans=fans))
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('donate_not_enough'))
        return None

class MonetizationMenu(Menu):
    def __init__(self, audio, game_state, back_target=None, show_ads=True):
        self.audio = audio
        self.game_state = game_state
        self.show_ads = show_ads
        if back_target:
            self.game_state.monetization_back_target = back_target
        self.back_target = self.game_state.monetization_back_target
        
        title_key = 'menu_monetization' if show_ads else 'menu_support_dev'
        super().__init__(self.game_state.get_text(title_key), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        self.options = []
        
        if self.show_ads:
            self.options.append({'text': gs.get_text('watch_ad'), 'action': self._watch_ad})
        
        self.options.extend([
            {'text': gs.get_text('support_gift_card'), 'action': lambda: "support_gift_card_type_menu"},
            {'text': gs.get_text('support_dev'), 'action': self._support_dev},
            {'text': gs.get_text('back'), 'action': lambda: self.back_target}
        ])

    def _watch_ad(self):
        if self.game_state.week <= self.game_state.last_ad_week:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('ad_cooldown'))
            return None

        self.audio.speak(self.game_state.get_text('ad_playing'))
        import time
        self.audio.play_sound("cash")
        
        success, amount = self.game_state.watch_ad()
        if success:
            self.audio.speak(self.game_state.get_text('ad_reward_received', amount=amount))
            self.audio.play_sound("confirm")
        return self.back_target

    def _support_dev(self):
        self.audio.speak(self.game_state.get_text('support_dev'))
        webbrowser.open("https://github.com/Lauju1909") 
        return None

class SupportGiftCardTypeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('support_gift_card_title'), [], audio, game_state)
        self.description = self.game_state.get_text('support_gift_card_desc')
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        self.options = [
            {'text': gs.get_text('support_gift_card_google'), 'action': lambda: self._start_input(gs.get_text('support_gift_card_google'))},
            {'text': gs.get_text('support_gift_card_steam'), 'action': lambda: self._start_input(gs.get_text('support_gift_card_steam'))},
            {'text': gs.get_text('support_gift_card_paysafe'), 'action': lambda: self._start_input(gs.get_text('support_gift_card_paysafe'))},
            {'text': gs.get_text('back'), 'action': lambda: "current_monetization_menu"}
        ]

    def _start_input(self, card_type):
        return GiftCardCodeInput(self.audio, self.game_state, card_type)

class GiftCardCodeInput(TextInputMenu):
    def __init__(self, audio, game_state, card_type):
        self.card_type = card_type
        super().__init__(
            'support_gift_card_title',
            'support_gift_card_prompt',
            audio, game_state,
            on_confirm=self._on_confirm,
            on_cancel=lambda: "support_gift_card_type_menu"
        )

    def _on_confirm(self, code):
        self.audio.speak(self.game_state.get_text('support_gift_card_thanks'))
        
        subject = self.game_state.get_text('support_gift_card_mail_subject')
        body = self.game_state.get_text('support_gift_card_mail_body', type=self.card_type, code=code)
        
        # URL encode for mailto
        subject_enc = urllib.parse.quote(subject)
        body_enc = urllib.parse.quote(body)
        
        mailto_url = f"mailto:lauju1909@gmail.com?subject={subject_enc}&body={body_enc}"
        webbrowser.open(mailto_url)
        
        return "current_monetization_menu"

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
        self.options.append({'text': "Spionage & Sabotage (Neu)", 'action': lambda: "espionage_menu"})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})

    def _select_rival(self, idx):
        self.game_state._pending_rival_idx = idx
        return "stock_rival_detail"

class StockRivalDetailMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        idx = getattr(self.game_state, '_pending_rival_idx', None)
        if idx is None or idx < 0 or idx >= len(self.game_state.rivals):
            title = self.game_state.get_text('stock_market_menu')
            options = [{'text': self.game_state.get_text('back'), 'action': lambda: "stock_market_menu"}]
            super().__init__(title, options, audio, game_state)
            return
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
             return "main_menu"
        return "main_menu"

class EngineLicensingMenu(Menu):
    """MenÃ¼ zur Lizenzierung der eigenen Engines."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('engine_licensing_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for i, eng in enumerate(self.game_state.engines):
            status = "Lizenziert" if getattr(eng, "is_licensed", False) else "Nicht Lizenziert"
            fee = getattr(eng, "license_fee", 0)
            self.options.append({
                'text': f"{eng.name} - Status: {status} - GebÃ¼hr: {fee}",
                'action': lambda idx=i: self._select_engine(idx)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select_engine(self, idx):
        self.game_state.ui_context['selected_engine_idx'] = idx
        return "engine_license_fee_menu"

class EngineLicenseFeeMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('engine_licensing_title', 'engine_license_fee_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "engine_licensing_menu")

    def _on_confirm(self, text):
        try:
            fee = int(text)
            if fee < 0: raise ValueError
        except ValueError:
            if hasattr(self.audio, "speak"):
                self.audio.speak(self.game_state.get_text('invalid_number'))
            return None
        idx = self.game_state.ui_context.get('selected_engine_idx', -1)
        if 0 <= idx < len(self.game_state.engines):
            eng = self.game_state.engines[idx]
            eng.license_fee = fee
            eng.is_licensed = fee > 0
            if hasattr(self.audio, "speak"):
                if fee > 0:
                    self.audio.speak(self.game_state.get_text('engine_licensed', name=eng.name, fee=fee))
                else:
                    self.audio.speak(self.game_state.get_text('engine_unlicensed', name=eng.name))
        return "engine_licensing_menu"

class GamePortingMenu(Menu):
    """MenÃ¼ zur Portierung eines Spiels."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('game_porting_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        self.valid_games = [g for g in self.game_state.game_history if getattr(g, "is_active", False) or getattr(g, "weeks_on_market", 0) > 0]
        for g in self.valid_games:
            self.options.append({
                'text': f"{g.name} (Plattform: {self.game_state.get_text(g.platform)})",
                'action': lambda game_name=g.name: self._select_game(game_name)
            })
        if not self.valid_games:
            self.options.append({
                'text': self.game_state.get_text('no_games_available'),
                'action': None
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select_game(self, game_name):
        self.game_state.ui_context['port_game_name'] = game_name
        return "port_platform_menu"

class PortPlatformMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('port_platform_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        orig_name = self.game_state.ui_context.get('port_game_name')
        orig_game = next((g for g in self.game_state.game_history if g.name == orig_name), None)
        
        self.available_platforms = []
        if orig_game:
            for p in self.game_state.active_platforms:
                if p != orig_game.platform:
                    self.available_platforms.append(p)
            for c in getattr(self.game_state, "custom_consoles", []):
                if c.name != orig_game.platform:
                    self.available_platforms.append(c.name)
        
        for p in self.available_platforms:
            self.options.append({
                'text': self.game_state.get_text(p),
                'action': lambda plat=p: self._port(plat, orig_name)
            })
            
        if not self.available_platforms:
            self.options.append({
                'text': self.game_state.get_text('no_platforms_available'),
                'action': None
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_porting_menu"})

    def _port(self, platform, orig_name):
        # Start Port Project
        from models import PortProject
        dev_cost = 50000  # basis
        total_weeks = 4
        
        if not hasattr(self.game_state, "port_projects"):
            self.game_state.port_projects = []
        self.game_state.port_projects.append(PortProject(orig_name, platform, dev_cost, total_weeks))
        self.game_state.money -= dev_cost
        self.game_state.track_income("game_development", -dev_cost)
        
        if hasattr(self.audio, "speak"):
            self.audio.speak(self.game_state.get_text('port_project_started', name=orig_name, platform=self.game_state.get_text(platform)))
        return "main_menu"

class AddonMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('addon_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        # Nur Spiele, die bereits verÃ¶ffentlicht sind
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
        # Bundle Logic: WÃ¤hle 3 Spiele
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
        return "publisher_deal_details_menu"

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
                 
            self.game_state.track_expense("merch", total_cost)
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
            
        self.game_state.track_expense("other", cost)
        rival.is_owned_by_player = True
        rival.owned_shares = 100
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('acquisition_success', name=rival.name))
        return "bank_menu"


class SubscriptionVaultMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('subscription_vault_title'), [], audio, game_state)
    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        for g in self.game_state.game_history:
            if g.is_active and g not in getattr(self.game_state, 'subscription_games', []):
                self.options.append({
                    'text': self.game_state.get_text('subscription_put_in_vault', name=g.name),
                    'action': lambda g=g: self.add_game(g)
                })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "subscription_service_menu"})
        super().announce_entry()
        
    def add_game(self, g):
        if not hasattr(self.game_state, 'subscription_games'):
            self.game_state.subscription_games = []
        self.game_state.subscription_games.append(g)
        self.audio.speak(self.game_state.get_text('subscription_added_to_vault', name=g.name))
        return "subscription_service_menu"

class CreatorSponsorshipMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('creator_menu_title'), [], audio, game_state)
        
    def announce_entry(self):
        self.current_index = 0
        self.options = []
        from game_data import CONTENT_CREATORS
        for c in CONTENT_CREATORS:
            self.options.append({
                'text': self.game_state.get_text('creator_sponsor_option', name=self.game_state.get_text(c['name_key']), cost=c['cost']),
                'action': lambda c=c: self.sponsor(c)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "marketing_menu"})
        super().announce_entry()
        
    def sponsor(self, c):
        if self.game_state.money < c['cost']:
            self.audio.speak(self.game_state.get_text('creator_fail_money', cost=c['cost']))
            return None
        self.game_state.track_expense("marketing", c['cost'])
        self.game_state.add_sponsorship(c['boost'], c['duration'])
        self.audio.speak(self.game_state.get_text('creator_success', name=self.game_state.get_text(c['name_key'])))
        return "marketing_menu"

class IPOMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('ipo_title', default='Boersengang (IPO)'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        payout = int((self.game_state.fans * 10 + self.game_state.money) * 0.3)
        self.options.append({
            'text': self.game_state.get_text('ipo_confirm', payout=payout, default=f'An die Boerse gehen (Erloes: {payout} EUR)'),
            'action': lambda p=payout: self._go_public(p)
        })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "bank_menu"})

    def _go_public(self, payout):
        self.game_state.is_public_company = True
        self.game_state.shareholder_trust = 100
        self.game_state.money += payout
        self.game_state.shareholder_target = self.game_state.money * 1.10
        self.game_state.track_income("other", payout)
        self.audio.play_sound('cheer')
        self.audio.speak(self.game_state.get_text('ipo_success', default="Der Boersengang war ein voller Erfolg!"), interrupt=True)
        return "bank_menu"


class ESportsMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('esports_menu_title', default='E-Sports Zentrale'), [], audio, game_state)
    def announce_entry(self):
        self.options = []
        if self.game_state.year < 2010:
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
        from game_data import GENRES
        
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

