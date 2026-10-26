"""Speichern/Laden und globale Einstellungen. Mixin fuer GameState."""
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


class PersistenceMixin:
    def load_global_settings(self):
        """Lädt systemweite Einstellungen inkl. Keybindings."""
        sets = {}
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r", encoding="utf-8") as f:
                    sets = json.load(f)
            except Exception:
                pass
                
        # Bestehende Settings aktualisieren statt komplett zu ersetzen (erhält Defaults)
        self.settings.update(sets)
        self.completed_tutorials = self.settings.get("completed_tutorials", [])
        
        # Tasten auslesen (falls vorhanden), ansonsten Standard lassen
        import pygame
        self.key_up = self.settings.get("key_up", pygame.K_UP)
        self.key_down = self.settings.get("key_down", pygame.K_DOWN)
        self.key_left = self.settings.get("key_left", pygame.K_LEFT)
        self.key_right = self.settings.get("key_right", pygame.K_RIGHT)
        self.key_confirm = self.settings.get("key_confirm", pygame.K_RETURN)
        self.key_back = self.settings.get("key_back", pygame.K_BACKSPACE)
        self.key_home = self.settings.get("key_home", pygame.K_HOME)
        self.key_end = self.settings.get("key_end", pygame.K_END)
        
        return self.settings

    def save_global_settings(self):
        """Speichert globale Einstellungen ab."""
        self.settings["key_up"] = self.key_up
        self.settings["key_down"] = self.key_down
        self.settings["key_left"] = self.key_left
        self.settings["key_right"] = self.key_right
        self.settings["key_confirm"] = self.key_confirm
        self.settings["key_back"] = self.key_back
        self.settings["key_home"] = self.key_home
        self.settings["key_end"] = self.key_end
        self.settings["completed_tutorials"] = self.completed_tutorials
        
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def save_game(self, slot=1):
        """Speichert den Spielstand in einem Slot."""
        filepath = f"save_slot_{slot}.json"
        data = {
            "company_name": self.company_name,
            "money": self.money,
            "fans": self.fans,
            "week": self.week,
            "high_score": self.high_score,
            "games_made": self.games_made,
            "total_revenue": self.total_revenue,
            "corporate_warfare": self.corporate_warfare.to_dict(),
            "union_manager": self.union_manager.to_dict(),
            "stock_manager": self.stock_manager.to_dict(),
            "subscription_manager": self.subscription_manager.to_dict(),
            "monetization_manager": self.monetization_manager.to_dict(),
            "publishing_manager": self.publishing_manager.to_dict(),
            "crypto_manager": self.crypto_manager.to_dict(),
            "monopoly_manager": self.monopoly_manager.to_dict(),
            "global_event_manager": self.global_event_manager.to_dict(),
            "office_level": self.office_level,
            "last_event_week": self.last_event_week,
            "last_trend_week": self.last_trend_week,
            "current_trend": self.current_trend,
            "active_events": getattr(self, "active_events", []),
            "settings": self.settings,
            "game_history": [g.to_dict() for g in self.game_history],
            "active_mmos": [m.to_dict() for m in getattr(self, "active_mmos", [])],
            "port_projects": [p.to_dict() for p in getattr(self, "port_projects", [])],
            "employees": [e.to_dict() for e in self.employees],
            "engines": [
                {"name": eng.name, "is_licensed": eng.is_licensed, "license_fee": eng.license_fee, 
                 "is_third_party": getattr(eng, "is_third_party", False), 
                 "usage_cost": getattr(eng, "usage_cost", 0), 
                 "revenue_share": getattr(eng, "revenue_share", 0.0), 
                 "features": [
                    {"category": f.category, "name": f.name, "tech_bonus": f.tech_bonus}
                    for f in eng.features
                ]} for eng in self.engines
            ],
            "unlocked_features": [
                {"category": f.category, "name": f.name, "tech_bonus": f.tech_bonus}
                for f in self.unlocked_features
            ],
            "unlocked_topics": self.unlocked_topics,
            "unlocked_genres": self.unlocked_genres,
            "unlocked_audiences": self.unlocked_audiences,
            "unlocked_technologies": self.unlocked_technologies,
            "bought_platforms": getattr(self, "bought_platforms", []),
            "active_platforms": getattr(self, "active_platforms", []),
            "unlocked_platforms": getattr(self, "unlocked_platforms", []),
            "rivals": [r.to_dict() for r in getattr(self, "rivals", [])],
            "last_goty_year": getattr(self, "last_goty_year", 0),
            "bank_loan": self.bank_loan.to_dict() if getattr(self, "bank_loan", None) else None,
            "accounting": getattr(self, "accounting", {"income": 0, "expenses": 0, "loan_paid": 0}),
            "custom_consoles": [c.to_dict() for c in getattr(self, "custom_consoles", [])],
            "emails": [
                {
                    "sender": m.sender, "subject": m.subject, "body": m.body,
                    "date_week": m.date_week, "game_name": m.game_name,
                    "is_bug": m.is_bug, "is_read": m.is_read
                } for m in self.emails
            ],
            "has_presswerk": getattr(self, "has_presswerk", False),
            "storage_capacity": getattr(self, "storage_capacity", 0),
            "used_storage": getattr(self, "used_storage", 0),
            "has_server_room": getattr(self, "has_server_room", False),
            "server_capacity": getattr(self, "server_capacity", 0),
            "publishing_offers": [o.to_dict() for o in getattr(self, "publishing_offers", [])],
            "published_third_party_games": [g.to_dict() for g in getattr(self, "published_third_party_games", [])],
            "office_items": getattr(self, "office_items", []),
            "office_objects": [(obj.to_dict() if hasattr(obj, 'to_dict') else obj) for obj in getattr(self, "office_objects", [])],
            "active_projects": [
                {
                    "project": ap["project"].to_dict(),
                    "progress": ap["progress"],
                    "total_weeks": ap["total_weeks"],
                    "bugs": ap["bugs"],
                    "crunch": ap.get("crunch", False),
                    "ready_to_finish": ap.get("ready_to_finish", False),
                    "event_count": ap.get("event_count", 0),
                    "aaa_event_done": ap.get("aaa_event_done", False),
                    "co_dev": ap.get("co_dev")
                } for ap in self.active_projects
            ],
            "soundcon_history": [s.to_dict() for s in getattr(self, "soundcon_history", [])],
            "soundcon_last_year": getattr(self, "soundcon_last_year", 0),
            "active_soundcon": self.active_soundcon.to_dict() if getattr(self, "active_soundcon", None) else None,
            "pending_soundcon_result": getattr(self, "pending_soundcon_result", None),
            "radio_contracts": [c.to_dict() for c in getattr(self, "radio_contracts", [])],
            "soundtrack_label": self.soundtrack_label.to_dict() if getattr(self, "soundtrack_label", None) else {},
            "podcast_network": self.podcast_network.to_dict() if hasattr(self, "podcast_network") else {},
            "audio_pass": self.audio_pass.to_dict() if getattr(self, "audio_pass", None) else {},
            "cloud_gaming": self.cloud_gaming.to_dict() if getattr(self, "cloud_gaming", None) else {},
            "fan_mail_inbox": [m.to_dict() for m in getattr(self, "fan_mail_inbox", [])],
            "sound_card_projects": [p.to_dict() for p in getattr(self, "sound_card_projects", [])],
            "custom_consoles": [c.to_dict() for c in getattr(self, "custom_consoles", [])],
            "active_custom_console": getattr(self, "active_custom_console").to_dict() if getattr(self, "active_custom_console", None) else None,
            "active_jingles": [{"jingle": j.to_dict(), "weeks_left": getattr(j, "weeks_left", 4)} for j in getattr(self, "active_jingles", [])],
            "unlocked_hardware_tech": getattr(self, "unlocked_hardware_tech", []),
            "it_upgrades": getattr(self, "it_upgrades", []),
            "active_cyber_effects": getattr(self, "active_cyber_effects", []),
            "current_convention_booking": getattr(self, "current_convention_booking", None),
            "active_personality_event": getattr(self, "active_personality_event", None),
            "active_personality_employee_name": self.active_personality_employee.name if getattr(self, "active_personality_employee", None) else None,
            "temp_dev_speed_penalty": getattr(self, "temp_dev_speed_penalty", 1.0),
            "temp_dev_speed_weeks": getattr(self, "temp_dev_speed_weeks", 0),
            "temp_quality_boost": getattr(self, "temp_quality_boost", 0.0),
            "temp_quality_weeks": getattr(self, "temp_quality_weeks", 0),
            "accessibility_reputation": getattr(self, "accessibility_reputation", 0),
            "accessibility_lab_history": getattr(self, "accessibility_lab_history", []),
            "last_accessibility_grant_year": getattr(self, "last_accessibility_grant_year", 0),
            "unlocked_achievements": getattr(self, "unlocked_achievements", []),
            "my_goty_wins": getattr(self, "my_goty_wins", 0),
            "esports_leagues": [l.to_dict() for l in getattr(self, "esports_leagues", [])],
            "difficulty": getattr(self, "difficulty", 1),
            "research_points": getattr(self, "research_points", 0),
            "prestige": getattr(self, "prestige", 0),
            "tax_rate": getattr(self, "tax_rate", 0.15),
            "sales_multiplier": getattr(self, "sales_multiplier", 1.0),
            "profit_multiplier": getattr(self, "profit_multiplier", 1.0),
            "logic_multiplier": getattr(self, "logic_multiplier", 1.0),
            "hype_multiplier": getattr(self, "hype_multiplier", 1.0),
            "dev_speed_multiplier": getattr(self, "dev_speed_multiplier", 1.0),
            "interest_rate": getattr(self, "interest_rate", 0.05),
            "marketing_efficiency": getattr(self, "marketing_efficiency", 1.0),
            "streamer_hype_multi": getattr(self, "streamer_hype_multi", 1.0),
            "quality_standard_multi": getattr(self, "quality_standard_multi", 1.0),
            "subscription_multi": getattr(self, "subscription_multi", 1.0),
            "goty_history": getattr(self, "goty_history", {}),
            "chart_history": getattr(self, "chart_history", []),
            "streaming_platform": self.streaming_platform.to_dict() if getattr(self, "streaming_platform", None) else None,
            "subscription_active": getattr(self, "subscription_active", False),
            "subscription_price": getattr(self, "subscription_price", 9.99),
            "subscription_subscribers": getattr(self, "subscription_subscribers", 0),
            "subscription_hype": getattr(self, "subscription_hype", 0.0),
            "financial_history": getattr(self, "financial_history", []),
            "bank_statements": [s.to_dict() for s in getattr(self, "bank_statements", [])],
            "owned_licenses": getattr(self, "owned_licenses", []),
            "active_addons": [a.to_dict() for a in getattr(self, "active_addons", [])],
            "active_bundles": [b.to_dict() for b in getattr(self, "active_bundles", [])],
            "active_merch_campaigns": [m.to_dict() for m in getattr(self, "active_merch_campaigns", [])],
            "manufacturing_jobs": [m.to_dict() for m in getattr(self, "manufacturing_jobs", [])],
            "active_merch": getattr(self, "active_merch", []),
            "active_tournaments": getattr(self, "active_tournaments", []),
            "active_sponsorships": getattr(self, "active_sponsorships", []),
            "active_crowdfundings": getattr(self, "active_crowdfundings", []),
            "failed_crowdfundings": getattr(self, "failed_crowdfundings", 0),
            "support_level": getattr(self, "support_level", 0),
            "qa_level": getattr(self, "qa_level", 0),
            "is_developing_console": getattr(self, "is_developing_console", False),
            "console_progress": getattr(self, "console_progress", 0),
            "console_total_weeks": getattr(self, "console_total_weeks", 48)
        }
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_str)
            
        # --- ANTI-CHEAT ---
        import hashlib, ctypes
        try:
            bak_path = f"save_slot_{slot}.bak"
            if os.path.exists(bak_path):
                ctypes.windll.kernel32.SetFileAttributesW(bak_path, 128) # 128 = NORMAL
            expected_hash = hashlib.sha256((json_str + "SuperSecretAntiCheatSalt123").encode("utf-8")).hexdigest()
            with open(bak_path, "w", encoding="utf-8") as f:
                json.dump({"hash": expected_hash}, f)
            ctypes.windll.kernel32.SetFileAttributesW(bak_path, 2)
        except Exception as e:
            print(f"Anti-Cheat Save Error: {e}")
            
        return True

    def delete_save_game(self, slot=1):
        """Löscht einen Spielstand und dessen Anti-Cheat Backup restlos."""
        filepath = f"save_slot_{slot}.json"
        bak_path = f"save_slot_{slot}.bak"
        
        # Lösche Haupt-Savegame
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass
                
        # Lösche verstecktes Backup
        if os.path.exists(bak_path):
            import ctypes
            try:
                # Schreibschutz/Hidden-Flag aufheben, um Datei löschen zu können
                ctypes.windll.kernel32.SetFileAttributesW(bak_path, 128) # FILE_ATTRIBUTE_NORMAL
                os.remove(bak_path)
            except Exception:
                pass
        
        return True

    def get_save_slots_info(self):
        """Gibt Infos über die 3 verfügbaren Slots zurück."""
        slots = {}
        for i in range(1, 4):
            path = f"save_slot_{i}.json"
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    slots[i] = f"Slot {i}: {data['company_name']} (Woche {data['week']}, {data['money']:,} Euro)"
                except Exception:
                    slots[i] = f"Slot {i}: [FEHLERHAFT]"
            else:
                slots[i] = f"Slot {i}: [LEER]"
        return slots

    def load_game(self, slot=1):
        """Lädt einen Spielstand aus einem Slot."""
        filepath = f"save_slot_{slot}.json"
        if not os.path.exists(filepath):
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            json_str = f.read()
            data = json.loads(json_str)

        # --- ANTI-CHEAT ---
        bak_path = f"save_slot_{slot}.bak"
        if os.path.exists(bak_path):
            import hashlib
            try:
                with open(bak_path, "r", encoding="utf-8") as f:
                    bak_data = json.load(f)
                expected_hash = hashlib.sha256((json_str + "SuperSecretAntiCheatSalt123").encode("utf-8")).hexdigest()
                if bak_data.get("hash") != expected_hash:
                    print(f"[Anti-Cheat] Manipulation detected! Expected: {bak_data.get('hash')}, Got: {expected_hash}")
                    return False
            except Exception:
                return False

        self.company_name = data["company_name"]
        self.money = data["money"]
        self.fans = data["fans"]
        self.week = data["week"]
        self.high_score = data["high_score"]
        self.games_made = data["games_made"]
        self.total_revenue = data["total_revenue"]
        if "corporate_warfare" in data:
            self.corporate_warfare.from_dict(data["corporate_warfare"])
        if "union_manager" in data:
            self.union_manager.from_dict(data["union_manager"])
        if "stock_manager" in data:
            self.stock_manager.from_dict(data["stock_manager"])
        if "subscription_manager" in data:
            self.subscription_manager.from_dict(data["subscription_manager"])
        if "monetization_manager" in data:
            self.monetization_manager.from_dict(data["monetization_manager"])
        if "publishing_manager" in data:
            self.publishing_manager.from_dict(data["publishing_manager"])
        if "crypto_manager" in data:
            self.crypto_manager.from_dict(data["crypto_manager"])
        if "monopoly_manager" in data:
            self.monopoly_manager.from_dict(data["monopoly_manager"])
        if "global_event_manager" in data:
            self.global_event_manager.from_dict(data["global_event_manager"])
        self.office_level = data["office_level"]
        self.last_event_week = data.get("last_event_week", 0)
        self.last_trend_week = data.get("last_trend_week", 0)
        self.current_trend = data.get("current_trend")
        self.active_events = data.get("active_events", [])
        self.metaverse_land_value = data.get("metaverse_land_value", 0.0)
        self.metaverse_investment = data.get("metaverse_investment", 0.0)
        self.metaverse_weeks_active = data.get("metaverse_weeks_active", 0)
        self.metaverse_burst = data.get("metaverse_burst", False)
        self.metaverse_land_value = data.get("metaverse_land_value", 0.0)
        self.metaverse_investment = data.get("metaverse_investment", 0.0)
        self.metaverse_weeks_active = data.get("metaverse_weeks_active", 0)
        self.metaverse_burst = data.get("metaverse_burst", False)
        self.has_presswerk = data.get("has_presswerk", False)
        self.storage_capacity = data.get("storage_capacity", 0)
        self.used_storage = data.get("used_storage", 0)
        self.has_server_room = data.get("has_server_room", False)
        self.server_capacity = data.get("server_capacity", 0)

        # Publisher Rolle laden
        self.publishing_offers = []
        if "publishing_offers" in data:
            for od in data["publishing_offers"]:
                self.publishing_offers.append(PublishingOffer(
                    od["studio_name"], od["game_name"], od["genre"], od["quality"], od["marketing_cost"], od["player_share"]
                ))

        self.published_third_party_games = []
        if "published_third_party_games" in data:
            for gd in data["published_third_party_games"]:
                dummy_offer = PublishingOffer(gd["studio_name"], gd["game_name"], gd["genre"], gd["quality"], 0, gd["player_share"])
                g = PublishedThirdPartyGame(dummy_offer)
                g.weeks_on_market = gd.get("weeks_on_market", 0)
                g.is_active = gd.get("is_active", True)
                g.total_sales = gd.get("total_sales", 0)
                g.total_revenue = gd.get("total_revenue", 0)
                g.player_profit = gd.get("player_profit", 0)
                self.published_third_party_games.append(g)

        # Engines laden
        self.unlocked_features = []
        for fd in data.get("unlocked_features", []):
            self.unlocked_features.append(
                EngineFeature(fd["category"], fd["name"], fd["tech_bonus"])
            )
        self.unlocked_topics = data.get("unlocked_topics", list(START_TOPICS))
        self.unlocked_genres = data.get("unlocked_genres", list(START_GENRES))
        self.unlocked_audiences = data.get("unlocked_audiences", list(START_AUDIENCES))
        self.unlocked_technologies = data.get("unlocked_technologies", [])

        self.engines = []
        for ed in data.get("engines", []):
            features = [
                EngineFeature(fd["category"], fd["name"], fd["tech_bonus"])
                for fd in ed["features"]
            ]
            eng = Engine(
                ed["name"], features, 
                is_third_party=ed.get("is_third_party", False),
                usage_cost=ed.get("usage_cost", 0),
                revenue_share=ed.get("revenue_share", 0.0)
            )
            eng.is_licensed = ed.get("is_licensed", False)
            eng.license_fee = ed.get("license_fee", 0)
            self.engines.append(eng)

        # Spielhistorie laden
        self.game_history = []
        for gd in data.get("game_history", []):
            self.game_history.append(GameProject.from_dict(gd))

        # Aktive MMOs laden
        self.active_mmos = []
        if "active_mmos" in data:
            for md in data["active_mmos"]:
                match_game = next((g for g in self.game_history if g.name == md.get("game_dict", {}).get("name")), None)
                if match_game:
                    m = ActiveMMO(match_game, md.get("players", 0), md.get("payment_model", "Abo"))
                    m.subscription_fee = md.get("subscription_fee", 15)
                    m.server_cost_per_10k = md.get("server_cost_per_10k", 5000)
                    m.weeks_active = md.get("weeks_active", 0)
                    self.active_mmos.append(m)

        self.port_projects = []
        if "port_projects" in data:
            from models import PortProject
            for pd in data["port_projects"]:
                port = PortProject(pd["original_game_name"], pd["new_platform"], pd["dev_cost"], pd["total_weeks"])
                port.progress = pd.get("progress", 0.0)
                port.is_finished = pd.get("is_finished", False)
                self.port_projects.append(port)

        # Mitarbeiter laden
        self.employees = []
        for ed in data.get("employees", []):
            emp = Employee.from_dict(ed)
            # Falls Trait fehlt (Migration), zufällig zuweisen
            if not emp.trait:

                from game_data import EMPLOYEE_TRAITS
                emp.trait = random.choice(EMPLOYEE_TRAITS)
            self.employees.append(emp)

        # E-Mails laden
        self.emails = []
        for md in data.get("emails", []):
            mail = Email(md["sender"], md["subject"], md["body"], md["date_week"], md.get("game_name"), md.get("is_bug", False))
            mail.is_read = md.get("is_read", False)
            self.emails.append(mail)

        self.settings = data.get("settings", {"language": "de", "music_enabled": True})

        # Rivalen laden
        # Aktive Projekte laden
        self.active_projects = []
        for ad in data.get("active_projects", []):
            if ad.get("is_contract"):
                from models import ContractWorkProject
                proj = ContractWorkProject.from_dict(ad["project"])
            else:
                from models import GameProject
                proj = GameProject.from_dict(ad["project"])
            
            self.active_projects.append({
                "project": proj,
                "progress": ad["progress"],
                "total_weeks": ad["total_weeks"],
                "bugs": ad.get("bugs", 0),
                "crunch": ad.get("crunch", False),
                "ready_to_finish": ad.get("ready_to_finish", False),
                "event_count": ad.get("event_count", 0),
                "aaa_event_done": ad.get("aaa_event_done", False),
                "co_dev": ad.get("co_dev")
            })
        self.rivals = []
        for r_data in data.get("rivals", []):
            games = []
            for g_data in r_data.get("games", []):
                rg = RivalGame(g_data["name"], g_data["topic"], g_data["genre"], g_data["score"], g_data["weeks_on_market"])
                rg.is_active = g_data.get("is_active", True)
                games.append(rg)
            rival = RivalStudio(r_data["name"], r_data.get("target_market_share", 10), games, r_data.get("next_release_week"))
            self.rivals.append(rival)
            
        if not self.rivals:
            self.rivals = self._init_rivals()
            
        self.last_goty_year = data.get("last_goty_year", 0)
        self.bought_platforms = data.get("bought_platforms", ["PC (MS-DOS)"])
        self.active_platforms = data.get("active_platforms", [p['name'] for p in get_available_platforms(self.week)])
        self.unlocked_platforms = data.get("unlocked_platforms", [])
        
        # Finanzen laden
        self.accounting = data.get("accounting", {"income": 0, "expenses": 0, "loan_paid": 0})
        loan_data = data.get("bank_loan")
        if loan_data:
            self.bank_loan = BankLoan(
                loan_data["amount_borrowed"], 0, loan_data["weeks_remaining"], 
                amount_remaining=loan_data["amount_remaining"], 
                weeks_remaining=loan_data["weeks_remaining"]
            )
            self.bank_loan.weekly_payment = loan_data["weekly_payment"]
        else:
            self.bank_loan = None
            
        self.custom_consoles = []
        if "custom_consoles" in data:
            for c_data in data["custom_consoles"]:
                cc = CustomConsole(
                    c_data["name"],
                    c_data.get("architecture", "Custom"),
                    c_data.get("performance", c_data.get("tech_level", 5)),
                    c_data.get("marketing_budget", 1000000),
                    c_data["dev_cost"],
                    c_data["release_week"]
                )
                cc.market_share = c_data.get("market_share", 0.05)
                self.custom_consoles.append(cc)

        # Büro laden & Migrieren
        self.office_items = data.get("office_items", [])
        self.office_objects = []
        
        # Versuche office_objects direkt zu laden
        objects_data = data.get("office_objects")
        if objects_data:
            from models import OfficeObject
            for od in objects_data:
                if isinstance(od, dict) and "object_type" in od:
                    self.office_objects.append(OfficeObject.from_dict(od))
                else:
                    self.office_objects.append(od)
        
        self.office_grid = [[None for _ in range(10)] for _ in range(10)]
        
        # Falls office_objects leer war aber office_items existiert (Migration)
        if not self.office_objects and self.office_items:
            from models import OfficeObject
            for item in self.office_items:
                if isinstance(item, dict):
                    y, x = item.get("y", 0), item.get("x", 0)
                    new_obj = OfficeObject(item.get("type", "Desk"), x, y, level=item.get("level", 1))
                    self.office_objects.append(new_obj)
        
        # Grid aus office_objects aufbauen
        for obj in self.office_objects:
            if not hasattr(obj, 'y') or not hasattr(obj, 'x'):
                continue
            y, x = obj.y, obj.x
            if 0 <= y < len(self.office_grid) and 0 <= x < len(self.office_grid[0]):
                self.office_grid[y][x] = obj

        # NEU: SoundCon & Soundtrack-Label laden
        self.soundcon_history = []
        if "soundcon_history" in data:
            for sd in data["soundcon_history"]:
                self.soundcon_history.append(SoundConEvent.from_dict(sd))
        self.soundcon_last_year = data.get("soundcon_last_year", 0)
        
        active_sc = data.get("active_soundcon")
        self.active_soundcon = SoundConEvent.from_dict(active_sc) if active_sc else None
        self.pending_soundcon_result = data.get("pending_soundcon_result")

        if "soundtrack_label" in data:
            self.soundtrack_label = SoundtrackLabel.from_dict(data["soundtrack_label"])
        else:
            self.soundtrack_label = None

        self.difficulty = data.get("difficulty", 1)
        self.research_points = data.get("research_points", 0)
        self.prestige = data.get("prestige", 0)
        self.tax_rate = data.get("tax_rate", 0.15)
        self.sales_multiplier = data.get("sales_multiplier", 1.0)
        self.profit_multiplier = data.get("profit_multiplier", 1.0)
        self.logic_multiplier = data.get("logic_multiplier", 1.0)
        self.hype_multiplier = data.get("hype_multiplier", 1.0)
        self.dev_speed_multiplier = data.get("dev_speed_multiplier", 1.0)
        self.interest_rate = data.get("interest_rate", 0.05)
        self.marketing_efficiency = data.get("marketing_efficiency", 1.0)
        self.streamer_hype_multi = data.get("streamer_hype_multi", 1.0)
        self.quality_standard_multi = data.get("quality_standard_multi", 1.0)
        self.subscription_multi = data.get("subscription_multi", 1.0)
        self.goty_history = data.get("goty_history", {})
        self.chart_history = data.get("chart_history", [])
        
        sp_data = data.get("streaming_platform")
        if sp_data:
            self.streaming_platform = StreamingPlatform.from_dict(sp_data)
        else:
            self.streaming_platform = None
            
        self.subscription_active = data.get("subscription_active", False)
        self.subscription_price = data.get("subscription_price", 9.99)
        self.subscription_subscribers = data.get("subscription_subscribers", 0)
        self.subscription_hype = data.get("subscription_hype", 0.0)
        self.financial_history = data.get("financial_history", [])
        
        self.bank_statements = []
        if "bank_statements" in data:
            for s in data["bank_statements"]:
                self.bank_statements.append(BankStatement(s["week"], s["year"], s["income_items"], s["expense_items"], s["final_balance"]))

        self.owned_licenses = data.get("owned_licenses", [])
        
        self.active_addons = []
        if "active_addons" in data:
            for a in data["active_addons"]:
                self.active_addons.append(AddonProject.from_dict(a) if hasattr(AddonProject, 'from_dict') else a)
                
        self.active_bundles = []
        if "active_bundles" in data:
            for b in data["active_bundles"]:
                self.active_bundles.append(BundleProject.from_dict(b) if hasattr(BundleProject, 'from_dict') else b)
                
        self.active_merch_campaigns = []
        if "active_merch_campaigns" in data:
            from models import MerchCampaign
            for m in data["active_merch_campaigns"]:
                self.active_merch_campaigns.append(MerchCampaign.from_dict(m))

        self.manufacturing_jobs = []
        if "manufacturing_jobs" in data:
            from models import ManufacturingJob
            for m in data["manufacturing_jobs"]:
                mj = ManufacturingJob(m["game_name"], m["amount"], m["cost_per_unit"], m["weeks_to_complete"])
                mj.weeks_left = m.get("weeks_left", mj.weeks_to_complete)
                mj.is_finished = m.get("is_finished", False)
                self.manufacturing_jobs.append(mj)
                
        self.active_merch = data.get("active_merch", [])
        self.active_tournaments = data.get("active_tournaments", [])
        self.active_sponsorships = data.get("active_sponsorships", [])
        self.active_crowdfundings = data.get("active_crowdfundings", [])
        self.failed_crowdfundings = data.get("failed_crowdfundings", 0)
        self.support_level = data.get("support_level", 0)
        self.qa_level = data.get("qa_level", 0)
        self.is_developing_console = data.get("is_developing_console", False)
        self.console_progress = data.get("console_progress", 0)
        self.console_total_weeks = data.get("console_total_weeks", 48)
        self.completed_tutorials = data.get("completed_tutorials", [])
            
        if "podcast_network" in data:
            self.podcast_network = PodcastNetwork.from_dict(data["podcast_network"])
        else:
            self.podcast_network = PodcastNetwork()

        if "audio_pass" in data:
            self.audio_pass = AudioPass.from_dict(data["audio_pass"])
        else:
            self.audio_pass = AudioPass()

        if "cloud_gaming" in data:
            self.cloud_gaming = CloudGamingService.from_dict(data["cloud_gaming"])
        else:
            self.cloud_gaming = CloudGamingService()

        # NEU: v3.11.0-beta.1 Expansion Variables laden
        from models import FanMail, SoundCardProject, RadioJingle
        
        self.fan_mail_inbox = []
        for md in data.get("fan_mail_inbox", []):
            self.fan_mail_inbox.append(FanMail.from_dict(md))
            
        self.sound_card_projects = []

        self.custom_consoles = []
        if "custom_consoles" in data:
            from models import CustomConsoleProject
            for c_data in data["custom_consoles"]:
                self.custom_consoles.append(CustomConsoleProject.from_dict(c_data))
        
        self.active_custom_console = None
        if "active_custom_console" in data and data["active_custom_console"]:
            from models import CustomConsoleProject
            self.active_custom_console = CustomConsoleProject.from_dict(data["active_custom_console"])
            
        for pd in data.get("sound_card_projects", []):
            self.sound_card_projects.append(SoundCardProject.from_dict(pd))
            
        self.active_jingles = []
        for jd in data.get("active_jingles", []):
            j = RadioJingle.from_dict(jd["jingle"])
            j.weeks_left = jd.get("weeks_left", 4)
            self.active_jingles.append(j)
            
        self.unlocked_hardware_tech = data.get("unlocked_hardware_tech", [])
        self.it_upgrades = data.get("it_upgrades", [])
        self.active_cyber_effects = data.get("active_cyber_effects", [])
        self.current_convention_booking = data.get("current_convention_booking", None)
        self.active_personality_event = data.get("active_personality_event", None)
        
        emp_name = data.get("active_personality_employee_name")
        if emp_name:
            self.active_personality_employee = next((e for e in self.employees if e.name == emp_name), None)
            if not self.active_personality_employee and self.employees:
                self.active_personality_employee = self.employees[0]
        else:
            self.active_personality_employee = None
            
        self.temp_dev_speed_penalty = data.get("temp_dev_speed_penalty", 1.0)
        self.temp_dev_speed_weeks = data.get("temp_dev_speed_weeks", 0)
        self.temp_quality_boost = data.get("temp_quality_boost", 0.0)
        self.temp_quality_weeks = data.get("temp_quality_weeks", 0)
        self.accessibility_reputation = data.get("accessibility_reputation", 0)
        self.accessibility_lab_history = data.get("accessibility_lab_history", [])
        self.last_accessibility_grant_year = data.get("last_accessibility_grant_year", 0)
        self.unlocked_achievements = data.get("unlocked_achievements", [])
        self.my_goty_wins = data.get("my_goty_wins", 0)

        # NEU: E-Sports-Ligen laden
        from models import EsportsLeague
        self.esports_leagues = []
        for ld in data.get("esports_leagues", []):
            self.esports_leagues.append(EsportsLeague.from_dict(ld))

        self.reset_draft()
        return True
