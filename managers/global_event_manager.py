import random
from models import Email

class GlobalEvent:
    def __init__(self, name, description, duration_weeks, effect_type):
        self.name = name
        self.description = description
        self.duration_weeks = duration_weeks
        self.effect_type = effect_type # e.g. "chip_crisis"
        self.weeks_active = 0
        self.is_active = True
        
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "duration_weeks": self.duration_weeks,
            "effect_type": self.effect_type,
            "weeks_active": self.weeks_active,
            "is_active": self.is_active
        }
        
    @classmethod
    def from_dict(cls, data):
        e = cls(data["name"], data["description"], data["duration_weeks"], data["effect_type"])
        e.weeks_active = data["weeks_active"]
        e.is_active = data["is_active"]
        return e

class GlobalEventManager:
    def __init__(self):
        self.current_event = None
        self.black_market_deal_active = False # If player bought chips on the black market
        
    def trigger_chip_crisis(self, game_state):
        duration = random.randint(20, 50) # Lasts 20-50 weeks
        self.current_event = GlobalEvent(
            "Globale Chip-Krise",
            "Ein weltweiter Mangel an Halbleitern lässt Hardware- und Serverkosten explodieren. Die Entwicklung verlangsamt sich durch fehlende Arbeits-PCs.",
            duration,
            "chip_crisis"
        )
        self.black_market_deal_active = False
        game_state.emails.insert(0, Email(
            "Wirtschafts-News",
            "EILMELDUNG: Chip-Krise!",
            self.current_event.description,
            game_state.week
        ))
        if hasattr(game_state, "audio"):
            game_state.audio.play_sound("error")
            
    def buy_black_market_chips(self, game_state):
        cost = 5000000 # 5 Mio EUR
        if game_state.money >= cost:
            game_state.track_expense("other", cost)
            self.black_market_deal_active = True
            return True, "Schwarzmarkt-Deal erfolgreich. Ihre Entwickler haben wieder PCs!"
        return False, "Nicht genug Geld (5.000.000 EUR benoetigt)."
        
    def get_development_speed_modifier(self):
        if self.current_event and self.current_event.effect_type == "chip_crisis":
            if not self.black_market_deal_active:
                return 0.8 # 20% slower
        return 1.0
        
    def get_server_cost_modifier(self):
        if self.current_event and self.current_event.effect_type == "chip_crisis":
            return 1.5 # 50% more expensive
        return 1.0
        
    def get_hardware_cost_modifier(self):
        if self.current_event and self.current_event.effect_type == "chip_crisis":
            return 2.0 # 100% more expensive
        return 1.0

    def tick(self, game_state):
        # Randomly trigger event if not active and year >= 2020
        if not self.current_event and game_state.get_calendar_year() >= 2020:
            if random.random() < 0.02: # 2% chance per week
                self.trigger_chip_crisis(game_state)
                
        if self.current_event:
            self.current_event.weeks_active += 1
            if self.current_event.weeks_active >= self.current_event.duration_weeks:
                # Event over
                game_state.emails.insert(0, Email(
                    "Wirtschafts-News",
                    "ENTWARNUNG: Chip-Krise beendet",
                    "Die Lieferketten haben sich stabilisiert. Hardware- und Serverpreise sinken auf Normalniveau.",
                    game_state.week
                ))
                if hasattr(game_state, "audio"):
                    game_state.audio.play_sound("confirm")
                self.current_event = None
                self.black_market_deal_active = False

    def to_dict(self):
        return {
            "current_event": self.current_event.to_dict() if self.current_event else None,
            "black_market_deal_active": self.black_market_deal_active
        }
        
    def from_dict(self, data):
        if not data: return
        if data.get("current_event"):
            self.current_event = GlobalEvent.from_dict(data["current_event"])
        else:
            self.current_event = None
        self.black_market_deal_active = data.get("black_market_deal_active", False)
