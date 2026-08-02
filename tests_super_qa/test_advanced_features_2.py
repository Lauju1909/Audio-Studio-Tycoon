from game_data import get_available_platforms

def test_balancing_absolute_years():
    from game_data import START_YEAR
    # In 1971, Week 48
    # Test absolute week based on (1971 - START_YEAR) * 48 + 48
    platforms_absolute = get_available_platforms((1971 - START_YEAR) * 48 + 48)
    names_abs = [p['name'] for p in platforms_absolute]
    
    assert 'IBM 360' in names_abs, "Platform 'IBM 360' expected in 1971 (Woche 48) absolute check but not found."
