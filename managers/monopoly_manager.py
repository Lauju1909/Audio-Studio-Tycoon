import random
from models import Email

class MonopolyManager:
    def __init__(self):
        self.lobbying_weeks_left = 0
        self.anti_trust_fines_paid = 0
        
    def to_dict(self):
        return {
            "lobbying_weeks_left": self.lobbying_weeks_left,
            "anti_trust_fines_paid": self.anti_trust_fines_paid
        }
        
    def from_dict(self, data):
        if not data: return
        self.lobbying_weeks_left = data.get("lobbying_weeks_left", 0)
        self.anti_trust_fines_paid = data.get("anti_trust_fines_paid", 0)

    def get_market_share(self, game_state):
        # Base market share is 5%. Each subsidiary adds 8%.
        subsidiaries = [r for r in game_state.rivals if getattr(r, 'is_owned_by_player', False)]
        return 5.0 + (len(subsidiaries) * 8.0)
        
    def bribe_politicians(self, game_state):
        cost = 15000000 # 15 Mio EUR
        if game_state.money >= cost:
            game_state.track_expense("other", cost)
            self.lobbying_weeks_left += 26 # Half a year of immunity
            return True, "Lobby-Arbeit erfolgreich. Das Kartellamt schaut fuer 6 Monate weg!"
        return False, "Nicht genug Geld (15.000.000 EUR benoetigt)."
        
    def sell_subsidiary(self, game_state, sub_index):
        subsidiaries = [r for r in game_state.rivals if getattr(r, 'is_owned_by_player', False)]
        if len(subsidiaries) <= sub_index:
            return False, "Tochtergesellschaft nicht gefunden."
            
        sub = subsidiaries[sub_index]
        sub.is_owned_by_player = False
        sub.owned_shares = 0
        
        sell_price = random.randint(3000000, 8000000)
        game_state.track_income("other", sell_price)
        
        return True, f"{sub.name} wurde fuer {sell_price:,} EUR verkauft. Marktanteil sinkt!"
        
    def tick(self, game_state):
        subsidiaries = [r for r in game_state.rivals if getattr(r, 'is_owned_by_player', False)]
        if not subsidiaries:
            return
            
        # Passive income from subsidiaries
        total_income = len(subsidiaries) * random.randint(50000, 150000)
        game_state.track_income("other", total_income)
        
        # Kartellamt Logic
        market_share = self.get_market_share(game_state)
        
        if self.lobbying_weeks_left > 0:
            self.lobbying_weeks_left -= 1
            return
            
        if market_share >= 40.0:
            # 5% of cash or fixed fine, whichever is higher
            fine = max(2000000, int(game_state.money * 0.05))
            game_state.track_expense("other", fine)
            self.anti_trust_fines_paid += fine
            
            # Send warning email occasionally
            if random.random() < 0.2:
                game_state.emails.insert(0, Email(
                    "Kartellamt",
                    "Monopol-Strafe verhaengt",
                    f"Ihr Marktanteil von {market_share}% gefaehrdet den fairen Wettbewerb.\nWir haben eine Strafe von {fine:,} EUR abgebucht.\nLoesen Sie Ihre Tochtergesellschaften auf!",
                    game_state.week
                ))
