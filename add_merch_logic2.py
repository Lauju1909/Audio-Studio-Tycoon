import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to load_game
if 'from models import Addon' in content and 'MerchCampaign' not in content:
    content = content.replace('from models import Addon', 'from models import Addon, MerchCampaign')

load_loc = content.find('self.active_addons = [Addon.from_dict(ad) for ad in data.get("active_addons", [])]')
if 'self.active_merch = [MerchCampaign.from_dict(m) for m in data.get("active_merch", [])]' not in content:
    content = content[:load_loc] + 'self.active_merch = [MerchCampaign.from_dict(m) for m in data.get("active_merch", [])]\n        ' + content[load_loc:]

# Add start_merch_campaign
merch_method = '''
    def start_merch_campaign(self, game_name, merch_type, duration_weeks, investment):
        """Startet eine neue Merchandising-Kampagne."""
        if self.money < investment:
            return False
            
        self.money -= investment
        self.track_expense("marketing", investment) # Marketing/Merch Kategorie
        
        from models import MerchCampaign
        camp = MerchCampaign(game_name, merch_type, duration_weeks, investment)
        self.active_merch.append(camp)
        return True
'''
if 'def start_merch_campaign' not in content:
    content += merch_method

# Add to _on_new_week
merch_loop = '''
        # Merchandising verarbeiten
        for m in list(getattr(self, "active_merch", [])):
            base_game = next((g for g in self.game_history if g.name == m.game_name), None)
            if base_game:
                # Einnahmen hängen von der IP-Rating und Base-Game Sales ab
                multiplier = 1.0
                if m.merch_type == "T-Shirts": multiplier = 1.2
                elif m.merch_type == "Action-Figuren": multiplier = 2.0
                elif m.merch_type == "Soundtrack CD/Vinyl": multiplier = 1.5
                
                # Base earnings dependent on investment and IP strength
                ip_strength = base_game.ip_rating / 100.0
                weekly_income = int((m.investment / m.duration_weeks) * 1.5 * multiplier * (0.5 + ip_strength))
                
                self.money += weekly_income
                m.total_revenue += weekly_income
                self.track_income("merch", weekly_income)
                
                # Passiver Hype/Fan boost
                self.fans += int(10 * multiplier)
                base_game.hype = min(100, base_game.hype + 1)
                
            m.weeks_active += 1
            if m.weeks_active >= m.duration_weeks:
                self.emails.insert(0, Email(
                    sender=self.get_text("sender_marketing"),
                    subject=f"Merch beendet: {m.game_name}",
                    body=f"Die {m.merch_type}-Kampagne für {m.game_name} ist beendet.\\nGesamtumsatz: {m.total_revenue}€"
                ))
                self.active_merch.remove(m)
'''
if '# Merchandising verarbeiten' not in content:
    target = '# Kredite verarbeiten'
    idx = content.find(target)
    content = content[:idx] + merch_loop + '\n        ' + content[idx:]

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
