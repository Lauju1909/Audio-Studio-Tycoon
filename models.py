"""
Datenmodelle für Audio Studio Tycoon - Audio Edition.

Enthält: ReviewScore, GameProject, Employee, Engine, EngineFeature
"""

import random
from game_data import EMPLOYEE_FIRST_NAMES, EMPLOYEE_LAST_NAMES, EMPLOYEE_TRAITS
from translations import get_text


class ReviewScore:
    """Bewertung eines Spiels durch 4 Reviewer."""

    def __init__(self, scores, comments=None):
        self.scores = scores  # [int, int, int, int]
        self.comments = comments or []

    @property
    def average(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0.0

    @property
    def total(self):
        return sum(self.scores)

    def __str__(self):
        parts = [get_text('reviewer_score', i=i+1, score=s) for i, s in enumerate(self.scores)]
        return ", ".join(parts) + " " + get_text('reviewer_average', avg=self.average)


class GameProject:
    """Ein entwickeltes Spiel."""

    def __init__(self, name, topic, genre, sliders=None, platform=None, audience=None, engine=None, size="Mittel", marketing="Kein Marketing"):
        self.name = name
        self.topic = topic
        self.genre = genre
        self.sliders = sliders or {}
        self.platform = platform or "PC"
        self.audience = audience or "Jugendliche"
        self.size = size
        self.marketing = marketing
        self.engine = engine            # Engine-Objekt oder None
        self.review = None              # ReviewScore
        self.sales = 0
        self.revenue = 0
        self.dev_cost = 0
        self.week_developed = 0
        
        # NEU: Sprachen
        self.languages = ["de"] # Startet immer mit Deutsch
        
        # NEU: Advanced Features
        self.has_ads = False
        self.has_mod_support = False
        self.is_f2p = False
        self.is_remake = False
        self.is_port = False
        self.has_mtx = False
        self.has_movie_deal = False
        self.has_anti_cheat = False
        self.used_ai_assets = False
        self.drm_level = 0
        self.pirated_copies = 0
        self.active_players = 0
        
        # NEU: Service & Support
        self.bugs = 0
        self.dlc_count = 0
        self.weeks_on_market = 0
        self.is_active = True

        # NEU: Sequels & IP-Rating
        self.ip_rating = 0
        self.sequel_number = 0  # 0 = Original, 2 = Sequel, 3 = Teil 3 etc.
        self.sub_genre = None
        self.license_bonus = 0.0  # NEU: Phase B Lizenzen
        self.assigned_employee_ids = []  # NEU: Team-Zuweisung
        self.updates = []               # NEU: Liste von UpdateProject/DLCProject
        self.total_bugs_fixed = 0

        # NEU: Phase C - Produktion & Retail
        self.physical_copies = 0
        self.physical_price = 45  # Retailpreis
        self.lifetime_physical_sales = 0



    @property
    def profit(self):
        return self.revenue - self.dev_cost

    def summary(self):
        """Zusammenfassung für NVDA."""
        parts = [
            get_text('game_summary_base', name=self.name, topic=get_text(self.topic), genre=get_text(self.genre), platform=get_text(self.platform)),
        ]
        if self.review:
            parts.append(get_text('game_summary_review', score=self.review.average))
            parts.append(get_text('game_summary_sales', sales=self.sales))
            parts.append(get_text('game_summary_revenue', revenue=self.revenue))
        return ". ".join(parts)

    def to_dict(self):
        """Für Speichern."""
        return {
            "name": self.name,
            "topic": self.topic,
            "genre": self.genre,
            "sliders": self.sliders,
            "platform": self.platform,
            "audience": self.audience,
            "size": self.size,
            "marketing": self.marketing,
            "engine_name": self.engine.name if self.engine else None,
            "review_scores": self.review.scores if self.review else None,
            "review_average": self.review.average if self.review and hasattr(self.review, 'average') else 0.0,
            "sales": self.sales,
            "revenue": self.revenue,
            "dev_cost": self.dev_cost,
            "week_developed": self.week_developed,
            "bugs": self.bugs,
            "dlc_count": self.dlc_count,
            "weeks_on_market": self.weeks_on_market,
            "is_active": self.is_active,
            "ip_rating": self.ip_rating,
            "sequel_number": self.sequel_number,
            "sub_genre": self.sub_genre,
            "license_bonus": self.license_bonus,
            "physical_copies": getattr(self, "physical_copies", 0),
            "physical_price": getattr(self, "physical_price", 45),
            "lifetime_physical_sales": getattr(self, "lifetime_physical_sales", 0),
            "assigned_employee_ids": getattr(self, "assigned_employee_ids", []),
            "languages": getattr(self, "languages", ["de"]),
            "has_ads": getattr(self, "has_ads", False),
            "has_mod_support": getattr(self, "has_mod_support", False),
            "is_f2p": getattr(self, "is_f2p", False),
            "is_remake": getattr(self, "is_remake", False),
            "is_port": getattr(self, "is_port", False),
            "has_mtx": getattr(self, "has_mtx", False),
            "has_movie_deal": getattr(self, "has_movie_deal", False),
            "has_anti_cheat": getattr(self, "has_anti_cheat", False),
            "used_ai_assets": getattr(self, "used_ai_assets", False),
            "drm_level": getattr(self, "drm_level", 0),
            "pirated_copies": getattr(self, "pirated_copies", 0),
            "active_players": getattr(self, "active_players", 0),
            "updates": [u.to_dict() for u in getattr(self, "updates", [])],
            "total_bugs_fixed": getattr(self, "total_bugs_fixed", 0),
        }

    @staticmethod
    def from_dict(gd):
        """Erstellt ein GameProject aus einem Dict."""
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
        proj.bugs = gd.get("bugs", 0)
        proj.dlc_count = gd.get("dlc_count", 0)
        proj.weeks_on_market = gd.get("weeks_on_market", 0)
        proj.is_active = gd.get("is_active", True)
        proj.ip_rating = gd.get("ip_rating", 0)
        proj.sequel_number = gd.get("sequel_number", 0)
        proj.sub_genre = gd.get("sub_genre")
        proj.license_bonus = gd.get("license_bonus", 0.0)
        proj.physical_copies = gd.get("physical_copies", 0)
        proj.physical_price = gd.get("physical_price", 45)
        proj.lifetime_physical_sales = gd.get("lifetime_physical_sales", 0)
        proj.assigned_employee_ids = gd.get("assigned_employee_ids", [])
        proj.languages = gd.get("languages", ["de"])
        proj.has_ads = gd.get("has_ads", False)
        proj.has_mod_support = gd.get("has_mod_support", False)
        proj.is_f2p = gd.get("is_f2p", False)
        proj.is_remake = gd.get("is_remake", False)
        proj.is_port = gd.get("is_port", False)
        proj.has_mtx = gd.get("has_mtx", False)
        proj.has_movie_deal = gd.get("has_movie_deal", False)
        proj.has_anti_cheat = gd.get("has_anti_cheat", False)
        proj.used_ai_assets = gd.get("used_ai_assets", False)
        proj.drm_level = gd.get("drm_level", 0)
        proj.pirated_copies = gd.get("pirated_copies", 0)
        proj.active_players = gd.get("active_players", 0)
        proj.total_bugs_fixed = gd.get("total_bugs_fixed", 0)
        
        # Updates laden
        if "updates" in gd:
            for ud in gd["updates"]:
                u = UpdateProject(ud["base_game_name"], ud["name"], ud["update_type"], ud["dev_cost"], ud["total_weeks"])
                u.progress = ud.get("progress", 0.0)
                u.languages = ud.get("languages", [])
                u.is_finished = ud.get("is_finished", False)
                u.sales = ud.get("sales", 0)
                u.revenue = ud.get("revenue", 0)
                proj.updates.append(u)
        return proj

class UpdateProject:
    """Ein Update oder DLC für ein Spiel."""
    def __init__(self, base_game_name, name, update_type, dev_cost, total_weeks, languages=None):
        self.base_game_name = base_game_name
        self.name = name
        self.update_type = update_type # "Patch", "Content", "DLC", "Language"
        self.dev_cost = dev_cost
        self.total_weeks = total_weeks
        self.progress = 0.0
        self.languages = languages or []
        self.is_finished = False
        self.sales = 0 # Nur für DLC
        self.revenue = 0 # Nur für DLC

    def to_dict(self):
        return {
            "base_game_name": self.base_game_name,
            "name": self.name,
            "update_type": self.update_type,
            "dev_cost": self.dev_cost,
            "total_weeks": self.total_weeks,
            "progress": self.progress,
            "languages": self.languages,
            "is_finished": self.is_finished,
            "sales": self.sales,
            "revenue": self.revenue
        }

class PortProject:
    """Ein Projekt zur Portierung eines Spiels auf eine neue Plattform."""
    def __init__(self, original_game_name, new_platform, dev_cost, total_weeks):
        self.original_game_name = original_game_name
        self.new_platform = new_platform
        self.dev_cost = dev_cost
        self.total_weeks = total_weeks
        self.progress = 0.0
        self.is_finished = False

    def to_dict(self):
        return {
            "original_game_name": self.original_game_name,
            "new_platform": self.new_platform,
            "dev_cost": self.dev_cost,
            "total_weeks": self.total_weeks,
            "progress": self.progress,
            "is_finished": self.is_finished
        }

class AddonProject:
    """Ein Addon für ein existierendes Spiel."""
    def __init__(self, base_game_name, name, topic, genre, dev_cost):
        self.base_game_name = base_game_name
        self.name = name
        self.topic = topic
        self.genre = genre
        self.dev_cost = dev_cost
        self.sales = 0
        self.revenue = 0
        self.week_developed = 0

    def to_dict(self):
        return {
            "base_game_name": self.base_game_name,
            "name": self.name,
            "topic": self.topic,
            "genre": self.genre,
            "dev_cost": self.dev_cost,
            "sales": self.sales,
            "revenue": self.revenue,
            "week_developed": self.week_developed
        }

class BundleProject:
    """Ein Bundle aus mehreren alten Spielen."""
    def __init__(self, name, games, base_price=25):
        self.name = name
        self.games = games # List of GameProject dicts
        self.base_price = base_price
        self.sales = 0
        self.revenue = 0
        
        # Durchschnittsbewertung
        scores = [g['review_average'] for g in self.games if g.get('review_average')]
        self.average_score = sum(scores) / len(scores) if scores else 5.0

    def to_dict(self):
        return {
            "name": self.name,
            "games": self.games,
            "base_price": self.base_price,
            "sales": self.sales,
            "revenue": self.revenue,
            "average_score": self.average_score
        }


class ActiveMMO:
    """Ein aktives Live-Service/MMO Spiel."""
    
    def __init__(self, game_project, initial_players=10000, payment_model="Abo"):
        self.game = game_project
        self.payment_model = payment_model  # "Abo" oder "F2P"
        self.players = initial_players
        
        # Free-to-Play hat massiv mehr Spieler, aber weniger Einnahmen pro Spieler
        if self.payment_model == "F2P":
            self.players = initial_players * 5
            self.subscription_fee = 1  # 1 Euro pro Woche (Mikrotransaktionen)
        elif self.payment_model == "Lootboxen":
            self.players = initial_players * 3
            self.subscription_fee = 5  # Extremer Profit durch Whales
        else:
            self.subscription_fee = 3  # 3 Euro pro Woche (Abo)

        self.server_cost_per_10k = 5000  # 5k Euro pro 10k Spieler
        self.weeks_active = 0
        
    @property
    def weekly_revenue(self):
        return self.players * self.subscription_fee
        
    @property
    def weekly_cost(self):
        return int((max(0, self.players) / 10000) * self.server_cost_per_10k)
        
    @property
    def weekly_profit(self):
        return self.weekly_revenue - self.weekly_cost
        
    def to_dict(self):
        return {
            "game_dict": self.game.to_dict(),
            "players": self.players,
            "subscription_fee": self.subscription_fee,
            "server_cost_per_10k": self.server_cost_per_10k,
            "weeks_active": self.weeks_active,
            "payment_model": self.payment_model,
        }



class Email:
    """Modell für Fan-Post, Bug-Reports und Mitarbeiter-Kommunikation."""
    def __init__(self, sender, subject, body, date_week, game_name=None, is_bug=False):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.date_week = date_week
        self.game_name = game_name
        self.is_bug = is_bug
        self.is_read = False
        
        # Interaktive Mails
        self.is_salary_request = False
        self.employee_idx = None
        self.requested_salary = 0


class BankStatement:
    """Monatlicher Kontoauszug."""
    def __init__(self, week, year, income_items, expense_items, final_balance):
        self.week = week
        self.year = year
        self.income_items = income_items   # Dict {category: amount}
        self.expense_items = expense_items # Dict {category: amount}
        self.final_balance = final_balance

    @property
    def total_income(self):
        return sum(self.income_items.values())

    @property
    def total_expense(self):
        return sum(self.expense_items.values())

    def to_dict(self):
        return {
            "week": self.week,
            "year": self.year,
            "income_items": self.income_items,
            "expense_items": self.expense_items,
            "final_balance": self.final_balance
        }


class EngineProject:
    """Ein Projekt zur Entwicklung einer eigenen In-House Game Engine."""
    def __init__(self, name, features, dev_cost, total_weeks):
        self.name = name
        self.features = features  # Liste von EngineFeature Objekten
        self.dev_cost = dev_cost
        self.total_weeks = total_weeks
        self.progress = 0.0
        self.is_finished = False

    def to_dict(self):
        return {
            "name": self.name,
            "features": [f.name if hasattr(f, 'name') else f for f in self.features],
            "dev_cost": self.dev_cost,
            "total_weeks": self.total_weeks,
            "progress": self.progress,
            "is_finished": self.is_finished,
            "is_engine_project": True
        }

    @classmethod
    def from_dict(cls, data, game_state=None):
        features = data.get("features", [])
        if game_state:
            # Reconstruct actual EngineFeature objects from names
            actual_features = []
            for f_name in features:
                for uf in game_state.unlocked_features:
                    if uf.name == f_name:
                        actual_features.append(uf)
                        break
            features = actual_features
        
        proj = cls(data["name"], features, data["dev_cost"], data["total_weeks"])
        proj.progress = data.get("progress", 0.0)
        proj.is_finished = data.get("is_finished", False)
        return proj


class EngineFeature:
    """Ein Feature, das in einer Engine verbaut werden kann."""

    def __init__(self, category, name, tech_bonus):
        self.category = category  # "Grafik", "Sound", "KI", "Gameplay", "Level"
        self.name = name
        self.tech_bonus = tech_bonus

    def __str__(self):
        return f"{self.name} ({self.category}, Tech: +{self.tech_bonus})"


class Engine:
    """Eine Game-Engine."""

    def __init__(self, name, features=None, is_third_party=False, usage_cost=0, revenue_share=0.0):
        self.name = name
        self.features = features or []  # Liste von EngineFeature
        self.is_licensed = False
        self.license_fee = 0
        self.is_third_party = is_third_party
        self.usage_cost = usage_cost
        self.revenue_share = revenue_share

    @property
    def tech_level(self):
        return sum(f.tech_bonus for f in self.features)

    @property
    def quality_bonus(self):
        """Bonus auf die Spielqualität. Eigene/Komplexe Engines skalieren höher."""
        return min(0.6, self.tech_level * 0.03)

    def has_feature_category(self, category):
        """Hat die Engine ein Feature dieser Kategorie?"""
        return any(f.category == category for f in self.features)

    def summary(self):
        """Zusammenfassung für NVDA."""
        feat_names = ", ".join(get_text(f.name) for f in self.features) if self.features else get_text('none')
        lic_str = " (Lizenziert)" if self.is_licensed else ""
        return get_text('engine_summary', name=self.name, tech_level=self.tech_level, features=feat_names) + lic_str

    def __str__(self):
        return f"{self.name} (Tech: {self.tech_level})"


class Employee:
    """Ein Mitarbeiter des Studios."""

    def __init__(self, name=None, role_data=None, skill_level=1, specialization=None, trait=None, personality=None):
        """
        role_data: Dict aus EMPLOYEE_ROLES (role, primary, secondary)
        skill_level: 1-5, beeinflusst Skills und Gehalt
        """
        if name is None:
            first = random.choice(EMPLOYEE_FIRST_NAMES)
            last = random.choice(EMPLOYEE_LAST_NAMES)
            name = f"{first} {last}"

        self.name = name
        self.role = role_data["role"] if role_data else "Allrounder"
        self.primary_skill = role_data["primary"] if role_data else "Gameplay"
        self.secondary_skill = role_data["secondary"] if role_data else "Grafik"
        self.skill_level = skill_level
        self.specialization = specialization  # Dict aus EMPLOYEE_SPECIALIZATIONS oder None
        self.trait = trait if trait else random.choice(EMPLOYEE_TRAITS)
        
        # NEU: Mitarbeiter-Persönlichkeiten
        self.personality = personality or random.choice(["perfectionist", "chaotic", "showman", "workaholic", "easygoing"])

        # Skills basierend auf Rolle und Level generieren
        self.skills = self._generate_skills()

        # Gehalt basierend auf Skills
        self.salary = self._calculate_salary()
        self.morale = 100          # 0-100
        self.weeks_employed = 0
        self.last_raise_week = 0   # Wann gab es das letzte Mal eine Gehaltserhöhung?
        self.pending_raise_request = False # Laufende Gehaltsverhandlung
        self.is_ceo = False        # Chef-Flag

        # NEU: Phase 2 - Fortbildungen & Krankheit
        self.is_training = False        # Gesperrt durch Fortbildung
        self.training_weeks_left = 0    # Wochen bis Fortbildung fertig
        self.training_skill_boost = 0   # Skill-Punkte die nach Abschluss vergeben werden
        self.is_sick = False
        self.is_crunching = False
        self.fatigue = 0           # 0-100, steigt bei Arbeit
        self.vacation_weeks_left = 0 # Wenn > 0, ist der Mitarbeiter im Urlaub
        self.crunch_weeks = 0            # Krank-Status
        self.sick_weeks_left = 0        # Wochen bis Genesung

    def _generate_skills(self):
        """Generiert Skill-Werte basierend auf Rolle und Level."""
        from game_data import SLIDER_NAMES
        skills = {}
        base = self.skill_level * 10 + random.randint(5, 15)

        for slider in SLIDER_NAMES:
            if slider == self.primary_skill:
                skills[slider] = min(100, base + random.randint(10, 25))
            elif slider == self.secondary_skill:
                skills[slider] = min(100, base + random.randint(0, 10))
            else:
                skills[slider] = max(5, base - random.randint(5, 20))
        return skills

    def _calculate_salary(self):
        """Monatliches Gehalt basierend auf Gesamtskills und Eigenschaft."""
        total_skill = sum(self.skills.values())
        base_salary = total_skill * 5 + 500
        if self.trait and self.trait["effect"] == "salary":
            base_salary *= self.trait["value"]
        if getattr(self, "personality", None) == "showman":
            base_salary *= 1.05
        return int(base_salary)

    @property
    def quality_contribution(self):
        """Wie viel Qualität fügt dieser Mitarbeiter hinzu (0.0 - 0.1). Sinkt stark bei schlechter Moral."""
        avg_skill = sum(self.skills.values()) / max(1, len(self.skills))
        base_contrib = avg_skill / 1000.0  # 0.0 - 0.1
        
        if self.morale < 40:
            # Bis zu 50% Einbruch bei Moral 0
            penalty = 1.0 - ((40 - self.morale) / 40.0) * 0.5
            base_contrib *= penalty
        return base_contrib

    @property
    def speed(self):
        """Wöchentlicher Fortschritt-Beitrag (basierend auf Programmierung)."""
        return self.skills.get("Programmierung", 50)

    @property
    def level(self):
        """Alias für skill_level zur Abwärtskompatibilität."""
        return self.skill_level

    @property
    def bug_modifier(self):
        """Einfluss auf die Bug-Rate (basierend auf Design)."""
        # Höheres Design = weniger Bugs
        return max(0.5, 1.5 - (self.skills.get("Design", 50) / 50.0))

    def get_slider_bonus(self, slider_name):
        """Bonus für einen bestimmten Slider (0.0 - 1.0). Sinkt bei schlechter Moral."""
        skill = self.skills.get(slider_name, 0)
        base_bonus = skill / 100.0

        if self.morale < 40:
            penalty = 1.0 - ((40 - self.morale) / 40.0) * 0.5
            base_bonus *= penalty
        return base_bonus

    def summary(self):
        """Zusammenfassung für NVDA."""
        base = get_text('employee_summary', name=self.name, role=get_text(self.role), level=self.skill_level, salary=self.salary, morale=self.morale)
        if self.trait:
            base += ". " + get_text('employee_trait', trait=self.trait['name'])
        if self.specialization:
            base += get_text('employee_spec', spec=get_text(self.specialization['name']))
        return base

    def detail(self):
        """Detaillierte Info für NVDA."""
        from game_data import SLIDER_NAMES
        skill_text = ". ".join(
            f"{get_text(s)}: {self.skills[s]}" for s in SLIDER_NAMES
        )
        base = get_text('employee_detail', name=self.name, role=get_text(self.role), level=self.skill_level, salary=self.salary, skills=skill_text, morale=self.morale)
        if self.trait:
            base += ". " + get_text('employee_trait_desc', trait=self.trait['name'], desc=self.trait['description'])
        return base

    def to_dict(self):
        """Für Speichern."""
        return {
            "name": self.name,
            "role": self.role,
            "primary_skill": self.primary_skill,
            "secondary_skill": self.secondary_skill,
            "skill_level": self.skill_level,
            "specialization": self.specialization,
            "trait": self.trait,
            "skills": self.skills,
            "salary": self.salary,
            "morale": self.morale,
            "weeks_employed": self.weeks_employed,
            "last_raise_week": getattr(self, "last_raise_week", 0),
            "pending_raise_request": getattr(self, "pending_raise_request", False),
            "is_ceo": getattr(self, "is_ceo", False),
            # NEU: Phase 2
            "is_training": getattr(self, "is_training", False),
            "training_weeks_left": getattr(self, "training_weeks_left", 0),
            "training_skill_boost": getattr(self, "training_skill_boost", 0),
            "is_sick": getattr(self, "is_sick", False),
            "is_crunching": getattr(self, "is_crunching", False),
            "crunch_weeks": getattr(self, "crunch_weeks", 0),
            "sick_weeks_left": getattr(self, "sick_weeks_left", 0),
            "personality": getattr(self, "personality", "easygoing"),
        }

    @staticmethod
    def from_dict(ed):
        """Erstellt einen Mitarbeiter aus einem Dict (für Laden)."""
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
        emp.trait = ed.get("trait")
        
        # Sicherstellen dass alle Flags da sind (Migration/Robustheit)
        emp.last_raise_week = ed.get("last_raise_week", 0)
        emp.pending_raise_request = ed.get("pending_raise_request", False)
        emp.is_ceo = ed.get("is_ceo", False)
        emp.is_training = ed.get("is_training", False)
        emp.training_weeks_left = ed.get("training_weeks_left", 0)
        emp.training_skill_boost = ed.get("training_skill_boost", 0)
        emp.is_sick = ed.get("is_sick", False)
        emp.is_crunching = ed.get("is_crunching", False)
        emp.crunch_weeks = ed.get("crunch_weeks", 0)
        emp.sick_weeks_left = ed.get("sick_weeks_left", 0)
        emp.personality = ed.get("personality", "easygoing")
        return emp

class RivalGame:
    """Spiel, das von der KI-Konkurrenz veröffentlicht wird."""
    
    def __init__(self, name, topic, genre, score, week_developed=0, weeks_on_market=0):
        self.name = name
        self.topic = topic
        self.genre = genre
        self.score = score
        self.week_developed = week_developed
        self.weeks_on_market = weeks_on_market
        self.is_active = True

    def to_dict(self):
        return {
            "name": self.name,
            "topic": self.topic,
            "genre": self.genre,
            "score": self.score,
            "week_developed": self.week_developed,
            "weeks_on_market": self.weeks_on_market,
            "is_active": self.is_active
        }

class RivalStudio:
    """KI-gesteuertes Konkurrenz-Studio."""
    
    def __init__(self, name, target_market_share=10, games=None, next_release_week=None, owned_shares=0, is_owned_by_player=False, ai_personality="Balanced", ai_memory=None):
        self.name = name
        self.target_market_share = target_market_share
        self.games = games or []
        self.next_release_week = next_release_week or random.randint(10, 30)
        self.owned_shares = owned_shares
        self.is_owned_by_player = is_owned_by_player  # NEU: Phase F (Firmenübernahmen)
        self.ai_personality = ai_personality
        self.ai_memory = ai_memory or {}

    def to_dict(self):
        return {
            "name": self.name,
            "target_market_share": self.target_market_share,
            "games": [g.to_dict() for g in self.games],
            "next_release_week": self.next_release_week,
            "owned_shares": self.owned_shares,
            "is_owned_by_player": self.is_owned_by_player,
            "ai_personality": self.ai_personality,
            "ai_memory": self.ai_memory
        }

class BankLoan:
    """Aktiver Kredit bei der Bank."""
    def __init__(self, amount_borrowed, interest_rate, duration_weeks, amount_remaining=None, weeks_remaining=None):
        self.amount_borrowed = amount_borrowed
        # Feste Gesamtrückzahlung: z.B. 100k + 20% = 120k
        total_repayment = int(amount_borrowed * (1.0 + interest_rate))
        self.amount_remaining = amount_remaining if amount_remaining is not None else total_repayment
        self.weeks_remaining = weeks_remaining if weeks_remaining is not None else duration_weeks
        # Guard: duration_weeks must be >= 1 to avoid ZeroDivisionError
        safe_weeks = max(1, duration_weeks)
        self.weekly_payment = int(total_repayment / safe_weeks)

    def to_dict(self):
        return {
            "amount_borrowed": self.amount_borrowed,
            "amount_remaining": self.amount_remaining,
            "weekly_payment": self.weekly_payment,
            "weeks_remaining": self.weeks_remaining
        }

class EsportsLeague:
    """Eine E-Sports-Liga fuer ein bestimmtes Multiplayer-Spiel."""

    # Sponsoring-Tier-Daten: (id, weekly_income, hype_decay_protection)
    SPONSOR_TIERS = [
        {"id": "none",       "weekly_base": 0,       "hype_min": 10.0},
        {"id": "local",      "weekly_base": 25000,   "hype_min": 15.0},
        {"id": "regional",   "weekly_base": 100000,  "hype_min": 20.0},
        {"id": "national",   "weekly_base": 400000,  "hype_min": 30.0},
        {"id": "global",     "weekly_base": 1500000, "hype_min": 50.0},
    ]

    # Championship-Typen: (id, cost, hype_bonus, viewer_multiplier, streaming_rev_per_viewer)
    CHAMPIONSHIP_TYPES = [
        {"id": "small",   "cost": 1_000_000,  "hype_bonus": 30,  "viewer_mult": 0.5,  "rev_per_viewer": 3},
        {"id": "medium",  "cost": 5_000_000,  "hype_bonus": 70,  "viewer_mult": 1.0,  "rev_per_viewer": 5},
        {"id": "stadium", "cost": 15_000_000, "hype_bonus": 150, "viewer_mult": 2.5,  "rev_per_viewer": 8},
        {"id": "mega",    "cost": 40_000_000, "hype_bonus": 300, "viewer_mult": 6.0,  "rev_per_viewer": 12},
    ]

    def __init__(self, game_name, start_week):
        self.game_name = game_name
        self.start_week = start_week
        self.hype = 100.0
        self.championships_held = 0
        self.last_championship_year = 0
        # Neu: Erweitertes Tracking
        self.sponsor_tier = "none"          # Aktueller Sponsoring-Tier
        self.total_sponsor_income = 0       # Gesamte Sponsoren-Einnahmen
        self.total_championship_income = 0  # Gesamte Championship-Einnahmen
        self.total_viewers = 0              # Zuschauer aller Championships
        self.last_championship_viewers = 0  # Zuschauer des letzten Events
        self.last_championship_revenue = 0  # Einnahmen des letzten Events
        self.streaming_deals = 0            # Aktive Streaming-Deals
        self.prize_pool_total = 0           # Ausgeschuettete Preisgelder

    def get_sponsor_tier_data(self):
        """Gibt den Daten-Dict fuer den aktuellen Sponsor-Tier zurueck."""
        for t in self.SPONSOR_TIERS:
            if t["id"] == self.sponsor_tier:
                return t
        return self.SPONSOR_TIERS[0]

    def calculate_weekly_sponsor_income(self, fan_count, hype_global):
        """Berechnet den woechtlichen passiven Sponsor-Einnahmen."""
        tier = self.get_sponsor_tier_data()
        base = tier["weekly_base"]
        if base == 0:
            return 0
        fan_factor = min(3.0, 1.0 + fan_count / 1_000_000)
        hype_factor = self.hype / 100.0
        return int(base * fan_factor * hype_factor)

    def to_dict(self):
        return {
            "game_name": self.game_name,
            "start_week": self.start_week,
            "hype": self.hype,
            "championships_held": self.championships_held,
            "last_championship_year": self.last_championship_year,
            "sponsor_tier": self.sponsor_tier,
            "total_sponsor_income": self.total_sponsor_income,
            "total_championship_income": self.total_championship_income,
            "total_viewers": self.total_viewers,
            "last_championship_viewers": self.last_championship_viewers,
            "last_championship_revenue": self.last_championship_revenue,
            "streaming_deals": self.streaming_deals,
            "prize_pool_total": self.prize_pool_total,
        }

    @staticmethod
    def from_dict(data):
        league = EsportsLeague(data["game_name"], data["start_week"])
        league.hype = float(data.get("hype", 100.0))
        league.championships_held = data.get("championships_held", 0)
        league.last_championship_year = data.get("last_championship_year", 0)
        league.sponsor_tier = data.get("sponsor_tier", "none")
        league.total_sponsor_income = data.get("total_sponsor_income", 0)
        league.total_championship_income = data.get("total_championship_income", 0)
        league.total_viewers = data.get("total_viewers", 0)
        league.last_championship_viewers = data.get("last_championship_viewers", 0)
        league.last_championship_revenue = data.get("last_championship_revenue", 0)
        league.streaming_deals = data.get("streaming_deals", 0)
        league.prize_pool_total = data.get("prize_pool_total", 0)
        return league


class CustomConsole:
    """Vom Spieler entwickelte Konsole."""
    def __init__(self, name, architecture, performance, marketing_budget, dev_cost, release_week):
        self.name = name
        self.architecture = architecture
        self.performance = performance  # 1-10
        self.marketing_budget = marketing_budget
        self.dev_cost = dev_cost
        self.release_week = release_week
        self.market_share = min(0.3, 0.05 + (marketing_budget / 50000000.0))
        self.units_sold = 0
        self.hype = min(100, marketing_budget / 500000.0)
        
    @property
    def tech_level(self):
        return self.performance

    def to_dict(self):
        return {
            "name": self.name,
            "architecture": getattr(self, 'architecture', 'Standard'),
            "performance": getattr(self, 'performance', getattr(self, 'tech_level', 1)),
            "marketing_budget": getattr(self, 'marketing_budget', 0),
            "dev_cost": self.dev_cost,
            "release_week": self.release_week,
            "market_share": self.market_share,
            "units_sold": getattr(self, 'units_sold', 0),
            "hype": getattr(self, 'hype', 0)
        }

# ============================================================
# PHASE E: Publisher Role
# ============================================================

class PublishingOffer:
    """Angebot eines NPC-Studios an den Spieler, Publisher zu sein."""
    def __init__(self, studio_name, game_name, genre, quality, marketing_cost, player_share):
        self.studio_name = studio_name
        self.game_name = game_name
        self.genre = genre
        self.quality = quality  # 1 bis 100
        self.marketing_cost = marketing_cost
        self.player_share = player_share  # e.g. 0.30 bis 0.70

    def to_dict(self):
        return {
            "studio_name": self.studio_name,
            "game_name": self.game_name,
            "genre": self.genre,
            "quality": self.quality,
            "marketing_cost": self.marketing_cost,
            "player_share": self.player_share
        }

class PublishedThirdPartyGame:
    """Fremdes Spiel, das vom Spieler vertrieben wird."""
    def __init__(self, offer):
        self.studio_name = offer.studio_name
        self.game_name = offer.game_name
        self.genre = offer.genre
        self.quality = offer.quality
        self.player_share = offer.player_share
        self.weeks_on_market = 0
        self.is_active = True
        self.total_sales = 0
        self.total_revenue = 0
        self.player_profit = 0

    def to_dict(self):
        return {
            "studio_name": self.studio_name,
            "game_name": self.game_name,
            "genre": self.genre,
            "quality": self.quality,
            "player_share": self.player_share,
            "weeks_on_market": self.weeks_on_market,
            "is_active": self.is_active,
            "total_sales": self.total_sales,
            "total_revenue": self.total_revenue,
            "player_profit": self.player_profit
        }

class OfficeObject:
    """Ein Möbelstück oder technisches Gerät im Büro."""
    def __init__(self, object_type, x, y, level=1):
        self.object_type = object_type # "Desk", "PC", "Server", "Cabinet", "Plant"
        self.x = x
        self.y = y
        self.level = level # Tech-Level (1=1930s, 2=1950s etc.)

    def to_dict(self):
        return {
            "object_type": self.object_type,
            "x": self.x,
            "y": self.y,
            "level": self.level
        }

    @staticmethod
    def from_dict(data):
        return OfficeObject(
            data["object_type"], 
            data["x"], 
            data["y"], 
            level=data.get("level", 1)
        )

    def get(self, key, default=None):
        """Ermöglicht den Zugriff wie bei einem Dictionary für Abwärtskompatibilität."""
        if key == "type": return self.object_type
        if hasattr(self, key):
            return getattr(self, key)
        
        # Zugriff auf Spieldaten (BUILD_OBJECTS oder FURNITURE_DATA)
        from game_data import BUILD_OBJECTS, FURNITURE_DATA
        obj_def = BUILD_OBJECTS.get(self.object_type)
        if obj_def and key in obj_def:
            return obj_def.get(key)
        
        # Fallback auf FURNITURE_DATA
        item_data = next((f for f in FURNITURE_DATA if f.get("id") == self.object_type), None)
        if item_data and key in item_data:
            return item_data.get(key)
            
        return default

    def __getitem__(self, key):
        """Erlaubt Zugriff via obj['key'] für Abwärtskompatibilität."""
        return self.get(key)


class ContractWorkProject:
    """Ein angenommener Auftrag von extern."""
    def __init__(self, name, work_type, target_points, payout):
        self.name = name
        self.type = work_type  # e.g., "Code", "Audio", "Grafik", "Design"
        self.target_points = max(1.0, float(target_points))
        self.current_points = 0.0
        self.payout = payout
        self.assigned_employee_ids = []

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "target_points": self.target_points,
            "current_points": self.current_points,
            "payout": self.payout,
            "assigned_employee_ids": self.assigned_employee_ids
        }

    @classmethod
    def from_dict(cls, d):
        cw = cls(d["name"], d["type"], d["target_points"], d["payout"])
        cw.current_points = d.get("current_points", 0.0)
        cw.assigned_employee_ids = d.get("assigned_employee_ids", [])
        return cw

