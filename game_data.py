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

# ============================================================
# THEMEN (Topics) - 20 verschiedene
# ============================================================
START_TOPICS = [
    "Fantasy",
    "Sci-Fi",
    "Mittelalter",
    "Sport",
    "Rennen",
]

RESEARCHABLE_TOPICS = [
    {"name": "Abakus", "cost": 5000, "unlock_year": 1930, "research_weeks": 2},
    {"name": "Radio-Drama", "cost": 4500, "unlock_year": 1930, "research_weeks": 2},
    {"name": "Stummfilm", "cost": 4500, "unlock_year": 1930, "research_weeks": 2},
    {"name": "Logistik", "cost": 5000, "unlock_year": 1930, "research_weeks": 2},
    {"name": "Schach", "cost": 5000, "unlock_year": 1930, "research_weeks": 2},
    {"name": "Mathematik", "cost": 5000, "unlock_year": 1930, "research_weeks": 2},
    {"name": "Prohibition", "cost": 4800, "unlock_year": 1931, "research_weeks": 2},
    {"name": "Swing-Musik", "cost": 4800, "unlock_year": 1931, "research_weeks": 2},
    {"name": "Astronomie", "cost": 5500, "unlock_year": 1931, "research_weeks": 2},
    {"name": "Landwirtschaft", "cost": 5500, "unlock_year": 1931, "research_weeks": 2},
    {"name": "Kochen", "cost": 6000, "unlock_year": 1932, "research_weeks": 2},
    {"name": "Politik", "cost": 6000, "unlock_year": 1932, "research_weeks": 2},
    {"name": "Detektiv", "cost": 6500, "unlock_year": 1933, "research_weeks": 2},
    {"name": "Kartenspiele", "cost": 6500, "unlock_year": 1933, "research_weeks": 2},
    {"name": "Architektur", "cost": 7000, "unlock_year": 1934, "research_weeks": 2},
    {"name": "Postwesen", "cost": 7000, "unlock_year": 1934, "research_weeks": 2},
    {"name": "Zirkus", "cost": 7500, "unlock_year": 1935, "research_weeks": 2},
    {"name": "Propaganda", "cost": 5200, "unlock_year": 1935, "research_weeks": 2},
    {"name": "Widerstand", "cost": 5200, "unlock_year": 1935, "research_weeks": 2},
    {"name": "Bergbau", "cost": 7500, "unlock_year": 1935, "research_weeks": 2},
    {"name": "Eisenbahn", "cost": 8000, "unlock_year": 1936, "research_weeks": 2},
    {"name": "Seefahrt", "cost": 8000, "unlock_year": 1936, "research_weeks": 2},
    {"name": "Feuerwehr", "cost": 8500, "unlock_year": 1937, "research_weeks": 2},
    {"name": "Kryptografie", "cost": 8500, "unlock_year": 1937, "research_weeks": 2},
    {"name": "Mars-Invasion", "cost": 9000, "unlock_year": 1938, "research_weeks": 2},
    {"name": "Radar-Technik", "cost": 5800, "unlock_year": 1939, "research_weeks": 2},
    {"name": "Zauberei", "cost": 9000, "unlock_year": 1938, "research_weeks": 2},
    {"name": "Militär", "cost": 9500, "unlock_year": 1939, "research_weeks": 2},
    {"name": "Chemie", "cost": 9500, "unlock_year": 1939, "research_weeks": 2},
    {"name": "U-Boot", "cost": 10000, "unlock_year": 1940, "research_weeks": 2},
    {"name": "Luftschlacht", "cost": 10500, "unlock_year": 1941, "research_weeks": 2},
    {"name": "Spionage", "cost": 11000, "unlock_year": 1942, "research_weeks": 2},
    {"name": "Panzer", "cost": 11500, "unlock_year": 1943, "research_weeks": 2},
    {"name": "Fallschirmjäger", "cost": 12000, "unlock_year": 1944, "research_weeks": 2},
    {"name": "Wiederaufbau", "cost": 12500, "unlock_year": 1945, "research_weeks": 2},
    {"name": "Journalismus", "cost": 13000, "unlock_year": 1946, "research_weeks": 2},
    {"name": "UFOs", "cost": 13500, "unlock_year": 1947, "research_weeks": 2},
    {"name": "Roboter", "cost": 14000, "unlock_year": 1948, "research_weeks": 2},
    {"name": "Dschungel", "cost": 14500, "unlock_year": 1949, "research_weeks": 2},
    {"name": "Rock 'n' Roll", "cost": 14800, "unlock_year": 1950, "research_weeks": 2},
    {"name": "Petticoat", "cost": 6500, "unlock_year": 1950, "research_weeks": 2},
    {"name": "UFO-Fieber", "cost": 6800, "unlock_year": 1951, "research_weeks": 2},
    {"name": "Archäologie", "cost": 15000, "unlock_year": 1950, "research_weeks": 2},
    {"name": "Weltraum", "cost": 15500, "unlock_year": 1951, "research_weeks": 2},
    {"name": "Wilder Westen", "cost": 16000, "unlock_year": 1952, "research_weeks": 2},
    {"name": "Bergsteigen", "cost": 16500, "unlock_year": 1953, "research_weeks": 2},
    {"name": "Fussball", "cost": 17000, "unlock_year": 1954, "research_weeks": 2},
    {"name": "Vergnügungspark", "cost": 17500, "unlock_year": 1955, "research_weeks": 2},
    {"name": "Monster", "cost": 18000, "unlock_year": 1956, "research_weeks": 2},
    {"name": "Satelliten", "cost": 18500, "unlock_year": 1957, "research_weeks": 2},
    {"name": "Tennis", "cost": 19000, "unlock_year": 1958, "research_weeks": 2},
    {"name": "Rennwagen", "cost": 19500, "unlock_year": 1959, "research_weeks": 2},
    {"name": "Tiefsee", "cost": 20000, "unlock_year": 1960, "research_weeks": 2},
    {"name": "Mafia", "cost": 20500, "unlock_year": 1961, "research_weeks": 2},
    {"name": "Fantasy", "cost": 21000, "unlock_year": 1962, "research_weeks": 2},
    {"name": "Agenten", "cost": 21500, "unlock_year": 1963, "research_weeks": 2},
    {"name": "Popstars", "cost": 22000, "unlock_year": 1964, "research_weeks": 2},
    {"name": "Dinosaurier", "cost": 22500, "unlock_year": 1965, "research_weeks": 2},
    {"name": "Ninjas", "cost": 23000, "unlock_year": 1966, "research_weeks": 2},
    {"name": "Flower Power", "cost": 23200, "unlock_year": 1967, "research_weeks": 2},
    {"name": "Hippies", "cost": 23500, "unlock_year": 1967, "research_weeks": 2},
    {"name": "Heavy Metal", "cost": 23800, "unlock_year": 1970, "research_weeks": 2},
    {"name": "Weltrevolution", "cost": 24000, "unlock_year": 1968, "research_weeks": 2},
    {"name": "Mondbasis", "cost": 24500, "unlock_year": 1969, "research_weeks": 2},
    {"name": "Kung-Fu", "cost": 25000, "unlock_year": 1970, "research_weeks": 2},
    {"name": "Piraten", "cost": 25500, "unlock_year": 1971, "research_weeks": 2},
    {"name": "Hip Hop", "cost": 25800, "unlock_year": 1973, "research_weeks": 2},
    {"name": "Basketball", "cost": 26000, "unlock_year": 1972, "research_weeks": 2},
    {"name": "Motorrad", "cost": 26500, "unlock_year": 1973, "research_weeks": 2},
    {"name": "Verliese", "cost": 27000, "unlock_year": 1974, "research_weeks": 2},
    {"name": "Polizei", "cost": 27500, "unlock_year": 1975, "research_weeks": 2},
    {"name": "Alien-Jagd", "cost": 28000, "unlock_year": 1976, "research_weeks": 2},
    {"name": "Laserschwert", "cost": 28500, "unlock_year": 1977, "research_weeks": 2},
    {"name": "Techno", "cost": 28800, "unlock_year": 1988, "research_weeks": 2},
    {"name": "Invaders", "cost": 29000, "unlock_year": 1978, "research_weeks": 2},
    {"name": "Horrorhaus", "cost": 29500, "unlock_year": 1979, "research_weeks": 2},
    {"name": "Gelbe Fresspunkte", "cost": 30000, "unlock_year": 1980, "research_weeks": 2},
    {"name": "Büro-Alltag", "cost": 30500, "unlock_year": 1981, "research_weeks": 2},
    {"name": "Cyberpunk", "cost": 31000, "unlock_year": 1982, "research_weeks": 2},
    {"name": "Vampire", "cost": 31500, "unlock_year": 1983, "research_weeks": 2},
    {"name": "Breakdance", "cost": 32000, "unlock_year": 1984, "research_weeks": 2},
    {"name": "Klempner", "cost": 32500, "unlock_year": 1985, "research_weeks": 2},
    {"name": "Postapokalypse", "cost": 33000, "unlock_year": 1986, "research_weeks": 2},
    {"name": "Mechs", "cost": 33500, "unlock_year": 1987, "research_weeks": 2},
    {"name": "Grunge", "cost": 33800, "unlock_year": 1991, "research_weeks": 2},
    {"name": "Skateboarding", "cost": 34000, "unlock_year": 1988, "research_weeks": 2},
    {"name": "Taschenmonster", "cost": 34500, "unlock_year": 1996, "research_weeks": 2},
    {"name": "Krankenhaus", "cost": 35000, "unlock_year": 1990, "research_weeks": 2},
    {"name": "Freizeitpark", "cost": 35500, "unlock_year": 1991, "research_weeks": 2},
    {"name": "Mars-Shooter", "cost": 36000, "unlock_year": 1992, "research_weeks": 2},
    {"name": "Urzeit/Survival", "cost": 36500, "unlock_year": 1993, "research_weeks": 2},
    {"name": "Anime", "cost": 37000, "unlock_year": 1994, "research_weeks": 2},
    {"name": "Hacking", "cost": 37500, "unlock_year": 1995, "research_weeks": 2},
    {"name": "Stealth-Agent", "cost": 38000, "unlock_year": 1996, "research_weeks": 2},
    {"name": "Elfen & Orks", "cost": 38500, "unlock_year": 1997, "research_weeks": 2},
    {"name": "Survival-Insel", "cost": 39000, "unlock_year": 1998, "research_weeks": 2},
    {"name": "Skandal-TV", "cost": 39500, "unlock_year": 1999, "research_weeks": 2},
    {"name": "Lebens-Sim", "cost": 40000, "unlock_year": 2000, "research_weeks": 2},
    {"name": "Zombie-Hype", "cost": 40500, "unlock_year": 2001, "research_weeks": 2},
    {"name": "Parkplatz-Manager", "cost": 41000, "unlock_year": 2002, "research_weeks": 2},
    {"name": "Cloud Computing", "cost": 41200, "unlock_year": 2006, "research_weeks": 2},
    {"name": "E-Sport", "cost": 41500, "unlock_year": 2003, "research_weeks": 2},
    {"name": "Zauberschule", "cost": 42000, "unlock_year": 2004, "research_weeks": 2},
    {"name": "Sandbox/Voxel", "cost": 42500, "unlock_year": 2005, "research_weeks": 2},
    {"name": "Wikinger", "cost": 43000, "unlock_year": 2006, "research_weeks": 2},
    {"name": "Smartphones", "cost": 43500, "unlock_year": 2007, "research_weeks": 2},
    {"name": "Freerunning", "cost": 44000, "unlock_year": 2008, "research_weeks": 2},
    {"name": "Block-Bauen", "cost": 44500, "unlock_year": 2009, "research_weeks": 2},
    {"name": "Social Networking", "cost": 45000, "unlock_year": 2010, "research_weeks": 2},
    {"name": "Indie-Entwickler", "cost": 45500, "unlock_year": 2011, "research_weeks": 2},
    {"name": "Battle-Royale", "cost": 46000, "unlock_year": 2012, "research_weeks": 2},
    {"name": "VR-Simulation", "cost": 46500, "unlock_year": 2013, "research_weeks": 2},
    {"name": "Farming-Hype", "cost": 47000, "unlock_year": 2014, "research_weeks": 2},
    {"name": "Cyber-Krieg", "cost": 47500, "unlock_year": 2015, "research_weeks": 2},
    {"name": "AR-Jagd", "cost": 48000, "unlock_year": 2016, "research_weeks": 2},
    {"name": "Krypto-Mining", "cost": 48500, "unlock_year": 2017, "research_weeks": 2},
    {"name": "Mars-Kolonisierung", "cost": 49000, "unlock_year": 2018, "research_weeks": 2},
    {"name": "Streaming-Star", "cost": 49500, "unlock_year": 2019, "research_weeks": 2},
    {"name": "KI-Dystopie", "cost": 50000, "unlock_year": 2020, "research_weeks": 2},
    {"name": "NFT-Sammeln", "cost": 50500, "unlock_year": 2021, "research_weeks": 2},
    {"name": "Metaverse", "cost": 51000, "unlock_year": 2022, "research_weeks": 2},
    {"name": "KI-Utopie", "cost": 51500, "unlock_year": 2023, "research_weeks": 2},
    {"name": "Endzeit-Bote", "cost": 52000, "unlock_year": 2024, "research_weeks": 2},
    {"name": "Gen-Labor", "cost": 52500, "unlock_year": 2025, "research_weeks": 2},
    {"name": "Neural-Link", "cost": 53000, "unlock_year": 2026, "research_weeks": 2},
    {"name": "KI-Ethik", "cost": 54000, "unlock_year": 2028, "research_weeks": 3},
    {"name": "Mars-Tourismus", "cost": 55000, "unlock_year": 2030, "research_weeks": 3},
    {"name": "Deep-Sea Mining", "cost": 56000, "unlock_year": 2032, "research_weeks": 3},
    {"name": "Quanten-Hacking", "cost": 58000, "unlock_year": 2035, "research_weeks": 4},
    {"name": "Galaktisches Imperium", "cost": 60000, "unlock_year": 2040, "research_weeks": 5},
    {"name": "Zeitreisen-Paradox", "cost": 65000, "unlock_year": 2045, "research_weeks": 5},

]



TOPICS = START_TOPICS + [t["name"] for t in RESEARCHABLE_TOPICS]

# ============================================================
# PHASE B: LIZENZEN (Für Marketing / Hype-Boosts)
# ============================================================
LICENSES = [
    # Kleine Lizenzen (Günstig, kleiner Boost)
    {"name": "Lokaler Buch-Bestseller", "base_cost": 50000, "hype_bonus": 15, "fan_bonus": 500},
    {"name": "Indie-Comic-Reihe", "base_cost": 80000, "hype_bonus": 20, "fan_bonus": 800},
    {"name": "Kultobjekt der 80er", "base_cost": 150000, "hype_bonus": 30, "fan_bonus": 1500},
    
    # Mittlere Lizenzen (Filme, TV)
    {"name": "TV-Krimi-Serie", "base_cost": 350000, "hype_bonus": 45, "fan_bonus": 3000},
    {"name": "Anime-Hit", "base_cost": 500000, "hype_bonus": 60, "fan_bonus": 5000},
    {"name": "Brettspiel-Klassiker", "base_cost": 650000, "hype_bonus": 75, "fan_bonus": 7500},

    # Große Lizenzen (Weltweite Blockbuster)
    {"name": "Fantasy-Buch-Epos", "base_cost": 1200000, "hype_bonus": 100, "fan_bonus": 15000},
    {"name": "Weltraum-Film-Franchise", "base_cost": 2500000, "hype_bonus": 140, "fan_bonus": 35000},
    {"name": "Offizielle Sport-Liga (Fußball)", "base_cost": 5000000, "hype_bonus": 200, "fan_bonus": 80000},
    {"name": "Superhelden-Universum", "base_cost": 8000000, "hype_bonus": 250, "fan_bonus": 150000},
]

# ============================================================
# PHASE B: ADDON & BUNDLE DATEN
# ============================================================
ADDON_DATA = {
    "cost_multi": 0.4,       # Addons kosten nur 40% eines neuen Spiels
    "time_multi": 0.3,       # Addons dauern nur 30% so lange in der Entwicklung
    "sales_boost": 1.5,      # Boosting von Base Game Sales um 50%
}

BUNDLE_DATA = {
    "min_games": 2,          # Min. Anzahl Spiele in einem Bundle
    "max_games": 4,          # Max. Anzahl Spiele
    "base_price": 25,        # Bundle-Preis
    "revenue_mod": 0.05,     # Wie viel extra Revenue ein Bundle macht
}

# ============================================================
# GENRES - 8 verschiedene
# ============================================================
GENRES = [
    "Action",
    "RPG",
    "Simulation",
    "Strategie",
    "Abenteuer",
    "Puzzle",
    "Sport",
    "Casual",
    "Horror",
    "Kampfspiel",
    "Rennspiel",
]

START_GENRES = ["Action", "Puzzle", "Casual"]

RESEARCHABLE_GENRES = [
    {"name": "RPG", "cost": 15000, "unlock_year": 1930, "research_weeks": 4},
    {"name": "Simulation", "cost": 10000, "unlock_year": 1930, "research_weeks": 3},
    {"name": "Strategie", "cost": 12000, "unlock_year": 1930, "research_weeks": 3},
    {"name": "Abenteuer", "cost": 15000, "unlock_year": 1930, "research_weeks": 4},
    {"name": "Sport", "cost": 8000, "unlock_year": 1930, "research_weeks": 2},
    {"name": "Horror", "cost": 20000, "unlock_year": 1930, "research_weeks": 5},
    {"name": "Kampfspiel", "cost": 18000, "unlock_year": 1930, "research_weeks": 4},
    {"name": "Rennspiel", "cost": 10000, "unlock_year": 1930, "research_weeks": 3},
]

# ============================================================
# SLIDER-NAMEN (6 Slider für die Entwicklungsphase)
# ============================================================
SLIDER_NAMES = [
    "Gameplay",
    "Grafik",
    "Sound",
    "Story",
    "KI",
    "Welt",
]

