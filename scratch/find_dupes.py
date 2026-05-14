
import re
from collections import Counter

with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

de_start = content.find('"de": {')
de_end = content.find('    },', de_start)
en_start = content.find('"en": {', de_end)
en_end = content.rfind('    }')

de_section = content[de_start:de_end]
en_section = content[en_start:en_end]

de_keys = re.findall(r'        "([^"]+)":', de_section)
en_keys = re.findall(r'        "([^"]+)":', en_section)

de_dupes = [k for k, v in Counter(de_keys).items() if v > 1]
en_dupes = [k for k, v in Counter(en_keys).items() if v > 1]

print(f"DE Duplikate: {de_dupes}")
print(f"EN Duplikate: {en_dupes}")

# Zeige Zeilen für Duplikate
for key in de_dupes + en_dupes:
    print(f"\nSuche nach: {key}")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if f'"{key}":' in line:
            print(f"  Zeile {i+1}: {line.strip()}")
