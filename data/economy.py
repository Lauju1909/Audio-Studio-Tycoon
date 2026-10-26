"""Trends, Publisher, Mail- und Review-Templates."""
from data.core import *  # noqa: F401,F403
from data.content import *  # noqa: F401,F403
from data.people import *  # noqa: F401,F403
from data.studio import *  # noqa: F401,F403

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
