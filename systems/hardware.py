"""Soundkarten-Hardware und Accessibility-Lab. Mixin fuer GameState."""
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


class HardwareMixin:
    def get_accessibility_lab_actions(self):
        """Liefert die verfuegbaren Aktionen fuer das Barrierefreiheits-Labor."""
        return [
            {
                "id": "screenreader_test",
                "name_key": "access_lab_action_screenreader",
                "cost": 4000,
                "reputation": 5,
                "fans": 120,
                "hype": 1.0,
                "bug_reduction": 2,
                "quality_boost": 0.0,
                "quality_weeks": 0,
            },
            {
                "id": "audio_description",
                "name_key": "access_lab_action_audio_description",
                "cost": 9000,
                "reputation": 8,
                "fans": 260,
                "hype": 2.0,
                "bug_reduction": 1,
                "quality_boost": 0.03,
                "quality_weeks": 6,
            },
            {
                "id": "community_beta",
                "name_key": "access_lab_action_community_beta",
                "cost": 15000,
                "reputation": 12,
                "fans": 500,
                "hype": 4.0,
                "bug_reduction": 5,
                "quality_boost": 0.04,
                "quality_weeks": 4,
            },
        ]

    def get_accessibility_weekly_fans(self):
        """Berechnet den passiven woechentlichen Fan-Zuwachs."""
        rep = getattr(self, "accessibility_reputation", 0)
        if rep <= 0:
            return 0
        return min(800, max(1, int(rep * 1.5)))

    def update_accessibility_reputation(self):
        """Wendet den passiven Community-Effekt des Barrierefreiheits-Labors an."""
        weekly_fans = self.get_accessibility_weekly_fans()
        if weekly_fans > 0:
            self.fans += weekly_fans
        if self.active_projects and getattr(self, "accessibility_reputation", 0) >= 50:
            self.hype = min(250, self.hype + 0.1)

        rep = getattr(self, "accessibility_reputation", 0)
        current_year = self.get_calendar_year()
        if rep >= 40 and current_year > getattr(self, "last_accessibility_grant_year", 0):
            grant_amount = int(10000 + rep * 500)
            self.track_income("other", grant_amount)
            self.last_accessibility_grant_year = current_year
            self.emails.insert(0, Email(
                sender=self.get_text('sender_system'),
                subject=self.get_text('subject_access_grant'),
                body=self.get_text('body_access_grant', amount=grant_amount, score=rep),
                date_week=self.week
            ))
        return weekly_fans

    def run_accessibility_lab_action(self, action_id):
        """Fuehrt eine Aktion im Barrierefreiheits-Labor aus."""
        action = next((a for a in self.get_accessibility_lab_actions() if a["id"] == action_id), None)
        if not action:
            return False, "invalid"
        if self.money < action["cost"]:
            return False, "no_money"

        self.track_expense("research", action["cost"])
        self.accessibility_reputation = min(
            100,
            getattr(self, "accessibility_reputation", 0) + action["reputation"]
        )
        self.fans = max(0, self.fans + action["fans"])
        self.hype = min(250, self.hype + action["hype"])

        bug_reduction = action.get("bug_reduction", 0)
        if bug_reduction:
            for ap in self.active_projects:
                ap["bugs"] = max(0, ap.get("bugs", 0) - bug_reduction)

        if action.get("quality_boost", 0) > 0:
            self.temp_quality_boost = max(
                getattr(self, "temp_quality_boost", 0.0),
                action["quality_boost"]
            )
            self.temp_quality_weeks = max(
                getattr(self, "temp_quality_weeks", 0),
                action["quality_weeks"]
            )

        self.accessibility_lab_history.append({
            "week": self.week,
            "action_id": action["id"],
            "cost": action["cost"],
            "reputation": action["reputation"],
        })
        if hasattr(self, "_check_achievements"):
            self._check_achievements()
        return True, action

    def start_sound_card_project(self, name: str, features: list) -> bool:
        """Startet ein neues Soundkarten-Entwicklungsprojekt."""
        if self.get_calendar_year() < 1980:
            return False
            
        # Entwicklungskosten berechnen
        from game_data import HARDWARE_TECH_LIST
        dev_cost = 20000 # Grundkosten
        for tech_id in features:
            tech = next((t for t in HARDWARE_TECH_LIST if t["id"] == tech_id), None)
            if tech:
                dev_cost += tech["cost"]
                
        if self.money < dev_cost:
            return False
            
        self.track_expense("hardware", dev_cost)
        
        from models import SoundCardProject
        project = SoundCardProject(
            name=name,
            features=features,
            dev_cost=dev_cost,
            progress=0.0
        )
        self.sound_card_projects.append(project)
        return True

    def unlock_hardware_technology(self, tech_id: str) -> bool:
        """Schaltet eine Soundkarten-Technologie frei (Lizenzkauf)."""
        from game_data import HARDWARE_TECH_LIST
        tech = next((t for t in HARDWARE_TECH_LIST if t["id"] == tech_id), None)
        if not tech:
            return False
            
        if tech_id in self.unlocked_hardware_tech:
            return False
            
        # Jahr prüfen
        if self.get_calendar_year() < tech["year"]:
            return False
            
        if self.money < tech["cost"]:
            return False
            
        self.track_expense("hardware", tech["cost"])
        self.unlocked_hardware_tech.append(tech_id)
        return True

    def update_hardware_development(self):
        """Aktualisiert wöchentlich den Entwicklungsfortschritt von Soundkarten."""
        # Nur ein unfertiges Projekt kann gleichzeitig entwickelt werden
        active_proj = next((p for p in self.sound_card_projects if not p.is_released), None)
        if not active_proj:
            return
            
        # Fortschrittsgeschwindigkeit
        active_emps = self._active_employees()
        if active_emps:
            avg_speed = sum(e.speed for e in active_emps) / len(active_emps) if active_emps else 0
        else:
            avg_speed = 30.0 # Standard
            
        # Jede Woche ca. 8% bis 15% Fortschritt basierend auf Mitarbeitern
        prog_inc = 5.0 + (avg_speed / 10.0)
        active_proj.progress = min(100.0, active_proj.progress + prog_inc)

    def release_sound_card(self, card_name: str) -> bool:
        """Veröffentlicht eine fertig entwickelte Soundkarte."""
        card = next((p for p in self.sound_card_projects if p.name == card_name and not p.is_released), None)
        if not card or card.progress < 100.0:
            return False
            
        card.is_released = True
        card.weeks_on_market = 0
        
        # Vorherige Karten verlieren an Marktanteil, wenn eine neue veröffentlicht wird
        for other_card in self.sound_card_projects:
            if other_card.is_released and other_card.name != card_name:
                other_card.market_share *= 0.5
                
        return True
