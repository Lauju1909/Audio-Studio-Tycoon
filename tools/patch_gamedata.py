import re
import os

game_data_path = "game_data.py"

with open(game_data_path, "r", encoding="utf-8") as f:
    content = f.read()

# Neue Technologien
NEW_TECHS = """
    {"name": "Kantinen-Ausbau 1", "cost": 15000, "week": 12, "research_weeks": 3, "description": "Schaltet fortgeschrittene Getränkestationen frei."},
    {"name": "Kantinen-Ausbau 2", "cost": 35000, "week": 26, "research_weeks": 4, "description": "Schaltet Snack-Automaten und Pizzaöfen frei."},
    {"name": "Kantinen-Ausbau 3", "cost": 75000, "week": 48, "research_weeks": 5, "description": "Schaltet Gourmet-Küche und Wein-Regal frei."},
    {"name": "Büroausstattung 2", "cost": 30000, "week": 18, "research_weeks": 4, "description": "Schaltet weitere Pflanzen und Dekorationen frei."},
    {"name": "Büroausstattung 3", "cost": 65000, "week": 36, "research_weeks": 5, "description": "Schaltet exotische Zimmerpflanzen und Luxus-Deko frei."},
    {"name": "Freizeit & Spiel 1", "cost": 25000, "week": 16, "research_weeks": 3, "description": "Schaltet Tischkicker und Dartscheiben frei."},
    {"name": "Freizeit & Spiel 2", "cost": 45000, "week": 32, "research_weeks": 4, "description": "Schaltet Billardtische und Flipper frei."},
    {"name": "Freizeit & Spiel 3", "cost": 95000, "week": 64, "research_weeks": 6, "description": "Schaltet VR-Stationen und Heimkino frei."},
    {"name": "Ergonomie am Arbeitsplatz 2", "cost": 60000, "week": 30, "research_weeks": 5, "description": "Schaltet Stehschreibtische frei."},
    {"name": "Ergonomie am Arbeitsplatz 3", "cost": 120000, "week": 60, "research_weeks": 6, "description": "Schaltet High-End Laufband-Tische frei."},
    {"name": "High-End Workstations 1", "cost": 85000, "week": 40, "research_weeks": 5, "description": "Schaltet Dual-Monitor Setups und Grafik-Tablets frei."},
    {"name": "High-End Workstations 2", "cost": 150000, "week": 72, "research_weeks": 6, "description": "Schaltet Triple-Monitore und Render-Farmen frei."},
    {"name": "Gamer-Setup", "cost": 70000, "week": 38, "research_weeks": 4, "description": "Schaltet RGB-Desks und Gamer-Schreibtische frei."},
    {"name": "Audio-Meisterschaft 2", "cost": 110000, "week": 44, "research_weeks": 5, "description": "Schaltet Drum-Set und Flügel für Sound-Boosts frei."},
    {"name": "Audio-Meisterschaft 3", "cost": 250000, "week": 80, "research_weeks": 7, "description": "Schaltet Regie-Platz und High-End Lautsprecher frei."},
    {"name": "Dekorations-Wahn 1", "cost": 20000, "week": 14, "research_weeks": 3, "description": "Schaltet kleine Bücheregale und Poster frei."},
    {"name": "Dekorations-Wahn 2", "cost": 50000, "week": 28, "research_weeks": 4, "description": "Schaltet Pokal-Vitrinen und Lava-Lampen frei."},
    {"name": "Dekorations-Wahn 3", "cost": 90000, "week": 50, "research_weeks": 5, "description": "Schaltet Neon-Schilder, Teppiche und Globen frei."},
    {"name": "Motion Capture Studio", "cost": 400000, "week": 96, "research_weeks": 8, "description": "Schaltet MoCap-Kameras frei."},
"""

if "Kantinen-Ausbau 1" not in content:
    content = content.replace("]\n\n# ============================================================\n# SCHWIERIGKEITSGRADE", NEW_TECHS + "]\n\n# ============================================================\n# SCHWIERIGKEITSGRADE")

