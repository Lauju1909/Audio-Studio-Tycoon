"""SoundCon, Soundtrack-Label, Radio und Jingles. Mixin fuer GameState."""
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


class SoundconMixin:
    def can_attend_soundcon(self) -> tuple:
        """Prüft ob der Spieler an der aktuellen SoundCon teilnehmen kann.

        Returns:
            (bool, str): True/False und Grund bei Ablehnung.
        """
        current_year = self.get_calendar_year()
        if self.soundcon_last_year >= current_year:
            return False, "soundcon_already_attended"
        if self.active_soundcon is not None:
            return False, "soundcon_already_booked"
        return True, ""

    def book_soundcon_booth(self, booth_tier: str) -> bool:
        """Bucht einen Messestand für die SoundCon.

        Args:
            booth_tier: Standgröße ('klein', 'mittel', 'groß', 'keynote').

        Returns:
            True bei Erfolg, False bei zu wenig Geld.
        """
        can, _ = self.can_attend_soundcon()
        if not can:
            return False

        tier_data = SoundConEvent.BOOTH_TIERS.get(booth_tier)
        if not tier_data:
            return False

        cost = tier_data["cost"]
        if self.money < cost:
            return False

        self.track_expense("other", cost)
        event = SoundConEvent(year=self.get_calendar_year(), booth_tier=booth_tier)
        self.active_soundcon = event
        return True

    def conduct_soundcon_qa(self) -> dict:
        """Führt eine Q&A-Runde auf der SoundCon durch (max. 3 Runden).

        Returns:
            Dict mit 'success', 'qa_round', 'message'.
        """
        if not self.active_soundcon:
            return {"success": False, "message": "soundcon_not_booked"}
        if self.active_soundcon.qa_rounds >= 3:
            return {"success": False, "message": "soundcon_qa_max"}

        self.active_soundcon.qa_rounds += 1
        qa_num = self.active_soundcon.qa_rounds
        if hasattr(self, 'audio'):
            self.audio.play_sound('confirm')
            self.audio.speak(
                self.get_text('soundcon_qa_done', round=qa_num), interrupt=False
            )
        return {"success": True, "qa_round": qa_num, "message": "soundcon_qa_success"}

    def conduct_soundcon_qa_interactive(self, hype_bonus, prestige_bonus, fan_bonus) -> dict:
        if not self.active_soundcon:
            return {"success": False, "message": "soundcon_not_booked"}
        if self.active_soundcon.qa_rounds >= 3:
            return {"success": False, "message": "soundcon_qa_max"}
            
        self.active_soundcon.qa_rounds += 1
        
        # Manuell Bonus hinzufügen
        self.active_soundcon.hype_gained = getattr(self.active_soundcon, 'hype_gained', 0) + hype_bonus
        self.active_soundcon.fans_gained = getattr(self.active_soundcon, 'fans_gained', 0) + fan_bonus
        self.active_soundcon.prestige_gained = getattr(self.active_soundcon, 'prestige_gained', 0) + prestige_bonus
        
        if hasattr(self, 'audio'):
            self.audio.play_sound('confirm')
            
        return {"success": True, "qa_round": self.active_soundcon.qa_rounds}

    def finish_soundcon(self) -> dict:
        """Schließt die SoundCon ab und berechnet die Ergebnisse.

        Returns:
            Ergebnis-Dict mit hype, fans, prestige, qa, tier.
        """
        if not self.active_soundcon:
            return {}

        result = self.active_soundcon.calculate_results(self)

        # Effekte anwenden
        self.hype   = min(250, self.hype + result["hype"])
        self.fans  += result["fans"]
        self.prestige += result["prestige"]

        # Archivieren
        self.soundcon_history.append(self.active_soundcon)
        self.soundcon_last_year = self.active_soundcon.year
        self.pending_soundcon_result = result
        self.active_soundcon = None

        # E-Mail mit Zusammenfassung
        self.emails.insert(0, Email(
            sender=self.get_text('soundcon_sender'),
            subject=self.get_text('soundcon_result_subject', year=self.get_calendar_year()),
            body=self.get_text(
                'soundcon_result_body',
                hype=result["hype"], fans=result["fans"],
                prestige=result["prestige"], qa=result["qa"],
                tier=self.get_text(f'soundcon_tier_{result["tier"]}')
            ),
            date_week=self.week
        ))
        if hasattr(self, 'audio'):
            self.audio.play_sound('success')
            self.audio.speak(
                self.get_text('soundcon_result_announce', fans=result["fans"]), interrupt=False
            )
        return result

    def found_soundtrack_label(self, label_name: str) -> bool:
        """Gründet ein Soundtrack-Label.

        Kostet 30.000 €. Scheitert wenn Label bereits existiert oder kein Geld.

        Args:
            label_name: Name des neuen Labels.

        Returns:
            True bei Erfolg, False bei Misserfolg.
        """
        FOUNDING_COST = 30_000
        if self.soundtrack_label is not None:
            return False  # Bereits gegründet
        if self.money < FOUNDING_COST:
            return False

        self.track_expense("other", FOUNDING_COST)
        label = SoundtrackLabel(label_name)
        label.founding_week = self.week
        self.soundtrack_label = label

        # Alle bisherigen Spiele retroaktiv hinzufügen
        for g in self.game_history:
            label.add_game(g.name)

        self.emails.insert(0, Email(
            sender=self.get_text('label_sender'),
            subject=self.get_text('label_founded_subject', name=label_name),
            body=self.get_text('label_founded_body', name=label_name, cost=FOUNDING_COST,
                               games=len(label.catalogued_games)),
            date_week=self.week
        ))
        if hasattr(self, 'audio'):
            self.audio.play_sound('success')
            self.audio.speak(self.get_text('label_founded_announce', name=label_name), interrupt=False)
        return True

    def sign_radio_contract(self, station_data: dict) -> bool:
        """Unterzeichnet einen Radiovertrag für das Soundtrack-Label.

        Args:
            station_data: Dict aus SoundtrackLabel.RADIO_STATIONS.

        Returns:
            True bei Erfolg.
        """
        if not self.soundtrack_label:
            return False
        cost = station_data.get("cost", 0)
        if self.money < cost:
            return False

        self.track_expense("other", cost)
        contract = RadioContract(
            station_name=station_data["name"],
            weekly_royalties=station_data["royalties"],
            duration_weeks=station_data["weeks"],
            hype_per_week=station_data["hype"]
        )
        self.soundtrack_label.radio_contracts.append(contract)

        self.emails.insert(0, Email(
            sender=self.get_text('label_sender'),
            subject=self.get_text('label_radio_subject', station=station_data["name"]),
            body=self.get_text('label_radio_body',
                               station=station_data["name"],
                               royalties=station_data["royalties"],
                               weeks=station_data["weeks"]),
            date_week=self.week
        ))
        if hasattr(self, 'audio'):
            self.audio.play_sound('confirm')
            self.audio.speak(
                self.get_text('label_radio_announce', station=station_data["name"]), interrupt=False
            )
        return True

    def create_radio_jingle(self, name: str, music_track: str, voice_style: str, sfx: str) -> bool:
        """Produziert ein neues Radio-Jingle zur Marketing-Unterstützung."""
        # Kosten berechnen
        cost = 5000 # Basiskosten
        if music_track != "none": cost += 2000
        if voice_style != "none": cost += 1500
        if sfx != "none": cost += 1000
        
        if self.money < cost:
            return False
            
        self.track_expense("marketing", cost)
        
        # Hype Bonus berechnen
        hype_bonus = 5.0
        if music_track != "none": hype_bonus += 3.0
        if voice_style != "none": hype_bonus += 2.0
        if sfx != "none": hype_bonus += 2.0
        
        from models import RadioJingle
        jingle = RadioJingle(
            name=name,
            music_track=music_track,
            voice_style=voice_style,
            sfx=sfx,
            hype_bonus=hype_bonus,
            cost=cost
        )
        jingle.weeks_left = 4
        self.active_jingles.append(jingle)
        
        # Hype auf alle aktiven Spiele anwenden
        for ap in self.active_projects:
            if getattr(self, 'strike_weeks_left', 0) > 0:
                continue
            proj = ap["project"]
            proj.hype = max(0.0, proj.hype + hype_bonus)
            
        return True
