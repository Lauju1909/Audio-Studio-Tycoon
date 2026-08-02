import random

class UnionManager:
    def __init__(self):
        self.ai_tools_active = False
        self.is_striking = False
        self.strike_weeks_left = 0
        self.union_anger = 0.0 # 0.0 to 100.0
        self.negotiation_cooldown = 0
        self.union_busted = False

    def tick(self, game_state):
        if self.union_busted:
            return

        # Passive anger gain/loss based on AI tools and average employee morale
        avg_morale = 100
        if game_state.employees:
            avg_morale = sum(emp.morale for emp in game_state.employees) / len(game_state.employees)

        if self.ai_tools_active:
            self.union_anger += 2.0
            # AI lowers employee morale over time
            for emp in game_state.employees:
                emp.morale = max(0, emp.morale - random.uniform(0.5, 1.5))
        else:
            if avg_morale > 70:
                self.union_anger = max(0, self.union_anger - 1.0)
            elif avg_morale < 40:
                self.union_anger += 1.0

        if self.negotiation_cooldown > 0:
            self.negotiation_cooldown -= 1

        # Check for strike
        if self.union_anger >= 100.0 and not self.is_striking and self.negotiation_cooldown == 0:
            self.is_striking = True
            self.strike_weeks_left = random.randint(4, 8)
            
            # Send Email
            from models import Email
            game_state.emails.insert(0, Email(
                sender=game_state.get_text("sender_union"),
                subject=game_state.get_text("subject_strike_started"),
                body=game_state.get_text("body_strike_started"),
                date_week=game_state.week
            ))
            if hasattr(game_state, "audio"):
                game_state.audio.play_sound("error")

        if self.is_striking:
            self.strike_weeks_left -= 1
            if self.strike_weeks_left <= 0:
                self.is_striking = False
                self.union_anger = 50.0  # Reset anger slightly after strike ends
                self.negotiation_cooldown = 10
                
                from models import Email
                game_state.emails.insert(0, Email(
                    sender=game_state.get_text("sender_union"),
                    subject=game_state.get_text("subject_strike_ended"),
                    body=game_state.get_text("body_strike_ended"),
                    date_week=game_state.week
                ))

    def negotiate(self, option, game_state):
        if option == "accept_demands":
            # Demands: +20% salary for all, disable AI tools
            for emp in game_state.employees:
                emp.salary = int(emp.salary * 1.2)
                emp.morale = min(100, emp.morale + 30)
            self.ai_tools_active = False
            self.is_striking = False
            self.strike_weeks_left = 0
            self.union_anger = 0.0
            self.negotiation_cooldown = 20
            return True, game_state.get_text("union_negotiation_success")
            
        elif option == "compromise":
            cost = len(game_state.employees) * 15000 # Bonus payment
            if game_state.money >= cost:
                game_state.track_expense("other", cost)
                self.is_striking = False
                self.strike_weeks_left = 0
                self.union_anger -= 30.0
                self.negotiation_cooldown = 10
                for emp in game_state.employees:
                    emp.morale = min(100, emp.morale + 15)
                return True, game_state.get_text("union_compromise_success", cost=cost)
            else:
                return False, game_state.get_text("not_enough_money")
                
        elif option == "union_busting":
            cost = 500000 # Expensive PR/Lawyers
            if game_state.money >= cost:
                game_state.track_expense("other", cost)
                if random.random() < 0.4: # 40% chance of success
                    self.union_busted = True
                    self.is_striking = False
                    self.strike_weeks_left = 0
                    self.union_anger = 0.0
                    for emp in game_state.employees:
                        emp.morale = max(0, emp.morale - 50)
                    return True, game_state.get_text("union_busting_success")
                else:
                    # Disaster
                    penalty = 1000000
                    game_state.track_expense("other", penalty)
                    game_state.fans = max(0, int(game_state.fans * 0.8)) # Lose 20% fans
                    return False, game_state.get_text("union_busting_fail", penalty=penalty)
            else:
                return False, game_state.get_text("not_enough_money")

    def to_dict(self):
        return {
            "ai_tools_active": self.ai_tools_active,
            "is_striking": self.is_striking,
            "strike_weeks_left": self.strike_weeks_left,
            "union_anger": self.union_anger,
            "negotiation_cooldown": self.negotiation_cooldown,
            "union_busted": self.union_busted
        }

    def from_dict(self, data):
        self.ai_tools_active = data.get("ai_tools_active", False)
        self.is_striking = data.get("is_striking", False)
        self.strike_weeks_left = data.get("strike_weeks_left", 0)
        self.union_anger = data.get("union_anger", 0.0)
        self.negotiation_cooldown = data.get("negotiation_cooldown", 0)
        self.union_busted = data.get("union_busted", False)
