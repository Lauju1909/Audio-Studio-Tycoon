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
    {"name": "Abakus", "cost": 5000, "week": 1, "research_weeks": 2},
    {"name": "Logistik", "cost": 5000, "week": 1, "research_weeks": 2},
    {"name": "Schach", "cost": 5000, "week": 1, "research_weeks": 2},
    {"name": "Mathematik", "cost": 5000, "week": 1, "research_weeks": 2},
    {"name": "Astronomie", "cost": 5500, "week": 48, "research_weeks": 2},
    {"name": "Landwirtschaft", "cost": 5500, "week": 48, "research_weeks": 2},
    {"name": "Kochen", "cost": 6000, "week": 96, "research_weeks": 2},
    {"name": "Politik", "cost": 6000, "week": 96, "research_weeks": 2},
    {"name": "Detektiv", "cost": 6500, "week": 144, "research_weeks": 2},
    {"name": "Kartenspiele", "cost": 6500, "week": 144, "research_weeks": 2},
    {"name": "Architektur", "cost": 7000, "week": 192, "research_weeks": 2},
    {"name": "Postwesen", "cost": 7000, "week": 192, "research_weeks": 2},
    {"name": "Zirkus", "cost": 7500, "week": 240, "research_weeks": 2},
    {"name": "Bergbau", "cost": 7500, "week": 240, "research_weeks": 2},
    {"name": "Eisenbahn", "cost": 8000, "week": 288, "research_weeks": 2},
    {"name": "Seefahrt", "cost": 8000, "week": 288, "research_weeks": 2},
    {"name": "Feuerwehr", "cost": 8500, "week": 336, "research_weeks": 2},
    {"name": "Kryptografie", "cost": 8500, "week": 336, "research_weeks": 2},
    {"name": "Mars-Invasion", "cost": 9000, "week": 384, "research_weeks": 2},
    {"name": "Zauberei", "cost": 9000, "week": 384, "research_weeks": 2},
    {"name": "Militär", "cost": 9500, "week": 432, "research_weeks": 2},
    {"name": "Chemie", "cost": 9500, "week": 432, "research_weeks": 2},
    {"name": "U-Boot", "cost": 10000, "week": 480, "research_weeks": 2},
    {"name": "Luftschlacht", "cost": 10500, "week": 528, "research_weeks": 2},
    {"name": "Spionage", "cost": 11000, "week": 576, "research_weeks": 2},
    {"name": "Panzer", "cost": 11500, "week": 624, "research_weeks": 2},
    {"name": "Fallschirmjäger", "cost": 12000, "week": 672, "research_weeks": 2},
    {"name": "Wiederaufbau", "cost": 12500, "week": 720, "research_weeks": 2},
    {"name": "Journalismus", "cost": 13000, "week": 768, "research_weeks": 2},
    {"name": "UFOs", "cost": 13500, "week": 816, "research_weeks": 2},
    {"name": "Roboter", "cost": 14000, "week": 864, "research_weeks": 2},
    {"name": "Dschungel", "cost": 14500, "week": 912, "research_weeks": 2},
    {"name": "Archäologie", "cost": 15000, "week": 960, "research_weeks": 2},
    {"name": "Weltraum", "cost": 15500, "week": 1008, "research_weeks": 2},
    {"name": "Wilder Westen", "cost": 16000, "week": 1056, "research_weeks": 2},
    {"name": "Bergsteigen", "cost": 16500, "week": 1104, "research_weeks": 2},
    {"name": "Fussball", "cost": 17000, "week": 1152, "research_weeks": 2},
    {"name": "Vergnügungspark", "cost": 17500, "week": 1200, "research_weeks": 2},
    {"name": "Monster", "cost": 18000, "week": 1248, "research_weeks": 2},
    {"name": "Satelliten", "cost": 18500, "week": 1296, "research_weeks": 2},
    {"name": "Tennis", "cost": 19000, "week": 1344, "research_weeks": 2},
    {"name": "Rennwagen", "cost": 19500, "week": 1392, "research_weeks": 2},
    {"name": "Tiefsee", "cost": 20000, "week": 1440, "research_weeks": 2},
    {"name": "Mafia", "cost": 20500, "week": 1488, "research_weeks": 2},
    {"name": "Fantasy", "cost": 21000, "week": 1536, "research_weeks": 2},
    {"name": "Agenten", "cost": 21500, "week": 1584, "research_weeks": 2},
    {"name": "Popstars", "cost": 22000, "week": 1632, "research_weeks": 2},
    {"name": "Dinosaurier", "cost": 22500, "week": 1680, "research_weeks": 2},
    {"name": "Ninjas", "cost": 23000, "week": 1728, "research_weeks": 2},
    {"name": "Hippies", "cost": 23500, "week": 1776, "research_weeks": 2},
    {"name": "Weltrevolution", "cost": 24000, "week": 1824, "research_weeks": 2},
    {"name": "Mondbasis", "cost": 24500, "week": 1872, "research_weeks": 2},
    {"name": "Kung-Fu", "cost": 25000, "week": 1920, "research_weeks": 2},
    {"name": "Piraten", "cost": 25500, "week": 1968, "research_weeks": 2},
    {"name": "Basketball", "cost": 26000, "week": 2016, "research_weeks": 2},
    {"name": "Motorrad", "cost": 26500, "week": 2064, "research_weeks": 2},
    {"name": "Verliese", "cost": 27000, "week": 2112, "research_weeks": 2},
    {"name": "Polizei", "cost": 27500, "week": 2160, "research_weeks": 2},
    {"name": "Alien-Jagd", "cost": 28000, "week": 2208, "research_weeks": 2},
    {"name": "Laserschwert", "cost": 28500, "week": 2256, "research_weeks": 2},
    {"name": "Invaders", "cost": 29000, "week": 2304, "research_weeks": 2},
    {"name": "Horrorhaus", "cost": 29500, "week": 2352, "research_weeks": 2},
    {"name": "Gelbe Fresspunkte", "cost": 30000, "week": 2400, "research_weeks": 2},
    {"name": "Büro-Alltag", "cost": 30500, "week": 2448, "research_weeks": 2},
    {"name": "Cyberpunk", "cost": 31000, "week": 2496, "research_weeks": 2},
    {"name": "Vampire", "cost": 31500, "week": 2544, "research_weeks": 2},
    {"name": "Breakdance", "cost": 32000, "week": 2592, "research_weeks": 2},
    {"name": "Klempner", "cost": 32500, "week": 2640, "research_weeks": 2},
    {"name": "Postapokalypse", "cost": 33000, "week": 2688, "research_weeks": 2},
    {"name": "Mechs", "cost": 33500, "week": 2736, "research_weeks": 2},
    {"name": "Skateboarding", "cost": 34000, "week": 2784, "research_weeks": 2},
    {"name": "Taschenmonster", "cost": 34500, "week": 2832, "research_weeks": 2},
    {"name": "Krankenhaus", "cost": 35000, "week": 2880, "research_weeks": 2},
    {"name": "Freizeitpark", "cost": 35500, "week": 2928, "research_weeks": 2},
    {"name": "Mars-Shooter", "cost": 36000, "week": 2976, "research_weeks": 2},
    {"name": "Urzeit/Survival", "cost": 36500, "week": 3024, "research_weeks": 2},
    {"name": "Anime", "cost": 37000, "week": 3072, "research_weeks": 2},
    {"name": "Hacking", "cost": 37500, "week": 3120, "research_weeks": 2},
    {"name": "Stealth-Agent", "cost": 38000, "week": 3168, "research_weeks": 2},
    {"name": "Elfen & Orks", "cost": 38500, "week": 3216, "research_weeks": 2},
    {"name": "Survival-Insel", "cost": 39000, "week": 3264, "research_weeks": 2},
    {"name": "Skandal-TV", "cost": 39500, "week": 3312, "research_weeks": 2},
    {"name": "Lebens-Sim", "cost": 40000, "week": 3360, "research_weeks": 2},
    {"name": "Zombie-Hype", "cost": 40500, "week": 3408, "research_weeks": 2},
    {"name": "Parkplatz-Manager", "cost": 41000, "week": 3456, "research_weeks": 2},
    {"name": "E-Sport", "cost": 41500, "week": 3504, "research_weeks": 2},
    {"name": "Zauberschule", "cost": 42000, "week": 3552, "research_weeks": 2},
    {"name": "Sandbox/Voxel", "cost": 42500, "week": 3600, "research_weeks": 2},
    {"name": "Wikinger", "cost": 43000, "week": 3648, "research_weeks": 2},
    {"name": "Smartphones", "cost": 43500, "week": 3696, "research_weeks": 2},
    {"name": "Freerunning", "cost": 44000, "week": 3744, "research_weeks": 2},
    {"name": "Block-Bauen", "cost": 44500, "week": 3792, "research_weeks": 2},
    {"name": "Social Networking", "cost": 45000, "week": 3840, "research_weeks": 2},
    {"name": "Indie-Entwickler", "cost": 45500, "week": 3888, "research_weeks": 2},
    {"name": "Battle-Royale", "cost": 46000, "week": 3936, "research_weeks": 2},
    {"name": "VR-Simulation", "cost": 46500, "week": 3984, "research_weeks": 2},
    {"name": "Farming-Hype", "cost": 47000, "week": 4032, "research_weeks": 2},
    {"name": "Cyber-Krieg", "cost": 47500, "week": 4080, "research_weeks": 2},
    {"name": "AR-Jagd", "cost": 48000, "week": 4128, "research_weeks": 2},
    {"name": "Krypto-Mining", "cost": 48500, "week": 4176, "research_weeks": 2},
    {"name": "Mars-Kolonisierung", "cost": 49000, "week": 4224, "research_weeks": 2},
    {"name": "Streaming-Star", "cost": 49500, "week": 4272, "research_weeks": 2},
    {"name": "KI-Dystopie", "cost": 50000, "week": 4320, "research_weeks": 2},
    {"name": "NFT-Sammeln", "cost": 50500, "week": 4368, "research_weeks": 2},
    {"name": "Metaverse", "cost": 51000, "week": 4416, "research_weeks": 2},
    {"name": "KI-Utopie", "cost": 51500, "week": 4464, "research_weeks": 2},
    {"name": "Endzeit-Bote", "cost": 52000, "week": 4512, "research_weeks": 2},
    {"name": "Gen-Labor", "cost": 52500, "week": 4560, "research_weeks": 2},
    {"name": "Neural-Link", "cost": 53000, "week": 4608, "research_weeks": 2},
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
    {"name": "RPG", "cost": 15000, "week": 5, "research_weeks": 4},
    {"name": "Simulation", "cost": 10000, "week": 2, "research_weeks": 3},
    {"name": "Strategie", "cost": 12000, "week": 3, "research_weeks": 3},
    {"name": "Abenteuer", "cost": 15000, "week": 5, "research_weeks": 4},
    {"name": "Sport", "cost": 8000, "week": 2, "research_weeks": 2},
    {"name": "Horror", "cost": 20000, "week": 10, "research_weeks": 5},
    {"name": "Kampfspiel", "cost": 18000, "week": 8, "research_weeks": 4},
    {"name": "Rennspiel", "cost": 10000, "week": 4, "research_weeks": 3},
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
    {"name": "Hand-Abakus", "license_fee": 10000, "market_multi": 1.0, "available_week": 1, "end_week": 481, "type": "Konsole"},
    {"name": "Zuse Z1", "license_fee": 10000, "market_multi": 1.0, "available_week": 240, "end_week": 720, "type": "Konsole"},
    {"name": "Zuse Z3", "license_fee": 16000, "market_multi": 1.6, "available_week": 528, "end_week": 1008, "type": "Konsole"},
    {"name": "ENIAC", "license_fee": 0, "market_multi": 2.4, "available_week": 768, "end_week": 1248, "type": "Heimcomputer"},
    {"name": "UNIVAC I", "license_fee": 0, "market_multi": 3.1, "available_week": 1008, "end_week": 1488, "type": "Heimcomputer"},
    {"name": "Nimrod", "license_fee": 31000, "market_multi": 3.1, "available_week": 1008, "end_week": 1488, "type": "Konsole"},
    {"name": "EDSAC (OXO)", "license_fee": 0, "market_multi": 3.3, "available_week": 1056, "end_week": 1536, "type": "Heimcomputer"},
    {"name": "PDP-1 (Spacewar)", "license_fee": 45000, "market_multi": 4.5, "available_week": 1440, "end_week": 1920, "type": "Konsole"},
    {"name": "IBM 360", "license_fee": 0, "market_multi": 5.2, "available_week": 1680, "end_week": 2160, "type": "Heimcomputer"},
    {"name": "Magnavox Odyssey", "license_fee": 63000, "market_multi": 6.3, "available_week": 2016, "end_week": 2496, "type": "Konsole"},
    {"name": "Fairchild Ch. F", "license_fee": 69000, "market_multi": 6.9, "available_week": 2208, "end_week": 2688, "type": "Konsole"},
    {"name": "Atari 2600", "license_fee": 70000, "market_multi": 7.0, "available_week": 2256, "end_week": 2736, "type": "Konsole"},
    {"name": "Bally Astrocade", "license_fee": 72000, "market_multi": 7.2, "available_week": 2304, "end_week": 2784, "type": "Konsole"},
    {"name": "C64", "license_fee": 0, "market_multi": 7.5, "available_week": 2400, "end_week": 2880, "type": "Heimcomputer"},
    {"name": "Vectrex", "license_fee": 78000, "market_multi": 7.8, "available_week": 2496, "end_week": 2976, "type": "Konsole"},
    {"name": "Famicom (NES)", "license_fee": 79000, "market_multi": 7.9, "available_week": 2544, "end_week": 3024, "type": "Konsole"},
    {"name": "Famicom Disk Sys", "license_fee": 84000, "market_multi": 8.4, "available_week": 2688, "end_week": 3168, "type": "Konsole"},
    {"name": "Sega Genesis", "license_fee": 87000, "market_multi": 8.7, "available_week": 2784, "end_week": 3264, "type": "Konsole"},
    {"name": "Neo Geo AES", "license_fee": 90000, "market_multi": 9.0, "available_week": 2880, "end_week": 3360, "type": "Konsole"},
    {"name": "SNES", "license_fee": 90000, "market_multi": 9.0, "available_week": 2880, "end_week": 3360, "type": "Konsole"},
    {"name": "Philips CD-i", "license_fee": 92000, "market_multi": 9.2, "available_week": 2928, "end_week": 3408, "type": "Konsole"},
    {"name": "Atari Jaguar", "license_fee": 94000, "market_multi": 9.4, "available_week": 3024, "end_week": 3504, "type": "Konsole"},
    {"name": "PlayStation 1", "license_fee": 96000, "market_multi": 9.6, "available_week": 3072, "end_week": 3552, "type": "Konsole"},
    {"name": "Nintendo 64", "license_fee": 99000, "market_multi": 9.9, "available_week": 3168, "end_week": 3648, "type": "Konsole"},
    {"name": "Dreamcast", "license_fee": 100000, "market_multi": 10.0, "available_week": 3264, "end_week": 3744, "type": "Konsole"},
    {"name": "PlayStation 2", "license_fee": 100000, "market_multi": 10.0, "available_week": 3360, "end_week": 3840, "type": "Konsole"},
    {"name": "GameCube", "license_fee": 100000, "market_multi": 10.0, "available_week": 3408, "end_week": 3888, "type": "Konsole"},
    {"name": "Xbox 360", "license_fee": 100000, "market_multi": 10.0, "available_week": 3600, "end_week": 4080, "type": "Konsole"},
    {"name": "PlayStation 3", "license_fee": 100000, "market_multi": 10.0, "available_week": 3648, "end_week": 4128, "type": "Konsole"},
    {"name": "Gizmondo", "license_fee": 100000, "market_multi": 10.0, "available_week": 3744, "end_week": 4224, "type": "Handheld"},
    {"name": "PlayStation 4", "license_fee": 100000, "market_multi": 10.0, "available_week": 3984, "end_week": 4464, "type": "Konsole"},
    {"name": "Switch", "license_fee": 100000, "market_multi": 10.0, "available_week": 4176, "end_week": 4656, "type": "Handheld"},
    {"name": "Playdate", "license_fee": 100000, "market_multi": 10.0, "available_week": 4224, "end_week": 4704, "type": "Handheld"},
    {"name": "PlayStation 5", "license_fee": 100000, "market_multi": 10.0, "available_week": 4320, "end_week": 4800, "type": "Konsole"},
    {"name": "Analogue Pocket", "license_fee": 100000, "market_multi": 10.0, "available_week": 4368, "end_week": 4848, "type": "Handheld"},
    {"name": "Evercade EXP", "license_fee": 100000, "market_multi": 10.0, "available_week": 4416, "end_week": 4896, "type": "Handheld"},
    {"name": "Cloud-Console", "license_fee": 100000, "market_multi": 10.0, "available_week": 4560, "end_week": 5040, "type": "Streaming"},
    {"name": "Neural-Box 1", "license_fee": 100000, "market_multi": 10.0, "available_week": 4608, "end_week": 5088, "type": "Konsole"},
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
    {"name": "Jugendliche", "cost": 25000, "week": 15, "research_weeks": 5},
]

