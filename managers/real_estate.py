import random

class RealEstateProperty:
    def __init__(self, name, capacity, base_cost, condition=100, location_quality=1.0):
        self.name = name
        self.capacity = capacity
        self.base_cost = base_cost
        self.condition = condition # 0 to 100
        self.location_quality = location_quality # 0.5 to 2.0 (affects passive prestige/hype)
        
        # Perks - True when bought
        self.has_canteen = False
        self.has_gym = False
        self.has_server_room = False
        self.has_lounge = False
        
        self.market_value = base_cost

    @property
    def max_condition(self):
        return 100

    def get_perk_cost(self, perk_name):
        costs = {
            "canteen": 500000,
            "gym": 800000,
            "server_room": 2500000,
            "lounge": 300000
        }
        return costs.get(perk_name, 0)
        
    def to_dict(self):
        return {
            "name": self.name,
            "capacity": self.capacity,
            "base_cost": self.base_cost,
            "condition": self.condition,
            "location_quality": self.location_quality,
            "has_canteen": self.has_canteen,
            "has_gym": self.has_gym,
            "has_server_room": self.has_server_room,
            "has_lounge": self.has_lounge,
            "market_value": self.market_value
        }
        
    @classmethod
    def from_dict(cls, data):
        prop = cls(
            data["name"], 
            data["capacity"], 
            data["base_cost"], 
            data.get("condition", 100), 
            data.get("location_quality", 1.0)
        )
        prop.has_canteen = data.get("has_canteen", False)
        prop.has_gym = data.get("has_gym", False)
        prop.has_server_room = data.get("has_server_room", False)
        prop.has_lounge = data.get("has_lounge", False)
        prop.market_value = data.get("market_value", prop.base_cost)
        return prop

