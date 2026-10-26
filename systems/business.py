"""Lizenzen, Publishing, Produktion, Server, Buero. Mixin fuer GameState."""
import random

import json
import os
from managers.corporate_warfare import CorporateWarfareManager
from managers.union_manager import UnionManager
from managers.it_security import ITSecurityManager
from managers.conventions import ConventionManager
from managers.real_estate import RealEstateManager
from managers.stock_manager import StockManager
from managers.subscription_manager import SubscriptionManager
from managers.monetization_manager import MonetizationManager
from managers.publishing_manager import PublishingManager
from managers.crypto_manager import CryptoManager
from managers.monopoly_manager import MonopolyManager
from managers.global_event_manager import GlobalEventManager
from models import (
    GameProject, ReviewScore, Employee, Engine, EngineFeature, 
    RivalStudio, RivalGame, Email, AddonProject, BundleProject, 
    ActiveMMO, BankLoan, CustomConsole, PublishingOffer, 
    PublishedThirdPartyGame, BankStatement,
    SoundConEvent, SoundtrackLabel, RadioContract, ManufacturingJob,
    StreamingPlatform, PodcastNetwork, AudioPass, CloudGamingService
)
from translations import get_system_language
from game_data import (
    get_compatibility, get_ideal_sliders, SLIDER_NAMES, PLATFORMS, AUDIENCE_MULTI, AUDIENCE_PRICE,
    RANDOM_EVENTS, ENGINE_FEATURES,
    EMPLOYEE_ROLES, DEV_PHASES, GAME_SIZES,
    TREND_TOPICS, TREND_GENRES, START_TOPICS, RESEARCHABLE_TOPICS,
    START_GENRES, START_AUDIENCES, RESEARCHABLE_GENRES, RESEARCHABLE_AUDIENCES,
    RESEARCHABLE_TECHNOLOGIES,
    get_available_platforms, START_YEAR, WEEKS_PER_YEAR,
)