# ============================================================
# IDEALE SLIDER-VERTEILUNG pro Genre
# ============================================================
GENRE_IDEAL_SLIDERS = {
    "Action": {
        "Gameplay": 9, "Grafik": 7, "Sound": 5, "Story": 2, "KI": 3, "Welt": 4,
    },
    "RPG": {
        "Gameplay": 6, "Grafik": 5, "Sound": 4, "Story": 9, "KI": 4, "Welt": 8,
    },
    "Simulation": {
        "Gameplay": 8, "Grafik": 4, "Sound": 3, "Story": 2, "KI": 7, "Welt": 6,
    },
    "Strategie": {
        "Gameplay": 7, "Grafik": 3, "Sound": 3, "Story": 4, "KI": 9, "Welt": 6,
    },
    "Abenteuer": {
        "Gameplay": 5, "Grafik": 6, "Sound": 6, "Story": 9, "KI": 3, "Welt": 7,
    },
    "Puzzle": {
        "Gameplay": 9, "Grafik": 4, "Sound": 5, "Story": 1, "KI": 5, "Welt": 2,
    },
    "Sport": {
        "Gameplay": 8, "Grafik": 7, "Sound": 5, "Story": 1, "KI": 6, "Welt": 3,
    },
    "Casual": {
        "Gameplay": 8, "Grafik": 5, "Sound": 6, "Story": 1, "KI": 3, "Welt": 3,
    },
    "Horror": {
        "Gameplay": 7, "Grafik": 8, "Sound": 9, "Story": 7, "KI": 4, "Welt": 6,
    },
    "Kampfspiel": {
        "Gameplay": 9, "Grafik": 7, "Sound": 6, "Story": 2, "KI": 7, "Welt": 3,
    },
    "Rennspiel": {
        "Gameplay": 8, "Grafik": 8, "Sound": 6, "Story": 1, "KI": 6, "Welt": 5,
    },
}

# ============================================================
# THEMA/GENRE KOMPATIBILITÄT
# 3 = Super, 2 = Gut, 1 = Okay, 0 = Schlecht
# ============================================================
TOPIC_GENRE_COMPAT = {
    "Abakus":[ 0,  0,  2,  1,  1,  1,  0,  0,  3,  0,  0],
    "Logistik":[ 0,  1,  1,  0,  1,  3,  1,  3,  2,  0,  1],
    "Schach":[ 3,  2,  2,  1,  1,  2,  0,  0,  3,  0,  2],
    "Mathematik":[ 2,  2,  0,  3,  0,  3,  0,  2,  2,  1,  0],
    "Astronomie":[ 0,  1,  2,  0,  1,  0,  3,  2,  3,  2,  1],
    "Landwirtschaft":[ 2,  2,  1,  2,  0,  1,  1,  1,  3,  3,  2],
    "Kochen":[ 1,  2,  0,  1,  0,  2,  3,  2,  0,  1,  2],
    "Politik":[ 1,  3,  3,  3,  1,  2,  1,  1,  2,  3,  3],
    "Detektiv":[ 2,  1,  1,  3,  0,  0,  0,  1,  1,  3,  0],
    "Kartenspiele":[ 3,  3,  3,  2,  0,  0,  2,  2,  0,  2,  3],
    "Architektur":[ 1,  3,  0,  2,  1,  0,  2,  1,  1,  2,  1],
    "Postwesen":[ 0,  2,  3,  0,  0,  2,  2,  1,  0,  1,  0],
    "Zirkus":[ 0,  3,  0,  1,  1,  3,  1,  2,  3,  1,  1],
    "Bergbau":[ 2,  3,  2,  3,  3,  0,  1,  1,  0,  2,  0],
    "Eisenbahn":[ 1,  1,  0,  0,  0,  1,  0,  0,  2,  0,  1],
    "Seefahrt":[ 2,  3,  1,  1,  3,  1,  3,  3,  1,  0,  0],
    "Feuerwehr":[ 3,  2,  3,  3,  3,  0,  0,  0,  3,  2,  0],
    "Kryptografie":[ 1,  1,  1,  3,  1,  3,  1,  2,  3,  1,  0],
    "Mars-Invasion":[ 3,  0,  0,  0,  0,  1,  1,  3,  3,  3,  1],
    "Zauberei":[ 3,  0,  1,  3,  0,  3,  2,  3,  2,  3,  3],
    "Militär":[ 1,  1,  2,  1,  0,  0,  2,  0,  0,  3,  1],
    "Chemie":[ 0,  0,  1,  0,  0,  1,  3,  0,  1,  0,  0],
    "U-Boot":[ 3,  2,  2,  1,  2,  1,  2,  3,  1,  2,  3],
    "Luftschlacht":[ 2,  0,  0,  3,  0,  0,  1,  2,  1,  2,  0],
    "Spionage":[ 1,  2,  2,  1,  3,  2,  0,  2,  0,  1,  2],
    "Panzer":[ 0,  0,  1,  2,  2,  1,  2,  1,  2,  3,  2],
    "Fallschirmjäger":[ 0,  0,  3,  2,  0,  0,  2,  1,  2,  1,  3],
    "Wiederaufbau":[ 3,  0,  0,  0,  1,  0,  2,  1,  3,  1,  0],
    "Journalismus":[ 2,  2,  0,  2,  1,  1,  0,  2,  3,  1,  1],
    "UFOs":[ 1,  1,  3,  0,  1,  2,  3,  1,  2,  1,  0],
    "Roboter":[ 3,  0,  3,  1,  1,  3,  2,  2,  1,  1,  0],
    "Dschungel":[ 1,  3,  2,  2,  0,  2,  2,  3,  2,  0,  0],
    "Archäologie":[ 2,  1,  2,  0,  0,  3,  2,  2,  3,  0,  3],
    "Weltraum":[ 1,  2,  0,  3,  0,  1,  2,  3,  0,  2,  2],
    "Wilder Westen":[ 0,  2,  2,  3,  2,  3,  2,  1,  1,  3,  3],
    "Bergsteigen":[ 1,  2,  3,  0,  2,  2,  1,  3,  2,  3,  3],
    "Fussball":[ 3,  1,  3,  1,  0,  2,  2,  0,  1,  2,  1],
    "Vergnügungspark":[ 1,  1,  0,  0,  1,  3,  0,  3,  3,  1,  3],
    "Monster":[ 3,  3,  1,  1,  0,  0,  3,  1,  1,  3,  0],
    "Satelliten":[ 1,  0,  3,  1,  3,  2,  3,  3,  3,  1,  3],
    "Tennis":[ 3,  2,  1,  2,  3,  1,  2,  3,  0,  2,  1],
    "Rennwagen":[ 2,  2,  2,  0,  1,  1,  1,  3,  1,  1,  0],
    "Tiefsee":[ 3,  3,  2,  3,  3,  0,  1,  3,  3,  0,  3],
    "Mafia":[ 3,  0,  2,  2,  3,  3,  1,  3,  1,  2,  3],
    "Fantasy":[ 3,  0,  3,  2,  3,  1,  3,  1,  0,  3,  0],
    "Agenten":[ 0,  3,  1,  3,  1,  0,  2,  3,  2,  1,  3],
    "Popstars":[ 2,  2,  3,  2,  3,  2,  0,  3,  0,  0,  2],
    "Dinosaurier":[ 1,  0,  0,  0,  1,  1,  0,  1,  1,  1,  3],
    "Ninjas":[ 0,  1,  3,  2,  2,  1,  0,  1,  2,  0,  0],
    "Hippies":[ 2,  3,  3,  1,  0,  1,  0,  2,  0,  0,  2],
    "Weltrevolution":[ 3,  2,  0,  2,  0,  3,  3,  0,  3,  2,  3],
    "Mondbasis":[ 1,  3,  1,  2,  3,  3,  3,  2,  2,  1,  0],
    "Kung-Fu":[ 2,  3,  1,  3,  3,  2,  0,  3,  2,  1,  3],
    "Piraten":[ 1,  2,  2,  2,  2,  2,  0,  1,  0,  1,  3],
    "Basketball":[ 3,  1,  3,  3,  3,  0,  0,  2,  1,  3,  1],
    "Motorrad":[ 2,  2,  3,  2,  3,  2,  2,  3,  2,  2,  2],
    "Verliese":[ 1,  0,  1,  2,  0,  1,  1,  1,  3,  2,  2],
    "Polizei":[ 0,  1,  2,  1,  2,  1,  2,  0,  1,  2,  0],
    "Alien-Jagd":[ 0,  2,  1,  3,  0,  0,  2,  3,  3,  3,  2],
    "Laserschwert":[ 1,  0,  2,  3,  0,  0,  3,  3,  0,  0,  1],
    "Invaders":[ 1,  2,  0,  1,  0,  3,  1,  3,  3,  3,  2],
    "Horrorhaus":[ 3,  2,  0,  0,  1,  1,  2,  0,  1,  1,  1],
    "Gelbe Fresspunkte":[ 0,  1,  0,  3,  3,  3,  2,  0,  1,  2,  2],
    "Büro-Alltag":[ 3,  0,  1,  2,  1,  3,  0,  1,  1,  2,  1],
    "Cyberpunk":[ 0,  0,  1,  2,  2,  3,  0,  3,  2,  3,  2],
    "Vampire":[ 3,  3,  0,  0,  3,  2,  2,  0,  0,  1,  0],
    "Breakdance":[ 2,  0,  1,  3,  3,  2,  1,  3,  3,  0,  3],
    "Klempner":[ 2,  3,  2,  2,  0,  1,  2,  3,  3,  2,  3],
    "Postapokalypse":[ 0,  3,  0,  2,  2,  2,  0,  3,  0,  3,  3],
    "Mechs":[ 0,  1,  2,  3,  3,  0,  1,  2,  1,  2,  3],
    "Skateboarding":[ 3,  0,  0,  1,  1,  2,  0,  3,  0,  1,  0],
    "Taschenmonster":[ 3,  0,  1,  3,  2,  2,  3,  3,  3,  1,  3],
    "Krankenhaus":[ 1,  3,  1,  1,  0,  2,  3,  2,  2,  0,  2],
    "Freizeitpark":[ 2,  3,  1,  3,  3,  2,  2,  3,  3,  2,  1],
    "Mars-Shooter":[ 1,  3,  1,  3,  0,  2,  3,  3,  3,  1,  3],
    "Urzeit/Survival":[ 0,  1,  2,  0,  3,  0,  3,  0,  1,  3,  1],
    "Anime":[ 0,  3,  2,  2,  3,  0,  2,  3,  2,  3,  0],
    "Hacking":[ 0,  1,  2,  1,  0,  3,  0,  0,  3,  1,  2],
    "Stealth-Agent":[ 0,  0,  2,  0,  2,  2,  2,  3,  1,  1,  3],
    "Elfen & Orks":[ 1,  1,  1,  0,  3,  1,  3,  1,  1,  3,  2],
    "Survival-Insel":[ 3,  2,  0,  3,  2,  1,  0,  3,  2,  2,  3],
    "Skandal-TV":[ 2,  3,  2,  1,  3,  3,  0,  1,  3,  2,  2],
    "Lebens-Sim":[ 2,  0,  3,  2,  0,  0,  3,  2,  1,  2,  1],
    "Zombie-Hype":[ 1,  2,  1,  0,  0,  2,  3,  0,  2,  1,  0],
    "Parkplatz-Manager":[ 2,  2,  3,  1,  1,  1,  2,  2,  1,  2,  3],
    "E-Sport":[ 2,  2,  0,  3,  0,  1,  1,  3,  2,  0,  3],
    "Zauberschule":[ 0,  2,  0,  3,  2,  2,  3,  2,  0,  1,  3],
    "Sandbox/Voxel":[ 0,  2,  1,  0,  3,  2,  3,  0,  1,  0,  0],
    "Wikinger":[ 2,  3,  0,  0,  1,  1,  3,  3,  2,  3,  1],
    "Smartphones":[ 3,  0,  3,  3,  2,  0,  2,  1,  3,  3,  1],
    "Freerunning":[ 2,  0,  2,  2,  0,  3,  2,  1,  0,  3,  0],
    "Block-Bauen":[ 1,  0,  0,  2,  1,  1,  1,  0,  1,  1,  1],
    "Social Networking":[ 2,  1,  0,  2,  1,  1,  2,  1,  0,  0,  1],
    "Indie-Entwickler":[ 0,  2,  1,  2,  0,  1,  2,  0,  1,  3,  0],
    "Battle-Royale":[ 0,  3,  3,  2,  0,  3,  1,  0,  2,  3,  0],
    "VR-Simulation":[ 0,  3,  3,  3,  0,  3,  3,  0,  0,  2,  1],
    "Farming-Hype":[ 0,  1,  2,  2,  3,  2,  3,  3,  0,  0,  1],
    "Cyber-Krieg":[ 3,  3,  1,  3,  2,  3,  3,  3,  0,  2,  3],
    "AR-Jagd":[ 2,  2,  2,  1,  3,  0,  0,  0,  0,  3,  0],
    "Krypto-Mining":[ 2,  1,  0,  2,  0,  3,  2,  3,  0,  2,  2],
    "Mars-Kolonisierung":[ 2,  0,  1,  1,  3,  1,  0,  2,  2,  0,  2],
    "Streaming-Star":[ 1,  3,  0,  2,  0,  1,  2,  2,  2,  2,  0],
    "KI-Dystopie":[ 1,  1,  3,  0,  1,  0,  0,  1,  3,  3,  3],
    "NFT-Sammeln":[ 2,  1,  2,  2,  2,  0,  0,  1,  1,  0,  0],
    "Metaverse":[ 2,  3,  3,  3,  3,  3,  2,  1,  0,  2,  3],
    "KI-Utopie":[ 0,  2,  3,  2,  0,  1,  3,  0,  0,  1,  2],
    "Endzeit-Bote":[ 1,  1,  2,  2,  2,  0,  0,  3,  3,  1,  1],
    "Gen-Labor":[ 3,  1,  2,  0,  3,  0,  3,  0,  3,  0,  2],
    "Neural-Link":[ 3,  3,  3,  2,  0,  3,  0,  2,  1,  3,  2],
}



# ============================================================
# PLATTFORMEN
# name, Lizenzgebühr, Markt-Multiplikator, verfügbar ab Woche, Ende Woche (None = nie), Typ
# ============================================================
PLATFORMS = [
    {"name": "Hand-Abakus", "license_fee": 10000, "market_multi": 1.0, "unlock_year": 1930, "end_year": 1940, "type": "Konsole"},
    {"name": "Zuse Z1", "license_fee": 10000, "market_multi": 1.0, "unlock_year": 1935, "end_year": 1945, "type": "Konsole"},
    {"name": "Zuse Z3", "license_fee": 16000, "market_multi": 1.6, "unlock_year": 1941, "end_year": 1951, "type": "Konsole"},
    {"name": "ENIAC", "license_fee": 0, "market_multi": 2.4, "unlock_year": 1946, "end_year": 1956, "type": "Heimcomputer"},
    {"name": "UNIVAC I", "license_fee": 0, "market_multi": 3.1, "unlock_year": 1951, "end_year": 1961, "type": "Heimcomputer"},
    {"name": "Nimrod", "license_fee": 31000, "market_multi": 3.1, "unlock_year": 1951, "end_year": 1961, "type": "Konsole"},
    {"name": "EDSAC (OXO)", "license_fee": 0, "market_multi": 3.3, "unlock_year": 1952, "end_year": 1962, "type": "Heimcomputer"},
    {"name": "PDP-1 (Spacewar)", "license_fee": 45000, "market_multi": 4.5, "unlock_year": 1960, "end_year": 1970, "type": "Konsole"},
    {"name": "IBM 360", "license_fee": 0, "market_multi": 5.2, "unlock_year": 1965, "end_year": 1975, "type": "Heimcomputer"},
    {"name": "Magnavox Odyssey", "license_fee": 63000, "market_multi": 6.3, "unlock_year": 1972, "end_year": 1982, "type": "Konsole"},
    {"name": "Fairchild Ch. F", "license_fee": 69000, "market_multi": 6.9, "unlock_year": 1976, "end_year": 1986, "type": "Konsole"},
    {"name": "Atari 2600", "license_fee": 70000, "market_multi": 7.0, "unlock_year": 1977, "end_year": 1987, "type": "Konsole"},
    {"name": "Commodore PET", "license_fee": 0, "market_multi": 6.5, "unlock_year": 1977, "end_year": 1987, "type": "Heimcomputer"},
    {"name": "Apple II", "license_fee": 0, "market_multi": 6.8, "unlock_year": 1977, "end_year": 1987, "type": "Heimcomputer"},
    {"name": "Bally Astrocade", "license_fee": 72000, "market_multi": 7.2, "unlock_year": 1978, "end_year": 1988, "type": "Konsole"},
    {"name": "C64", "license_fee": 0, "market_multi": 7.5, "unlock_year": 1980, "end_year": 1990, "type": "Heimcomputer"},
    {"name": "Vectrex", "license_fee": 78000, "market_multi": 7.8, "unlock_year": 1982, "end_year": 1992, "type": "Konsole"},
    {"name": "ZX Spectrum", "license_fee": 0, "market_multi": 7.6, "unlock_year": 1982, "end_year": 1992, "type": "Heimcomputer"},
    {"name": "Famicom (NES)", "license_fee": 79000, "market_multi": 7.9, "unlock_year": 1983, "end_year": 1993, "type": "Konsole"},
    {"name": "Famicom Disk Sys", "license_fee": 84000, "market_multi": 8.4, "unlock_year": 1986, "end_year": 1996, "type": "Konsole"},
    {"name": "Sega Genesis", "license_fee": 87000, "market_multi": 8.7, "unlock_year": 1988, "end_year": 1998, "type": "Konsole"},
    {"name": "Neo Geo AES", "license_fee": 90000, "market_multi": 9.0, "unlock_year": 1990, "end_year": 2000, "type": "Konsole"},
    {"name": "SNES", "license_fee": 90000, "market_multi": 9.0, "unlock_year": 1990, "end_year": 2000, "type": "Konsole"},
    {"name": "Game Boy", "license_fee": 85000, "market_multi": 8.5, "unlock_year": 1989, "end_year": 1999, "type": "Handheld"},
    {"name": "Philips CD-i", "license_fee": 92000, "market_multi": 9.2, "unlock_year": 1991, "end_year": 2001, "type": "Konsole"},
    {"name": "Atari Jaguar", "license_fee": 94000, "market_multi": 9.4, "unlock_year": 1993, "end_year": 2003, "type": "Konsole"},
    {"name": "PlayStation 1", "license_fee": 96000, "market_multi": 9.6, "unlock_year": 1994, "end_year": 2004, "type": "Konsole"},
    {"name": "Sega Saturn", "license_fee": 95000, "market_multi": 9.5, "unlock_year": 1994, "end_year": 2004, "type": "Konsole"},
    {"name": "Nintendo 64", "license_fee": 99000, "market_multi": 9.9, "unlock_year": 1996, "end_year": 2006, "type": "Konsole"},
    {"name": "Dreamcast", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 1998, "end_year": 2008, "type": "Konsole"},
    {"name": "PlayStation 2", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2000, "end_year": 2010, "type": "Konsole"},
    {"name": "PlayStation Portable", "license_fee": 98000, "market_multi": 9.8, "unlock_year": 2004, "end_year": 2014, "type": "Handheld"},
    {"name": "GameCube", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2001, "end_year": 2011, "type": "Konsole"},
    {"name": "Xbox 360", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2005, "end_year": 2015, "type": "Konsole"},
    {"name": "PlayStation 3", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2006, "end_year": 2016, "type": "Konsole"},
    {"name": "Gizmondo", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2008, "end_year": 2018, "type": "Handheld"},
    {"name": "PlayStation 4", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2013, "end_year": 2023, "type": "Konsole"},
    {"name": "Xbox One", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2013, "end_year": 2023, "type": "Konsole"},
    {"name": "PlayStation 4 Pro", "license_fee": 110000, "market_multi": 10.5, "unlock_year": 2016, "end_year": 2026, "type": "Konsole"},
    {"name": "Switch", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2017, "end_year": 2027, "type": "Handheld"},
    {"name": "Playdate", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2018, "end_year": 2028, "type": "Handheld"},
    {"name": "PlayStation 5", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2020, "end_year": 2030, "type": "Konsole"},
    {"name": "Analogue Pocket", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2021, "end_year": 2031, "type": "Handheld"},
    {"name": "Evercade EXP", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2022, "end_year": 2032, "type": "Handheld"},
    {"name": "Steam Deck", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2022, "end_year": 2032, "type": "Handheld"},
    {"name": "Cloud-Console", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2025, "end_year": 2035, "type": "Streaming"},
    {"name": "Neural-Box 1", "license_fee": 100000, "market_multi": 10.0, "unlock_year": 2026, "end_year": 2036, "type": "Konsole"},
]


