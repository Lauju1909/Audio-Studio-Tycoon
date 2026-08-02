from models import Email

class StockManager:
    def __init__(self):
        self.is_public = False
        self.shareholder_trust = 100.0
        self.owned_shares_percent = 100.0
        self.quarters_public = 0
        self.last_quarter_money = 0
        self.earnings_call_weeks_left = 12
        self.target_profit = 0

    def to_dict(self):
        return {
            "is_public": self.is_public,
            "shareholder_trust": self.shareholder_trust,
            "owned_shares_percent": self.owned_shares_percent,
            "quarters_public": self.quarters_public,
            "last_quarter_money": self.last_quarter_money,
            "earnings_call_weeks_left": self.earnings_call_weeks_left,
            "target_profit": self.target_profit
        }

    def from_dict(self, data):
        if not data: return
        self.is_public = data.get("is_public", False)
        self.shareholder_trust = data.get("shareholder_trust", 100.0)
        self.owned_shares_percent = data.get("owned_shares_percent", 100.0)
        self.quarters_public = data.get("quarters_public", 0)
        self.last_quarter_money = data.get("last_quarter_money", 0)
        self.earnings_call_weeks_left = data.get("earnings_call_weeks_left", 12)
        self.target_profit = data.get("target_profit", 0)

    def go_public(self, game_state, payout):
        self.is_public = True
        self.owned_shares_percent = 51.0 # Sold 49%
        self.shareholder_trust = 100.0
        self.earnings_call_weeks_left = 12
        self.last_quarter_money = game_state.money + payout
        self.target_profit = payout * 0.05 # 5% profit expected next quarter
        
        game_state.track_income("other", payout)

    def tick(self, game_state):
        if not self.is_public:
            return
            
        self.earnings_call_weeks_left -= 1
        
        if self.earnings_call_weeks_left <= 0:
            self._hold_earnings_call(game_state)

    def _hold_earnings_call(self, game_state):
        profit = game_state.money - self.last_quarter_money
        
        if profit >= self.target_profit:
            self.shareholder_trust = min(100.0, self.shareholder_trust + 15)
            game_state.emails.insert(0, Email(
                game_state.get_text("sender_board", default="Board of Directors"),
                game_state.get_text("shareholder_happy_subject", default="Earnings Call: Target Met"),
                game_state.get_text("shareholder_happy", default="Shareholders are happy! Revenue targets met. (+15 Trust)"),
                game_state.week
            ))
        else:
            self.shareholder_trust = max(0.0, self.shareholder_trust - 25)
            game_state.emails.insert(0, Email(
                game_state.get_text("sender_board", default="Board of Directors"),
                game_state.get_text("shareholder_angry_subject", default="Earnings Call: Target Missed!"),
                game_state.get_text("shareholder_angry", default="Shareholders are furious! Targets missed. (-25 Trust)"),
                game_state.week
            ))
            
        if self.shareholder_trust <= 0:
            # Game Over Event
            game_state.game_over = True
            game_state.game_over_reason = game_state.get_text("shareholder_fired", default="You have been fired by the board of directors! GAME OVER.")
            
        self.quarters_public += 1
        self.last_quarter_money = game_state.money
        self.target_profit = max(500000, game_state.money * 0.02) # expect 2% return minimum
        self.earnings_call_weeks_left = 12

    def pay_dividend(self, game_state, amount):
        if game_state.money >= amount:
            game_state.track_expense("other", amount)
            boost = (amount / max(1, self.target_profit)) * 10
            self.shareholder_trust = min(100.0, self.shareholder_trust + boost)
            return True, game_state.get_text("dividend_paid_success", default=f"Dividend paid! Trust increased by {boost:.1f}%")
        return False, game_state.get_text("not_enough_money", default="Not enough money!")

    def buyback_shares(self, game_state):
        if self.owned_shares_percent >= 100.0:
            return False, "Already own 100% of the company."
            
        # 1% costs heavily:
        cost = max(1000000, int((game_state.fans * 100 + game_state.money) * 0.01))
        if game_state.money >= cost:
            game_state.track_expense("other", cost)
            self.owned_shares_percent += 1.0
            if self.owned_shares_percent >= 100.0:
                self.owned_shares_percent = 100.0
                self.is_public = False # Privatized!
                return True, game_state.get_text("company_privatized", default="Company successfully privatized! We are independent again.")
            return True, game_state.get_text("shares_bought_back", default=f"Bought back 1% of shares for {cost} EUR.")
            
        return False, game_state.get_text("not_enough_money", default="Not enough money!")