# Neue Objekte
NEW_OBJECTS = """
    # Pflanzen (10)
    "plant_cactus": {"name": "Kaktus", "cost": 100, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Sticht leicht. +1 Moral.", "morale_bonus": 1},
    "plant_fern": {"name": "Farn", "cost": 250, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein schöner Farn. +1 Moral.", "morale_bonus": 1},
    "plant_rubber": {"name": "Gummibaum", "cost": 400, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein großer Gummibaum. +1 Moral.", "req_tech": "Büroausstattung 2", "morale_bonus": 1},
    "plant_monstera": {"name": "Monstera", "cost": 600, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Schickes Blattwerk. +2 Moral.", "req_tech": "Büroausstattung 2", "morale_bonus": 2},
    "plant_bonsai": {"name": "Bonsai", "cost": 800, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Fördert die Ruhe. +2 Moral.", "req_tech": "Büroausstattung 2", "morale_bonus": 2},
    "plant_palm": {"name": "Zimmer-Palme", "cost": 1200, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Karibik im Büro. +2 Moral.", "req_tech": "Büroausstattung 3", "morale_bonus": 2},
    "plant_oak": {"name": "Eiche im Topf", "cost": 2000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein ganzer Baum drinnen. +3 Moral.", "req_tech": "Büroausstattung 3", "morale_bonus": 3},
    "plant_venus": {"name": "Venusfliegenfalle", "cost": 1500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Fängt nervige Bugs? +2 Moral.", "req_tech": "Büroausstattung 3", "morale_bonus": 2},

    # Essen/Trinken (9)
    "drink_espresso": {"name": "Espresso-Maschine", "cost": 1500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Schneller Wachmacher. +2 Moral.", "req_tech": "Kantinen-Ausbau 1", "morale_bonus": 2},
    "drink_tea": {"name": "Tee-Kocher", "cost": 900, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Für eine entspannte Pause. +1 Moral.", "req_tech": "Kantinen-Ausbau 1", "morale_bonus": 1},
    "food_snack": {"name": "Snack-Automat", "cost": 4000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Chips und Schoko. +2 Moral.", "req_tech": "Kantinen-Ausbau 2", "morale_bonus": 2},
    "drink_soft": {"name": "Softdrink-Automat", "cost": 5000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Cola auf Knopfdruck. +2 Moral.", "req_tech": "Kantinen-Ausbau 2", "morale_bonus": 2},
    "fridge_mini": {"name": "Mini-Kühlschrank", "cost": 2500, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Kühlt die Getränke. +1 Moral.", "req_tech": "Kantinen-Ausbau 2", "morale_bonus": 1},
    "food_pizza": {"name": "Pizza-Ofen", "cost": 12000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Frische Pizza für Crunch-Times. +4 Moral.", "req_tech": "Kantinen-Ausbau 2", "morale_bonus": 4},
    "food_gourmet": {"name": "Gourmet-Küche", "cost": 30000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Ein eigener Kochbereich. +6 Moral.", "req_tech": "Kantinen-Ausbau 3", "morale_bonus": 6},
    "drink_wine": {"name": "Wein-Regal", "cost": 15000, "layer": "furniture", "employees": 0, "bonus": None, "desc": "Für erfolgreiche Abschlüsse. +3 Moral.", "req_tech": "Kantinen-Ausbau 3", "morale_bonus": 3},

    # Unterhaltung (12)
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

    # Tische/Schreibtische (11)
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

    # Sound-Technik (8)
    "sound_mic": {"name": "Mikrofon-Ständer", "cost": 8000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+5% Sound-Bonus.", "req_tech": "Studios & Kabinen"},
    "sound_synth": {"name": "Synthesizer-Station", "cost": 15000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+8% Sound-Bonus.", "req_tech": "Studios & Kabinen"},
    "sound_piano": {"name": "Flügel (Klavier)", "cost": 40000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+12% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 2"},
    "sound_drum": {"name": "Drum-Set", "cost": 30000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+10% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 2"},
    "sound_console": {"name": "Mix-Konsole Rießig", "cost": 50000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+15% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 3"},
    "sound_speakers": {"name": "High-End Lautsprecher", "cost": 20000, "layer": "furniture", "employees": 0, "bonus": "sound", "desc": "+5% Sound passiv pro Lautsprecher.", "req_tech": "Audio-Meisterschaft 3"},
    "sound_director": {"name": "Regie-Platz", "cost": 80000, "layer": "furniture", "employees": 1, "bonus": "sound", "desc": "+25% Sound-Bonus.", "req_tech": "Audio-Meisterschaft 3"},
    "sound_wall": {"name": "Akustik-Wände", "cost": 3500, "layer": "structure", "employees": 0, "bonus": "sound", "desc": "Schallisolierte Wand. +1% Sound passiv.", "req_tech": "Studios & Kabinen"},

    # Grafik-Technik (7)
    "gfx_drawing": {"name": "Zeichenblock-Tisch", "cost": 2500, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+5% Grafik-Bonus."},
    "gfx_tablet": {"name": "Grafik-Tablet", "cost": 6000, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+10% Grafik-Bonus.", "req_tech": "High-End Workstations 1"},
    "gfx_dual": {"name": "Dual-Monitor-Setup", "cost": 12000, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+15% Grafik-Bonus.", "req_tech": "High-End Workstations 1"},
    "gfx_triple": {"name": "Triple-Monitor", "cost": 25000, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+20% Grafik-Bonus.", "req_tech": "High-End Workstations 2"},
    "gfx_green": {"name": "Greenscreen", "cost": 40000, "layer": "structure", "employees": 0, "bonus": "graphics", "desc": "Für Trailer und Filme. +5% Grafik passiv.", "req_tech": "High-End Workstations 2"},
    "gfx_mocap": {"name": "MoCap-Kameras", "cost": 150000, "layer": "furniture", "employees": 1, "bonus": "graphics", "desc": "+30% Grafik-Bonus.", "req_tech": "Motion Capture Studio"},
    "gfx_render": {"name": "Render-Farm", "cost": 200000, "layer": "furniture", "employees": 0, "bonus": "graphics", "desc": "Passiv +20% Grafik.", "req_tech": "High-End Workstations 2"},

    # Entwickler-Boni (6)
    "dev_board": {"name": "Whiteboard", "cost": 1500, "layer": "furniture", "employees": 0, "bonus": "qa", "desc": "-5% Bugs passiv.", "req_tech": "Kantinen-Ausbau 1"},
    "srv_small": {"name": "Server-Rack klein", "cost": 8000, "layer": "furniture", "employees": 0, "bonus": "mmo", "desc": "Kleine MMO-Kapazität."},
    "srv_big": {"name": "Server-Schrank", "cost": 30000, "layer": "furniture", "employees": 0, "bonus": "mmo", "desc": "Gute MMO-Kapazität.", "req_tech": "Live-Service Architektur"},
    "srv_center": {"name": "Server-Zentrum", "cost": 100000, "layer": "furniture", "employees": 0, "bonus": "mmo", "desc": "Massive MMO-Kapazität.", "req_tech": "Live-Service Architektur"},
    "dev_ops": {"name": "DevOps-Station", "cost": 40000, "layer": "furniture", "employees": 1, "bonus": "qa", "desc": "-30% Bugs passiv.", "req_tech": "Live-Service Architektur"},

    # Dekoration (11)
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

    # Strukturen (3 neue)
    "wall_steel": {"name": "Wand Stahl", "cost": 500, "layer": "structure", "employees": 0, "bonus": None, "desc": "Massive Wand."},
    "wall_glass": {"name": "Wand Glas", "cost": 1000, "layer": "structure", "employees": 0, "bonus": None, "desc": "Transparente Wand. Sehr modern."},
    "door_glass": {"name": "Tür Glas", "cost": 1200, "layer": "structure", "employees": 0, "bonus": None, "desc": "Glastür."},
"""

if '"plant_cactus":' not in content:
    content = content.replace('"sound_booth":   {"name": "Sound-Kabine",', NEW_OBJECTS + '\n    "sound_booth":   {"name": "Sound-Kabine",')

with open(game_data_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Game Data successfully patched with massive content.")
