import random
from models import Email

class ITSecurityManager:
    def __init__(self):
        pass
        
    def tick(self, state):
        # Starts in 2000 (Week 520)
        if state.week < 52 * 10:
            return
            
        # Initialize variables if not present
        if not hasattr(state, 'it_upgrades'):
            state.it_upgrades = []
        if not hasattr(state, 'active_cyber_effects'):
            state.active_cyber_effects = []
            
        self._process_active_effects(state)
        self._check_for_attacks(state)
        
    def _process_active_effects(self, state):
        remaining = []
        for effect in state.active_cyber_effects:
            effect["weeks_left"] -= 1
            if effect["weeks_left"] > 0:
                remaining.append(effect)
            else:
                if effect["type"] == "ddos":
                    # Inform user DDoS is over
                    state.emails.insert(0, Email(
                        sender="IT-Security",
                        subject="DDoS-Attacke beendet",
                        body="Unsere Server sind wieder online! Der Shop und die MMOs laufen wieder.",
                        date_week=state.week
                    ))
        state.active_cyber_effects = remaining
        
    def _check_for_attacks(self, state):
        # Only 1 attack per month max
        if state.week % 4 != 0:
            return
            
        # Base threat level based on money and fans
        threat_level = 0.0
        if state.money > 10000000:
            threat_level += 0.05
        if state.fans > 100000:
            threat_level += 0.05
            
        if threat_level <= 0:
            return
            
        # Defenses reduce chance
        if "firewall_1" in state.it_upgrades:
            threat_level -= 0.05
        if "firewall_2" in state.it_upgrades:
            threat_level -= 0.05
            
        threat_level = max(0.01, threat_level) # Always a tiny risk if rich
        
        if random.random() < threat_level:
            self._trigger_random_attack(state)
            
    def _trigger_random_attack(self, state):
        attacks = ["ddos", "leak", "phishing", "ransomware"]
        attack = random.choice(attacks)
        
        if attack == "ddos":
            # DDoS disables digital sales
            state.active_cyber_effects.append({"type": "ddos", "weeks_left": 3})
            state.emails.insert(0, Email(
                sender="Hacker-Kollektiv",
                subject="Deine Server sind OFFLINE",
                body="Wir haben deine Server mit einer DDoS-Attacke lahmgelegt! Alle digitalen Verkäufe sind für 3 Wochen pausiert.",
                date_week=state.week
            ))
            
        elif attack == "phishing":
            if "phishing_training" in state.it_upgrades:
                state.emails.insert(0, Email(
                    sender="IT-Security",
                    subject="Phishing-Angriff abgewehrt!",
                    body="Jemand hat versucht, unsere Mitarbeiter zu phishen, aber dank des Trainings ist niemand darauf reingefallen.",
                    date_week=state.week
                ))
            else:
                stolen = min(state.money * 0.1, 5000000) # 10% of money, max 5M
                state.money -= stolen
                state.track_expense("cyber_attack", stolen)
                state.emails.insert(0, Email(
                    sender="IT-Security",
                    subject="GEHACKT! Phishing erfolgreich",
                    body=f"Ein Mitarbeiter hat sein Passwort weitergegeben. Kriminelle haben ${stolen:,.2f} von unseren Konten gestohlen!",
                    date_week=state.week
                ))
                
        elif attack == "leak":
            if getattr(state, "current_project", None) and not state.current_project.is_released:
                state.current_project.hype = max(0, state.current_project.hype - 30)
                state.emails.insert(0, Email(
                    sender="IT-Security",
                    subject="Quellcode GELEAKT!",
                    body=f"Hacker haben den Code von '{state.current_project.name}' geleakt. Der Hype ist massiv eingebrochen!",
                    date_week=state.week
                ))
                
        elif attack == "ransomware":
            if "encrypted_backups" in state.it_upgrades:
                state.emails.insert(0, Email(
                    sender="IT-Security",
                    subject="Ransomware abgewehrt",
                    body="Eine Ransomware hat unsere Systeme verschlüsselt. Da wir aber sichere Backups haben, konnten wir alles in wenigen Stunden wiederherstellen!",
                    date_week=state.week
                ))
            elif getattr(state, "current_project", None) and not state.current_project.is_released:
                # The game just loses 25% progress.
                lost_progress = state.current_project.progress * 0.25
                state.current_project.progress -= lost_progress
                state.emails.insert(0, Email(
                    sender="Hacker-Kollektiv",
                    subject="Ransomware! Systeme verschlüsselt",
                    body="Wir haben deine Entwickler-PCs verschlüsselt. Ohne Backups hast du 25% des Projektfortschritts verloren!",
                    date_week=state.week
                ))