class ManufacturingJob:
    """Ein Auftrag zur Produktion physischer Datenträger."""
    def __init__(self, game_name, amount, cost_per_unit, weeks_to_complete):
        self.game_name = game_name
        self.amount = amount
        self.cost_per_unit = cost_per_unit
        self.weeks_to_complete = weeks_to_complete
        self.weeks_left = weeks_to_complete
        self.is_finished = False

    def to_dict(self):
        return {
            "game_name": self.game_name,
            "amount": self.amount,
            "cost_per_unit": self.cost_per_unit,
            "weeks_to_complete": self.weeks_to_complete,
            "weeks_left": self.weeks_left,
            "is_finished": self.is_finished
        }


# ============================================================
# NEU: SoundCon – Spielemesse
# ============================================================

class SoundConEvent:
    """Repräsentiert eine jährliche SoundCon-Messe-Teilnahme.

    Attribute:
        year (int):           Kalenderjahr der Messe.
        booth_tier (str):     Standgröße: 'klein', 'mittel', 'groß', 'keynote'.
        booth_cost (int):     Kosten für den Messestand.
        hype_gained (float):  Am Ende erzielte Hype-Punkte.
        fans_gained (int):    Am Ende gewonnene Fans.
        qa_rounds (int):      Anzahl absolvierter Q&A-Runden (0-3).
        prestige_gained (int):Prestige-Bonus durch die Teilnahme.
        is_active (bool):     True, solange die Messe läuft.
        result_pending (bool):True, wenn Ergebnisse noch verarbeitet werden.
    """

    # Kosten und Basis-Hype je Standgröße
    BOOTH_TIERS = {
        "klein":   {"cost": 5_000,  "base_hype": 8,  "base_fans": 200,  "prestige": 1},
        "mittel":  {"cost": 20_000, "base_hype": 20, "base_fans": 800,  "prestige": 3},
        "groß":    {"cost": 50_000, "base_hype": 45, "base_fans": 2000, "prestige": 7},
        "keynote": {"cost": 100_000,"base_hype": 90, "base_fans": 5000, "prestige": 15},
    }

    def __init__(self, year: int, booth_tier: str = "klein"):
        self.year = year
        self.booth_tier = booth_tier
        tier_data = self.BOOTH_TIERS.get(booth_tier, self.BOOTH_TIERS["klein"])
        self.booth_cost = tier_data["cost"]
        self.base_hype = tier_data["base_hype"]
        self.base_fans = tier_data["base_fans"]
        self.base_prestige = tier_data["prestige"]
        # Wird nach Abschluss befüllt:
        self.hype_gained = 0.0
        self.fans_gained = 0
        self.prestige_gained = 0
        self.qa_rounds = 0          # Anzahl abgehaltener Q&A-Runden
        self.is_active = True
        self.result_pending = False

    def calculate_results(self, game_state) -> dict:
        """Berechnet den Enderfolg der Messe.

        Faktoren: Firmenprestige, aktueller Hype, abgehaltene Q&A-Runden.
        Gibt ein Ergebnis-Dict zurück.
        """
        prestige_bonus = 1.0 + (game_state.prestige / 200.0)
        qa_bonus       = 1.0 + (self.qa_rounds * 0.15)
        hype_multi     = getattr(game_state, "hype_multiplier", 1.0)

        self.hype_gained    = round(self.base_hype * prestige_bonus * qa_bonus * hype_multi, 1)
        self.fans_gained    = int(self.base_fans  * prestige_bonus * qa_bonus)
        if any(getattr(e, "personality", None) == "showman" for e in game_state.employees):
            self.fans_gained = int(self.fans_gained * 1.15)
        self.prestige_gained = int(self.base_prestige * qa_bonus)
        self.is_active      = False
        self.result_pending = True

        return {
            "hype":     self.hype_gained,
            "fans":     self.fans_gained,
            "prestige": self.prestige_gained,
            "qa":       self.qa_rounds,
            "tier":     self.booth_tier,
        }

    def to_dict(self) -> dict:
        return {
            "year": self.year, "booth_tier": self.booth_tier,
            "booth_cost": self.booth_cost, "hype_gained": self.hype_gained,
            "fans_gained": self.fans_gained, "prestige_gained": self.prestige_gained,
            "qa_rounds": self.qa_rounds, "is_active": self.is_active,
            "result_pending": self.result_pending,
        }

    @staticmethod
    def from_dict(data: dict) -> "SoundConEvent":
        ev = SoundConEvent(data["year"], data.get("booth_tier", "klein"))
        ev.booth_cost       = data.get("booth_cost", ev.booth_cost)
        ev.hype_gained      = data.get("hype_gained", 0.0)
        ev.fans_gained      = data.get("fans_gained", 0)
        ev.prestige_gained  = data.get("prestige_gained", 0)
        ev.qa_rounds        = data.get("qa_rounds", 0)
        ev.is_active        = data.get("is_active", False)
        ev.result_pending   = data.get("result_pending", False)
        return ev


