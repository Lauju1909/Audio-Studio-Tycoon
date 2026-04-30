import json
import os

with open('translations.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_keys_de = {
    'sender_historian': 'Historiker',
    'subject_pioneer_times': 'Willkommen in der Pionierzeit!',
    'body_pioneer_times': 'Das Jahr ist 1930. Du bist ein Visionär mit einer großen Idee: Man kann Maschinen beibringen, Spiele zu spielen und zu entwickeln! Mit bescheidenen Mitteln in einer Garage beginnst du dein Studio. Du bist selbst der Chefentwickler und programmierst die ersten Spiele allein. Später kannst du Personal einstellen, um größere Projekte zu stemmen! Verfügbare Themen: Abakus, Mathematik, Schach und Logistik.',
    'difficulty_easy': 'Einfach',
    'difficulty_easy_desc': 'Mehr Startgeld, schwächere Rivalen, großzügigere Reviews.',
    'difficulty_normal_desc': 'Die Standard-Erfahrung.',
    'difficulty_hard_desc': 'Weniger Startgeld, stärkere Rivalen, strengere Reviews.',
    'difficulty_legendary_desc': 'Extrem wenig Geld, übermächtige Rivalen, gnadenlose Reviews.',
    'game_name_title': 'Spieltitel eingeben'
}

new_keys_en = {
    'sender_historian': 'Historian',
    'subject_pioneer_times': 'Welcome to the Pioneer Times!',
    'body_pioneer_times': 'The year is 1930. You are a visionary with a big idea: you can teach machines to play and develop games! With modest means in a garage, you start your studio. You are the lead developer and program the first games alone. Later you can hire staff to handle larger projects! Available topics: Abacus, Mathematics, Chess, and Logistics.',
    'difficulty_easy': 'Easy',
    'difficulty_easy_desc': 'More starting money, weaker rivals, more generous reviews.',
    'difficulty_normal_desc': 'The standard experience.',
    'difficulty_hard_desc': 'Less starting money, stronger rivals, stricter reviews.',
    'difficulty_legendary_desc': 'Extremely little money, overpowered rivals, merciless reviews.',
    'game_name_title': 'Enter Game Title'
}

de_start = -1
en_start = -1
for i, line in enumerate(lines):
    if '"de": {' in line: de_start = i
    if '"en": {' in line: en_start = i

if de_start != -1 and en_start != -1:
    for k, v in reversed(list(new_keys_de.items())):
        lines.insert(de_start + 1, f'        "{k}": "{v}",\n')
        en_start += 1
    for k, v in reversed(list(new_keys_en.items())):
        lines.insert(en_start + 1, f'        "{k}": "{v}",\n')

with open('translations.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
