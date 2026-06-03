import codecs

lines = []
with codecs.open('translations.py', 'r', 'utf-8') as f:
    lines = f.readlines()

de_lines = []
en_lines = []

de_dict = {
    'ipo_title': 'Börsengang (IPO)',
    'ipo_confirm': 'An die Börse gehen (Erlös: {payout} EUR)',
    'ipo_success': 'Der Börsengang war ein voller Erfolg! Wir sind nun eine Aktiengesellschaft.',
    'ipo_option': 'Börsengang (IPO) planen',
    'shareholder_title': 'Jahreshauptversammlung',
    'shareholder_happy': 'Aktionäre sind glücklich! Umsatzziele erreicht. (+10 Vertrauen)',
    'shareholder_angry': 'Aktionäre sind unzufrieden! Ziele verfehlt. (-25 Vertrauen)',
    'shareholder_fired': 'Du wurdest als CEO vom Aufsichtsrat entlassen! GAME OVER.',
    'shareholder_trust_msg': 'Das Vertrauen der Aktionäre liegt bei {trust}%.'
}

en_dict = {
    'ipo_title': 'Initial Public Offering (IPO)',
    'ipo_confirm': 'Go Public (Payout: {payout} EUR)',
    'ipo_success': 'The IPO was a massive success! We are now a public company.',
    'ipo_option': 'Plan Initial Public Offering (IPO)',
    'shareholder_title': 'Annual Shareholder Meeting',
    'shareholder_happy': 'Shareholders are happy! Revenue targets met. (+10 Trust)',
    'shareholder_angry': 'Shareholders are furious! Targets missed. (-25 Trust)',
    'shareholder_fired': 'You have been fired by the board of directors! GAME OVER.',
    'shareholder_trust_msg': 'Shareholder trust is currently at {trust}%.'
}

for k, v in de_dict.items():
    de_lines.append(f'        "{k}": "{v}",\n')
for k, v in en_dict.items():
    en_lines.append(f'        "{k}": "{v}",\n')

# find en start
en_idx = -1
for i, line in enumerate(lines):
    if '"en": {' in line:
        en_idx = i
        break
lines = lines[:en_idx+1] + en_lines + lines[en_idx+1:]

# find de start
de_idx = -1
for i, line in enumerate(lines):
    if '"de": {' in line:
        de_idx = i
        break
lines = lines[:de_idx+1] + de_lines + lines[de_idx+1:]

with codecs.open('translations.py', 'w', 'utf-8') as f:
    f.writelines(lines)
