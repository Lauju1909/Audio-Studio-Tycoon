
with open('menus/business.py', 'r', encoding='utf-8') as f:
    content = f.read()

transmedia_code = """
class TransmediaMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Transmedia Empire (Film & Serien)", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options.clear()
        
        # Only show games with IP rating > 40 and no existing movie deal
        eligible_games = [g for g in self.game_state.game_history if g.ip_rating >= 40 and not getattr(g, "has_movie_deal", False)]
        
        for g in eligible_games:
            self.options.append({
                'text': f"{g.name} (IP: {g.ip_rating})",
                'action': lambda game=g: self._select_game(game)
            })
            
        if not eligible_games:
            self.options.append({
                'text': "Keine geeigneten IPs (IP-Rating > 40 & noch keine Adaption) verfuegbar.",
                'action': lambda: None
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "business_menu"})

    def _select_game(self, game):
        # We need to set up the deal context
        self.game_state.selected_transmedia_game = game
        return "transmedia_deal_menu"

class TransmediaDealMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        game = getattr(self.game_state, "selected_transmedia_game", None)
        title = f"Transmedia Deal für {game.name}" if game else "Transmedia Deal"
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options.clear()
        game = getattr(self.game_state, "selected_transmedia_game", None)
        
        if not game:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "transmedia_menu"})
            return
            
        import random
        
        # Movie Deal
        movie_offer = 5000000 + (game.ip_rating * 100000)
        self.options.append({
            'text': f"Kino-Film Deal ({movie_offer:,} EUR Vorschuss)",
            'action': lambda: self._sign_deal(game, movie_offer, "Kino")
        })
        
        # Series Deal (Netflix style) unlocks later (2012)
        if self.game_state.get_calendar_year() >= 2012:
            series_offer = 3000000 + (game.ip_rating * 150000)
            self.options.append({
                'text': f"Streaming-Serie Deal ({series_offer:,} EUR Vorschuss)",
                'action': lambda: self._sign_deal(game, series_offer, "Streaming")
            })
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "transmedia_menu"})

    def _sign_deal(self, game, upfront, deal_type):
        import random
        
        self.game_state.money += upfront
        game.has_movie_deal = True
        
        # Simulate massive sales boost based on deal type
        hit_chance = 0.7 if deal_type == "Streaming" else 0.5
        
        if random.random() < hit_chance:
            # Massive Hit! Reactivate game if inactive, or just boost stats massively
            bonus_sales = random.randint(500000, 2000000)
            bonus_revenue = bonus_sales * 25 # Assuming 25 per copy
            game.sales += bonus_sales
            game.revenue += bonus_revenue
            game.ip_rating += random.randint(10, 30)
            
            # Optionally reactivate the game
            game.is_active = True
            game.weeks_on_market = max(1, game.weeks_on_market)
            
            self.audio.play_sound('cash')
            self.audio.speak(f"Ein gigantischer Hit! Die {deal_type}-Adaption treibt die Verkufe von {game.name} durch die Decke! (+{bonus_sales:,} Sales)")
        else:
            # Flop, just minor boost
            bonus_sales = random.randint(10000, 50000)
            game.sales += bonus_sales
            game.revenue += bonus_sales * 25
            game.ip_rating -= random.randint(1, 5)
            self.audio.play_sound('error')
            self.audio.speak(f"Die {deal_type}-Adaption war ein Flop bei den Kritikern. Die Fans sind enttuscht. (+{bonus_sales:,} Sales)")
            
        return "transmedia_menu"
"""

if "class TransmediaMenu(Menu):" not in content:
    content += "\n" + transmedia_code
    with open('menus/business.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added TransmediaMenu to business.py")
else:
    print("TransmediaMenu already in business.py")