AUDIENCE_MULTI = {
    "Jeder":           1.5,
    "Jugendliche":     1.0,
    "Hardcore-Gamer":  0.7,
}

AUDIENCE_PRICE = {
    "Jeder":           20,
    "Jugendliche":     30,
    "Hardcore-Gamer":  50,
}

AUDIENCES = list(AUDIENCE_PRICE.keys())
START_AUDIENCES = ["Jeder"]

RESEARCHABLE_AUDIENCES = [
    {"name": "Jugendliche", "cost": 25000, "unlock_year": 1930, "research_weeks": 5},
]

# ============================================================
# ENDGAME-TECHNOLOGIEN (Forschung)
# ============================================================
RESEARCHABLE_TECHNOLOGIES = [
    {"name": "Radio-Werbung",                 "cost": 10000,  "unlock_year": 1930,  "research_weeks": 2, "description": "Schaltet Radio-Kampagnen frei."},
    {"name": "Fernsehen",                     "cost": 50000,  "unlock_year": 1940,"research_weeks": 4, "description": "Schaltet TV-Werbung frei."},
    {"name": "Satelliten-TV",                 "cost": 120000, "unlock_year": 1962,"research_weeks": 6, "description": "Erhöht die Reichweite von TV-Werbung massiv."},
    {"name": "Digitaler Vertrieb & Logistik", "cost": 150000, "unlock_year": 2003, "research_weeks": 6, "description": "Erlaubt den Vertrieb ohne Publisher (Eigenvertrieb) und AAA-Spiele."},
    {"name": "CD-Produktion",                 "cost": 80000,  "unlock_year": 1982,"research_weeks": 5, "description": "Schaltet die Pressmaschine für CDs frei."},
    {"name": "Website & Forum",               "cost": 60000,  "unlock_year": 1996,"research_weeks": 4, "description": "Schaltet Online-Community-Marketing frei."},
    {"name": "Social Media Marketing",        "cost": 100000, "unlock_year": 2006,"research_weeks": 5, "description": "Schaltet Social-Media-Kampagnen frei."},
    {"name": "Crowdfunding",                  "cost": 200000, "unlock_year": 2009,"research_weeks": 6, "description": "Ermöglicht Finanzierung durch Fans."},
    {"name": "Live-Service Architektur",      "cost": 300000, "unlock_year": 2004, "research_weeks": 8, "description": "Ermöglicht die Entwicklung und den Betrieb von MMOs und Live-Service Spielen."},
    {"name": "Investment & M&A",              "cost": 500000, "unlock_year": 1990, "research_weeks": 10, "description": "Ermöglicht den Aufkauf von Konkurrenz-Studios am Aktienmarkt."},
    {"name": "Hardware Labor",                "cost": 1000000,"unlock_year": 1975, "research_weeks": 15, "description": "Schaltet die Entwicklung eigener Konsolen frei."},
    {"name": "Büroausstattung 1",             "cost": 25000,  "unlock_year": 1930, "research_weeks": 4, "description": "Schaltet Arcade-Automaten und Erholungsobjekte frei."},
    {"name": "Arbeitsrecht-Experten",         "cost": 80000, "unlock_year": 1930, "research_weeks": 6, "description": "Schaltet die Rechtsabteilung frei, um Headhunting zu erschweren."},
    {"name": "Geheimdienst-Netzwerk",         "cost": 120000, "unlock_year": 1930, "research_weeks": 8, "description": "Schaltet die Marktforschungs-Station frei (KI-Spionage)."},
    {"name": "Krisenmanagement",              "cost": 50000, "unlock_year": 1930, "research_weeks": 5, "description": "Schaltet die PR-Zentrale frei, um Hype-Verlust durch Sabotage zu reduzieren."},
    {"name": "Büroausstattung 2",             "cost": 30000,  "unlock_year": 1930, "research_weeks": 4, "description": "Schaltet weitere Pflanzen und Dekorationen frei."},
    {"name": "Büroausstattung 3",             "cost": 65000,  "unlock_year": 1930, "research_weeks": 5, "description": "Schaltet exotische Zimmerpflanzen und Luxus-Deko frei."},
    {"name": "Gesundes Arbeiten",             "cost": 40000,  "unlock_year": 1990, "research_weeks": 5, "description": "Schaltet ergonomische Tische frei."},
    {"name": "Ergonomie am Arbeitsplatz 2",   "cost": 60000,  "unlock_year": 2000, "research_weeks": 5, "description": "Schaltet Stehschreibtische frei."},
    {"name": "Ergonomie am Arbeitsplatz 3",   "cost": 120000, "unlock_year": 2010, "research_weeks": 6, "description": "Schaltet High-End Laufband-Tische frei."},
    {"name": "Kantinen-Ausbau 1",             "cost": 15000,  "unlock_year": 1950, "research_weeks": 3, "description": "Schaltet fortgeschrittene Getränkestationen frei."},
    {"name": "Kantinen-Ausbau 2",             "cost": 35000,  "unlock_year": 1970, "research_weeks": 4, "description": "Schaltet Snack-Automaten und Pizzaöfen frei."},
    {"name": "Kantinen-Ausbau 3",             "cost": 75000,  "unlock_year": 2000, "research_weeks": 5, "description": "Schaltet Gourmet-Küche und Wein-Regal frei."},
    {"name": "Freizeit & Spiel 1",            "cost": 25000,  "unlock_year": 1950, "research_weeks": 3, "description": "Schaltet Tischkicker und Dartscheiben frei."},
    {"name": "Freizeit & Spiel 2",            "cost": 45000,  "unlock_year": 1980, "research_weeks": 4, "description": "Schaltet Billardtische und Flipper frei."},
    {"name": "Freizeit & Spiel 3",            "cost": 95000,  "unlock_year": 2016, "research_weeks": 6, "description": "Schaltet VR-Stationen und Heimkino frei."},
    {"name": "Studios & Kabinen",             "cost": 80000,  "unlock_year": 1930, "research_weeks": 6, "description": "Schaltet hochmoderne Soundkabinen frei."},
    {"name": "Audio-Meisterschaft 2",         "cost": 110000, "unlock_year": 1950, "research_weeks": 5, "description": "Schaltet Drum-Set und Flügel für Sound-Boosts frei."},
    {"name": "Audio-Meisterschaft 3",         "cost": 250000, "unlock_year": 1975, "research_weeks": 7, "description": "Schaltet Regie-Platz und High-End Lautsprecher frei."},
    {"name": "High-End Workstations 1",       "cost": 85000,  "unlock_year": 1990, "research_weeks": 5, "description": "Schaltet Dual-Monitor Setups und Grafik-Tablets frei."},
    {"name": "High-End Workstations 2",       "cost": 150000, "unlock_year": 2005, "research_weeks": 6, "description": "Schaltet Triple-Monitore und Render-Farmen frei."},
    {"name": "Motion Capture Studio",         "cost": 400000, "unlock_year": 1995, "research_weeks": 8, "description": "Schaltet MoCap-Kameras frei."},
    {"name": "Gamer-Setup",                   "cost": 70000,  "unlock_year": 2010, "research_weeks": 4, "description": "Schaltet RGB-Desks und Gamer-Schreibtische frei."},
    {"name": "Dekorations-Wahn 1",            "cost": 20000,  "unlock_year": 1930, "research_weeks": 3, "description": "Schaltet kleine Bücheregale und Poster frei."},
    {"name": "Dekorations-Wahn 2",            "cost": 50000,  "unlock_year": 1963, "research_weeks": 4, "description": "Schaltet Pokal-Vitrinen und Lava-Lampen frei."},
    {"name": "Dekorations-Wahn 3",            "cost": 90000,  "unlock_year": 1980, "research_weeks": 5, "description": "Schaltet Neon-Schilder, Teppiche und Globen frei."},
]

# ============================================================
# SCHWIERIGKEITSGRADE
# ============================================================
DIFFICULTY_LEVELS = [
    {
        "name": "difficulty_easy",
        "start_money": 150000,
        "rival_strength": 0.7,
        "review_bonus": 0.5,
        "market_multi": 1.3,
        "description": "difficulty_easy_desc",
    },
    {
        "name": "difficulty_normal",
        "start_money": 100000,
        "rival_strength": 1.0,
        "review_bonus": 0.0,
        "market_multi": 1.0,
        "description": "difficulty_normal_desc",
    },
    {
        "name": "difficulty_hard",
        "start_money": 50000,
        "rival_strength": 1.3,
        "review_bonus": -0.5,
        "market_multi": 0.8,
        "description": "difficulty_hard_desc",
    },
    {
        "name": "difficulty_legendary",
        "start_money": 20000,
        "rival_strength": 1.6,
        "review_bonus": -1.0,
        "market_multi": 0.6,
        "description": "difficulty_legendary_desc",
    },
]

# ============================================================
# SUB-GENRES
# ============================================================
SUB_GENRES = {
    "Action": [
        {"name": "Shooter", "slider_adjust": {"Gameplay": 2, "Grafik": 1, "Sound": 0, "Story": -1, "KI": 0, "Welt": -1}},
        {"name": "Beat 'em Up", "slider_adjust": {"Gameplay": 2, "Grafik": 0, "Sound": 1, "Story": -1, "KI": 1, "Welt": -2}},
        {"name": "Stealth", "slider_adjust": {"Gameplay": 1, "Grafik": 0, "Sound": 1, "Story": 1, "KI": 2, "Welt": -2}},
    ],
    "RPG": [
        {"name": "JRPG", "slider_adjust": {"Gameplay": 0, "Grafik": 1, "Sound": 1, "Story": 2, "KI": -1, "Welt": -1}},
        {"name": "Action-RPG", "slider_adjust": {"Gameplay": 2, "Grafik": 1, "Sound": 0, "Story": -1, "KI": 0, "Welt": 0}},
        {"name": "Dungeon Crawler", "slider_adjust": {"Gameplay": 1, "Grafik": -1, "Sound": 0, "Story": -1, "KI": 1, "Welt": 2}},
    ],
    "Simulation": [
        {"name": "Lebenssimulation", "slider_adjust": {"Gameplay": 1, "Grafik": 1, "Sound": 0, "Story": 0, "KI": 1, "Welt": 0}},
        {"name": "Wirtschaftssim", "slider_adjust": {"Gameplay": 2, "Grafik": -1, "Sound": -1, "Story": 0, "KI": 2, "Welt": 0}},
        {"name": "Fahrsimulation", "slider_adjust": {"Gameplay": 1, "Grafik": 2, "Sound": 1, "Story": -2, "KI": 0, "Welt": 1}},
    ],
    "Strategie": [
        {"name": "Echtzeit", "slider_adjust": {"Gameplay": 1, "Grafik": 0, "Sound": 0, "Story": -1, "KI": 2, "Welt": 1}},
        {"name": "Rundenbasiert", "slider_adjust": {"Gameplay": 0, "Grafik": -1, "Sound": 0, "Story": 1, "KI": 2, "Welt": 1}},
        {"name": "Tower Defense", "slider_adjust": {"Gameplay": 2, "Grafik": 1, "Sound": 0, "Story": -2, "KI": 1, "Welt": 0}},
    ],
    "Abenteuer": [
        {"name": "Point & Click", "slider_adjust": {"Gameplay": -1, "Grafik": 1, "Sound": 1, "Story": 2, "KI": 0, "Welt": 0}},
        {"name": "Open World", "slider_adjust": {"Gameplay": 1, "Grafik": 1, "Sound": 0, "Story": 0, "KI": 0, "Welt": 2}},
        {"name": "Visual Novel", "slider_adjust": {"Gameplay": -2, "Grafik": 2, "Sound": 1, "Story": 3, "KI": -1, "Welt": -1}},
    ],
    "Puzzle": [
        {"name": "Match-3", "slider_adjust": {"Gameplay": 2, "Grafik": 1, "Sound": 1, "Story": -2, "KI": 0, "Welt": -1}},
        {"name": "Rätsel-Abenteuer", "slider_adjust": {"Gameplay": 1, "Grafik": 0, "Sound": 0, "Story": 2, "KI": 0, "Welt": 0}},
    ],
    "Sport": [
        {"name": "Mannschaftssport", "slider_adjust": {"Gameplay": 1, "Grafik": 1, "Sound": 0, "Story": -1, "KI": 1, "Welt": 0}},
        {"name": "Extremsport", "slider_adjust": {"Gameplay": 2, "Grafik": 1, "Sound": 1, "Story": -2, "KI": 0, "Welt": 1}},
    ],
    "Casual": [
        {"name": "Party-Spiel", "slider_adjust": {"Gameplay": 2, "Grafik": 0, "Sound": 2, "Story": -2, "KI": -1, "Welt": 0}},
        {"name": "Idle Game", "slider_adjust": {"Gameplay": 1, "Grafik": -1, "Sound": -1, "Story": -1, "KI": 2, "Welt": 0}},
        {"name": "Sandbox", "slider_adjust": {"Gameplay": 1, "Grafik": 0, "Sound": 0, "Story": -2, "KI": 0, "Welt": 3}},
    ],
    "Horror": [
        {"name": "Survival Horror", "slider_adjust": {"Gameplay": 1, "Grafik": 1, "Sound": 1, "Story": 0, "KI": 0, "Welt": 0}},
        {"name": "Psycho-Horror", "slider_adjust": {"Gameplay": -1, "Grafik": 0, "Sound": 2, "Story": 2, "KI": 0, "Welt": 0}},
    ],
    "Kampfspiel": [
        {"name": "2D Fighter", "slider_adjust": {"Gameplay": 2, "Grafik": 0, "Sound": 1, "Story": -1, "KI": 1, "Welt": -2}},
        {"name": "Arena Brawler", "slider_adjust": {"Gameplay": 1, "Grafik": 1, "Sound": 0, "Story": -1, "KI": 1, "Welt": 1}},
    ],
    "Rennspiel": [
        {"name": "Arcade Racing", "slider_adjust": {"Gameplay": 2, "Grafik": 1, "Sound": 1, "Story": -2, "KI": 0, "Welt": 1}},
        {"name": "Renn-Simulation", "slider_adjust": {"Gameplay": 0, "Grafik": 2, "Sound": 0, "Story": -2, "KI": 1, "Welt": 2}},
    ],
}



