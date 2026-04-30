import os
import sys
import json
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import translations

def translate_key(key, lang="de"):
    # Basic dictionary for common terms
    dict_de = {
        "menu_new_game": "Neues Spiel",
        "menu_load_game": "Spiel laden",
        "menu_settings": "Einstellungen",
        "menu_help": "Hilfe",
        "menu_quit": "Spiel verlassen",
        "menu_mod_portal": "Mod Portal",
        "main_title": "Hauptmenü",
        "game_menu": "Entwicklerbüro",
        "menu_develop_game": "Neues Spiel entwickeln",
        "menu_co_dev_start": "Co-Entwicklung starten",
        "hr_menu": "Personalverwaltung",
        "research_menu": "Forschungszentrum",
        "office_menu": "Büroausstattung",
        "email_inbox_status": "Posteingang",
        "bank_menu": "Bank & Finanzen",
        "service_menu": "Services & Abos",
        "active_games_menu_title": "Aktive Spiele & Einnahmen",
        "save_menu": "Spiel speichern",
        "settings_menu": "Einstellungen",
        "difficulty_menu": "Schwierigkeitsgrad wählen",
        "company_name_title": "Firmenname eingeben",
        "volume_settings": "Lautstärke-Einstellungen",
        "auto_update_toggle": "Auto-Update umschalten",
        "check_update": "Nach Updates suchen",
        "keybindings_menu": "Tastenbelegung",
        "hire_employee": "Mitarbeiter einstellen",
        "fire_employee": "Mitarbeiter entlassen",
        "training_employee": "Mitarbeiter schulen",
        "menu_teambuilding": "Teambuilding-Event",
        "teambuilding_pizza": "Pizza bestellen",
        "teambuilding_party": "Büro-Party veranstalten",
        "teambuilding_trip": "Betriebsausflug",
        "loan_menu": "Kredit aufnehmen",
        "loan_50k": "50.000€ Kredit aufnehmen",
        "loan_100k": "100.000€ Kredit aufnehmen",
        "delete_email": "E-Mail löschen",
        "research_topic": "Neues Thema erforschen",
        "research_genre": "Neues Genre erforschen",
        "research_audience": "Neue Zielgruppe erforschen",
        "research_feature": "Neues Feature erforschen",
        "research_technology": "Neue Technologie erforschen",
        "create_engine": "Eigene Engine entwickeln",
        "hardware_dev": "Hardware entwickeln",
        "create_engine_title": "Engine benennen",
        "engine_feature_select": "Engine-Features auswählen",
        "service_manage_subscription": "Abo verwalten",
        "game_service_options": "Service-Optionen",
        "subscription_menu_title": "Abonnement-Zentrum",
        "subscription_start": "Abo starten",
        "subscription_price_up": "Abo-Preis erhöhen",
        "subscription_price_down": "Abo-Preis senken",
        "topic_menu": "Thema wählen",
        "genre_menu": "Genre wählen",
        "platform_menu": "Plattform wählen",
        "audience_menu": "Zielgruppe wählen",
        "game_size_menu": "Spielgröße wählen",
        "engine_select_menu": "Engine wählen",
        "marketing_menu": "Marketing-Kampagne starten",
        "marketing_none": "Kein Marketing",
        "marketing_small": "Kleine Kampagne",
        "marketing_medium": "Mittlere Kampagne",
        "marketing_large": "Große Kampagne",
        "game_name_title": "Spiel benennen",
        "dev_sliders_title": "Entwicklungs-Fokus",
        "dev_progress_menu": "Entwicklung...",
        "finish_game": "Spiel veröffentlichen",
        "menu_co_dev_partner_title": "Co-Dev Partner wählen",
        "co_dev_partner_option": "Partner auswählen",
        "no_active_games": "Keine aktiven Spiele",
        "multiplayer_join_room": "Raum beitreten"
    }
    
    dict_en = {
        "menu_new_game": "New Game",
        "menu_load_game": "Load Game",
        "menu_settings": "Settings",
        "menu_help": "Help",
        "menu_quit": "Quit Game",
        "menu_mod_portal": "Mod Portal",
        "main_title": "Main Menu",
        "game_menu": "Developer Office",
        "menu_develop_game": "Develop New Game",
        "menu_co_dev_start": "Start Co-Development",
        "hr_menu": "Human Resources",
        "research_menu": "Research Center",
        "office_menu": "Office Equipment",
        "email_inbox_status": "Inbox",
        "bank_menu": "Bank & Finances",
        "service_menu": "Services & Subs",
        "active_games_menu_title": "Active Games & Revenue",
        "save_menu": "Save Game",
        "settings_menu": "Settings",
        "difficulty_menu": "Select Difficulty",
        "company_name_title": "Enter Company Name",
        "volume_settings": "Volume Settings",
        "auto_update_toggle": "Toggle Auto-Update",
        "check_update": "Check for Updates",
        "keybindings_menu": "Keybindings",
        "hire_employee": "Hire Employee",
        "fire_employee": "Fire Employee",
        "training_employee": "Train Employee",
        "menu_teambuilding": "Teambuilding Event",
        "teambuilding_pizza": "Order Pizza",
        "teambuilding_party": "Host Office Party",
        "teambuilding_trip": "Company Trip",
        "loan_menu": "Take Loan",
        "loan_50k": "Take 50,000 Loan",
        "loan_100k": "Take 100,000 Loan",
        "delete_email": "Delete Email",
        "research_topic": "Research New Topic",
        "research_genre": "Research New Genre",
        "research_audience": "Research New Audience",
        "research_feature": "Research New Feature",
        "research_technology": "Research New Technology",
        "create_engine": "Create Custom Engine",
        "hardware_dev": "Develop Hardware",
        "create_engine_title": "Name Engine",
        "engine_feature_select": "Select Engine Features",
        "service_manage_subscription": "Manage Subscription",
        "game_service_options": "Service Options",
        "subscription_menu_title": "Subscription Center",
        "subscription_start": "Start Subscription",
        "subscription_price_up": "Increase Sub Price",
        "subscription_price_down": "Decrease Sub Price",
        "topic_menu": "Select Topic",
        "genre_menu": "Select Genre",
        "platform_menu": "Select Platform",
        "audience_menu": "Select Audience",
        "game_size_menu": "Select Game Size",
        "engine_select_menu": "Select Engine",
        "marketing_menu": "Start Marketing Campaign",
        "marketing_none": "No Marketing",
        "marketing_small": "Small Campaign",
        "marketing_medium": "Medium Campaign",
        "marketing_large": "Large Campaign",
        "game_name_title": "Name Game",
        "dev_sliders_title": "Development Focus",
        "dev_progress_menu": "Developing...",
        "finish_game": "Publish Game",
        "menu_co_dev_partner_title": "Select Co-Dev Partner",
        "co_dev_partner_option": "Select Partner",
        "no_active_games": "No active games",
        "multiplayer_join_room": "Join Room"
    }
    
    if lang == "de":
        if key in dict_de: return dict_de[key]
    else:
        if key in dict_en: return dict_en[key]
        
    # Fallback Generation
    pretty = key.replace("_", " ").title()
    if lang == "de" and "Menu" in pretty: pretty = pretty.replace("Menu", "Menü")
    return pretty

