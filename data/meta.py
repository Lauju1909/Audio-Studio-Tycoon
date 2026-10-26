"""Erfolge, Merch, Esports, Upgrades, Hardware, Fanpost, Persoenlichkeit."""
from data.core import *  # noqa: F401,F403
from data.content import *  # noqa: F401,F403
from data.people import *  # noqa: F401,F403
from data.studio import *  # noqa: F401,F403
from data.economy import *  # noqa: F401,F403
from data.events import *  # noqa: F401,F403

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


# ============================================================
# PROGRESSION UNLOCKS
# ============================================================
FEATURE_UNLOCKS = {
    "esports": {"year": 2005, "name": "E-Sports"},
    "vr_headset": {"year": 2016, "name": "VR Hardware Labor"},
    "metaverse": {"year": 2018, "name": "Das AudioVerse (Metaverse)"},
    "transmedia": {"year": 2000, "name": "Filmrechte & Transmedia"},
    "ipo": {"year": 1995, "office_level": 3, "name": "Boersengang (IPO)"},
    "darknet": {"year": 2000, "name": "Cyber-Attacken / Darknet"},
    "cloud_gaming": {"year": 2010, "name": "Cloud Gaming"},
    "merch": {"year": 1990, "name": "Merchandising"},
    "ai_tools": {"year": 2020, "name": "KI-Tools"},
    "streaming_platform": {"year": 2005, "name": "Streaming-Plattform"},
    "creator_sponsorship": {"year": 2010, "name": "Content Creators Sponsern"},
    "acquisition": {"year": 2000, "office_level": 3, "name": "Studio-Akquise"},
    "soundcon": {"year": 1995, "name": "SoundCon Messe"},
    "soundtrack_label": {"year": 1985, "name": "Soundtrack-Label"},
    "subscription_vault": {"year": 1995, "name": "Abo-Modell"},
    "live_services": {"year": 2012, "name": "Live-Services (Lootboxen)"},
    "publishing_label": {"year": 2005, "name": "Publishing Label (Indie-Fund)"},
    "crypto_scam": {"year": 2019, "name": "Web3 & Blockchain-Games"}
}