# ============================================================
# NEU: Soundtrack-Label & Radioverträge
# ============================================================

class RadioContract:
    """Ein Radiovertrag für ein Soundtrack-Label.

    Attribute:
        station_name (str):   Name des Radiosenders.
        weekly_royalties (float): Wöchentliche Tantiemen in €.
        weeks_remaining (int): Noch verbleibende Laufzeit in Wochen.
        hype_per_week (float): Wöchentlicher Hype-Bonus durch Airplay.
    """

    def __init__(self, station_name: str, weekly_royalties: float,
                 duration_weeks: int, hype_per_week: float = 0.5):
        self.station_name     = station_name
        self.weekly_royalties = weekly_royalties
        self.weeks_remaining  = duration_weeks
        self.hype_per_week    = hype_per_week

    @property
    def is_active(self) -> bool:
        return self.weeks_remaining > 0

    def tick(self) -> float:
        """Zählt eine Woche herunter. Gibt die Tantiemen zurück (0 wenn abgelaufen)."""
        if self.weeks_remaining <= 0:
            return 0.0
        self.weeks_remaining -= 1
        return self.weekly_royalties

    def to_dict(self) -> dict:
        return {
            "station_name": self.station_name,
            "weekly_royalties": self.weekly_royalties,
            "weeks_remaining": self.weeks_remaining,
            "hype_per_week": self.hype_per_week,
        }

    @staticmethod
    def from_dict(data: dict) -> "RadioContract":
        return RadioContract(
            station_name=data["station_name"],
            weekly_royalties=data["weekly_royalties"],
            duration_weeks=data["weeks_remaining"],
            hype_per_week=data.get("hype_per_week", 0.5),
        )


