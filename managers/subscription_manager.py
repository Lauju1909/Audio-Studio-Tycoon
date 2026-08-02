
class SubscriptionManager:
    def __init__(self):
        self.is_active = False
        self.subscribers = 0
        self.monthly_fee = 9.99
        self.weeks_since_last_release = 0
        self.catalog = [] # List of game names added
        
    def to_dict(self):
        return {
            "is_active": self.is_active,
            "subscribers": self.subscribers,
            "monthly_fee": self.monthly_fee,
            "weeks_since_last_release": self.weeks_since_last_release,
            "catalog": self.catalog
        }
        
    def from_dict(self, data):
        if not data: return
        self.is_active = data.get("is_active", False)
        self.subscribers = data.get("subscribers", 0)
        self.monthly_fee = data.get("monthly_fee", 9.99)
        self.weeks_since_last_release = data.get("weeks_since_last_release", 0)
        self.catalog = data.get("catalog", [])
        
    def launch_service(self, game_state):
        cost = 5000000 # 5 Mio to start
        if game_state.money >= cost:
            game_state.track_expense("other", cost)
            self.is_active = True
            self.subscribers = int(game_state.fans * 0.05) # 5% of fans subscribe immediately
            return True, game_state.get_text("sub_launch_success", default="AudioPass erfolgreich gestartet!")
        return False, game_state.get_text("not_enough_money", default="Nicht genug Geld (5.000.000 EUR benoetigt).")
        
    def add_own_game(self, game_state, game):
        if game.name in self.catalog:
            return False, game_state.get_text("sub_already_in_catalog", default="Spiel ist bereits im AudioPass.")
        self.catalog.append(game.name)
        self.weeks_since_last_release = 0
        
        # Boost based on game review
        review = getattr(game.review, 'average', 50)
        boost = int((review * 1000) * (game_state.fans / 1000000 + 1))
        self.subscribers += boost
        return True, game_state.get_text("sub_game_added", name=game.name, boost=boost, default=f"{game.name} zum Katalog hinzugefuegt! {boost} neue Abonnenten.")

    def buy_third_party_game(self, game_state, rival_game):
        if rival_game.name in self.catalog:
            return False, game_state.get_text("sub_already_in_catalog", default="Spiel ist bereits im AudioPass.")
            
        cost = int(getattr(rival_game, 'total_sales', 0) * 10) # 10 EUR per sale as a licensing fee
        if game_state.money >= cost:
            game_state.track_expense("other", cost)
            self.catalog.append(rival_game.name)
            self.weeks_since_last_release = 0
            
            boost = int(getattr(rival_game, 'total_sales', 0) * 0.2) # 20% of buyers subscribe
            self.subscribers += boost
            return True, game_state.get_text("sub_third_party_added", name=rival_game.name, boost=boost, default=f"{rival_game.name} lizenziert! {boost} neue Abonnenten.")
            
        return False, game_state.get_text("not_enough_money_cost", cost=cost, default=f"Nicht genug Geld (Lizenkosten: {cost} EUR).")

    def tick(self, game_state):
        if not self.is_active:
            return
            
        self.weeks_since_last_release += 1
        
        # Churn rate: if no releases for > 12 weeks, churn increases
        churn_rate = 0.005 # base churn 0.5% per week
        if self.weeks_since_last_release > 12:
            churn_rate += 0.01 * ((self.weeks_since_last_release - 12) / 4) # +1% per month drought
            
        churn = int(self.subscribers * churn_rate)
        self.subscribers = max(0, self.subscribers - churn)
        
        # Income and server costs
        income = int((self.subscribers * self.monthly_fee) / 4) # weekly income
        server_cost = int(self.subscribers * 0.5 / 4) # 0.50 EUR per sub per month
        
        # Apply Real Estate Server Room perk
        if hasattr(game_state, "real_estate_manager"):
            rem = game_state.real_estate_manager
            if rem.active_property_index >= 0 and rem.active_property_index < len(rem.owned_properties):
                active_prop = rem.owned_properties[rem.active_property_index]
                if active_prop.has_server_room:
                    server_cost = int(server_cost * 0.5) # 50% discount
        
        if income > 0:
            game_state.track_income("other", income) # or new category 'subscription'
        if server_cost > 0:
            game_state.track_expense("other", server_cost)
