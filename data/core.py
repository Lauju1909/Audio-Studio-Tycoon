"""
Statische Spieldaten für Audio Studio Tycoon - Audio Edition.

Enthält Themen, Genres, Kompatibilitätstabelle, Slider-Gewichtungen,
Plattformen, Engine-Features, Mitarbeiter-Daten und Zufallsereignisse.
"""

# ============================================================
# GLOBALE ZEITKONSTANTEN
# ============================================================
START_YEAR = 1930       # Das Spiel beginnt im Jahr 1930
WEEKS_PER_YEAR = 48     # 48 Wochen pro Spieljahr (historische Zeitachse)

# ============================================================
# LOKALISIERUNG & DIENSTE
# ============================================================
SUPPORTED_LANGUAGES = [
    {"id": "de", "name": "Deutsch", "market_multi": 1.0},
    {"id": "en", "name": "English", "market_multi": 1.2},
    {"id": "fr", "name": "Français", "market_multi": 0.3},
    {"id": "es", "name": "Español", "market_multi": 0.4},
    {"id": "it", "name": "Italiano", "market_multi": 0.2},
    {"id": "jp", "name": "Japanese", "market_multi": 0.5},
]
SUBSCRIPTION_UNLOCK_YEAR = 1995
