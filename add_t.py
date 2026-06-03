import re

with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

en_dict = '''
        "cf_choice_title": "Start Development",
        "cf_normal_dev": "Start Normal Development",
        "cf_start_campaign": "SoundStarter Campaign ({target} EUR)",
        "cf_success": "Campaign successful! Raised {amount} EUR!",
        "cf_failed": "Campaign failed! Not enough hype or fans.",
        "sender_angry_backers": "Angry Backers",
        "subject_cf_fail": "Where is our game?!",
        "body_cf_fail": "We backed {name} a year ago and it is still not finished! Scam!",
'''

de_dict = '''
        "cf_choice_title": "Entwicklung starten",
        "cf_normal_dev": "Normale Entwicklung starten",
        "cf_start_campaign": "SoundStarter Kampagne ({target} EUR)",
        "cf_success": "Kampagne erfolgreich! {amount} EUR gesammelt!",
        "cf_failed": "Kampagne gescheitert! Zu wenig Hype/Fans.",
        "sender_angry_backers": "Wütende Backer",
        "subject_cf_fail": "Wo ist unser Spiel?!",
        "body_cf_fail": "Wir haben {name} vor einem Jahr unterstützt und es ist immer noch nicht fertig! Betrug!",
'''

content = content.replace('"en": {', '"en": {' + en_dict)
content = content.replace('"de": {', '"de": {' + de_dict)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(content)
