from ..base import Menu, TextInputMenu
import random
import webbrowser
import urllib.parse


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
            if self.game_state.is_feature_unlocked("ipo"):
                options.insert(1, {'text': self.game_state.get_text('ipo_option', default='Boersengang (IPO) planen'), 'action': lambda: "ipo_menu"})
            else:
                from game_data import FEATURE_UNLOCKS
                if "ipo" in FEATURE_UNLOCKS:
                    options.insert(1, {'text': f"{self.game_state.get_text('ipo_option', default='Boersengang (IPO) planen')} (Ab {FEATURE_UNLOCKS['ipo'].get('year', '???')}, Level {FEATURE_UNLOCKS['ipo'].get('office_level', '?')})", 'action': lambda: None})
            
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