# ============================================================
# ENGINE-FEATURES (Historische Forschungs-Datenbank 1930-2026)
# unlock_year: Jahr ab dem erforschbar
# category, name, tech_bonus, cost, research_weeks
# Die Spielwoche wird dynamisch via get_available_features() berechnet.
# ============================================================
ENGINE_FEATURES = [
    {"category": "Engine", "name": "Papier-Logik", "cost": 1000, "tech_bonus": 10, "unlock_year": 1930},
    {"category": "Sound", "name": "Magnetband-Aufnahme", "cost": 3000, "tech_bonus": 15, "unlock_year": 1935},
    {"category": "Technik", "name": "Relais-Steuerung", "cost": 5000, "tech_bonus": 5, "unlock_year": 1932},
    {"category": "Technik", "name": "Lochkarten-Input", "cost": 13000, "tech_bonus": 10, "unlock_year": 1936},
    {"category": "Technik", "name": "Vakuum-Röhren", "cost": 23000, "tech_bonus": 15, "unlock_year": 1941},
    {"category": "Grafik", "name": "Oszilloskop-Grafik", "cost": 33000, "tech_bonus": 5, "unlock_year": 1946},
    {"category": "Technik", "name": "Transistor V1", "cost": 37000, "tech_bonus": 20, "unlock_year": 1948},
    {"category": "Technik", "name": "Magnetkernspeicher", "cost": 45000, "tech_bonus": 10, "unlock_year": 1952},
    {"category": "Sound", "name": "Mono-Beep V1", "cost": 53000, "tech_bonus": 5, "unlock_year": 1956},
    {"category": "Sound", "name": "Stereo-Sound", "cost": 65000, "tech_bonus": 20, "unlock_year": 1958},
    {"category": "Grafik", "name": "Vektor-Linien", "cost": 57000, "tech_bonus": 15, "unlock_year": 1958},
    {"category": "Grafik", "name": "CRT-Standard", "cost": 65000, "tech_bonus": 10, "unlock_year": 1962},
    {"category": "Sound", "name": "Moog Synthesizer", "cost": 75000, "tech_bonus": 35, "unlock_year": 1964},
    {"category": "Grafik", "name": "ASCII-Grafik", "cost": 75000, "tech_bonus": 5, "unlock_year": 1967},
    {"category": "Technik", "name": "Mikroprozessor", "cost": 83000, "tech_bonus": 30, "unlock_year": 1971},
    {"category": "Sound", "name": "PCM Audio", "cost": 95000, "tech_bonus": 40, "unlock_year": 1972},
    {"category": "Grafik", "name": "Tilemaps V1", "cost": 89000, "tech_bonus": 20, "unlock_year": 1974},
    {"category": "Grafik", "name": "Parallax-Scrolling", "cost": 93000, "tech_bonus": 15, "unlock_year": 1976},
    {"category": "Grafik", "name": "Sprite-Rotation", "cost": 97000, "tech_bonus": 10, "unlock_year": 1978},
    {"category": "Sound", "name": "FM-Synthese", "cost": 101000, "tech_bonus": 20, "unlock_year": 1980},
    {"category": "Sound", "name": "Dolby Surround", "cost": 105000, "tech_bonus": 30, "unlock_year": 1982},
    {"category": "Grafik", "name": "Vierfarb-Sprites", "cost": 105000, "tech_bonus": 10, "unlock_year": 1982},
    {"category": "Sound", "name": "MIDI Support", "cost": 110000, "tech_bonus": 45, "unlock_year": 1983},
    {"category": "Physik", "name": "Physik V1", "cost": 109000, "tech_bonus": 10, "unlock_year": 1984},
    {"category": "Gameplay", "name": "Savegame-Batterie", "cost": 111000, "tech_bonus": 30, "unlock_year": 1985},
    {"category": "Sound", "name": "Wavetable-Sound", "cost": 115000, "tech_bonus": 25, "unlock_year": 1987},
    {"category": "Grafik", "name": "Mode 7 Pseudo-3D", "cost": 119000, "tech_bonus": 30, "unlock_year": 1989},
    {"category": "Grafik", "name": "Raycasting", "cost": 123000, "tech_bonus": 40, "unlock_year": 1991},
    {"category": "Technik", "name": "Z-Buffer", "cost": 127000, "tech_bonus": 20, "unlock_year": 1993},
    {"category": "Grafik", "name": "Texture Mapping", "cost": 129000, "tech_bonus": 30, "unlock_year": 1994},
    {"category": "Sound", "name": "CD-Audio", "cost": 131000, "tech_bonus": 50, "unlock_year": 1995},
    {"category": "Sound", "name": "MP3 Support", "cost": 135000, "tech_bonus": 40, "unlock_year": 1995},
    {"category": "Grafik", "name": "Echtzeit-Licht", "cost": 133000, "tech_bonus": 20, "unlock_year": 1996},
    {"category": "Technik", "name": "VST Plugins", "cost": 140000, "tech_bonus": 60, "unlock_year": 1996},
    {"category": "KI", "name": "KI V1 (A*)", "cost": 135000, "tech_bonus": 20, "unlock_year": 1997},
    {"category": "Gameplay", "name": "Multiplayer V2", "cost": 137000, "tech_bonus": 40, "unlock_year": 1998},
    {"category": "Grafik", "name": "Vertex-Shader", "cost": 141000, "tech_bonus": 50, "unlock_year": 2000},
    {"category": "Physik", "name": "Ragdoll-Physik", "cost": 145000, "tech_bonus": 40, "unlock_year": 2002},
    {"category": "Technik", "name": "64-bit Engine", "cost": 155000, "tech_bonus": 80, "unlock_year": 2003},
    {"category": "Grafik", "name": "Pixel-Shader", "cost": 149000, "tech_bonus": 60, "unlock_year": 2004},
    {"category": "Physik", "name": "PhysX Support", "cost": 160000, "tech_bonus": 70, "unlock_year": 2005},
    {"category": "Technik", "name": "Blu-Ray Support", "cost": 153000, "tech_bonus": 100, "unlock_year": 2006},
    {"category": "Physik", "name": "Physische Engine V3", "cost": 157000, "tech_bonus": 60, "unlock_year": 2008},
    {"category": "Gameplay", "name": "Cloud-Saves", "cost": 161000, "tech_bonus": 20, "unlock_year": 2010},
    {"category": "Grafik", "name": "Motion Capture", "cost": 165000, "tech_bonus": 80, "unlock_year": 2012},
    {"category": "Sound", "name": "Dolby Atmos", "cost": 180000, "tech_bonus": 100, "unlock_year": 2012},
    {"category": "KI", "name": "Prozedurale Welt", "cost": 169000, "tech_bonus": 100, "unlock_year": 2014},
    {"category": "Grafik", "name": "HDR-Support", "cost": 173000, "tech_bonus": 40, "unlock_year": 2016},
    {"category": "Sound", "name": "VR-Audio", "cost": 190000, "tech_bonus": 110, "unlock_year": 2016},
    {"category": "Grafik", "name": "Echtzeit-Raytracing", "cost": 177000, "tech_bonus": 200, "unlock_year": 2018},
    {"category": "KI", "name": "KI-Storytelling", "cost": 181000, "tech_bonus": 150, "unlock_year": 2020},
    {"category": "Gameplay", "name": "Full-Body VR", "cost": 185000, "tech_bonus": 120, "unlock_year": 2022},
    {"category": "Grafik", "name": "Generative Assets", "cost": 187000, "tech_bonus": 200, "unlock_year": 2023},
    {"category": "Technik", "name": "Quanten-Ladezeit", "cost": 191000, "tech_bonus": 100, "unlock_year": 2025},
    {"category": "Technik", "name": "Neural-Sync", "cost": 193000, "tech_bonus": 10, "unlock_year": 2026},
]



# ============================================================
# MITARBEITER-NAMEN (zufällig)
# ============================================================
EMPLOYEE_FIRST_NAMES = [
    "Max", "Anna", "Felix", "Sarah", "Tim", "Julia", "Leon", "Laura",
    "Lukas", "Marie", "Jonas", "Lena", "Niklas", "Emma", "David",
    "Sophie", "Jan", "Mia", "Tom", "Lisa", "Kai", "Nina", "Ben",
    "Hanna", "Erik", "Lea", "Paul", "Clara", "Finn", "Ella",
    "Oliver", "Emilia", "Sebastian", "Johanna", "Alexander", "Mila",
    "Julian", "Pia", "Fabian", "Charlotte", "Moritz", "Luisa",
    "Markus", "Sandra", "Christian", "Nicole", "Andreas", "Stefanie",
    "Michael", "Sabine", "Thomas", "Melanie", "Jürgen", "Petra",
    "Hans", "Ursula", "Werner", "Helga", "Peter", "Karin",
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer",
    "Michael", "Linda", "William", "Elizabeth", "David", "Barbara",
]

EMPLOYEE_LAST_NAMES = [
    "Müller", "Schmidt", "Weber", "Fischer", "Wagner", "Bauer",
    "Koch", "Richter", "Klein", "Wolf", "Schwarz", "Braun",
    "Zimmermann", "Hartmann", "Krüger", "Hofmann", "Lange",
    "Jung", "Peters", "König", "Lang", "Berg", "Stein",
    "Meier", "Schulz", "Hoffmann", "Schäfer", "Bayer", "Eberhardt",
    "Vogel", "Hermann", "Kühn", "Huber", "Mayer", "Lehmann",
    "Friedrich", "Günther", "Kohl", "Liedtke", "Zander", "Fiedler",
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
    "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez",
]

EMPLOYEE_ROLES = [
    {"role": "Programmierer",  "primary": "KI",       "secondary": "Gameplay"},
    {"role": "Grafik-Designer","primary": "Grafik",   "secondary": "Welt"},
    {"role": "Sound-Designer", "primary": "Sound",    "secondary": "Gameplay"},
    {"role": "Supporter",      "primary": "Story",    "secondary": "Welt"},
]

# ============================================================
# MITARBEITER-EIGENSCHAFTEN (Traits)
# ============================================================
EMPLOYEE_TRAITS = [
    {"name": "Schneller Lerner", "effect": "speed", "value": 1.1, "description": "Arbeitet 10% schneller."},
    {"name": "Perfektionist",    "effect": "quality", "value": 1.1, "description": "Steigert die Spielqualität um 10%."},
    {"name": "Faulpelz",         "effect": "speed", "value": 0.8, "description": "Arbeitet 20% langsamer."},
    {"name": "Teamplayer",       "effect": "morale_loss", "value": 0.5, "description": "Verliert nur halb so schnell Moral."},
    {"name": "Griesgram",        "effect": "morale_loss", "value": 1.5, "description": "Verliert 50% schneller Moral."},
    {"name": "Bug-Magnet",       "effect": "bugs", "value": 1.5, "description": "Verursacht 50% mehr Bugs."},
    {"name": "Sauberer Coder",   "effect": "bugs", "value": 0.5, "description": "Verursacht 50% weniger Bugs."},
    {"name": "Geldgeil",         "effect": "salary", "value": 1.2, "description": "Verlangt 20% mehr Gehalt."},
    {"name": "Bescheiden",       "effect": "salary", "value": 0.8, "description": "Begnügt sich mit 20% weniger Gehalt."},
]

# ============================================================
# MITARBEITER-SPEZIALISIERUNGEN (Boni)
# ============================================================
EMPLOYEE_SPECIALIZATIONS = [
    {"name": "Sound-Genie",      "bonus_type": "Sound",    "bonus_value": 0.2, "description": "Verbessert die Audio-Qualität massiv."},
    {"name": "Code-Maschine",    "bonus_type": "KI",       "bonus_value": 0.2, "description": "Optimiert Programmierung und KI."},
    {"name": "Design-Gott",      "bonus_type": "Grafik",   "bonus_value": 0.2, "description": "Ein Auge für erstklassige Grafik."},
    {"name": "Story-Master",     "bonus_type": "Story",    "bonus_value": 0.2, "description": "Schreibt packende Dialoge und Plots."},
    {"name": "Motivationstrainer", "bonus_type": "Moral",   "bonus_value": 10,  "description": "Hält die Moral im Team hoch."},
    {"name": "Bug-Jäger",        "bonus_type": "Bugs",     "bonus_value": 0.5, "description": "Findet und behebt Bugs doppelt so schnell."},
    {"name": "Marketing-Experte", "bonus_type": "Marketing", "bonus_value": 0.3, "description": "Erhöht die Effektivität von Marketing."},
    {"name": "Action-Experte",    "bonus_type": "Genre", "target": "Action",    "bonus_value": 0.15, "description": "Bonus auf Action-Spiele."},
    {"name": "RPG-Veteran",       "bonus_type": "Genre", "target": "RPG",       "bonus_value": 0.15, "description": "Bonus auf Rollenspiele."},
    {"name": "Strategie-Genie",   "bonus_type": "Genre", "target": "Strategie", "bonus_value": 0.15, "description": "Bonus auf Strategiespiele."},
    {"name": "Simulations-Profi", "bonus_type": "Genre", "target": "Simulation","bonus_value": 0.15, "description": "Bonus auf Simulationen."},
    {"name": "Sport-Fanatiker",   "bonus_type": "Genre", "target": "Sport",      "bonus_value": 0.15, "description": "Bonus auf Sportspiele."},
    {"name": "Fantasy-Fan",       "bonus_type": "Topic", "target": "Fantasy",   "bonus_value": 0.1,  "description": "Bonus auf Fantasy-Themen."},
    {"name": "Sci-Fi-Nerd",       "bonus_type": "Topic", "target": "Sci-Fi",    "bonus_value": 0.1,  "description": "Bonus auf Sci-Fi-Themen."},
    {"name": "Geschichts-Kenner", "bonus_type": "Topic", "target": "Mittelalter","bonus_value": 0.1,  "description": "Bonus auf historische Themen."},
]


# ============================================================
# ENTWICKLUNGSPHASEN
# ============================================================
DEV_PHASES = [
    {"name": "Konzept",    "duration_weeks": 1, "primary_sliders": ["Story", "Gameplay"]},
    {"name": "Engine",     "duration_weeks": 1, "primary_sliders": ["KI", "Gameplay"]},
    {"name": "Design",     "duration_weeks": 1, "primary_sliders": ["Grafik", "Welt"]},
    {"name": "Produktion", "duration_weeks": 2, "primary_sliders": ["Gameplay", "Grafik", "Sound"]},
    {"name": "Testing",    "duration_weeks": 1, "primary_sliders": ["KI", "Gameplay"]},
]



# ============================================================
# AAA DEV EVENTS
# ============================================================
AAA_DEV_EVENTS = [
    {
        "id": "aaa_cgi_leak",
        "options": [
            {"id": "finish", "cost": 2000000, "hype": 100, "bugs": 0, "morale": 0},
            {"id": "ignore", "cost": 0, "hype": -50, "bugs": 0, "morale": 0}
        ]
    },
    {
        "id": "aaa_feature_creep",
        "options": [
            {"id": "implement", "cost": 1000000, "hype": 30, "bugs": 200, "morale": 0},
            {"id": "focus", "cost": 0, "hype": 0, "bugs": 0, "morale": -10}
        ]
    },
    {
        "id": "aaa_celebrity_voice",
        "options": [
            {"id": "hire", "cost": 3000000, "hype": 150, "bugs": 0, "morale": 0},
            {"id": "pass", "cost": 0, "hype": 0, "bugs": 0, "morale": 0}
        ]
    }
]

# ============================================================
# ALLGEMEINE ENTWICKLUNGS-EVENTS (fuer alle Spielgroessen)
# Konsequenzen: delay=+Wochen, speed=-Wochen (beschleunigt),
#               cost=EUR, hype=Hype-Aend., bugs=Bugs, morale=Moral-Aend.
# ============================================================
GENERAL_DEV_EVENTS = [
    {
        "id": "dev_key_employee_sick",
        "options": [
            {"id": "hire_freelancer", "cost": 15000, "delay": 0, "speed": 0, "hype": 0, "bugs": 5, "morale": 0},
            {"id": "continue_without", "cost": 0, "delay": 3, "speed": 0, "hype": 0, "bugs": 10, "morale": -10}
        ]
    },
    {
        "id": "dev_tech_breakthrough",
        "options": [
            {"id": "implement_now", "cost": 5000, "delay": 2, "speed": 0, "hype": 15, "bugs": 5, "morale": 5},
            {"id": "save_for_sequel", "cost": 0, "delay": 0, "speed": 0, "hype": 0, "bugs": 0, "morale": 0}
        ]
    },
    {
        "id": "dev_scope_creep",
        "options": [
            {"id": "add_feature", "cost": 8000, "delay": 4, "speed": 0, "hype": 20, "bugs": 15, "morale": -5},
            {"id": "stay_focused", "cost": 0, "delay": 0, "speed": 0, "hype": -5, "bugs": 0, "morale": 5}
        ]
    },
    {
        "id": "dev_crunch_offer",
        "options": [
            {"id": "accept_crunch", "cost": 0, "delay": 0, "speed": 3, "hype": 0, "bugs": 20, "morale": -25},
            {"id": "decline_crunch", "cost": 0, "delay": 0, "speed": 0, "hype": 0, "bugs": 0, "morale": 0}
        ]
    },
    {
        "id": "dev_positive_review",
        "options": [
            {"id": "release_demo", "cost": 3000, "delay": 1, "speed": 0, "hype": 30, "bugs": 0, "morale": 10},
            {"id": "keep_secret", "cost": 0, "delay": 0, "speed": 0, "hype": 5, "bugs": 0, "morale": 0}
        ]
    },
    {
        "id": "dev_data_loss",
        "options": [
            {"id": "restore_backup", "cost": 2000, "delay": 1, "speed": 0, "hype": 0, "bugs": 5, "morale": -10},
            {"id": "rewrite", "cost": 0, "delay": 5, "speed": 0, "hype": 0, "bugs": 0, "morale": -20}
        ]
    },
    {
        "id": "dev_viral_moment",
        "options": [
            {"id": "embrace_hype", "cost": 5000, "delay": 0, "speed": 0, "hype": 50, "bugs": 0, "morale": 15},
            {"id": "focus_quality", "cost": 0, "delay": 0, "speed": 0, "hype": 10, "bugs": 0, "morale": 0}
        ]
    },
    {
        "id": "dev_rival_copy",
        "options": [
            {"id": "speed_up", "cost": 10000, "delay": 0, "speed": 2, "hype": 10, "bugs": 10, "morale": -5},
            {"id": "ignore_rival", "cost": 0, "delay": 0, "speed": 0, "hype": -10, "bugs": 0, "morale": 5}
        ]
    },
    {
        "id": "dev_pizza_party",
        "options": [
            {"id": "buy_pizza", "cost": 500, "delay": 0, "speed": 1, "hype": 0, "bugs": 0, "morale": 20},
            {"id": "no_pizza", "cost": 0, "delay": 0, "speed": 0, "hype": 0, "bugs": 0, "morale": -5}
        ]
    },
    {
        "id": "dev_refactoring_needed",
        "options": [
            {"id": "do_refactor", "cost": 0, "delay": 3, "speed": 2, "hype": 0, "bugs": -15, "morale": 5},
            {"id": "skip_refactor", "cost": 0, "delay": 0, "speed": 0, "hype": 0, "bugs": 10, "morale": 0}
        ]
    },
    {
        "id": "dev_art_style_debate",
        "options": [
            {"id": "realistic_art", "cost": 10000, "delay": 2, "speed": 0, "hype": 25, "bugs": 5, "morale": 0},
            {"id": "stylized_art", "cost": 2000, "delay": 0, "speed": 1, "hype": 10, "bugs": 0, "morale": 5}
        ]
    },
    {
        "id": "dev_sound_engine_bug",
        "options": [
            {"id": "fix_sound", "cost": 0, "delay": 2, "speed": 0, "hype": 0, "bugs": -10, "morale": -5},
            {"id": "ignore_sound", "cost": 0, "delay": 0, "speed": 0, "hype": -5, "bugs": 5, "morale": 0}
        ]
    },
    {
        "id": "dev_easter_egg",
        "options": [
            {"id": "add_easter_egg", "cost": 1000, "delay": 1, "speed": 0, "hype": 15, "bugs": 2, "morale": 10},
            {"id": "no_easter_egg", "cost": 0, "delay": 0, "speed": 0, "hype": 0, "bugs": 0, "morale": 0}
        ]
    },
    {
        "id": "dev_translation_error",
        "options": [
            {"id": "hire_translator", "cost": 5000, "delay": 1, "speed": 0, "hype": 10, "bugs": -5, "morale": 0},
            {"id": "auto_translate", "cost": 0, "delay": 0, "speed": 0, "hype": -10, "bugs": 10, "morale": 0}
        ]
    },
    {
        "id": "dev_dev_con_trip",
        "options": [
            {"id": "send_team", "cost": 12000, "delay": 2, "speed": 0, "hype": 40, "bugs": -5, "morale": 30},
            {"id": "stay_at_work", "cost": 0, "delay": 0, "speed": 0, "hype": 0, "bugs": 0, "morale": -10}
        ]
    },
    {
        "id": "dev_middleware_update",
        "options": [
            {"id": "update_now", "cost": 0, "delay": 2, "speed": 1, "hype": 5, "bugs": -5, "morale": 0},
            {"id": "wait_update", "cost": 0, "delay": 0, "speed": 0, "hype": 0, "bugs": 5, "morale": 0}
        ]
    },
    {
        "id": "dev_keyboard_fail",
        "options": [
            {"id": "mechanical_keys", "cost": 3000, "delay": 0, "speed": 1, "hype": 0, "bugs": 0, "morale": 15},
            {"id": "standard_keys", "cost": 500, "delay": 0, "speed": 0, "hype": 0, "bugs": 0, "morale": 0}
        ]
    },
    {
        "id": "dev_leaked_screens",
        "options": [
            {"id": "use_as_promo", "cost": 0, "delay": 0, "speed": 0, "hype": 30, "bugs": 0, "morale": 10},
            {"id": "damage_control", "cost": 5000, "delay": 1, "speed": 0, "hype": -10, "bugs": 0, "morale": -5}
        ]
    }
]