def run():
    import glob
    files = glob.glob("*.py") + glob.glob("menus/*.py")
    
    keys_found = set()
    pattern = re.compile(r"get_text\(['\"]([^'\"]+)['\"]")
    
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
            for match in pattern.findall(content):
                keys_found.add(match)
                
    existing_en = translations.TRANSLATIONS.get("en", {})
    existing_de = translations.TRANSLATIONS.get("de", {})
    
    for key in keys_found:
        if key not in existing_de:
            existing_de[key] = translate_key(key, "de")
        if key not in existing_en:
            existing_en[key] = translate_key(key, "en")
            
    translations.TRANSLATIONS["de"] = existing_de
    translations.TRANSLATIONS["en"] = existing_en
    
    out_lines = []
    out_lines.append('"""\nTranslations for Audio Studio Tycoon.\nSupports German (de) and English (en).\n"""\n')
    out_lines.append('import sys\n\n')
    out_lines.append('def get_system_language():\n    try:\n        if sys.platform == "win32":\n            import ctypes\n            windll = ctypes.windll.kernel32\n            lang_id = windll.GetUserDefaultUILanguage()\n            primary_lang = lang_id & 0x3ff\n            if primary_lang == 0x07:\n                return "de"\n        return "en"\n    except Exception:\n        return "en"\n\n')
    out_lines.append('CURRENT_LANGUAGE = get_system_language()\n\n')
    out_lines.append('def set_language(lang):\n    global CURRENT_LANGUAGE\n    CURRENT_LANGUAGE = lang\n\n')
    out_lines.append('def get_text(key, **kwargs):\n    text = TRANSLATIONS.get(CURRENT_LANGUAGE, TRANSLATIONS["en"]).get(key, key)\n    if kwargs:\n        try:\n            return text.format(**kwargs)\n        except Exception:\n            return text\n    return text\n\n')
    
    out_lines.append('TRANSLATIONS = {\n')
    for lang in ["de", "en"]:
        out_lines.append(f'    "{lang}": {{\n')
        # Sort keys
        sorted_keys = sorted(list(translations.TRANSLATIONS[lang].keys()))
        for key in sorted_keys:
            val = translations.TRANSLATIONS[lang][key].replace('"', '\\"')
            out_lines.append(f'        "{key}": "{val}",\n')
        out_lines[-1] = out_lines[-1].rstrip(',\n') + '\n' # Remove last comma
        out_lines.append('    },\n')
    out_lines[-1] = out_lines[-1].rstrip(',\n') + '\n'
    out_lines.append('}\n')
    
    with open("translations.py", "w", encoding="utf-8") as f:
        f.writelines(out_lines)
        
    print(f"Updated translations.py! Found and added missing keys.")

if __name__ == "__main__":
    run()
