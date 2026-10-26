"""Buero, Bauobjekte, Spielgroessen, Marketing, Training."""
from data.core import *  # noqa: F401,F403
from data.content import *  # noqa: F401,F403
from data.people import *  # noqa: F401,F403

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
