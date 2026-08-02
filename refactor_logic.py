
def main():
    with open('logic.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert imports and managers instantiation in GameState.__init__
    init_target = """        self.monetization_back_target = "bank_menu" # Default target for back button"""
    init_replacement = """        self.monetization_back_target = "bank_menu" # Default target for back button
        
        # Managers
        from managers.hr import HRManager
        from managers.finance import FinanceManager
        from managers.marketing import MarketingManager
        self.hr_manager = HRManager(self)
        self.finance_manager = FinanceManager(self)
        self.marketing_manager = MarketingManager(self)"""
    
    content = content.replace(init_target, init_replacement)

    # 2. Extracting from _on_new_week
    # We will find _on_new_week, locate the lines to keep, and insert the manager tick calls.
    
    # We keep the beginning of _on_new_week up to:
    #         self._process_audio_pass()
    
    # Then we have the is_new_month calculation:
    month_calc = """        # Monatsankündigung (dynamisch basierend auf WEEKS_PER_YEAR)
        week_in_year = (self.week - 1) % WEEKS_PER_YEAR + 1
        prev_week_in_year = (self.week - 2) % WEEKS_PER_YEAR + 1 if self.week > 1 else 0
        
        current_month = int((week_in_year - 1) * 12 / WEEKS_PER_YEAR)
        prev_month = int((prev_week_in_year - 1) * 12 / WEEKS_PER_YEAR) if self.week > 1 else -1
        
        is_new_month = (current_month != prev_month)"""

    # We need to remove from "        # Merchandising verarbeiten" 
    # to the end of the HR stuff, just before:
    #         # Projektfortschritt für alle aktiven Projekte
    # Wait, there's a lot of stuff.
    
    start_remove = "        # Merchandising verarbeiten"
    end_remove = "        # Projektfortschritt für alle aktiven Projekte"
    
    if start_remove in content and end_remove in content:
        before = content.split(start_remove)[0]
        after = end_remove + content.split(end_remove, 1)[1]
        
        # Now we need to re-insert the is_new_month block and the manager ticks
        new_logic = f"""
{month_calc}

        if is_new_month and self.week > 1:
            cal = self.get_calendar_text()
            self.emails.insert(0, Email(
                sender=self.get_text('sender_calendar'),
                subject=self.get_text('subject_new_month', date=cal),
                body=self.get_text('body_new_month', date=cal,
                                   money=self.money, fans=int(self.fans)),
                date_week=self.week
            ))
            if hasattr(self, 'audio'):
                self.audio.speak(self.get_text('announce_new_month', date=cal), interrupt=False)

        # Manager Ticks
        self.hr_manager.tick()
        self.finance_manager.tick(is_new_month)
        self.marketing_manager.tick(is_new_month)
        
        # Eigene Konsolenverkaeufe und Marktanteil
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

        # Zufallsereignisse prüfen
        self.check_random_event()
        
        # Abgelaufene Events entfernen
        new_active = []
        for e in self.active_events:
            if "duration" in e:
                e["duration"] -= 1
                if e["duration"] > 0:
                    new_active.append(e)
            else:
                new_active.append(e)
        self.active_events = new_active

        """
        
        content = before + new_logic + after
        
    with open('logic.py', 'w', encoding='utf-8') as f:
        f.write(content)
        print("Success")

if __name__ == '__main__':
    main()