# ============================================================
# ENDGAME-TECHNOLOGIEN (Forschung)
# ============================================================
RESEARCHABLE_TECHNOLOGIES = [
    {"name": "Digitaler Vertrieb & Logistik", "cost": 150000, "week": 30, "research_weeks": 6, "description": "Erlaubt den Vertrieb ohne Publisher (Eigenvertrieb) und AAA-Spiele."},
    {"name": "Live-Service Architektur",      "cost": 300000, "week": 40, "research_weeks": 8, "description": "Ermöglicht die Entwicklung und den Betrieb von MMOs und Live-Service Spielen."},
    {"name": "Investment & M&A",              "cost": 500000, "week": 50, "research_weeks": 10, "description": "Ermöglicht den Aufkauf von Konkurrenz-Studios am Aktienmarkt."},
    {"name": "Hardware Labor",                "cost": 1000000,"week": 60, "research_weeks": 15, "description": "Schaltet die Entwicklung eigener Konsolen frei."},
    {"name": "Büroausstattung 1",             "cost": 25000,  "week": 10, "research_weeks": 4, "description": "Schaltet Arcade-Automaten und Erholungsobjekte frei."},
    {"name": "Arbeitsrecht-Experten",         "cost": 80000, "week": 20, "research_weeks": 6, "description": "Schaltet die Rechtsabteilung frei, um Headhunting zu erschweren."},
    {"name": "Geheimdienst-Netzwerk",         "cost": 120000, "week": 35, "research_weeks": 8, "description": "Schaltet die Marktforschungs-Station frei (KI-Spionage)."},
    {"name": "Krisenmanagement",              "cost": 50000, "week": 25, "research_weeks": 5, "description": "Schaltet die PR-Zentrale frei, um Hype-Verlust durch Sabotage zu reduzieren."},
    {"name": "Büroausstattung 2",             "cost": 30000,  "week": 18, "research_weeks": 4, "description": "Schaltet weitere Pflanzen und Dekorationen frei."},
    {"name": "Büroausstattung 3",             "cost": 65000,  "week": 36, "research_weeks": 5, "description": "Schaltet exotische Zimmerpflanzen und Luxus-Deko frei."},
    {"name": "Gesundes Arbeiten",             "cost": 40000,  "week": 15, "research_weeks": 5, "description": "Schaltet ergonomische Tische frei."},
    {"name": "Ergonomie am Arbeitsplatz 2",   "cost": 60000,  "week": 30, "research_weeks": 5, "description": "Schaltet Stehschreibtische frei."},
    {"name": "Ergonomie am Arbeitsplatz 3",   "cost": 120000, "week": 60, "research_weeks": 6, "description": "Schaltet High-End Laufband-Tische frei."},
    {"name": "Kantinen-Ausbau 1",             "cost": 15000,  "week": 12, "research_weeks": 3, "description": "Schaltet fortgeschrittene Getränkestationen frei."},
    {"name": "Kantinen-Ausbau 2",             "cost": 35000,  "week": 26, "research_weeks": 4, "description": "Schaltet Snack-Automaten und Pizzaöfen frei."},
    {"name": "Kantinen-Ausbau 3",             "cost": 75000,  "week": 48, "research_weeks": 5, "description": "Schaltet Gourmet-Küche und Wein-Regal frei."},
    {"name": "Freizeit & Spiel 1",            "cost": 25000,  "week": 16, "research_weeks": 3, "description": "Schaltet Tischkicker und Dartscheiben frei."},
    {"name": "Freizeit & Spiel 2",            "cost": 45000,  "week": 32, "research_weeks": 4, "description": "Schaltet Billardtische und Flipper frei."},
    {"name": "Freizeit & Spiel 3",            "cost": 95000,  "week": 64, "research_weeks": 6, "description": "Schaltet VR-Stationen und Heimkino frei."},
    {"name": "Studios & Kabinen",             "cost": 80000,  "week": 25, "research_weeks": 6, "description": "Schaltet hochmoderne Soundkabinen frei."},
    {"name": "Audio-Meisterschaft 2",         "cost": 110000, "week": 44, "research_weeks": 5, "description": "Schaltet Drum-Set und Flügel für Sound-Boosts frei."},
    {"name": "Audio-Meisterschaft 3",         "cost": 250000, "week": 80, "research_weeks": 7, "description": "Schaltet Regie-Platz und High-End Lautsprecher frei."},
    {"name": "High-End Workstations 1",       "cost": 85000,  "week": 40, "research_weeks": 5, "description": "Schaltet Dual-Monitor Setups und Grafik-Tablets frei."},
    {"name": "High-End Workstations 2",       "cost": 150000, "week": 72, "research_weeks": 6, "description": "Schaltet Triple-Monitore und Render-Farmen frei."},
    {"name": "Motion Capture Studio",         "cost": 400000, "week": 96, "research_weeks": 8, "description": "Schaltet MoCap-Kameras frei."},
    {"name": "Gamer-Setup",                   "cost": 70000,  "week": 38, "research_weeks": 4, "description": "Schaltet RGB-Desks und Gamer-Schreibtische frei."},
    {"name": "Dekorations-Wahn 1",            "cost": 20000,  "week": 14, "research_weeks": 3, "description": "Schaltet kleine Bücheregale und Poster frei."},
    {"name": "Dekorations-Wahn 2",            "cost": 50000,  "week": 28, "research_weeks": 4, "description": "Schaltet Pokal-Vitrinen und Lava-Lampen frei."},
    {"name": "Dekorations-Wahn 3",            "cost": 90000,  "week": 50, "research_weeks": 5, "description": "Schaltet Neon-Schilder, Teppiche und Globen frei."},
]

