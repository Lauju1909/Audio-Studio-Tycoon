import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = "from menus import ("
replace = target + "\n    OfficePerksMenu, HeadhuntingEventMenu,"
content = content.replace(target, replace)

target_dict = '        "hr_menu": lambda: HRMenu(audio, state),'
replace_dict = target_dict + '\n        "office_perks_menu": lambda: OfficePerksMenu(audio, state),\n        "headhunting_event_menu": lambda: HeadhuntingEventMenu(audio, state),'
content = content.replace(target_dict, replace_dict)

target_auto_switch = '''                # GOTY-Ergebnis anzeigen
                if getattr(state, "pending_goty_results", None) and current_key not in ("goty_menu", "dev_progress_menu", "aaa_dev_event_menu"):'''
replace_auto_switch = '''                # Headhunting Event
                if getattr(state, "pending_headhunt_event", None) and current_key != "headhunting_event_menu":
                    current_key = "headhunting_event_menu"
                    current_menu = menu_factories[current_key]()
                    current_menu.announce_entry()

''' + target_auto_switch
content = content.replace(target_auto_switch, replace_auto_switch)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('main.py updated')
