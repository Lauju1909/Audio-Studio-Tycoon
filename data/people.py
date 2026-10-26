"""Mitarbeiter, Rollen, Traits und Entwicklungs-Events."""
from data.core import *  # noqa: F401,F403
from data.content import *  # noqa: F401,F403

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