# ============================================================
# SCHWIERIGKEITSGRADE
# ============================================================
DIFFICULTY_LEVELS = [
    {
        "name": "Einfach",
        "start_money": 150000,
        "rival_strength": 0.7,
        "review_bonus": 0.5,
        "market_multi": 1.3,
        "description": "Mehr Startgeld, schwächere Rivalen, großzügigere Reviews.",
    },
    {
        "name": "Normal",
        "start_money": 100000,
        "rival_strength": 1.0,
        "review_bonus": 0.0,
        "market_multi": 1.0,
        "description": "Die Standard-Erfahrung.",
    },
    {
        "name": "Schwer",
        "start_money": 50000,
        "rival_strength": 1.3,
        "review_bonus": -0.5,
        "market_multi": 0.8,
        "description": "Weniger Startgeld, stärkere Rivalen, strengere Reviews.",
    },
    {
        "name": "Legendär",
        "start_money": 20000,
        "rival_strength": 1.6,
        "review_bonus": -1.0,
        "market_multi": 0.6,
        "description": "Extrem wenig Geld, übermächtige Rivalen, gnadenlose Reviews.",
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
    {"category": "Engine", "name": "Papier-Logik", "cost": 1000, "tech_bonus": 10, "week": 1},
    {"category": "Technik", "name": "Relais-Steuerung", "cost": 5000, "tech_bonus": 5, "week": 96},
    {"category": "Technik", "name": "Lochkarten-Input", "cost": 13000, "tech_bonus": 10, "week": 288},
    {"category": "Technik", "name": "Vakuum-Röhren", "cost": 23000, "tech_bonus": 15, "week": 528},
    {"category": "Grafik", "name": "Oszilloskop-Grafik", "cost": 33000, "tech_bonus": 5, "week": 768},
    {"category": "Technik", "name": "Transistor V1", "cost": 37000, "tech_bonus": 20, "week": 864},
    {"category": "Technik", "name": "Magnetkernspeicher", "cost": 45000, "tech_bonus": 10, "week": 1056},
    {"category": "Sound", "name": "Mono-Beep V1", "cost": 53000, "tech_bonus": 5, "week": 1248},
    {"category": "Grafik", "name": "Vektor-Linien", "cost": 57000, "tech_bonus": 15, "week": 1344},
    {"category": "Grafik", "name": "CRT-Standard", "cost": 65000, "tech_bonus": 10, "week": 1536},
    {"category": "Grafik", "name": "ASCII-Grafik", "cost": 75000, "tech_bonus": 5, "week": 1776},
    {"category": "Technik", "name": "Mikroprozessor", "cost": 83000, "tech_bonus": 30, "week": 1968},
    {"category": "Grafik", "name": "Tilemaps V1", "cost": 89000, "tech_bonus": 20, "week": 2112},
    {"category": "Grafik", "name": "Parallax-Scrolling", "cost": 93000, "tech_bonus": 15, "week": 2208},
    {"category": "Grafik", "name": "Sprite-Rotation", "cost": 97000, "tech_bonus": 10, "week": 2304},
    {"category": "Sound", "name": "FM-Synthese", "cost": 101000, "tech_bonus": 20, "week": 2400},
    {"category": "Grafik", "name": "Vierfarb-Sprites", "cost": 105000, "tech_bonus": 10, "week": 2496},
    {"category": "Physik", "name": "Physik V1", "cost": 109000, "tech_bonus": 10, "week": 2592},
    {"category": "Gameplay", "name": "Savegame-Batterie", "cost": 111000, "tech_bonus": 30, "week": 2640},
    {"category": "Sound", "name": "Wavetable-Sound", "cost": 115000, "tech_bonus": 25, "week": 2736},
    {"category": "Grafik", "name": "Mode 7 Pseudo-3D", "cost": 119000, "tech_bonus": 30, "week": 2832},
    {"category": "Grafik", "name": "Raycasting", "cost": 123000, "tech_bonus": 40, "week": 2928},
    {"category": "Technik", "name": "Z-Buffer", "cost": 127000, "tech_bonus": 20, "week": 3024},
    {"category": "Grafik", "name": "Texture Mapping", "cost": 129000, "tech_bonus": 30, "week": 3072},
    {"category": "Sound", "name": "CD-Audio", "cost": 131000, "tech_bonus": 50, "week": 3120},
    {"category": "Grafik", "name": "Echtzeit-Licht", "cost": 133000, "tech_bonus": 20, "week": 3168},
    {"category": "KI", "name": "KI V1 (A*)", "cost": 135000, "tech_bonus": 20, "week": 3216},
    {"category": "Gameplay", "name": "Multiplayer V2", "cost": 137000, "tech_bonus": 40, "week": 3264},
    {"category": "Grafik", "name": "Vertex-Shader", "cost": 141000, "tech_bonus": 50, "week": 3360},
    {"category": "Physik", "name": "Ragdoll-Physik", "cost": 145000, "tech_bonus": 40, "week": 3456},
    {"category": "Grafik", "name": "Pixel-Shader", "cost": 149000, "tech_bonus": 60, "week": 3552},
    {"category": "Technik", "name": "Blu-Ray Support", "cost": 153000, "tech_bonus": 100, "week": 3648},
    {"category": "Physik", "name": "Physische Engine V3", "cost": 157000, "tech_bonus": 60, "week": 3744},
    {"category": "Gameplay", "name": "Cloud-Saves", "cost": 161000, "tech_bonus": 20, "week": 3840},
    {"category": "Grafik", "name": "Motion Capture", "cost": 165000, "tech_bonus": 80, "week": 3936},
    {"category": "KI", "name": "Prozedurale Welt", "cost": 169000, "tech_bonus": 100, "week": 4032},
    {"category": "Grafik", "name": "HDR-Support", "cost": 173000, "tech_bonus": 40, "week": 4128},
    {"category": "Grafik", "name": "Echtzeit-Raytracing", "cost": 177000, "tech_bonus": 200, "week": 4224},
    {"category": "KI", "name": "KI-Storytelling", "cost": 181000, "tech_bonus": 150, "week": 4320},
    {"category": "Gameplay", "name": "Full-Body VR", "cost": 185000, "tech_bonus": 120, "week": 4416},
    {"category": "Grafik", "name": "Generative Assets", "cost": 187000, "tech_bonus": 200, "week": 4464},
    {"category": "Technik", "name": "Quanten-Ladezeit", "cost": 191000, "tech_bonus": 100, "week": 4560},
    {"category": "Technik", "name": "Neural-Sync", "cost": 193000, "tech_bonus": 10, "week": 4608},
]



# ============================================================
# MITARBEITER-NAMEN (zufällig)
# ============================================================
EMPLOYEE_FIRST_NAMES = [
    "Max", "Anna", "Felix", "Sarah", "Tim", "Julia", "Leon", "Laura",
    "Lukas", "Marie", "Jonas", "Lena", "Niklas", "Emma", "David",
    "Sophie", "Jan", "Mia", "Tom", "Lisa", "Kai", "Nina", "Ben",
    "Hanna", "Erik", "Lea", "Paul", "Clara", "Finn", "Ella",
]

EMPLOYEE_LAST_NAMES = [
    "Müller", "Schmidt", "Weber", "Fischer", "Wagner", "Bauer",
    "Koch", "Richter", "Klein", "Wolf", "Schwarz", "Braun",
    "Zimmermann", "Hartmann", "Krüger", "Hofmann", "Lange",
    "Jung", "Peters", "König", "Lang", "Berg", "Stein",
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
    "coffee":        {"name": "Kaffeemaschine",          "cost": 500,    "layer": "furniture", "employees": 0, "bonus": None,         "desc": "Gibt kleinen Moral-Boost. +1 Moral pro Woche."},
    "plant":         {"name": "Pflanze",                 "cost": 300,    "layer": "furniture", "employees": 0, "bonus": None,         "desc": "Dekorativ. +1 Moral pro Woche."},
    "sofa":          {"name": "Sofa",                    "cost": 1200,   "layer": "furniture", "employees": 0, "bonus": None,         "desc": "Erholungszone. +2 Moral pro Woche."},
    "research_desk": {"name": "Forschungs-Schreibtisch", "cost": 5000,   "layer": "furniture", "employees": 0, "bonus": "research",   "desc": "Schaltet Forschung frei."},
    "server_rack":   {"name": "Server-Rack",             "cost": 15000,  "layer": "furniture", "employees": 0, "bonus": "mmo",        "desc": "Serverkapazität für MMOs."},
    "mixing_desk":   {"name": "Mischpult",               "cost": 20000,  "layer": "furniture", "employees": 1, "bonus": "sound",      "desc": "+10% auf Sound-Bewertung."},
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
        "name": "Global-Play",
        "description": "Ein solider Publisher mit gutem Vertrieb.",
        "advance": 5000,
        "royalty": 0.40,
        "min_score": 6
    },
    {
        "name": "Titan-Publishing",
        "description": "Premium-Partner für AAA-Titel.",
        "advance": 25000,
        "royalty": 0.60,
        "min_score": 8
    },
    {
        "name": "Star-Distribute",
        "description": "Perfekt für Einsteiger, geringe Hürden.",
        "advance": 1000,
        "royalty": 0.20,
        "min_score": 4
    }
]

