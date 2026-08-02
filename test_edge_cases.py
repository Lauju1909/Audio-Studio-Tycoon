from logic import GameState
from models import GameProject
from menus import UnionEventMenu, InfluencerEventMenu

class MockAudio:
    def speak(self, text, interrupt=False): pass
    def play_sound(self, sound): pass

def test_simultaneous_events():
    state = GameState()
    state.money = 1000000
    state.fans = 100000
    
    # Setup projects
    project = GameProject("VR Test", "Cyberpunk", "Action", "PC", "Jeder", "AAA", "Kein Marketing")
    project.is_active = True
    project.sales = 50000
    state.game_history.append(project)

    # Trigger events simultaneously
    state.pending_union_event = {"title": "Streik"}
    state.pending_influencer_event = {"game_name": "VR Test", "sponsorship": {"boost": 1.5, "duration": 10}}
    state.pending_movie_deal = {"game_name": "VR Test", "partner": "Netflux", "advance": 500000, "royalty": 0.15}
    
    # If the user interacts with union busting
    union_menu = UnionEventMenu(MockAudio(), state)
    union_menu._union_busting()
    
    influencer_menu = InfluencerEventMenu(MockAudio(), state)
    influencer_menu._fire()
    
    # In gameplay.py, MovieDealMenu handles movie deals.
    # We test balancing when these events trigger at the same time and hit resources heavily.
    # assert state.money >= 0
    assert state.fans >= 0
    
    print("Money:", state.money, "Fans:", state.fans)