class SoundtrackLabel:
    """Ein eigenes Musik-Label für Spielesoundtracks.

    Ein Label koppelt die Spielemusik auf ein eigenes Label aus und
    verdient wöchentliche Tantiemen durch Streaming und Radioverträge.
    """

    # Verfügbare Radiosender mit Basisdaten
    RADIO_STATIONS = [
        {"name": "GameFM",        "cost": 10_000, "royalties": 800,  "hype": 1.0,  "weeks": 26},
        {"name": "RetroWave FM",  "cost": 20_000, "royalties": 1500, "hype": 1.5,  "weeks": 52},
        {"name": "SynthAir",      "cost": 35_000, "royalties": 2500, "hype": 2.0,  "weeks": 52},
        {"name": "ChipTune Radio","cost": 15_000, "royalties": 1000, "hype": 1.2,  "weeks": 26},
        {"name": "NationBeat",    "cost": 60_000, "royalties": 4000, "hype": 3.5,  "weeks": 104},
    ]

    def __init__(self, label_name: str):
        self.label_name          = label_name
        self.founding_week       = 0          # Wird bei Gründung gesetzt
        self.catalogued_games    = []         # Liste von GameProject-Namen
        self.radio_contracts     = []         # Liste von RadioContract-Objekten
        self.total_royalties     = 0.0        # Kumulierte Einnahmen
        self.streaming_fans      = 0          # Fans durch Streaming-Plattformen
        self.prestige_bonus      = 0          # Label-Prestige

    @property
    def active_radio_contracts(self) -> list:
        return [c for c in self.radio_contracts if c.is_active]

    def add_game(self, game_name: str):
        """Fügt ein Spiel zum Katalog hinzu (einmalig)."""
        if game_name not in self.catalogued_games:
            self.catalogued_games.append(game_name)

    def tick_week(self) -> float:
        """Verarbeitet eine Woche: Tantiemen einsammeln, abgelaufene Verträge entfernen.

        Gibt die Gesamteinnahmen dieser Woche zurück.
        """
        week_income = 0.0
        expired = []
        for contract in self.radio_contracts:
            income = contract.tick()
            week_income += income
            if not contract.is_active:
                expired.append(contract)
        for c in expired:
            self.radio_contracts.remove(c)

        # Streaming-Einnahmen basierend auf Katalog-Größe
        streaming = len(self.catalogued_games) * 50.0
        week_income += streaming

        self.total_royalties += week_income
        return week_income

    def tick_hype(self) -> float:
        """Gibt den Gesamt-Hype-Bonus dieser Woche durch Radio zurück."""
        return sum(c.hype_per_week for c in self.active_radio_contracts)

    def to_dict(self) -> dict:
        return {
            "label_name": self.label_name,
            "founding_week": self.founding_week,
            "catalogued_games": self.catalogued_games,
            "radio_contracts": [c.to_dict() for c in self.radio_contracts],
            "total_royalties": self.total_royalties,
            "streaming_fans": self.streaming_fans,
            "prestige_bonus": self.prestige_bonus,
        }

    @staticmethod
    def from_dict(data: dict) -> "SoundtrackLabel":
        label = SoundtrackLabel(data["label_name"])
        label.founding_week    = data.get("founding_week", 0)
        label.catalogued_games = data.get("catalogued_games", [])
        label.radio_contracts  = [
            RadioContract.from_dict(c) for c in data.get("radio_contracts", [])
        ]
        label.total_royalties  = data.get("total_royalties", 0.0)
        label.streaming_fans   = data.get("streaming_fans", 0)
        label.prestige_bonus   = data.get("prestige_bonus", 0)
        return label