class RealEstateManager:
    def __init__(self):
        self.owned_properties = []
        self.active_property_index = -1 # Which office is currently in use
        self.market_listings = []
        self.market_refresh_timer = 0
        self.market_trend = 1.0 # Market multiplier
        
    def is_unlocked(self, state):
        """Unlocked if player has 50M in the bank or year is >= 2008"""
        if state.money >= 50_000_000:
            return True
        if state.get_calendar_year() >= 2008:
            return True
        return False
        
    def tick(self, state):
        if not self.is_unlocked(state):
            return
            
        # Refresh market every 12 weeks
        self.market_refresh_timer -= 1
        if self.market_refresh_timer <= 0:
            self._refresh_market()
            self.market_refresh_timer = 12
            
        # Property maintenance and condition degradation
        for idx, prop in enumerate(self.owned_properties):
            # Fluctuate market value
            fluctuation = random.uniform(0.98, 1.03)
            prop.market_value = int(prop.market_value * fluctuation * self.market_trend)
            
            # Condition degrades slightly each week if it's the active office
            if idx == self.active_property_index:
                if random.random() < 0.1: # 10% chance per week to lose 1 condition
                    prop.condition = max(0, prop.condition - 1)
                    
        # Apply perks and penalties for active property
        if self.active_property_index >= 0 and self.active_property_index < len(self.owned_properties):
            active_prop = self.owned_properties[self.active_property_index]
            
            # Bad condition lowers morale
            if active_prop.condition < 50:
                if random.random() < 0.05:
                    for emp in state.employees:
                        emp.morale = max(0, emp.morale - 1)
                        
            # Canteen restores morale
            if active_prop.has_canteen and random.random() < 0.1:
                for emp in state.employees:
                    emp.morale = min(100, emp.morale + 1)
                    
            # Gym reduces fatigue
            if active_prop.has_gym and random.random() < 0.2:
                for emp in state.employees:
                    emp.fatigue = max(0, emp.fatigue - 1)
                    
        # Server room discount is applied in MonetizationManager/Finance
        
    def _refresh_market(self):
        self.market_trend = random.uniform(0.9, 1.1)
        self.market_listings = []
        
        # Generate 3 random properties
        templates = [
            {"name": "Heruntergekommenes Lagerhaus", "cap": 15, "cost": 1_000_000, "loc": 0.6, "cond": 40},
            {"name": "Standard Bro", "cap": 30, "cost": 5_000_000, "loc": 1.0, "cond": 80},
            {"name": "Start-Up Loft", "cap": 25, "cost": 8_000_000, "loc": 1.2, "cond": 95},
            {"name": "Innenstadt Hochhaus-Etage", "cap": 50, "cost": 25_000_000, "loc": 1.5, "cond": 100},
            {"name": "Suburbaner Campus", "cap": 100, "cost": 60_000_000, "loc": 1.3, "cond": 100},
            {"name": "Tech-Gigant Wolkenkratzer", "cap": 250, "cost": 150_000_000, "loc": 2.0, "cond": 100}
        ]
        
        choices = random.sample(templates, min(3, len(templates)))
        for c in choices:
            variance = random.uniform(0.8, 1.2)
            self.market_listings.append(RealEstateProperty(
                name=c["name"],
                capacity=int(c["cap"] * random.uniform(0.9, 1.1)),
                base_cost=int(c["cost"] * variance * self.market_trend),
                condition=c["cond"],
                location_quality=c["loc"]
            ))
            
    def buy_property(self, state, list_index):
        if list_index < 0 or list_index >= len(self.market_listings):
            return False
        prop = self.market_listings[list_index]
        if state.money >= prop.base_cost:
            state.money -= prop.base_cost
            state.track_expense("infrastructure", prop.base_cost)
            self.owned_properties.append(prop)
            self.market_listings.pop(list_index)
            
            # Auto-move if it's the first property
            if self.active_property_index == -1:
                self.active_property_index = 0
            return True
        return False
        
    def sell_property(self, state, prop_index):
        if prop_index < 0 or prop_index >= len(self.owned_properties):
            return False
            
        prop = self.owned_properties[prop_index]
        sell_price = prop.market_value
        state.money += sell_price
        state.track_income("other", sell_price)
        
        self.owned_properties.pop(prop_index)
        
        # Adjust active index
        if self.active_property_index == prop_index:
            self.active_property_index = 0 if len(self.owned_properties) > 0 else -1
        elif self.active_property_index > prop_index:
            self.active_property_index -= 1
            
        return True
        
    def renovate_property(self, state, prop_index):
        if prop_index < 0 or prop_index >= len(self.owned_properties):
            return False
        prop = self.owned_properties[prop_index]
        missing = 100 - prop.condition
        if missing <= 0:
            return False
            
        cost = missing * 10000 # 10k per percent
        if state.money >= cost:
            state.money -= cost
            state.track_expense("infrastructure", cost)
            prop.condition = 100
            prop.market_value += int(cost * 0.8) # Increases value slightly
            return True
        return False
        
    def buy_perk(self, state, prop_index, perk_name):
        if prop_index < 0 or prop_index >= len(self.owned_properties):
            return False
        prop = self.owned_properties[prop_index]
        cost = prop.get_perk_cost(perk_name)
        
        if getattr(prop, f"has_{perk_name}", True):
            return False # Already has it or invalid
            
        if cost > 0 and state.money >= cost:
            state.money -= cost
            state.track_expense("infrastructure", cost)
            setattr(prop, f"has_{perk_name}", True)
            prop.market_value += int(cost * 0.5)
            return True
        return False

    def to_dict(self):
        return {
            "owned_properties": [p.to_dict() for p in self.owned_properties],
            "active_property_index": self.active_property_index,
            "market_listings": [p.to_dict() for p in self.market_listings],
            "market_refresh_timer": self.market_refresh_timer,
            "market_trend": self.market_trend
        }
        
    def from_dict(self, data):
        self.owned_properties = [RealEstateProperty.from_dict(p) for p in data.get("owned_properties", [])]
        self.active_property_index = data.get("active_property_index", -1)
        self.market_listings = [RealEstateProperty.from_dict(p) for p in data.get("market_listings", [])]
        self.market_refresh_timer = data.get("market_refresh_timer", 0)
        self.market_trend = data.get("market_trend", 1.0)
