import sys

with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

# English
en_old = '''        "activate_mod_support": "Add Mod Support (10,000 EUR)",
        "has_mod_support_active": "Mod Support: Active",
        "activate_ads": "Activate In-Game Ads",
        "has_ads_active": "In-Game Ads: Active",'''

en_new = '''        "activate_mod_support": "Add Mod Support (10,000 EUR)",
        "has_mod_support_active": "Mod Support: Active",
        "activate_ads": "Activate In-Game Ads",
        "has_ads_active": "In-Game Ads: Active",
        "start_patch": "Develop Patch (Fix Bugs)",
        "start_content_update": "Develop Content Update (Free)",
        "start_dlc": "Develop DLC (Paid)",
        "patch_started": "Patch development started.",
        "content_started": "Content update development started.",
        "dlc_started": "DLC development started.",
        "vacation_menu_title": "Send Employee on Vacation",
        "vacation_employee_option": "{name} (Fatigue: {fatigue}%)",
        "vacation_none_available": "No available employees.",
        "vacation_success": "{name} is now on vacation for 4 weeks.",
        "subject_burnout": "Employee Burnout!",
        "body_burnout": "{name} suffered a burnout and will be absent for {weeks} weeks!",'''

content = content.replace(en_old, en_new)

# German
de_old = '''        "activate_mod_support": "Mod-Support hinzufuegen (10.000 EUR)",
        "has_mod_support_active": "Mod-Support: Aktiviert",
        "activate_ads": "In-Game Werbung aktivieren",
        "has_ads_active": "In-Game Werbung: Aktiviert",'''

de_new = '''        "activate_mod_support": "Mod-Support hinzufuegen (10.000 EUR)",
        "has_mod_support_active": "Mod-Support: Aktiviert",
        "activate_ads": "In-Game Werbung aktivieren",
        "has_ads_active": "In-Game Werbung: Aktiviert",
        "start_patch": "Patch entwickeln (Bugs beheben)",
        "start_content_update": "Content-Update entwickeln (Kostenlos)",
        "start_dlc": "DLC entwickeln (Kostenpflichtig)",
        "patch_started": "Patch-Entwicklung gestartet.",
        "content_started": "Content-Update gestartet.",
        "dlc_started": "DLC-Entwicklung gestartet.",
        "vacation_menu_title": "Mitarbeiter in Urlaub schicken",
        "vacation_employee_option": "{name} (Erschoepfung: {fatigue}%)",
        "vacation_none_available": "Keine verfuegbaren Mitarbeiter.",
        "vacation_success": "{name} ist nun fuer 4 Wochen im Urlaub.",
        "subject_burnout": "Mitarbeiter-Burnout!",
        "body_burnout": "{name} hat einen Burnout erlitten und faellt fuer {weeks} Wochen aus!",'''

content = content.replace(de_old, de_new)

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated translations.py")