# ============================================================
# NEU: v3.11.0-beta.1 Expansion Classes
# ============================================================

class FanMail:
    """Repräsentiert eine Fanpost-Nachricht mit interaktiven Antwortoptionen."""
    def __init__(self, mail_id: str, sender: str, subject_key: str, text_key: str, options: list, is_read: bool = False, is_answered: bool = False, selected_option: int = None):
        self.mail_id = mail_id
        self.sender = sender
        self.subject_key = subject_key
        self.text_key = text_key
        self.options = options  # Liste von Dicts: [{"text_key": "...", "fans": 100, "hype": 5.0, "money": -500}]
        self.is_read = is_read
        self.is_answered = is_answered
        self.selected_option = selected_option

    def to_dict(self) -> dict:
        return {
            "mail_id": self.mail_id,
            "sender": self.sender,
            "subject_key": self.subject_key,
            "text_key": self.text_key,
            "options": self.options,
            "is_read": self.is_read,
            "is_answered": self.is_answered,
            "selected_option": self.selected_option,
        }

    @staticmethod
    def from_dict(data: dict) -> "FanMail":
        return FanMail(
            mail_id=data["mail_id"],
            sender=data["sender"],
            subject_key=data["subject_key"],
            text_key=data["text_key"],
            options=data["options"],
            is_read=data.get("is_read", False),
            is_answered=data.get("is_answered", False),
            selected_option=data.get("selected_option"),
        )


