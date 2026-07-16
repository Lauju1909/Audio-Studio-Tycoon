import random

class PublisherDeal:
    """Repräsentiert einen einzelnen Publisher-Vertrag."""
    def __init__(self, deal_id, publisher_name, genre_focus, upfront_funding, rev_share_percent, deadline_weeks, min_quality):
        self.id = deal_id
        self.publisher_name = publisher_name
        self.genre_focus = genre_focus
        self.upfront_funding = upfront_funding
        self.rev_share_percent = rev_share_percent # Anteil, den der Publisher einbehält
        self.deadline_weeks = deadline_weeks
        self.min_quality = min_quality # Erwartete Mindest-Bewertung in Prozent
        
        self.active = False
        self.failed = False
        self.completed = False
        self.weeks_passed = 0
        self.game_attached = None

class PublisherManager:
    """Verwaltet fortschrittliche Publisher-Mechaniken (Deals, Meilensteine, Ruf)."""
    def __init__(self, state):
        self.state = state
        self.available_deals = []
        self.active_deals = []
        self.reputation = {} # publisher_name: int (0-100)
        self._generate_initial_publishers()

    def _generate_initial_publishers(self):
        """Generiert die Basis-Publisher für das Spiel."""
        self.publishers = [
            {"name": "EAudio", "focus": "Action", "base_funding": 500000, "base_share": 60, "strictness": "high"},
            {"name": "Square Sound", "focus": "RPG", "base_funding": 300000, "base_share": 40, "strictness": "medium"},
            {"name": "IndieTune", "focus": "Simulation", "base_funding": 50000, "base_share": 20, "strictness": "low"}
        ]
        for p in self.publishers:
            self.reputation[p["name"]] = 50 # Neutraler Start-Ruf

    def generate_deals(self):
        """Generiert neue Vertragsangebote basierend auf dem Ruf."""
        self.available_deals.clear()
        for p in self.publishers:
            rep = self.reputation.get(p["name"], 50)
            
            # Höherer Ruf = Mehr Vorab-Funding, geringere Publisher-Abgabe
            funding_mod = 0.5 + (rep / 100)
            share_mod = 1.2 - (rep / 100)
            
            funding = int(p["base_funding"] * funding_mod)
            share = max(10, min(80, int(p["base_share"] * share_mod)))
            
            deal = PublisherDeal(
                deal_id=f"{p['name']}_{random.randint(1000,9999)}",
                publisher_name=p["name"],
                genre_focus=p["focus"],
                upfront_funding=funding,
                rev_share_percent=share,
                deadline_weeks=random.randint(20, 60),
                min_quality=random.randint(60, 90)
            )
            self.available_deals.append(deal)

    def sign_deal(self, deal_id):
        """Nimmt einen Vertrag an und zahlt den Vorschuss aus."""
        deal = next((d for d in self.available_deals if d.id == deal_id), None)
        if deal:
            deal.active = True
            self.available_deals.remove(deal)
            self.active_deals.append(deal)
            self.state.money += deal.upfront_funding
            return True
        return False

    def attach_game_to_deal(self, deal_id, game_name):
        """Verknüpft ein Spiel in Entwicklung mit einem aktiven Vertrag."""
        deal = next((d for d in self.active_deals if d.id == deal_id and not d.game_attached), None)
        if deal:
            deal.game_attached = game_name
            return True
        return False

    def update_tick(self):
        """Wird wöchentlich aufgerufen, um Deadlines zu prüfen."""
        for deal in self.active_deals:
            if not deal.completed and not deal.failed:
                deal.weeks_passed += 1
                if deal.weeks_passed > deal.deadline_weeks:
                    deal.failed = True
                    # Vertragsstrafe bei Überschreiten der Deadline
                    penalty = int(deal.upfront_funding * 1.5)
                    self.state.money -= penalty
                    self.reputation[deal.publisher_name] = max(0, self.reputation[deal.publisher_name] - 20)
                    
                    # Optional: Benachrichtigung über State-Event auslösen

    def evaluate_released_game(self, game_name, review_score):
        """Prüft beim Release eines Spiels, ob es einen Vertrag erfüllt."""
        for deal in self.active_deals:
            if deal.game_attached == game_name and not deal.completed and not deal.failed:
                deal.completed = True
                if review_score >= deal.min_quality:
                    self.reputation[deal.publisher_name] = min(100, self.reputation[deal.publisher_name] + 15)
                else:
                    # Mindestqualität verfehlt
                    self.reputation[deal.publisher_name] = max(0, self.reputation[deal.publisher_name] - 10)
