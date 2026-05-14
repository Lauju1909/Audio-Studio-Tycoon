import os
import sys
import json
import urllib.request
import urllib.parse
import re
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import translations

# --- CONFIGURATION ---
TARGET_LANGUAGES = ['en'] # The user can add 'es', 'fr', 'it', etc.
TRANSLATIONS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'translations.py')
# ---------------------

def translate_text(text, target_lang, source_lang='de'):
    """Translates a text using the free Google Translate API."""
    if not text.strip():
        return text
        
    # Protect placeholders: {name} -> __NAME__
    placeholders = {}
    
    def replacer(match):
        ph = match.group(1)
        token = f"__PH_{len(placeholders)}__"
        placeholders[token] = ph
        return token
        
    protected_text = re.sub(r'\{([^}]+)\}', replacer, text)
    
    encoded_text = urllib.parse.quote(protected_text)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_text}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            translated = "".join([sentence[0] for sentence in result[0]])
            
            # Restore placeholders
            for token, ph in placeholders.items():
                token_pattern = re.compile(token.replace('_', r'_?\s*'))
                translated = token_pattern.sub(f"{{{ph}}}", translated)
                
            return translated
    except Exception as e:
        print(f"Fehler bei der Übersetzung von '{text}': {e}")
        return text

def run():
    print("Starte automatisches Übersetzungssystem für Audio Studio Tycoon...")
    
    source_dict = translations.TRANSLATIONS.get('de', {})
    if not source_dict:
        print("Keine deutschen Übersetzungen gefunden!")
        return

    all_translations = {'de': source_dict}
    
    for lang in TARGET_LANGUAGES:
        print(f"\nVerarbeite Sprache: {lang}")
        lang_dict = translations.TRANSLATIONS.get(lang, {})
                
        updated = False
        for key, text in source_dict.items():
            if key not in lang_dict:
                print(f"  Übersetze '{key}' -> {lang}...")
                translated = translate_text(text, lang)
                lang_dict[key] = translated
                updated = True
                time.sleep(0.5) # Kurze Pause, um API-Rate-Limits zu vermeiden
                
        all_translations[lang] = lang_dict
        if updated:
            print(f"  Sprache {lang} aktualisiert.")
        else:
            print("  Alles auf dem neuesten Stand.")

    print("\nGeneriere translations.py...")
    
    out_lines = []
    out_lines.append('"""\nTranslations for Audio Studio Tycoon.\nSupports German (de) and other automatically translated languages.\n"""\n')
    out_lines.append('import sys\n\n')
    out_lines.append('def get_system_language():\n    try:\n        if sys.platform == "win32":\n            import ctypes\n            windll = ctypes.windll.kernel32\n            lang_id = windll.GetUserDefaultUILanguage()\n            primary_lang = lang_id & 0x3ff\n            if primary_lang == 0x07:\n                return "de"\n        return "en"\n    except Exception:\n        return "en"\n\n')
    out_lines.append('CURRENT_LANGUAGE = get_system_language()\n\n')
    out_lines.append('def set_language(lang):\n    global CURRENT_LANGUAGE\n    CURRENT_LANGUAGE = lang\n\n')
    out_lines.append('def get_text(text_key, **kwargs):\n    text = TRANSLATIONS.get(CURRENT_LANGUAGE, TRANSLATIONS["en"]).get(text_key, text_key)\n    if kwargs:\n        try:\n            return text.format(**kwargs)\n        except Exception:\n            return text\n    return text\n\n')
    
    out_lines.append('TRANSLATIONS = {\n')
    for lang, lang_dict in all_translations.items():
        out_lines.append(f'    "{lang}": {{\n')
        sorted_keys = sorted(list(lang_dict.keys()))
        for key in sorted_keys:
            val = str(lang_dict[key]).replace('"', '\\"').replace('\n', '\\n')
            out_lines.append(f'        "{key}": "{val}",\n')
        # Remove trailing comma for the last entry in the dictionary
        if sorted_keys:
            out_lines[-1] = out_lines[-1].rstrip(',\n') + '\n'
        out_lines.append('    },\n')
    out_lines[-1] = out_lines[-1].rstrip(',\n') + '\n'
    out_lines.append('}\n')
    
    with open(TRANSLATIONS_FILE, "w", encoding="utf-8") as f:
        f.writelines(out_lines)
        
    print("Vorgang abgeschlossen! Die Datei translations.py wurde aktualisiert.")

if __name__ == "__main__":
    run()
