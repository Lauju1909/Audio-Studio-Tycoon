import random
from models import Email

class ConventionManager:
    """Verwaltet jährliche Messen und Conventions (z.B. Global Audio Expo)."""
    
    def __init__(self):
        self.convention_week = 24  # Jedes Jahr in Woche 24
        self.is_active = False
        
        self.booth_tiers = {
            "none": {"cost": 0, "hype_multi": 0.0, "name": "Kein Stand"},
            "small": {"cost": 50000, "hype_multi": 1.5, "name": "Kleiner Indie-Stand"},
            "medium": {"cost": 250000, "hype_multi": 3.0, "name": "Mittlerer Messestand"},
            "mega": {"cost": 1000000, "hype_multi": 7.0, "name": "Mega-Booth Halle"}
        }

    def tick(self, state):
        """Wird jede Woche aufgerufen."""
        # Check if feature is unlocked (from 1995 onwards)
        if hasattr(state, "is_feature_unlocked") and not state.is_feature_unlocked("soundcon"):
            return
            
        # Ankündigung der Messe 4 Wochen vorher
        week_in_year = (state.week - 1) % 52 + 1
        
        if week_in_year == self.convention_week - 4:
            state.emails.insert(0, Email(
                sender="Expo Orga-Team",
                subject="Anmeldung zur Global Audio Expo",
                body=f"Die größte Messe des Jahres steht bevor (Woche {self.convention_week})! Buche jetzt einen Stand, um deine aktuellen Projekte der Welt zu präsentieren.",
                date_week=state.week
            ))
            
        # Messe-Woche
        if week_in_year == self.convention_week:
            self._run_convention(state)
            
    def book_booth(self, state, tier: str, game_project=None):
        """Bucht einen Stand für die Messe und weist optional ein Projekt zu, das gezeigt werden soll."""
        if tier not in self.booth_tiers or tier == "none":
            return False
            
        cost = self.booth_tiers[tier]["cost"]
        if state.money < cost:
            return False
            
        state.track_expense("marketing", cost) # Messen gelten als Marketing
        
        # In state merken, was gebucht wurde
        state.current_convention_booking = {
            "tier": tier,
            "project": game_project
        }
        return True

    def _run_convention(self, state):
        """Führt die Messe in Woche 24 aus."""
        booking = getattr(state, "current_convention_booking", None)
        
        if not booking or booking["tier"] == "none":
            # Nichts gebucht
            return
            
        tier_data = self.booth_tiers[booking["tier"]]
        project = booking["project"]
        
        body_msg = f"Wir haben unseren {tier_data['name']} auf der Global Audio Expo eröffnet! "
        
        if project and project.review is None:
            # Projekt Hype boosten basierend auf Fortschritt und Stand-Größe
            progress_factor = min(1.0, max(0.1, project.progress / 100.0))
            hype_gain = int(10 * tier_data["hype_multi"] * progress_factor * random.uniform(0.8, 1.2))
            
            project.hype = getattr(project, "hype", 0) + hype_gain
            body_msg += f"\nUnsere Demo für '{project.name}' kam fantastisch an. Das Spiel hat +{hype_gain} Hype generiert!"
            
            # Chance auf "Best of Show" Award bei Medium/Mega Booth
            if booking["tier"] in ["medium", "mega"]:
                if random.random() < (0.15 if booking["tier"] == "mega" else 0.05):
                    project.quality_boost = getattr(project, "quality_boost", 0) + 1.0
                    body_msg += "\n\n!!! WIR HABEN DEN 'BEST OF SHOW' AWARD GEWONNEN !!! Das gibt einen massiven Qualitätsboost!"
                    if hasattr(state, "audio"):
                        state.audio.play_sound("success")
        else:
            body_msg += "\nWir waren präsent, hatten aber keine neuen spielbaren Demos dabei. Immerhin haben wir Präsenz gezeigt."
            
        state.emails.insert(0, Email(
            sender="PR Manager",
            subject="Bericht von der Global Audio Expo",
            body=body_msg,
            date_week=state.week
        ))
        
        # Reset booking for next year
        state.current_convention_booking = None
