import os

path = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_keys_de = """        "publisher_deals_title": "Publisher-Verträge",
        "publisher_no_deals": "Derzeit keine Publisher-Verträge verfügbar.",
        "publisher_deal_info": "{name} | Vorab: {funding} EUR | Anteil: {share}% | Frist: {deadline} Ww. | Ziel: {quality}%",
"""

new_keys_en = """        "publisher_deals_title": "Publisher Deals",
        "publisher_no_deals": "No publisher deals available at the moment.",
        "publisher_deal_info": "{name} | Upfront: {funding} EUR | Share: {share}% | Deadline: {deadline} w. | Target: {quality}%",
"""

content = content.replace('"tutorial_welcome_8": "Press Enter to close this window.",', '"tutorial_welcome_8": "Press Enter to close this window.",\n' + new_keys_en)

content = content.replace('"streaming_monthly_report_body": "Abonnenten: {subs}\\nEinnahmen: {rev} EUR\\nKosten: {cost} EUR\\nHardware-Boost durch Cross-Promo aktiv!"', '"streaming_monthly_report_body": "Abonnenten: {subs}\\nEinnahmen: {rev} EUR\\nKosten: {cost} EUR\\nHardware-Boost durch Cross-Promo aktiv!",\n' + new_keys_de)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
