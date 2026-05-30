# -*- coding: utf-8 -*-
import re

with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_de = '''
    "office_perks_menu": "Büro-Perks",
    "perk_fruit_basket": "Obstkorb (Stress sinkt leicht)",
    "perk_kicker_table": "Tischkicker (Stress sinkt mittel)",
    "perk_company_car": "Firmenwagen (Stress sinkt stark)",
    "perk_removed_subj": "Perk gestrichen",
    "perk_removed_body": "Das Perk {perk} wurde gestrichen. Die Mitarbeiter sind etwas enttäuscht.",
    "headhunting_title": "Headhunting-Angriff!",
    "headhunting_desc": "{name} hat ein Angebot eines Konkurrenten über  pro Monat erhalten. Wollen Sie mitgehen?",
    "match_offer": "Angebot mitgehen ()",
    "let_them_go": "Gehen lassen",
    "sender_union": "Gewerkschaft",
    "subject_strike": "STREIK!",
    "body_strike": "Aufgrund von zu hohem Stress streikt die Belegschaft für {weeks} Wochen! Ausfallkosten: .",
    "subject_strike_ended": "Streik beendet",
    "body_strike_ended": "Die Mitarbeiter nehmen die Arbeit wieder auf. Achten Sie auf weniger Crunchtime!",
'''

new_en = '''
    "office_perks_menu": "Office Perks",
    "perk_fruit_basket": "Fruit Basket (Slight stress reduction)",
    "perk_kicker_table": "Kicker Table (Medium stress reduction)",
    "perk_company_car": "Company Car (High stress reduction)",
    "perk_removed_subj": "Perk Removed",
    "perk_removed_body": "The perk {perk} was removed. Employees are a bit disappointed.",
    "headhunting_title": "Headhunting Alert!",
    "headhunting_desc": "{name} got an offer from a rival for /month. Do you want to match it?",
    "match_offer": "Match Offer ()",
    "let_them_go": "Let Them Go",
    "sender_union": "Labor Union",
    "subject_strike": "STRIKE!",
    "body_strike": "Due to high stress, the staff is on strike for {weeks} weeks! Cost: .",
    "subject_strike_ended": "Strike Ended",
    "body_strike_ended": "The employees are back to work. Try to avoid excessive crunch!",
'''

de_target = '"de": {'
content = content.replace(de_target, de_target + new_de)

en_target = '"en": {'
content = content.replace(en_target, en_target + new_en)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('translations.py updated')
