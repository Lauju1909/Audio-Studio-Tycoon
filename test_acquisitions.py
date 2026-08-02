from logic import GameState
from models import RivalStudio

class DummyAudio:
    def speak(self, text, interrupt=False):
        pass
    def play_sound(self, name):
        pass

def test_acquisitions():
    gs = GameState()
    gs.audio = DummyAudio()
    gs.money = 1000000000
    gs.rivals = [RivalStudio("TestRival", target_market_share=10, owned_shares=0)]
    
    # Test Buy Shares
    res, info = gs.buy_shares(0)
    assert res == True
    assert info == 10
    assert gs.rivals[0].owned_shares == 10
    
    # Test Max Shares limit
    gs.rivals[0].owned_shares = 50
    res, info = gs.buy_shares(0)
    assert res == False
    assert info == "max_shares"
    
    # Test M&A Buyout
    from menus.business import AcquisitionMenu
    menu = AcquisitionMenu(gs.audio, gs)
    menu.announce_entry()
    
    # It should have the option to buy out the remaining 50%
    # The cost is (100 - 50) * 50000 = 2500000
    res = menu.acquire_studio(0, 2500000)
    assert res == "bank_menu"
    assert gs.rivals[0].is_owned_by_player == True
    assert gs.rivals[0].owned_shares == 100
