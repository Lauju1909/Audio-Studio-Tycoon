import os
import re

print("Patching Game Data...")

with open("game_data.py", "r", encoding="utf-8") as f:
    gd = f.read()

# Add Content Creators
if "CONTENT_CREATORS" not in gd:
    cc = """
# ============================================================
# CONTENT CREATORS
# ============================================================
CONTENT_CREATORS = [
    {"id": "small_streamer", "name_key": "creator_small", "cost": 10000, "boost": 1.2, "duration": 4},
    {"id": "medium_streamer", "name_key": "creator_medium", "cost": 50000, "boost": 1.5, "duration": 4},
    {"id": "large_streamer", "name_key": "creator_large", "cost": 250000, "boost": 2.5, "duration": 4},
]
"""
    gd += cc

# Add Campus
if "campus_upgrade" not in gd:
    campus_upgrade = """
    {
        "id": "campus_upgrade",
        "name_key": "upgrade_campus",
        "cost": 1000000,
        "bonus": "campus_morale",
    },
"""
    gd = gd.replace('"id": "legal_protection",\n        "name_key": "upgrade_legal",\n        "cost": 80000,\n        "bonus": "legal_protection",\n    }', '"id": "legal_protection",\n        "name_key": "upgrade_legal",\n        "cost": 80000,\n        "bonus": "legal_protection",\n    },' + campus_upgrade)

with open("game_data.py", "w", encoding="utf-8") as f:
    f.write(gd)

print("Patching Logic...")

with open("logic.py", "r", encoding="utf-8") as f:
    lg = f.read()

# Initialize active_sponsorships
if "self.active_sponsorships =" not in lg:
    lg = lg.replace("self.active_tournaments = []", "self.active_tournaments = []\n        self.active_sponsorships = []")

if "def _process_sponsorships(self):" not in lg:
    spons_code = """
    def _process_sponsorships(self):
        if not hasattr(self, "active_sponsorships"):
            self.active_sponsorships = []
        for s in list(self.active_sponsorships):
            s["duration"] -= 1
            if s["duration"] <= 0:
                self.streamer_hype_multi /= s["boost"]
                self.active_sponsorships.remove(s)
                
    def add_sponsorship(self, boost, duration):
        if not hasattr(self, "active_sponsorships"):
            self.active_sponsorships = []
        self.active_sponsorships.append({"boost": boost, "duration": duration})
        self.streamer_hype_multi *= boost
"""
    lg = lg.replace("def _process_tournaments(self):", spons_code + "\n    def _process_tournaments(self):")
    lg = lg.replace("self._process_tournaments()", "self._process_tournaments()\n        self._process_sponsorships()")

# Add Campus logic in new week
if "campus_morale" not in lg:
    campus_logic = """
        perk_relief = 0.0
        owned_bonuses = [o.get("bonus") for o in self.office_objects]
        if "morale_room" in owned_bonuses:
            perk_relief += 1.0
        if "campus_morale" in owned_bonuses:
            perk_relief += 3.0
"""
    lg = lg.replace("""        perk_relief = 0.0
        if "morale_room" in [o.get("bonus") for o in self.office_objects]:
            perk_relief += 1.0""", campus_logic)

with open("logic.py", "w", encoding="utf-8") as f:
    f.write(lg)

print("Patching Business Menu (Subscription Vault)...")

with open("menus/business.py", "r", encoding="utf-8") as f:
    bm = f.read()

if "subscription_add_game_menu" not in bm:
    add_vault = """
            self.options.append({'text': gs.get_text('subscription_add_game'), 'action': lambda: "subscription_add_game_menu"})
"""
    bm = bm.replace("self.options.append({'text': gs.get_text('subscription_stop')", add_vault + "            self.options.append({'text': gs.get_text('subscription_stop')")

    vault_menu_class = """
class SubscriptionVaultMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('subscription_vault_title'), [], audio, game_state)
    def announce_entry(self):
        self.current_index = 0
        self.options = []
        
        for g in self.game_state.game_history:
            if g.is_active and g not in getattr(self.game_state, 'subscription_games', []):
                self.options.append({
                    'text': self.game_state.get_text('subscription_put_in_vault', name=g.name),
                    'action': lambda g=g: self.add_game(g)
                })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "subscription_service_menu"})
        super().announce_entry()
        
    def add_game(self, g):
        if not hasattr(self.game_state, 'subscription_games'):
            self.game_state.subscription_games = []
        self.game_state.subscription_games.append(g)
        self.audio.speak(self.game_state.get_text('subscription_added_to_vault', name=g.name))
        return "subscription_service_menu"

class CreatorSponsorshipMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('creator_menu_title'), [], audio, game_state)
        
    def announce_entry(self):
        self.current_index = 0
        self.options = []
        from game_data import CONTENT_CREATORS
        for c in CONTENT_CREATORS:
            self.options.append({
                'text': self.game_state.get_text('creator_sponsor_option', name=self.game_state.get_text(c['name_key']), cost=c['cost']),
                'action': lambda c=c: self.sponsor(c)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "marketing_menu"})
        super().announce_entry()
        
    def sponsor(self, c):
        if self.game_state.money < c['cost']:
            self.audio.speak(self.game_state.get_text('creator_fail_money', cost=c['cost']))
            return None
        self.game_state.track_expense("marketing", c['cost'])
        self.game_state.add_sponsorship(c['boost'], c['duration'])
        self.audio.speak(self.game_state.get_text('creator_success', name=self.game_state.get_text(c['name_key'])))
        return "marketing_menu"
"""
    bm = bm + "\n" + vault_menu_class

with open("menus/business.py", "w", encoding="utf-8") as f:
    f.write(bm)

print("Patching Marketing Menu...")

with open("menus/marketing_jingle.py", "r", encoding="utf-8") as f:
    mm = f.read()

if "creator_menu" not in mm:
    mm = mm.replace("self.options.append({'text': gs.get_text('back'), 'action': lambda: \"marketing_menu\"})", "self.options.append({'text': gs.get_text('creator_menu_title'), 'action': lambda: \"creator_menu\"})\n        self.options.append({'text': gs.get_text('back'), 'action': lambda: \"marketing_menu\"})")

with open("menus/marketing_jingle.py", "w", encoding="utf-8") as f:
    f.write(mm)

print("Patching Init...")

with open("menus/__init__.py", "r", encoding="utf-8") as f:
    mi = f.read()

if "CreatorSponsorshipMenu" not in mi:
    mi = mi.replace("from .business import (", "from .business import (\n    SubscriptionVaultMenu, CreatorSponsorshipMenu,")
    mi = mi.replace('"MerchAmountMenu",', '"MerchAmountMenu", "SubscriptionVaultMenu", "CreatorSponsorshipMenu",')

with open("menus/__init__.py", "w", encoding="utf-8") as f:
    f.write(mi)

print("Done with script patches.")
