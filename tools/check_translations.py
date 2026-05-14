
import json
import os

translations_path = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'
missing_de_path = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\missing_de.json'
missing_en_path = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\missing_en.json'

with open(missing_de_path, 'r', encoding='utf-8') as f:
    missing_de = json.load(f)

with open(missing_en_path, 'r', encoding='utf-8') as f:
    missing_en = json.load(f)

# Mock the module to get the TRANSLATIONS dict
with open(translations_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# We need to execute the file to get the dict, but we can also just extract it or mock the imports
# Simplest: use exec but mock sys and other imports if needed
namespace = {}
try:
    exec(content, namespace)
    translations = namespace.get('TRANSLATIONS', {})
except Exception as e:
    print(f"Error executing translations.py: {e}")
    translations = {}

de_keys = translations.get('de', {}).keys()
en_keys = translations.get('en', {}).keys()

still_missing_de = [k for k in missing_de if k not in de_keys]
still_missing_en = [k for k in missing_en if k not in en_keys]

print(f"Still missing in DE: {still_missing_de}")
print(f"Still missing in EN: {still_missing_en}")

from collections import Counter
import re

def find_duplicates(section_name, start_marker, end_marker):
    start_index = content.find(start_marker)
    end_index = content.find(end_marker, start_index)
    section_content = content[start_index:end_index]
    keys = re.findall(r'"([^"]+)":', section_content)
    counts = Counter(keys)
    dupes = [k for k, v in counts.items() if v > 1]
    return dupes

de_dupes = find_duplicates("DE", '"de": {', '},')
en_dupes = find_duplicates("EN", '"en": {', '}')

print(f"Duplicates in DE: {de_dupes}")
print(f"Duplicates in EN: {en_dupes}")

de_dict = translations.get('de', {})
untranslated = []
for k, v in de_dict.items():
    en_val = translations.get('en', {}).get(k)
    # If the German value is equal to the English value, and they are not the same as the key (which might be intended for some technical terms)
    if en_val and v == en_val and v != k:
        untranslated.append((k, v))
    # Or if the value is English but the key is German
    elif any(word in v.lower() for word in ["management", "experts", "network", "simulation", "horror", "sports", "interface"]):
        # This is a bit risky but good for identification
        if k != v and v == en_val:
            if (k, v) not in untranslated:
                untranslated.append((k, v))

print(f"Untranslated (same as EN): {len(untranslated)}")
for k, v in untranslated:
    try:
        print(f"  {k}: {v}")
    except UnicodeEncodeError:
        print(f"  {k.encode('ascii', 'replace').decode()}: {v.encode('ascii', 'replace').decode()}")
