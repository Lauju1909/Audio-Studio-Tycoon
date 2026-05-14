
import json
import re

translations_path = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'

with open(translations_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

namespace = {}
try:
    exec(content, namespace)
    translations = namespace.get('TRANSLATIONS', {})
except Exception as e:
    print(f"Error executing translations.py: {e}")
    translations = {}

de_dict = translations.get('de', {})
en_dict = translations.get('en', {})
untranslated = []

for k, v in de_dict.items():
    en_val = en_dict.get(k)
    if en_val and v == en_val and v != k:
        untranslated.append((k, v))

print(f"Total untranslated: {len(untranslated)}")
for k, v in untranslated:
    print(f"{k}: {v}")
