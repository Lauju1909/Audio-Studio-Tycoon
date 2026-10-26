"""Finanzen, Berichte, Abos, Streaming, Cloud, Podcasts. Mixin fuer GameState."""
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


class FinanceMixin:
    def is_bankrupt(self):
        """Prüft ob die Firma pleite ist."""
        return self.money < -50000  # Kreditrahmen von 50k

    def donate(self, amount):
        """Spendet einen Betrag an die Community/Wohltätigkeit."""
        if self.money >= amount:
            self.track_expense("other", amount)
            
            # Fan-Bonus: 1 Fan pro 100 EUR Spende, plus Bonus bei großen Beträgen
            fans_gained = int(amount / 100)
            if amount >= 10000: fans_gained = int(fans_gained * 1.2)
            if amount >= 100000: fans_gained = int(fans_gained * 1.5)
            
            self.fans += fans_gained
            return True, fans_gained
        return False, 0

    def track_income(self, category, amount):
        """Trackt Einnahmen in einer Kategorie."""
        if not hasattr(self, "current_week_balance"):
            self.money += amount
            return
        if category in self.current_week_balance["income"]:
            self.current_week_balance["income"][category] += amount
        else:
            self.current_week_balance["income"]["other"] += amount
        self.money += amount
        if hasattr(self, "accounting"):
            self.accounting["income"] += amount
        
        # NEU: Monatliche Verfolgung
        self.accrued_income[category] = self.accrued_income.get(category, 0) + amount

    def track_expense(self, category, amount):
        """Trackt Ausgaben in einer Kategorie."""
        if category in ["production", "hardware"] and hasattr(self, "global_event_manager"):
            amount = int(amount * self.global_event_manager.get_hardware_cost_modifier())
            
        if not hasattr(self, "current_week_balance"):
            self.money -= amount
            return
        if category in self.current_week_balance["expenses"]:
            self.current_week_balance["expenses"][category] += amount
        else:
            self.current_week_balance["expenses"]["other"] += amount
        self.money -= amount
        if hasattr(self, "accounting"):
            self.accounting["expenses"] += amount

        # NEU: Monatliche Verfolgung
        self.accrued_expenses[category] = self.accrued_expenses.get(category, 0) + amount

    def finalize_weekly_balance(self):
        """Speichert die aktuelle Wochenbilanz in die Historie und setzt sie zurück."""
        if not hasattr(self, "current_week_balance"): return
        
        total_income = sum(self.current_week_balance["income"].values())
        total_expenses = sum(self.current_week_balance["expenses"].values())
        
        balance_entry = {
            "week": self.week,
            "income": self.current_week_balance["income"].copy(),
            "expenses": self.current_week_balance["expenses"].copy(),
            "total_income": total_income,
            "total_expenses": total_expenses,
            "profit": total_income - total_expenses
        }
        if not hasattr(self, "financial_history"): self.financial_history = []
        self.financial_history.append(balance_entry)
        
        if len(self.financial_history) > 200:
            self.financial_history.pop(0)
            
        # Reset für neue Woche
        self.current_week_balance = {
            "income": {k: 0 for k in self.current_week_balance["income"]},
            "expenses": {k: 0 for k in self.current_week_balance["expenses"]}
        }

    def _process_engine_licensing(self):
        """Berechnet wöchentliche Lizenzeinnahmen aus lizenzierten Engines."""
        for eng in getattr(self, "engines", []):
            if getattr(eng, "is_licensed", False):
                fee = getattr(eng, "license_fee", 0)
                if fee > 0:
                    optimal_fee = max(1, eng.tech_level * 10)
                    demand = max(0, 100 - ((fee / optimal_fee) * 50))
                    income = int(demand * fee)
                    if income > 0:
                        self.track_income("engine_license", income)

    def _process_cloud_gaming(self):
        cg = getattr(self, "cloud_gaming", None)
        if cg and cg.active:
            target_subs = max(0, int((self.hype * 200 * cg.tech_level) - (cg.price * 500)))
            if cg.subscribers < target_subs:
                cg.subscribers += int((target_subs - cg.subscribers) * 0.1) + 5
            else:
                cg.subscribers -= int((cg.subscribers - target_subs) * 0.2) + 5
            cg.subscribers = max(0, cg.subscribers)
            
            income = int(cg.subscribers * (cg.price / 4.0)) # weekly
            server_cost = int(cg.subscribers * (cg.server_cost_per_sub / 4.0))
            server_cost = int(server_cost * self.global_event_manager.get_server_cost_modifier())
            
            self.track_income("other", income)
            self.track_expense("server_costs", server_cost)

    def _process_audio_pass(self):
        ap = getattr(self, "audio_pass", None)
        if ap and ap.active:
            # We assume it has a tick_month, but let's just do a weekly approximation here
            # Since AudioPass tick_month is defined in models, we can call it once a month, 
            # but let's call it weekly with / 4
            income = int(ap.tick_month() / 4.0) if hasattr(ap, 'tick_month') else 0
            self.track_income("other", income)

    def _process_podcast_network(self):
        """Verarbeitet das Podcast-Netzwerk."""
        if not hasattr(self, "podcast_network") or not self.podcast_network.is_active:
            return
            
        for pod in self.podcast_network.active_podcasts:
            pod.weeks_running += 1
            # Revenue calculation
            base_income = self.podcast_network.subscribers * (pod.quality / 100.0) * 0.05
            # Factor in format
            if pod.format_type == "Täglich":
                base_income *= 2.0
            elif pod.format_type == "Wöchentlich":
                base_income *= 1.0
            elif pod.format_type == "Hörbuch":
                base_income *= 0.5 # lower frequency but higher rep
                
            income = int(base_income)
            pod.total_revenue += income
            self.track_income("other", income)
            
            # Reputation shift
            if pod.quality >= 70:
                self.podcast_network.reputation = min(100, self.podcast_network.reputation + 1)
                if random.random() < 0.1:
                    self.podcast_network.subscribers += int(self.podcast_network.reputation * 10)
            elif pod.quality <= 40:
                self.podcast_network.reputation = max(0, self.podcast_network.reputation - 2)
                self.podcast_network.subscribers = max(0, self.podcast_network.subscribers - int(self.podcast_network.subscribers * 0.05))

    def update_subscription_service(self):
        """Aktualisiert den Abo-Dienst (Abonnenten-Wachstum, Einnahmen, Kosten)."""
        if not getattr(self, "subscription_active", False):
            if hasattr(self, "subscription_subscribers"):
                self.subscription_subscribers = 0
            return

        # 1. Wachstum berechnen
        # Basis-Interesse (Hype hilft extrem)
        growth_base = (self.hype * 50) + 100
        
        # Preis-Effekt: 9.99 ist Standard. 
        price_factor = 1.0
        if self.subscription_price > 15.0:
            price_factor = 0.5
        if self.subscription_price > 20.0:
            price_factor = -0.05 # Leichter Verlust bei Wucherpreisen
        if self.subscription_price < 7.0:
            price_factor = 1.5
            
        # Bibliotheks-Effekt (Anzahl der Spiele im Abo)
        game_count = len(getattr(self, "subscription_games", []))
        library_factor = 0.5 + (game_count * 0.1) # 5 Spiele = 1.0 (normal)
        
        # Zufällige Fluktuation

        drift = random.uniform(0.95, 1.05)
        
        # Abonnenten-Änderung (Wachstum oder Schrumpfen)
        change = int(growth_base * price_factor * library_factor * drift)
        
        # Falls keine Spiele im Abo sind, verliert man massiv Leute
        if game_count == 0:
            change = -int(self.subscription_subscribers * 0.2) - 50
            
        self.subscription_subscribers = max(0, self.subscription_subscribers + change)
        
        # 2. Finanzen
        # Einnahmen (wöchentlich ca. 1/4 des Monatspreises)
        income = int(self.subscription_subscribers * (self.subscription_price / 4))
        if income > 0:
            self.track_income("subscription", income)
            
        # Serverkosten (0.05€ pro Abonnent pro Woche + Grundgebühr pro Spiel)
        server_costs = int(self.subscription_subscribers * 0.05) + (game_count * 200)
        server_costs = int(server_costs * self.global_event_manager.get_server_cost_modifier())
        if server_costs > 0:
            self.track_expense("server_costs", server_costs)

    def get_financial_report(self):
        """Gibt einen Bericht über die Finanzen der letzten Woche aus."""
        if not self.financial_history:
            return self.get_text('no_finances_yet')
            
        last = self.financial_history[-1]
        
        # Einnahmen Details
        inc_parts = []
        for cat, val in last["income"].items():
            if val > 0:
                inc_parts.append(f"{self.get_text('finance_' + cat)}: {val:,.0f} €")
        
        # Ausgaben Details
        exp_parts = []
        for cat, val in last["expenses"].items():
            if val > 0:
                exp_parts.append(f"{self.get_text('finance_' + cat)}: {val:,.0f} €")
                
        report = [
            f"--- {self.get_text('finance_report_title')} ({self.get_text('calendar_week')} {last['week']}) ---",
            f"{self.get_text('finance_total_income')}: {last['total_income']:,.0f} €",
            ". ".join(inc_parts) if inc_parts else self.get_text('none'),
            f"{self.get_text('finance_total_expenses')}: {last['total_expenses']:,.0f} €",
            ". ".join(exp_parts) if exp_parts else self.get_text('none'),
            f"{self.get_text('finance_net_profit')}: {last['profit']:,.0f} €",
            f"--- {self.get_text('current_balance')}: {self.money:,.0f} € ---"
        ]
        return "\n".join(report)

    def get_yearly_report(self):
        """Generiert eine Zusammenfassung des vergangenen Spieljahres."""
        from game_data import WEEKS_PER_YEAR, START_YEAR
        if not hasattr(self, "financial_history") or not self.financial_history:
            return self.get_text('no_finances_yet')
            
        if len(self.financial_history) < WEEKS_PER_YEAR:
            history = self.financial_history
        else:
            history = self.financial_history[-WEEKS_PER_YEAR:]
            
        total_inc = sum(w["total_income"] for w in history)
        total_exp = sum(w["total_expenses"] for w in history)
        profit = total_inc - total_exp
        
        # Meistverkauftes Spiel in diesem Jahr
        year_start_week = self.week - WEEKS_PER_YEAR
        year_games = [g for g in self.game_history if g.week_developed >= year_start_week]
        best_game = max(year_games, key=lambda g: g.sales) if year_games else None
        
        report = [
            f"--- {self.get_text('yearly_report_title', year=self.week // WEEKS_PER_YEAR + START_YEAR - 1)} ---",
            f"{self.get_text('finance_total_income')}: {total_inc:,.0f} €",
            f"{self.get_text('finance_total_expenses')}: {total_exp:,.0f} €",
            f"{self.get_text('finance_net_profit')}: {profit:,.0f} €",
        ]
        
        if best_game:
            report.append(f"{self.get_text('yearly_best_game')}: {best_game.name} ({best_game.sales:,} {self.get_text('sales')})")
        
        return "\n".join(report)

    def _send_monthly_bank_statement(self):
        """Generiert und speichert einen monatlichen Kontoauszug."""
        import game_data
        year = (self.week - 1) // game_data.WEEKS_PER_YEAR + game_data.START_YEAR
        # Dynamische Monatsberechnung (1 bis 12)
        int(((self.week - 1) % game_data.WEEKS_PER_YEAR) * 12 / game_data.WEEKS_PER_YEAR) + 1
        
        # NEU: Steuern berechnen (vom monatlichen Gewinn)
        taxes = 0
        total_income = sum(self.accrued_income.values())
        total_expense = sum(self.accrued_expenses.values())
        profit = total_income - total_expense
        if profit > 0:
            taxes = max(0, int(profit * max(0.0, self.tax_rate)))
            self.track_expense("taxes", taxes)
            
        statement = BankStatement(
            week=self.week,
            year=year,
            income_items=self.accrued_income.copy(),
            expense_items=self.accrued_expenses.copy(),
            final_balance=self.money
        )
        
        self.bank_statements.insert(0, statement)
        
        # Reset accrued data for next month
        self.accrued_income = {}
        self.accrued_expenses = {}
        
        # Email senden
        cal = self.get_calendar_text()
        body_lines = [
            f"{self.get_text('monthly_statement_period')}: {cal}",
            "",
            f"{self.get_text('finance_total_income')}: {statement.total_income:,.0f} EUR",
        ]
        for cat, val in statement.income_items.items():
            if val > 0:
                body_lines.append(f"  + {self.get_text('finance_' + cat)}: {val:,.0f} EUR")
        
        body_lines.append("")
        body_lines.append(f"{self.get_text('finance_total_expenses')}: {statement.total_expense:,.0f} EUR")
        for cat, val in statement.expense_items.items():
            if val > 0:
                body_lines.append(f"  - {self.get_text('finance_' + cat)}: {val:,.0f} EUR")
                
        profit = statement.total_income - statement.total_expense
        sign = "+" if profit >= 0 else ""
        body_lines.extend([
            "",
            f"{self.get_text('finance_net_profit')}: {sign}{profit:,.0f} EUR",
            f"{self.get_text('current_balance')}: {self.money:,.0f} EUR",
        ])
        
        self.emails.insert(0, Email(
            sender=self.get_text("sender_bank"),
            subject=self.get_text("subject_monthly_statement", date=cal),
            body="\n".join(body_lines),
            date_week=self.week
        ))

    def delete_bank_statement(self, idx):
        """Löscht einen Kontoauszug aus der Liste."""
        if 0 <= idx < len(self.bank_statements):
            self.bank_statements.pop(idx)
            return True
        return False

    def get_financial_summary(self):
        """Gibt eine kurze akustische Zusammenfassung der Finanzen zurück."""
        # Suche nach financial_history falls vorhanden
        profit = 0
        if hasattr(self, "financial_history") and self.financial_history:
            # Profit der letzten 4 Wochen
            last_4 = self.financial_history[-4:]
            inc = sum(w["total_income"] for w in last_4)
            exp = sum(w["total_expenses"] for w in last_4)
            profit = inc - exp
        
        summary = self.get_text('finance_summary_hotkey', 
                                money=self.money, 
                                profit=profit, 
                                fans=self.fans)
        return summary

    def found_streaming_platform(self) -> bool:
        if self.get_calendar_year() < 2011:
            return False
        cost = 10000000
        if self.money < cost:
            return False
        self.streaming_platform = StreamingPlatform(self.week)
        self.track_expense("other", cost)
        return True

    def upgrade_streaming_server(self) -> bool:
        if not self.streaming_platform:
            return False
        cost = self.streaming_platform.server_level * 5000000
        if self.money < cost:
            return False
        self.track_expense("other", cost)
        self.streaming_platform.server_level += 1
        return True

    def _process_streaming_platform_monthly(self):
        if not self.streaming_platform:
            return
        
        # Costs
        maintenance = self.streaming_platform.get_maintenance_cost()
        self.track_expense("other", maintenance)
        
        # Revenue
        rev = self.streaming_platform.get_monthly_revenue()
        if rev > 0:
            self.track_income("other", rev)
            
        # Growth
        growth_rate = 1.05
        if self.streaming_platform.exclusive_esports:
            growth_rate += 0.05
            
        new_subs = int(self.streaming_platform.subscribers * growth_rate) + 1000
        # Cap by server level
        cap = self.streaming_platform.get_max_capacity()
        if new_subs > cap:
            new_subs = cap
        self.streaming_platform.subscribers = new_subs
        
        # Hardware boost
        if self.streaming_platform.subscribers > 100000:
            for console in getattr(self, "custom_consoles", []):
                if console.market_phase != "discontinued":
                    boost = int(self.streaming_platform.subscribers * 0.01)
                    console.units_sold += boost
                    console.revenue += boost * console.price
                    self.track_income("console_sales", boost * console.price)
                    
        # Send report
        subject = self.get_text("streaming_monthly_report_subject")
        body = self.get_text("streaming_monthly_report_body", subs=self.streaming_platform.subscribers, rev=rev, cost=maintenance)
        self.emails.append(Email("Streaming Team", subject, body, self.week))

    def watch_ad(self):
        self.track_income("other", 5000)
        return True, 5000
