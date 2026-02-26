"""
Statische Spieldaten für Audio Studio Tycoon - Audio Edition.

Enthält Themen, Genres, Kompatibilitätstabelle, Slider-Gewichtungen,
Plattformen, Engine-Features, Mitarbeiter-Daten und Zufallsereignisse.
"""

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
    {"name": "Spionage", "cost": 5000, "week": 2, "research_weeks": 2},
    {"name": "Piraten", "cost": 8000, "week": 3, "research_weeks": 2},
    {"name": "Zombies", "cost": 12000, "week": 5, "research_weeks": 3},
    {"name": "Krankenhaus", "cost": 15000, "week": 8, "research_weeks": 3},
    {"name": "Schule", "cost": 10000, "week": 10, "research_weeks": 2},
    {"name": "Stadt", "cost": 18000, "week": 15, "research_weeks": 3},
    {"name": "Weltraum", "cost": 25000, "week": 20, "research_weeks": 4},
    {"name": "Krieg", "cost": 30000, "week": 25, "research_weeks": 4},
    {"name": "Musik", "cost": 12000, "week": 12, "research_weeks": 3},
    {"name": "Kochen", "cost": 8000, "week": 6, "research_weeks": 2},
    {"name": "Tiere", "cost": 15000, "week": 15, "research_weeks": 3},
    {"name": "Horror", "cost": 25000, "week": 22, "research_weeks": 4},
    {"name": "Superheld", "cost": 40000, "week": 30, "research_weeks": 5},
    {"name": "Cyberpunk", "cost": 50000, "week": 40, "research_weeks": 6},
    {"name": "Detektiv", "cost": 20000, "week": 18, "research_weeks": 3},
    {"name": "Dinosaurier", "cost": 35000, "week": 28, "research_weeks": 4},
    {"name": "Vampire", "cost": 22000, "week": 20, "research_weeks": 3},
    {"name": "Feuerwehr", "cost": 15000, "week": 14, "research_weeks": 3},
    {"name": "Polizei", "cost": 18000, "week": 16, "research_weeks": 3},
    {"name": "Wilder Westen", "cost": 28000, "week": 24, "research_weeks": 4},
]

TOPICS = START_TOPICS + [t["name"] for t in RESEARCHABLE_TOPICS]

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
    #                    Act  RPG  Sim  Str  Abe  Puz  Spo  Cas  Hor  Kam  Ren
    "Fantasy":          [  2,   3,   1,   2,   3,   1,   0,   1,   1,   2,   0  ],
    "Sci-Fi":           [  3,   2,   2,   3,   2,   1,   0,   1,   2,   2,   2  ],
    "Mittelalter":      [  2,   3,   2,   3,   2,   0,   0,   0,   1,   2,   0  ],
    "Spionage":         [  3,   1,   1,   2,   3,   2,   0,   1,   1,   2,   1  ],
    "Piraten":          [  3,   2,   1,   2,   3,   1,   0,   1,   1,   2,   1  ],
    "Zombies":          [  3,   1,   0,   2,   2,   1,   0,   1,   3,   2,   0  ],
    "Sport":            [  1,   0,   2,   1,   0,   0,   3,   2,   0,   1,   1  ],
    "Rennen":           [  2,   0,   2,   0,   0,   0,   3,   2,   0,   0,   3  ],
    "Krankenhaus":      [  0,   0,   3,   1,   1,   2,   0,   2,   2,   0,   0  ],
    "Schule":           [  0,   1,   3,   1,   1,   2,   0,   2,   1,   1,   0  ],
    "Stadt":            [  0,   1,   3,   2,   1,   1,   0,   1,   0,   2,   2  ],
    "Weltraum":         [  3,   2,   2,   3,   2,   0,   0,   1,   2,   1,   2  ],
    "Krieg":            [  3,   1,   1,   3,   1,   0,   0,   0,   1,   2,   1  ],
    "Musik":            [  0,   0,   2,   0,   0,   3,   0,   3,   0,   0,   0  ],
    "Kochen":           [  0,   0,   3,   0,   0,   2,   0,   3,   0,   0,   0  ],
    "Tiere":            [  1,   1,   3,   1,   2,   2,   0,   3,   0,   1,   1  ],
    "Horror":           [  2,   1,   0,   1,   3,   1,   0,   0,   3,   1,   0  ],
    "Superheld":        [  3,   2,   0,   1,   3,   0,   0,   1,   0,   3,   1  ],
    "Cyberpunk":        [  3,   3,   1,   2,   2,   0,   0,   0,   1,   2,   2  ],
    "Detektiv":         [  1,   1,   1,   1,   3,   3,   0,   1,   2,   0,   0  ],
    "Dinosaurier":      [  3,   2,   2,   1,   3,   1,   0,   1,   2,   2,   1  ],
    "Vampire":          [  2,   3,   1,   1,   2,   1,   0,   1,   3,   2,   0  ],
    "Feuerwehr":        [  2,   1,   3,   2,   1,   1,   0,   2,   0,   0,   2  ],
    "Polizei":          [  3,   1,   2,   2,   2,   2,   0,   1,   1,   1,   2  ],
    "Wilder Westen":    [  3,   2,   1,   2,   3,   0,   0,   1,   1,   1,   2  ],
}

