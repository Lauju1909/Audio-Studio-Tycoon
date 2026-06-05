import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# 1. Add to init
for i, line in enumerate(lines):
    if 'self.active_addons = []' in line:
        lines.insert(i, '        self.active_merch_campaigns = []')
        break

# 2. Add to to_dict
for i, line in enumerate(lines):
    if '"active_addons": [a.to_dict() for a in self.active_addons],' in line:
        lines.insert(i, '            "active_merch_campaigns": [m.to_dict() for m in getattr(self, "active_merch_campaigns", [])],')
        break

# 3. Add to load_game
for i, line in enumerate(lines):
    if 'self.active_addons = [Addon.from_dict(ad) for ad in data.get("active_addons", [])]' in line:
        lines.insert(i, '        from models import MerchCampaign')
        lines.insert(i+1, '        self.active_merch_campaigns = [MerchCampaign.from_dict(m) for m in data.get("active_merch_campaigns", [])]')
        break

# 4. Add start_merch_campaign method
merch_method = '''
    def start_merch_campaign(self, game_name, merch_type, duration_weeks, investment):
        """Startet eine neue Merchandising-Kampagne."""
        if self.money < investment:
            return False
            
        self.money -= investment
        self.track_expense("marketing", investment)
        
        from models import MerchCampaign
        camp = MerchCampaign(game_name, merch_type, duration_weeks, investment)
        self.active_merch_campaigns.append(camp)
        return True
'''

for i, line in enumerate(lines):
    if 'def start_update_project' in line:
        lines.insert(i, merch_method)
        break

# 5. Add processing to _on_new_week
merch_loop = '''
        # Merchandising verarbeiten
        for m in list(getattr(self, "active_merch_campaigns", [])):
            base_game = next((g for g in self.game_history if g.name == m.game_name), None)
            if base_game:
                multiplier = 1.0
                if m.merch_type == "T-Shirts": multiplier = 1.2
                elif m.merch_type == "Action-Figuren": multiplier = 2.0
                elif m.merch_type == "Soundtrack CD/Vinyl": multiplier = 1.5
                
                ip_strength = base_game.ip_rating / 100.0
                weekly_income = int((m.investment / m.duration_weeks) * 1.5 * multiplier * (0.5 + ip_strength))
                
                self.money += weekly_income
                m.total_revenue += weekly_income
                self.track_income("merch", weekly_income)
                
                self.fans += int(10 * multiplier)
                base_game.hype = min(100, base_game.hype + 1)
                
            m.weeks_active += 1
            if m.weeks_active >= m.duration_weeks:
                self.emails.insert(0, Email(
                    sender=self.get_text("sender_marketing"),
                    subject=f"Merch beendet: {m.game_name}",
                    body=f"Die {m.merch_type}-Kampagne fÃ¼r {m.game_name} ist beendet.\\nGesamtumsatz: {m.total_revenue} Euro"
                ))
                self.active_merch_campaigns.remove(m)
'''

for i, line in enumerate(lines):
    if '# Kredite verarbeiten' in line:
        lines.insert(i, merch_loop)
        break

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