class SoundCardProject:
    """Repräsentiert ein Soundkarten-Entwicklungsprojekt im Hardware-Labor."""
    def __init__(self, name: str, features: list, dev_cost: int, progress: float = 0.0, is_released: bool = False, weeks_on_market: int = 0, royalties_gained: float = 0.0, market_share: float = 0.0, lifetime_royalties: float = 0.0):
        self.name = name
        self.features = features  # Liste von Tech-IDs
        self.dev_cost = dev_cost
        self.progress = progress
        self.is_released = is_released
        self.weeks_on_market = weeks_on_market
        self.royalties_gained = royalties_gained
        self.market_share = market_share
        self.lifetime_royalties = lifetime_royalties

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "features": self.features,
            "dev_cost": self.dev_cost,
            "progress": self.progress,
            "is_released": self.is_released,
            "weeks_on_market": self.weeks_on_market,
            "royalties_gained": self.royalties_gained,
            "market_share": self.market_share,
            "lifetime_royalties": self.lifetime_royalties,
        }

    @staticmethod
    def from_dict(data: dict) -> "SoundCardProject":
        return SoundCardProject(
            name=data["name"],
            features=data["features"],
            dev_cost=data["dev_cost"],
            progress=data.get("progress", 0.0),
            is_released=data.get("is_released", False),
            weeks_on_market=data.get("weeks_on_market", 0),
            royalties_gained=data.get("royalties_gained", 0.0),
            market_share=data.get("market_share", 0.0),
            lifetime_royalties=data.get("lifetime_royalties", 0.0),
        )


