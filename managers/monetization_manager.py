import random
from models import Email

class MonetizationManager:
    def __init__(self):
        self.lootboxes_active = False
        self.battle_pass_active = False
        
        self.fan_trust = 100.0
        self.government_heat = 0.0
        
        self.pr_managers = 0
        self.ethics_managers = 0
        
    def to_dict(self):
        return {
            "lootboxes_active": self.lootboxes_active,
            "battle_pass_active": self.battle_pass_active,
            "fan_trust": self.fan_trust,
            "government_heat": self.government_heat,
            "pr_managers": self.pr_managers,
            "ethics_managers": self.ethics_managers
        }
        
    def from_dict(self, data):
        if not data: return
        self.lootboxes_active = data.get("lootboxes_active", False)
        self.battle_pass_active = data.get("battle_pass_active", False)
        self.fan_trust = data.get("fan_trust", 100.0)
        self.government_heat = data.get("government_heat", 0.0)
        self.pr_managers = data.get("pr_managers", 0)
        self.ethics_managers = data.get("ethics_managers", 0)
        
    def toggle_lootboxes(self):
        self.lootboxes_active = not self.lootboxes_active
        return self.lootboxes_active
        
    def toggle_battle_pass(self):
        self.battle_pass_active = not self.battle_pass_active
        return self.battle_pass_active
        
    def hire_pr_manager(self, game_state):
        cost = 100000
        if game_state.money >= cost:
            game_state.track_expense("staff", cost)
            self.pr_managers += 1
            return True, game_state.get_text("hire_pr_success", default="PR-Manager eingestellt! (Hilft gegen Shitstorms)")
        return False, game_state.get_text("not_enough_money_cost", cost=cost, default=f"Nicht genug Geld ({cost} EUR benoetigt).")
        
    def hire_ethics_manager(self, game_state):
        cost = 250000
        if game_state.money >= cost:
            game_state.track_expense("staff", cost)
            self.ethics_managers += 1
            return True, game_state.get_text("hire_ethics_success", default="Ethik-Manager eingestellt! (Reduziert Government Heat)")
        return False, game_state.get_text("not_enough_money_cost", cost=cost, default=f"Nicht genug Geld ({cost} EUR benoetigt).")

    def tick(self, game_state):
        # Salary for managers
        salary_cost = (self.pr_managers * 2000) + (self.ethics_managers * 5000)
        if salary_cost > 0:
            game_state.track_expense("staff", salary_cost)
            
        income = 0
        active_games = [g for g in game_state.game_history if getattr(g, 'sales', 0) > 0 and game_state.week - getattr(g, 'release_week', 0) < 104] # Games released in last 2 years
        
        if not active_games and (self.lootboxes_active or self.battle_pass_active):
            return # No active games, no effect
            
        total_active_sales = sum(g.sales for g in active_games)
        
        if self.lootboxes_active:
            # Massive random income, but burns trust and generates heat
            income += int(total_active_sales * random.uniform(0.1, 0.5))
            trust_burn = random.uniform(0.5, 2.0) - (self.pr_managers * 0.2)
            self.fan_trust = max(0.0, self.fan_trust - max(0, trust_burn))
            
            heat_gain = random.uniform(1.0, 3.0) - (self.ethics_managers * 0.5)
            self.government_heat = min(100.0, self.government_heat + max(0, heat_gain))
            
        if self.battle_pass_active:
            # Steady income, moderate trust burn, low heat
            income += int(total_active_sales * 0.1)
            trust_burn = 0.2 - (self.pr_managers * 0.05)
            self.fan_trust = max(0.0, self.fan_trust - max(0, trust_burn))
            
            heat_gain = 0.1 - (self.ethics_managers * 0.05)
            self.government_heat = min(100.0, self.government_heat + max(0, heat_gain))
            
        if not self.lootboxes_active and not self.battle_pass_active:
            # Recover trust and heat if disabled
            self.fan_trust = min(100.0, self.fan_trust + 0.5 + (self.pr_managers * 0.2))
            self.government_heat = max(0.0, self.government_heat - 0.5 - (self.ethics_managers * 0.2))
            
        if income > 0:
            game_state.track_income("other", income)
            
        # Shitstorm Event
        if self.fan_trust < 20:
            if random.random() < 0.1:
                fan_loss = int(game_state.fans * random.uniform(0.1, 0.3))
                game_state.fans = max(0, game_state.fans - fan_loss)
                game_state.emails.insert(0, Email(
                    game_state.get_text("sender_community", default="Community"),
                    game_state.get_text("shitstorm_monetization_subject", default="Shitstorm: Monetarisierung"),
                    game_state.get_text("shitstorm_monetization_body", fan_loss=fan_loss, default=f"Die Spieler haben genug! Eure Gier kostet euch {fan_loss} Fans."),
                    game_state.week
                ))
                self.fan_trust += 20 # Temporary relief
                
        # Government Investigation Event
        if self.government_heat >= 95:
            fine = int(game_state.money * 0.5) # 50% of cash
            game_state.track_expense("other", fine)
            game_state.emails.insert(0, Email(
                game_state.get_text("sender_government", default="Gluecksspielbehoerde"),
                game_state.get_text("fine_monetization_subject", default="Strafzahlung wegen illegalem Gluecksspiel"),
                game_state.get_text("fine_monetization_body", fine=fine, default=f"Ihre Lootbox-Mechaniken wurden als illegales Gluecksspiel eingestuft. Strafe: {fine} EUR."),
                game_state.week
            ))
            self.government_heat = 0 # Reset heat after fine
