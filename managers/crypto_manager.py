import random
from models import Email

class CryptoManager:
    def __init__(self):
        self.ico_launched = False
        self.coin_price = 0.0
        self.hype_level = 0.0
        self.weeks_since_launch = 0
        self.crashed = False
        
    def to_dict(self):
        return {
            "ico_launched": self.ico_launched,
            "coin_price": self.coin_price,
            "hype_level": self.hype_level,
            "weeks_since_launch": self.weeks_since_launch,
            "crashed": self.crashed
        }
        
    def from_dict(self, data):
        if not data: return
        self.ico_launched = data.get("ico_launched", False)
        self.coin_price = data.get("coin_price", 0.0)
        self.hype_level = data.get("hype_level", 0.0)
        self.weeks_since_launch = data.get("weeks_since_launch", 0)
        self.crashed = data.get("crashed", False)
        
    def launch_ico(self, game_state):
        if self.ico_launched:
            return False, "ICO wurde bereits durchgefuehrt."
        
        self.ico_launched = True
        self.crashed = False
        self.coin_price = 1.0
        self.hype_level = 100.0
        self.weeks_since_launch = 0
        
        # Massive initial cash injection
        ico_revenue = random.randint(20000000, 50000000) # 20 to 50 million
        game_state.track_income("other", ico_revenue)
        
        game_state.emails.insert(0, Email(
            "Crypto Bros",
            "To the Moon! 🚀",
            f"Der ICO war ein voller Erfolg! Wir haben {ico_revenue:,} EUR eingenommen. Die Blockchain gehoert uns!",
            game_state.week
        ))
        
        return True, f"ICO erfolgreich! +{ico_revenue:,} EUR eingenommen."
        
    def pump_coin(self, game_state):
        if not self.ico_launched or self.crashed:
            return False, "Kein aktiver Coin zum Pumpen."
            
        cost = 1000000 # 1 Mio EUR
        if game_state.money >= cost:
            game_state.track_expense("other", cost)
            self.hype_level = min(100.0, self.hype_level + 30.0)
            self.coin_price = min(10000.0, self.coin_price * 1.3)
            return True, "Influencer bezahlt. Der Hype steigt extrem!"
            
        return False, "Nicht genug Geld fuer den Pump (1 Mio EUR)."
        
    def trigger_crash(self, game_state):
        self.crashed = True
        self.coin_price = 0.001
        self.hype_level = 0.0
        
        # Destroy fan trust and maximize government heat in monetization manager
        if hasattr(game_state, "monetization_manager"):
            game_state.monetization_manager.fan_trust = 0.0
            game_state.monetization_manager.government_heat = 100.0
            
        # Direct lawsuit expense due to unregistered securities
        lawsuit = int(game_state.money * 0.25)
        game_state.track_expense("other", lawsuit)
        
        # Massive fan loss
        fan_loss = int(game_state.fans * 0.4) # Lose 40% of all fans
        game_state.fans = max(0, game_state.fans - fan_loss)
        
        game_state.emails.insert(0, Email(
            "SEC & Verbraucherschutz",
            "Krypto-Blase geplatzt! Ermittlungen eingeleitet",
            f"Ihr Coin-Projekt ist als illegaler Scam zusammengebrochen (Rug Pull). Wir haben eine Strafe von {lawsuit:,} EUR verhaengt.\nZusaetzlich haben sich {fan_loss:,} enttaeuschte Fans abgewandt.",
            game_state.week
        ))
        
    def tick(self, game_state):
        if not self.ico_launched or self.crashed:
            return
            
        self.weeks_since_launch += 1
        
        # Hype decays slowly
        self.hype_level = max(0.0, self.hype_level - random.uniform(1.0, 5.0))
        
        # Coin price fluctuates
        volatility = random.uniform(-0.15, 0.25) if self.hype_level > 50 else random.uniform(-0.3, 0.05)
        self.coin_price = max(0.01, min(10000.0, self.coin_price * (1.0 + volatility)))
        
        # Passive income from transaction fees (Play-to-Earn)
        fees = int(self.coin_price * self.hype_level * 2000)
        if fees > 0:
            game_state.track_income("other", fees)
            
        # Crash risk increases over time and as hype drops
        crash_chance = 0.005 + (0.001 * self.weeks_since_launch)
        if self.hype_level < 25:
            crash_chance += 0.1 # High risk if hype dies
            
        if random.random() < crash_chance:
            self.trigger_crash(game_state)
