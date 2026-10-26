"""Zufallsereignisse, Trends, Mails, Sponsoring, Turniere, Erfolge. Mixin fuer GameState."""
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


class EventsMixin:
    def add_welcome_emails(self):
        """Erstellt die Willkommens-E-Mails in der aktuell gesetzten Sprache."""
        # Willkommensnachricht: Die 1930er Ära
        self.emails.append(Email(
            sender=self.get_text('sender_historian'),
            subject=self.get_text('subject_pioneer_times'),
            body=self.get_text('body_pioneer_times'),
            date_week=1
        ))
        
        # Initialisierung von Inhalten, die Sprach-Keys benötigen
        self.rivals = self._init_rivals()
        from game_data import get_available_platforms
        self.active_platforms = [p['name'] for p in get_available_platforms(1)]

    def _process_sponsorships(self):
        if not hasattr(self, "active_sponsorships"):
            self.active_sponsorships = []
        
        for s in list(self.active_sponsorships):
            if random.random() < 0.05 and getattr(self, "pending_influencer_event", None) is None:
                active_games = [g for g in self.game_history if g.is_active]
                if active_games:
                    game = random.choice(active_games)
                    self.pending_influencer_event = {
                        "game_name": game.name,
                        "sponsorship": s
                    }
                    
            s["duration"] -= 1
            if s["duration"] <= 0:
                self.streamer_hype_multi /= s["boost"]
                self.active_sponsorships.remove(s)

    def add_sponsorship(self, boost, duration):
        if not hasattr(self, "active_sponsorships"):
            self.active_sponsorships = []
        self.active_sponsorships.append({"boost": boost, "duration": duration})
        self.streamer_hype_multi *= boost

    def _process_tournaments(self):
        """Verarbeitet aktive E-Sport-Turniere: liefert Einnahmen, Hype und Fans."""
        if not getattr(self, "active_tournaments", []):
            return
        finished = []
        for tournament in self.active_tournaments:
            tournament["weeks_left"] = tournament.get("weeks_left", 4) - 1
            if tournament["weeks_left"] <= 0:
                finished.append(tournament)
        for t in finished:
            self.active_tournaments.remove(t)
            prize = t.get("prize_pool", 50000)
            hype_gain = t.get("hype_bonus", 20)
            fan_gain = t.get("fan_bonus", 10000)
            self.track_income("other", prize)
            self.hype = min(250, self.hype + hype_gain)
            self.fans += fan_gain
            self.emails.insert(0, Email(
                sender=self.get_text('sender_industry_news'),
                subject=self.get_text('esports_result_subject', name=t.get("name", "Turnier")),
                body=self.get_text(
                    'esports_result_body',
                    name=t.get("name", "Turnier"),
                    prize=prize,
                    fans=fan_gain,
                    hype=hype_gain
                ),
                date_week=self.week
            ))
            if hasattr(self, 'audio'):
                self.audio.play_sound('cheer')
                self.audio.speak(self.get_text(
                    'esports_result_subject',
                    name=t.get("name", "Turnier")
                ), interrupt=False)

    def _process_esports_leagues(self):
        """Verarbeitet aktive E-Sports-Ligen wöchentlich:
        - Hype-Zerfall (0.3-0.5% pro Woche, geschützt durch Sponsor-Tier)
        - Passive Sponsoren-Einnahmen basierend auf Tier, Hype und Fans
        - Aktive Spieler-Retention (GaaS-Boost)
        - Streaming-Deal-Einnahmen wöchentlich
        """
        leagues = getattr(self, 'esports_leagues', [])
        if not leagues:
            return

        import random
        total_passive_income = 0

        for league in leagues:
            # 1. Hype-Zerfall: Tier schützt vor schnellem Verfall
            tier_data = league.get_sponsor_tier_data()
            hype_min = tier_data["hype_min"]
            decay_rate = 0.997 if league.sponsor_tier == "global" else \
                         0.995 if league.sponsor_tier == "national" else \
                         0.993 if league.sponsor_tier == "regional" else \
                         0.990 if league.sponsor_tier == "local" else \
                         0.988
            league.hype = max(hype_min, league.hype * decay_rate)

            # 2. Sponsoren-Einnahmen basierend auf Tier
            sponsor_weekly = league.calculate_weekly_sponsor_income(
                self.fans, getattr(self, 'hype', 50)
            )
            if sponsor_weekly > 0:
                variation = random.uniform(0.9, 1.1)
                sponsor_weekly = int(sponsor_weekly * variation)
                league.total_sponsor_income += sponsor_weekly
                total_passive_income += sponsor_weekly

            # 3. Streaming-Deal-Einnahmen
            if league.streaming_deals > 0:
                stream_income = int(league.streaming_deals * 50000 * (league.hype / 100.0))
                stream_income = int(stream_income * random.uniform(0.85, 1.15))
                league.total_sponsor_income += stream_income
                total_passive_income += stream_income

            # 4. Aktive Spieler-Retention: Spiel bleibt relevant
            game = next((g for g in self.game_history if g.name == league.game_name), None)
            if game:
                retention_boost = max(200, int(self.fans * 0.005 * (league.hype / 100.0)))
                game.active_players = max(
                    getattr(game, 'active_players', 0),
                    retention_boost
                )

            # 5. Hype global boostet leicht, wenn Liga aktiv
            hype_boost = 0.1 * (league.hype / 100.0)
            self.hype = min(100, getattr(self, 'hype', 50) + hype_boost)

        if total_passive_income > 0:
            self.money += total_passive_income
            self.track_income("esports", total_passive_income)

    def _check_goty(self):
        """Ermittelt das Spiel des Jahres."""
        year = self.get_calendar_year()
        
        # Bereits vergeben?
        if year == self.last_goty_year: 
            return
        self.last_goty_year = year
        
        # Alle Spiele dieses Jahres (Spieler)
        my_games_this_year = [g for g in self.game_history if (START_YEAR + (g.week_developed - 1) // WEEKS_PER_YEAR) == year]
        my_best = max(my_games_this_year, key=lambda g: getattr(g.review, 'average', 0)) if my_games_this_year else None
        
        # Alle Spiele dieses Jahres (Rivalen)
        rival_games_this_year = []
        for r in self.rivals:
            # Finde das beste Spiel dieses Rivalen, das in DIESEM Jahr erschienen ist
            yearly_rival_games = [rg for rg in r.games if (START_YEAR + (rg.week_developed - 1) // WEEKS_PER_YEAR) == year]
            if yearly_rival_games:
                best_rg = max(yearly_rival_games, key=lambda g: g.score)
                rival_games_this_year.append((r.name, best_rg))
                
        rival_best_tuple = max(rival_games_this_year, key=lambda t: t[1].score) if rival_games_this_year else None
        
        my_score = my_best.review.average if my_best and my_best.review else 0
        rival_score = rival_best_tuple[1].score if rival_best_tuple else 0
        
        if my_score == 0 and rival_score == 0:
            return # Kein Spiel erschienen
            
        goty_data = {
            "year": year,
            "my_score": my_score,
            "my_game": my_best.name if my_best else None,
            "rival_score": rival_score,
            "rival_name": rival_best_tuple[0] if rival_best_tuple else None,
            "rival_game": rival_best_tuple[1].name if rival_best_tuple else None,
        }
        
        # Track wins for achievements
        if my_score > rival_score and my_score > 0:
            if not hasattr(self, "my_goty_wins"):
                self.my_goty_wins = 0
            self.my_goty_wins += 1
        
        self.pending_goty_results = goty_data
        if hasattr(self, 'audio'):
            self.audio.play_sound('drumroll')
            self.audio.speak(self.get_text('goty_ceremony_start'), interrupt=True)

    def process_emails(self):
        """Generiert zufällige E-Mails."""
        
        if not self.game_history:
            return
            
        # Chance auf Mail
        if random.random() < 0.2:
            game = random.choice(self.game_history)
            if random.random() < 0.5:
                # Bug Report
                game.bugs += random.randint(1, 5)
                mail = Email(
                    sender=self.get_text('sender_disappointed'),
                    subject=self.get_text('subject_bug_report', game=game.name),
                    body=self.get_text('body_bug_report', game=game.name),
                    date_week=self.week,
                    game_name=game.name,
                    is_bug=True
                )
            else:
                # Fan Mail
                mail = Email(
                    sender=self.get_text('sender_fan'),
                    subject=self.get_text('subject_fan_praise', game=game.name),
                    body=self.get_text('body_fan_praise', game=game.name, topic=self.get_text(game.topic)),
                    date_week=self.week,
                    game_name=game.name
                )
            self.emails.insert(0, mail)

    def update_trends(self):
        # Aktualisiert Markttrends alle 1/4 bis fast 1/2 Jahr
        min_w = WEEKS_PER_YEAR // 4
        max_w = int(WEEKS_PER_YEAR * 0.4) + 1
        if self.week - self.last_trend_week < random.randint(min_w, max_w):
            return None
        
        # Trend auswählen
        topic_trend = random.choice(TREND_TOPICS)
        genre_trend = random.choice(TREND_GENRES)
        
        self.current_trend = {
            "topic": topic_trend["topic"],
            "genre": genre_trend["genre"],
            "text": f"{topic_trend['text']} Und: {genre_trend['text']}",
            "week_started": self.week
        }
        self.last_trend_week = self.week
        return self.current_trend

    def check_random_event(self):
        """Prüft ob ein Zufallsereignis oder Trendwechsel ausgelöst wird."""
        # Trend prüfen
        trend = self.update_trends()
        if trend:
            return {"title": "Markttrend-Wechsel", "text": trend["text"], "effect": "trend"}

        if self.week - self.last_event_week < 8:
            return None
        if random.random() < 0.25:
            event = random.choice(RANDOM_EVENTS)
            self.last_event_week = self.week
            self.apply_event(event)
            return event
        return None

    def apply_event(self, event):
        """Wendet ein Ereignis an."""
        if "duration" in event:
            # Dauerhafte Events zur Liste hinzufügen (Kopie)
            ev_copy = dict(event)
            self.active_events.append(ev_copy)
        elif event["effect"] == "money":
            self.track_income("other", event["value"])
        elif event["effect"] == "fans":
            self.fans = max(0, self.fans + event["value"])
        elif event["effect"] == "hype_boost":
            self.hype += event["hype_amount"]
            
        body = self.get_text("event_" + event["id"], weeks=event.get("duration", 0), hype=event.get("hype_amount", 0))
        self.emails.insert(0, Email(
            sender=self.get_text('sender_industry_news'),
            subject=self.get_text('news_title'),
            body=body,
            date_week=self.week
        ))
        
        # Audio Warnung
        if hasattr(self, 'audio'):
            self.audio.play_sound('warn') # Fallback wenn Datei fehlt
            self.audio.speak(body, interrupt=True)

    def generate_trend(self):
        """Erzeugt einen neuen Markttrend (Thema und Genre)."""
        from game_data import TREND_TOPICS, TREND_GENRES
        topic = random.choice(TREND_TOPICS)
        genre = random.choice(TREND_GENRES)
        self.current_trend = {
            "topic": topic["topic"],
            "genre": genre["genre"],
            "text": f"{topic['text']} {genre['text']}"
        }
        # Benachrichtigung via Email
        self.emails.append(Email(
            sender=self.get_text('sender_intel'),
            subject=self.get_text('sender_intel'),
            body=f"{self.get_text('main_trend')} {self.current_trend['text']}",
            date_week=self.week
        ))

    def receive_fan_mail(self):
        """Generiert eine neue Fanpost mit Antwortoptionen."""

        from models import FanMail
        from game_data import FAN_MAIL_TEMPLATES
        
        # Chance basierend auf Fans und Hype
        chance = 0.10 + min(0.30, self.fans / 200000.0)
        if random.random() > chance:
            return False
            
        template = random.choice(FAN_MAIL_TEMPLATES)
        
        # Eindeutige ID vergeben
        mail_id = f"fanmail_{self.week}_{random.randint(1000, 9999)}"
        
        # Zufälliger Fan-Name
        fan_firstnames = ["Thomas", "Michael", "Andreas", "Christian", "Stefan", "Lukas", "Julia", "Sarah", "Laura", "Katharina"]
        fan_lastnames = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"]
        sender_name = f"{random.choice(fan_firstnames)} {random.choice(fan_lastnames)}"
        
        # FanMail erstellen
        mail = FanMail(
            mail_id=mail_id,
            sender=sender_name,
            subject_key=template["subject_key"],
            text_key=template["text_key"],
            options=template["options"]
        )
        self.fan_mail_inbox.append(mail)
        
        # E-Mail-Benachrichtigung an den Spieler
        self.emails.insert(0, Email(
            sender=sender_name,
            subject=self.get_text(template["subject_key"]),
            body=self.get_text(template["text_key"]),
            date_week=self.week
        ))
        
        # Audio-Feedback
        if hasattr(self, 'audio'):
            self.audio.play_sound('click')
            
        return True

    def answer_fan_mail(self, mail_id: str, option_idx: int) -> bool:
        """Beantwortet eine Fanpost und wendet die entsprechenden Effekte an."""
        mail = next((m for m in self.fan_mail_inbox if m.mail_id == mail_id), None)
        if not mail or mail.is_answered:
            return False
            
        if option_idx < 0 or option_idx >= len(mail.options):
            return False
            
        mail.is_answered = True
        mail.selected_option = option_idx
        mail.is_read = True
        
        option = mail.options[option_idx]
        effects = option.get("effects", option.get("value", {}))
        
        # Effekte anwenden
        # 1. Fans
        fans_diff = effects.get("fans", 0)
        self.fans = max(0, self.fans + fans_diff)
        
        # 2. Hype (auf alle aktiven Projekte addieren)
        hype_diff = effects.get("hype", 0.0)
        for ap in self.active_projects:
            if getattr(self, 'strike_weeks_left', 0) > 0:
                continue
            proj = ap["project"]
            proj.hype = max(0.0, proj.hype + hype_diff)
            
        # 3. Geld
        money_diff = effects.get("money", 0)
        if money_diff != 0:
            if money_diff > 0:
                self.track_income("other", money_diff)
            else:
                self.track_expense("other", abs(money_diff))
                
        return True

    def trigger_personality_event(self) -> bool:
        """Prüft und triggert wöchentlich Büro-Events basierend auf Mitarbeiter-Persönlichkeiten."""
        if getattr(self, "active_personality_event", None) is not None:
            return False
            
        # 10% Chance pro Woche

        if random.random() > 0.10:
            return False
            
        if not self.employees:
            return False
            
        # Vorhandene Persönlichkeiten im Team ermitteln
        team_personalities = [e.personality for e in self.employees if getattr(e, "personality", None)]
        if not team_personalities:
            return False
            
        from game_data import OFFICE_PERSONALITY_EVENTS
        eligible_events = []
        for event in OFFICE_PERSONALITY_EVENTS:
            req = event["personality_required"]
            if req in team_personalities:
                eligible_events.append(event)
                
        if not eligible_events:
            return False
            
        chosen_event = random.choice(eligible_events)
        
        # Finde einen passenden Mitarbeiter als Hauptakteur des Events
        protagonist = next((e for e in self.employees if getattr(e, "personality", None) == chosen_event["personality_required"]), self.employees[0])
        
        self.active_personality_event = chosen_event
        self.active_personality_employee = protagonist
        
        # Benachrichtigungs-Email senden
        self.emails.insert(0, Email(
            sender=protagonist.name,
            subject=self.get_text("subject_office_event"),
            body=self.get_text("body_office_event", name=protagonist.name),
            date_week=self.week
        ))
        
        if hasattr(self, 'audio'):
            self.audio.play_sound('warn')
            
        return True

    def answer_personality_event(self, option_idx: int) -> bool:
        """Beantwortet das aktive Büro-Event und wendet Effekte an."""
        event = getattr(self, "active_personality_event", None)
        if not event:
            return False
            
        if option_idx < 0 or option_idx >= len(event["options"]):
            return False
            
        option = event["options"][option_idx]
        effects = option.get("effects", {})
        
        # 1. Moral der Mitarbeiter
        morale_diff = effects.get("morale", 0)
        if morale_diff != 0:
            protagonist = getattr(self, "active_personality_employee", None)
            if protagonist:
                protagonist.morale = max(0, min(100, protagonist.morale + morale_diff))
            else:
                for emp in self.employees:
                    emp.morale = max(0, min(100, emp.morale + morale_diff))
                    
        # 2. Geld
        money_diff = effects.get("money", 0)
        if money_diff != 0:
            if money_diff > 0:
                self.track_income("other", money_diff)
            else:
                self.track_expense("other", abs(money_diff))
                
        # 3. Hype
        hype_diff = effects.get("hype", 0.0)
        if hype_diff != 0.0:
            for ap in self.active_projects:
                ap["project"].hype = max(0.0, ap["project"].hype + hype_diff)
                
        # 4. Fans
        fans_diff = effects.get("fans", 0)
        if fans_diff != 0:
            self.fans = max(0, self.fans + fans_diff)
            
        # 5. Spezielle temporäre Modifikatoren
        if "dev_speed_penalty" in effects:
            self.temp_dev_speed_penalty = effects["dev_speed_penalty"]
            self.temp_dev_speed_weeks = 4
            
        if "quality_boost" in effects:
            self.temp_quality_boost = effects["quality_boost"]
            self.temp_quality_weeks = 4
            
        # Event zurücksetzen
        self.active_personality_event = None
        self.active_personality_employee = None
        return True

    def _check_achievements(self):
        """Prüft ob neue Meilensteine erreicht wurden."""
        from game_data import ACHIEVEMENTS
        
        if not hasattr(self, "unlocked_achievements"):
            self.unlocked_achievements = []
        if not hasattr(self, "my_goty_wins"):
            self.my_goty_wins = 0
            
        for ach in ACHIEVEMENTS:
            if ach["id"] in self.unlocked_achievements:
                continue
                
            unlocked = False
            
            if ach["type"] == "money":
                if self.money >= ach["threshold"]:
                    unlocked = True
            elif ach["type"] == "fans":
                if self.fans >= ach["threshold"]:
                    unlocked = True
            elif ach["type"] == "game_size":
                if any(g.size == ach["threshold"] for g in self.game_history):
                    unlocked = True
            elif ach["type"] == "score":
                if any(getattr(g.review, 'average', 0) >= ach["threshold"] for g in self.game_history if hasattr(g, 'review')):
                    unlocked = True
            elif ach["type"] == "goty":
                if self.my_goty_wins >= ach["threshold"]:
                    unlocked = True
            elif ach["type"] == "accessibility":
                if getattr(self, "accessibility_reputation", 0) >= ach["threshold"]:
                    unlocked = True
                    
            if unlocked:
                self.unlocked_achievements.append(ach["id"])
                
                # Bonus anwenden
                bonus_str = ""
                if ach["bonus_type"] == "fans":
                    self.fans += ach["bonus_value"]
                    bonus_str = f"+{ach['bonus_value']:,} Fans"
                elif ach["bonus_type"] == "money":
                    self.track_income("other", ach["bonus_value"])
                    bonus_str = f"+{ach['bonus_value']:,} €"
                elif ach["bonus_type"] == "hype":
                    self.hype = min(250, self.hype + ach["bonus_value"])
                    bonus_str = f"+{ach['bonus_value']:,} Hype"
                    
                # E-Mail generieren
                title = self.get_text(f"ach_{ach['id']}_name")
                desc = self.get_text(f"ach_{ach['id']}_desc")
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_system'),
                    subject=self.get_text('subject_achievement', title=title),
                    body=self.get_text('body_achievement', desc=desc, bonus=bonus_str),
                    date_week=self.week
                ))
                
                # Audio-Feedback
                if hasattr(self, "audio") and self.audio:
                    self.audio.play_sound("achievement.wav") # Sound falls vorhanden
                    self.audio.speak(f"Meilenstein erreicht: {title}. {desc}", interrupt=False)

    def toggle_exclusive_esports(self):
        if self.streaming_platform:
            self.streaming_platform.exclusive_esports = not self.streaming_platform.exclusive_esports