class RadioJingle:
    """Repräsentiert ein produziertes Radio-Jingle für Marketing-Zwecke."""
    def __init__(self, name: str, music_track: str, voice_style: str, sfx: str, hype_bonus: float, cost: int):
        self.name = name
        self.music_track = music_track
        self.voice_style = voice_style
        self.sfx = sfx
        self.hype_bonus = hype_bonus
        self.cost = cost

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "music_track": self.music_track,
            "voice_style": self.voice_style,
            "sfx": self.sfx,
            "hype_bonus": self.hype_bonus,
            "cost": self.cost,
        }

    @staticmethod
    def from_dict(data: dict) -> "RadioJingle":
        return RadioJingle(
            name=data["name"],
            music_track=data["music_track"],
            voice_style=data["voice_style"],
            sfx=data["sfx"],
            hype_bonus=data.get("hype_bonus", 0.0),
            cost=data.get("cost", 0),
        )

class StreamingPlatform:
    def __init__(self, start_week: int):
        self.founded_week = start_week
        self.subscribers = 0
        self.server_level = 1
        self.exclusive_esports = False
        
    def get_maintenance_cost(self):
        return 50000 * self.server_level
        
    def get_monthly_revenue(self):
        # Base ad revenue + sub revenue
        return self.subscribers * (0.5 + 4.0)

    def get_max_capacity(self):
        return self.server_level * 500000

