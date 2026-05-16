import json
import os
import re

TRANS_PATH = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'
MISSING_PATH = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\scratch\missing_translations.json'

MANUAL_DE = {
    "production_merge_title": "Produktion & Lagerverwaltung",
    "story_Krankenhaus_desc": "Rette Leben und manage den stressigen Alltag einer Klinik.",
    "Echo-Effekt": "Echo-Effekt",
    "Extremsport": "Extremsport",
    "Fahrsimulation": "Fahrsimulation",
    "Film-Sync": "Film-Synchronisation",
    "Hörbuch-Boom": "Hörbuch-Boom",
    "Hörgeräte-Tech": "Hörgeräte-Technologie",
    "KI-Mastering": "KI-Mastering",
    "Multiroom-Audio": "Multiroom-Audio",
    "Neuro-Interface": "Neuro-Interface",
}

def overhaul():
    print("Starting SAFE translation system overhaul...")
    
    if not os.path.exists(MISSING_PATH):
        print(f"Missing translations file not found at {MISSING_PATH}")
        return

    with open(MISSING_PATH, 'r', encoding='utf-8') as f:
        missing_data = json.load(f)
    
    en_missing_from_de = missing_data.get('en_missing_from_de', {})
    de_missing_from_en = missing_data.get('de_missing_from_en', {})
    
    with open(TRANS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    en_start = -1
    de_start = -1
    for i, line in enumerate(lines):
        if '"en": {' in line: en_start = i
        if '"de": {' in line: de_start = i

    if en_start == -1 or de_start == -1:
        print("Blocks not found. Aborting.")
        return

    def find_block_end(start_idx):
        brace_count = 0
        for i in range(start_idx, len(lines)):
            brace_count += lines[i].count('{')
            brace_count -= lines[i].count('}')
            if brace_count == 0: return i
        return -1

    en_end = find_block_end(en_start)
    de_end = find_block_end(de_start)
    
    # Existing keys
    existing_de_keys = {}
    for i in range(de_start + 1, de_end):
        m = re.search(r'"([^"]+)":\s*"([^"]*)"', lines[i])
        if m: existing_de_keys[m.group(1)] = i

    # Update/Fix German block
    # 1. Apply de_missing_from_en
    for key, val in de_missing_from_en.items():
        if key in existing_de_keys:
            idx = existing_de_keys[key]
            lines[idx] = f'        "{key}": "{val}",\n'
        else:
            lines.insert(de_end, f'        "{key}": "{val}",\n')
            de_end += 1

    # 2. Apply manual fixes
    for key, val in MANUAL_DE.items():
        if key in existing_de_keys:
            idx = existing_de_keys[key]
            lines[idx] = f'        "{key}": "{val}",\n'
        else:
            lines.insert(de_end, f'        "{key}": "{val}",\n')
            de_end += 1

    # Update get_text logic
    gt_start = -1
    for i, line in enumerate(lines):
        if 'def get_text(text_key, **kwargs):' in line:
            gt_start = i
            break
    
    if gt_start != -1:
        gt_end = gt_start
        for i in range(gt_start + 1, len(lines)):
            if lines[i].strip() and not lines[i].startswith('    ') and not lines[i].startswith('\t'):
                if not lines[i].startswith('"""') and not lines[i].startswith("'''"):
                    gt_end = i - 1
                    break
            gt_end = i
            
        new_gt = [
            'def get_text(text_key, **kwargs):\n',
            '    """\n',
            '    Retrieves the translated text for a given key.\n',
            '    Prioritizes: Static -> Cache -> English -> German -> Key.\n',
            '    """\n',
            '    if text_key is None:\n',
            '        return ""\n',
            '    \n',
            '    # 1. Try static translation (Current Language)\n',
            '    text = TRANSLATIONS.get(CURRENT_LANGUAGE, {}).get(text_key)\n',
            '    \n',
            '    # 2. Try cache\n',
            '    if text is None:\n',
            '        cache_key = f"{CURRENT_LANGUAGE}_{text_key}"\n',
            '        with CACHE_LOCK:\n',
            '            text = _TRANSLATION_CACHE.get(cache_key)\n',
            '            \n',
            '    # 3. Fallbacks\n',
            '    # If not found in current language, try English static\n',
            '    if text is None and CURRENT_LANGUAGE != "en":\n',
            '        text = TRANSLATIONS.get("en", {}).get(text_key)\n',
            '    \n',
            '    # If still not found, try German static\n',
            '    if text is None and CURRENT_LANGUAGE != "de":\n',
            '        text = TRANSLATIONS.get("de", {}).get(text_key)\n',
            '        \n',
            '    # 4. If still not found, trigger background translation and return key\n',
            '    if text is None:\n',
            '        text = text_key\n',
            '        if CURRENT_LANGUAGE not in ["en", "de"]:\n',
            '            cache_key = f"{CURRENT_LANGUAGE}_{text_key}"\n',
            '            global PENDING_TRANSLATIONS\n',
            '            with CACHE_LOCK:\n',
            '                is_cached = cache_key in _TRANSLATION_CACHE\n',
            '            \n',
            '            if PENDING_TRANSLATIONS < 50 and not is_cached:\n',
            '                PENDING_TRANSLATIONS += 1\n',
            '                threading.Thread(\n',
            '                    target=background_translate, \n',
            '                    args=(text_key, CURRENT_LANGUAGE, cache_key),\n',
            '                    daemon=True\n',
            '                ).start()\n',
            '\n',
            '    if kwargs:\n',
            '        try:\n',
            '            return text.format(**kwargs)\n',
            '        except:\n',
            '            return text\n',
            '    return text\n'
        ]
        lines[gt_start:gt_end+1] = new_gt

    with open(TRANS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("SAFE Overhaul complete.")

if __name__ == "__main__":
    overhaul()
