"""Entwicklungsprojekte: Spiele, Engines, Ports, Updates, Addons. Mixin fuer GameState."""
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


class DevMixin:
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
            "size": "Mittel",
            "marketing": "Kein Marketing",
            "sub_genre": None,
            "publisher": None,
        }
        self.aaa_event_triggered = False

    def estimate_dev_time(self):
        """Schätzt die Entwicklungszeit für den aktuellen Draft (in Wochen, ca.-Angabe)."""
        size = self.current_draft.get("size", "Mittel")
        base_weeks = {"Klein": 5, "Mittel": 15, "Groß": 30, "AAA": 60}.get(size, 15)
        # Teamgröße und Speed-Modifier einrechnen
        speed = self.get_team_speed_modifier()
        if getattr(self, "co_dev_partner", None):
            speed *= 1.8
        # Geschätzte Kalenderwochen (ca.)
        estimated = max(1, int(base_weeks / max(0.5, speed)))
        return estimated

    def start_development(self):
        """Startet die Entwicklung eines neuen Spiels."""
        try:
            name = self.current_draft.get("name", "Untitled") or "Untitled"
            topic = self.current_draft.get("topic", "Fantasy")
            genre = self.current_draft.get("genre", "Action")
            platform = self.current_draft.get("platform", {"name": "PC"})
            audience = self.current_draft.get("audience", "Jeder")
            engine = self.current_draft.get("engine", None)
            size = self.current_draft.get("size", "Mittel")
            marketing = self.current_draft.get("marketing", "Kein Marketing")
            sliders = self.current_draft.get("sliders", {})
            
            plat_name = platform['name'] if isinstance(platform, dict) else platform
            
            project = GameProject(
                name=name, topic=topic, genre=genre, sliders=sliders,
                platform=plat_name, audience=audience, engine=engine,
                size=size, marketing=marketing
            )
            
            # Team-Zuweisung
            if "assigned_employee_ids" in self.current_draft:
                project.assigned_employee_ids = self.current_draft["assigned_employee_ids"]
            else:
                project.assigned_employee_ids = [i for i, e in enumerate(self.employees) if not getattr(e, 'is_sick', False) and not getattr(e, 'is_training', False) and getattr(e, 'vacation_weeks_left', 0) <= 0]
            
            project.sequel_number = self.current_draft.get("sequel_number", 0)
            project.sub_genre = self.current_draft.get("sub_genre", None)
            project.is_remaster = self.current_draft.get("is_remaster", False)
            
            base_weeks = {"Klein": 5, "Mittel": 15, "Groß": 30, "AAA": 60}.get(size, 15)
            
            new_active = {
                "project": project,
                "progress": 0.0,
                "total_weeks": base_weeks,
                "bugs": 0,
                "crunch": False,
                "ready_to_finish": False,
                "event_count": 0,
                "aaa_event_done": False,
                "co_dev": getattr(self, "co_dev_partner", None),
                "publisher": self.current_draft.get("publisher")
            }
            self.active_projects.append(new_active)
            self.reset_draft()
            self.co_dev_partner = None # Reset für nächstes Spiel
        except Exception as e:
            with open("crash_log.txt", "a", encoding="utf-8") as f:
                import traceback
                f.write(f"\nSTART_DEV CRASH: {str(e)}\n")
                f.write(traceback.format_exc())
            raise e

    def can_start_development(self, size):
        """Prüft ob alle Voraussetzungen für den Entwicklungsstart erfüllt sind."""
        # 1. Genug Mitarbeiter?
        if not self.employees:
            return False, "no_employees"
            
        # 2. Genug Geld? (Wird beim Start abgezogen, hier nur Vorab-Check)
        # 3. Genug Arbeitsplätze?
        workplaces = sum(1 for obj in self.office_objects if obj.object_type == "Desk" or obj.object_type == "workplace")
        if workplaces < len(self.employees):
            return False, "not_enough_workplaces"
            
        # 4. Spezielle Anforderungen für AAA (z.B. 1980+)
        if size == "AAA" and self.get_calendar_year() < 1980:
            return False, "aaa_too_early"
            
        return True, ""

    def start_crowdfunding_campaign(self, target_amount):
        """Startet eine Crowdfunding Kampagne für das aktuelle Draft."""
        if not self.current_draft:
            return False, "Kein Projektentwurf vorhanden."
            
        name = self.current_draft.get("name", "Untitled") or "Untitled"
        
        # Basis-Wahrscheinlichkeit durch Fans
        # 1 Fan = ~1 EUR potenziell
        expected_funding = self.fans * random.uniform(0.5, 1.5)
        
        # Hype Bonus
        hype_bonus = 1.0 + (self.hype / 100.0)
        expected_funding *= hype_bonus
        
        if expected_funding >= target_amount:
            # Erfolg!
            self.money += target_amount
            self.track_income("other", target_amount)
            self.fans += int(target_amount / 100) # Ein paar Fans kommen dazu durch die Kampagne
            self.hype = min(250, self.hype + 50) # Massive Hype
            
            # Merke das Crowdfunding
            deadline = self.week + random.randint(40, 60) # ~ 1 Jahr Zeit
            self.active_crowdfundings.append({
                "project_name": name,
                "deadline_week": deadline,
                "target": target_amount
            })
            
            # Projekt starten (wir markieren das Projekt als crowdfunded)
            self.start_development()
            
            # Das soeben erstellte Projekt ist das letzte in active_projects
            if self.active_projects:
                proj = self.active_projects[-1]["project"]
                proj.is_crowdfunded = True
            
            return True, "success"
        else:
            # Fehlschlag!
            self.hype = max(0, self.hype - 20) # Peinlicher Fehlschlag
            self.failed_crowdfundings += 1
            return False, "failed"

    def start_port_project(self, game_name, new_platform):
        """Startet einen Port eines alten Spiels auf eine neue Plattform."""
        original_game = next((g for g in self.game_history if g.name == game_name), None)
        if not original_game:
            return False

        # Neues GameProject erstellen
        port_name = f"{original_game.name} ({new_platform})"
        
        project = GameProject(
            name=port_name,
            topic=original_game.topic,
            genre=original_game.genre,
            sliders=original_game.sliders.copy() if original_game.sliders else {},
            platform=new_platform,
            audience=original_game.audience,
            engine=original_game.engine,
            size=original_game.size,
            marketing="Kein Marketing"
        )
        
        # Attribute uebernehmen
        project.is_port = True
        project.original_game_name = game_name
        project.sub_genre = original_game.sub_genre
        project.sequel_number = original_game.sequel_number
        project.languages = original_game.languages.copy()
        
        # Entwicklungszeit ist deutlich geringer (30% der Originalzeit)
        base_weeks = {"Klein": 5, "Mittel": 15, "Groß": 30, "AAA": 60}.get(original_game.size, 15)
        port_weeks = max(2, int(base_weeks * 0.3))
        
        # Team zuweisen (alle verfuegbaren)
        project.assigned_employee_ids = [i for i, e in enumerate(self.employees) if not getattr(e, 'is_sick', False) and not getattr(e, 'is_training', False) and getattr(e, 'vacation_weeks_left', 0) <= 0]

        new_active = {
            "project": project,
            "progress": 0.0,
            "total_weeks": port_weeks,
            "bugs": 0,
            "crunch": False,
            "ready_to_finish": False,
            "event_count": 0,
            "aaa_event_done": False,
            "co_dev": None,
            "publisher": None
        }
        self.active_projects.append(new_active)
        return True

    def start_merch_campaign(self, game_name, merch_type, duration_weeks, investment):
        """Startet eine neue Merchandising-Kampagne."""
        if self.money < investment:
            return False
            
        self.track_expense("marketing", investment)
        
        from models import MerchCampaign
        camp = MerchCampaign(game_name, merch_type, duration_weeks, investment)
        self.active_merch_campaigns.append(camp)
        return True

    def start_update_project(self, game_name, update_type, name="Update", selected_languages=None):
        """Startet ein Update- oder DLC-Projekt für ein existierendes Spiel."""
        # Suche das Basisspiel
        game = next((g for g in self.game_history if g.name == game_name), None)
        if not game:
            return False
            
        dev_cost = 0
        total_weeks = 0
        
        if update_type == "Patch":
            # Repariert 50% der Bugs
            dev_cost = 5000
            total_weeks = 2
        elif update_type == "Content":
            # Erhöht Hype und Fans
            dev_cost = 20000
            total_weeks = 4
        elif update_type == "DLC":
            # Kostet mehr, bringt aber Einnahmen
            dev_cost = 50000
            total_weeks = 8
        elif update_type == "Language":
            # Fügt neue Sprachen hinzu
            langs = selected_languages or []
            dev_cost = len(langs) * 10000
            # Mindestens 1 Woche, um ZeroDivisionError zu vermeiden
            total_weeks = max(1, len(langs))
            
        from models import UpdateProject
        update = UpdateProject(
            base_game_name=game_name,
            name=name,
            update_type=update_type,
            dev_cost=dev_cost,
            total_weeks=total_weeks,
            languages=selected_languages
        )
        
        new_active = {
            "project": update,
            "progress": 0.0,
            "total_weeks": total_weeks,
            "bugs": 0
        }
        self.active_projects.append(new_active)
        return True

    def start_manufacturing_job(self, game_name, amount, cost_per_unit, weeks):
        """Startet einen Auftrag zur Produktion physischer Kopien."""
        if self.money < amount * cost_per_unit:
            return False
            
        self.track_expense("production", amount * cost_per_unit)
        
        job = ManufacturingJob(game_name, amount, cost_per_unit, weeks)
        self.manufacturing_jobs.append(job)
        return True

    def add_mtx_to_game(self, game_name):
        """Fügt Mikrotransaktionen/Lootboxen zu einem bestehenden Spiel hinzu."""
        game = next((g for g in self.game_history if g.name == game_name), None)
        if game and not getattr(game, 'has_mtx', False):
            game.has_mtx = True
            # Initialer Shitstorm bei den Fans
            fan_loss = int(self.fans * 0.05)
            self.fans = max(0, self.fans - fan_loss)
            
            # Email using get_text for blind-accessibility localization
            self.emails.insert(0, Email(
                sender=self.get_text('mtx_email_sender', default="Community Manager"),
                subject=self.get_text('mtx_email_subject', default="Shitstorm!"),
                body=self.get_text('mtx_email_body', game=game.name, fans=fan_loss, default=f"Lootboxen in {game.name} kosten uns {fan_loss} Fans!"),
                date_week=self.week
            ))
            return True
        return False

    def buy_anti_cheat(self, game_name):
        """Kauft ein Anti-Cheat System für ein MMO oder F2P Spiel."""
        game = next((g for g in self.game_history if g.name == game_name), None)
        if game and not getattr(game, 'has_anti_cheat', False):
            if game.is_f2p or any(m.game.name == game_name for m in getattr(self, 'active_mmos', [])):
                cost = 100000
                if self.money >= cost:
                    self.money -= cost
                    game.has_anti_cheat = True
                    return True
        return False

    def use_ai_assets(self, ap_idx):
        """Nutzt KI-generierte Assets fur einen massiven Fortschrittsschub auf eigenes Risiko."""
        if 0 <= ap_idx < len(self.active_projects):
            ap = self.active_projects[ap_idx]
            proj = ap["project"]
            if not getattr(proj, 'used_ai_assets', False):
                proj.used_ai_assets = True
                progress_boost = min(10.0, ap["total_weeks"] * 0.3)
                ap["progress"] += progress_boost
                
                self.emails.insert(0, Email(
                    sender=self.get_text('ai_email_sender', default="Lead Developer"),
                    subject=self.get_text('ai_email_subject', default="KI-Assets integriert"),
                    body=self.get_text('ai_email_body', default="Boss, wir haben die KI-Assets ins Spiel integriert. Das spart uns Wochen an Arbeit! Hoffen wir, dass niemand merkt, woher die Daten stammen..."),
                    date_week=self.week
                ))
                return True
        return False

    def use_ai_soundtrack(self, ap_idx):
        """Nutzt KI-generierte Soundtracks für das Projekt (benötigt Forschung)."""
        if 0 <= ap_idx < len(self.active_projects):
            ap = self.active_projects[ap_idx]
            proj = ap["project"]
            if not getattr(proj, 'used_ai_soundtrack', False):
                proj.used_ai_soundtrack = True
                self.emails.insert(0, Email(
                    sender=self.get_text('ai_email_sender', default="Lead Developer"),
                    subject="KI-Soundtrack integriert",
                    body="Wir haben die Musik komplett durch KI generieren lassen. Es klingt unglaublich gut, und wir haben uns Monate an Studiozeit gespart. Hoffentlich gibt es keinen Shitstorm...",
                    date_week=self.week
                ))
                return True
        return False

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
        self.track_expense("production", cost)
        print(f"Old dlc_count: {game.dlc_count}"); game.dlc_count += 1; print(f"New dlc_count: {game.dlc_count}")
        game.is_active = True # Bringt Spiel zurück in die Charts
        # Markt-Reset: Ca. 1 Monat (dynamisch)
        reset_weeks = max(4, int(WEEKS_PER_YEAR / 10))
        game.weeks_on_market = max(0, game.weeks_on_market - reset_weeks)
        self.fans += 500
        return True

    def release_mmo_update(self, mmo_index):
        """Programmiert ein Content-Update für ein MMO, um Spieler zurückzugewinnen."""
        mmo = self.active_mmos[mmo_index]
        cost = 50000
        if self.money < cost:
            return False
        self.track_expense("mmo", cost)
        # Füge Spieler hinzu basierend auf Basis-Spielerzahl (z.B. +10% max)
        new_players = int(mmo.game.sales * 0.05)
        mmo.players += new_players
        self.fans += 1000
        return True

    def create_engine(self, name, feature_list):
        """Erstellt eine neue Engine aus freigeschalteten Features."""
        engine = Engine(name, feature_list)
        self.engines.append(engine)
        return engine

    def create_addon(self, base_game_idx):
        """Erstellt ein Addon für ein Basisspiel."""
        from game_data import ADDON_DATA
        
        base_game = self.game_history[base_game_idx]
        if not base_game.is_active:
            return None # Nur für aktive Spiele
            
        # Überprüfe ob schon ein Addon dafür existiert
        if any(a.base_game_name == base_game.name for a in self.active_addons):
            return None
            
        cost = int(base_game.dev_cost * ADDON_DATA["cost_multi"])
        if self.money < cost:
            return None
            
        self.track_expense("production", cost)
        addon = AddonProject(
            base_game_name=base_game.name,
            name=f"{base_game.name}: Expansion",
            topic=base_game.topic,
            genre=base_game.genre,
            dev_cost=cost
        )
        addon.week_developed = self.week
        self.active_addons.append(addon)
        
        return {
            'name': addon.name,
            'sales': 0,
            'revenue': 0, # Wird in den nächsten Wochen generiert
            'cost': cost
        }

    def create_bundle(self, game_indices):
        """Kombiniert mehrere inaktive Spiele zu einem Bundle."""
        from game_data import BUNDLE_DATA
        
        if len(game_indices) < BUNDLE_DATA["min_games"] or len(game_indices) > BUNDLE_DATA["max_games"]:
            return None
            
        games = []
        for idx in game_indices:
            game = self.game_history[idx]
            if game.is_active:
                return None # Spiele müssen vom Markt sein
            games.append(game.to_dict())
            
        # Name des Bundles generieren
        topics = list(set([g['topic'] for g in games]))
        bundle_name = f"{self.company_name} {topics[0]} Collection" if topics else f"{self.company_name} Mega Bundle"
        
        bundle = BundleProject(name=bundle_name, games=games, base_price=BUNDLE_DATA["base_price"])
        self.active_bundles.append(bundle)
        
        # Initialer Boost durch Bundle-Ankündigung
        initial_sales = int(1000 * bundle.average_score)
        initial_revenue = initial_sales * bundle.base_price
        
        bundle.sales += initial_sales
        bundle.revenue += initial_revenue
        self.track_income("sales", initial_revenue)
        
        return {
            'name': bundle.name,
            'sales': bundle.sales,
            'revenue': bundle.revenue
        }

    def finalize_game(self, ap_dict, early_access=False):
        """Schließt die Spielentwicklung ab."""
        project = ap_dict["project"]
        bugs = ap_dict["bugs"]
        
        was_early_access = project in self.game_history
        
        project.week_developed = self.week

        # Kosten und Marketing abziehen
        new_dev_cost = self.calculate_dev_cost(project)
        cost_diff = new_dev_cost - getattr(project, "dev_cost", 0)
        project.dev_cost = new_dev_cost
        if cost_diff > 0:
            self.track_expense("production", cost_diff)

        project.review = self.calculate_review(project, bugs=bugs)
        
        # KI-Assets Copyright Strike logic
        if getattr(project, 'used_ai_assets', False):
            if random.random() < 0.30: # 30% Lawsuit chance
                project.review.scores = [max(1, s - 2) for s in project.review.scores]
                lawsuit_cost = 500000
                self.money -= lawsuit_cost
                self.track_expense("other", lawsuit_cost)
                self.fans = max(0, self.fans - 50000)
                self.emails.insert(0, Email(
                    sender=self.get_text('lawsuit_email_sender', default="Anwaltskanzlei"),
                    subject=self.get_text('lawsuit_email_subject', default="URHEBERRECHTSVERLETZUNG!"),
                    body=self.get_text('lawsuit_email_body', game=project.name, cost=lawsuit_cost, default=f"Sie werden wegen Urheberrechtsverletzung durch KI-generierte Assets in {project.name} verklagt! Strafe: {lawsuit_cost} Euro. Die Fans sind empört!"),
                    date_week=self.week
                ))
            else:
                # Minor penalty for generic assets
                project.review.scores = [max(1, s - 1) for s in project.review.scores]
        
        # Hype-Bonus berechnen und anwenden
        self.hype += self.calculate_hype(project)
        hype_multi = 1.0 + (self.hype / 100.0)
        new_sales = int(self.calculate_sales(project) * hype_multi)
        project.sales = getattr(project, "sales", 0) + new_sales

        if getattr(project, "is_f2p", False):
            project.active_players = getattr(project, "active_players", 0) + new_sales
            price = 0
        else:
            price = AUDIENCE_PRICE.get(project.audience, 30)
            if "(VR)" in project.platform:
                price = int(price * 1.5) # VR Spiele sind deutlich teurer
            
        total_revenue_new = int(new_sales * price * self.profit_multiplier)
        
        # Publisher Royalties
        publisher = ap_dict.get("publisher")
        
        if publisher:
            royalty_cut = int(total_revenue_new * publisher["royalty"])
            new_revenue = total_revenue_new - royalty_cut
            if not was_early_access:
                self.track_income("publishing", publisher["advance"])
        else:
            if "Digitaler Vertrieb & Logistik" in self.unlocked_technologies:
                distribution_margin = 0.15 
            else:
                distribution_margin = 0.30 
                
            dist_cost = int(total_revenue_new * distribution_margin)
            new_revenue = total_revenue_new - dist_cost
            if hasattr(project, "distribution_cost"):
                project.distribution_cost += dist_cost
            else:
                project.distribution_cost = dist_cost
                
        # Dritte-Partei Engine Revenue Share
        if getattr(project, "engine", None):
            rev_share = getattr(project.engine, "revenue_share", 0.0)
            if rev_share > 0.0:
                engine_cut = int(new_revenue * rev_share)
                new_revenue -= engine_cut
                # Track engine expense optionally
                self.track_expense("other", engine_cut)

        project.revenue = getattr(project, "revenue", 0) + new_revenue

        # Co-Dev aus dem AP-Dict
        if ap_dict.get("co_dev") and not was_early_access:
            partner = ap_dict["co_dev"]
            refund = int(new_dev_cost * 0.5)
            self.track_income("other", refund)
            project.revenue = int(project.revenue * 0.5)
            self.emails.insert(0, Email(
                sender=partner,
                subject=self.get_text('subject_co_dev', name=project.name),
                body=self.get_text('body_co_dev', refund=refund, revenue=project.revenue),
                date_week=self.week
            ))
            
        # Projekt aus Liste entfernen
        if not early_access:
            if ap_dict in self.active_projects:
                self.active_projects.remove(ap_dict)
            
            # Crowdfunding abschliessen
            if getattr(project, "is_crowdfunded", False):
                to_remove = []
                for cf in self.active_crowdfundings:
                    if cf["project_name"] == project.name:
                        to_remove.append(cf)
                for cf in to_remove:
                    self.active_crowdfundings.remove(cf)
            
        # Post-Game Logic
        self.co_dev_partner = None

        self.track_income("sales", new_revenue)
            
        # Fan-Gain durch Spiel und Lizenz
        fan_base_gain = int(new_revenue * 0.005 * (project.review.average / 10))
        if getattr(project, 'license_bonus', 0) > 0 and not was_early_access:
            fan_base_gain += int(project.license_bonus * 50)
            
        # VR-Fan-Boost fr gute Spiele!
        if "(VR)" in project.platform and project.review.average >= 75:
            fan_base_gain *= 3
            
        self.fans += fan_base_gain
        if not was_early_access:
            self.games_made += 1
        self.total_revenue += new_revenue

        # Moral-Anpassung nach Release
        for emp in self.employees:
            if project.review and project.review.average >= 7:
                emp.morale = min(100, emp.morale + 5)
            elif project.review and project.review.average < 4:
                emp.morale = max(0, emp.morale - 10)

        # Wenn es ein MMO ist, erstelle ActiveMMO Objekt
        if project.size == "MMO" and not was_early_access:
            # Initiale Spielerzahl basierend auf Hype und Review
            initial_players = int((project.review.average * 10000) * (1 + self.hype * 0.05))
            mmo = ActiveMMO(game_project=project, initial_players=initial_players)
            self.active_mmos.append(mmo)
        
        # Hype wird erst JETZT verbraucht, damit MMOs den Bonus noch mitnehmen
        self.hype = 0
        # IP-Rating berechnen (0-100 basierend auf Review)
        if project.review:
            avg = project.review.average
            project.ip_rating = int(min(100, max(0, (avg - 3) * 14.3)))  # 3→0, 10→100
        
        # Sub-Genre aus Draft übernehmen
        project.sub_genre = self.current_draft.get("sub_genre", None)

        if project not in self.game_history:
            self.game_history.append(project)
        return project

    def finalize_engine(self, ap_dict):
        """Schließt die Engine-Entwicklung ab."""
        proj = ap_dict["project"]
        from models import Engine
        new_engine = Engine(proj.name, proj.features)
        self.engines.append(new_engine)
        
        if ap_dict in self.active_projects:
            self.active_projects.remove(ap_dict)
            
        self.emails.insert(0, Email(
            sender=self.get_text('engine_email_sender', default="Lead Engineer"),
            subject=self.get_text('engine_email_subject', default="Engine fertiggestellt!"),
            body=self.get_text('engine_email_body', default=f"Boss, die Entwicklung von {proj.name} ist abgeschlossen. Die Engine steht uns nun zur Verfügung!"),
            date_week=self.week
        ))
        return True

    def start_engine_project(self, name, features):
        """Startet ein Projekt zur Entwicklung einer eigenen Engine."""
        from models import EngineProject
        
        base_cost = 500000
        base_weeks = 4
        
        for f in features:
            base_cost += f.tech_bonus * 40000
            base_weeks += f.tech_bonus * 1
            
        if self.money < base_cost:
            return False
            
        proj = EngineProject(name, features, base_cost, base_weeks)
        
        self.money -= base_cost
        self.track_expense("other", base_cost)
        
        self.active_projects.append({
            "project": proj,
            "progress": 0.0,
            "total_weeks": base_weeks,
            "bugs": 0,
            "crunch": False,
            "ready_to_finish": False,
            "assigned_employee_ids": []
        })
        return True

    def _process_port_projects(self):
        """Verarbeitet aktive Portierungs-Projekte."""
        if not hasattr(self, "port_projects"):
            self.port_projects = []
            
        for port in list(self.port_projects):
            if not port.is_finished:
                # Calculate progress based on employees
                progress_gain = 0.0
                for emp in self.employees:
                    if emp.morale > 0 and not getattr(emp, "is_training", False) and not getattr(emp, "is_sick", False):
                        progress_gain += emp.speed / 1000.0  # arbitrary scale
                
                port.progress += progress_gain
                
                if port.progress >= 1.0:
                    port.progress = 1.0
                    port.is_finished = True
                    self.port_projects.remove(port)
                    # Create new game project based on original game
                    orig = next((g for g in self.game_history if g.name == port.original_game_name), None)
                    if orig:
                        from models import GameProject, ReviewScore
                        new_name = f"{orig.name} ({port.new_platform})"
                        new_game = GameProject(new_name, orig.topic, orig.genre, orig.sliders, port.new_platform, orig.audience, orig.engine, orig.size, orig.marketing)
                        new_game.review = ReviewScore([min(10, s + random.randint(-1, 1)) for s in orig.review.scores])
                        new_game.sales = 0
                        new_game.revenue = 0
                        new_game.dev_cost = port.dev_cost
                        new_game.week_developed = self.week
                        self.game_history.append(new_game)
                        self.emails.insert(0, Email(
                            sender="System",
                            subject="Portierung abgeschlossen",
                            body=f"Das Spiel {port.original_game_name} wurde erfolgreich auf {port.new_platform} portiert und veröffentlicht!",
                            date_week=self.week
                        ))
                        if hasattr(self, "audio"):
                            self.audio.speak(f"Portierung von {port.original_game_name} auf {port.new_platform} abgeschlossen.")

    def _finish_update_project(self, update):
        """Wendet die Effekte eines fertigen Updates/DLCs an."""
        game = next((g for g in self.game_history if g.name == update.base_game_name), None)
        if not game: return
        
        game.updates.append(update)
        
        if update.update_type == "Patch":
            bugs_to_fix = int(game.bugs * 0.5) + 1
            game.bugs = max(0, game.bugs - bugs_to_fix)
            game.total_bugs_fixed += bugs_to_fix
        elif update.update_type == "Content":
            self.fans += 500
            self.hype = min(100, self.hype + 20)
        elif update.update_type == "Language":
            for l in update.languages:
                if l not in game.languages:
                    game.languages.append(l)
        elif update.update_type == "DLC":
            game.dlc_count += 1
            game.is_active = True
            game.sales += int(game.sales * 0.1)
                    
        self.emails.insert(0, Email(
            sender=self.get_text('sender_dev'),
            subject=self.get_text('subject_update_finished', name=update.name),
            body=self.get_text('body_update_finished', game=game.name, type=update.update_type),
            date_week=self.week
        ))

    def generate_contract_work_options(self):
        """Generiert 3 zufaellige Auftragsarbeiten."""

        options = []
        types = ["Code", "Audio", "Grafik", "Design"]
        
        base_points = 50 + (self.prestige * 5)
        base_payout = 2000 + (self.prestige * 200)
        
        for i in range(3):
            ctype = random.choice(types)
            diff = random.randint(1, 3)
            
            target_points = base_points * diff * random.uniform(0.8, 1.2)
            payout = base_payout * diff * random.uniform(0.9, 1.3)
            
            titles = []
            if ctype == "Code":
                titles = ["Datenbank-Optimierung", "Netzwerk-Code", "KI-Routinen", "Bugfixing extern"]
            elif ctype == "Audio":
                titles = ["Soundeffekte", "Podcast-Jingle", "Hintergrundmusik", "Voice-Over"]
            elif ctype == "Grafik":
                titles = ["Logo-Design", "3D-Modellierung", "Sprite-Animationen", "UI-Mockups"]
            else:
                titles = ["Level-Design", "Gamedesign-Dokument", "Balancing-Tabelle", "Quest-Schreiben"]
                
            name = f"{random.choice(titles)} ({ctype})"
            
            options.append({
                "name": name,
                "type": ctype,
                "target_points": int(target_points),
                "payout": int(payout)
            })
            
        return options

    def start_contract_work(self, option_data):
        """Startet einen ausgewaehlten Auftrag."""
        from models import ContractWorkProject
        cw = ContractWorkProject(
            name=option_data["name"],
            work_type=option_data["type"],
            target_points=option_data["target_points"],
            payout=option_data["payout"]
        )
        self.active_projects.append({
            "project": cw,
            "progress": 0.0,
            "total_weeks": 9999,
            "bugs": 0,
            "crunch": False,
            "ready_to_finish": False,
            "assigned_employee_ids": []
        })
        return True

    def finish_contract_work(self, ap_dict):
        """Schliesst eine Auftragsarbeit ab und zahlt aus."""
        proj = ap_dict["project"]
        self.track_income("other", proj.payout)
        if ap_dict in self.active_projects:
            self.active_projects.remove(ap_dict)
        return True
