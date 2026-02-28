"""
Spielzustand für Audio Studio Tycoon - Audio Edition.

Verwaltet Firmendaten, Geld, Fans, Mitarbeiter, Engines,
Spielhistorie, Ereignisse und die Bewertungslogik.
"""

import random
import json
import os
from models import GameProject, ReviewScore, Employee, Engine, EngineFeature, RivalStudio, RivalGame
from translations import TRANSLATIONS
from game_data import (
    get_compatibility, get_ideal_sliders, SLIDER_NAMES, GENRES,
    PLATFORMS, AUDIENCE_MULTI, AUDIENCE_PRICE,
    RANDOM_EVENTS, OFFICE_LEVELS, ENGINE_FEATURES,
    EMPLOYEE_ROLES, DEV_PHASES, GAME_SIZES,
    TREND_TOPICS, TREND_GENRES, TRAINING_OPTIONS,
    START_TOPICS, RESEARCHABLE_TOPICS,
    START_GENRES, START_AUDIENCES, RESEARCHABLE_GENRES, RESEARCHABLE_AUDIENCES,
    RESEARCHABLE_TECHNOLOGIES,
    get_available_platforms, get_available_features,
)


class GameState:
    def __init__(self):
        self.company_name = ""
        self.money = 70000
        self.fans = 0
        self.week = 1
        self.game_history = []    # Liste aller GameProject
        self.high_score = 0.0
        self.games_made = 0
        self.total_revenue = 0

        # Trends
        self.current_trend = {}  # {'topic': '...', 'genre': '...', 'week_started': X}
        self.last_trend_week = 0

        # Mitarbeiter
        self.employees = []

        # Engines
        self.engines = []
        self.unlocked_features = []  # Liste von EngineFeature (freigeschaltet)
        self._init_starter_engine()

        # Büro
        self.office_level = 0  # Index in OFFICE_LEVELS

        # Ereignisse
        self.last_event_week = 0
        self.active_events = []

        # Forschungs-System
        self.is_researching = False
        self.research_progress = 0
        self.research_total_weeks = 0
        self.current_research_draft = None
        
        self.unlocked_topics = list(START_TOPICS)
        self.unlocked_genres = list(START_GENRES)
        self.unlocked_audiences = list(START_AUDIENCES)
        self.unlocked_technologies = []

        # Aktuelles Projekt
        self.current_draft = {
            "name": "",
            "topic": None,
            "genre": None,
            "platform": None,
            "audience": None,
            "engine": None,
            "sliders": {},
            "size": "Mittel",
            "marketing": "Kein Marketing",
        }
        
        # Posteingang
        self.emails = []
        
        # Aktive MMOs
        self.active_mmos = []

        # Einstellungen
        self.settings = {
            "language": "de",
            "music_enabled": True,
            "tts_engine": "auto" # mgl: auto, nvda, sapi
        }

        # Echtzeit-Zeitsteuerung
        self.time_speed = 1.0  # 0=Pause, 1=Normal, 2=Schnell, 4=Sehr Schnell
        self.pause_for_menu = False # Flag für Menüs (z.B. Texteingabe)
        self.week_progress = 0.0
        self.is_developing = False
        self.dev_progress = 0.0
        self.dev_total_weeks = 0
        self.active_project = None
        self.crunch_active = False
        self.current_bugs = 0
        self.hype = 0.0
        self.active_expo_hype = 0
        
        # NEU: Phase 7 - Konkurrenz & GOTY
        self.rivals = self._init_rivals()
        self.last_goty_year = 0
        
        # NEU: Phase 7 - DevKits & Hardware Markt
        self.bought_platforms = ["PC (MS-DOS)"]
        self.active_platforms = [p['name'] for p in get_available_platforms(1)]
        
        # NEU: Phase 7 - Finanzen & Buchhaltung
        self.bank_loan = None
        self.accounting = {"income": 0, "expenses": 0, "loan_paid": 0}
        
        # NEU: Phase 7 - Eigene Konsole
        self.custom_consoles = []
        self.is_developing_console = False
        self.console_progress = 0
        self.console_total_weeks = 50
        self.current_console_draft = None

    def get_market_platforms(self):
        from game_data import get_available_platforms
        base = get_available_platforms(self.week)
        out = list(base)
        for cc in getattr(self, "custom_consoles", []):
            if self.week >= cc.release_week:
                # Für spielereigene Konsole zahlt man 0 Lizenzgebühr
                out.append({
                    "name": cc.name,
                    "market_multi": cc.market_share,
                    "license_fee": 0
                })
        return out

    def save_global_settings(self):
        """Speichert die globalen Einstellungen (Sprache, Musik, TTS)."""
        import json
        import os
        try:
            with open("global_settings.json", "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der globalen Einstellungen: {e}")

    def load_global_settings(self):
        """Lädt die globalen Einstellungen beim Spielstart."""
        import json
        import os
        if os.path.exists("global_settings.json"):
            try:
                with open("global_settings.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.settings.update(data)
            except Exception as e:
                print(f"Fehler beim Laden der globalen Einstellungen: {e}")

    def _init_rivals(self):
        """Erstellt 3 Konkurrenz-Studios."""
        return [
            RivalStudio("MicroHard", target_market_share=30, next_release_week=random.randint(5, 20)),
            RivalStudio("Electric Farts", target_market_share=25, next_release_week=random.randint(15, 30)),
            RivalStudio("Nintengo", target_market_share=20, next_release_week=random.randint(25, 40))
        ]

    def _init_starter_engine(self):
        """Erstellt die Starter-Engine mit Basis-Features."""
        starter_features = []
        for f_data in ENGINE_FEATURES:
            if f_data["cost"] == 0:
                feat = EngineFeature(f_data["category"], f_data["name"], f_data["tech_bonus"])
                starter_features.append(feat)
                self.unlocked_features.append(feat)

        starter = Engine("Basis-Engine", starter_features)
        self.engines.append(starter)

    def reset_draft(self):
        """Setzt den aktuellen Entwurf zurück."""
        self.current_draft = {
            "name": "",
            "topic": None,
            "genre": None,
            "platform": None,
            "audience": None,
            "engine": None,
            "sliders": {},
            "marketing": "Kein Marketing",
        }
        self.aaa_event_triggered = False

    def get_text(self, key, **kwargs):
        """Holt einen übersetzten Text basierend auf dem aktuellen Sprach-Setting."""
        lang = self.settings.get("language", "de")
        text = TRANSLATIONS.get(lang, TRANSLATIONS['de']).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def get_calendar_text(self):
        """Gibt Jahr und Woche zurück (52 Wochen pro Jahr)."""
        year = (self.week - 1) // 52 + 1
        week_in_year = (self.week - 1) % 52 + 1
        lang = self.settings.get("language", "de")
        if lang == "de":
            return f"Jahr {year}, Woche {week_in_year}"
        else:
            return f"Year {year}, Week {week_in_year}"

    def get_speed_text(self):
        """Gibt Text für aktuelle Geschwindigkeit zurück."""
        if self.time_speed == 0: return self.get_text('paused')
        if self.time_speed == 1: return self.get_text('speed_normal')
        if self.time_speed == 2: return self.get_text('speed_fast')
        return self.get_text('speed_ultra')

    def update_tick(self, dt_ms):
        """Aktualisiert Spielzeit basierend auf Millisekunden."""
        if self.time_speed == 0 or self.pause_for_menu:
            return

        ms_per_week = 5000 / self.time_speed
        self.week_progress += dt_ms / ms_per_week
        
        # Hype Decay (ca. 10% pro Woche)
        if self.hype > 0:
            decay_sec = 0.1 * (dt_ms / ms_per_week)
            self.hype = max(0.0, self.hype - decay_sec)

        if self.week_progress >= 1.0:
            self.week_progress -= 1.0
            self.week += 1
            self._on_new_week()

    def _on_new_week(self):
        """Logik die jede Woche passiert (Gehalt, Zufallsereignisse)."""
        # Jahres-Reset für Buchhaltung
        if (self.week - 1) % 52 == 0:
            self.accounting = {"income": 0, "expenses": 0, "loan_paid": 0}
            
        # Gehälter abziehen
        total_salary = sum(e.salary for e in self.employees)
        self.money -= total_salary
        self.accounting["expenses"] += total_salary
        
        # Kreditabzahlung
        if getattr(self, "bank_loan", None):
            payment = self.bank_loan.weekly_payment
            self.money -= payment
            self.accounting["loan_paid"] += payment
            self.bank_loan.amount_remaining -= payment
            self.bank_loan.weeks_remaining -= 1
            if self.bank_loan.weeks_remaining <= 0 or self.bank_loan.amount_remaining <= 0:
                self.bank_loan = None
                from models import Email
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_bank'),
                    subject=self.get_text('subject_loan_paid'),
                    body=self.get_text('body_loan_paid'),
                    date_week=self.week
                ))
        
        # Trend check (alle 20-40 Wochen)
        if self.week - self.last_trend_week >= random.randint(20, 40):
            if self.week % 8 == 0:
                self.generate_trend()
                
        # Zufallsereignisse prüfen
        self.check_random_event()
        
        # Abgelaufene Events entfernen
        new_active = []
        for e in self.active_events:
            e["duration"] -= 1
            if e["duration"] > 0:
                new_active.append(e)
        self.active_events = new_active
                
        # Marktanteil der eigenen Konsole erhöhen
        if hasattr(self, "custom_consoles"):
            for cc in self.custom_consoles:
                cc.market_share = min(0.5, cc.market_share + (cc.tech_level * 0.0005))
            
        # Projektfortschritt falls aktiv
        if self.is_developing:
            boost = 2 if self.crunch_active else 1
            # Remaster-Bonus: 1.5x schneller
            if self.current_draft.get("is_remaster"):
                boost *= 1.5
                
            # Burnout-Event Malus
            for e in self.active_events:
                if e["effect"] == "dev_speed_drop":
                    boost *= e["multiplier"]
            
            # Team Speed Modifier durch Eigenschaften
            boost *= self.get_team_speed_modifier()
            
            self.dev_progress += boost
            
            if self.crunch_active:
                # Moral-Malus
                for emp in self.employees:
                    morale_loss = random.randint(2, 5)
                    if emp.trait and emp.trait["effect"] == "morale_loss":
                        morale_loss = int(morale_loss * emp.trait["value"])
                    emp.morale = max(0, emp.morale - morale_loss)
                    
                # Bug-Zuwachs
                base_bugs = random.randint(1, 3)
                self.current_bugs += int(base_bugs * self.get_team_bug_modifier())
            
            # Zufällige Bugs auch ohne Crunch (seltener)
            if random.random() < 0.1:
                self.current_bugs += int(1 * self.get_team_bug_modifier())
                
            # Supporter fixen aktiv Bugs jede Woche während der Entwicklung
            supporter_count = sum(1 for e in self.employees if e.role == "Supporter")
            if supporter_count > 0 and self.current_bugs > 0:
                self.current_bugs = max(0, self.current_bugs - supporter_count)

            # AAA Events (Max 1x pro Projekt)
            if self.current_draft.get("size") == "AAA" and not getattr(self, "aaa_event_triggered", False):
                if 0.2 < (self.dev_progress / max(1, getattr(self, "dev_total_weeks", 1))) < 0.8:
                    if random.random() < 0.05:  # 5% Chance pro Woche
                        from game_data import AAA_DEV_EVENTS
                        self.pending_dev_event = random.choice(AAA_DEV_EVENTS)
                        self.aaa_event_triggered = True
                        self.time_speed = 0 # Pause game

        # Forschungsfortschritt
        elif self.is_researching:
            self.research_progress += 1
            if self.research_progress >= self.research_total_weeks:
                self.complete_research()

        # Konsolenentwicklung
        if getattr(self, "is_developing_console", False):
            self.console_progress += 1
            if self.console_progress >= self.console_total_weeks:
                self.is_developing_console = False
                c = self.current_console_draft
                from models import CustomConsole, Email
                new_console = CustomConsole(c['name'], c['tech_level'], c['cost'], self.week)
                if not hasattr(self, "custom_consoles"): self.custom_consoles = []
                self.custom_consoles.append(new_console)
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_hardware'),
                    subject=self.get_text('subject_console_done'),
                    body=self.get_text('body_console_done', name=c['name']),
                    date_week=self.week
                ))
                self.current_console_draft = None

        # Zufällige Branchen-News (5% Chance pro Woche)
        if random.random() < 0.05:
            self._generate_industry_news()

        # Expo Trigger (Woche 26 jedes Jahr)
        week_in_year = (self.week - 1) % 52 + 1
        if week_in_year == 26:
            from models import Email
            self.emails.append(Email(
                sender=self.get_text('sender_assistant'),
                subject=self.get_text('subject_expo'),
                body=self.get_text('body_expo'),
                date_week=self.week
            ))
            
        # NEU: Phase 7 - Hardware-Markt Updates
        current_platforms = [p['name'] for p in get_available_platforms(self.week)]
        for p in current_platforms:
            if p not in self.active_platforms:
                self.active_platforms.append(p)
                from models import Email
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_hardware_news'),
                    subject=self.get_text('subject_new_console', name=p),
                    body=self.get_text('body_new_console', name=p),
                    date_week=self.week
                ))
        for p in list(self.active_platforms):
            if p not in current_platforms:
                self.active_platforms.remove(p)
                from models import Email
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_hardware_news'),
                    subject=self.get_text('subject_console_dead', name=p),
                    body=self.get_text('body_console_dead', name=p),
                    date_week=self.week
                ))
            
        # NEU: Phase 7 - Rivalen und GOTY evaluieren
        self._process_rivals()
        if week_in_year == 52:
            self._check_goty()

    def _process_rivals(self):
        """Lässt Rivalen Spiele veröffentlichen und Marktanteile beeinflussen."""
        from game_data import TREND_TOPICS, TREND_GENRES
        from models import Email
        
        for rival in self.rivals:
            if self.week >= rival.next_release_week:
                # Rivale veröffentlicht ein Spiel!
                topic = random.choice(TREND_TOPICS)["topic"]
                genre = random.choice(TREND_GENRES)["genre"]
                
                # Konkurrenz wird im Laufe der Jahre etwas besser
                base_score = random.uniform(5.5, 8.5)
                year = (self.week - 1) // 52 + 1
                base_score += min(1.5, year * 0.1) # Max +1.5 über Zeit
                score = round(min(10.0, base_score), 1)
                
                r_game = RivalGame(f"{rival.name} {genre}", topic, genre, score)
                rival.games.append(r_game)
                rival.next_release_week = self.week + random.randint(20, 50)
                
                # Benachrichtigung
                if score >= 8.5:
                    self.emails.append(Email(
                        sender=self.get_text('sender_industry_news'),
                        subject=self.get_text('subject_rival_hit', name=rival.name),
                        body=self.get_text('body_rival_hit', name=rival.name, game=r_game.name, score=score, genre=self.get_text(genre)),
                        date_week=self.week
                    ))

                # Dividende ausschütten, falls Anteile besessen werden
                if getattr(rival, 'owned_shares', 0) > 0:
                    dividend = int((score * 10000) * (rival.owned_shares / 100))
                    self.money += dividend
                    self.accounting["income"] += dividend
                    self.emails.append(Email(
                        sender=self.get_text('sender_bank'),
                        subject=self.get_text('subject_dividend'),
                        body=self.get_text('body_dividend', name=rival.name, amount=dividend),
                        date_week=self.week
                    ))
                
                # Marktauswirkung: Zieht Hype und Verkäufe ab, wenn wir auch ein Spiel im gleichen Genre haben
                for my_game in self.game_history:
                    if my_game.is_active and my_game.genre == genre:
                        # Unser Spiel verliert Hype
                        self.hype = max(0, self.hype - 10)
                        # Verkäufe sinken für diese Woche (implizit verringert, da Hype sinkt)

    def _check_goty(self):
        """Ermittelt das Spiel des Jahres."""
        from models import Email
        year = (self.week - 1) // 52 + 1
        
        # Bereits vergeben?
        if year == self.last_goty_year: return
        self.last_goty_year = year
        
        # Alle Spiele dieses Jahres (Spieler)
        my_games_this_year = [g for g in self.game_history if ((g.week_developed - 1) // 52 + 1) == year]
        my_best = max(my_games_this_year, key=lambda g: getattr(g.review, 'average', 0)) if my_games_this_year else None
        
        # Alle Spiele dieses Jahres (Rivalen)
        rival_games_this_year = []
        for r in self.rivals:
            for rg in r.games:
                # rg.weeks_on_market könnte man zurückrechnen, einfacher: wenn sie im letzten 52-Wochen Fenster kamen
                pass # Für Einfachheit ignorieren wir das Release-Datum im Modell und nehmen einfach das zuletzt hinzugefügte
            if r.games:
                rival_games_this_year.append((r.name, r.games[-1]))
                
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
        
        self.pending_goty_results = goty_data

    def _generate_industry_news(self):
        """Erzeugt zufällige Markt-Ereignisse."""
        from models import Email
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

    # ==========================================================
    # MITARBEITER
    # ==========================================================

    def get_max_employees(self):
        """Maximale Mitarbeiter basierend auf Büro-Level."""
        return OFFICE_LEVELS[self.office_level]["max_employees"]

    def can_hire(self):
        return len(self.employees) < self.get_max_employees()

    def generate_candidate(self):
        """Generiert einen zufälligen Bewerber."""
        from game_data import EMPLOYEE_SPECIALIZATIONS
        role_data = random.choice(EMPLOYEE_ROLES)
        level = random.randint(1, min(3, 1 + self.games_made // 3))
        
        spec = None
        if random.random() < 0.3: # 30% Chance auf Spezialisierung
            spec = random.choice(EMPLOYEE_SPECIALIZATIONS)
            
        return Employee(role_data=role_data, skill_level=level, specialization=spec)

    def hire_employee(self, employee):
        """Stellt einen Mitarbeiter ein."""
        if not self.can_hire():
            return False
        # Einstellungsgebühr = 2 Wochen Gehalt
        hire_cost = employee.salary * 2
        if self.money < hire_cost:
            return False
        self.money -= hire_cost
        self.employees.append(employee)
        return True

    def fire_employee(self, index):
        """Entlässt einen Mitarbeiter."""
        if 0 <= index < len(self.employees):
            emp = self.employees.pop(index)
            # Abfindung = 4 Wochen Gehalt
            self.money -= emp.salary * 4
            return emp
        return None

    def pay_salaries(self):
        """Bezahlt alle Gehälter (wöchentlich)."""
        total = sum(e.salary for e in self.employees)
        self.money -= total
        return total

    def advance_week(self, weeks=1):
        """Rückt die Zeit vor und verarbeitet wöchentliche Ereignisse."""
        for _ in range(weeks):
            self.week += 1
            self.pay_salaries()
            
            # Trends und Zufallsereignisse
            self.check_random_event()
            
            # Verkäufe für aktive Spiele
            for g in self.game_history:
                if g.is_active:
                    g.weeks_on_market += 1
                    # Verkäufe sinken mit der Zeit
                    new_sales = int(self.calculate_sales(g) / (1 + g.weeks_on_market * 0.2))
                    if g.bugs > 0:
                        new_sales = int(new_sales * 0.5) # Bugs halbieren Verkäufe
                        
                    # Hacker-Event Malus
                    for e in self.active_events:
                        if e["effect"] == "sales_drop":
                            new_sales = int(new_sales * e["multiplier"])
                    
                    price = AUDIENCE_PRICE.get(g.audience, 30)
                    g.sales += new_sales
                    g.revenue += new_sales * price
                    self.money += new_sales * price
                    
                    # Nach 12-20 Wochen oder bei sehr niedrigen Verkäufen vom Markt nehmen
                    if g.weeks_on_market > 20 or new_sales < 100:
                        g.is_active = False

            # MMOs verarbeiten (Einnahmen, Kosten, Spielerschwund)
            for mmo in self.active_mmos:
                if mmo.game.is_active:
                    mmo.weeks_active += 1
                    # Einnahmen und Kosten
                    self.money += mmo.weekly_revenue
                    self.money -= mmo.weekly_cost
                    mmo.game.revenue += mmo.weekly_revenue
                    
                    # Spielerschwund (ca. 2% pro Woche)
                    mmo.players = int(mmo.players * 0.98)
                    
                    if mmo.players < 1000:
                        mmo.game.is_active = False # Server shut down

            # Fan-Mails & Bugs generieren
            self.process_emails()

    def process_emails(self):
        """Generiert zufällige E-Mails."""
        from models import Email
        
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
            
    def release_patch(self, game_index):
        """Veröffentlicht einen kostenlosen Patch."""
        game = self.game_history[game_index]
        if game.bugs > 0:
            game.bugs = 0
            self.fans += 100
            return True
        return False

    def release_dlc(self, game_index):
        """Veröffentlicht einen kostenpflichtigen DLC."""
        game = self.game_history[game_index]
        cost = 20000
        if self.money < cost:
            return False
        self.money -= cost
        game.dlc_count += 1
        game.is_active = True # Bringt Spiel zurück in die Charts
        game.weeks_on_market = max(0, game.weeks_on_market - 5)
        self.fans += 500
        return True

    def release_mmo_update(self, mmo_index):
        """Programmiert ein Content-Update für ein MMO, um Spieler zurückzugewinnen."""
        mmo = self.active_mmos[mmo_index]
        cost = 50000
        if self.money < cost:
            return False
        self.money -= cost
        # Füge Spieler hinzu basierend auf Basis-Spielerzahl (z.B. +10% max)
        new_players = int(mmo.game.sales * 0.05)
        mmo.players += new_players
        self.fans += 1000
        return True

    def get_team_bonus(self):
        """Gesamtbonus des Teams auf Spielqualität."""
        if not self.employees:
            return 0.0
        base_bonus = sum(e.quality_contribution for e in self.employees)
        return base_bonus * self.get_team_quality_modifier()

    def get_team_slider_bonus(self, slider_name):
        """Durchschnittlicher Skill-Bonus des Teams für einen Slider."""
        if not self.employees:
            return 0.0
        bonuses = [e.get_slider_bonus(slider_name) for e in self.employees]
        return sum(bonuses) / len(bonuses)

    def get_team_speed_modifier(self):
        if not self.employees: return 1.0
        mods = [e.trait["value"] for e in self.employees if e.trait and e.trait["effect"] == "speed"]
        return sum(mods) / len(mods) if mods else 1.0

    def get_team_bug_modifier(self):
        if not self.employees: return 1.0
        mods = [e.trait["value"] for e in self.employees if e.trait and e.trait["effect"] == "bugs"]
        return sum(mods) / len(mods) if mods else 1.0

    def get_team_quality_modifier(self):
        if not self.employees: return 1.0
        mods = [e.trait["value"] for e in self.employees if e.trait and e.trait["effect"] == "quality"]
        return sum(mods) / len(mods) if mods else 1.0

    # ==========================================================
    # FORSCHUNG & ENGINES
    # ==========================================================

    def start_research(self, res_data, res_type):
        """Startet ein neues Forschungsprojekt."""
        if self.money < res_data["cost"] or self.is_researching or self.is_developing:
            return False
            
        self.money -= res_data["cost"]
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
            
        from models import Email
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

    def create_engine(self, name, feature_list):
        """Erstellt eine neue Engine aus freigeschalteten Features."""
        engine = Engine(name, feature_list)
        self.engines.append(engine)
        return engine

    def get_researchable_features(self):
        """Features die erforschbar, aber noch nicht freigeschaltet sind."""
        available = get_available_features(self.week)
        unlocked_names = {f.name for f in self.unlocked_features}
        return [f for f in available if f["name"] not in unlocked_names]

    def get_researchable_topics(self):
        """Themen die erforschbar, aber noch nicht freigeschaltet sind."""
        return [t for t in RESEARCHABLE_TOPICS if t["name"] not in self.unlocked_topics and self.week >= t["week"]]

    def get_researchable_genres(self):
        """Genres die erforschbar, aber noch nicht freigeschaltet sind."""
        return [g for g in RESEARCHABLE_GENRES if g["name"] not in self.unlocked_genres and self.week >= g["week"]]

    def get_researchable_audiences(self):
        """Zielgruppen die erforschbar, aber noch nicht freigeschaltet sind."""
        return [a for a in RESEARCHABLE_AUDIENCES if a["name"] not in self.unlocked_audiences and self.week >= a["week"]]

    def get_researchable_technologies(self):
        """Endgame-Technologien, die noch nicht freigeschaltet sind."""
        return [t for t in RESEARCHABLE_TECHNOLOGIES if t["name"] not in self.unlocked_technologies and self.week >= t["week"]]

    # ==========================================================
    # AKTIENMARKT / INVESTMENTS
    # ==========================================================

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
        self.money -= price
        self.accounting["expenses"] += price
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
        self.money += sell_price
        self.accounting["income"] += sell_price
        rival.owned_shares -= 10
        return True, rival.owned_shares

    # ==========================================================
    # BÜRO
    # ==========================================================

    def can_upgrade_office(self):
        """Kann das Büro aufgerüstet werden?"""
        if self.office_level >= len(OFFICE_LEVELS) - 1:
            return False
        next_level = OFFICE_LEVELS[self.office_level + 1]
        return self.money >= next_level["cost"]

    def upgrade_office(self):
        """Rüstet das Büro auf."""
        if not self.can_upgrade_office():
            return False
        next_level = OFFICE_LEVELS[self.office_level + 1]
        self.money -= next_level["cost"]
        self.office_level += 1
        return True

    def get_office_info(self):
        """Info über aktuelles Büro."""
        office = OFFICE_LEVELS[self.office_level]
        return office

    # ==========================================================
    # TRENDS
    # ==========================================================

    def update_trends(self):
        """Aktualisiert Markttrends alle 12-20 Wochen."""
        if self.week - self.last_trend_week < random.randint(12, 20):
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

    # ==========================================================
    # ZUFALLSEREIGNISSE
    # ==========================================================

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
        if event["effect"] == "money":
            self.money += event["value"]
        elif event["effect"] == "fans":
            self.fans = max(0, self.fans + event["value"])
        elif event["effect"] == "hype_boost":
            self.hype += event["hype_amount"]
        else:
            # Dauerhafte Events zur Liste hinzufügen (Kopie)
            ev_copy = dict(event)
            self.active_events.append(ev_copy)
            
        # Spieler benachrichtigen
        from models import Email
        body = self.get_text("event_" + event["id"], weeks=event.get("duration", 0), hype=event.get("hype_amount", 0))
        self.emails.insert(0, Email(
            sender="News Reader",
            subject="Markt-Ereignis",
            body=body,
            date_week=self.week
        ))
        
        # Audio Warnung
        if hasattr(self, 'audio'):
            self.audio.play_sound('warn') # Fallback wenn Datei fehlt
            self.audio.speak(body, interrupt=True)

    # ==========================================================
    # BEWERTUNG
    # ==========================================================

    def calculate_review(self, project):
        """
        Berechnet die Bewertung eines Spiels.
        Inklusive Trend-Bonus.
        """
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
            team_bonus = self.get_team_slider_bonus(sname)
            effective_val = player_val + team_bonus
            total_diff += abs(effective_val - ideal_val)
            max_diff += 10
        slider_match = 1.0 - (total_diff / max_diff) if max_diff > 0 else 0.5

        # 3. Team-Bonus (0.0 - 1.0)
        team_quality = min(1.0, self.get_team_bonus() * 5)

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
        base_score *= random_factor * trend_bonus

        # Massive Bonus for perfect synergy and slider configuration
        if synergy >= 0.8 and slider_match >= 0.8:
            base_score += 1.5

        # Sequel Bonus/Malus
        if len(self.game_history) > 0:
            last = self.game_history[-1]
            if last.topic == topic and last.genre == genre:
                base_score *= 0.8
            
            # Sequel Bonus: Wenn der Name eine Steigerung andeutet
            is_sequel = False
            if project.name.startswith(last.name) and project.name != last.name:
                is_sequel = True
            
            if is_sequel:
                if last.review and last.review.average >= 7.5:
                    base_score *= 1.15  # Hype Bonus
                elif last.review and last.review.average < 5.0:
                    base_score *= 0.85  # Enttäuschungs-Malus

        if self.high_score > 0:
            ratio = (base_score * 10) / self.high_score
            if ratio < 0.8:
                base_score *= 0.9

        prestige = OFFICE_LEVELS[self.office_level]["prestige"]
        base_score *= (1.0 + prestige * 0.03)

        base_review = max(1.0, min(10.0, float(base_score * 10)))

        scores = []
        for _ in range(4):
            variance = random.uniform(-1.2, 1.2)
            s = int(round(max(1.0, min(10.0, base_review + variance))))
            scores.append(s)

        # NEU: Review-Texte generieren
        comments = []
        
        # Intro
        intro_key = random.choice(['review_intro_1', 'review_intro_2', 'review_intro_3'])
        intro = self.get_text(intro_key, company=self.company_name, game=project.name)
        comments.append(intro)
        
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

        if avg >= 9: score_m = 6.0
        elif avg >= 8: score_m = 4.0
        elif avg >= 7: score_m = 2.5
        elif avg >= 6: score_m = 1.8
        elif avg >= 5: score_m = 1.2
        elif avg >= 4: score_m = 0.8
        else: score_m = 0.3

        fan_bonus = 1.0 + (self.fans / 100000)

        plat_multi = 1.0
        for p in PLATFORMS:
            if p["name"] == project.platform:
                plat_multi = p["market_multi"]
                break

        audience_multi = AUDIENCE_MULTI.get(project.audience, 1.0)
        rand_m = random.uniform(0.8, 1.2)

        sales = int(base_sales * score_m * fan_bonus * plat_multi * audience_multi * rand_m)
        return sales

    def calculate_dev_cost(self, project):
        """Berechnet Entwicklungskosten inkl. Größe und Marketing."""
        # Basis-Kosten basierend auf Größe
        size_data = next((s for s in GAME_SIZES if s["name"] == project.size), GAME_SIZES[1])
        base_cost = 10000 * size_data["cost_multi"]

        # Team-Kosten
        dev_weeks = sum(p["duration_weeks"] for p in DEV_PHASES) * size_data["time_multi"]
        salary_cost = sum(e.salary for e in self.employees) * dev_weeks

        # Marketing-Kosten
        from game_data import MARKETING_OPTIONS_PH5
        mark_data = next((m for m in MARKETING_OPTIONS_PH5 if m["name"] == project.marketing), {"cost": 0})
        marketing_cost = mark_data["cost"]

        return int(base_cost + salary_cost + marketing_cost)

    def finalize_game(self, project):
        """Schließt die Spielentwicklung ab."""
        project.week_developed = self.week

        # Kosten und Marketing abziehen
        project.dev_cost = self.calculate_dev_cost(project)
        self.money -= project.dev_cost
        if hasattr(self, "accounting"):
            self.accounting["expenses"] += project.dev_cost

        project.review = self.calculate_review(project)
        # Hype-Bonus für Verkäufe
        hype_multi = 1.0 + (self.hype / 100.0)
        project.sales = int(self.calculate_sales(project) * hype_multi)

        # Reset Crunch & Bugs & Hype
        self.crunch_active = False
        self.current_bugs = 0
        self.hype = 0 # Hype wird beim Release verbraucht

        price = AUDIENCE_PRICE.get(project.audience, 30)
        total_revenue = project.sales * price
        
        # Publisher Royalties
        publisher = self.current_draft.get("publisher")
        if publisher:
            royalty_cut = int(total_revenue * publisher["royalty"])
            project.revenue = total_revenue - royalty_cut
            # Einmaliger Bonus bei Vertragsabschluss (Advance)
            self.money += publisher["advance"]
        else:
            # Self-Publishing -> Vertriebskosten
            if "Digitaler Vertrieb & Logistik" in self.unlocked_technologies:
                distribution_margin = 0.15 # 15% mit Technologie
            else:
                distribution_margin = 0.30 # 30% ohne Technologie
                
            dist_cost = int(total_revenue * distribution_margin)
            project.revenue = total_revenue - dist_cost
            project.distribution_cost = dist_cost

        self.money += project.revenue
        if hasattr(self, "accounting"):
            self.accounting["income"] += project.revenue
            
        self.fans += project.sales // 10
        self.games_made += 1
        self.total_revenue += project.revenue

        # Zeit vorrücken
        size_data = next((s for s in GAME_SIZES if s["name"] == project.size), GAME_SIZES[1])
        dev_weeks = int(sum(p["duration_weeks"] for p in DEV_PHASES) * size_data["time_multi"])
        self.week += dev_weeks

        for emp in self.employees:
            emp.weeks_employed += dev_weeks
            if project.review and project.review.average >= 7:
                emp.morale = min(100, emp.morale + 5)
            elif project.review and project.review.average < 4:
                emp.morale = max(0, emp.morale - 10)

        # Wenn es ein MMO ist, erstelle ActiveMMO Objekt
        if project.size == "MMO":
            from models import ActiveMMO
            # Initiale Spielerzahl basierend auf Hype und Review
            initial_players = int((project.review.average * 10000) * (1 + self.hype * 0.05))
            mmo = ActiveMMO(game_project=project, initial_players=initial_players)
            self.active_mmos.append(mmo)

        self.game_history.append(project)
        return project

    # ==========================================================
    # TRAINING
    # ==========================================================

    def train_employee(self, emp_index, train_data):
        """Verbessert Skills eines Mitarbeiters."""
        if self.money < train_data["cost"]:
            return False
        
        emp = self.employees[emp_index]
        self.money -= train_data["cost"]
        
        # Skill-Boost auf Primärskill
        sname = emp.primary_skill
        emp.skills[sname] = min(100, emp.skills.get(sname, 0) + train_data["skill_boost"])
        # Kleiner Boost auf Sekundärskill
        s2 = emp.secondary_skill
        emp.skills[s2] = min(100, emp.skills.get(s2, 0) + train_data["skill_boost"] // 2)
        
        # Gehalt steigt leicht
        emp.salary = emp._calculate_salary()
        return True

    # ==========================================================
    # PLEITE CHECK
    # ==========================================================

    def is_bankrupt(self):
        """Prüft ob die Firma pleite ist."""
        return self.money < -50000  # Kreditrahmen von 50k


    # ==========================================================
    # STATUS
    # ==========================================================

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
        from models import Email
        self.emails.append(Email(
            sender="Marktforschung",
            subject="Marktanalyse veröffentlicht",
            body=f"Unsere Daten zeigen: {self.current_trend['text']}",
            date_week=self.week
        ))

    def get_status_text(self):
        """Statusübersicht als Text."""
        office = OFFICE_LEVELS[self.office_level]
        return (
            f"Firma: {self.company_name}. "
            f"Geld: {self.money:,} Euro. "
            f"Fans: {self.fans:,}. "
            f"Woche: {self.week}. "
            f"Büro: {office['name']}. "
            f"Mitarbeiter: {len(self.employees)} von {office['max_employees']}. "
            f"Spiele entwickelt: {self.games_made}."
        )

    # ==========================================================
    # SPEICHERN / LADEN
    # ==========================================================

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
            "office_level": self.office_level,
            "last_event_week": self.last_event_week,
            "last_trend_week": self.last_trend_week,
            "current_trend": self.current_trend,
            "active_events": getattr(self, "active_events", []),
            "settings": self.settings,
            "game_history": [g.to_dict() for g in self.game_history],
            "active_mmos": [m.to_dict() for m in getattr(self, "active_mmos", [])],
            "employees": [e.to_dict() for e in self.employees],
            "engines": [
                {"name": eng.name, "features": [
                    {"category": f.category, "name": f.name, "tech_bonus": f.tech_bonus}
                    for f in eng.features
                ]} for eng in self.engines
            ],
            "unlocked_features": [
                {"category": f.category, "name": f.name, "tech_bonus": f.tech_bonus}
                for f in self.unlocked_features
            ],
            "unlocked_technologies": self.unlocked_technologies,
            "bought_platforms": getattr(self, "bought_platforms", []),
            "active_platforms": getattr(self, "active_platforms", []),
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
            ]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
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
                except:
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
            data = json.load(f)

        self.company_name = data["company_name"]
        self.money = data["money"]
        self.fans = data["fans"]
        self.week = data["week"]
        self.high_score = data["high_score"]
        self.games_made = data["games_made"]
        self.total_revenue = data["total_revenue"]
        self.office_level = data["office_level"]
        self.last_event_week = data.get("last_event_week", 0)
        self.last_trend_week = data.get("last_trend_week", 0)
        self.current_trend = data.get("current_trend")
        self.active_events = data.get("active_events", [])

        # Engines laden
        self.unlocked_features = []
        for fd in data.get("unlocked_features", []):
            self.unlocked_features.append(
                EngineFeature(fd["category"], fd["name"], fd["tech_bonus"])
            )
        self.unlocked_technologies = data.get("unlocked_technologies", [])

        self.engines = []
        for ed in data.get("engines", []):
            features = [
                EngineFeature(fd["category"], fd["name"], fd["tech_bonus"])
                for fd in ed["features"]
            ]
            self.engines.append(Engine(ed["name"], features))

        # Spielhistorie laden
        self.game_history = []
        for gd in data.get("game_history", []):
            proj = GameProject(
                gd["name"], gd["topic"], gd["genre"],
                gd.get("sliders"), gd.get("platform"), gd.get("audience"),
                size=gd.get("size", "Mittel"), marketing=gd.get("marketing", "Kein Marketing")
            )
            if gd.get("review_scores"):
                proj.review = ReviewScore(gd["review_scores"])
            proj.sales = gd.get("sales", 0)
            proj.revenue = gd.get("revenue", 0)
            proj.dev_cost = gd.get("dev_cost", 0)
            proj.week_developed = gd.get("week_developed", 0)
            self.game_history.append(proj)

        # Aktive MMOs laden
        self.active_mmos = []
        if "active_mmos" in data:
            from models import ActiveMMO
            for md in data["active_mmos"]:
                match_game = next((g for g in self.game_history if g.name == md.get("game_dict", {}).get("name")), None)
                if match_game:
                    m = ActiveMMO(match_game, md.get("players", 0))
                    m.subscription_fee = md.get("subscription_fee", 15)
                    m.server_cost_per_10k = md.get("server_cost_per_10k", 5000)
                    m.weeks_active = md.get("weeks_active", 0)
                    self.active_mmos.append(m)

        # Mitarbeiter laden
        self.employees = []
        for ed in data.get("employees", []):
            emp = Employee.__new__(Employee)
            emp.name = ed["name"]
            emp.role = ed["role"]
            emp.primary_skill = ed["primary_skill"]
            emp.secondary_skill = ed["secondary_skill"]
            emp.skill_level = ed["skill_level"]
            emp.skills = ed["skills"]
            emp.salary = ed["salary"]
            emp.morale = ed["morale"]
            emp.weeks_employed = ed["weeks_employed"]
            emp.specialization = ed.get("specialization")
            import random
            from game_data import EMPLOYEE_TRAITS
            emp.trait = ed.get("trait") if ed.get("trait") else random.choice(EMPLOYEE_TRAITS)
            self.employees.append(emp)

        # E-Mails laden
        self.emails = []
        from models import Email
        for md in data.get("emails", []):
            mail = Email(md["sender"], md["subject"], md["body"], md["date_week"], md.get("game_name"), md.get("is_bug", False))
            mail.is_read = md.get("is_read", False)
            self.emails.append(mail)

        self.settings = data.get("settings", {"language": "de", "music_enabled": True})

        # Rivalen laden
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
        
        # Finanzen laden
        self.accounting = data.get("accounting", {"income": 0, "expenses": 0, "loan_paid": 0})
        loan_data = data.get("bank_loan")
        if loan_data:
            from models import BankLoan
            self.bank_loan = BankLoan(
                loan_data["amount_borrowed"], 0, loan_data["weeks_remaining"], 
                amount_remaining=loan_data["amount_remaining"], 
                weeks_remaining=loan_data["weeks_remaining"]
            )
            self.bank_loan.weekly_payment = loan_data["weekly_payment"]
        else:
            self.bank_loan = None
            
        # Custom Consoles laden
        self.custom_consoles = []
        if "custom_consoles" in data:
            from models import CustomConsole
            for c_data in data["custom_consoles"]:
                cc = CustomConsole(c_data["name"], c_data["tech_level"], c_data["dev_cost"], c_data["release_week"])
                cc.market_share = c_data.get("market_share", 0.05)
                self.custom_consoles.append(cc)

        self.reset_draft()
        return True
