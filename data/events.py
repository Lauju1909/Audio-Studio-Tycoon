"""Zufalls-, historische und Jahres-Events."""
from data.core import *  # noqa: F401,F403
from data.content import *  # noqa: F401,F403
from data.people import *  # noqa: F401,F403
from data.studio import *  # noqa: F401,F403
from data.economy import *  # noqa: F401,F403

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