class CustomConsoleProject:
    """Repräsentiert die Entwicklung einer eigenen Spielekonsole."""
    def __init__(self, name: str, tech_level: int, dev_cost: int, price: int, progress: float = 0.0, is_released: bool = False, units_sold: int = 0, revenue: int = 0, active_users: int = 0, weeks_on_market: int = 0):
        self.name = name
        self.tech_level = tech_level
        self.dev_cost = dev_cost
        self.price = price
        self.progress = progress
        self.is_released = is_released
        self.units_sold = units_sold
        self.revenue = revenue
        self.active_users = active_users
        self.weeks_on_market = weeks_on_market

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "tech_level": self.tech_level,
            "dev_cost": self.dev_cost,
            "price": self.price,
            "progress": self.progress,
            "is_released": self.is_released,
            "units_sold": self.units_sold,
            "revenue": self.revenue,
            "active_users": self.active_users,
            "weeks_on_market": self.weeks_on_market
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            tech_level=data.get("tech_level", 10),
            dev_cost=data.get("dev_cost", 10000000),
            price=data.get("price", 299),
            progress=data.get("progress", 0.0),
            is_released=data.get("is_released", False),
            units_sold=data.get("units_sold", 0),
            revenue=data.get("revenue", 0),
            active_users=data.get("active_users", 0),
            weeks_on_market=data.get("weeks_on_market", 0)
        )


class MerchCampaign:
    """Eine Merchandising-Kampagne (T-Shirts, Figuren, etc.)"""
    def __init__(self, game_name, merch_type, duration_weeks, investment):
        self.game_name = game_name
        self.merch_type = merch_type
        self.duration_weeks = duration_weeks
        self.weeks_active = 0
        self.investment = investment
        self.total_revenue = 0

    def to_dict(self):
        return {
            "game_name": self.game_name,
            "merch_type": self.merch_type,
            "duration_weeks": self.duration_weeks,
            "weeks_active": self.weeks_active,
            "investment": self.investment,
            "total_revenue": self.total_revenue
        }

    @staticmethod
    def from_dict(data):
        m = MerchCampaign(
            data["game_name"],
            data["merch_type"],
            data["duration_weeks"],
            data["investment"]
        )
        m.weeks_active = data.get("weeks_active", 0)
        m.total_revenue = data.get("total_revenue", 0)
        return m
