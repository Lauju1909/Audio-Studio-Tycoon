import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import translations

missing_de = {
    "decline_poach": "Abwerbung ablehnen",
    "online_error": "Online Fehler",
    "volume_sfx": "SFX Lautstärke",
    "expo_finished": "Messe beendet",
    "email_deleted": "E-Mail gelöscht",
    "menu_numbering": "Menü-Nummerierung",
    "online_connected": "Online Verbunden",
    "tts_auto": "TTS Automatisch",
    "event_": "Event ",
    "attend_expo": "Messe besuchen",
    "accept_counter_offer": "Gegenangebot annehmen",
    "no_active_games": "Keine aktiven Spiele",
    "multiplayer_menu_title": "Multiplayer",
    "lang_de": "Deutsch",
    "volume_speech": "Sprach-Lautstärke",
    "volume_music": "Musik-Lautstärke",
    "percent_label": "Prozent",
    "active_games_menu_title": "Aktive Spiele"
}

missing_en = {
    "decline_poach": "Decline Poach",
    "online_error": "Online Error",
    "volume_sfx": "SFX Volume",
    "expo_finished": "Expo Finished",
    "email_deleted": "Email Deleted",
    "menu_numbering": "Menu Numbering",
    "online_connected": "Online Connected",
    "tts_auto": "TTS Auto",
    "event_": "Event ",
    "attend_expo": "Attend Expo",
    "accept_counter_offer": "Accept Counter Offer",
    "no_active_games": "No active games",
    "multiplayer_menu_title": "Multiplayer",
    "lang_de": "German",
    "volume_speech": "Speech Volume",
    "volume_music": "Music Volume",
    "percent_label": "Percent",
    "active_games_menu_title": "Active Games"
}

# Load the file as text and patch the dictionary
def patch():
    existing_de = translations.TRANSLATIONS["de"]
    existing_en = translations.TRANSLATIONS["en"]
    
    # Remove bad ones if they exist
    bad_keys = ["acquisition_menu_title", "aaa_event_title", "body_co_dev"]
    
    for k, v in missing_de.items():
        existing_de[k] = v
    for k, v in missing_en.items():
        existing_en[k] = v
        
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
        
        my_dict = existing_de if lang == "de" else existing_en
        # Also clean up any obvious bad fallbacks like "Title" in DE
        clean_dict = {}
        for k, v in my_dict.items():
            if lang == "de" and v == k.replace("_", " ").title():
                pass # This is a garbage fallback, skip it
            else:
                clean_dict[k] = v
                
        sorted_keys = sorted(list(clean_dict.keys()))
        for key in sorted_keys:
            val = clean_dict[key].replace('"', '\\"')
            out_lines.append(f'        "{key}": "{val}",\n')
        out_lines[-1] = out_lines[-1].rstrip(',\n') + '\n' # Remove last comma
        out_lines.append('    },\n')
    out_lines[-1] = out_lines[-1].rstrip(',\n') + '\n'
    out_lines.append('}\n')
    
    with open("translations.py", "w", encoding="utf-8") as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    patch()
