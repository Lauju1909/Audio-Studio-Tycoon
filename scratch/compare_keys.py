
import re

with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

de_start = content.find('"de": {')
de_end = content.find('    },', de_start)
en_start = content.find('"en": {', de_end)
en_end = content.rfind('    }')

de_section = content[de_start:de_end]
en_section = content[en_start:en_end]

de_keys = set(re.findall(r'        "([^"]+)":', de_section))
en_keys = set(re.findall(r'        "([^"]+)":', en_section))

only_de = de_keys - en_keys
only_en = en_keys - de_keys

print(f"Nur in DE ({len(only_de)}): {sorted(list(only_de))}")
print(f"Nur in EN ({len(only_en)}): {sorted(list(only_en))}")
