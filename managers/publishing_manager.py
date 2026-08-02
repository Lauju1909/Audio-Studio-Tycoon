import random
from models import Email

class PublishingManager:
    def __init__(self):
        self.is_active = False
        self.prestige = 0
        self.active_pitches = []
        self.funded_projects = []
        self.weeks_since_last_pitch = 0
        
    def to_dict(self):
        return {
            "is_active": self.is_active,
            "prestige": self.prestige,
            "active_pitches": self.active_pitches,
            "funded_projects": self.funded_projects,
            "weeks_since_last_pitch": self.weeks_since_last_pitch
        }
        
    def from_dict(self, data):
        if not data: return
        self.is_active = data.get("is_active", False)
        self.prestige = data.get("prestige", 0)
        self.active_pitches = data.get("active_pitches", [])
        self.funded_projects = data.get("funded_projects", [])
        self.weeks_since_last_pitch = data.get("weeks_since_last_pitch", 0)

    def launch_label(self, game_state):
        cost = 10000000 # 10 Mio EUR
        if game_state.money >= cost:
            game_state.track_expense("other", cost)
            self.is_active = True
            return True, "Publishing Label gegruendet!"
        return False, "Nicht genug Geld (10.000.000 EUR benoetigt)."
        
    def _generate_pitch(self, game_state):
        # Base budget depends on prestige
        base_budget = 250000 + (self.prestige * 50000)
        budget = int(random.uniform(base_budget * 0.5, base_budget * 2.0))
        
        studios = ["Pixel Forge", "Neon Dreams", "Code Monkeys", "Starlight Devs", "Rebel Games"]
        games = ["Dungeon Delver", "Space Trucker", "Zombie Farm", "Neon Racer", "Mystery Manor"]
        
        pitch = {
            "id": random.randint(10000, 99999),
            "studio": random.choice(studios),
            "game_name": random.choice(games),
            "budget": budget,
            "revenue_share": random.randint(50, 80), # Player gets 50-80%
            "dev_time": random.randint(20, 52) # 20-52 weeks
        }
        self.active_pitches.append(pitch)
        
        game_state.emails.insert(0, Email(
            pitch["studio"],
            "Neuer Pitch: " + pitch["game_name"],
            f"Wir suchen {budget:,} EUR Funding fuer unser neues Spiel. Wir bieten {pitch['revenue_share']}% Revenue-Share bei Release.",
            game_state.week
        ))
        
    def fund_pitch(self, game_state, pitch_id):
        pitch = next((p for p in self.active_pitches if p["id"] == pitch_id), None)
        if not pitch:
            return False, "Pitch nicht gefunden."
            
        if game_state.money >= pitch["budget"]:
            game_state.track_expense("other", pitch["budget"])
            
            project = {
                "name": pitch["game_name"],
                "studio": pitch["studio"],
                "budget": pitch["budget"],
                "revenue_share": pitch["revenue_share"],
                "weeks_left": pitch["dev_time"],
                "base_quality": random.randint(40, 70) + min(30, self.prestige * 2) # Higher prestige = better pitches
            }
            self.funded_projects.append(project)
            self.active_pitches.remove(pitch)
            return True, f"Projekt {pitch['game_name']} erfolgreich finanziert!"
            
        return False, f"Nicht genug Geld ({pitch['budget']:,} EUR benoetigt)."
        
    def reject_pitch(self, pitch_id):
        self.active_pitches = [p for p in self.active_pitches if p["id"] != pitch_id]
        
    def tick(self, game_state):
        if not self.is_active:
            return
            
        # Pitch generation
        self.weeks_since_last_pitch += 1
        if self.weeks_since_last_pitch >= 12 and random.random() < 0.2:
            self._generate_pitch(game_state)
            self.weeks_since_last_pitch = 0
            
        # Expire old pitches
        if len(self.active_pitches) > 3:
            self.active_pitches.pop(0) # Remove oldest
            
        # Process funded projects
        finished_projects = []
        for project in self.funded_projects:
            project["weeks_left"] -= 1
            if project["weeks_left"] <= 0:
                finished_projects.append(project)
                
        for project in finished_projects:
            self.funded_projects.remove(project)
            
            # Resolve release
            variance = random.randint(-15, 15)
            review = min(100, max(10, project["base_quality"] + variance))
            
            # Revenue calculation
            sales = project["budget"] * (review / 50.0) * random.uniform(0.5, 2.0)
            if review >= 80:
                sales *= 2 # Hit multiplier
                self.prestige += 1
                
            player_revenue = int(sales * (project["revenue_share"] / 100.0))
            profit = player_revenue - project["budget"]
            
            if player_revenue > 0:
                game_state.track_income("other", player_revenue)
                
            msg = f"Das von uns publizierte Spiel '{project['name']}' von {project['studio']} wurde veroeffentlicht!\n\n"
            msg += f"Review-Score: {review}%\n"
            msg += f"Unser Umsatzanteil: {player_revenue:,} EUR\n"
            msg += f"Netto-Gewinn: {profit:,} EUR"
            
            game_state.emails.insert(0, Email(
                "Publishing Label",
                f"Release: {project['name']}",
                msg,
                game_state.week
            ))
