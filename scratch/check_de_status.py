import sys
import os

# Add the path to the game directory
sys.path.append(r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon')

from translations import TRANSLATIONS

def audit_german():
    de = TRANSLATIONS.get('de', {})
    en = TRANSLATIONS.get('en', {})
    
    missing_count = 0
    identical_count = 0
    total_count = len(en)
    
    for key, en_val in en.items():
        if key not in de:
            missing_count += 1
            print(f"MISSING: {key}")
        elif de[key] == en_val and en_val.strip() != "" and len(en_val) > 3:
            # Simple heuristic: if it's the same and longer than 3 chars (to avoid OK, Yes, No, etc.)
            identical_count += 1
            # print(f"IDENTICAL: {key} -> {en_val}")
            
    print(f"\nTotal English keys: {total_count}")
    print(f"Missing German keys: {missing_count}")
    print(f"Identical German keys (heuristic): {identical_count}")

if __name__ == "__main__":
    audit_german()
