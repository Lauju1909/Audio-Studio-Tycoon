import json
import os
import re

TRANS_PATH = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'
MISSING_PATH = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\scratch\missing_translations.json'

def fix_encoding(text):
    if not isinstance(text, str):
        return text
    # Fix the trophy emoji and others if needed
    text = text.replace('ðŸ †', '🏆')
    return text

def merge_translations():
    with open(MISSING_PATH, 'r', encoding='utf-8') as f:
        missing_data = json.load(f)
    
    en_missing_from_de = missing_data.get('en_missing_from_de', {})
    de_missing_from_en = missing_data.get('de_missing_from_en', {})
    
    with open(TRANS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update English translations (en_missing_from_de actually means English keys that should be in German, 
    # but the json has "en_missing_from_de" with English values. Wait.)
    # Let's check the json structure again.
    # "en_missing_from_de": { "production_merge_title": "Production & Storage Management", ... }
    # These are keys present in English but missing from German.
    
    # 2. Update German translations
    # Find the "de": { ... } block
    de_match = re.search(r'"de":\s*\{', content)
    if not de_match:
        print("Could not find German translations block")
        return
    
    # Extract the German block
    # This is tricky because the file is large.
    # Let's try to find the end of the "de" block.
    # It usually ends with a closing brace followed by a comma or the end of the TRANSLATIONS dict.
    
    # Actually, it's easier to just rebuild the TRANSLATIONS dict in a script and write it back, 
    # but the file has a lot of header code.
    
    # Let's try to find the lines for "en": { and "de": {
    lines = content.split('\n')
    en_start = -1
    de_start = -1
    
    for i, line in enumerate(lines):
        if '"en": {' in line:
            en_start = i
        if '"de": {' in line:
            de_start = i
            
    if en_start == -1 or de_start == -1:
        print(f"Starts not found: en={en_start}, de={de_start}")
        return

    # Helper to find closing brace
    def find_block_end(start_idx):
        brace_count = 0
        for i in range(start_idx, len(lines)):
            brace_count += lines[i].count('{')
            brace_count -= lines[i].count('}')
            if brace_count == 0:
                return i
        return -1

    en_end = find_block_end(en_start)
    de_end = find_block_end(de_start)
    
    print(f"EN Block: {en_start} to {en_end}")
    print(f"DE Block: {de_start} to {de_end}")

    # Instead of regex, let's just do a simple line replacement for the missing keys.
    # For German:
    new_de_lines = []
    # We add the missing ones at the end of the existing ones (before the closing brace)
    
    # Let's collect existing DE keys to avoid duplicates
    existing_de_keys = set()
    for i in range(de_start + 1, de_end):
        m = re.search(r'"([^"]+)":', lines[i])
        if m:
            existing_de_keys.add(m.group(1))
            
    # Also fix encoding in existing lines
    for i in range(de_start + 1, de_end):
        lines[i] = fix_encoding(lines[i])

    added_count = 0
    # Add from "de_missing_from_en" (which seems to be the actual German translations found in another file)
    for key, val in de_missing_from_en.items():
        if key not in existing_de_keys:
            val = fix_encoding(val)
            # Find the last key entry in DE and insert after it, or just before the end
            lines.insert(de_end, f'        "{key}": "{val}",')
            de_end += 1
            added_count += 1
            existing_de_keys.add(key)
            
    print(f"Added {added_count} German translations.")
    
    # 3. Update get_text logic
    # Find get_text function
    gt_start = -1
    gt_end = -1
    for i, line in enumerate(lines):
        if 'def get_text(text_key, **kwargs):' in line:
            gt_start = i
            break
    
    if gt_start != -1:
        gt_end = find_block_end(gt_start) # This might not work for functions if brace count is 0 inside
        # Functions in Python don't use braces. I need another way.
        # Let's find the next 'def ' or end of file.
        for i in range(gt_start + 1, len(lines)):
            if lines[i].startswith('def ') or lines[i].startswith('TRANSLATIONS ='):
                gt_end = i - 1
                break
        if gt_end == -1: gt_end = len(lines) - 1
        
        print(f"get_text: {gt_start} to {gt_end}")
        
        new_gt = [
            'def get_text(text_key, **kwargs):',
            '    """',
            '    Retrieves the translated text for a given key.',
            '    Prioritizes: Static -> Cache -> English -> German -> Key.',
            '    """',
            '    # 1. Try static translation',
            '    text = TRANSLATIONS.get(CURRENT_LANGUAGE, {}).get(text_key)',
            '    ',
            '    # 2. Try cache',
            '    if text is None:',
            '        cache_key = f"{CURRENT_LANGUAGE}_{text_key}"',
            '        with CACHE_LOCK:',
            '            text = _TRANSLATION_CACHE.get(cache_key)',
            '            ',
            '    # 3. Fallbacks',
            '    if text is None and CURRENT_LANGUAGE != "en":',
            '        text = TRANSLATIONS.get("en", {}).get(text_key)',
            '    ',
            '    if text is None and CURRENT_LANGUAGE != "de":',
            '        text = TRANSLATIONS.get("de", {}).get(text_key)',
            '        ',
            '    # 4. If still not found, trigger background translation',
            '    if text is None:',
            '        text = text_key # Fallback to key while translating',
            '        if CURRENT_LANGUAGE not in ["en", "de"]:',
            '            cache_key = f"{CURRENT_LANGUAGE}_{text_key}"',
            '            # Only start if not already pending/cached',
            '            global PENDING_TRANSLATIONS',
            '            if PENDING_TRANSLATIONS < 50 and cache_key not in _TRANSLATION_CACHE:',
            '                PENDING_TRANSLATIONS += 1',
            '                thread = threading.Thread(',
            '                    target=background_translate, ',
            '                    args=(text_key, CURRENT_LANGUAGE, cache_key),',
            '                    daemon=True',
            '                )',
            '                thread.start()',
            '',
            '    if kwargs:',
            '        try:',
            '            return text.format(**kwargs)',
            '        except:',
            '            return text',
            '    return text'
        ]
        
        # Replace the function
        lines[gt_start:gt_end+1] = new_gt

    with open(TRANS_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("translations.py updated successfully.")

if __name__ == "__main__":
    merge_translations()
