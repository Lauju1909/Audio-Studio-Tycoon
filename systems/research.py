"""Forschung und freischaltbare Inhalte. Mixin fuer GameState."""
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


class ResearchMixin:
    def _init_starter_engine(self):
        """Erstellt die Starter-Engine mit Basis-Features."""
        from game_data import ENGINE_FEATURES
        starter_features = []
        for f_data in ENGINE_FEATURES:
            if f_data["cost"] == 0:
                feat = EngineFeature(f_data["category"], f_data["name"], f_data["tech_bonus"])
                starter_features.append(feat)
                self.unlocked_features.append(feat)

        starter = Engine("Basis-Engine", starter_features)
        self.engines.append(starter)

    def _unlock_historical_topics(self, silent=False):
        """Prüft das aktuelle Jahr und schaltet neue historische Themen und Ereignisse frei."""
        from game_data import get_newly_unlocked_topics, YEAR_EVENTS, START_YEAR
        
        calendar_year = START_YEAR + (self.week - 1) // WEEKS_PER_YEAR
        new_topics = get_newly_unlocked_topics(calendar_year)
        
        # 1. Themen freischalten
        for topic in new_topics:
            name = topic["name"]
            if name not in self.unlocked_topics:
                self.unlocked_topics.append(name)
                if not silent:
                    # E-Mail Benachrichtigung
                    self.emails.insert(0, Email(
                        sender=self.get_text("sender_historian"),
                        subject=self.get_text("subject_new_topic"),
                        body=self.get_text("body_new_topic", topic=self.get_text(name)),
                        date_week=self.week
                    ))

        # 2. Historisches Ereignis verarbeiten
        if calendar_year in YEAR_EVENTS:
            event = YEAR_EVENTS[calendar_year]
            effect_type = event.get("effect")
            val = event.get("value")
            
            if not silent:
                # E-Mail senden
                event_text = self.get_text(event["text"])
                impact_desc = f"{effect_type} -> {val}"
                self.emails.insert(0, Email(
                    sender=self.get_text("sender_world_events"),
                    subject=self.get_text("subject_historical_event", year=calendar_year),
                    body=f"{event_text}\n\n{self.get_text('event_impact')}: {impact_desc}",
                    date_week=self.week
                ))

            # Effekt anwenden
            if effect_type == "money":
                if val > 0: self.track_income("other", val)
                else: self.track_expense("other", abs(val))
            elif effect_type == "money_multi":
                diff = self.money * (val - 1)
                if diff > 0:
                    self.track_income("other", diff)
                elif diff < 0:
                    self.track_expense("other", abs(diff))
            elif effect_type == "fans":
                self.fans += val
            elif effect_type == "hype":
                self.hype = min(250, self.hype + val)
            elif effect_type == "hype_multi":
                self.hype_multiplier *= val
            elif effect_type == "rp":
                self.research_points += val
            elif effect_type == "prestige":
                self.prestige += val
            elif effect_type == "tax_increase":
                self.tax_rate = max(0.0, min(0.99, self.tax_rate + val))
            elif effect_type == "sales_multi":
                self.sales_multiplier *= val
            elif effect_type == "logic_boost":
                self.logic_multiplier *= val
            elif effect_type == "dev_speed":
                self.dev_speed_multiplier *= val
            elif effect_type == "interest_increase":
                self.interest_rate += val
            elif effect_type == "marketing_rev":
                self.marketing_efficiency *= val
            elif effect_type == "streamer_impact":
                self.streamer_hype_multi *= val
            elif effect_type == "subscription_boom" or effect_type == "subscription_standard":
                self.subscription_multi *= val
            elif effect_type == "quality_standard" or effect_type == "story_standard" or effect_type == "graphics_standard":
                self.quality_standard_multi *= val
            elif effect_type == "trend_topic":
                self.current_trend = {
                    'topic': val,
                    'genre': self.current_trend.get('genre', 'Action'),
                    'week_started': self.week
                }
            elif effect_type == "trend_genre":
                self.current_trend = {
                    'topic': self.current_trend.get('topic', 'Fantasy'),
                    'genre': val,
                    'week_started': self.week
                }
            elif effect_type == "trend_difficulty":
                # Schwierigkeit als Trend ist ein neues Konzept, wir merken es uns
                self.difficulty_trend = val 
            elif effect_type == "unlock_tech":
                if val not in self.unlocked_technologies:
                    self.unlocked_technologies.append(val)
            elif effect_type == "unlock_platform":
                from game_data import PLATFORMS
                p_name_part = str(event.get("value", ""))
                # Finde die Plattform, die den Namen enthält
                for p in PLATFORMS:
                    if p_name_part.lower() in p["name"].lower():
                        if p["name"] not in self.unlocked_platforms:
                            self.unlocked_platforms.append(p["name"])
                            # Benachrichtigung via Email
                            self.emails.insert(0, Email(
                                sender=self.get_text('sender_historical'),
                                subject=self.get_text('subject_platform_unlocked', name=p["name"]),
                                body=self.get_text('body_platform_unlocked', name=p["name"]),
                                date_week=self.week
                            ))
                            if hasattr(self, 'audio'):
                                self.audio.play_sound('confirm')
                                self.audio.speak(self.get_text('announce_platform_unlocked', name=p["name"]), interrupt=False)
                        break
            elif effect_type == "game_end":
                self.game_over = True
                self.game_over_reason = "historical_end"

    def get_research_block_reason(self):
        """Gibt den Grund zurück, warum Forschung gerade nicht möglich ist (oder None)."""
        if self.is_researching:
            name = self.current_research_draft['data']['name'] if self.current_research_draft else '?'
            return self.get_text('research_blocked_already_researching', name=name)
        if self.is_developing:
            proj_name = self.active_projects[0]["project"].name if self.active_projects else '?'
            return self.get_text('research_blocked_developing', name=proj_name)
        return None

    def start_research(self, res_data, res_type):
        """Startet ein neues Forschungsprojekt."""
        if self.money < res_data["cost"]:
            return False
        if self.is_researching or self.is_developing:
            return False
            
        self.track_expense("research", res_data["cost"])
        self.is_researching = True
        self.research_progress = 0
        self.research_total_weeks = res_data.get("research_weeks", 4)
        self.current_research_draft = {
            "data": res_data,
            "type": res_type
        }
        return True

    def complete_research(self):
        """Schließt die aktuelle Forschung ab."""
        self.is_researching = False
        if not self.current_research_draft:
            return
            
        res_type = self.current_research_draft["type"]
        res_data = self.current_research_draft["data"]
        
        if res_type == "feature":
            feat = EngineFeature(res_data["category"], res_data["name"], res_data["tech_bonus"])
            self.unlocked_features.append(feat)
        elif res_type == "genre":
            self.unlocked_genres.append(res_data["name"])
        elif res_type == "audience":
            self.unlocked_audiences.append(res_data["name"])
        elif res_type == "topic":
            self.unlocked_topics.append(res_data["name"])
        elif res_type == "technology":
            self.unlocked_technologies.append(res_data["name"])
            
        self.emails.insert(0, Email(
            sender=self.get_text('sender_assistant'),
            subject=self.get_text('subject_research_done'),
            body=self.get_text('body_research_done', name=res_data["name"]),
            date_week=self.week
        ))
        
        # Audio Warnung für abgeschlossene Forschung
        if hasattr(self, 'audio'):
            self.audio.play_sound('success')
            self.audio.speak(self.get_text('body_research_done', name=res_data["name"]), interrupt=False)
            
        self.current_research_draft = None

    def get_researchable_features(self):
        """Features die erforschbar, aber noch nicht freigeschaltet sind."""
        unlocked_names = {f.name for f in self.unlocked_features}
        return [f for f in ENGINE_FEATURES if f["name"] not in unlocked_names and self.week >= ((f.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

    def get_researchable_topics(self):
        """Themen die erforschbar, aber noch nicht freigeschaltet sind."""
        return [t for t in RESEARCHABLE_TOPICS if t["name"] not in self.unlocked_topics and self.week >= ((t.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

    def get_researchable_genres(self):
        """Genres die erforschbar, aber noch nicht freigeschaltet sind."""
        return [g for g in RESEARCHABLE_GENRES if g["name"] not in self.unlocked_genres and self.week >= ((g.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

    def get_researchable_audiences(self):
        """Zielgruppen die erforschbar, aber noch nicht freigeschaltet sind."""
        return [a for a in RESEARCHABLE_AUDIENCES if a["name"] not in self.unlocked_audiences and self.week >= ((a.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]

    def get_researchable_technologies(self):
        """Endgame-Technologien, die noch nicht freigeschaltet sind."""
        return [t for t in RESEARCHABLE_TECHNOLOGIES if t["name"] not in self.unlocked_technologies and self.week >= ((t.get("unlock_year", START_YEAR) - START_YEAR) * WEEKS_PER_YEAR + 1)]
