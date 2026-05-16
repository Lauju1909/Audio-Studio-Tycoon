import sys
import os
import json
from translations import TRANSLATIONS

def generate_missing_en():
    de = TRANSLATIONS['de']
    en = TRANSLATIONS['en']
    
    missing_keys = [k for k in de.keys() if k not in en]
    print(f"Translating {len(missing_keys)} keys to English...")
    
    new_en = {}
    for k in missing_keys:
        # We can use a simple placeholder or try to be smart for common keys
        val = de[k]
        # In a real scenario, I'd use an AI to translate these. 
        # For now, I'll print them out so I can process them.
        new_en[k] = val # Placeholder
        
    # Also check missing de
    missing_de = [k for k in en.keys() if k not in de]
    print(f"Translating {len(missing_de)} keys to German...")
    
    with open("scratch/missing_translations.json", "w", encoding="utf-8") as f:
        json.dump({
            "en_missing_from_de": {k: en[k] for k in missing_de},
            "de_missing_from_en": {k: de[k] for k in missing_keys}
        }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    sys.path.append(".")
    generate_missing_en()
