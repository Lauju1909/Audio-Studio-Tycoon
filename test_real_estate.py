from logic import GameState

class DummyAudio:
    def speak(self, text, interrupt=False): pass
    def play_sound(self, name): pass

def test_real_estate_manager():
    gs = GameState()
    gs.audio = DummyAudio()
    
    # Not unlocked yet
    gs.money = 10_000_000
    gs.week = 52 # Year 1981
    assert not gs.real_estate_manager.is_unlocked(gs)
    
    # Unlock by money
    gs.money = 51_000_000
    gs.money = 300_000_000 # Make sure we can afford any property
    assert gs.real_estate_manager.is_unlocked(gs)
    
    gs._on_new_week()
    assert len(gs.real_estate_manager.market_listings) == 3
    
    for _ in range(12):
        gs._on_new_week()
        
    assert len(gs.real_estate_manager.market_listings) > 0
    
    prop = gs.real_estate_manager.market_listings[0]
    prop.base_cost
    
    assert gs.real_estate_manager.buy_property(gs, 0)
    assert len(gs.real_estate_manager.owned_properties) == 1
    assert gs.real_estate_manager.active_property_index == 0
    
    # Check if buying perk works
    assert gs.real_estate_manager.buy_perk(gs, 0, "canteen")
    assert gs.real_estate_manager.owned_properties[0].has_canteen
    
    # Check serialization
    d = gs.real_estate_manager.to_dict()
    gs.real_estate_manager.from_dict(d)
    assert gs.real_estate_manager.owned_properties[0].has_canteen
    
    # Sell property
    assert gs.real_estate_manager.sell_property(gs, 0)
    assert len(gs.real_estate_manager.owned_properties) == 0
