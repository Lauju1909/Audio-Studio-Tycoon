import json

file_path = 'translations.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

de_inject = '''        'office_upgrades_menu_title': "Büroausstattung & Upgrades",
        'upgrade_coffee': "Kaffeevollautomat",
        'upgrade_chairs': "Ergonomische Stühle",
        'upgrade_morale_room': "Pausenraum mit Tischkicker",
        'upgrade_intel': "Marktforschungs-Abo",
        'upgrade_security': "Security-Dienst",
        'upgrade_pr': "PR-Agentur Retainer",
        'upgrade_legal': "Anwaltskanzlei Retainer",
        'upgrade_bought': "{name} wurde gekauft und im Büro installiert!",
        'sender_accounting': "Buchhaltung",
        'subject_yearly_report': "Jahresbilanz {year}",
        'body_yearly_report': "Hier ist der Bericht für das vergangene Jahr.\\nEinnahmen: {income} EUR\\nAusgaben: {expenses} EUR\\n------------------\\nGewinn: {profit} EUR\\nWeiter so!",
'''

en_inject = '''        'office_upgrades_menu_title': "Office Upgrades",
        'upgrade_coffee': "Coffee Machine",
        'upgrade_chairs': "Ergonomic Chairs",
        'upgrade_morale_room': "Break Room with Foosball",
        'upgrade_intel': "Market Research Sub",
        'upgrade_security': "Security Service",
        'upgrade_pr': "PR Agency Retainer",
        'upgrade_legal': "Law Firm Retainer",
        'upgrade_bought': "{name} purchased and installed!",
        'sender_accounting': "Accounting",
        'subject_yearly_report': "Annual Report {year}",
        'body_yearly_report': "Here is the report for the past year.\\nIncome: {income} EUR\\nExpenses: {expenses} EUR\\n------------------\\nProfit: {profit} EUR\\nKeep it up!",
'''

content = content.replace(
    "'expo_event_security_safe': \"Die Security hat alles geregelt. Guter Hype-Zuwachs.\",", 
    "'expo_event_security_safe': \"Die Security hat alles geregelt. Guter Hype-Zuwachs.\",\\n" + de_inject
)
content = content.replace(
    "'expo_event_security_safe': \"Security handled everything. Good hype boost.\",", 
    "'expo_event_security_safe': \"Security handled everything. Good hype boost.\",\\n" + en_inject
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
