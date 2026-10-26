"""
Simulation und Wochen-Zyklus System für Audio Studio Tycoon.
Verwaltet Zeitverlauf, wöchentliche Updates, Marktverkäufe, Events und Statusberichte.
"""

import random
from models import Email, CustomConsole
from game_data import (
    WEEKS_PER_YEAR, START_YEAR, AUDIENCE_PRICE, FEATURE_UNLOCKS,
    AAA_DEV_EVENTS, GENERAL_DEV_EVENTS, BUNDLE_DATA, PLATFORMS,
    HARDWARE_TECH_LIST
)


class SimulationMixin:
    """Mixin für Zeitsteuerung, wöchentlichen Simulationszyklus und Statusanzeigen."""

    def get_calendar_year(self):
        """Gibt das aktuelle Kalenderjahr zurück (Start: START_YEAR)."""
        return START_YEAR + (self.week - 1) // WEEKS_PER_YEAR

    def is_feature_unlocked(self, feature_id):
        """Prüft ob ein Feature laut FEATURE_UNLOCKS verfügbar ist."""
        feature = FEATURE_UNLOCKS.get(feature_id)
        if not feature:
            return True

        current_year = self.get_calendar_year()
        if "year" in feature and current_year < feature["year"]:
            return False

        if "office_level" in feature and self.office_level < feature["office_level"]:
            return False

        return True

    def get_calendar_text(self):
        """Gibt Kalenderjahr, Monat und Woche zurück (dynamisch basierend auf WEEKS_PER_YEAR)."""
        year = self.get_calendar_year()
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1

        month_idx = int((week_in_year - 1) * 12 / WEEKS_PER_YEAR)
        month_key = [
            "month_jan", "month_feb", "month_mar", "month_apr", "month_may", "month_jun",
            "month_jul", "month_aug", "month_sep", "month_oct", "month_nov", "month_dec"
        ][min(month_idx, 11)]

        month_name = self.get_text(month_key)
        weeks_per_month = WEEKS_PER_YEAR / 12
        week_in_month = int(((week_in_year - 1) % weeks_per_month) + 1)

        return f"{month_name} {year}, {self.get_text('calendar_week')} {week_in_month}"

    def get_speed_text(self):
        """Gibt Text für aktuelle Geschwindigkeit zurück."""
        if self.time_speed == 0:
            return self.get_text('paused')
        if self.time_speed == 0.5:
            return self.get_text('speed_slow')
        if self.time_speed == 1:
            return self.get_text('speed_normal')
        if self.time_speed == 2:
            return self.get_text('speed_fast')
        return self.get_text('speed_ultra')

    def update_tick(self, dt_ms):
        """Aktualisiert Spielzeit basierend auf Millisekunden."""
        if self.time_speed == 0 or self.pause_for_menu:
            return

        ms_per_week = 15000 / self.time_speed
        self.week_progress += dt_ms / ms_per_week

        # Hype Decay (ca. 10% pro Woche)
        if self.hype > 0:
            decay_sec = 0.1 * (dt_ms / ms_per_week)
            self.hype = max(0.0, self.hype - decay_sec)

        while self.week_progress >= 1.0:
            self.week_progress -= 1.0
            self.week += 1
            self._on_new_week()

    @property
    def is_developing(self):
        return len(self.active_projects) > 0

    def _on_new_week(self):
        """Logik die jede Woche passiert (Gehalt, Zufallsereignisse, Verkäufe, etc.)."""
        # --- Mitarbeiter-Wochenupdate & Headhunting ---
        for emp in self.employees:
            emp.weeks_employed = getattr(emp, "weeks_employed", 0) + 1

            if emp.weeks_employed % 48 == 0 and emp.skill_level > 1:
                emp.talent_points = getattr(emp, "talent_points", 0) + 1

            if 'Marketing-Guru' in getattr(emp, 'talents', []):
                self.hype = min(100.0, self.hype + 0.1)

            if getattr(self, "pending_headhunt_event", None) is None:
                if emp.skill_level >= 3 and not emp.is_ceo:
                    if random.random() < 0.005:  # 0.5% chance per week per senior employee
                        rival_offer = int(emp.salary * random.uniform(1.3, 2.0))
                        self.pending_headhunt_event = {
                            "employee": emp,
                            "rival_offer": rival_offer
                        }
                        if hasattr(self.audio, "play_sound"):
                            self.audio.play_sound("error")
                        if hasattr(self.audio, "speak"):
                            self.audio.speak(f"Achtung! Ein Rivale versucht {emp.name} abzuwerben!")

        # Subsystem-Updates
        self.update_subscription_service()
        self._process_engine_licensing()
        self._process_port_projects()
        if hasattr(self, 'publisher_manager'):
            self.publisher_manager.update_tick()
        self._process_podcast_network()
        self._process_cloud_gaming()
        self._process_audio_pass()

        # Monatsankündigung
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        prev_week_in_year = (self.week - 2) % WEEKS_PER_YEAR + 1 if self.week > 1 else 0

        current_month = int((week_in_year - 1) * 12 / WEEKS_PER_YEAR)
        prev_month = int((prev_week_in_year - 1) * 12 / WEEKS_PER_YEAR) if self.week > 1 else -1

        is_new_month = (current_month != prev_month)

        if is_new_month and self.week > 1:
            cal = self.get_calendar_text()
            self.emails.insert(0, Email(
                sender=self.get_text('sender_calendar'),
                subject=self.get_text('subject_new_month', date=cal),
                body=self.get_text('body_new_month', date=cal,
                                   money=self.money, fans=int(self.fans)),
                date_week=self.week
            ))
            if hasattr(self, 'audio'):
                self.audio.speak(self.get_text('announce_new_month', date=cal), interrupt=False)

        # Manager Ticks
        self.hr_manager.tick()
        self.finance_manager.tick(is_new_month)
        self.marketing_manager.tick(is_new_month)
        self.corporate_warfare.tick(self)
        self.union_manager.tick(self)
        self.stock_manager.tick(self)
        self.subscription_manager.tick(self)
        self.monetization_manager.tick(self)
        self.publishing_manager.tick(self)
        self.crypto_manager.tick(self)
        self.monopoly_manager.tick(self)
        self.global_event_manager.tick(self)
        self.it_manager.tick(self)
        self.convention_manager.tick(self)
        self.real_estate_manager.tick(self)

        # Eigene Konsolenverkaeufe und Marktanteil
        if hasattr(self, "custom_consoles"):
            for cc in self.custom_consoles:
                base_sales = int(5000 * cc.market_share * (1.0 + getattr(cc, 'hype', 0) / 100))
                exclusives_bonus = 1.0
                for game in self.game_history:
                    if game.platform == cc.name and game.sales > 0:
                        exclusives_bonus += 0.5 * (game.review.average / 10.0)

                weekly_sales = int(base_sales * exclusives_bonus)
                saturation = getattr(cc, 'units_sold', 0) / 100000000.0
                weekly_sales = int(weekly_sales * max(0.1, 1.0 - saturation))

                cc.units_sold = getattr(cc, 'units_sold', 0) + weekly_sales
                profit = weekly_sales * 50
                if profit > 0:
                    self.money += profit
                    self.track_income("hardware", profit)

                cc.market_share = min(0.6, cc.market_share + (weekly_sales / 10000000.0))
                if getattr(cc, 'hype', 0) > 0:
                    cc.hype = max(0, cc.hype - 0.5)

        # Metaverse Bubble Logic
        if getattr(self, "metaverse_investment", 0) > 0 and not getattr(self, "metaverse_burst", False):
            self.metaverse_weeks_active = getattr(self, "metaverse_weeks_active", 0) + 1
            growth = random.uniform(0.01, 0.05)
            self.metaverse_land_value *= (1 + growth)

            if self.metaverse_weeks_active > 24:
                risk = 0.005 + (self.metaverse_weeks_active - 24) * 0.001
                if random.random() < risk:
                    self.metaverse_burst = True
                    self.metaverse_land_value = 0
                    self.hype = max(0, self.hype - 30)
                    for e in self.employees:
                        e.morale = max(0, e.morale - 20)
                    self.active_events.append({
                        "name": "AudioVerse-Blase geplatzt!",
                        "effect": "none",
                        "multiplier": 1.0,
                        "duration": 4
                    })

        # Zufallsereignisse prüfen
        self.check_random_event()

        # Abgelaufene Events entfernen
        new_active = []
        for e in self.active_events:
            if "duration" in e:
                e["duration"] -= 1
                if e["duration"] > 0:
                    new_active.append(e)
            else:
                new_active.append(e)
        self.active_events = new_active

        # Projektfortschritt für alle aktiven Projekte
        for ap in list(self.active_projects):
            if getattr(self, 'strike_weeks_left', 0) > 0 or (hasattr(self, 'union_manager') and self.union_manager.is_striking):
                continue
            proj = ap["project"]

            # Auftragsarbeiten
            if getattr(proj, "target_points", None) is not None:
                points_added = 0.0
                skill_map = {"Code": "Programmierung", "Audio": "Sound", "Grafik": "Grafik", "Design": "Design"}
                skill_name = skill_map.get(proj.type, "Programmierung")

                active_emps = self._active_employees(proj)
                for emp in active_emps:
                    base_points = emp.skills.get(skill_name, 50) / 10.0
                    if 'Agile Coach' in getattr(emp, 'talents', []):
                        base_points *= 1.2
                    points_added += base_points

                if not active_emps:
                    points_added = 5.0

                points_added *= getattr(self, "dev_speed_multiplier", 1.0)
                if hasattr(self, 'union_manager') and self.union_manager.ai_tools_active:
                    points_added *= 2.0
                proj.current_points = min(proj.target_points, proj.current_points + points_added)

                if proj.current_points >= proj.target_points:
                    ap["ready_to_finish"] = True

                # Moral-Malus
                if ap.get("crunch"):
                    has_break = self.has_office_bonus("morale_room")
                    break_mod = 0.5 if has_break else 1.0
                    for emp in active_emps:
                        morale_loss = int(random.randint(2, 5) * break_mod)
                        if getattr(emp, "personality", None) == "workaholic":
                            morale_loss = int(morale_loss * 1.5)
                        if 'Crunch-Survivor' in getattr(emp, 'talents', []):
                            emp.morale = 100
                        else:
                            emp.morale = max(0, emp.morale - morale_loss)
                else:
                    for emp in active_emps:
                        if getattr(emp, "personality", None) == "workaholic":
                            if 'Crunch-Survivor' in getattr(emp, 'talents', []):
                                emp.morale = 100
                            else:
                                emp.morale = max(0, emp.morale - 1)
                        else:
                            emp.morale = max(0, emp.morale - 1)
                continue

            boost = 2 if ap.get("crunch") else 1
            if getattr(proj, 'is_remaster', False):
                boost *= 1.5

            # Burnout-Event Malus / Talent-Boom Bonus
            for e in self.active_events:
                if e["effect"] == "dev_speed_drop":
                    boost *= e["multiplier"]
                elif e["effect"] == "dev_speed_boost":
                    boost *= e["multiplier"]

            # Team Speed Modifier durch Eigenschaften
            boost *= self.get_team_speed_modifier(proj)

            if ap.get("co_dev"):
                boost *= 1.8

            boost *= self.dev_speed_multiplier
            if hasattr(self, 'union_manager') and self.union_manager.ai_tools_active:
                boost *= 2.0
            if getattr(self, 'office_perks', []):
                boost *= (1.0 + len(self.office_perks) * 0.02)

            # VR-spezifischer Malus für ungeschultes Personal
            if "(VR)" in getattr(proj, "platform", ""):
                active_emps = self._active_employees(proj)
                if active_emps:
                    avg_skill = sum(e.skill_level for e in active_emps) / len(active_emps) if active_emps else 0
                    if avg_skill < 3.5:
                        boost *= 0.4
                    elif avg_skill < 4.5:
                        boost *= 0.7

            boost *= self.global_event_manager.get_development_speed_modifier()

            ap["progress"] += boost

            if ap.get("crunch"):
                has_break = self.has_office_bonus("morale_room")
                break_mod = 0.5 if has_break else 1.0
                active_emps = self._active_employees(proj)
                for emp in active_emps:
                    morale_loss = int(random.randint(2, 5) * break_mod)
                    if getattr(emp, "personality", None) == "workaholic":
                        morale_loss = int(morale_loss * 1.5)
                    if 'Crunch-Survivor' in getattr(emp, 'talents', []):
                        emp.morale = 100
                    else:
                        emp.morale = max(0, emp.morale - morale_loss)
            else:
                active_emps = self._active_employees(proj)
                for emp in active_emps:
                    if getattr(emp, "personality", None) == "workaholic":
                        if 'Crunch-Survivor' in getattr(emp, 'talents', []):
                            emp.morale = 100
                        else:
                            emp.morale = max(0, emp.morale - 1)

                base_bugs = random.randint(1, 3)
                ap["bugs"] += int(base_bugs * self.get_team_bug_modifier(proj))

            if random.random() < 0.1:
                ap["bugs"] += int(1 * self.get_team_bug_modifier(proj))

            active_supps = [e for e in self._active_employees(proj) if e.role == "Supporter"]
            if active_supps and ap["bugs"] > 0:
                ap["bugs"] = max(0, ap["bugs"] - len(active_supps))

            # Fertigstellung-Check
            if ap["progress"] >= ap["total_weeks"]:
                ap["ready_to_finish"] = True
                if proj.__class__.__name__ == "EngineProject":
                    self.finalize_engine(ap)
                    continue
                elif proj.__class__.__name__ in ["UpdateProject", "DLCProject"]:
                    self._finish_update_project(proj)
                    if ap in self.active_projects:
                        self.active_projects.remove(ap)
                    continue

            # AAA Events (Max 1x pro Projekt)
            if getattr(proj, "size", None) == "AAA" and not ap.get("aaa_event_done"):
                prog_pct = ap["progress"] / ap["total_weeks"]
                if 0.2 < prog_pct < 0.8 and random.random() < 0.05:
                    self.pending_dev_event = {
                        "data": random.choice(AAA_DEV_EVENTS),
                        "ap": ap
                    }
                    ap["aaa_event_done"] = True
                    self.time_speed = 0

            # Allgemeine Events
            max_ev = {"Klein": 1, "Mittel": 1, "Groß": 2, "AAA": 0}.get(getattr(proj, "size", None), 1)
            if ap.get("event_count", 0) < max_ev:
                prog_pct = ap["progress"] / ap["total_weeks"]
                if 0.15 < prog_pct < 0.85:
                    chance = {"Klein": 0.04, "Mittel": 0.05, "Groß": 0.06}.get(getattr(proj, "size", None), 0.05)
                    if random.random() < chance:
                        self.pending_dev_event = {
                            "data": random.choice(GENERAL_DEV_EVENTS),
                            "ap": ap
                        }
                        ap["event_count"] = ap.get("event_count", 0) + 1
                        self.time_speed = 0

        # Forschungsfortschritt
        if self.is_researching:
            if getattr(self, 'strike_weeks_left', 0) == 0:
                self.research_progress += 1
            if self.research_progress >= self.research_total_weeks:
                self.complete_research()

        # Konsolenentwicklung
        if getattr(self, "is_developing_console", False):
            if getattr(self, 'strike_weeks_left', 0) == 0:
                self.console_progress += 1
            if self.console_progress >= getattr(self, 'console_total_weeks', 100):
                self.is_developing_console = False
                c = self.current_console_draft
                if isinstance(c, dict):
                    new_console = CustomConsole(
                        name=c['name'],
                        architecture=c.get('architecture', 'RISC'),
                        performance=c.get('performance', 1),
                        marketing_budget=c.get('marketing_budget', 0),
                        dev_cost=c['cost'],
                        release_week=self.week
                    )
                else:
                    new_console = CustomConsole(
                        name=c.name,
                        architecture=c.architecture,
                        performance=c.performance,
                        marketing_budget=c.marketing_budget,
                        dev_cost=c.dev_cost,
                        release_week=self.week
                    )
                if not hasattr(self, "custom_consoles"):
                    self.custom_consoles = []
                self.custom_consoles.append(new_console)
                self.emails.insert(0, Email(
                    sender=self.get_text('sender_hardware'),
                    subject=self.get_text('subject_console_done'),
                    body=self.get_text('body_console_done', name=c['name'] if isinstance(c, dict) else c.name),
                    date_week=self.week
                ))
                self.current_console_draft = None

        # Expo Trigger (Mitte des Jahres)
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        if week_in_year == (WEEKS_PER_YEAR // 2):
            self.emails.append(Email(
                sender=self.get_text('sender_assistant'),
                subject=self.get_text('subject_expo', default="Spiele-Messe: Ausstellung!"),
                body=self.get_text('body_expo', default="Die jährliche Spiele-Messe steht vor der Tür. Wir können dort ausstellen!"),
                date_week=self.week,
                is_bug=False
            ))
            self.emails[-1].is_expo_invite = True

        # Saisonale Modifikatoren
        season_mod = 1.0
        winter_start = WEEKS_PER_YEAR - 3
        if winter_start <= week_in_year <= WEEKS_PER_YEAR:
            season_mod = 1.5
        summer_start = int(WEEKS_PER_YEAR * 0.6)
        summer_end = int(WEEKS_PER_YEAR * 0.75)
        if summer_start <= week_in_year <= summer_end:
            season_mod = 0.8

        # Achievements prüfen
        if hasattr(self, "_check_achievements"):
            self._check_achievements()

        # Verkäufe für aktive Spiele
        for g in self.game_history:
            if g.is_active:
                g.weeks_on_market += 1
                decay_factor = 0.1 if getattr(g, "has_mod_support", False) else 0.2

                new_sales = int((self.calculate_sales(g) * season_mod) / (1 + g.weeks_on_market * decay_factor))
                if getattr(g, "bugs", 0) > 0:
                    new_sales = int(new_sales * 0.5)
                    fan_loss = int(g.bugs * 2.0)
                    fan_loss = max(0, fan_loss - (getattr(self, "support_level", 0) * 5))
                    self.fans = max(0, self.fans - fan_loss)

                for e in self.active_events:
                    if e["effect"] == "sales_drop":
                        new_sales = int(new_sales * e["multiplier"])
                    elif e["effect"] == "sales_boost":
                        new_sales = int(new_sales * e["multiplier"])

                if getattr(g, "is_f2p", False):
                    g.active_players = int(getattr(g, "active_players", 0) * 0.95) + new_sales
                    current_active = g.active_players
                else:
                    current_active = new_sales * 5

                if getattr(g, "has_ads", False):
                    ad_rev = int(current_active * 0.5)
                    if ad_rev > 0:
                        self.track_income("other", ad_rev)
                        g.revenue += ad_rev
                        self.hype = max(0.0, self.hype - 0.5)

                if getattr(g, "has_mtx", False):
                    mtx_rev = int(current_active * 1.5)
                    if mtx_rev > 0:
                        self.track_income("other", mtx_rev)
                        g.revenue += mtx_rev
                        self.fans = max(0, self.fans - 20)

                if getattr(g, "is_f2p", False):
                    if not getattr(g, "has_anti_cheat", False):
                        if random.random() < 0.05:
                            lost_players = int(g.active_players * 0.15)
                            g.active_players -= lost_players
                            self.fans = max(0, self.fans - lost_players)
                            self.emails.insert(0, Email(
                                sender=self.get_text('cheater_email_sender', default="Community Manager"),
                                subject=self.get_text('cheater_email_subject', game=g.name, default="Cheater in {game}!"),
                                body=self.get_text('cheater_email_body', game=g.name, lost=lost_players, default="Eine massive Cheater-Welle ruiniert das Spiel! Wir verlieren Spieler!"),
                                date_week=self.week
                            ))

                    f2p_revenue = int(g.active_players * 0.2 * self.profit_multiplier)
                    g.sales += new_sales
                    g.revenue += f2p_revenue
                    self.track_income("sales", f2p_revenue)
                    if g.weeks_on_market > int(WEEKS_PER_YEAR * 0.4) or new_sales < 100:
                        g.is_active = False
                    continue

                price = AUDIENCE_PRICE.get(g.audience, 30)

                physical_sold = 0
                if getattr(g, "physical_copies", 0) > 0:
                    physical_sold = min(new_sales, g.physical_copies)
                    g.physical_copies -= physical_sold
                    self.used_storage -= physical_sold
                    g.lifetime_physical_sales = getattr(g, "lifetime_physical_sales", 0) + physical_sold

                digital_sold = new_sales - physical_sold

                is_ddos = any(e.get("type") == "ddos" for e in getattr(self, "active_cyber_effects", []))
                if is_ddos:
                    digital_sold = 0

                physical_rev = physical_sold * getattr(g, "physical_price", 45)
                digital_rev = digital_sold * price

                g.sales += physical_sold + digital_sold
                total_rev = int((digital_rev + physical_rev) * self.profit_multiplier)
                g.revenue += total_rev

                self.track_income("sales", total_rev)

                for addon in self.active_addons:
                    if addon.base_game_name == g.name:
                        new_sales = int(new_sales * 1.5)

                if g.weeks_on_market > int(WEEKS_PER_YEAR * 0.4) or new_sales < 100:
                    g.is_active = False

        # Einnahmen durch Addons
        for addon in self.active_addons:
            base_game = next((g for g in self.game_history if g.name == addon.base_game_name), None)
            if base_game and base_game.is_active:
                elapsed = max(1, self.week - addon.week_developed)
                sales = int(base_game.sales * 0.05 / (1 + elapsed * 0.1))
                if sales > 0:
                    revenue = int(sales * 15 * self.profit_multiplier)
                    addon.sales += sales
                    addon.revenue += revenue
                    self.track_income("sales", revenue)

        # Einnahmen durch Bundles
        for bundle in self.active_bundles:
            sales = max(10, int(500 * (bundle.average_score / 10) * BUNDLE_DATA["revenue_mod"]))
            revenue = int(sales * bundle.base_price * self.profit_multiplier)
            bundle.sales += sales
            bundle.revenue += revenue
            self.track_income("sales", revenue)

        # Lizenzen verwalten
        licenses_to_remove = []
        for lic in self.active_licenses:
            if hasattr(lic, "duration"):
                lic.duration -= 1
                if lic.duration <= 0 and not getattr(lic, "used", False):
                    licenses_to_remove.append(lic)

        for lic in licenses_to_remove:
            self.active_licenses.remove(lic)
            self.emails.append(Email(
                sender=self.get_text('sender_system'),
                subject=self.get_text('subject_license_expired'),
                body=self.get_text('body_license_expired', name=lic.name),
                date_week=self.week
            ))

        # MMOs & Server Usage verarbeiten
        total_mmo_players = sum(m.players for m in self.active_mmos if m.game.is_active)
        total_subs = getattr(self, "subscription_subscribers", 0)
        ad_games_traffic = sum(g.sales for g in self.game_history if g.is_active and getattr(g, "has_ads", False)) // 10
        server_usage = total_mmo_players + total_subs + ad_games_traffic

        server_capacity = getattr(self, 'server_capacity', 0)
        server_overloaded = server_usage > server_capacity

        if server_overloaded:
            self.hype = max(0.0, self.hype - 2.0)

        for mmo in self.active_mmos:
            if mmo.game.is_active:
                mmo.weeks_active += 1
                is_ddos = any(e.get("type") == "ddos" for e in getattr(self, "active_cyber_effects", []))

                if not is_ddos:
                    rev = int(mmo.weekly_revenue * self.profit_multiplier)
                    self.track_income("mmo", rev)
                    mmo.game.revenue += rev
                else:
                    rev = 0

                self.track_expense("mmo", mmo.weekly_cost)

                if getattr(mmo.game, "has_mtx", False):
                    if not is_ddos:
                        mtx_rev = int(mmo.players * 1.5)
                        self.track_income("other", mtx_rev)
                        mmo.game.revenue += mtx_rev
                    mmo.players = int(mmo.players * 0.95)

                if not getattr(mmo.game, "has_anti_cheat", False):
                    if random.random() < 0.05:
                        lost_players = int(mmo.players * 0.15)
                        mmo.players -= lost_players
                        self.fans = max(0, self.fans - lost_players)
                        self.emails.insert(0, Email(
                            sender=self.get_text('cheater_email_sender', default="Community Manager"),
                            subject=self.get_text('cheater_email_subject', game=mmo.game.name, default="Cheater in {game}!"),
                            body=self.get_text('cheater_email_body', game=mmo.game.name, lost=lost_players, default="Eine massive Cheater-Welle ruiniert das Spiel! Wir verlieren Spieler!"),
                            date_week=self.week
                        ))

                if server_overloaded:
                    mmo.players = int(mmo.players * 0.85)
                else:
                    mmo.players = int(mmo.players * 0.98)

                if mmo.players < 1000:
                    mmo.game.is_active = False

        if server_overloaded and server_usage > 0 and is_new_month:
            self.emails.append(Email(
                sender=self.get_text('sender_system'),
                subject=self.get_text('subject_server_overload'),
                body=self.get_text('body_server_overload'),
                date_week=self.week,
                is_bug=True
            ))

        # Fan-Mails & Bugs
        self.process_emails()

        # Lagerkosten
        if self.used_storage > 0:
            storage_cost = int(self.used_storage * 0.1)
            self.track_expense("other", storage_cost)

        # Merchandising
        for merch in self.active_merch:
            if merch["stock"] > 0:
                sales = int(random.randint(5, 40) * merch["hype_multi"] * (1 + self.hype / 100))
                sales = min(sales, merch["stock"])
                if sales > 0:
                    rev = int(sales * merch["sell_price"] * self.profit_multiplier)
                    self.track_income("merch", rev)
                    merch["stock"] -= sales
                    merch["sales"] += sales
                    merch["revenue"] += rev
                    self.used_storage -= sales
                    if merch["stock"] <= 0:
                        self.emails.append(Email(
                            sender=self.get_text("sender_logistics"),
                            subject=self.get_text("subject_merch_sold_out"),
                            body=self.get_text("body_merch_sold_out", name=merch["name"]),
                            date_week=self.week
                        ))
        self.active_merch = [m for m in self.active_merch if m["stock"] > 0]

        # Publishing Angebote
        if self.office_level >= 2 and random.random() < 0.05:
            self._generate_publishing_offer()

        # Third-Party Spiele
        for published_game in self.published_third_party_games:
            if published_game.is_active:
                published_game.weeks_on_market += 1
                base_sales = published_game.quality * 1000
                sales_this_week = int(base_sales / (1 + published_game.weeks_on_market * 0.1))
                published_game.total_sales += sales_this_week
                gross_revenue = int(sales_this_week * 30 * self.profit_multiplier)
                player_cut = int(gross_revenue * published_game.player_share)
                our_cut = gross_revenue - player_cut
                self.track_income("sales", our_cut)
                published_game.total_revenue += gross_revenue
                published_game.player_profit += player_cut
                if sales_this_week < 50 or published_game.weeks_on_market > int(WEEKS_PER_YEAR * 0.6):
                    published_game.is_active = False

        # Temporäre Modifikatoren abbauen
        if getattr(self, "temp_dev_speed_weeks", 0) > 0:
            self.temp_dev_speed_weeks -= 1
            if self.temp_dev_speed_weeks <= 0:
                self.temp_dev_speed_penalty = 1.0

        if getattr(self, "temp_quality_weeks", 0) > 0:
            self.temp_quality_weeks -= 1
            if self.temp_quality_weeks <= 0:
                self.temp_quality_boost = 0.0

        # Jingles aktualisieren
        active_jingles = []
        for jingle in getattr(self, "active_jingles", []):
            if hasattr(jingle, "weeks_left"):
                jingle.weeks_left -= 1
                if jingle.weeks_left > 0:
                    active_jingles.append(jingle)
            else:
                jingle.weeks_left = 3
                active_jingles.append(jingle)
        self.active_jingles = active_jingles

        # Soundkarten & Konsolen Updates
        self.update_hardware_development()

        if getattr(self, "active_custom_console", None):
            cc = self.active_custom_console
            if not getattr(cc, "is_released", False):
                progress_gain = 0
                for emp in self.employees:
                    if not emp.is_training and not emp.is_sick and emp.morale > 0:
                        progress_gain += emp.skills.get("Programmierung", 50) / 100.0

                total_weeks = getattr(cc, "total_weeks", 50)
                weekly_progress = (progress_gain / total_weeks) * 0.5
                cc.progress += weekly_progress
                if cc.progress >= 1.0:
                    cc.progress = 1.0
                    cc.is_released = True
                    cc.weeks_on_market = 0
                    if hasattr(self.audio, "play_sound"):
                        self.audio.play_sound("success")
                    if hasattr(self.audio, "speak"):
                        self.audio.speak(self.get_text('console_finished', name=cc.name))

                    PLATFORMS.append({
                        "name": cc.name,
                        "license_fee": 0,
                        "market_multi": 1.0 + (cc.tech_level / 100.0),
                        "unlock_year": self.get_calendar_year(),
                        "end_year": self.get_calendar_year() + 10,
                        "type": "Konsole"
                    })
            else:
                cc.weeks_on_market += 1
                base_sales = int(cc.tech_level * 500 * (1.0 + (self.fans / 10000.0)))
                decay = max(0.1, 1.0 - (cc.weeks_on_market / 100.0))
                weekly_sales = int(base_sales * decay)
                cc.units_sold += weekly_sales

                revenue = weekly_sales * cc.price
                cc.revenue += revenue
                self.money += revenue
                if revenue > 0:
                    self.track_income("hardware", revenue)

                cc.active_users += weekly_sales
                if cc.active_users > 0:
                    cc.active_users = int(cc.active_users * 0.99)

        for card in getattr(self, "sound_card_projects", []):
            if card.is_released:
                card.weeks_on_market += 1
                features_bonus = sum(f["sound_bonus"] for f in HARDWARE_TECH_LIST if f["id"] in card.features)
                base_market_share = 0.05 + features_bonus
                card.market_share = max(0.005, base_market_share / (1.0 + card.weeks_on_market * 0.04))

                royalties = int(card.market_share * random.randint(4000, 12000))
                card.royalties_gained = royalties
                card.lifetime_royalties += royalties
                self.track_income("hardware", royalties)

        # Fanpost, Barrierefreiheit, Büro-Events
        self.receive_fan_mail()
        self.update_accessibility_reputation()
        self.trigger_personality_event()

        # Bilanz finalisieren
        self.finalize_weekly_balance()

        # Rivalen, Turniere, Esports, GOTY
        self._process_rivals()
        self._process_tournaments()
        self._process_esports_leagues()
        self._process_sponsorships()
        if week_in_year == WEEKS_PER_YEAR:
            self._check_goty()

    def get_status_text(self):
        """Gibt einen vollständigen Statustext für den Screenreader aus."""
        lang = self.settings.get("language", "de")
        cal = self.get_calendar_text()

        dev_info = ""
        if self.active_projects:
            names = [ap["project"].name for ap in self.active_projects[:2]]
            if len(self.active_projects) > 2:
                names.append(f"+{len(self.active_projects)-2}")
            dev_info = f" | {self.get_text('developing')}: {', '.join(names)}"
        elif self.is_researching and self.current_research_draft:
            r_name = self.current_research_draft['data']['name']
            progress_pct = int((self.research_progress / max(1, self.research_total_weeks)) * 100)
            dev_info = f" | {self.get_text('researching')}: {r_name} {progress_pct}%"

        emp_count = len(self.employees)
        max_emp = self.get_max_employees()
        unread = sum(1 for e in self.emails if not e.is_read)
        office_name = "Eigenes Studio" if getattr(self, "office_items", []) else "Garage"

        if lang == "de":
            status = (
                f"{self.company_name} | {cal}{dev_info} | "
                f"{self.get_text('money_label')}: {self.money:,.0f} € | "
                f"{self.get_text('fans')}: {self.fans:,} | "
                f"{self.get_text('office')}: {office_name} ({emp_count}/{max_emp} MA) | "
                f"{self.get_text('menu_history_count').replace('{count}.', str(self.games_made))} | "
                f"Hype: {int(self.hype)}"
            )
            if unread > 0:
                status += f" | {unread} ungelesene E-Mails"
        else:
            status = (
                f"{self.company_name} | {cal}{dev_info} | "
                f"{self.get_text('money_label')}: {self.money:,.0f} € | "
                f"{self.get_text('fans')}: {self.fans:,} | "
                f"{self.get_text('office')}: {office_name} ({emp_count}/{max_emp} staff) | "
                f"{self.get_text('menu_history_count').replace('{count}.', str(self.games_made))} | "
                f"Hype: {int(self.hype)}"
            )
            if unread > 0:
                status += f" | {unread} unread emails"
        return status

    def get_status_summary(self):
        """Gibt eine Zusammenfassung der Statuswerte zurück."""
        total_level = sum(emp.level for emp in self.employees)
        cal = self.get_calendar_text()

        summary = self.get_text(
            'status_summary_hotkey',
            date=cal,
            money=self.money,
            rp=self.research_points,
            employees=len(self.employees),
            total_level=total_level,
            fans=self.fans,
            prestige=self.prestige,
            accessibility=getattr(self, "accessibility_reputation", 0),
            accessibility_weekly=self.get_accessibility_weekly_fans()
        )
        return summary
