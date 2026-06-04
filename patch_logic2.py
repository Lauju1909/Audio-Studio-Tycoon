import sys

with open('logic.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_rivals = '''    def _process_rivals(self):
        """Lsst Rivalen Spiele verffentlichen und Marktanteile beeinflussen."""
        import competitor_ai
        
        for rival in self.rivals:
            if getattr(rival, 'is_owned_by_player', False):
                # Phase 2 M&A: Passive Einnahmen durch den Backkatalog
                back_catalog_income = int(sum(getattr(g, 'score', 0) * 100 for g in getattr(rival, 'games', [])))
                if back_catalog_income > 0:
                    self.track_income("other", back_catalog_income)
                continue

            r_game = competitor_ai.evaluate_turn(rival, self)'''

new_rivals = '''    def _process_rivals(self):
        """Lsst Rivalen Spiele verffentlichen und Marktanteile beeinflussen."""
        import competitor_ai
        
        for rival in self.rivals:
            is_owned = getattr(rival, 'is_owned_by_player', False)
            if is_owned:
                # Phase 2 M&A: Passive Einnahmen durch den Backkatalog
                back_catalog_income = int(sum(getattr(g, 'score', 0) * 100 for g in getattr(rival, 'games', [])))
                if back_catalog_income > 0:
                    self.money += back_catalog_income
                    self.track_income("other", back_catalog_income)

            r_game = competitor_ai.evaluate_turn(rival, self)
            
            if r_game and is_owned:
                # Apply quality boost
                quality_boost = getattr(rival, 'games_quality_boost', 0)
                if quality_boost > 0:
                    r_game.score = min(10.0, r_game.score + quality_boost / 10.0)
                    
                # Develop for our console
                if getattr(rival, 'develop_for_custom_console', False) and getattr(self, 'active_custom_console', None):
                    self.active_custom_console['market_presence'] += 5.0
                    
                # Einnahmen aus dem neuen Spiel direkt an den Spieler
                release_income = int(r_game.score * random.randint(100000, 500000))
                self.money += release_income
                self.track_income("publishing", release_income)
                
                self.emails.append(Email(
                    sender=self.get_text('sender_industry_news'),
                    subject=f"Tochterfirma {rival.name} verffentlicht {r_game.name}!",
                    body=f"Dein Tochterstudio {rival.name} hat '{r_game.name}' verffentlicht (Wertung: {r_game.score:.1f}/10). Einnahmen: {release_income:,} EUR.",
                    date_week=self.week
                ))
            elif r_game:'''

content = content.replace(old_rivals, new_rivals)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched _process_rivals")
