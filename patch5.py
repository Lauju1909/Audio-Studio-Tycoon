import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('body=f"Die {m.merch_type}-Kampagne fÃ¼r {m.game_name} ist beendet.\\nGesamtumsatz: {m.total_revenue} Euro"', 'body=f"Die {m.merch_type}-Kampagne fÃ¼r {m.game_name} ist beendet.\\nGesamtumsatz: {m.total_revenue} Euro", date_week=self.week')

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
