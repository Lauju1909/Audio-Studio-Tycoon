"""Themen, Genres, Plattformen, Zielgruppen, Technologien, Engine-Features."""
from data.core import *  # noqa: F401,F403

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
    {"name": "Oculus Rift (VR)", "license_fee": 300000, "market_multi": 8.0, "unlock_year": 2016, "end_year": 2026, "type": "VR"},
    {"name": "HTC Vive (VR)", "license_fee": 350000, "market_multi": 8.5, "unlock_year": 2016, "end_year": 2026, "type": "VR"},
    {"name": "PSVR (VR)", "license_fee": 300000, "market_multi": 8.0, "unlock_year": 2016, "end_year": 2026, "type": "VR"},
    {"name": "Meta Quest 2 (VR)", "license_fee": 500000, "market_multi": 12.0, "unlock_year": 2020, "end_year": 2030, "type": "VR"},
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
    {"name": "KI-Soundtrack Generation",      "cost": 150000, "unlock_year": 2023, "research_weeks": 8, "description": "Ermöglicht die Generierung kompletter Soundtracks durch KI."},
    {"name": "Neural-Engine Grafik-Rendering", "cost": 250000, "unlock_year": 2027, "research_weeks": 8, "description": "Schaltet voll-neuronale Echtzeit-Grafik für Spiele-Engines frei."},
    {"name": "Quanten-Physik-Engine",          "cost": 450000, "unlock_year": 2030, "research_weeks": 10, "description": "Vollständige physikalische Mikrosimulation in Echtzeit."},
    {"name": "Holodeck-Immersions-Engine",    "cost": 650000, "unlock_year": 2035, "research_weeks": 12, "description": "Schaltet holografische 3D-Spielumgebungen frei."},
    {"name": "Gedanken-Steuerungs-Engine",    "cost": 850000, "unlock_year": 2040, "research_weeks": 14, "description": "Erlaubt direkte Spielsteuerung per Gehirnschnittstelle (BCI)."},
    {"name": "Next-Gen Testlabor & QA",        "cost": 120000, "unlock_year": 1995, "research_weeks": 6, "description": "Schaltet ein modernes QA-Testzentrum im Studio frei."},
    {"name": "Performance-Labor",             "cost": 180000, "unlock_year": 2005, "research_weeks": 6, "description": "Optimiert Spiele-Engine für schwächere Hardware."},
    {"name": "Studio-Esports-Arena",          "cost": 400000, "unlock_year": 2015, "research_weeks": 8, "description": "Eigene E-Sports-Arena im Studio-Hauptgebäude."},
    {"name": "KI-Entwickler-Zentrale",        "cost": 500000, "unlock_year": 2026, "research_weeks": 10, "description": "Integriertes KI-Studio für prozedurale Spielwelt-Generierung."},
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
