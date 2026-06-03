import codecs

lines = []
with codecs.open('translations.py', 'r', 'utf-8') as f:
    lines = f.readlines()

de_lines = []
en_lines = []

de_dict = {
    'cf_choice_title': 'Entwicklung starten oder Crowdfunding Kampagne?',
    'cf_normal_dev': 'Normale Entwicklung starten',
    'cf_start_campaign': 'SoundStarter Kampagne ({target} EUR)',
    'cf_success': 'SoundStarter Kampagne erfolgreich! {amount} EUR gesammelt!',
    'cf_failed': 'SoundStarter Kampagne gescheitert! Wir haben nicht genug Fans oder Hype.',
    'sender_angry_backers': 'Wütende Backer',
    'subject_cf_fail': 'Wo ist unser Spiel?!',
    'body_cf_fail': 'Wir haben {name} vor über einem Jahr unterstützt und es ist immer noch nicht fertig! Betrug!'
}

en_dict = {
    'cf_choice_title': 'Start Development or Crowdfunding Campaign?',
    'cf_normal_dev': 'Start Normal Development',
    'cf_start_campaign': 'SoundStarter Campaign ({target} EUR)',
    'cf_success': 'SoundStarter Campaign successful! {amount} EUR collected!',
    'cf_failed': 'SoundStarter Campaign failed! We do not have enough fans or hype.',
    'sender_angry_backers': 'Angry Backers',
    'subject_cf_fail': 'Where is our game?!',
    'body_cf_fail': 'We backed {name} over a year ago and it is still not finished! Scam!'
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
