import sys

# Update translations for Merchandising
with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

merch_translations = '''
    "menu_merchandising": {
        "de": "Merchandising",
        "en": "Merchandising"
    },
    "merch_campaigns": {
        "de": "Aktive Kampagnen",
        "en": "Active Campaigns"
    },
    "merch_type_tshirt": {
        "de": "T-Shirts",
        "en": "T-Shirts"
    },
    "merch_type_figures": {
        "de": "Action-Figuren",
        "en": "Action Figures"
    },
    "merch_type_soundtrack": {
        "de": "Soundtrack CD/Vinyl",
        "en": "Soundtrack CD/Vinyl"
    },
    "start_merch": {
        "de": "Merch-Kampagne starten",
        "en": "Start Merch Campaign"
    },
    "merch_profit": {
        "de": "Profit pro Woche:",
        "en": "Profit per Week:"
    },
'''

if '"menu_merchandising"' not in content:
    content = content.replace('"menu_marketing":', merch_translations + '    "menu_marketing":')
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
