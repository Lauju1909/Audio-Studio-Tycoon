
import sys
import os

# Path to translations.py
file_path = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'

def extract_keys(content, lang_start_marker):
    keys = set()
    start_index = content.find(lang_start_marker)
    if start_index == -1:
        return keys
    
    # Find the matching closing brace
    brace_count = 0
    in_lang_block = False
    for i in range(start_index, len(content)):
        if content[i] == '{':
            brace_count += 1
            in_lang_block = True
        elif content[i] == '}':
            brace_count -= 1
            if in_lang_block and brace_count == 0:
                end_index = i
                break
    else:
        end_index = len(content)

    lang_block = content[start_index:end_index]
    
    # Very simple key extraction assuming "key": "value" format
    import re
    # Match strings starting with " and followed by ":
    found_keys = re.findall(r'"([^"]+)":', lang_block)
    return set(found_keys)

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    de_keys = extract_keys(content, '"de": {')
    en_keys = extract_keys(content, '"en": {')

    missing_in_en = de_keys - en_keys
    missing_in_de = en_keys - de_keys

    print(f"Keys in German: {len(de_keys)}")
    print(f"Keys in English: {len(en_keys)}")
    
    if missing_in_en:
        print("\nMissing in English:")
        for k in sorted(missing_in_en):
            print(f"  - {k}")
    else:
        print("\nNo keys missing in English.")

    if missing_in_de:
        print("\nMissing in German:")
        for k in sorted(missing_in_de):
            print(f"  - {k}")
    else:
        print("\nNo keys missing in German.")

except Exception as e:
    print(f"Error: {e}")
