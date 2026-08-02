import re

filepath = 'translations.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

de_str = '''    "sender_darknet": "Unbekannter Kontakt",
    "subject_warfare_result": "Mission abgeschlossen",
    "warfare_rival_not_found": "Fehler: Das Ziel {name} konnte nicht gefunden werden.",
    "warfare_no_project": "Kein Projekt in Planung",
    "warfare_espionage_success": "Spionage erfolgreich! {name} plant als Nächstes: {details}.",
    "warfare_espionage_fail": "Spionage aufgeflogen! Ein massives PR-Desaster kostet uns 5000 Fans.",
    "warfare_sabotage_success": "Sabotage erfolgreich! Der Release von {name} verzögert sich um {delay} Wochen.",
    "warfare_sabotage_fail": "Sabotage aufgeflogen! Wir wurden verklagt und müssen 250.000$ Strafe zahlen.",
    "warfare_takeover_success": "Übernahme erfolgreich! {name} ist nun unser Tochterunternehmen.",
    "warfare_takeover_fail": "Übernahme gescheitert. Unser Angebot von {bid}$ war zu niedrig (Erwartet: ca. {expected}$).",
    "menu_darknet_title": "Darknet-Terminal (Corporate Warfare)",
    "menu_darknet_espionage": "1. Industriespionage starten (50.000$)",
    "menu_darknet_sabotage": "2. Server-Sabotage beauftragen (150.000$)",
    "menu_darknet_takeover": "3. Feindliche Übernahme einleiten",
    "menu_darknet_back": "Esc/Backspace: Terminal schließen",
    "warfare_select_target": "Ziel auswählen (Pfeiltasten, Enter = Bestätigen):",
    "warfare_input_bid": "Gebot für Übernahme eingeben (Zahlen):",
'''

en_str = '''    "sender_darknet": "Unknown Contact",
    "subject_warfare_result": "Mission Completed",
    "warfare_rival_not_found": "Error: Target {name} could not be found.",
    "warfare_no_project": "No planned project",
    "warfare_espionage_success": "Espionage successful! {name} is planning: {details}.",
    "warfare_espionage_fail": "Espionage exposed! A massive PR disaster costs us 5000 fans.",
    "warfare_sabotage_success": "Sabotage successful! The release of {name} is delayed by {delay} weeks.",
    "warfare_sabotage_fail": "Sabotage exposed! We were sued and must pay $250,000 in damages.",
    "warfare_takeover_success": "Takeover successful! {name} is now our subsidiary.",
    "warfare_takeover_fail": "Takeover failed. Our bid of ${bid} was too low (Expected: ~${expected}).",
    "menu_darknet_title": "Darknet Terminal (Corporate Warfare)",
    "menu_darknet_espionage": "1. Start Industrial Espionage ($50,000)",
    "menu_darknet_sabotage": "2. Order Server Sabotage ($150,000)",
    "menu_darknet_takeover": "3. Initiate Hostile Takeover",
    "menu_darknet_back": "Esc/Backspace: Close Terminal",
    "warfare_select_target": "Select Target (Arrow keys, Enter = Confirm):",
    "warfare_input_bid": "Enter Takeover Bid (Numbers):",
'''

content = re.sub(r"('de':\s*\{)", r"\1\n" + de_str, content)
content = re.sub(r"('en':\s*\{)", r"\1\n" + en_str, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Translations updated.')
