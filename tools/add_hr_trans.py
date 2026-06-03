import codecs

lines = []
with codecs.open('translations.py', 'r', 'utf-8') as f:
    lines = f.readlines()

de_lines = []
en_lines = []

de_dict = {
    'perk_wellness_benefits': 'Wellness & Gesundheitsprogramm (2000 EUR/Woche)',
    'perk_therapist': 'Betriebstherapeut für Burnout-Prävention (5000 EUR/Woche)',
    'perk_hr_department': 'HR-Abteilung für Personalbetreuung (10000 EUR/Woche)',
    'subject_burnout_quit': 'Kündigung wegen Burnout!',
    'body_burnout_quit': 'Chef, {name} hat einen schweren Burnout durch den ständigen Crunch erlitten und sofort gekündigt. Wir brauchen dringend eine HR-Abteilung oder Therapeuten!'
}

en_dict = {
    'perk_wellness_benefits': 'Wellness & Health Benefits (2000 EUR/week)',
    'perk_therapist': 'Company Therapist for Burnout Prevention (5000 EUR/week)',
    'perk_hr_department': 'HR Department for Employee Care (10000 EUR/week)',
    'subject_burnout_quit': 'Resignation due to Burnout!',
    'body_burnout_quit': 'Boss, {name} suffered a severe burnout from constant crunching and resigned immediately. We urgently need an HR department or therapists!'
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