# MARKETING-OPTIONEN PH_5
MARKETING_OPTIONS_PH5 = [
    {"name": "Social Media Hype", "cost": 500, "hype": 10, "description": "Günstiger Hype auf X und TikTok."},
    {"name": "Gaming Web-Ads", "cost": 2500, "hype": 25, "description": "Banner auf großen Audio-Seiten."},
    {"name": "TV & Cinema Spots", "cost": 15000, "hype": 70, "description": "Massive Präsenz, sehr teuer."},
    {"name": "Global PR Tour", "cost": 50000, "hype": 150, "description": "Die ultimative Werbekampagne."},
]

# ============================================================
# HISTORISCHE JAHRESEVENTS (wird per Jahreswechsel ausgelöst)
# effect: money | fans | market_boom | market_crash | hype
# ============================================================
HISTORICAL_YEAR_EVENTS = {
    1930: {"text": "Weltwirtschaftskrise. -20% Profit. Fokus auf Billig-Logik.", "effect": "money", "value": -10000},
    1931: {"text": "Erster 'Logic-Contest'. Forschungspunkte-Bonus (+25 RP).", "effect": "hype", "value": 20},
    1932: {"text": "Olympia Los Angeles. Thema 'Sport' wird Trend.", "effect": "fans", "value": 5000},
    1933: {"text": "Ende der Prohibition. Bars brauchen Unterhaltung (+20% Sales).", "effect": "money", "value": 10000},
    1934: {"text": "Erfindung des Radars. Technik-Hype für Detektiv-Themen.", "effect": "hype", "value": 20},
    1935: {"text": "Monopoly Veröffentlichung. Thema 'Brettspiel' ist Gigantisch.", "effect": "fans", "value": 5000},
    1936: {"text": "Jesse Owens Erfolg. Thema 'Leichtathletik' erhält Boost.", "effect": "hype", "value": 20},
    1937: {"text": "Luftschiff-Unglück. Thema 'Luftfahrt' verliert Hype (-50%).", "effect": "hype", "value": 20},
    1938: {"text": "Mars-Hörspiel Panik. Thema 'Aliens' wird zum Dauerbrenner.", "effect": "hype", "value": 20},
    1939: {"text": "Ausbruch 2. Weltkrieg. Steuern +10%, Recruiting verlangsamt.", "effect": "hype", "value": 20},
    1940: {"text": "Enigma-Entschlüsselung. Forschung 'Logik' wird 30% effektiver.", "effect": "hype", "value": 20},
    1941: {"text": "Pearl Harbor. Thema 'Pazifik-Krieg' wird Trend.", "effect": "fans", "value": 5000},
    1942: {"text": "Zuse Z3 Demonstration. Thema 'Mathematik' erhält +200% Hype.", "effect": "hype", "value": 20},
    1943: {"text": "Casablanca Film-Hype. Thema 'Agenten/Liebe' wird Trend.", "effect": "fans", "value": 5000},
    1944: {"text": "D-Day. Thema 'Militär' erreicht Allzeithoch.", "effect": "hype", "value": 20},
    1945: {"text": "Kriegsende. Friedens-Feiern (+100% Sales).", "effect": "money", "value": 10000},
    1946: {"text": "Erster Linienflug. Thema 'Pioniere' wird Trend.", "effect": "fans", "value": 5000},
    1947: {"text": "Roswell-UFO. Thema 'UFO' bringt 5 Jahre Hype.", "effect": "hype", "value": 20},
    1948: {"text": "Marshall-Plan. Firmen-Zuschuss (Einmalig 1.000$).", "effect": "money", "value": -10000},
    1949: {"text": "Erfindung der LP-Platte. Sound-Forschung wird freigeschaltet.", "effect": "hype", "value": 20},
    1950: {"text": "Koreakrieg. Thema 'Militär' bleibt stark.", "effect": "hype", "value": 20},
    1951: {"text": "Erste Computer 'UNIVAC'. Großrechner-Wahn (+50% Prestige).", "effect": "hype", "value": 20},
    1952: {"text": "Erstes Video-Game (OXO). Geburtsstunde digitaler Unterhaltung.", "effect": "hype", "value": 20},
    1953: {"text": "DNA-Entdeckung. Thema 'Wissenschaft' wird Trend.", "effect": "fans", "value": 5000},
    1954: {"text": "Wunder von Bern. Thema 'Fussball' ist Pflicht für Erfolg.", "effect": "hype", "value": 20},
    1955: {"text": "Disneyland. Thema 'Themenpark' boomt.", "effect": "hype", "value": 20},
    1956: {"text": "Elvis Presley Durchbruch. Thema 'Musik/Rock' ist Trend.", "effect": "fans", "value": 5000},
    1957: {"text": "Sputnik 1. Weltraum-Trend (500% Hype).", "effect": "fans", "value": 5000},
    1958: {"text": "Tennis for Two. Sport-Genre wird moderner.", "effect": "hype", "value": 20},
    1959: {"text": "Barbie-Puppe. Thema 'Mode/Puppen' wird Trend.", "effect": "fans", "value": 5000},
    1960: {"text": "Pille-Einführung. Thema 'Freiheit' wird Trend.", "effect": "fans", "value": 5000},
    1961: {"text": "Berliner Mauerbau. Exportkosten nach Osten steigen um 50%.", "effect": "hype", "value": 20},
    1962: {"text": "Spacewar! Release. Action-Genre wird erfunden.", "effect": "hype", "value": 20},
    1963: {"text": "Kennedy Attentat. Weltweite Trauer: Sales -30%.", "effect": "money", "value": -10000},
    1964: {"text": "Beatles in USA. Thema 'Band' erhält massiven Bonus.", "effect": "hype", "value": 20},
    1965: {"text": "Vietnam-Eskalation. Thema 'Chaos/Protest' wird Trend.", "effect": "fans", "value": 5000},
    1966: {"text": "Star Trek. Sci-Fi RPGs werden möglich.", "effect": "hype", "value": 20},
    1967: {"text": "Summer of Love. Thema 'Hippie' wird Trend.", "effect": "fans", "value": 5000},
    1968: {"text": "Mai-Unruhen. Personal verlangt mehr Lohn (+15%).", "effect": "hype", "value": 20},
    1969: {"text": "Apollo 11. Maximaler Hype für Technik-Menschheit.", "effect": "hype", "value": 20},
    1970: {"text": "Earth Day Start. Thema 'Natur' wird Trend.", "effect": "fans", "value": 5000},
    1971: {"text": "Oregon Trail. Thema 'Pioniere/Lernen' wird Trend.", "effect": "fans", "value": 5000},
    1972: {"text": "Pong Release. Die Industrie explodiert (+200% Markt).", "effect": "fans", "value": 5000},
    1973: {"text": "Ölkrise. Stromkosten im Studio +50%.", "effect": "hype", "value": 20},
    1974: {"text": "D&D Veröffentlichung. RPG-Genre wird massentauglich.", "effect": "hype", "value": 20},
    1975: {"text": "Bill Gates gründet MS. Rivalen-KI wird intelligenter.", "effect": "hype", "value": 20},
    1976: {"text": "Apple I Release. Heimcomputer-Markt öffnet sich.", "effect": "fans", "value": -5000},
    1977: {"text": "Star Wars. Thema 'Weltraum-Krieg' ist Gigantisch.", "effect": "fans", "value": 5000},
    1978: {"text": "Space Invaders. Action-Genre dominiert den Markt.", "effect": "fans", "value": -5000},
    1979: {"text": "Sony Walkman. Sound-Marketing wird verfügbar.", "effect": "hype", "value": 20},
    1980: {"text": "Pac-Man Fieber. Geschicklichkeits-Genre ist Trend.", "effect": "fans", "value": 5000},
    1981: {"text": "IBM PC Veröffentlichung. Standardisierung der Büro-Technik.", "effect": "hype", "value": 20},
    1982: {"text": "Marktüberschwemmung. **Crash:** Nur Top-Spiele verkaufen sich.", "effect": "hype", "value": 20},
    1983: {"text": "Dragon's Lair (LD). Grafik-Anforderungen steigen massiv.", "effect": "hype", "value": 20},
    1984: {"text": "Tetris Erfindung. Puzzle-Genre erhält +300% Hype.", "effect": "hype", "value": 20},
    1985: {"text": "Super Mario Bros. Platformer wird zum Weltstandard.", "effect": "hype", "value": 20},
    1986: {"text": "Zelda Release. Umfang-Anforderungen steigen (Speichern).", "effect": "hype", "value": 20},
    1987: {"text": "Final Fantasy. RPG-Storytelling wird wichtiger.", "effect": "hype", "value": 20},
    1988: {"text": "Mega Drive Launch. 16-Bit Grafik wird Erwartungs-Standard.", "effect": "hype", "value": 20},
    1989: {"text": "Gameboy Release. Der Handheld-Markt explodiert.", "effect": "fans", "value": -5000},
    1990: {"text": "Mauerfall (BRD). Neuer Markt 'Ostdeutschland' (+15% Sales).", "effect": "money", "value": 10000},
    1991: {"text": "Street Fighter II. Fighting-Genre wird Trend.", "effect": "fans", "value": 5000},
    1992: {"text": "Wolfenstein 3D. Ego-Shooter Genre wird erfunden.", "effect": "hype", "value": 20},
    1993: {"text": "Doom Release. Gewalt-Debatte: Zensur-Risiko steigt.", "effect": "hype", "value": 20},
    1994: {"text": "PlayStation Launch. CD-ROM wird zum Pflicht-Medium.", "effect": "hype", "value": 20},
    1995: {"text": "Windows 95. PC-Markt wird Einsteigerfreundlich.", "effect": "fans", "value": -5000},
    1996: {"text": "Pokémon Boom. Thema 'Monster' ist unschlagbar.", "effect": "hype", "value": 20},
    1997: {"text": "Ultima Online. MMO-Zeitalter beginnt (Serverkosten!).", "effect": "hype", "value": 20},
    1998: {"text": "Metal Gear Solid. Stealth-Action wird Trend.", "effect": "fans", "value": 5000},
    1999: {"text": "Matrix Film. Thema 'Simulation/Neo' ist Trend.", "effect": "fans", "value": 5000},
    2000: {"text": "PS2 Launch. DVD-Standard setzt sich durch.", "effect": "hype", "value": 20},
    2001: {"text": "9/11 Terror. Markt ist sensibel für Gewalt (-20%).", "effect": "fans", "value": -5000},
    2002: {"text": "Xbox Live Start. Online-Multiplayer wird Standard.", "effect": "hype", "value": 20},
    2003: {"text": "Steam Launch. Digitaler Verkauf öffnet seine Tore.", "effect": "hype", "value": 20},
    2004: {"text": "World of Warcraft. Abomodelle bringen Millionen Dollar.", "effect": "hype", "value": 20},
    2005: {"text": "YouTube Gründung. Das Ende der Print-Magazine naht.", "effect": "hype", "value": 20},
    2006: {"text": "Wii Console. Fuchtel-Steuerung wird Megatrend.", "effect": "hype", "value": 20},
    2007: {"text": "iPhone Release. Casual-Gaming vernichtet Core-Markt.", "effect": "fans", "value": -5000},
    2008: {"text": "Finanzkrise. Bank-Zinsen +20%.", "effect": "money", "value": 10000},
    2009: {"text": "Minecraft Alpha. Sandbox/Voxel wird zum Genre-König.", "effect": "hype", "value": 20},
    2010: {"text": "iPad Release. Touch-Gaming wird massiv.", "effect": "hype", "value": 20},
    2011: {"text": "Twitch Launch. Streamer entscheiden über Erfolg/Misserfolg.", "effect": "hype", "value": 20},
    2012: {"text": "Crowdfunding-Boom. Du kannst Projekte vorfinanzieren lassen.", "effect": "hype", "value": 20},
    2013: {"text": "GTA V Release. Open-World Standards sind extrem hoch.", "effect": "hype", "value": 20},
    2014: {"text": "VR-Fieber (Oculus). Thema 'VR' bringt Prestige.", "effect": "hype", "value": 20},
    2015: {"text": "Witcher 3 Release. Story-Telling muss Weltklasse sein.", "effect": "hype", "value": 20},
    2016: {"text": "Switch Ankündigung. Hybrid-Gaming wird Thema.", "effect": "hype", "value": 20},
    2017: {"text": "Battle Royale Boom. Jeder will 100-Spieler-Modus.", "effect": "hype", "value": 20},
    2018: {"text": "Raytracing-GPU. Grafik-Wertungen über 90 fordern RT.", "effect": "hype", "value": 20},
    2019: {"text": "Game Pass Start. Neue Monetarisierung: Pauschale.", "effect": "hype", "value": 20},
    2020: {"text": "Pandemie / Lockdown. Alle Sales +150%. Home-Office möglich.", "effect": "money", "value": 10000},
    2021: {"text": "Krypto-Crash. In-Game Krypto-Gewinne wertlos.", "effect": "hype", "value": 20},
    2022: {"text": "Elden Ring Boom. Schwierige Spiele werden zum Trend.", "effect": "fans", "value": 5000},
    2023: {"text": "KI-Explosion. Programmierung 50% schneller (KI-Tool).", "effect": "hype", "value": 20},
    2024: {"text": "Erste Mars-Mission. Thema 'Mars' ist Trend bis Ende Spiel.", "effect": "fans", "value": 5000},
    2025: {"text": "Cyber-Brain Launch. Neue Plattform 'Neural' verfügbar.", "effect": "hype", "value": 20},
    2026: {"text": "Neural-Sync Standard. Das Spiel endet hier - oder geht ewig weiter.", "effect": "hype", "value": 20},
}