# ============================================================
# BÜRO-STUFEN
# ============================================================
OFFICE_LEVELS = [
    {"name": "Garage",          "max_employees": 1,  "cost": 0,       "prestige": 0},
    {"name": "Kleines Büro",    "max_employees": 3,  "cost": 50000,   "prestige": 1},
    {"name": "Mittleres Büro",  "max_employees": 6,  "cost": 200000,  "prestige": 2},
    {"name": "Großes Studio",   "max_employees": 12, "cost": 500000,  "prestige": 3},
    {"name": "Hauptquartier",   "max_employees": 20, "cost": 1500000, "prestige": 5},
]

# ============================================================
# BÜRO-OBJEKTE (Neues 3-Ebenen-Bausystem)
# layer: "structure" = Wände/Türen, "furniture" = Möbel/Einrichtung
# ============================================================
BUILD_OBJECTS = {
    "wall":          {"name": "Wand",                    "cost": 200,    "layer": "structure", "employees": 0, "bonus": None,         "desc": "Grundlegende Wand. Grenzt Räume ab."},
    "door":          {"name": "Tür",                     "cost": 500,    "layer": "structure", "employees": 0, "bonus": None,         "desc": "Tür in einer Wand. Benötigt angrenzende Wand.", "requires_adjacent_wall": True},
    "window":        {"name": "Fenster",                 "cost": 800,    "layer": "structure", "employees": 0, "bonus": None,         "desc": "Fenster in einer Wand. Hebt die Moral.", "requires_adjacent_wall": True, "morale_bonus": 2},
    "dev_desk":      {"name": "Entwickler-Schreibtisch", "cost": 1000,   "layer": "furniture", "employees": 1, "bonus": None,         "desc": "Arbeitsplatz für einen Entwickler."},
    "coffee":        {"name": "Kaffeemaschine",          "cost": 500,    "layer": "furniture", "employees": 0, "bonus": None,         "desc": "Gibt kleinen Moral-Boost. +1 Moral pro Woche.", "morale_bonus": 1},
    "plant":         {"name": "Pflanze",                 "cost": 300,    "layer": "furniture", "employees": 0, "bonus": None,         "desc": "Dekorativ. +1 Moral pro Woche.", "morale_bonus": 1},
    "sofa":          {"name": "Sofa",                    "cost": 1200,   "layer": "furniture", "employees": 0, "bonus": None,         "desc": "Erholungszone. +2 Moral pro Woche.", "morale_bonus": 2},
    "research_desk": {"name": "Forschungs-Schreibtisch", "cost": 5000,   "layer": "furniture", "employees": 0, "bonus": "research",   "desc": "Schaltet Forschung frei."},
    "server_rack":   {"name": "Server-Rack",             "cost": 15000,  "layer": "furniture", "employees": 0, "bonus": "mmo",        "desc": "Serverkapazität für MMOs."},
    "mixing_desk":   {"name": "Mischpult",               "cost": 20000,  "layer": "furniture", "employees": 1, "bonus": "sound",      "desc": "+10% auf Sound-Bewertung."},
    "mixing_desk_v2": {"name": "Modernes Mischpult V2",   "cost": 35000,  "layer": "furniture", "employees": 1, "bonus": "sound",      "desc": "+20% auf Sound-Bewertung.", "req_tech": "Audio-Meisterschaft 2"},
    "art_station":   {"name": "Grafik-Station",          "cost": 20000,  "layer": "furniture", "employees": 1, "bonus": "graphics",   "desc": "+10% auf Grafik-Bewertung."},
    "qa_station":    {"name": "QA-Workstation",          "cost": 8000,   "layer": "furniture", "employees": 0, "bonus": "qa",         "desc": "Reduziert Bugs um 20%."},
    "marketing_board":{"name": "Marketing-Pinnwand",    "cost": 6000,   "layer": "furniture", "employees": 0, "bonus": "marketing",  "desc": "Schaltet große Marketing-Kampagnen frei."},
    "press_machine": {"name": "Pressmaschine",           "cost": 80000,  "layer": "furniture", "employees": 0, "bonus": "production", "desc": "Erlaubt die Herstellung physischer Kopien."},
    "break_couch":   {"name": "Pausenraum-Sofa",         "cost": 10000,  "layer": "furniture", "employees": 0, "bonus": "morale_room","desc": "Reduziert Moral-Abfall deutlich."},
    "water_cooler":  {"name": "Wasserspender",           "cost": 800,    "layer": "furniture", "employees": 0, "bonus": None,         "desc": "Kleine Erfrischung. +1 Moral pro Woche.", "morale_bonus": 1},
    "plant_cactus": {"name": "Kaktus", "cost": 100, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Sticht leicht. +1 Moral.", "morale_bonus": 1},
    "plant_fern": {"name": "Farn", "cost": 250, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein schöner Farn. +1 Moral.", "morale_bonus": 1},
    "plant_rubber": {"name": "Gummibaum", "cost": 400, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein großer Gummibaum. +1 Moral.", "req_tech": "Büroausstattung 2", "morale_bonus": 1},
    "plant_monstera": {"name": "Monstera", "cost": 600, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Schickes Blattwerk. +2 Moral.", "req_tech": "Büroausstattung 2", "morale_bonus": 2},
    "plant_bonsai": {"name": "Bonsai", "cost": 800, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Fördert die Ruhe. +2 Moral.", "req_tech": "Büroausstattung 2", "morale_bonus": 2},
    "plant_palm": {"name": "Zimmer-Palme", "cost": 1200, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Karibik im Büro. +2 Moral.", "req_tech": "Büroausstattung 3", "morale_bonus": 2},
    "plant_oak": {"name": "Eiche im Topf", "cost": 2000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein ganzer Baum drinnen. +3 Moral.", "req_tech": "Büroausstattung 3", "morale_bonus": 3},
    "plant_venus": {"name": "Venusfliegenfalle", "cost": 1500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Fängt nervige Bugs? +2 Moral.", "req_tech": "Büroausstattung 3", "morale_bonus": 2},
    "drink_espresso": {"name": "Espresso-Maschine", "cost": 1500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Schneller Wachmacher. +2 Moral.", "req_tech": "Kantinen-Ausbau 1", "morale_bonus": 2},
    "drink_tea": {"name": "Tee-Kocher", "cost": 900, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Für eine entspannte Pause. +1 Moral.", "req_tech": "Kantinen-Ausbau 1", "morale_bonus": 1},
    "food_snack": {"name": "Snack-Automat", "cost": 4000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Chips und Schoko. +2 Moral.", "req_tech": "Kantinen-Ausbau 2", "morale_bonus": 2},
    "drink_soft": {"name": "Softdrink-Automat", "cost": 5000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Cola auf Knopfdruck. +2 Moral.", "req_tech": "Kantinen-Ausbau 2", "morale_bonus": 2},
    "fridge_mini": {"name": "Mini-Kühlschrank", "cost": 2500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Kühlt die Getränke. +1 Moral.", "req_tech": "Kantinen-Ausbau 2", "morale_bonus": 1},
    "food_pizza": {"name": "Pizza-Ofen", "cost": 12000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Frische Pizza für Crunch-Times. +4 Moral.", "req_tech": "Kantinen-Ausbau 2", "morale_bonus": 4},
    "food_gourmet": {"name": "Gourmet-Küche", "cost": 30000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein eigener Kochbereich. +6 Moral.", "req_tech": "Kantinen-Ausbau 3", "morale_bonus": 6},
    "drink_wine": {"name": "Wein-Regal", "cost": 15000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Für erfolgreiche Abschlüsse. +3 Moral.", "req_tech": "Kantinen-Ausbau 3", "morale_bonus": 3},
    "arcade_machine":{"name": "Arcade-Automat",          "cost": 3500,   "layer": "furniture", "employees": 0, "bonus": None,         "desc": "Für zwischendurch. +3 Moral pro Woche.", "morale_bonus": 3, "req_tech": "Büroausstattung 1"},
    "rec_dart": {"name": "Dartscheibe", "cost": 600, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Zielscheibe im Pausenraum. +1 Moral.", "req_tech": "Freizeit & Spiel 1", "morale_bonus": 1},
    "rec_kicker": {"name": "Tischkicker", "cost": 1800, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Der Klassiker in Startups. +2 Moral.", "req_tech": "Freizeit & Spiel 1", "morale_bonus": 2},
    "rec_ttable": {"name": "Tischtennisplatte", "cost": 2500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Bewegung am Arbeitsplatz. +2 Moral.", "req_tech": "Freizeit & Spiel 1", "morale_bonus": 2},
    "rec_billiard": {"name": "Billardtisch", "cost": 6000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Edles Spielzeug. +3 Moral.", "req_tech": "Freizeit & Spiel 2", "morale_bonus": 3},
    "rec_pinball": {"name": "Flipper-Automat", "cost": 8000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Klingelt kräftig. +3 Moral.", "req_tech": "Freizeit & Spiel 2", "morale_bonus": 3},
    "rec_boxing": {"name": "Boxsack", "cost": 1200, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Für den Frustabbau. +1 Moral.", "req_tech": "Freizeit & Spiel 2", "morale_bonus": 1},
    "rec_vr": {"name": "VR-Station", "cost": 20000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Modernste Unterhaltung. +5 Moral.", "req_tech": "Freizeit & Spiel 3", "morale_bonus": 5},
    "rec_cinema": {"name": "Heimkino", "cost": 45000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein eigener Kino-Saal. +8 Moral.", "req_tech": "Freizeit & Spiel 3", "morale_bonus": 8},
    "rec_karaoke": {"name": "Musik-Jukebox", "cost": 10000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Hintergrundmusik. +4 Moral.", "req_tech": "Freizeit & Spiel 3", "morale_bonus": 4},
    "rec_massage": {"name": "Massage-Sessel", "cost": 15000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Absolute Entspannung. +5 Moral.", "req_tech": "Freizeit & Spiel 3", "morale_bonus": 5},
    "rec_aquarium": {"name": "Aquarium", "cost": 8000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Beruhigende Fische. +3 Moral.", "req_tech": "Freizeit & Spiel 2", "morale_bonus": 3},
    "desk_wood": {"name": "Holztisch", "cost": 600, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Einfacher Tisch für 1 Entwickler."},
    "desk_metal": {"name": "Metalltisch", "cost": 1500, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Robuster Metalltisch für 1 Entwickler."},
    "desk_glass": {"name": "Glas-Tisch", "cost": 3000, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Stylisch, aber schmutzanfällig. +1 Moral.", "morale_bonus": 1},
    "desk_stand": {"name": "Stehschreibtisch", "cost": 4500, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Arbeiten im Stehen.", "req_tech": "Ergonomie am Arbeitsplatz 2"},
    "desk_treadmill": {"name": "Laufband-Schreibtisch", "cost": 12000, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Arbeiten und joggen.", "req_tech": "Ergonomie am Arbeitsplatz 3", "morale_bonus": 2},
    "desk_lshape": {"name": "L-Form-Desk", "cost": 5000, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Viel Platz für Dokumente.", "req_tech": "Ergonomie am Arbeitsplatz 2"},
    "desk_gamer": {"name": "Gamer-Desk", "cost": 8000, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Mit Carbon-Optik.", "req_tech": "Gamer-Setup"},
    "desk_rgb": {"name": "RGB-Desk", "cost": 12000, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Leuchtet in allen Farben. +1 Moral.", "req_tech": "Gamer-Setup", "morale_bonus": 1},
    "desk_boss": {"name": "Chef-Schreibtisch", "cost": 25000, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Ein gigantischer Chefsessel. +3 Moral.", "req_tech": "Ergonomie am Arbeitsplatz 3", "morale_bonus": 3},
    "desk_luxury": {"name": "Luxus-Tisch", "cost": 50000, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Aus Mahagoni. +5 Moral.", "req_tech": "Ergonomie am Arbeitsplatz 3", "morale_bonus": 5},
    "desk_obsidian": {"name": "Obsidian-Tisch", "cost": 100000, "layer": "furniture", "employees": 1, "bonus": None, "desc": "Für den ultimativen Flex. +10 Moral.", "req_tech": "Ergonomie am Arbeitsplatz 3", "morale_bonus": 10},
    "sound_mic": {"name": "Mikrofon-Ständer", "cost": 8000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+5% Sound-Bonus.", "req_tech": "Studios & Kabinen"},
    "sound_synth": {"name": "Synthesizer-Station", "cost": 15000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+8% Sound-Bonus.", "req_tech": "Studios & Kabinen"},
    "sound_piano": {"name": "Flügel (Klavier)", "cost": 40000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+12% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 2"},
    "sound_drum": {"name": "Drum-Set", "cost": 30000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+10% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 2"},
    "sound_console": {"name": "Mix-Konsole Riesig", "cost": 50000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+15% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 3"},
    "sound_speakers": {"name": "High-End Lautsprecher", "cost": 20000, "layer": "furniture", "employees": 0, "bonus": "sound", "desc": "+5% Sound passiv pro Lautsprecher.", "req_tech": "Audio-Meisterschaft 3"},
    "sound_director": {"name": "Regie-Platz", "cost": 80000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+25% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 3"},
    "sound_wall": {"name": "Akustik-Wände", "cost": 3500, "layer": "structure", "employees": 0, "bonus": "sound", "desc": "Schallisolierte Wand. +1% Sound passiv.", "req_tech": "Studios & Kabinen"},
    "gfx_drawing": {"name": "Zeichenblock-Tisch", "cost": 2500, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+5% Grafik-Bonus."},
    "gfx_tablet": {"name": "Grafik-Tablet", "cost": 6000, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+10% Grafik-Bonus.", "req_tech": "High-End Workstations 1"},
    "gfx_dual": {"name": "Dual-Monitor-Setup", "cost": 12000, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+15% Grafik-Bonus.", "req_tech": "High-End Workstations 1"},
    "gfx_triple": {"name": "Triple-Monitor", "cost": 25000, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+20% Grafik-Bonus.", "req_tech": "High-End Workstations 2"},
    "gfx_green": {"name": "Greenscreen", "cost": 40000, "layer": "structure", "employees": 0, "bonus": "graphics", "desc": "Für Trailer und Filme. +5% Grafik passiv.", "req_tech": "High-End Workstations 2"},
    "gfx_mocap": {"name": "MoCap-Kameras", "cost": 150000, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+30% Grafik-Bonus.", "req_tech": "Motion Capture Studio"},
    "gfx_render": {"name": "Render-Farm", "cost": 200000, "layer": "furniture", "employees": 0, "bonus": "graphics", "desc": "Passiv +20% Grafik.", "req_tech": "High-End Workstations 2"},
    "dev_board": {"name": "Whiteboard", "cost": 1500, "layer": "furniture", "employees": 0, "bonus": "qa", "desc": "-5% Bugs passiv.", "req_tech": "Kantinen-Ausbau 1"},
    "srv_small": {"name": "Server-Rack klein", "cost": 8000, "layer": "furniture", "employees": 0, "bonus": "mmo", "desc": "Kleine MMO-Kapazität."},
    "srv_big": {"name": "Server-Schrank", "cost": 30000, "layer": "furniture", "employees": 0, "bonus": "mmo", "desc": "Gute MMO-Kapazität.", "req_tech": "Live-Service Architektur"},
    "srv_center": {"name": "Server-Zentrum", "cost": 100000, "layer": "furniture", "employees": 0, "bonus": "mmo", "desc": "Massive MMO-Kapazität.", "req_tech": "Live-Service Architektur"},
    "dev_ops": {"name": "DevOps-Station", "cost": 40000, "layer": "furniture", "employees": 1, "bonus": "qa", "desc": "-30% Bugs passiv.", "req_tech": "Live-Service Architektur"},
    "dec_book_s": {"name": "Bücherregal klein", "cost": 900, "layer": "furniture", "employees": 0, "bonus": None, "desc": "+1 Moral.", "req_tech": "Dekorations-Wahn 1", "morale_bonus": 1},
    "dec_book_l": {"name": "Bücherregal groß", "cost": 2500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "+2 Moral.", "req_tech": "Dekorations-Wahn 1", "morale_bonus": 2},
    "dec_locker": {"name": "Schließfach", "cost": 1200, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Für Wertsachen.", "req_tech": "Dekorations-Wahn 1"},
    "dec_trophy": {"name": "Pokal-Vitrine", "cost": 5000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Für deine Game Awards. +3 Moral.", "req_tech": "Dekorations-Wahn 2", "morale_bonus": 3},
    "dec_rug_r": {"name": "Teppich rot", "cost": 1500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein schicker roter Teppich.", "req_tech": "Dekorations-Wahn 3"},
    "dec_rug_b": {"name": "Teppich blau", "cost": 1500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein schicker blauer Teppich.", "req_tech": "Dekorations-Wahn 3"},
    "dec_poster_r": {"name": "Poster Retro", "cost": 500, "layer": "structure", "employees": 0, "bonus": None, "desc": "Altes Spielzeug-Poster. +1 Moral.", "req_tech": "Dekorations-Wahn 1", "morale_bonus": 1},
    "dec_poster_m": {"name": "Poster Modern", "cost": 800, "layer": "structure", "employees": 0, "bonus": None, "desc": "Filmposter. +1 Moral.", "req_tech": "Dekorations-Wahn 1", "morale_bonus": 1},
    "dec_neon": {"name": "Neon-Schild", "cost": 4000, "layer": "structure", "employees": 0, "bonus": None, "desc": "Leuchtet toll im Dunkeln. +2 Moral.", "req_tech": "Dekorations-Wahn 3", "morale_bonus": 2},
    "dec_lava": {"name": "Lava-Lampe", "cost": 1200, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Entspannende Blasen. +1 Moral.", "req_tech": "Dekorations-Wahn 2", "morale_bonus": 1},
    "dec_globe": {"name": "Globus", "cost": 2200, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Die ganze Welt. +1 Moral.", "req_tech": "Dekorations-Wahn 3", "morale_bonus": 1},
    "wall_steel": {"name": "Wand Stahl", "cost": 500, "layer": "structure", "employees": 0, "bonus": None, "desc": "Massive Wand."},
    "wall_glass": {"name": "Wand Glas", "cost": 1000, "layer": "structure", "employees": 0, "bonus": None, "desc": "Transparente Wand. Sehr modern."},
    "door_glass": {"name": "Tür Glas", "cost": 1200, "layer": "structure", "employees": 0, "bonus": None, "desc": "Glastür."},
    "ergonomic_desk":{"name": "Ergonomischer Schreibtisch","cost": 2500,"layer": "furniture", "employees": 1, "bonus": None,       "desc": "Arbeitsplatz für Entwickler. Besser als Standard.", "req_tech": "Gesundes Arbeiten"},
    "sound_booth":   {"name": "Sound-Kabine",            "cost": 30000,  "layer": "furniture", "employees": 1, "bonus": "sound",      "desc": "+15% auf Sound-Bewertung.", "req_tech": "Studios & Kabinen"},
    "security_hub":  {"name": "Sicherheits-Zentrale",    "cost": 45000,  "layer": "furniture", "employees": 0, "bonus": "security",   "desc": "Verringert die Chance auf Industriespionage und Abwerbeversuche um 50%.", "req_tech": "Investment & M&A"},
    "legal_desk":    {"name": "Rechtsabteilung",         "cost": 65000,  "layer": "furniture", "employees": 1, "bonus": "legal_protection", "desc": "Erschwert Abwerbeversuche massiv und schützt Top-Mitarbeiter.", "req_tech": "Arbeitsrecht-Experten"},
    "intel_station": {"name": "Marktforschungs-Station", "cost": 85000,  "layer": "furniture", "employees": 1, "bonus": "competitor_intel", "desc": "Analysiert Konkurrenz-Projekte und warnt vor Genre-Sniping.", "req_tech": "Geheimdienst-Netzwerk"},
    "pr_desk":       {"name": "PR-Zentrale",             "cost": 40000,  "layer": "furniture", "employees": 1, "bonus": "pr_defense", "desc": "Reduziert Hype-Verlust durch konkurrierende Veröffentlichungen.", "req_tech": "Krisenmanagement"},
    "gold_record":   {"name": "Goldene Schallplatte",    "cost": 0,      "layer": "structure", "employees": 0, "bonus": None,         "desc": "Deine erste Million verkaufte Exemplare! +10 Moral.", "morale_bonus": 10},
    "master_tape":   {"name": "Master-Bandmaschine",     "cost": 5000,   "layer": "furniture", "employees": 0, "bonus": "sound",      "desc": "Klassische Analog-Technik. +5% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 1"},
}

# Rückwärtskompatibilität für bestehende System-Methoden
OFFICE_ROOMS = [dict(id=k, **v) for k, v in BUILD_OBJECTS.items()]

# ============================================================
# SPIELGRÖSSE
# ============================================================
GAME_SIZES = [
    {
        "name": "Klein",
        "cost_multi": 0.5,
        "time_multi": 0.5,
        "revenue_multi": 0.4,
        "slider_budget": 20,
        "min_employees": 0,
        "description": "Ein kleines Indie-Spiel. Günstig, schnell, aber weniger Umsatzpotenzial.",
    },
    {
        "name": "Mittel",
        "cost_multi": 1.0,
        "time_multi": 1.0,
        "revenue_multi": 1.0,
        "slider_budget": 30,
        "min_employees": 0,
        "description": "Ein normales Spiel. Standardkosten und Umsatz.",
    },
    {
        "name": "Groß",
        "cost_multi": 2.0,
        "time_multi": 1.5,
        "revenue_multi": 2.5,
        "slider_budget": 40,
        "min_employees": 3,
        "description": "Ein großes Spiel. Höhere Kosten, aber deutlich mehr Umsatz. Mindestens 3 Mitarbeiter.",
    },
    {
        "name": "AAA",
        "cost_multi": 4.0,
        "time_multi": 2.0,
        "revenue_multi": 5.0,
        "slider_budget": 50,
        "min_employees": 6,
        "min_tech_level": 5,
        "description": "Ein Blockbuster. Enorme Kosten, aber riesiges Umsatzpotenzial. Mindestens 6 Mitarbeiter, Tech-Level 5.",
    },
    {
        "name": "MMO",
        "cost_multi": 8.0,
        "time_multi": 3.0,
        "revenue_multi": 1.0, # Revenue comes from subscriptions
        "slider_budget": 60,
        "min_employees": 10,
        "min_tech_level": 6,
        "req_tech": "Live-Service Architektur",
        "description": "Ein Live-Service Spiel. Laufende Serverkosten, aber stetige Abo-Einnahmen. Benötigt Tech-Level 6 und spezielle Technologie.",
    },
]

# ============================================================
# MARKETING-KAMPAGNEN
# ============================================================
MARKETING_CAMPAIGNS = [
    {
        "name": "Kein Marketing",
        "cost": 0,
        "sales_multi": 1.0,
        "fan_multi": 1.0,
        "description": "Ohne Marketing-Kampagne.",
    },
    {
        "name": "Kleine Kampagne",
        "cost": 10000,
        "sales_multi": 1.3,
        "fan_multi": 1.2,
        "description": "Online-Werbung und Social Media. Kosten: 10.000 Euro.",
    },
    {
        "name": "Mittlere Kampagne",
        "cost": 40000,
        "sales_multi": 1.8,
        "fan_multi": 1.5,
        "description": "Werbung plus Messe-Auftritt. Kosten: 40.000 Euro.",
    },
    {
        "name": "Große Kampagne",
        "cost": 100000,
        "sales_multi": 2.5,
        "fan_multi": 2.0,
        "description": "TV-Werbung, große Messe, Influencer. Kosten: 100.000 Euro.",
    },
]

# ============================================================
# TRAINING
# ============================================================
TRAINING_OPTIONS = [
    {
        "name": "Workshop",
        "skill_boost": 5,
        "cost": 5000,
        "lock_weeks": 1,   # 1 Woche gesperrt
        "description": "Ein Workshop. +5 Skill-Punkte auf den Hauptbereich. Dauer: 1 Woche.",
    },
    {
        "name": "Fortbildung",
        "skill_boost": 10,
        "cost": 15000,
        "lock_weeks": 3,   # 3 Wochen gesperrt
        "description": "Eine umfangreiche Fortbildung. +10 Skill-Punkte auf den Hauptbereich. Dauer: 3 Wochen.",
    },
    {
        "name": "Experten-Seminar",
        "skill_boost": 20,
        "cost": 40000,
        "lock_weeks": 6,   # 6 Wochen gesperrt
        "description": "Ein Experten-Seminar. +20 Skill-Punkte auf den Hauptbereich. Dauer: 6 Wochen.",
    },
    {
        "name": "Spezialisierungskurs",
        "skill_boost": 0,
        "cost": 100000,
        "lock_weeks": 10,  # 10 Wochen gesperrt
        "description": "Der Meister-Kurs. Verleiht dem Mitarbeiter eine sehr starke, dauerhafte Experten-Eigenschaft. Dauer: 10 Wochen.",
        "is_specialization": True
    },
]


# ============================================================
# MARKTTRENDS (dynamisch wechselnd)
# ============================================================
TREND_TOPICS = [
    {"topic": "Zombies",     "text": "Zombies sind gerade im Trend!"},
    {"topic": "Weltraum",    "text": "Weltraum-Spiele sind total beliebt!"},
    {"topic": "Fantasy",     "text": "Fantasy erlebt ein Revival!"},
    {"topic": "Cyberpunk",   "text": "Cyberpunk ist der heißeste Trend!"},
    {"topic": "Horror",      "text": "Horror-Spiele boomen gerade!"},
    {"topic": "Sport",       "text": "Sport-Spiele verkaufen sich wie verrückt!"},
    {"topic": "Superheld",   "text": "Superhelden-Spiele sind mega populär!"},
    {"topic": "Piraten",     "text": "Piraten-Spiele sind wieder auf Kurs!"},
]

TREND_GENRES = [
    {"genre": "Action",      "text": "Action-Spiele dominieren die Charts!"},
    {"genre": "RPG",         "text": "RPGs sind extrem beliebt!"},
    {"genre": "Simulation",  "text": "Simulationsspiele sind der neue Hit!"},
    {"genre": "Casual",      "text": "Casual-Games erreichen die breite Masse!"},
    {"genre": "Strategie",   "text": "Strategiespiele erleben einen Boom!"},
]


# PUBLISHER
PUBLISHERS = [
    {
        "name": "publisher_global",
        "description": "publisher_global_desc",
        "advance": 5000,
        "royalty": 0.40,
        "min_score": 6
    },
    {
        "name": "publisher_titan",
        "description": "publisher_titan_desc",
        "advance": 25000,
        "royalty": 0.60,
        "min_score": 8
    },
    {
        "name": "publisher_star",
        "description": "publisher_star_desc",
        "advance": 1000,
        "royalty": 0.20,
        "min_score": 4
    }
]

# MARKETING-OPTIONEN PH_5
MARKETING_OPTIONS_PH5 = [
    {"name": "marketing_social", "cost": 500, "hype": 10, "description": "marketing_social_desc"},
    {"name": "marketing_web", "cost": 2500, "hype": 25, "description": "marketing_web_desc"},
    {"name": "marketing_tv", "cost": 15000, "hype": 70, "description": "marketing_tv_desc"},
    {"name": "marketing_pr", "cost": 50000, "hype": 150, "description": "marketing_pr_desc"},
]

# ============================================================
# HISTORISCHE JAHRESEVENTS (wird per Jahreswechsel ausgelöst)



# ============================================================
# TEMPLATES (E-Mails & Reviews)
# ============================================================
MAIL_TEMPLATES = {
    "bug_report": {
        "subject": "subject_bug_report",
        "body": "body_bug_report",
    },
    "fan_praise": {
        "subject": "subject_fan_praise",
        "body": "body_fan_praise",
    }
}

REVIEW_TEMPLATES = {
    "intro": [
        "Wir haben uns '{game}' von {company} genau angesehen.",
        "Endlich ist '{game}' da. Hat sich das Warten gelohnt?",
        "Heute im Test: Das neue Werk von {company} namens '{game}'.",
    ],
    "positive": [
        "Die Kombination aus {topic} und {genre} ist ein genialer Schachzug.",
        "Ein echtes Meisterwerk für alle Fans von {genre}-Spielen.",
        "Selten hat uns ein Spiel mit dem Thema {topic} so gefesselt.",
    ],
    "negative": [
        "Leider wirkt die Verknüpfung von {topic} und {genre} sehr weit hergeholt.",
        "Hier hat man sich bei der Themenwahl deutlich vergriffen.",
        "Thematisch und spielerisch leider eine Enttäuschung.",
    ],
    "conclusion": [
        "Ein Muss für jede Spielesammlung.",
        "Gute Unterhaltung für zwischendurch.",
        "Leider nur Durchschnitt.",
        "Ein Titel, den man getrost ignorieren kann.",
    ]
}


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

# ============================================================
# ZUFÄLLIGE MARKTEREIGNISSE
# Sofortige Events + dauerhafte Events (Phase 8)
# ============================================================
RANDOM_EVENTS = [
    # --- Sofortige Events (money/fans) ---
    {
        "id": "expo",
        "effect": "fans",
        "value": 500,
    },
    {
        "id": "boom",
        "effect": "money",
        "value": 15000,
    },
    {
        "id": "recession",
        "effect": "money",
        "value": -10000,
    },
    {
        "id": "retro",
        "effect": "fans",
        "value": 300,
    },
    {
        "id": "award",
        "effect": "fans",
        "value": 1000,
    },
    {
        "id": "tax",
        "effect": "money",
        "value": -12000,
    },
    {
        "id": "investor",
        "effect": "money",
        "value": 25000,
    },
    {
        "id": "viral",
        "effect": "fans",
        "value": 2000,
    },
    {
        "id": "server_crash",
        "effect": "fans",
        "value": -500,
    },
    # Neue Events (v2.4)
    {
        "id": "indie_award",
        "effect": "fans",
        "value": 1500,
    },
    {
        "id": "talent_drought",
        "effect": "money",
        "value": -8000,
    },
    {
        "id": "fan_tournament",
        "effect": "fans",
        "value": 3000,
    },
    {
        "id": "celebrity_plays",
        "effect": "fans",
        "value": 5000,
    },
    {
        "id": "tax_refund",
        "effect": "money",
        "value": 18000,
    },
    {
        "id": "crowdfunding",
        "effect": "money",
        "value": 30000,
    },
    {
        "id": "gamescom",
        "effect": "hype",
        "value": 40,
    },
    {
        "id": "summer_slump",
        "effect": "fans",
        "value": -800,
    },
    {
        "id": "christmas_rush",
        "effect": "money",
        "value": 20000,
    },
    {
        "id": "anniversary",
        "effect": "fans",
        "value": 2500,
    },
    {
        "id": "plagiat_lawsuit",
        "effect": "money",
        "value": -25000,
    },
    {
        "id": "industry_conference",
        "effect": "hype",
        "value": 25,
    },
    {
        "id": "super_review",
        "effect": "fans",
        "value": 4000,
    },
    {
        "id": "hardware_failure",
        "effect": "money",
        "value": -15000,
    },
    # --- Dauerhafte Events (mit duration) ---
    {
        "id": "hacker_attack",
        "type": "negative",
        "duration": 4,
        "effect": "sales_drop",
        "multiplier": 0.5
    },
    {
        "id": "viral_post",
        "type": "positive",
        "duration": 2,
        "effect": "hype_boost",
        "hype_amount": 50
    },
    {
        "id": "industry_burnout",
        "type": "negative",
        "duration": 3,
        "effect": "dev_speed_drop",
        "multiplier": 0.5
    },
    {
        "id": "talent_boom",
        "type": "positive",
        "duration": 4,
        "effect": "dev_speed_boost",
        "multiplier": 1.5
    },
    {
        "id": "market_hype",
        "type": "positive",
        "duration": 3,
        "effect": "sales_boost",
        "multiplier": 1.4
    },
]


# ============================================================
# HISTORISCHE THEMEN (Freigeschaltet per Spieljahr 1930-2026)
# unlock_year = erstes Jahr, in dem das Thema nutzbar ist
# hype_level: 1=Gering, 2=Mittel, 3=Hoch, 4=Extrem, 5=Gigantisch
# synergy: Genre, das am besten passt
# ============================================================
HISTORICAL_TOPICS = [
    # === Die Pionier-Dekade 1930–1939 ===
    {"name": "Abakus",          "unlock_year": 1930, "synergy": "Puzzle",    "hype_level": 1},
    {"name": "Radio-Drama",     "unlock_year": 1930, "synergy": "Abenteuer", "hype_level": 4},
    {"name": "Logistik",        "unlock_year": 1930, "synergy": "Strategie", "hype_level": 3},
    {"name": "Schach",          "unlock_year": 1930, "synergy": "Puzzle",    "hype_level": 2},
    {"name": "Mathematik",      "unlock_year": 1930, "synergy": "Puzzle",    "hype_level": 3},
    {"name": "Swing-Musik",     "unlock_year": 1931, "synergy": "Casual",    "hype_level": 4},
    {"name": "Astronomie",      "unlock_year": 1931, "synergy": "Strategie", "hype_level": 2},
    {"name": "Landwirtschaft",  "unlock_year": 1931, "synergy": "Simulation","hype_level": 2},
    {"name": "Kochen",          "unlock_year": 1932, "synergy": "Simulation","hype_level": 1},
    {"name": "Hörspiel",        "unlock_year": 1932, "synergy": "Abenteuer", "hype_level": 5},
    {"name": "Politik",         "unlock_year": 1932, "synergy": "Strategie", "hype_level": 2},
    {"name": "Detektiv",        "unlock_year": 1933, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Kartenspiele",    "unlock_year": 1933, "synergy": "Puzzle",    "hype_level": 3},
    {"name": "Architektur",     "unlock_year": 1934, "synergy": "Simulation","hype_level": 2},
    {"name": "Postwesen",       "unlock_year": 1934, "synergy": "Simulation","hype_level": 1},
    {"name": "Zirkus",          "unlock_year": 1935, "synergy": "Casual",    "hype_level": 2},
    {"name": "Tonbandgerät",    "unlock_year": 1935, "synergy": "Simulation","hype_level": 3},
    {"name": "Bergbau",         "unlock_year": 1935, "synergy": "Simulation","hype_level": 2},
    {"name": "Eisenbahn",       "unlock_year": 1936, "synergy": "Simulation","hype_level": 3},
    {"name": "Seefahrt",        "unlock_year": 1936, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Kryptografie",    "unlock_year": 1937, "synergy": "Puzzle",    "hype_level": 4},
    {"name": "Feuerwehr",       "unlock_year": 1937, "synergy": "Simulation","hype_level": 2},
    {"name": "Mars-Invasion",   "unlock_year": 1938, "synergy": "Action",    "hype_level": 4},
    {"name": "Zauberei",        "unlock_year": 1938, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Militär",         "unlock_year": 1939, "synergy": "Strategie", "hype_level": 4},
    {"name": "Chemie",          "unlock_year": 1939, "synergy": "Puzzle",    "hype_level": 2},
    {"name": "Brettspiel",      "unlock_year": 1935, "synergy": "Puzzle",    "hype_level": 3},
    {"name": "Leichtathletik",  "unlock_year": 1936, "synergy": "Sport",     "hype_level": 3},
    {"name": "Aliens",          "unlock_year": 1938, "synergy": "Action",    "hype_level": 4},
    {"name": "Pazifik-Krieg",   "unlock_year": 1941, "synergy": "Strategie", "hype_level": 4},
    {"name": "Frieden",         "unlock_year": 1945, "synergy": "Casual",    "hype_level": 5},
    {"name": "Pioniere",        "unlock_year": 1946, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Wissenschaft",    "unlock_year": 1953, "synergy": "Simulation","hype_level": 4},
    {"name": "Themenpark",      "unlock_year": 1955, "synergy": "Simulation","hype_level": 4},
    {"name": "Mode/Puppen",     "unlock_year": 1959, "synergy": "Casual",    "hype_level": 3},
    {"name": "Freiheit",        "unlock_year": 1960, "synergy": "Simulation","hype_level": 2},
    {"name": "Band",            "unlock_year": 1964, "synergy": "Casual",    "hype_level": 4},
    {"name": "Chaos/Protest",   "unlock_year": 1965, "synergy": "Simulation","hype_level": 2},
    {"name": "Natur",           "unlock_year": 1970, "synergy": "Simulation","hype_level": 3},
    {"name": "Lernen",          "unlock_year": 1971, "synergy": "Puzzle",    "hype_level": 2},

    # === Die Aufbau-Jahre 1940–1959 ===
    {"name": "U-Boot",          "unlock_year": 1940, "synergy": "Simulation","hype_level": 3},
    {"name": "Magnetband",      "unlock_year": 1940, "synergy": "Simulation","hype_level": 3},
    {"name": "Mehrspuraufnahme","unlock_year": 1941, "synergy": "Simulation","hype_level": 4},
    {"name": "Spionage",        "unlock_year": 1942, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Panzer",          "unlock_year": 1943, "synergy": "Simulation","hype_level": 3},
    {"name": "Fallschirmjäger", "unlock_year": 1944, "synergy": "Action",    "hype_level": 2},
    {"name": "Wiederaufbau",    "unlock_year": 1945, "synergy": "Simulation","hype_level": 3},
    {"name": "Journalismus",    "unlock_year": 1946, "synergy": "Strategie", "hype_level": 2},
    {"name": "UFOs",            "unlock_year": 1947, "synergy": "Abenteuer", "hype_level": 4},
    {"name": "Vinyl-Schallplatte","unlock_year": 1948, "synergy": "Casual",  "hype_level": 5},
    {"name": "Roboter",         "unlock_year": 1948, "synergy": "Action",    "hype_level": 3},
    {"name": "Dschungel",       "unlock_year": 1949, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Rock 'n' Roll",   "unlock_year": 1950, "synergy": "Casual",    "hype_level": 5},
    {"name": "Archäologie",     "unlock_year": 1950, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Weltraum",        "unlock_year": 1951, "synergy": "Simulation","hype_level": 4},
    {"name": "Transistorradio", "unlock_year": 1952, "synergy": "Simulation","hype_level": 4},
    {"name": "Wilder Westen",   "unlock_year": 1952, "synergy": "Action",    "hype_level": 3},
    {"name": "Bergsteigen",     "unlock_year": 1953, "synergy": "Sport",     "hype_level": 2},
    {"name": "Fußball",         "unlock_year": 1954, "synergy": "Sport",     "hype_level": 5},
    {"name": "Vergnügungspark", "unlock_year": 1955, "synergy": "Simulation","hype_level": 3},
    {"name": "Monster",         "unlock_year": 1956, "synergy": "Horror",    "hype_level": 2},
    {"name": "Satelliten",      "unlock_year": 1957, "synergy": "Simulation","hype_level": 3},
    {"name": "Tennis",          "unlock_year": 1958, "synergy": "Sport",     "hype_level": 4},
    {"name": "Rennwagen",       "unlock_year": 1959, "synergy": "Rennspiel", "hype_level": 3},

    # === Pop-Kultur Ära 1960–1979 ===
    {"name": "Tiefsee",         "unlock_year": 1960, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Stereo-Sound",    "unlock_year": 1960, "synergy": "Simulation","hype_level": 4},
    {"name": "Mafia",           "unlock_year": 1961, "synergy": "Action",    "hype_level": 3},
    {"name": "Fantasy",         "unlock_year": 1962, "synergy": "RPG",       "hype_level": 3},
    {"name": "Musikkassette",   "unlock_year": 1963, "synergy": "Casual",    "hype_level": 5},
    {"name": "Agenten",         "unlock_year": 1963, "synergy": "Abenteuer", "hype_level": 4},
    {"name": "Popstars",        "unlock_year": 1964, "synergy": "Casual",    "hype_level": 3},
    {"name": "Dinosaurier",     "unlock_year": 1965, "synergy": "Action",    "hype_level": 4},
    {"name": "Ninjas",          "unlock_year": 1966, "synergy": "Action",    "hype_level": 3},
    {"name": "Hippies",         "unlock_year": 1967, "synergy": "Simulation","hype_level": 2},
    {"name": "Weltrevolution",  "unlock_year": 1968, "synergy": "Strategie", "hype_level": 3},
    {"name": "Mondbasis",       "unlock_year": 1969, "synergy": "Simulation","hype_level": 5},
    {"name": "Synthesizer",     "unlock_year": 1970, "synergy": "Puzzle",    "hype_level": 3},
    {"name": "Kung-Fu",         "unlock_year": 1970, "synergy": "Kampfspiel","hype_level": 3},
    {"name": "Piraten",         "unlock_year": 1971, "synergy": "Abenteuer", "hype_level": 4},
    {"name": "Basketball",      "unlock_year": 1972, "synergy": "Sport",     "hype_level": 2},
    {"name": "Motorrad",        "unlock_year": 1973, "synergy": "Rennspiel", "hype_level": 3},
    {"name": "Elektronik-Pop",  "unlock_year": 1974, "synergy": "Puzzle",    "hype_level": 5},
    {"name": "Verliese",        "unlock_year": 1974, "synergy": "RPG",       "hype_level": 4},
    {"name": "Polizei",         "unlock_year": 1975, "synergy": "Action",    "hype_level": 2},
    {"name": "Alien-Jagd",      "unlock_year": 1976, "synergy": "Action",    "hype_level": 3},
    {"name": "Laserschwert",    "unlock_year": 1977, "synergy": "Action",    "hype_level": 4},
    {"name": "Invaders",        "unlock_year": 1978, "synergy": "Action",    "hype_level": 4},
    {"name": "Horrorhaus",      "unlock_year": 1979, "synergy": "Horror",    "hype_level": 3},

    # === Digitale Explosion 1980–1999 ===
    {"name": "Gelbe Fresspunkte","unlock_year": 1980, "synergy": "Puzzle",   "hype_level": 5},
    {"name": "Walkman",         "unlock_year": 1980, "synergy": "Casual",    "hype_level": 5},
    {"name": "Büro-Alltag",     "unlock_year": 1981, "synergy": "Simulation","hype_level": 1},
    {"name": "CD-Technologie",  "unlock_year": 1982, "synergy": "Simulation","hype_level": 5},
    {"name": "Cyberpunk",       "unlock_year": 1982, "synergy": "RPG",       "hype_level": 4},
    {"name": "Vampire",         "unlock_year": 1983, "synergy": "Horror",    "hype_level": 3},
    {"name": "Breakdance",      "unlock_year": 1984, "synergy": "Casual",    "hype_level": 2},
    {"name": "Klempner",        "unlock_year": 1985, "synergy": "Action",    "hype_level": 5},
    {"name": "Postapokalypse",  "unlock_year": 1986, "synergy": "RPG",       "hype_level": 3},
    {"name": "Mechs",           "unlock_year": 1987, "synergy": "Action",    "hype_level": 4},
    {"name": "Skateboarding",   "unlock_year": 1988, "synergy": "Sport",     "hype_level": 3},
    {"name": "Taschenmonster",  "unlock_year": 1989, "synergy": "RPG",       "hype_level": 5},
    {"name": "Digital-Audio-Workstation","unlock_year": 1991, "synergy": "Simulation","hype_level": 4},
    {"name": "Techno-Rave",     "unlock_year": 1990, "synergy": "Action",    "hype_level": 4},
    {"name": "Krankenhaus",     "unlock_year": 1990, "synergy": "Simulation","hype_level": 3},
    {"name": "Freizeitpark",    "unlock_year": 1991, "synergy": "Simulation","hype_level": 4},
    {"name": "Mars-Shooter",    "unlock_year": 1992, "synergy": "Action",    "hype_level": 5},
    {"name": "Urzeit/Survival", "unlock_year": 1993, "synergy": "Simulation","hype_level": 3},
    {"name": "Anime",           "unlock_year": 1994, "synergy": "RPG",       "hype_level": 3},
    {"name": "Hacking",         "unlock_year": 1995, "synergy": "Puzzle",    "hype_level": 4},
    {"name": "Stealth-Agent",   "unlock_year": 1996, "synergy": "Action",    "hype_level": 4},
    {"name": "Internet-Radio",  "unlock_year": 1997, "synergy": "Simulation","hype_level": 3},
    {"name": "Elfen & Orks",    "unlock_year": 1997, "synergy": "RPG",       "hype_level": 3},
    {"name": "Survival-Insel",  "unlock_year": 1998, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Skandal-TV",      "unlock_year": 1999, "synergy": "Simulation","hype_level": 2},

    # === Neues Jahrtausend 2000–2015 ===
    {"name": "Lebens-Sim",      "unlock_year": 2000, "synergy": "Simulation","hype_level": 5},
    {"name": "MP3-Player",      "unlock_year": 2000, "synergy": "Casual",    "hype_level": 5},
    {"name": "Zombie-Hype",     "unlock_year": 2001, "synergy": "Horror",    "hype_level": 4},
    {"name": "Musik-Download",  "unlock_year": 2003, "synergy": "Casual",    "hype_level": 4},
    {"name": "Parkplatz-Manager","unlock_year": 2002, "synergy": "Simulation","hype_level": 1},
    {"name": "E-Sport",         "unlock_year": 2003, "synergy": "Action",    "hype_level": 3},
    {"name": "Zauberschule",    "unlock_year": 2004, "synergy": "RPG",       "hype_level": 4},
    {"name": "Podcast-Boom",    "unlock_year": 2005, "synergy": "Simulation","hype_level": 3},
    {"name": "Sandbox/Voxel",   "unlock_year": 2005, "synergy": "Abenteuer", "hype_level": 5},
    {"name": "Wikinger",        "unlock_year": 2006, "synergy": "Action",    "hype_level": 4},
    {"name": "Smartphones",     "unlock_year": 2007, "synergy": "Puzzle",    "hype_level": 3},
    {"name": "Musik-Streaming", "unlock_year": 2008, "synergy": "Simulation","hype_level": 5},
    {"name": "Freerunning",     "unlock_year": 2008, "synergy": "Action",    "hype_level": 2},
    {"name": "Block-Bauen",     "unlock_year": 2009, "synergy": "Abenteuer", "hype_level": 5},
    {"name": "Streaming-Rev",   "unlock_year": 2010, "synergy": "Simulation","hype_level": 5},
    {"name": "Social Network",  "unlock_year": 2010, "synergy": "Simulation","hype_level": 3},
    {"name": "Hi-Res Audio",    "unlock_year": 2012, "synergy": "Simulation","hype_level": 3},
    {"name": "Indie-Entwickler","unlock_year": 2011, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Battle-Royale",   "unlock_year": 2012, "synergy": "Action",    "hype_level": 5},
    {"name": "VR-Simulation",   "unlock_year": 2013, "synergy": "Simulation","hype_level": 3},
    {"name": "Farming-Hype",    "unlock_year": 2014, "synergy": "Simulation","hype_level": 4},
    {"name": "ASMR",            "unlock_year": 2015, "synergy": "Simulation","hype_level": 2},
    {"name": "Cyber-Krieg",     "unlock_year": 2015, "synergy": "Strategie", "hype_level": 3},

    # === Die Zukunft 2016–2026 ===
    {"name": "3D-Audio",        "unlock_year": 2017, "synergy": "Action",    "hype_level": 4},
    {"name": "AR-Jagd",         "unlock_year": 2016, "synergy": "Action",    "hype_level": 3},
    {"name": "Krypto-Mining",   "unlock_year": 2017, "synergy": "Strategie", "hype_level": 2},
    {"name": "Mars-Kolonisierung","unlock_year": 2018,"synergy": "Simulation","hype_level": 4},
    {"name": "Streaming-Star",  "unlock_year": 2019, "synergy": "Simulation","hype_level": 3},
    {"name": "KI-Dystopie",     "unlock_year": 2020, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Spatial-Audio",   "unlock_year": 2020, "synergy": "Action",    "hype_level": 4},
    {"name": "NFT-Sammeln",     "unlock_year": 2021, "synergy": "Strategie", "hype_level": 1},
    {"name": "KI-Komposition",  "unlock_year": 2022, "synergy": "Simulation","hype_level": 5},
    {"name": "Metaverse",       "unlock_year": 2022, "synergy": "Simulation","hype_level": 2},
    {"name": "KI-Utopie",       "unlock_year": 2023, "synergy": "Strategie", "hype_level": 4},
    {"name": "KI-Stimmen",      "unlock_year": 2024, "synergy": "Simulation","hype_level": 5},
    {"name": "Endzeit-Bote",    "unlock_year": 2024, "synergy": "Action",    "hype_level": 3},
    {"name": "Gen-Labor",       "unlock_year": 2025, "synergy": "Simulation","hype_level": 4},
    {"name": "Holo-Konzerte",   "unlock_year": 2025, "synergy": "Casual",    "hype_level": 4},
    {"name": "Neural-Link",     "unlock_year": 2026, "synergy": "RPG",       "hype_level": 5},
    # === Zusätzliche Audio-Fokus Themen ===
    {"name": "Hörbuch-Boom",    "unlock_year": 2000, "synergy": "Simulation","hype_level": 4},
    {"name": "SoundCloud-Rap",  "unlock_year": 2012, "synergy": "Casual",    "hype_level": 3},
    {"name": "Vinyl-Revival",   "unlock_year": 2015, "synergy": "Casual",    "hype_level": 4},
    {"name": "Auto-Tune",       "unlock_year": 1998, "synergy": "Casual",    "hype_level": 4},
    {"name": "Multiroom-Audio", "unlock_year": 2010, "synergy": "Simulation","hype_level": 3},
    {"name": "Dolby Atmos",     "unlock_year": 2012, "synergy": "Action",    "hype_level": 4},
    {"name": "Noise Cancelling","unlock_year": 2000, "synergy": "Simulation","hype_level": 3},
    {"name": "Hörgeräte-Tech",  "unlock_year": 1950, "synergy": "Simulation","hype_level": 2},
    {"name": "Echo-Effekt",     "unlock_year": 1960, "synergy": "Casual",    "hype_level": 3},
    {"name": "Reverb-Kammern",  "unlock_year": 1945, "synergy": "Simulation","hype_level": 2},
    {"name": "Film-Sync",       "unlock_year": 1930, "synergy": "Action",    "hype_level": 3},
    {"name": "Surround-Sound",  "unlock_year": 1975, "synergy": "Action",    "hype_level": 4},
    {"name": "Audio-Fingerprint","unlock_year": 2005, "synergy": "Puzzle",   "hype_level": 3},
    {"name": "Algo-Playlists",  "unlock_year": 2015, "synergy": "Strategie", "hype_level": 4},
    {"name": "Lo-Fi Beats",     "unlock_year": 2017, "synergy": "Casual",    "hype_level": 4},
    {"name": "True Wireless",   "unlock_year": 2016, "synergy": "Simulation","hype_level": 4},
    {"name": "Podcasting 2.0",  "unlock_year": 2020, "synergy": "Simulation","hype_level": 3},
    {"name": "KI-Mastering",    "unlock_year": 2021, "synergy": "Simulation","hype_level": 5},
    {"name": "Audio-Deepfakes", "unlock_year": 2023, "synergy": "Abenteuer", "hype_level": 4},
    {"name": "Neuro-Interface", "unlock_year": 2026, "synergy": "RPG",       "hype_level": 5},
]


def get_historical_topics_for_year(calendar_year):
    """Gibt alle historischen Themen zurück, die bis zum gegebenen Jahr verfügbar sind."""
    return [t for t in HISTORICAL_TOPICS if t["unlock_year"] <= calendar_year]


def get_newly_unlocked_topics(calendar_year):
    """Gibt alle Themen zurück, die GENAU in diesem Jahr neu verfügbar werden."""
    return [t for t in HISTORICAL_TOPICS if t["unlock_year"] == calendar_year]


# ============================================================
# HISTORISCHE JAHRES-EREIGNISSE
# ============================================================
YEAR_EVENTS = {
    1930: {"text": "event_1930", "effect": "money_multi", "value": 0.8},    # Weltwirtschaftskrise
    1931: {"text": "event_1931", "effect": "rp", "value": 25},            # Logic-Contest
    1932: {"text": "event_1932", "effect": "trend_topic", "value": "Sport"}, # Olympia
    1933: {"text": "event_1933", "effect": "sales_multi", "value": 1.2},   # Ende Prohibition
    1934: {"text": "event_1934", "effect": "hype", "value": 15},           # Radar
    1935: {"text": "event_1935", "effect": "trend_topic", "value": "Brettspiel"}, # Monopoly
    1936: {"text": "event_1936", "effect": "trend_topic", "value": "Leichtathletik"}, # Jesse Owens
    1937: {"text": "event_1937", "effect": "hype_multi", "value": 0.5, "topic": "Luftfahrt"}, # Luftschiff-Unglück
    1938: {"text": "event_1938", "effect": "trend_topic", "value": "Aliens"}, # Mars-Hörspiel
    1939: {"text": "event_1939", "effect": "tax_increase", "value": 0.1},  # WWII Ausbruch
    1940: {"text": "event_1940", "effect": "logic_boost", "value": 1.3},    # Enigma
    1941: {"text": "event_1941", "effect": "trend_topic", "value": "Pazifik-Krieg"}, # Pearl Harbor
    1942: {"text": "event_1942", "effect": "hype", "value": 200, "topic": "Mathematik"}, # Zuse Z3
    1943: {"text": "event_1943", "effect": "trend_topic", "value": "Agenten"}, # Casablanca
    1944: {"text": "event_1944", "effect": "trend_topic", "value": "Militär"}, # D-Day
    1945: {"text": "event_1945", "effect": "sales_multi", "value": 2.0},   # Kriegsende
    1946: {"text": "event_1946", "effect": "trend_topic", "value": "Pioniere"}, # Erster Linienflug
    1947: {"text": "event_1947", "effect": "trend_topic", "value": "UFOs"},  # Roswell
    1948: {"text": "event_1948", "effect": "money", "value": 1000},        # Marshall-Plan
    1949: {"text": "event_1949", "effect": "unlock_tech", "value": "Sound-Forschung"}, # LP-Platte
    1950: {"text": "event_1950", "effect": "trend_topic", "value": "Militär"}, # Koreakrieg
    1951: {"text": "event_1951", "effect": "prestige", "value": 50},       # UNIVAC
    1952: {"text": "event_1952", "effect": "hype", "value": 40},           # OXO (Erstes Game)
    1953: {"text": "event_1953", "effect": "trend_topic", "value": "Wissenschaft"}, # DNA
    1954: {"text": "event_1954", "effect": "trend_topic", "value": "Fußball"}, # Wunder von Bern
    1955: {"text": "event_1955", "effect": "trend_topic", "value": "Vergnügungspark"}, # Disneyland
    1956: {"text": "event_1956", "effect": "trend_topic", "value": "Rock 'n' Roll"}, # Elvis
    1957: {"text": "event_1957", "effect": "hype", "value": 500, "topic": "Weltraum"}, # Sputnik
    1958: {"text": "event_1958", "effect": "hype", "value": 30},           # Tennis for Two
    1959: {"text": "event_1959", "effect": "trend_topic", "value": "Mode/Puppen"}, # Barbie
    1960: {"text": "event_1960", "effect": "trend_topic", "value": "Freiheit"}, # Pille
    1961: {"text": "event_1961", "effect": "money_multi", "value": 0.5},   # Mauerbau (Exportkosten)
    1962: {"text": "event_1962", "effect": "hype", "value": 50},           # Spacewar!
    1963: {"text": "event_1963", "effect": "sales_multi", "value": 0.7},   # Kennedy
    1964: {"text": "event_1964", "effect": "trend_topic", "value": "Band"}, # Beatles
    1965: {"text": "event_1965", "effect": "trend_topic", "value": "Chaos/Protest"}, # Vietnam
    1966: {"text": "event_1966", "effect": "unlock_genre", "value": "RPG"}, # Star Trek
    1967: {"text": "event_1967", "effect": "trend_topic", "value": "Hippies"}, # Summer of Love
    1968: {"text": "event_1968", "effect": "salary_increase", "value": 0.15}, # Mai-Unruhen
    1969: {"text": "event_1969", "effect": "hype", "value": 100},          # Apollo 11
    1970: {"text": "event_1970", "effect": "trend_topic", "value": "Natur"}, # Earth Day
    1971: {"text": "event_1971", "effect": "trend_topic", "value": "Lernen"}, # Oregon Trail
    1972: {"text": "event_1972", "effect": "market_boom", "value": 2.0},   # Pong
    1973: {"text": "event_1973", "effect": "cost_increase", "value": 0.5}, # Ölkrise
    1974: {"text": "event_1974", "effect": "unlock_genre", "value": "RPG"}, # D&D
    1975: {"text": "event_1975", "effect": "rival_boost", "value": 1.2},    # Bill Gates MS
    1976: {"text": "event_1976", "effect": "market_boom", "value": 1.5},   # Apple I
    1977: {"text": "event_1977", "effect": "trend_topic", "value": "Weltraum"}, # Star Wars
    1978: {"text": "event_1978", "effect": "trend_genre", "value": "Action"}, # Space Invaders
    1979: {"text": "event_1979", "effect": "unlock_tech", "value": "Sound-Marketing"}, # Walkman
    1980: {"text": "event_1980", "effect": "trend_genre", "value": "Puzzle"}, # Pac-Man
    1981: {"text": "event_1981", "effect": "hype", "value": 40},           # IBM PC
    1982: {"text": "event_1982", "effect": "market_crash", "value": 0.1},  # Crash
    1983: {"text": "event_1983", "effect": "quality_penalty", "value": 2.0}, # Dragon's Lair
    1984: {"text": "event_1984", "effect": "hype", "value": 300, "topic": "Puzzle"}, # Tetris
    1985: {"text": "event_1985", "effect": "trend_genre", "value": "Action"}, # Super Mario
    1986: {"text": "event_1986", "effect": "complexity_boost", "value": 1.2}, # Zelda
    1987: {"text": "event_1987", "effect": "story_boost", "value": 1.5},    # Final Fantasy
    1988: {"text": "event_1988", "effect": "graphics_standard", "value": 2}, # Mega Drive
    1989: {"text": "event_1989", "effect": "market_boom", "value": 1.3},   # Gameboy
    1990: {"text": "event_1990", "effect": "sales_multi", "value": 1.15},  # Mauerfall
    1991: {"text": "event_1991", "effect": "trend_genre", "value": "Kampfspiel"}, # Street Fighter II
    1992: {"text": "event_1992", "effect": "unlock_genre", "value": "Action"}, # Wolfenstein 3D
    1993: {"text": "event_1993", "effect": "censorship_risk", "value": 0.5}, # Doom
    1994: {"text": "event_1994", "effect": "medium_upgrade", "value": "CD-ROM"}, # PlayStation
    1995: {"text": "event_1995", "effect": "market_boom", "value": 1.4},   # Windows 95
    1996: {"text": "event_1996", "effect": "trend_topic", "value": "Monster"}, # Pokémon
    1997: {"text": "event_1997", "effect": "server_costs", "value": 2.0},   # Ultima Online
    1998: {"text": "event_1998", "effect": "trend_genre", "value": "Action"}, # Metal Gear Solid
    1999: {"text": "event_1999", "effect": "trend_topic", "value": "Simulation"}, # Matrix
    2000: {"text": "event_2000", "effect": "market_boom", "value": 1.5},   # PS2
    2001: {"text": "event_2001", "effect": "sales_multi", "value": 0.8},   # 9/11
    2002: {"text": "event_2002", "effect": "multiplayer_boost", "value": 1.5}, # Xbox Live
    2003: {"text": "event_2003", "effect": "digital_sales", "value": 1.2},  # Steam
    2004: {"text": "event_2004", "effect": "subscription_boom", "value": 2.0}, # WoW
    2005: {"text": "event_2005", "effect": "marketing_rev", "value": 1.5},  # YouTube
    2006: {"text": "event_2006", "effect": "trend_genre", "value": "Casual"}, # Wii
    2007: {"text": "event_2007", "effect": "market_shift", "value": "Casual"}, # iPhone
    2008: {"text": "event_2008", "effect": "interest_increase", "value": 0.2}, # Finanzkrise
    2009: {"text": "event_2009", "effect": "trend_topic", "value": "Sandbox/Voxel"}, # Minecraft
    2010: {"text": "event_2010", "effect": "market_boom", "value": 1.4},   # iPad
    2011: {"text": "event_2011", "effect": "streamer_impact", "value": 2.0}, # Twitch
    2012: {"text": "event_2012", "effect": "crowdfunding", "value": 1.5},  # Crowdfunding
    2013: {"text": "event_2013", "effect": "quality_standard", "value": 1.5}, # GTA V
    2014: {"text": "event_2014", "effect": "prestige", "value": 30},       # VR-Fieber
    2015: {"text": "event_2015", "effect": "story_standard", "value": 2.0}, # Witcher 3
    2016: {"text": "event_2016", "effect": "trend_topic", "value": "AR-Jagd"}, # Switch / AR
    2017: {"text": "event_2017", "effect": "trend_topic", "value": "Battle-Royale"}, # Battle Royale
    2018: {"text": "event_2018", "effect": "graphics_standard", "value": 3.0}, # Raytracing
    2019: {"text": "event_2019", "effect": "subscription_standard", "value": 1.5}, # Game Pass
    2020: {"text": "event_2020", "effect": "sales_multi", "value": 2.5},   # Pandemie
    2021: {"text": "event_2021", "effect": "crypto_crash", "value": 0.0},  # Krypto-Crash
    2022: {"text": "event_2022", "effect": "trend_difficulty", "value": "Hard"}, # Elden Ring
    2023: {"text": "event_2023", "effect": "dev_speed", "value": 1.5},     # KI-Explosion
    2024: {"text": "event_2024", "effect": "trend_topic", "value": "Mars-Kolonisierung"}, # Mars-Mission
    2025: {"text": "event_2025", "effect": "unlock_platform", "value": "Neural"}, # Cyber-Brain
    2026: {"text": "event_2026", "effect": "game_end", "value": 0},        # Neural-Sync
}


def get_year_event(year):
    """Gibt das historische Ereignis für ein bestimmtes Jahr zurück."""
    return YEAR_EVENTS.get(year)

# ============================================================
# ACHIEVEMENTS (Meilensteine)
# ============================================================
ACHIEVEMENTS = [
    {"id": "millionaire", "type": "money", "threshold": 1000000, "bonus_type": "fans", "bonus_value": 5000},
    {"id": "mega_millionaire", "type": "money", "threshold": 10000000, "bonus_type": "fans", "bonus_value": 50000},
    {"id": "first_aaa", "type": "game_size", "threshold": "AAA", "bonus_type": "hype", "bonus_value": 50},
    {"id": "star_dev", "type": "fans", "threshold": 1000000, "bonus_type": "money", "bonus_value": 500000},
    {"id": "masterpiece", "type": "score", "threshold": 10.0, "bonus_type": "hype", "bonus_value": 100},
    {"id": "goty_winner", "type": "goty", "threshold": 1, "bonus_type": "fans", "bonus_value": 10000},
    {"id": "inclusive_studio", "type": "accessibility", "threshold": 25, "bonus_type": "fans", "bonus_value": 2500},
    {"id": "accessibility_champion", "type": "accessibility", "threshold": 75, "bonus_type": "money", "bonus_value": 150000},
]

# ============================================================
# PHASE F: MERCHANDISE
# ============================================================
MERCH_TYPES = [
    {
        "name": "T-Shirts",
        "production_cost": 5,      # Kosten pro Stück
        "sell_price": 20,          # Verkaufspreis
        "hype_multi": 1.0,         # Wie schnell sie sich verkaufen (Basierend auf Game-Hype/Fans)
        "description": "Günstige Produktion, stetiger Absatz.",
    },
    {
        "name": "Plüschtiere",
        "production_cost": 10,
        "sell_price": 35,
        "hype_multi": 1.5,
        "description": "Mittlere Kosten. Fans lieben Plüschtiere ihrer Lieblingshelden.",
    },
    {
        "name": "Sammlerfiguren",
        "production_cost": 50,
        "sell_price": 150,
        "hype_multi": 0.5,         # Verkaufen sich langsamer, aber hohe Marge
        "description": "Teure Premium-Produktion für Hardcore-Fans.",
    },
]

# ============================================================
# PHASE F: E-SPORTS TURNIERE
# ============================================================
ESPORTS_TOURNAMENTS = [
    {
        "name": "Lokales Turnier",
        "cost": 50000,             # Veranstaltungs-Kosten
        "hype_bonus": 50,          # Hype für das Spiel (Push für Verkäufe/MMO-Zahlen)
        "fan_bonus": 5000,         # Neue Fans
        "min_game_sales": 10000,   # Spiel muss mind. X Mal verkauft sein (oder Spieler haben)
        "description": "Ein kleines lokales Turnier. Bringt ordentlich Hype.",
    },
    {
        "name": "Regionale Meisterschaft",
        "cost": 250000,
        "hype_bonus": 150,
        "fan_bonus": 25000,
        "min_game_sales": 100000,
        "description": "Großes Turnier mit ansprechendem Preispool.",
    },
    {
        "name": "World Championship",
        "cost": 1500000,
        "hype_bonus": 500,
        "fan_bonus": 150000,
        "min_game_sales": 1000000,
        "description": "Das gigantische E-Sports Jahreshighlight. Maximaler Hype!",
    },
]

# ============================================================
# BÜRO-UPGRADES (Phase 1)
# ============================================================
OFFICE_UPGRADES = [
    {
        "id": "coffee_machine",
        "name_key": "upgrade_coffee",
        "cost": 5000,
        "bonus": "morale_boost",
    },
    {
        "id": "ergonomic_chairs",
        "name_key": "upgrade_chairs",
        "cost": 15000,
        "bonus": "dev_speed",
    },
    {
        "id": "morale_room",
        "name_key": "upgrade_morale_room",
        "cost": 30000,
        "bonus": "morale_room",
    },
    {
        "id": "competitor_intel",
        "name_key": "upgrade_intel",
        "cost": 40000,
        "bonus": "competitor_intel",
    },
    {
        "id": "security",
        "name_key": "upgrade_security",
        "cost": 50000,
        "bonus": "security",
    },
    {
        "id": "pr_defense",
        "name_key": "upgrade_pr",
        "cost": 60000,
        "bonus": "pr_defense",
    },
    {
        "id": "legal_protection",
        "name_key": "upgrade_legal",
        "cost": 80000,
        "bonus": "legal_protection",
    },
    {
        "id": "campus_upgrade",
        "name_key": "upgrade_campus",
        "cost": 1000000,
        "bonus": "campus_morale",
    },

]



# ============================================================
# NEU: SPRACHUNTERSTÜTZUNG
# ============================================================
SUPPORTED_LANGUAGES = [
    {"id": "de", "name": "Deutsch", "cost_per_size": 1000},
    {"id": "en", "name": "Englisch", "cost_per_size": 1000},
    {"id": "fr", "name": "Französisch", "cost_per_size": 1500},
    {"id": "es", "name": "Spanisch", "cost_per_size": 1500},
    {"id": "it", "name": "Italienisch", "cost_per_size": 1500},
    {"id": "jp", "name": "Japanisch", "cost_per_size": 3000},
    {"id": "zh", "name": "Chinesisch", "cost_per_size": 3000},
]

# ============================================================
# NEU: BÜRO-SYSTEM (Raster & Räume)
# ============================================================
OFFICE_ROOM_TYPES = [
    {"id": "dev", "name": "Entwickler-Raum", "cost_per_tile": 500, "description": "Hier arbeiten Programmierer und Designer."},
    {"id": "sound", "name": "Tonstudio", "cost_per_tile": 1000, "description": "Erhöht die Sound-Qualität der Spiele."},
    {"id": "research", "name": "Forschung", "cost_per_tile": 800, "description": "Beschleunigt die Forschung neuer Technologien."},
    {"id": "break", "name": "Aufenthaltsraum", "cost_per_tile": 400, "description": "Regeneriert die Moral der Mitarbeiter."},
]

FURNITURE_DATA = [
    {"id": "desk_wood", "name": "Holztisch", "cost": 200, "type": "workplace", "year": 1930},
    {"id": "desk_modern", "name": "Moderner Schreibtisch", "cost": 1000, "type": "workplace", "year": 1980},
    {"id": "pc_80s", "name": "Heimcomputer (80er)", "cost": 1500, "type": "equipment", "year": 1980, "bonus": "dev_speed"},
    {"id": "pc_90s", "name": "Workstation (90er)", "cost": 3000, "type": "equipment", "year": 1990, "bonus": "dev_speed"},
    {"id": "server_rack", "name": "Server-Rack", "cost": 10000, "type": "equipment", "year": 1995, "bonus": "mmo_capacity"},
]

SUBSCRIPTION_UNLOCK_YEAR = 1995


# ============================================================
# NEU: v3.11.0-beta.1 Expansion Constants
# ============================================================

HARDWARE_TECH_LIST = [
    {"id": "synthesizer_8bit", "name_key": "hw_tech_8bit", "cost": 15000, "year": 1980, "sound_bonus": 0.05},
    {"id": "fm_synthesis", "name_key": "hw_tech_fm", "cost": 25000, "year": 1980, "sound_bonus": 0.10},
    {"id": "midi_support", "name_key": "hw_tech_midi", "cost": 35000, "year": 1984, "sound_bonus": 0.15},
    {"id": "wavetable", "name_key": "hw_tech_wavetable", "cost": 50000, "year": 1988, "sound_bonus": 0.20},
    {"id": "binaural_3d", "name_key": "hw_tech_3d", "cost": 120000, "year": 2000, "sound_bonus": 0.35},
]

FAN_MAIL_TEMPLATES = [
    {
        "id": "fan_mail_retro",
        "subject_key": "fan_mail_retro_sub",
        "text_key": "fan_mail_retro_text",
        "options": [
            {"text_key": "fan_mail_retro_opt1", "effects": {"fans": 300, "hype": 5.0, "money": 0}},
            {"text_key": "fan_mail_retro_opt2", "effects": {"fans": -100, "hype": -2.0, "money": 500}},
            {"text_key": "fan_mail_retro_opt3", "effects": {"fans": 100, "hype": 1.0, "money": 0}},
        ]
    },
    {
        "id": "fan_mail_soundcard",
        "subject_key": "fan_mail_sc_sub",
        "text_key": "fan_mail_sc_text",
        "options": [
            {"text_key": "fan_mail_sc_opt1", "effects": {"fans": 500, "hype": 10.0, "money": -1000}},
            {"text_key": "fan_mail_sc_opt2", "effects": {"fans": 200, "hype": 3.0, "money": 0}},
            {"text_key": "fan_mail_sc_opt3", "effects": {"fans": -200, "hype": -5.0, "money": 0}},
        ]
    },
    {
        "id": "fan_mail_bug",
        "subject_key": "fan_mail_bug_sub",
        "text_key": "fan_mail_bug_text",
        "options": [
            {"text_key": "fan_mail_bug_opt1", "effects": {"fans": 400, "hype": 4.0, "money": 0}},
            {"text_key": "fan_mail_bug_opt2", "effects": {"fans": -300, "hype": -8.0, "money": 0}},
        ]
    }
]

OFFICE_PERSONALITY_EVENTS = [
    {
        "id": "event_perfectionist_delay",
        "personality_required": "perfectionist",
        "title_key": "event_perf_title",
        "text_key": "event_perf_text",
        "options": [
            {"text_key": "event_perf_opt1", "effects": {"morale": 15, "dev_speed_penalty": 0.5, "money": 0}},
            {"text_key": "event_perf_opt2", "effects": {"morale": -20, "quality_boost": 0.05, "money": 0}},
        ]
    },
    {
        "id": "event_chaotic_idea",
        "personality_required": "chaotic",
        "title_key": "event_ch_title",
        "text_key": "event_ch_text",
        "options": [
            {"text_key": "event_ch_opt1", "effects": {"money": -2000, "hype": 15.0, "morale": 10}},
            {"text_key": "event_ch_opt2", "effects": {"morale": -15, "hype": 0, "money": 0}},
        ]
    },
    {
        "id": "event_showman_con",
        "personality_required": "showman",
        "title_key": "event_sh_title",
        "text_key": "event_sh_text",
        "options": [
            {"text_key": "event_sh_opt1", "effects": {"money": -5000, "fans": 1000, "hype": 20.0}},
            {"text_key": "event_sh_opt2", "effects": {"morale": -15, "fans": 0, "hype": 0}},
        ]
    }
]


# ============================================================
# CONTENT CREATORS
# ============================================================
CONTENT_CREATORS = [
    {"id": "small_streamer", "name_key": "creator_small", "cost": 10000, "boost": 1.2, "duration": 4},
    {"id": "medium_streamer", "name_key": "creator_medium", "cost": 50000, "boost": 1.5, "duration": 4},
    {"id": "large_streamer", "name_key": "creator_large", "cost": 250000, "boost": 2.5, "duration": 4},
]
