from logic import GameState
from menus.business import CloudGamingMenu

class DummyAudio:
    def speak(self, text, interrupt=False):
        pass
    def play_sound(self, file):
        pass

def test_cloud_gaming():
    gs = GameState()
    gs.audio = DummyAudio()
    gs.money = 20000000
    gs.hype = 50
    cg = gs.cloud_gaming
    assert not cg.active

    menu = CloudGamingMenu(DummyAudio(), gs)
    menu.on_enter()

    # Start service
    menu._start()
    assert cg.active
    assert cg.tech_level == 1

    # Process week
    gs._on_new_week()
    assert cg.subscribers > 0

    # Upgrade
    menu._upgrade()
    assert cg.tech_level == 2
    
    # Toggle
    menu._toggle()
    assert not cg.active

    # Price up
    menu._price_up()
    assert cg.price == 15.99

    # Price down
    menu._price_down()
    assert cg.price == 14.99
