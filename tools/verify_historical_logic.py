
import sys
import os

# Pfad zum Hauptverzeichnis hinzufügen
sys.path.append(os.getcwd())

from game_data import (
    get_historical_topics_for_year, get_available_features, 
    get_available_platforms, get_year_event,
    get_newly_unlocked_topics
)
from logic import GameState

def test_calendar():
    print("Testing Calendar Logic...")
    gs = GameState()
    
    # Week 1
    assert gs.get_calendar_year() == 1930, f"Expected 1930, got {gs.get_calendar_year()}"
    cal1 = gs.get_calendar_text()
    assert "1930" in cal1 and f"{gs.get_text('calendar_week')} 1" in cal1, f"Unexpected cal1: {cal1}"
    
    # Week 49 (Year 2)
    gs.week = 49
    assert gs.get_calendar_year() == 1931, f"Expected 1931, got {gs.get_calendar_year()}"
    cal49 = gs.get_calendar_text()
    assert "1931" in cal49 and f"{gs.get_text('calendar_week')} 1" in cal49, f"Unexpected cal49: {cal49}"
    
    # Week (48 * 2) + 1 = 97 (Year 3)
    gs.week = 97
    assert gs.get_calendar_year() == 1932, f"Expected 1932, got {gs.get_calendar_year()}"
    
    print("Calendar Logic: OK")

def test_topics():
    print("Testing Topic Logic...")
    
    # 1930 topics
    topics_1930 = get_historical_topics_for_year(1930)
    assert len(topics_1930) > 0, "No topics for 1930"
    topic_names = [t["name"] for t in topics_1930]
    assert "Abakus" in topic_names
    assert "Mathematik" in topic_names
    
    # Newly unlocked
    new_1969 = get_newly_unlocked_topics(1969)
    new_names_1969 = [t["name"] for t in new_1969]
    assert "Mondbasis" in new_names_1969, f"Mondbasis missing in 1969 unlocks: {new_names_1969}"
    
    # GameState initialization
    gs = GameState()
    assert "Abakus" in gs.unlocked_topics, "Abakus should be unlocked at start"
    assert "Mondbasis" not in gs.unlocked_topics, "Mondbasis should NOT be unlocked at start"
    
    print("Topic Logic: OK")

def test_features():
    print("Testing Engine Feature Logic...")
    
    # Week 1 (1930)
    features_w1 = get_available_features(1)
    f_names_w1 = [f["name"] for f in features_w1]
    assert "Papier-Logik" in f_names_w1
    assert "Vakuum-Röhren" not in f_names_w1
    
    # 1941 (Week 529 roughly)
    # (1941 - 1930) * 48 + 1 = 11 * 48 + 1 = 528 + 1 = 529
    features_1941 = get_available_features(529)
    f_names_1941 = [f["name"] for f in features_1941]
    assert "Vakuum-Röhren" in f_names_1941
    
    print("Engine Feature Logic: OK")

def test_platforms():
    print("Testing Platform Logic...")
    
    # Week 1 (1930)
    platforms_w1 = get_available_platforms(1)
    p_names_w1 = [p["name"] for p in platforms_w1]
    assert "Hand-Abakus" in p_names_w1
    assert "Atari 2600" not in p_names_w1
    
    # 1977 (Week 2257)
    platforms_1977 = get_available_platforms(2257)
    p_names_1977 = [p["name"] for p in platforms_1977]
    assert "Atari 2600" in p_names_1977
    
    print("Platform Logic: OK")

def test_events():
    print("Testing Historical Events...")
    from translations import get_text
    
    # 1930 event
    evt_1930 = get_year_event(1930)
    assert evt_1930 is not None
    assert "Billig-Logik" in get_text(evt_1930["text"])
    
    # 1969 event
    evt_1969 = get_year_event(1969)
    assert evt_1969 is not None
    assert "Apollo 11" in get_text(evt_1969["text"])
    
    print("Historical Events: OK")

if __name__ == "__main__":
    import traceback
    try:
        test_calendar()
        test_topics()
        test_features()
        test_platforms()
        test_events()
        print("\nALL HISTORICAL LOGIC TESTS PASSED!")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        traceback.print_exc()
        sys.exit(1)
        sys.exit(1)
