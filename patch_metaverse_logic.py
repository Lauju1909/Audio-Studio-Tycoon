
with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to __init__
init_target = "        self.active_events = []"
init_replace = """        self.active_events = []
        self.metaverse_land_value = 0.0
        self.metaverse_investment = 0.0
        self.metaverse_weeks_active = 0
        self.metaverse_burst = False"""

if init_target in content:
    content = content.replace(init_target, init_replace)

# Add to _on_new_week
tick_target = "        # Random Events (falls aktiviert)"
tick_replace = """        # Metaverse Bubble Logic
        if self.metaverse_investment > 0 and not self.metaverse_burst:
            self.metaverse_weeks_active += 1
            # Value inflates by 1% to 5% every week!
            import random
            growth = random.uniform(0.01, 0.05)
            self.metaverse_land_value *= (1 + growth)
            
            # Crash Logic after 24 weeks
            if self.metaverse_weeks_active > 24:
                # increasing risk
                risk = 0.005 + (self.metaverse_weeks_active - 24) * 0.001
                if random.random() < risk:
                    # BUBBLE BURST!
                    self.metaverse_burst = True
                    self.track_expense("metaverse_crash", self.metaverse_investment) # Just track it? No, money is already gone when invested.
                    self.metaverse_land_value = 0
                    self.hype = max(0, self.hype - 30)
                    for e in self.employees:
                        e.morale = max(0, e.morale - 20)
                    self.active_events.append({
                        "name": "AudioVerse-Blase geplatzt!",
                        "effect": "none",
                        "multiplier": 1.0,
                        "duration": 4
                    })

        # Random Events (falls aktiviert)"""

if tick_target in content:
    content = content.replace(tick_target, tick_replace)

# Add to to_dict
to_dict_target = '            "active_events": self.active_events,'
to_dict_replace = """            "active_events": self.active_events,
            "metaverse_land_value": self.metaverse_land_value,
            "metaverse_investment": self.metaverse_investment,
            "metaverse_weeks_active": getattr(self, 'metaverse_weeks_active', 0),
            "metaverse_burst": getattr(self, 'metaverse_burst', False),"""
if to_dict_target in content:
    content = content.replace(to_dict_target, to_dict_replace)

# Add to load_dict
load_target = '        self.active_events = data.get("active_events", [])'
load_replace = """        self.active_events = data.get("active_events", [])
        self.metaverse_land_value = data.get("metaverse_land_value", 0.0)
        self.metaverse_investment = data.get("metaverse_investment", 0.0)
        self.metaverse_weeks_active = data.get("metaverse_weeks_active", 0)
        self.metaverse_burst = data.get("metaverse_burst", False)"""
if load_target in content:
    content = content.replace(load_target, load_replace)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched logic.py for Metaverse")
