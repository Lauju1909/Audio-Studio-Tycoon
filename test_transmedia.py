from logic import GameState
from models import GameProject
import menus.business as mb
from audio import AudioManager

class DummyAudio(AudioManager):
    def __init__(self):
        pass
    def play_sound(self, name):
        pass
    def speak(self, text, interrupt=False):
        pass
    def generate_speech(self, text):
        return None

def test_transmedia_empire():
    gs = GameState()
    gs.week = 52 * 90  # Year 2020 (Starts at 1930 + 90 = 2020)
    audio = DummyAudio()
    
    # Unlock Transmedia manually if needed, or by year
    assert gs.get_calendar_year() >= 2012
    assert gs.is_feature_unlocked("transmedia")
    
    # Create game
    game = GameProject("Transmedia Test Game", "Test", "Test", size="AAA")
    game.ip_rating = 50
    gs.game_history.append(game)
    
    menu = mb.TransmediaMenu(audio, gs)
    assert len(menu.options) == 2 # 1 Game + Back
    
    # Select game
    assert menu._select_game(game) == "transmedia_deal_menu"
    assert gs.selected_transmedia_game == game
    
    deal_menu = mb.TransmediaDealMenu(audio, gs)
    assert len(deal_menu.options) == 3 # Kino, Streaming, Back
    
    # Sign streaming deal
    initial_money = gs.money
    initial_sales = game.sales
    deal_menu._sign_deal(game, 5000000, "Streaming")
    
    assert gs.money == initial_money + 5000000
    assert getattr(game, 'has_movie_deal', False) == True
    assert game.sales > initial_sales

    # Check menu update
    deal_menu._update_options()
    
    menu._update_options()
    assert len(menu.options) == 2 # "Keine verfuegbar" + Back since game is now has_movie_deal