# ============================================================
# PLATTFORMEN
# name, Lizenzgebühr, Markt-Multiplikator, verfügbar ab Woche, Ende Woche (None = nie), Typ
# ============================================================
PLATFORMS = [
    {"name": "Zenith-Core 88",  "license_fee": 0,      "market_multi": 1.0,  "available_week": 1,  "end_week": 200,   "type": "PC"},
    {"name": "Micro-Gate",      "license_fee": 0,      "market_multi": 1.2,  "available_week": 30, "end_week": None, "type": "PC"},
    {"name": "Penguin-OS",      "license_fee": 0,      "market_multi": 0.5,  "available_week": 50, "end_week": None, "type": "PC"},
    
    {"name": "Nova-Station 1",  "license_fee": 20000,  "market_multi": 1.5,  "available_week": 1,  "end_week": 500,  "type": "Konsole"},
    {"name": "Nova-Station 2",  "license_fee": 40000,  "market_multi": 2.2,  "available_week": 80, "end_week": 1250,  "type": "Konsole"},
    
    {"name": "Kuro-Hand",       "license_fee": 15000,  "market_multi": 1.3,  "available_week": 1,  "end_week": 300,   "type": "Handheld"},
    {"name": "Kuro-Classic",    "license_fee": 30000,  "market_multi": 1.8,  "available_week": 70, "end_week": 1000,  "type": "Konsole"},
    
    {"name": "Orion-Box",       "license_fee": 25000,  "market_multi": 1.4,  "available_week": 20, "end_week": 750,  "type": "Konsole"},
    {"name": "Orion-Box 360",   "license_fee": 45000,  "market_multi": 2.0,  "available_week": 140,"end_week": 1750,  "type": "Konsole"},
    
    {"name": "Pocket-Play",     "license_fee": 10000,  "market_multi": 0.8,  "available_week": 1,  "end_week": 400,   "type": "Handheld"},
    {"name": "Smartphone",      "license_fee": 5000,   "market_multi": 2.5,  "available_week": 360,"end_week": None, "type": "Mobile"},
    {"name": "Tablet OS",       "license_fee": 7000,   "market_multi": 1.8,  "available_week": 400,"end_week": None, "type": "Mobile"},
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
]

# ============================================================
# REVIEW-TEXTE
# ============================================================
REVIEW_TEMPLATES = {
    "intro": [
        "Das neue Spiel von {company} ist da!",
        "Wir haben uns '{game}' genau angesehen.",
        "Endlich ist '{game}' auf dem Markt!"
    ],
    "positive": [
        "Die Story und das Gameplay waren erstklassig!",
        "Die technische Umsetzung ist absolut brillant.",
        "Ein Meilenstein für das Genre {genre}.",
        "Selten hat uns ein Spiel so gefesselt."
    ],
    "negative": [
        "Die Grafik ist leider total veraltet.",
        "Das Gameplay fühlt sich hölzern an.",
        "Es gibt viel zu viele Bugs zum Release.",
        "Das Thema {topic} wurde schwach umgesetzt."
    ],
    "conclusion": [
        "Ein absolutes Muss für jeden Fan!",
        "Kann man spielen, muss man aber nicht.",
        "Leider eine Enttäuschung auf ganzer Linie.",
        "Wir sind gespannt auf das nächste Projekt."
    ]
}

# ============================================================
# FAN-MAILS & BUG-REPORTS
# ============================================================
MAIL_TEMPLATES = {
    "fan_praise": {
        "subject": "Ich liebe {game}!",
        "body": "Hey! Ich spiele gerade '{game}' und es ist fantastisch. Besonders das Thema {topic} gefällt mir!"
    },
    "fan_critique": {
        "subject": "Enttäuscht von {game}",
        "body": "Eigentlich mag ich eure Spiele, aber '{game}' ist nicht so gut. Das Genre {genre} passt irgendwie nicht."
    },
    "bug_report": {
        "subject": "BUG gefunden in {game}!",
        "body": "Hilfe! Ich hänge im Level fest. Es scheint ein technisches Problem zu geben. Bitte fixen!"
    }
}

