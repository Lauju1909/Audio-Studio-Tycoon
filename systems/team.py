"""Team-Boni, Training und Teambuilding. Mixin fuer GameState."""
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


class TeamMixin:
    def _active_employees(self, project=None):
        """Liefert nur Mitarbeiter, die nicht krank, nicht in Training und nicht im Urlaub sind. Filtert nach Projekt-Team wenn angegeben."""
        base = [e for e in self.employees if not getattr(e, 'is_sick', False) and not getattr(e, 'is_training', False) and getattr(e, 'vacation_weeks_left', 0) <= 0]
        if project and hasattr(project, 'assigned_employee_ids') and project.assigned_employee_ids:
            # Nur Mitarbeiter, deren Index in der Liste ist
            return [e for i, e in enumerate(self.employees) if i in project.assigned_employee_ids and e in base]
        return base

    def get_team_bonus(self, project=None):
        """Gesamtbonus des Teams auf Spielqualität (nur aktive Mitarbeiter)."""
        active = self._active_employees(project)
        if not active:
            return 0.0
        
        total_bonus = 0.0
        for e in active:
            eb = e.quality_contribution
            # Spezialisierungs-Bonus einrechnen
            if project and e.specialization:
                spec = e.specialization
                btype = spec.get("bonus_type")
                target = spec.get("target")
                val = spec.get("bonus_value", 0)
                
                if btype == "Genre" and (project.genre == target or project.sub_genre == target):
                    eb *= (1.0 + val)
                elif btype == "Topic" and project.topic == target:
                    eb *= (1.0 + val)
            total_bonus += eb
            
        return total_bonus * self.get_team_quality_modifier(project)

    def get_team_slider_bonus(self, slider_name, project=None):
        """Durchschnittlicher Skill-Bonus des Teams für einen Slider (nur aktive Mitarbeiter)."""
        active = self._active_employees(project)
        if not active:
            return 0.0
        
        bonuses = []
        for e in active:
            b = e.get_slider_bonus(slider_name)
            # Spezialisierungen für bestimmte Kategorien (Code, Sound, Design, Story)
            if e.specialization:
                spec = e.specialization
                btype = spec.get("bonus_type")
                val = spec.get("bonus_value", 0)
                
                # Mapping Slider -> Spezialisierung
                mapping = {
                    "Sound": "Sound",
                    "KI": "KI",
                    "Gameplay": "KI", # Code-Maschine hilft auch bei Gameplay
                    "Grafik": "Grafik",
                    "Welt": "Grafik", # Design-Gott hilft auch bei Welt
                    "Story": "Story"
                }
                if mapping.get(slider_name) == btype:
                    b *= (1.0 + val)
            bonuses.append(b)
            
        return sum(bonuses) / len(bonuses) if bonuses else 0

    def get_team_speed_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
        
        # Durchschnittlicher Speed-Skill (50 = 1.0)
        avg_speed = sum(e.speed for e in active) / len(active) if active else 0
        
        # Trait-Modifikatoren (Robust gegen alte Strings oder fehlende Keys)
        trait_mods = []
        for e in active:
            val = 1.0
            if hasattr(e, 'trait') and isinstance(e.trait, dict):
                if e.trait.get("effect") == "speed":
                    val = e.trait.get("value", 1.0)
            trait_mods.append(val)
        trait_avg = sum(trait_mods) / len(trait_mods) if trait_mods else 0
        
        # NEU: Persönlichkeits-Modifikatoren (workaholic: +20% Speed)
        pers_mods = [1.20 if getattr(e, 'personality', None) == 'workaholic' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods) if pers_mods else 0
        
        # NEU: Temporäre Event-Mali
        temp_penalty = getattr(self, "temp_dev_speed_penalty", 1.0)
        
        base_multi = (avg_speed / 50.0) * trait_avg * pers_avg
        return base_multi * self.dev_speed_multiplier * self.logic_multiplier * temp_penalty

    def get_team_bug_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
            
        # Durchschnittlicher Bug-Modifier der Mitarbeiter
        avg_mod = sum(e.bug_modifier for e in active) / len(active) if active else 0
        
        # Trait-Modifikatoren
        trait_mods = []
        for e in active:
            val = 1.0
            if hasattr(e, 'trait') and isinstance(e.trait, dict):
                if e.trait.get("effect") == "bugs":
                    val = e.trait.get("value", 1.0)
            trait_mods.append(val)
        trait_avg = sum(trait_mods) / len(trait_mods) if trait_mods else 0
        
        # NEU: Persönlichkeits-Modifikatoren (chaotic: +15% Bugs)
        pers_mods = [1.15 if getattr(e, 'personality', None) == 'chaotic' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods) if pers_mods else 0
        
        # QA Bonus
        qa_bonus = 0.7 if self.has_office_bonus("qa_tools") else 1.0
        if "Next-Gen Testlabor & QA" in self.unlocked_technologies:
            qa_bonus *= 0.6
        if "Performance-Labor" in self.unlocked_technologies:
            qa_bonus *= 0.8
        
        return avg_mod * trait_avg * qa_bonus * pers_avg

    def get_team_quality_modifier(self, project=None):
        active = self._active_employees(project)
        if not active:
            return 1.0
        mods = [e.trait["value"] if e.trait and e.trait["effect"] == "quality" else 1.0 for e in active]
        
        # NEU: Persönlichkeits-Modifikatoren (perfectionist: +15% Qualität)
        pers_mods = [1.15 if getattr(e, 'personality', None) == 'perfectionist' else 1.0 for e in active]
        pers_avg = sum(pers_mods) / len(pers_mods) if pers_mods else 0
        
        # NEU: Temporärer Event-Bonus
        temp_boost = getattr(self, "temp_quality_boost", 0.0)
        return (sum(mods) / len(mods) if mods else 0.0) * pers_avg * (1.0 + temp_boost)

    def train_employee(self, emp_index, train_data):
        """Verbessert Skills eines Mitarbeiters."""
        if self.money < train_data["cost"]:
            return False
        
        emp = self.employees[emp_index]
        self.track_expense("staff", train_data["cost"])
        
        if train_data.get("is_specialization"):

            from game_data import EMPLOYEE_TRAITS
            # Nur gute Traits raussuchen (z.B. Speed-Booster oder Quality)
            good_traits = [t for t in EMPLOYEE_TRAITS if t["effect"] in ["speed", "quality"] and t["value"] > 1.0]
            if not good_traits:
                good_traits = EMPLOYEE_TRAITS
            emp.trait = random.choice(good_traits)
            emp.trait_learned = True
        else:
            # Skill-Boost auf Primärskill
            sname = emp.primary_skill
            emp.skills[sname] = min(100, emp.skills.get(sname, 0) + train_data["skill_boost"])
            # Kleiner Boost auf Sekundärskill
            s2 = emp.secondary_skill
            emp.skills[s2] = min(100, emp.skills.get(s2, 0) + train_data["skill_boost"] // 2)
        
        # Gehalt steigt leicht
        emp.salary = emp._calculate_salary()
        return True

    def perform_teambuilding(self, action_type="Pizza"):
        """Führt eine Team-Building Maßnahme durch."""
        costs = {"Pizza": 500, "Ausflug": 5000, "Party": 2000}
        morale_boost = {"Pizza": 5, "Ausflug": 25, "Party": 15}
        
        cost = costs.get(action_type, 1000)
        if self.money >= cost:
            self.track_expense("staff", cost)
            boost = morale_boost.get(action_type, 10)
            for emp in self.employees:
                emp.morale = min(100, emp.morale + boost)
            return True
        return False

    def start_training(self, emp_idx, training_option):
        """Startet eine Fortbildung für einen Mitarbeiter (Phase 2)."""
        if not (0 <= emp_idx < len(self.employees)):
            return False, "invalid_employee"
        
        emp = self.employees[emp_idx]
        
        if getattr(emp, 'is_training', False):
            return False, "already_training"
        if getattr(emp, 'is_sick', False):
            return False, "is_sick"
        
        cost = training_option.get("cost", 0)
        if self.money < cost:
            return False, "no_money"
        
        self.track_expense("staff", cost)
        
        lock_weeks = training_option.get("lock_weeks", 1)
        skill_boost = training_option.get("skill_boost", 0)
        is_spec = training_option.get("is_specialization", False)
        
        emp.is_training = True
        emp.training_weeks_left = lock_weeks
        emp.training_skill_boost = skill_boost
        
        # Spezialisierungskurs: Sofort eine zufällige freie Spezialisierung vergeben
        if is_spec:
            from game_data import EMPLOYEE_SPECIALIZATIONS

            current_spec = getattr(emp, 'specialization', None)
            if current_spec:
                spec_name = current_spec.get("name")
            else:
                spec_name = None
            free_specs = [s for s in EMPLOYEE_SPECIALIZATIONS if s["name"] != spec_name]
            if free_specs:
                emp.specialization = random.choice(free_specs)
        
        return True, lock_weeks
