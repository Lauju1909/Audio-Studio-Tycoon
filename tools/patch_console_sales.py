import codecs

lines = []
with codecs.open('logic.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_block = """        # Eigene Konsolenverkaeufe und Marktanteil
        if hasattr(self, "custom_consoles"):
            for cc in self.custom_consoles:
                # Basis-Wachstum + Hype
                base_sales = int(5000 * cc.market_share * (1.0 + getattr(cc, 'hype', 0) / 100))
                
                # Exklusivtitel-Bonus
                exclusives_bonus = 1.0
                for game in self.game_history:
                    if game.platform == cc.name and game.sales > 0:
                        exclusives_bonus += 0.5 * (game.review.average / 10.0) # Sehr gute Exklusivtitel pushen extrem!
                        
                weekly_sales = int(base_sales * exclusives_bonus)
                
                # Saettigung: Irgendwann kauft es keiner mehr
                saturation = getattr(cc, 'units_sold', 0) / 100000000.0 # Ab 100 Mio wird es schwerer
                weekly_sales = int(weekly_sales * max(0.1, 1.0 - saturation))
                
                cc.units_sold = getattr(cc, 'units_sold', 0) + weekly_sales
                
                # Gewinn pro verkaufter Konsole (z.B. 50 EUR pro Stueck)
                profit = weekly_sales * 50
                if profit > 0:
                    self.money += profit
                    self.track_income("hardware", profit)
                
                # Marktanteil waechst langsam durch Verkaeufe
                cc.market_share = min(0.6, cc.market_share + (weekly_sales / 10000000.0))
                
                # Hype nimmt ab
                if getattr(cc, 'hype', 0) > 0:
                    cc.hype = max(0, cc.hype - 0.5)
"""

start = -1
end = -1
for i, line in enumerate(lines):
    if '# Marktanteil der eigenen Konsole' in line:
        start = i
    if start != -1 and 'cc.market_share = min(0.5' in line:
        end = i + 1
        break

if start != -1 and end != -1:
    lines = lines[:start] + [new_block + '\n'] + lines[end:]

with codecs.open('logic.py', 'w', 'utf-8') as f:
    f.writelines(lines)