# ============================================================
# ENGINE-FEATURES (zum Freischalten / Erforschen)
# category, name, tech_bonus, cost, week, research_weeks
# ============================================================
ENGINE_FEATURES = [
    # Grafik
    {"category": "Grafik",    "name": "2D Grafik V1",        "tech_bonus": 1,  "cost": 0,      "week": 1,  "research_weeks": 1},
    {"category": "Grafik",    "name": "2D Grafik V2",        "tech_bonus": 3,  "cost": 25000,  "week": 10, "research_weeks": 6},
    {"category": "Grafik",    "name": "3D Grafik V1",        "tech_bonus": 5,  "cost": 80000,  "week": 30, "research_weeks": 12},
    {"category": "Grafik",    "name": "3D Grafik V2",        "tech_bonus": 8,  "cost": 150000, "week": 60, "research_weeks": 20},
    # Sound
    {"category": "Sound",     "name": "Mono Sound",          "tech_bonus": 1,  "cost": 0,      "week": 1,  "research_weeks": 1},
    {"category": "Sound",     "name": "Stereo Sound",        "tech_bonus": 3,  "cost": 15000,  "week": 10, "research_weeks": 4},
    {"category": "Sound",     "name": "Surround Sound",      "tech_bonus": 5,  "cost": 50000,  "week": 40, "research_weeks": 8},
    # KI
    {"category": "KI",        "name": "Einfache KI",         "tech_bonus": 1,  "cost": 0,      "week": 1,  "research_weeks": 1},
    {"category": "KI",        "name": "Fortgeschrittene KI", "tech_bonus": 3,  "cost": 30000,  "week": 20, "research_weeks": 7},
    {"category": "KI",        "name": "Lernende KI",         "tech_bonus": 6,  "cost": 90000,  "week": 50, "research_weeks": 15},
    # Gameplay
    {"category": "Gameplay",  "name": "Basis Steuerung",     "tech_bonus": 1,  "cost": 0,      "week": 1,  "research_weeks": 1},
    {"category": "Gameplay",  "name": "Physik-Engine",       "tech_bonus": 3,  "cost": 40000,  "week": 15, "research_weeks": 10},
    {"category": "Gameplay",  "name": "Online-Multiplayer",  "tech_bonus": 6,  "cost": 120000, "week": 45, "research_weeks": 18},
    # Level-Design
    {"category": "Level",     "name": "Lineares Design",     "tech_bonus": 1,  "cost": 0,      "week": 1,  "research_weeks": 1},
    {"category": "Level",     "name": "Open World",          "tech_bonus": 5,  "cost": 80000,  "week": 35, "research_weeks": 15},
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
# ZUFALLSEREIGNISSE
# ============================================================
RANDOM_EVENTS = [
    {
        "title": "Spielemesse",
        "text": "Auf der großen Spielemesse präsentierst du dein Studio! Fans steigen.",
        "effect": "fans",
        "value": 500,
    },
    {
        "title": "Wirtschaftsboom",
        "text": "Die Wirtschaft boomt! Spieler kaufen mehr.",
        "effect": "money",
        "value": 15000,
    },
    {
        "title": "Rezession",
        "text": "Eine Wirtschaftskrise trifft die Branche. Umsätze sinken.",
        "effect": "money",
        "value": -10000,
    },
    {
        "title": "Retro-Trend",
        "text": "Retro-Spiele sind plötzlich wieder total angesagt!",
        "effect": "fans",
        "value": 300,
    },
    {
        "title": "Hacker-Angriff",
        "text": "Hacker haben deine Server angegriffen! Reparaturkosten fallen an.",
        "effect": "money",
        "value": -8000,
    },
    {
        "title": "Award-Nominierung",
        "text": "Dein letztes Spiel wurde für einen Award nominiert!",
        "effect": "fans",
        "value": 1000,
    },
    {
        "title": "Steuernachzahlung",
        "text": "Das Finanzamt fordert eine Nachzahlung.",
        "effect": "money",
        "value": -12000,
    },
    {
        "title": "Spende eines Investors",
        "text": "Ein geheimnisvoller Investor glaubt an dein Studio!",
        "effect": "money",
        "value": 25000,
    },
    {
        "title": "Viral-Hit",
        "text": "Ein Video über dein Studio geht viral!",
        "effect": "fans",
        "value": 2000,
    },
    {
        "title": "Server-Ausfall",
        "text": "Dein Online-Service ist ausgefallen. Fans sind verärgert.",
        "effect": "fans",
        "value": -500,
    },
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
        "description": "Ein Workshop. +5 Skill-Punkte auf den Hauptbereich.",
    },
    {
        "name": "Fortbildung",
        "skill_boost": 10,
        "cost": 15000,
        "description": "Eine umfangreiche Fortbildung. +10 Skill-Punkte auf den Hauptbereich.",
    },
    {
        "name": "Experten-Seminar",
        "skill_boost": 20,
        "cost": 40000,
        "description": "Ein Experten-Seminar. +20 Skill-Punkte auf den Hauptbereich.",
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
    """Gibt Engine-Features zurück, die in der aktuellen Woche erforschbar sind."""
    current_week = int(week)
    return [f for f in ENGINE_FEATURES if int(f["week"]) <= current_week]

# ============================================================
# ZUFÄLLIGE MARKTEREIGNISSE (Phase 8)
# ============================================================
RANDOM_EVENTS = [
    {
        "id": "hacker_attack",
        "type": "negative",
        "duration": 4, # Wochen
        "effect": "sales_drop",
        "multiplier": 0.5
    },
    {
        "id": "viral_post",
        "type": "positive",
        "duration": 2, # Wochen
        "effect": "hype_boost",
        "hype_amount": 50
    },
    {
        "id": "industry_burnout",
        "type": "negative",
        "duration": 3, # Wochen
        "effect": "dev_speed_drop",
        "multiplier": 0.5
    }
]