class BusinessMixin:
    def can_upgrade_office(self):
        return False

    def upgrade_office(self):
        return False

    def get_office_info(self):
        """Info über aktuelles Büro."""
        return {"name": "Eigenes Studio", "cost": 0, "max_employees": self.get_max_employees()}

    def get_available_licenses(self):
        """Gibt eine Liste von Lizenzen zurück, die man kaufen kann (abhängig von Studio-Level)."""
        from game_data import LICENSES
        available = []
        for lic in LICENSES:
            # Man kann Lizenzen nur kaufen, wenn man sie noch nicht ungenutzt besitzt
            already_owned = any(owned['name'] == lic['name'] and not owned['used'] for owned in self.owned_licenses)
            if not already_owned:
                available.append(lic)
        return available

    def buy_license(self, license_arg):
        """Kauft eine Lizenz für das Studio (Akzeptiert Index oder Lizenz-Dict)."""
        available = self.get_available_licenses()
        license_data = None
        
        if isinstance(license_arg, int):
            if 0 <= license_arg < len(available):
                license_data = available[license_arg]
        elif isinstance(license_arg, dict):
            license_data = license_arg
            
        if not license_data:
            return False
            
        cost = license_data["base_cost"]
        if self.money >= cost:
            self.track_expense("other", cost)
            self.owned_licenses.append({
                "name": license_data["name"],
                "purchased_week": self.week,
                "expires_week": self.week + WEEKS_PER_YEAR, # Verfällt nach 1 Jahr
                "used": False,
                "hype_bonus": license_data["hype_bonus"]
            })
            return True
        return False

    def generate_publisher_deals(self):
        """Generiert eine Liste von Publisher-Deals für das aktuelle Projekt."""
        deals = []
        if not self.current_draft.get("name"):
            return deals

        # 3 Publisher Deals
        for i in range(3):
            name = f"Publisher {chr(65+i)}"
            upfront = random.randint(10000, 50000) * self.office_level
            royalty = random.randint(10, 40)
            marketing = random.choice(["Kein Marketing", "Wenig Marketing", "Großes Marketing"])
            target_score = random.randint(6, 9)
            penalty = random.randint(5000, 20000) * self.office_level
            
            deals.append({
                "name": name,
                "upfront": upfront,
                "royalty": royalty,
                "marketing": marketing,
                "target_score": target_score,
                "penalty": penalty
            })
            
        return deals

    def get_unused_licenses(self):
        """Gibt alle gekauften Lizenzen zurück, die noch nicht verfallen und unbenutzt sind."""
        valid_licenses = []
        for lic in self.owned_licenses:
            if not lic['used'] and self.week <= lic['expires_week']:
                valid_licenses.append(lic)
        return valid_licenses

    def get_active_licenses(self):
        """Alternativer Name für get_unused_licenses, oft genutzt in playtest."""
        return self.get_unused_licenses()

    def use_license(self, license_name):
        """Markiert eine Lizenz als genutzt und wendet sie auf den aktuellen Entwurf an."""
        for lic in self.owned_licenses:
            if lic['name'] == license_name and not lic['used'] and self.week <= lic['expires_week']:
                lic['used'] = True
                self.current_draft["license"] = lic
                return True
        return False

    def produce_physical_copies(self, game_idx, amount, cost_per_unit=1.5):
        """Gibt physikalische Einheiten in Auftrag."""
        if not getattr(self, "has_presswerk", False):
            return False, "no_presswerk"

        if 0 <= game_idx < len(self.game_history):
            g = self.game_history[game_idx]
            if not getattr(g, "is_active", False):
                return False, "game_inactive"

            total_cost = int(amount * cost_per_unit)
            if self.money < total_cost:
                return False, "not_enough_money"

            available_storage = getattr(self, "storage_capacity", 0) - getattr(self, "used_storage", 0)
            if amount > available_storage:
                return False, "storage_full"

            self.track_expense("production", total_cost)
            self.used_storage += amount
            g.physical_copies = getattr(g, "physical_copies", 0) + amount
            return True, total_cost
        
        return False, "invalid_game"

    def build_server_room(self):
        """Baut den ersten Serverraum."""
        cost = 1000000
        if self.money >= cost and getattr(self, "office_level", 0) >= 3 and not getattr(self, "has_server_room", False):
            self.track_expense("mmo", cost)
            self.has_server_room = True
            self.server_capacity = 50000
            return True
        return False

    def expand_server_capacity(self):
        """Erweitert Serverkapazität um 50.000 Spieler."""
        cost = 250000
        if self.money >= cost and getattr(self, "has_server_room", False):
            self.track_expense("mmo", cost)
            self.server_capacity += 50000
            return True
        return False

    def apply_mmo_update(self, active_mmo_idx, cost=500000, player_boost=0.2):
        """Veröffentlicht ein Content-Update für ein aktives MMO."""
        if 0 <= active_mmo_idx < len(getattr(self, "active_mmos", [])):
            if self.money >= cost:
                self.track_expense("mmo", cost)
                mmo = self.active_mmos[active_mmo_idx]
                mmo.players = int(mmo.players * (1 + player_boost))
                mmo.game.hype = min(100, getattr(mmo.game, "hype", 0) + 20)
                return True, "success"
            return False, "not_enough_money"
        return False, "not_found"

    def _generate_publishing_offer(self):
        """Generiert ein zufälliges Publishing-Angebot für den Spieler."""
        from game_data import START_TOPICS, START_GENRES
        
        studios = ["Pixel Wizards", "Neon Interactive", "Bitforge Studios", "Quantum Games", "Hyperion Soft"]
        words = ["Quest", "Saga", "Chronicles", "World", "Strike", "Legends", "Simulator", "Manager"]
        
        studio = random.choice(studios)
        game_topic = random.choice(list(START_TOPICS))
        game_genre = random.choice(list(START_GENRES))
        game_name = f"{self.get_text(game_topic)} {random.choice(words)}"
        
        quality = random.randint(30, 95)
        # Marketingkosten skalieren mit Qualität
        marketing_cost = int((quality ** 2) * 50) 
        
        # Player Share (wie viel % der Einnahmen wir bekommen)
        player_share = random.uniform(0.3, 0.7)
        
        offer = PublishingOffer(studio, game_name, game_genre, quality, marketing_cost, player_share)
        
        if not hasattr(self, "publishing_offers"):
            self.publishing_offers = []
        self.publishing_offers.append(offer)
        
        # Email Notification
        msg = self.get_text('publisher_deal_info_email', studio=studio, game=game_name, quality=quality, cost=marketing_cost, share=int(player_share*100))
        self.emails.append(Email(
            sender=self.get_text('sender_headhunter'), 
            subject=self.get_text('publisher_deals_title'), 
            body=msg, 
            date_week=self.week, 
            is_bug=False
        ))

    def accept_publishing_offer(self, idx):
        """Akzeptiert ein Angebot und startet den Verkauf."""
        if not hasattr(self, "publishing_offers") or idx < 0 or idx >= len(self.publishing_offers):
            return False, "invalid_offer"
            
        offer = self.publishing_offers[idx]
        if self.money < offer.marketing_cost:
            return False, "not_enough_money"
            
        self.track_expense("marketing", offer.marketing_cost)
             
        game = PublishedThirdPartyGame(offer)
        
        if not hasattr(self, "published_third_party_games"):
            self.published_third_party_games = []
        self.published_third_party_games.append(game)
        
        self.publishing_offers.pop(idx)
        return True, "success"

    def reject_publishing_offer(self, idx):
        """Lehnt ein Angebot ab und löscht es."""
        if hasattr(self, "publishing_offers") and 0 <= idx < len(self.publishing_offers):
            self.publishing_offers.pop(idx)
            return True
        return False

    def build_presswerk(self):
        """Baut ein eigenes Presswerk. Voraussetzung: Studio-Level 2 und 500k Euro."""
        cost = 500000
        if self.office_level < 2:
            return False, "office_too_small"
        if self.has_presswerk:
            return False, "already_built"
        if self.money < cost:
            return False, "no_money"
            
        self.track_expense("production", cost)
        self.has_presswerk = True
        self.storage_capacity = 50000 # Startkapazität
        return True, "success"

    def expand_storage(self):
        """Erweitert das Lager um 100.000 Einheiten für 100.000 Euro."""
        cost = 100000
        if not self.has_presswerk:
            return False, "no_presswerk"
        if self.money < cost:
            return False, "no_money"
            
        self.track_expense("production", cost)
        self.storage_capacity += 100000
        return True, "success"

    def produce_copies(self, game_index, amount):
        """Produziert physische Kopien eines Spiels."""
        if not self.has_presswerk:
            return False, "no_presswerk"
        if game_index < 0 or game_index >= len(self.game_history):
            return False, "invalid_game"
            
        game = self.game_history[game_index]
        if not game.is_active:
            return False, "game_inactive"
            
        # Kosten pro Kopie: 1.50 Euro
        unit_cost = 1.5
        total_cost = int(amount * unit_cost)
        
        if self.money < total_cost:
            return False, "no_money"
        if self.used_storage + amount > self.storage_capacity:
            return False, "no_storage"
            
        self.track_expense("production", total_cost)
        game.physical_copies = getattr(game, "physical_copies", 0) + amount
        # Wir setzen den Retail-Preis auf 45 Euro, falls nicht vorhanden
        if not hasattr(game, "physical_price"):
            game.physical_price = 45
            
        self.used_storage += amount
        return True, "success"
            
        return True, "success"

    def has_office_bonus(self, bonus_name):
        """Prüft ob ein bestimmter Bonus (z.B. 'research', 'mmo') durch Einrichtung aktiv ist."""
        for item in self.office_items:
            # Suche in game_data.BUILD_OBJECTS nach dem Bonus
            from game_data import BUILD_OBJECTS
            obj_def = BUILD_OBJECTS.get(item["type"], {})
            if obj_def.get("bonus") == bonus_name:
                return True
        return False

    def place_office_item(self, item_type, x, y):
        """Platziert ein Objekt im Büro-Grid (Ebenen-basiert)."""
        from game_data import BUILD_OBJECTS
        obj_def = BUILD_OBJECTS.get(item_type)
        if not obj_def:
            return False, "invalid_item"
            
        cost = obj_def.get("cost", 0)
        if self.money < cost:
            return False, "no_money"

        # Check adjacence requirement (e.g. door needs wall)
        if obj_def.get("requires_adjacent_wall"):
            adjacent_wall = False
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    neighbor = self.office_grid[ny][nx]
                    if neighbor and neighbor["type"] == "wall":
                        adjacent_wall = True
                        break
            if not adjacent_wall:
                return False, "needs_wall"
        
        # Grid collision check
        if self.office_grid[y][x] is not None:
            return False, "collision"
            
        # Pay
        self.track_expense("other", cost)
            
        # Place
        item_data = {
            "type": item_type,
            "x": x,
            "y": y,
            "width": 1,
            "height": 1,
            "employees": obj_def.get("employees", 0)
        }
        from models import OfficeObject
        obj = OfficeObject.from_dict({"object_type": item_type, "x": x, "y": y, "level": 1})
        
        if not hasattr(self, "office_items"): self.office_items = []
        if not hasattr(self, "office_objects"): self.office_objects = []
        
        self.office_items.append(item_data)
        self.office_objects.append(obj)
        self.office_grid[y][x] = obj
                
        return True, "success"

    def remove_office_item(self, x, y):
        """Entfernt ein Objekt und erstattet 50% der Kosten."""
        item = getattr(self, "office_grid", [[None]*10]*10)[y][x]
        if not item: return False
        
        # Mitarbeiter Limit check if it's a desk
        if item.get("employees", 0) > 0:
            current = len(self.employees)
            future_max = self.get_max_employees() - item.get("employees", 0)
            if current > future_max:
                return False 
            
        # Remove
        if item in self.office_items:
            self.office_items.remove(item)
        
        # Also remove from office_objects if it's an OfficeObject or find the matching one
        if hasattr(self, "office_objects"):
            to_remove = None
            for obj in self.office_objects:
                if obj.x == x and obj.y == y:
                    to_remove = obj
                    break
            if to_remove:
                self.office_objects.remove(to_remove)
                
        self.office_grid[y][x] = None
        
        # Refund 50%
        from game_data import BUILD_OBJECTS
        obj_def = BUILD_OBJECTS.get(item.get("type"), {})
        self.track_income("other", obj_def.get("cost", 0) * 0.5)
        
        return True

    def get_office_item(self, x, y):
        return self.office_grid[y][x]

    def place_office_room(self, x1, y1, x2, y2, room_type):
        """Platziert einen Raum im Büro-Raster."""
        from game_data import OFFICE_ROOM_TYPES
        room_data = next((r for r in OFFICE_ROOM_TYPES if r["id"] == room_type), None)
        if not room_data: return False
        
        width = x2 - x1 + 1
        height = y2 - y1 + 1
        cost = width * height * room_data["cost_per_tile"]
        
        if self.money < cost: return False
        
        # Check if area is within grid
        if x1 < 0 or y1 < 0 or x2 >= len(self.office_grid) or y2 >= len(self.office_grid[0]):
            return False
            
        self.track_expense("other", cost)
        
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.office_grid[x][y] = room_type
        return True

    def buy_office_furniture(self, x, y, item_id):
        """Kauft ein Möbelstück und platziert es."""
        from game_data import FURNITURE_DATA
        item_data = next((f for f in FURNITURE_DATA if f["id"] == item_id), None)
        if not item_data: return False
        
        if self.money < item_data["cost"]: return False
        
        # Check grid
        if x < 0 or x >= len(self.office_grid) or y < 0 or y >= len(self.office_grid[0]):
            return False
            
        # Nur in Räumen platzierbar? (Optional: Desk nur in 'dev' Raum)
        # room = self.office_grid[x][y]
        
        self.track_expense("other", item_data["cost"])
        
        new_obj = OfficeObject(item_data["type"], x, y, level=1)
        self.office_objects.append(new_obj)
        return True

    def expand_office_grid(self):
        """Vergrößert das Büro-Raster."""
        cost = 50000 * (len(self.office_grid) // 10)
        if self.money < cost: return False
        
        self.track_expense("other", cost)
        
        new_size = len(self.office_grid) + 5
        new_grid = [[None for _ in range(new_size)] for _ in range(new_size)]
        
        # Copy old grid
        for x in range(len(self.office_grid)):
            for y in range(len(self.office_grid[0])):
                new_grid[x][y] = self.office_grid[x][y]
        
        self.office_grid = new_grid
        return True
