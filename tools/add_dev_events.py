insert_after = 729  # nach der schliessenden ] der AAA_DEV_EVENTS

new_content = '''
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
]

'''

with open("game_data.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Nach Zeile 729 einfuegen
lines.insert(729, new_content)

with open("game_data.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Done. Neue Zeilen:", len(lines))
