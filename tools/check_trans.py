import json
with open('translations.py', 'r', encoding='utf-8') as f:
    text = f.read()

de_idx = text.find('"de": {')
en_idx = text.find('"en": {')
print(de_idx, en_idx)
