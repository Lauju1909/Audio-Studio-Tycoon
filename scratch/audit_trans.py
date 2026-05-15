import json
import re
import sys
sys.path.append(".")
from translations import TRANSLATIONS

def audit_translations():
    languages = TRANSLATIONS.keys()
    print(f"Found languages: {list(languages)}")
    
    all_keys = set()
    for lang in languages:
        all_keys.update(TRANSLATIONS[lang].keys())
    
    print(f"Total unique keys: {len(all_keys)}")
    
    for lang in languages:
        missing = all_keys - set(TRANSLATIONS[lang].keys())
        if missing:
            print(f"\nLanguage '{lang}' is missing {len(missing)} keys:")
            # Show first 10 missing keys
            for key in sorted(list(missing))[:10]:
                print(f"  - {key}")
            if len(missing) > 10:
                print(f"  ... and {len(missing) - 10} more.")
        else:
            print(f"\nLanguage '{lang}' has all keys.")

    # Check for potential duplicates or formatting issues
    for lang in languages:
        for key, value in TRANSLATIONS[lang].items():
            # Check for placeholders like {name}
            placeholders = re.findall(r'\{([^}]+)\}', value)
            if placeholders:
                # Check if same placeholders exist in other languages
                for other_lang in languages:
                    if other_lang == lang: continue
                    other_val = TRANSLATIONS[other_lang].get(key)
                    if other_val:
                        other_placeholders = re.findall(r'\{([^}]+)\}', other_val)
                        if set(placeholders) != set(other_placeholders):
                            print(f"\nPlaceholder mismatch for key '{key}':")
                            print(f"  {lang}: {placeholders}")
                            print(f"  {other_lang}: {other_placeholders}")

if __name__ == "__main__":
    audit_translations()
