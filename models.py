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
        return sum(self.scores) / len(self.scores)

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
        
        # NEU: Service & Support
        self.bugs = 0
        self.dlc_count = 0
        self.weeks_on_market = 0
        self.is_active = True

        # NEU: Sequels & IP-Rating
        self.ip_rating = 0
        self.sequel_number = 0  # 0 = Original, 2 = Sequel, 3 = Teil 3 etc.
        self.sub_genre = None

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
        }


class ActiveMMO:
    """Ein aktives Live-Service/MMO Spiel."""
    
    def __init__(self, game_project, initial_players=10000):
        self.game = game_project
        self.players = initial_players
        self.subscription_fee = 15  # 15 Euro pro Monat / 4 = ca. 3.75 pro Woche, machen wir einfach 3 Euro pro Woche
        self.server_cost_per_10k = 5000  # 5k Euro pro 10k Spieler
        self.weeks_active = 0
        
    @property
    def weekly_revenue(self):
        return self.players * 3
        
    @property
    def weekly_cost(self):
        return int((self.players / 10000) * self.server_cost_per_10k)
        
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
        }



class Email:
    """Modell für Fan-Post und Bug-Reports."""
    def __init__(self, sender, subject, body, date_week, game_name=None, is_bug=False):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.date_week = date_week
        self.game_name = game_name
        self.is_bug = is_bug
        self.is_read = False


class EngineFeature:
    """Ein Feature, das in einer Engine verbaut werden kann."""

    def __init__(self, category, name, tech_bonus):
        self.category = category  # "Grafik", "Sound", "KI", "Gameplay", "Level"
        self.name = name
        self.tech_bonus = tech_bonus

    def __str__(self):
        return f"{self.name} ({self.category}, Tech: +{self.tech_bonus})"


class Engine:
    """Eine vom Spieler erstellte Game-Engine."""

    def __init__(self, name, features=None):
        self.name = name
        self.features = features or []  # Liste von EngineFeature

    @property
    def tech_level(self):
        return sum(f.tech_bonus for f in self.features)

    @property
    def quality_bonus(self):
        """Bonus auf die Spielqualität (0.0 - 0.3)."""
        return min(0.3, self.tech_level * 0.02)

    def has_feature_category(self, category):
        """Hat die Engine ein Feature dieser Kategorie?"""
        return any(f.category == category for f in self.features)

    def summary(self):
        """Zusammenfassung für NVDA."""
        feat_names = ", ".join(get_text(f.name) for f in self.features) if self.features else get_text('none')
        return get_text('engine_summary', name=self.name, tech_level=self.tech_level, features=feat_names)

    def __str__(self):
        return f"{self.name} (Tech: {self.tech_level})"


class Employee:
    """Ein Mitarbeiter des Studios."""

    def __init__(self, name=None, role_data=None, skill_level=1, specialization=None, trait=None):
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

        # Skills basierend auf Rolle und Level generieren
        self.skills = self._generate_skills()

        # Gehalt basierend auf Skills
        self.salary = self._calculate_salary()
        self.morale = 100          # 0-100
        self.weeks_employed = 0

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
        """Wöchentliches Gehalt basierend auf Gesamtskills und Eigenschaft."""
        total_skill = sum(self.skills.values())
        base_salary = total_skill * 5 + 500
        if self.trait and self.trait["effect"] == "salary":
            base_salary *= self.trait["value"]
        return int(base_salary)

    @property
    def quality_contribution(self):
        """Wie viel Qualität fügt dieser Mitarbeiter hinzu (0.0 - 0.1)."""
        avg_skill = sum(self.skills.values()) / len(self.skills)
        return avg_skill / 1000.0  # 0.0 - 0.1

    def get_slider_bonus(self, slider_name):
        """Bonus für einen bestimmten Slider (0.0 - 1.0)."""
        skill = self.skills.get(slider_name, 0)
        return skill / 100.0

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
        }

class RivalGame:
    """Spiel, das von der KI-Konkurrenz veröffentlicht wird."""
    
    def __init__(self, name, topic, genre, score, weeks_on_market=0):
        self.name = name
        self.topic = topic
        self.genre = genre
        self.score = score
        self.weeks_on_market = weeks_on_market
        self.is_active = True

    def to_dict(self):
        return {
            "name": self.name,
            "topic": self.topic,
            "genre": self.genre,
            "score": self.score,
            "weeks_on_market": self.weeks_on_market,
            "is_active": self.is_active
        }

class RivalStudio:
    """KI-gesteuertes Konkurrenz-Studio."""
    
    def __init__(self, name, target_market_share=10, games=None, next_release_week=None, owned_shares=0):
        self.name = name
        self.target_market_share = target_market_share
        self.games = games or []
        self.next_release_week = next_release_week or random.randint(10, 30)
        self.owned_shares = owned_shares

    def to_dict(self):
        return {
            "name": self.name,
            "target_market_share": self.target_market_share,
            "games": [g.to_dict() for g in self.games],
            "next_release_week": self.next_release_week,
            "owned_shares": self.owned_shares
        }

class BankLoan:
    """Aktiver Kredit bei der Bank."""
    def __init__(self, amount_borrowed, interest_rate, duration_weeks, amount_remaining=None, weeks_remaining=None):
        self.amount_borrowed = amount_borrowed
        # Feste Gesamtrückzahlung: z.B. 100k + 20% = 120k
        total_repayment = int(amount_borrowed * (1.0 + interest_rate))
        self.amount_remaining = amount_remaining if amount_remaining is not None else total_repayment
        self.weeks_remaining = weeks_remaining if weeks_remaining is not None else duration_weeks
        self.weekly_payment = int(total_repayment / duration_weeks)

    def to_dict(self):
        return {
            "amount_borrowed": self.amount_borrowed,
            "amount_remaining": self.amount_remaining,
            "weekly_payment": self.weekly_payment,
            "weeks_remaining": self.weeks_remaining
        }

class CustomConsole:
    """Vom Spieler entwickelte Konsole."""
    def __init__(self, name, tech_level, dev_cost, release_week):
        self.name = name
        self.tech_level = tech_level
        self.dev_cost = dev_cost
        self.release_week = release_week
        self.market_share = 0.05 # Startet mit 5% Marktanteil
        
    def to_dict(self):
        return {
            "name": self.name,
            "tech_level": self.tech_level,
            "dev_cost": self.dev_cost,
            "release_week": self.release_week,
            "market_share": self.market_share
        }

