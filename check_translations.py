import sys
sys.path.append('.')
from translations import TRANSLATIONS
import json

en = TRANSLATIONS.get("en", {})
de = TRANSLATIONS.get("de", {})

same = []
for k in en.keys():
    if en[k] == de[k] and len(en[k]) > 10:
        same.append({k: en[k]})

with open("same.json", "w", encoding="utf-8") as f:
    json.dump(same, f, indent=2, ensure_ascii=False)
