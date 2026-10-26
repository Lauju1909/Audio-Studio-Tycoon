"""Zugriffsfunktionen auf die Spieldaten."""
from data.core import *  # noqa: F401,F403
from data.content import *  # noqa: F401,F403
from data.people import *  # noqa: F401,F403
from data.studio import *  # noqa: F401,F403
from data.economy import *  # noqa: F401,F403
from data.events import *  # noqa: F401,F403
from data.meta import *  # noqa: F401,F403


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def get_compatibility(topic, genre):
    """Gibt Kompatibilitätswert (0-3) zurück."""
    if topic not in TOPIC_GENRE_COMPAT:
        return 1
    genre_index = GENRES.index(genre) if genre in GENRES else 0
    return TOPIC_GENRE_COMPAT[topic][genre_index]

def get_compatibility_text(value):
    """Beschreibender Text für Kompatibilitätswert."""
    texts = {
        0: "Schlechte Kombination",
        1: "Okay Kombination",
        2: "Gute Kombination",
        3: "Super Kombination",
    }
    return texts.get(value, "Unbekannt")

def get_ideal_sliders(genre):
    """Ideale Slider-Verteilung für ein Genre."""
    return GENRE_IDEAL_SLIDERS.get(genre, {s: 5 for s in SLIDER_NAMES})

def get_available_platforms(week):
    """Gibt Plattformen zurück, die in der aktuellen Woche verfügbar sind."""
    current_week = float(week)
    available = []
    for p in PLATFORMS:
        ay = p.get("unlock_year")
        ey = p.get("end_year")
        
        if ay is not None:
            start = (ay - START_YEAR) * WEEKS_PER_YEAR + 1
        else:
            start = 0.0
            
        if ey is not None:
            end = (ey - START_YEAR) * WEEKS_PER_YEAR + 1
        else:
            end = 99999.0
            
        if start <= current_week <= end:
            available.append(p)
    return available

def get_available_features(week):
    """Gibt Engine-Features zurück, die in der aktuellen Woche erforschbar sind."""
    current_week = int(week)
    result = []
    for f in ENGINE_FEATURES:
        if "unlock_year" in f:
            unlock_week = (f["unlock_year"] - START_YEAR) * WEEKS_PER_YEAR + 1
            if unlock_week <= current_week:
                result.append(f)
        elif "week" in f:
            if int(f["week"]) <= current_week:
                result.append(f)
    return result

def get_feature_unlock_week(feature):
    """Gibt die Spielwoche zurück, ab der ein Feature erforschbar ist."""
    if "unlock_year" in feature:
        return (feature["unlock_year"] - START_YEAR) * WEEKS_PER_YEAR + 1
    if "week" in feature:
        return int(feature["week"])
    return 1

def get_historical_topics_for_year(calendar_year):
    """Gibt alle historischen Themen zurück, die bis zum gegebenen Jahr verfügbar sind."""
    return [t for t in HISTORICAL_TOPICS if t["unlock_year"] <= calendar_year]

def get_newly_unlocked_topics(calendar_year):
    """Gibt alle Themen zurück, die GENAU in diesem Jahr neu verfügbar werden."""
    return [t for t in HISTORICAL_TOPICS if t["unlock_year"] == calendar_year]

def get_year_event(year):
    """Gibt das historische Ereignis für ein bestimmtes Jahr zurück."""
    return YEAR_EVENTS.get(year)
