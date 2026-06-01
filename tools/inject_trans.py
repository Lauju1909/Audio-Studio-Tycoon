import os

new_keys_de = """
    "menu_add_mtx": "Mikrotransaktionen/Lootboxen integrieren",
    "mtx_added_success": "Lootboxen in {game} integriert! Erwarte einen Backlash der Community...",
    "mtx_email_sender": "Community Manager",
    "mtx_email_subject": "Shitstorm wegen Lootboxen",
    "mtx_email_body": "Boss, die Spieler hassen die neuen Lootboxen in {game}. Wir haben {fans} Fans verloren!",
"""

new_keys_en = """
    "menu_add_mtx": "Integrate Microtransactions/Lootboxes",
    "mtx_added_success": "Lootboxes integrated into {game}! Expect community backlash...",
    "mtx_email_sender": "Community Manager",
    "mtx_email_subject": "Shitstorm incoming!",
    "mtx_email_body": "Boss, players hate the new lootboxes in {game}. We lost {fans} fans!",
"""

with open('translations.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Insert into DE
text = text.replace('"de": {', '"de": {' + new_keys_de)
text = text.replace('"en": {', '"en": {' + new_keys_en)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Translations injected.")
