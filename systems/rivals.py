"""Rivalen, Aktienmarkt der Rivalen und Branchennews. Mixin fuer GameState."""
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


class RivalsMixin:
    def _init_rivals(self):
        """Erstellt 3 Konkurrenz-Studios."""
        return [
            RivalStudio("MicroHard", target_market_share=30, next_release_week=random.randint(10, 30), ai_personality="Trendchaser"),
            RivalStudio("Electric Farts", target_market_share=25, next_release_week=random.randint(20, 45), ai_personality="Aggressive"),
            RivalStudio("Nintengo", target_market_share=20, next_release_week=random.randint(35, 60), ai_personality="Perfectionist")
        ]

    def _process_rivals(self):
        """Lsst Rivalen Spiele verffentlichen und Marktanteile beeinflussen."""
        import competitor_ai
        
        for rival in self.rivals:
            is_owned = getattr(rival, 'is_owned_by_player', False)
            if is_owned:
                # Phase 2 M&A: Passive Einnahmen durch den Backkatalog
                back_catalog_income = int(sum(getattr(g, 'score', 0) * 200 for g in getattr(rival, 'games', [])))
                if back_catalog_income > 0:
                    self.money += back_catalog_income
                    self.track_income("other", back_catalog_income)

            r_game = competitor_ai.evaluate_turn(rival, self)
            
            if r_game and is_owned:
                # Apply quality boost
                quality_boost = getattr(rival, 'games_quality_boost', 0)
                if quality_boost > 0:
                    r_game.score = min(10.0, r_game.score + quality_boost / 10.0)
                    
                # Develop for our console
                if getattr(rival, 'develop_for_custom_console', False) and getattr(self, 'active_custom_console', None):
                    self.active_custom_console['market_presence'] += 5.0
                    
                # Einnahmen aus dem neuen Spiel direkt an den Spieler
                release_income = int(r_game.score * random.randint(100000, 500000))
                self.money += release_income
                self.track_income("publishing", release_income)
                
                self.emails.append(Email(
                    sender=self.get_text('sender_industry_news'),
                    subject=f"Tochterfirma {rival.name} verffentlicht {r_game.name}!",
                    body=f"Dein Tochterstudio {rival.name} hat '{r_game.name}' verffentlicht (Wertung: {r_game.score:.1f}/10). Einnahmen: {release_income:,} EUR.",
                    date_week=self.week
                ))
            elif r_game:
                # Sabotage-Check: Wenn der Spieler gerade das gleiche Genre entwickelt
                sabotage_msg = ""
                can_sabotage = (self.week - self.last_sabotage_week) >= 4
                
                if can_sabotage and self.is_developing and any(ap["project"].genre == r_game.genre for ap in self.active_projects):
                    # Hype-Verlust skaliert mit Schwierigkeit
                    diff_multi = {0: 0.3, 1: 0.6, 2: 1.0, 3: 1.5}.get(self.difficulty, 1.0)
                    base_loss = random.randint(10, 25)
                    loss = int(base_loss * diff_multi)
                    
                    # PR Defense Check (Phase II)
                    pr_bonus = 1.0
                    for obj in getattr(self, 'office_objects', []):
                        if obj.get('bonus') == 'pr_defense':
                            pr_bonus = 0.5
                    
                    loss = int(loss * pr_bonus)
                    
                    self.hype = max(0, self.hype - loss)
                    self.last_sabotage_week = self.week
                    sabotage_msg = f"\n\n{self.get_text('sabotage_warning', name=rival.name, genre=self.get_text(r_game.genre))}"
                
                # Benachrichtigung
                if r_game.score >= 8.5 or sabotage_msg:
                    self.emails.append(Email(
                        sender=self.get_text('sender_industry_news'),
                        subject=self.get_text('subject_rival_hit', name=rival.name),
                        body=self.get_text('body_rival_hit', name=rival.name, game=r_game.name, score=r_game.score, genre=self.get_text(r_game.genre)) + sabotage_msg,
                        date_week=self.week
                    ))

                # Dividende ausschütten, falls Anteile besessen werden
                if getattr(rival, 'owned_shares', 0) > 0:
                    dividend = int((r_game.score * 10000) * (rival.owned_shares / 100))
                    self.track_income("other", dividend)
                    self.emails.append(Email(
                        sender=self.get_text('sender_bank'),
                        subject=self.get_text('subject_dividend'),
                        body=self.get_text('body_dividend', name=rival.name, amount=dividend),
                        date_week=self.week
                    ))
                
                # Marktauswirkung: Zieht Hype und Verkäufe ab, wenn wir auch ein Spiel im gleichen Genre haben
                for my_game in self.game_history:
                    if my_game.is_active and my_game.genre == r_game.genre:
                        # Unser Spiel verliert Hype (passiv über Zeit)
                        self.hype = max(0, self.hype - 10)

    def _generate_industry_news(self):
        """Erzeugt zufällige Markt-Ereignisse."""
        news_types = [
            {"text": self.get_text('news_hardware_boom'), "multi": 1.2},
            {"text": self.get_text('news_recession'), "multi": 0.85},
            {"text": self.get_text('news_rival_bankrupt'), "multi": 1.0},
        ]
        news = random.choice(news_types)
        # Email-Objekt erstellen
        mail = Email(
            sender=self.get_text('sender_industry_news'),
            subject=self.get_text('news_title'),
            body=news["text"],
            date_week=self.week
        )
        self.emails.append(mail)

    def get_share_price(self, rival):
        """Berechnet den Kaufpreis für 10% Anteile an einem Rivalen."""
        return 50000 + int(rival.owned_shares / 10) * 5000

    def buy_shares(self, rival_index):
        """Kauft 10% Anteile an einem Rivalen-Studio."""
        if rival_index < 0 or rival_index >= len(self.rivals):
            return False, "invalid"
        rival = self.rivals[rival_index]
        if rival.owned_shares >= 50:
            return False, "max_shares"
        price = self.get_share_price(rival)
        if self.money < price:
            return False, "no_money"
        self.track_expense("shares", price)
        rival.owned_shares += 10
        return True, rival.owned_shares

    def sell_shares(self, rival_index):
        """Verkauft 10% Anteile an einem Rivalen-Studio."""
        if rival_index < 0 or rival_index >= len(self.rivals):
            return False, "invalid"
        rival = self.rivals[rival_index]
        if rival.owned_shares <= 0:
            return False, "no_shares"
        # Verkaufspreis = 80% des aktuellen Kaufpreises
        sell_price = int(self.get_share_price(rival) * 0.8)
        self.track_income("shares", sell_price)
        rival.owned_shares -= 10
        return True, rival.owned_shares
