import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# 1. Remove manual self.money subtraction/addition from start_merch_campaign
for i, line in enumerate(lines):
    if 'self.money -= investment' in line and 'track_expense' in lines[i+1]:
        lines.pop(i) # remove self.money -= investment
        break

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
    if 'self._process_port_projects()' in line:
        lines.insert(i+1, merch_loop)
        break

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
