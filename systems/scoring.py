"""Hype, Review-, Verkaufs- und Entwicklungskosten-Berechnung. Mixin fuer GameState."""
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


class ScoringMixin:
    def calculate_hype(self, project):
        """Berechnet den Hype für ein Spiel basierend auf Marketing, Lizenzen und Events."""
        hype = 0
        # Marketing - Jetzt dynamisch aus game_data.py
        from game_data import MARKETING_OPTIONS_PH5
        m_option = next((m for m in MARKETING_OPTIONS_PH5 if m["name"] == project.marketing), None)
        
        if m_option:
            hype += m_option.get("hype", 0)
        elif project.marketing == 'publisher_deal':
            hype += 40
        elif project.marketing == 'small': # Legacy Support
            hype += 10
        elif project.marketing == 'medium':
            hype += 25
        elif project.marketing == 'large':
            hype += 50
            
        # Marketing-Effizienz anwenden
        hype *= self.marketing_efficiency

        # Lizenzen
        if getattr(project, 'license_bonus', 0) > 0:
            hype += project.license_bonus

        # Projektbezogener Hype aus Fanpost, Jingles und Community-Aktionen
        hype += getattr(project, 'hype', 0.0)

        # Zufallsereignis Bonus
        for event in self.active_events:
            if event["effect"] == "hype_boost":
                hype += event.get("hype_amount", event.get("amount", 0))

        # Globaler Hype-Multiplikator
        hype *= self.hype_multiplier

        return min(250, int(hype))

    def calculate_review(self, project, bugs=0):
        """
        Berechnet die Bewertung eines Spiels.
        Inklusive Trend-Bonus.
        """
        if getattr(project, "is_port", False) and project.original_game_name:
            original_game = next((g for g in self.game_history if g.name == project.original_game_name), None)
            if original_game and original_game.review:
                # Port review is slightly worse or equal to the original game
                variance = random.uniform(-0.5, 0)
                base_review = original_game.review.average + variance
                base_review = max(1.0, min(10.0, float(base_review)))
                
                scores = []
                for _ in range(4):
                    v = random.uniform(-1.0, 1.0)
                    s = int(round(max(1.0, min(10.0, base_review + v))))
                    scores.append(s)
                
                comments = []
                comments.append(self.get_text('review_port_intro', game=project.name, platform=project.platform))
                if base_review >= 7.0:
                    comments.append(self.get_text('review_port_good'))
                else:
                    comments.append(self.get_text('review_port_bad'))
                    
                review = ReviewScore(scores, comments=comments)
                return review

        topic = project.topic
        genre = project.genre
        sliders = project.sliders

        # 1. Synergiewert (0.0 - 1.0)
        compat_raw = get_compatibility(topic, genre)
        synergy = compat_raw / 3.0

        # 2. Slider-Match (0.0 - 1.0)
        ideal = get_ideal_sliders(genre)
        total_diff = 0
        max_diff = 0
        for sname in SLIDER_NAMES:
            player_val = sliders.get(sname, 5)
            ideal_val = ideal.get(sname, 5)
            team_bonus = self.get_team_slider_bonus(sname, project=project)
            effective_val = player_val + team_bonus
            total_diff += abs(effective_val - ideal_val)
            max_diff += 10
        slider_match = 1.0 - (total_diff / max_diff) if max_diff > 0 else 0.5

        # 3. Team-Bonus (0.0 - 1.0)
        team_quality = min(1.0, self.get_team_bonus(project) * 5)

        # 4. Engine-Bonus (0.0 - 1.0)
        engine_quality = 0.3
        if project.engine:
            engine_quality = min(1.0, 0.3 + project.engine.quality_bonus)

        # 5. Trend-Bonus
        trend_bonus = 1.0
        if self.current_trend:
            if topic == self.current_trend["topic"]:
                trend_bonus += 0.2
            if genre == self.current_trend["genre"]:
                trend_bonus += 0.2

        # 6. Zufallsfaktor
        random_factor = random.uniform(0.9, 1.1)

        # Basis-Score
        base_score = (
            (synergy * 0.35) +
            (slider_match * 0.35) +
            (team_quality * 0.15) +
            (engine_quality * 0.10) +
            (0.5 * 0.05)
        )
        # Schwierigkeits-Standard (steigt über die Jahre)
        base_score *= random_factor * trend_bonus

        # Game Dev Tech-Bonus
        tech_bonus = 0.0
        if "Neural-Engine Grafik-Rendering" in self.unlocked_technologies:
            tech_bonus += 0.05
        if "Quanten-Physik-Engine" in self.unlocked_technologies:
            tech_bonus += 0.05
        if "Holodeck-Immersions-Engine" in self.unlocked_technologies:
            tech_bonus += 0.08
        if "Gedanken-Steuerungs-Engine" in self.unlocked_technologies:
            tech_bonus += 0.10
        if "KI-Entwickler-Zentrale" in self.unlocked_technologies:
            tech_bonus += 0.05
        base_score *= (1.0 + tech_bonus)

        # Bug-Malus (Massiv wenn viele Bugs)
        bug_penalty = (bugs * 0.02) # 50 Bugs = -1.0 (10 Punkte auf 10er Skala)
        base_score = max(0.1, base_score - bug_penalty)

        # Massive Bonus for perfect synergy and slider configuration
        if synergy >= 0.8 and slider_match >= 0.8:
            base_score += 0.15

        # Sequel Bonus/Malus (IP-Rating basiert)
        sequel_num = getattr(project, 'sequel_number', 0)
        if sequel_num > 0:
            # Finde das Originalspiel oder Vorgänger in der Historie
            ip_bonus = 0
            for past in reversed(self.game_history):
                if past.topic == topic and past.genre == genre:
                    ip = getattr(past, 'ip_rating', 0)
                    if ip >= 70:
                        ip_bonus = 0.15  # Starker Hype-Bonus
                    elif ip >= 40:
                        ip_bonus = 0.05
                    elif ip < 20:
                        ip_bonus = -0.10  # Schlechte IP enttäuscht
                    break
            base_score *= (1.0 + ip_bonus)
            # Sequel-Fatigue: jedes weitere Sequel wird schwieriger
            if sequel_num >= 4:
                base_score *= 0.90
            elif sequel_num >= 3:
                base_score *= 0.95
        elif len(self.game_history) > 0:
            # Gleiche Topic+Genre Wiederholung ohne Sequel-Flag
            last = self.game_history[-1]
            if last.topic == topic and last.genre == genre:
                base_score *= 0.8

        if self.high_score > 0:
            ratio = (base_score * 10) / self.high_score
            if ratio < 0.8:
                base_score *= 0.9

        prestige = sum(item.get("cost", 0) for item in getattr(self, "office_items", [])) // 2000
        base_score *= (1.0 + prestige * 0.03)

        # Schwierigkeitsgrad-Bonus auf Review
        from game_data import DIFFICULTY_LEVELS
        diff = DIFFICULTY_LEVELS[self.difficulty]
        base_score += diff["review_bonus"] * 0.1  # Normalisiert (max ±0.1 auf 0-1 Skala)

        # Lizenz-Bonus
        base_score += getattr(project, 'license_bonus', 0.0)

        # Barrierefreiheits-Reputation: saubere Screenreader-UX hilft Reviews leicht.
        accessibility_bonus = min(0.05, getattr(self, "accessibility_reputation", 0) / 2000.0)
        base_score += accessibility_bonus

        # Qualitätsstandard-Multiplikator anwenden (macht es über die Jahre schwerer)
        base_review = max(1.0, min(10.0, float(base_score * 10 / self.quality_standard_multi)))

        # Crowdfunding Review-Penalty
        if getattr(project, "is_crowdfunded", False):
            base_review -= 1.0 # Backers expect the world!
            if bugs > 0:
                base_review -= (bugs * 0.05) # Even harsher on bugs!
                
        # DRM Review Modifiers
        drm_level = getattr(project, "drm_level", 0)
        if drm_level == 0:
            base_review += 0.3 # Fans love DRM-free games
        elif drm_level == 2:
            base_review -= 0.5 # Fans hate aggressive DRM
            if bugs > 0:
                base_review -= 0.5 # Aggressive DRM + Bugs = Disaster

        if getattr(project, "used_ai_soundtrack", False):
            if random.random() < 0.4:
                base_review -= 1.5
                self.fans = max(0, int(self.fans * 0.9))
                self.emails.insert(0, Email(self.get_text('sender_community', default="Community"), "Shitstorm wegen KI-Musik", f"Die Spieler hassen den KI-generierten Soundtrack von {project.name}. Massive Kritik online!", self.week))
            else:
                base_review += 1.0

        base_review = max(1.0, min(10.0, base_review))

        scores = []
        for _ in range(4):
            variance = random.uniform(-1.2, 1.2)
            s = int(round(max(1.0, min(10.0, base_review + variance))))
            scores.append(s)

        # NEU: Review-Texte generieren
        comments = []
        
        # Intro
        intro_key = random.choice(['review_intro_1', 'review_intro_2', 'review_intro_3', 'review_intro_4', 'review_intro_5'])
        prefix = self.get_text('review_prefix')
        intro = self.get_text(intro_key, company=self.company_name, game=project.name)
        comments.append(f"{prefix}{intro}")
        
        # Story Text
        story_key = f"story_{project.topic}"
        story_text = self.get_text(story_key)
        if story_text != story_key:
            comments.append(story_text)
        
        # Positiv/Negativ basierend auf Slidern/Synergie
        if synergy >= 0.8:
            key = random.choice(['review_pos_1', 'review_pos_2', 'review_pos_3'])
            comments.append(self.get_text(key, genre=self.get_text(project.genre), topic=self.get_text(project.topic)))
        elif synergy < 0.5:
            key = random.choice(['review_neg_1', 'review_neg_2', 'review_neg_3'])
            comments.append(self.get_text(key, genre=self.get_text(project.genre), topic=self.get_text(project.topic)))
            
        if slider_match < 0.6:
            comments.append(self.get_text('review_bad_gameplay'))
        elif slider_match >= 0.9:
            comments.append(self.get_text('review_good_gameplay'))

        if getattr(self, "accessibility_reputation", 0) >= 50:
            comments.append(self.get_text('review_accessibility_praise'))

        # Fazit
        if base_review >= 8.0:
            concl_key = 'review_concl_1'
        elif base_review >= 5.0:
            concl_key = 'review_concl_2'
        else:
            concl_key = 'review_concl_3'
        comments.append(self.get_text(concl_key))

        review = ReviewScore(scores, comments=comments)
        if review.average > self.high_score:
            self.high_score = review.average

        return review

    def calculate_sales(self, project):
        """Berechnet Verkäufe inkl. Marketing und Größe."""
        if not project.review:
            return 0

        avg = project.review.average
        # Basis-Verkäufe skalieren mit Größe
        size_data = next((s for s in GAME_SIZES if s["name"] == project.size), GAME_SIZES[1])
        base_sales = 5000 * size_data["revenue_multi"]

        if avg >= 9: 
            score_m = 6.0
        elif avg >= 8: 
            score_m = 4.0
        elif avg >= 7: 
            score_m = 2.5
        elif avg >= 6: 
            score_m = 1.8
        elif avg >= 5: 
            score_m = 1.2
        elif avg >= 4: 
            score_m = 0.8
        else: 
            score_m = 0.3

        fan_bonus = 1.0 + (self.fans / 100000)

        plat_multi = 1.0
        for p in PLATFORMS:
            if p["name"] == project.platform:
                plat_multi = p["market_multi"]
                break

        audience_multi = AUDIENCE_MULTI.get(project.audience, 1.0)
        rand_m = random.uniform(0.8, 1.2)

        # Schwierigkeitsgrad Markt-Multiplikator
        from game_data import DIFFICULTY_LEVELS
        diff_market = DIFFICULTY_LEVELS[self.difficulty]["market_multi"]

        sales = int(base_sales * score_m * fan_bonus * plat_multi * audience_multi * rand_m * diff_market * self.sales_multiplier)
        if getattr(project, "is_f2p", False):
            sales *= 10
        if getattr(project, "is_remake", False):
            sales = int(sales * 2.0)
        if getattr(project, "is_port", False):
            sales = int(sales * 0.4)
        if getattr(project, "is_crowdfunded", False):
            sales = int(sales * 1.5) # Backers guaranteed purchase
            
        # Piraterie berechnen
        drm_level = getattr(project, "drm_level", 0)
        piracy_rate = 0.0
        
        # Basis-Piraterie nach Plattform (PC hat mehr)
        if "PC" in project.platform:
            if drm_level == 0: piracy_rate = 0.35
            elif drm_level == 1: piracy_rate = 0.15
            elif drm_level == 2: piracy_rate = 0.02
        else:
            if drm_level == 0: piracy_rate = 0.10
            elif drm_level == 1: piracy_rate = 0.03
            elif drm_level == 2: piracy_rate = 0.00
            
        pirated = int(sales * piracy_rate)
        project.pirated_copies = pirated
        sales -= pirated
        
        return sales

    def calculate_dev_cost(self, project):
        """Berechnet Entwicklungskosten inkl. Größe und Marketing."""
        # Basis-Kosten basierend auf Größe
        size_data = next((s for s in GAME_SIZES if s["name"] == project.size), GAME_SIZES[1])
        base_cost = 10000 * size_data["cost_multi"]

        # Team-Kosten (nur zugewiesene MA)
        dev_weeks = sum(p["duration_weeks"] for p in DEV_PHASES) * size_data["time_multi"]
        assigned_emps = [self.employees[i] for i in getattr(project, 'assigned_employee_ids', []) if i < len(self.employees)]
        if not assigned_emps: assigned_emps = self.employees # Fallback
        salary_cost = sum(e.salary for e in assigned_emps) * dev_weeks

        from game_data import MARKETING_OPTIONS_PH5
        mark_data = next((m for m in MARKETING_OPTIONS_PH5 if m["name"] == project.marketing), {"cost": 0})
        marketing_cost = mark_data["cost"]
        
        # Engine usage cost (Dritte-Partei)
        engine_usage_cost = 0
        if getattr(project, "engine", None):
            engine_usage_cost = getattr(project.engine, "usage_cost", 0)

        # VR-Cost modifier
        if "(VR)" in project.platform:
            base_cost *= 2.5
            salary_cost *= 2.0

        return int(base_cost + salary_cost + marketing_cost + engine_usage_cost)

    def get_current_charts(self, top_n=10):
        """Gibt die aktuellen Verkaufscharts zurueck (Spieler + Rivalen)."""
        entries = []
        for g in self.game_history:
            entries.append({
                'name': g.name,
                'studio': self.company_name,
                'sales': getattr(g, 'sales', 0),
                'is_active': getattr(g, 'is_active', False)
            })
        for rival in self.rivals:
            for rg in rival.games:
                entries.append({
                    'name': rg.name,
                    'studio': rival.name,
                    'sales': int(rg.score * 10000),
                    'is_active': (self.week - rg.week_developed) < 20
                })
        entries.sort(key=lambda e: e['sales'], reverse=True)
        return entries[:top_n]
