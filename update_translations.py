import codecs

def update():
    with codecs.open('translations.py', 'r', 'utf-8') as f:
        content = f.read()

    en_adds = '''
        "upgrade_qa_lab": "Upgrade QA Lab to level {level} ({cost} EUR)",
        "upgrade_support": "Upgrade Support Department to level {level} ({cost} EUR)",
        "buy_servers": "Buy 50000 server capacity (Current: {capacity}) ({cost} EUR)",
        "qa_lab_upgraded": "QA Lab upgraded to level {level}!",
        "support_upgraded": "Support Department upgraded to level {level}!",
        "servers_bought": "Server capacity increased to {capacity}!",
'''

    de_adds = '''
        "upgrade_qa_lab": "QA-Labor auf Level {level} aufrüsten ({cost} EUR)",
        "upgrade_support": "Support-Abteilung auf Level {level} aufrüsten ({cost} EUR)",
        "buy_servers": "50000 Server-Kapazität kaufen (Aktuell: {capacity}) ({cost} EUR)",
        "qa_lab_upgraded": "QA-Labor auf Level {level} aufgerüstet!",
        "support_upgraded": "Support-Abteilung auf Level {level} aufgerüstet!",
        "servers_bought": "Server-Kapazität auf {capacity} erhöht!",
'''

    content = content.replace('"en": {', '"en": {' + en_adds)
    content = content.replace('"de": {', '"de": {' + de_adds)

    with codecs.open('translations.py', 'w', 'utf-8') as f:
        f.write(content)

    print("Updated translations.py")

if __name__ == "__main__":
    update()
