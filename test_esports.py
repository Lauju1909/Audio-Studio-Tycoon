import pytest
from logic import GameState
from models import GameProject, EsportsLeague
from menus.business import ESportsCreateLeagueMenu, ESportsChampionshipMenu, ESportsSponsorMenu

class DummyAudio:
    def speak(self, text, interrupt=False):
        pass
    def play_sound(self, sound):
        pass

@pytest.fixture
def state():
    s = GameState()
    s.money = 50_000_000
    s.fans = 100_000
    s.ui_context = {}
    return s

def test_esports_league_creation(state):
    game = GameProject("Multi Game", "Sport", "Action")
    game.sales = 1000000
    state.game_history.append(game)
    state.year = 2010

    menu = ESportsCreateLeagueMenu(DummyAudio(), state)
    menu.announce_entry()

    create_opt = next((o for o in menu.options if "Multi Game" in o['text']), None)
    assert create_opt is not None
    create_opt['action']()
    
    assert hasattr(state, 'esports_leagues')
    assert len(state.esports_leagues) == 1
    assert state.esports_leagues[0].game_name == "Multi Game"

def test_esports_championship(state):
    league = EsportsLeague("Multi Game", 1)
    league.hype = 100
    state.esports_leagues = [league]
    state.ui_context['selected_league_idx'] = 0
    state.year = 2010
    state.fans = 1000000

    menu = ESportsChampionshipMenu(DummyAudio(), state)
    menu.announce_entry()
    
    # Just grab any championship option (e.g. the first one which is Small)
    opt = menu.options[0]
    opt['action']()
    
    assert league.championships_held == 1
    assert league.hype > 100
    assert league.total_championship_income > 0

def test_esports_sponsor(state):
    league = EsportsLeague("Multi Game", 1)
    state.esports_leagues = [league]
    state.ui_context['selected_league_idx'] = 0

    menu = ESportsSponsorMenu(DummyAudio(), state)
    menu.announce_entry()

    # Find the global upgrade
    opt = next((o for o in menu.options if "global" in o['text'] or "Global" in o['text']), None)
    assert opt is not None

    opt['action']()
    assert league.sponsor_tier == "global"
