import os

new_keys_de = """
    "menu_anti_cheat": "Anti-Cheat System kaufen (100.000 €)",
    "anti_cheat_success": "Anti-Cheat für {game} erfolgreich installiert!",
    "cheater_email_sender": "Community Manager",
    "cheater_email_subject": "Cheater in {game}!",
    "cheater_email_body": "Boss! Eine massive Cheater-Welle ruiniert das Spiel! Wir haben {lost} ehrliche Spieler verloren. Wir brauchen ein Anti-Cheat System!",
"""

new_keys_en = """
    "menu_anti_cheat": "Buy Anti-Cheat System (100,000 €)",
    "anti_cheat_success": "Anti-Cheat for {game} successfully installed!",
    "cheater_email_sender": "Community Manager",
    "cheater_email_subject": "Cheaters in {game}!",
    "cheater_email_body": "Boss! A massive cheater wave is ruining the game! We lost {lost} honest players. We need an Anti-Cheat system!",
"""

with open('translations.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Insert into DE
text = text.replace('"de": {', '"de": {' + new_keys_de)
text = text.replace('"en": {', '"en": {' + new_keys_en)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Translations injected.")