def get_year_event(calendar_year):
    """Gibt das historische Jahresevent für ein gegebenes Spieljahr zurück, oder None."""
    return HISTORICAL_YEAR_EVENTS.get(calendar_year, None)


# ============================================================
# TEMPLATES (E-Mails & Reviews)
# ============================================================
MAIL_TEMPLATES = {
    "bug_report": {
        "subject": "Beschwerde zu {game}",
        "body": "Hallo! Ich habe '{game}' gespielt, aber es stürzt ständig ab. Bitte behebt die Fehler!",
    },
    "fan_praise": {
        "subject": "Ich liebe {game}!",
        "body": "Hey! '{game}' ist fantastisch. Besonders das Thema {topic} gefällt mir sehr gut. Weiter so!",
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
        aw = p.get("available_week")
        ew = p.get("end_week")
        start = float(aw) if aw is not None else 0.0
        end = float(ew) if ew is not None else 99999.0
        if start <= current_week <= end:
            available.append(p)
    return available


def get_available_features(week):
    """Gibt Engine-Features zurück, die in der aktuellen Woche erforschbar sind.
    Unterstützt sowohl 'week' (alt) als auch 'unlock_year' (neu, historisch).
    """
    current_week = int(week)
    result = []
    for f in ENGINE_FEATURES:
        if "week" in f:
            # Altes Format: direkte Woche
            if int(f["week"]) <= current_week:
                result.append(f)
        elif "unlock_year" in f:
            # Neues Format: unlock_year → Spielwoche berechnen
            unlock_week = (f["unlock_year"] - START_YEAR) * WEEKS_PER_YEAR + 1
            if unlock_week <= current_week:
                result.append(f)
    return result


def get_feature_unlock_week(feature):
    """Gibt die Spielwoche zurück, ab der ein Feature erforschbar ist."""
    if "week" in feature:
        return int(feature["week"])
    elif "unlock_year" in feature:
        return (feature["unlock_year"] - START_YEAR) * WEEKS_PER_YEAR + 1
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
    {"name": "Logistik",        "unlock_year": 1930, "synergy": "Strategie", "hype_level": 3},
    {"name": "Schach",          "unlock_year": 1930, "synergy": "Puzzle",    "hype_level": 2},
    {"name": "Mathematik",      "unlock_year": 1930, "synergy": "Puzzle",    "hype_level": 3},
    {"name": "Astronomie",      "unlock_year": 1931, "synergy": "Strategie", "hype_level": 2},
    {"name": "Landwirtschaft",  "unlock_year": 1931, "synergy": "Simulation","hype_level": 2},
    {"name": "Kochen",          "unlock_year": 1932, "synergy": "Simulation","hype_level": 1},
    {"name": "Politik",         "unlock_year": 1932, "synergy": "Strategie", "hype_level": 2},
    {"name": "Detektiv",        "unlock_year": 1933, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Kartenspiele",    "unlock_year": 1933, "synergy": "Puzzle",    "hype_level": 3},
    {"name": "Architektur",     "unlock_year": 1934, "synergy": "Simulation","hype_level": 2},
    {"name": "Postwesen",       "unlock_year": 1934, "synergy": "Simulation","hype_level": 1},
    {"name": "Zirkus",          "unlock_year": 1935, "synergy": "Casual",    "hype_level": 2},
    {"name": "Bergbau",         "unlock_year": 1935, "synergy": "Simulation","hype_level": 2},
    {"name": "Eisenbahn",       "unlock_year": 1936, "synergy": "Simulation","hype_level": 3},
    {"name": "Seefahrt",        "unlock_year": 1936, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Kryptografie",    "unlock_year": 1937, "synergy": "Puzzle",    "hype_level": 4},
    {"name": "Feuerwehr",       "unlock_year": 1937, "synergy": "Simulation","hype_level": 2},
    {"name": "Mars-Invasion",   "unlock_year": 1938, "synergy": "Action",    "hype_level": 4},
    {"name": "Zauberei",        "unlock_year": 1938, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Militär",         "unlock_year": 1939, "synergy": "Strategie", "hype_level": 4},
    {"name": "Chemie",          "unlock_year": 1939, "synergy": "Puzzle",    "hype_level": 2},

    # === Die Aufbau-Jahre 1940–1959 ===
    {"name": "U-Boot",          "unlock_year": 1940, "synergy": "Simulation","hype_level": 3},
    {"name": "Luftschlacht",    "unlock_year": 1941, "synergy": "Action",    "hype_level": 4},
    {"name": "Spionage",        "unlock_year": 1942, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Panzer",          "unlock_year": 1943, "synergy": "Simulation","hype_level": 3},
    {"name": "Fallschirmjäger", "unlock_year": 1944, "synergy": "Action",    "hype_level": 2},
    {"name": "Wiederaufbau",    "unlock_year": 1945, "synergy": "Simulation","hype_level": 3},
    {"name": "Journalismus",    "unlock_year": 1946, "synergy": "Strategie", "hype_level": 2},
    {"name": "UFOs",            "unlock_year": 1947, "synergy": "Abenteuer", "hype_level": 4},
    {"name": "Roboter",         "unlock_year": 1948, "synergy": "Action",    "hype_level": 3},
    {"name": "Dschungel",       "unlock_year": 1949, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Archäologie",     "unlock_year": 1950, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Weltraum",        "unlock_year": 1951, "synergy": "Simulation","hype_level": 4},
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
    {"name": "Mafia",           "unlock_year": 1961, "synergy": "Action",    "hype_level": 3},
    {"name": "Fantasy",         "unlock_year": 1962, "synergy": "RPG",       "hype_level": 3},
    {"name": "Agenten",         "unlock_year": 1963, "synergy": "Abenteuer", "hype_level": 4},
    {"name": "Popstars",        "unlock_year": 1964, "synergy": "Casual",    "hype_level": 3},
    {"name": "Dinosaurier",     "unlock_year": 1965, "synergy": "Action",    "hype_level": 4},
    {"name": "Ninjas",          "unlock_year": 1966, "synergy": "Action",    "hype_level": 3},
    {"name": "Hippies",         "unlock_year": 1967, "synergy": "Simulation","hype_level": 2},
    {"name": "Weltrevolution",  "unlock_year": 1968, "synergy": "Strategie", "hype_level": 3},
    {"name": "Mondbasis",       "unlock_year": 1969, "synergy": "Simulation","hype_level": 5},
    {"name": "Kung-Fu",         "unlock_year": 1970, "synergy": "Kampfspiel","hype_level": 3},
    {"name": "Piraten",         "unlock_year": 1971, "synergy": "Abenteuer", "hype_level": 4},
    {"name": "Basketball",      "unlock_year": 1972, "synergy": "Sport",     "hype_level": 2},
    {"name": "Motorrad",        "unlock_year": 1973, "synergy": "Rennspiel", "hype_level": 3},
    {"name": "Verliese",        "unlock_year": 1974, "synergy": "RPG",       "hype_level": 4},
    {"name": "Polizei",         "unlock_year": 1975, "synergy": "Action",    "hype_level": 2},
    {"name": "Alien-Jagd",      "unlock_year": 1976, "synergy": "Action",    "hype_level": 3},
    {"name": "Laserschwert",    "unlock_year": 1977, "synergy": "Action",    "hype_level": 4},
    {"name": "Invaders",        "unlock_year": 1978, "synergy": "Action",    "hype_level": 4},
    {"name": "Horrorhaus",      "unlock_year": 1979, "synergy": "Horror",    "hype_level": 3},

    # === Digitale Explosion 1980–1999 ===
    {"name": "Gelbe Fresspunkte","unlock_year": 1980, "synergy": "Puzzle",   "hype_level": 5},
    {"name": "Büro-Alltag",     "unlock_year": 1981, "synergy": "Simulation","hype_level": 1},
    {"name": "Cyberpunk",       "unlock_year": 1982, "synergy": "RPG",       "hype_level": 4},
    {"name": "Vampire",         "unlock_year": 1983, "synergy": "Horror",    "hype_level": 3},
    {"name": "Breakdance",      "unlock_year": 1984, "synergy": "Casual",    "hype_level": 2},
    {"name": "Klempner",        "unlock_year": 1985, "synergy": "Action",    "hype_level": 5},
    {"name": "Postapokalypse",  "unlock_year": 1986, "synergy": "RPG",       "hype_level": 3},
    {"name": "Mechs",           "unlock_year": 1987, "synergy": "Action",    "hype_level": 4},
    {"name": "Skateboarding",   "unlock_year": 1988, "synergy": "Sport",     "hype_level": 3},
    {"name": "Taschenmonster",  "unlock_year": 1989, "synergy": "RPG",       "hype_level": 5},
    {"name": "Krankenhaus",     "unlock_year": 1990, "synergy": "Simulation","hype_level": 3},
    {"name": "Freizeitpark",    "unlock_year": 1991, "synergy": "Simulation","hype_level": 4},
    {"name": "Mars-Shooter",    "unlock_year": 1992, "synergy": "Action",    "hype_level": 5},
    {"name": "Urzeit/Survival", "unlock_year": 1993, "synergy": "Simulation","hype_level": 3},
    {"name": "Anime",           "unlock_year": 1994, "synergy": "RPG",       "hype_level": 3},
    {"name": "Hacking",         "unlock_year": 1995, "synergy": "Puzzle",    "hype_level": 4},
    {"name": "Stealth-Agent",   "unlock_year": 1996, "synergy": "Action",    "hype_level": 4},
    {"name": "Elfen & Orks",    "unlock_year": 1997, "synergy": "RPG",       "hype_level": 3},
    {"name": "Survival-Insel",  "unlock_year": 1998, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "Skandal-TV",      "unlock_year": 1999, "synergy": "Simulation","hype_level": 2},

    # === Neues Jahrtausend 2000–2015 ===
    {"name": "Lebens-Sim",      "unlock_year": 2000, "synergy": "Simulation","hype_level": 5},
    {"name": "Zombie-Hype",     "unlock_year": 2001, "synergy": "Horror",    "hype_level": 4},
    {"name": "Parkplatz-Manager","unlock_year": 2002, "synergy": "Simulation","hype_level": 1},
    {"name": "E-Sport",         "unlock_year": 2003, "synergy": "Action",    "hype_level": 3},
    {"name": "Zauberschule",    "unlock_year": 2004, "synergy": "RPG",       "hype_level": 4},
    {"name": "Sandbox/Voxel",   "unlock_year": 2005, "synergy": "Abenteuer", "hype_level": 5},
    {"name": "Wikinger",        "unlock_year": 2006, "synergy": "Action",    "hype_level": 4},
    {"name": "Smartphones",     "unlock_year": 2007, "synergy": "Puzzle",    "hype_level": 3},
    {"name": "Freerunning",     "unlock_year": 2008, "synergy": "Action",    "hype_level": 2},
    {"name": "Block-Bauen",     "unlock_year": 2009, "synergy": "Abenteuer", "hype_level": 5},
    {"name": "Social Network",  "unlock_year": 2010, "synergy": "Simulation","hype_level": 3},
    {"name": "Indie-Entwickler","unlock_year": 2011, "synergy": "Abenteuer", "hype_level": 2},
    {"name": "Battle-Royale",   "unlock_year": 2012, "synergy": "Action",    "hype_level": 5},
    {"name": "VR-Simulation",   "unlock_year": 2013, "synergy": "Simulation","hype_level": 3},
    {"name": "Farming-Hype",    "unlock_year": 2014, "synergy": "Simulation","hype_level": 4},
    {"name": "Cyber-Krieg",     "unlock_year": 2015, "synergy": "Strategie", "hype_level": 3},

    # === Die Zukunft 2016–2026 ===
    {"name": "AR-Jagd",         "unlock_year": 2016, "synergy": "Action",    "hype_level": 3},
    {"name": "Krypto-Mining",   "unlock_year": 2017, "synergy": "Strategie", "hype_level": 2},
    {"name": "Mars-Kolonisierung","unlock_year": 2018,"synergy": "Simulation","hype_level": 4},
    {"name": "Streaming-Star",  "unlock_year": 2019, "synergy": "Simulation","hype_level": 3},
    {"name": "KI-Dystopie",     "unlock_year": 2020, "synergy": "Abenteuer", "hype_level": 3},
    {"name": "NFT-Sammeln",     "unlock_year": 2021, "synergy": "Strategie", "hype_level": 1},
    {"name": "Metaverse",       "unlock_year": 2022, "synergy": "Simulation","hype_level": 2},
    {"name": "KI-Utopie",       "unlock_year": 2023, "synergy": "Strategie", "hype_level": 4},
    {"name": "Endzeit-Bote",    "unlock_year": 2024, "synergy": "Action",    "hype_level": 3},
    {"name": "Gen-Labor",       "unlock_year": 2025, "synergy": "Simulation","hype_level": 4},
    {"name": "Neural-Link",     "unlock_year": 2026, "synergy": "RPG",       "hype_level": 5},
]


def get_historical_topics_for_year(calendar_year):
    """Gibt alle historischen Themen zurück, die bis zum gegebenen Jahr verfügbar sind."""
    return [t for t in HISTORICAL_TOPICS if t["unlock_year"] <= calendar_year]


def get_newly_unlocked_topics(calendar_year):
    """Gibt alle Themen zurück, die GENAU in diesem Jahr neu verfügbar werden."""
    return [t for t in HISTORICAL_TOPICS if t["unlock_year"] == calendar_year]

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
    }
]


