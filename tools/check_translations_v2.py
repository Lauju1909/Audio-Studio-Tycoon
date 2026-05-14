import os
import sys

# Add the directory to sys.path to import translations
sys.path.append('c:/Users/lauri/.gemini/antigravity/scratch/Audio_Studio_Tycoon')

import translations

de_keys = set(translations.TRANSLATIONS['de'].keys())
en_keys = set(translations.TRANSLATIONS['en'].keys())

missing_in_de = en_keys - de_keys
missing_in_en = de_keys - en_keys

print(f"Total keys in EN: {len(en_keys)}")
print(f"Total keys in DE: {len(de_keys)}")
print(f"Missing in DE: {len(missing_in_de)}")
for key in sorted(missing_in_de):
    print(f"DE missing: {key}")

print(f"Missing in EN: {len(missing_in_en)}")
# Only print first 20 missing in EN if there are many
for key in sorted(missing_in_en)[:20]:
    print(f"EN missing: {key}")
