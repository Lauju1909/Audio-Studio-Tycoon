import re
import json

TRANS_PATH = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'

def repair():
    with open(TRANS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix mangled UTF-8 characters (the ones we found in check_bytes_all.py)
    # The bytes c3 b0 c5 b8 c2 8f e2 80 a0 decode as "ðŸ †" in UTF-8
    content = content.replace('ðŸ †', '🏆')
    
    # 2. Fix other common mangled chars (just in case they exist elsewhere)
    replacements = {
        'Ã¤': 'ä',
        'Ã¶': 'ö',
        'Ã¼': 'ü',
        'ÃŸ': 'ß',
        'Ã„': 'Ä',
        'Ã–': 'Ö',
        'Ãœ': 'Ü',
        'Ã©': 'é',
    }
    for old, new in replacements.items():
        content = content.replace(old, new)

    # 3. Replace 'ae', 'oe', 'ue' in German block
    # We'll only do this for the German block to avoid breaking English.
    # The German block starts at '"de": {'
    de_start = content.find('"de": {')
    if de_start != -1:
        de_block = content[de_start:]
        
        # Mapping for common words to be safer
        # or just regex for common patterns
        
        # Fix 'ue' -> 'ü'
        de_block = re.sub(r'([Uu])eber', r'\1ber', de_block) # Ueber -> Über
        de_block = de_block.replace('moeglich', 'möglich')
        de_block = de_block.replace('laeuft', 'läuft')
        de_block = de_block.replace('veroeffentlichen', 'veröffentlichen')
        de_block = de_block.replace('zerstoert', 'zerstört')
        de_block = de_block.replace('Ueberstunden', 'Überstunden')
        de_block = de_block.replace('Schluessel', 'Schlüssel')
        de_block = de_block.replace('hinzufuegen', 'hinzufügen')
        de_block = de_block.replace('fuer', 'für')
        de_block = de_block.replace('Fuer', 'Für')
        de_block = de_block.replace('Bestätigen', 'Bestätigen') # Already correct?
        de_block = de_block.replace('Möchten', 'Möchten')
        de_block = de_block.replace('veröffentlichen', 'veröffentlichen')
        de_block = de_block.replace('Glückwunsch', 'Glückwunsch')
        
        # General replacements for common endings/patterns
        # - "ue" -> "ü" is very common in "müssen", "dürfen", "können" (koennen), etc.
        de_block = de_block.replace('koennen', 'können')
        de_block = de_block.replace('duerfen', 'dürfen')
        de_block = de_block.replace('muessen', 'müssen')
        de_block = de_block.replace('waehrend', 'während')
        de_block = de_block.replace('spaeter', 'später')
        
        # Re-assemble
        content = content[:de_start] + de_block

    # 4. Update get_text logic
    # We'll use a regex to replace the function body
    get_text_pattern = re.compile(r'def get_text\(text_key, \*\*kwargs\):.*?(?=def|\Z)', re.DOTALL)
    new_get_text = """def get_text(text_key, **kwargs):
    \"\"\"
    Retrieves the translated text for a given key.
    Prioritizes: Current Lang -> English -> German -> Key.
    Also supports dynamic translation for missing keys in other languages.
    \"\"\"
    if text_key is None:
        return ""
        
    # 1. Try current language static translation
    text = TRANSLATIONS.get(CURRENT_LANGUAGE, {}).get(text_key)
    
    # 2. If not found and not in English, try English static translation
    if text is None and CURRENT_LANGUAGE != "en":
        text = TRANSLATIONS.get("en", {}).get(text_key)
        
    # 3. If still not found and not in German, try German static translation
    if text is None and CURRENT_LANGUAGE != "de":
        text = TRANSLATIONS.get("de", {}).get(text_key)
        
    # 4. If still not found, use the key itself as a base
    if text is None:
        text = text_key
        # Optional: trigger background translation if it's a new language
        if CURRENT_LANGUAGE not in ["en", "de"]:
            cache_key = f"{CURRENT_LANGUAGE}_{text_key}"
            with CACHE_LOCK:
                if cache_key not in _TRANSLATION_CACHE:
                    global PENDING_TRANSLATIONS
                    if PENDING_TRANSLATIONS < 50:
                        PENDING_TRANSLATIONS += 1
                        threading.Thread(
                            target=background_translate, 
                            args=(text_key, CURRENT_LANGUAGE, cache_key),
                            daemon=True
                        ).start()
            
            # Try to return cached translation if available
            with CACHE_LOCK:
                cached = _TRANSLATION_CACHE.get(cache_key)
                if cached:
                    text = cached

    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
            
    return text
"""
    content = get_text_pattern.sub(new_get_text, content)

    with open(TRANS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Repair complete.")

if __name__ == "__main__":
    repair()
