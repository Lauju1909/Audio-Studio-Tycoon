import sys
import os

# Add project path to sys.path to import translations
sys.path.append(r"C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon")

try:
    import translations
    from translations import TRANSLATIONS
except ImportError as e:
    print(f"Error importing translations: {e}")
    sys.exit(1)

def check_parity():
    en_keys = set(TRANSLATIONS.get("en", {}).keys())
    de_keys = set(TRANSLATIONS.get("de", {}).keys())
    
    missing_in_de = en_keys - de_keys
    missing_in_en = de_keys - en_keys
    
    print(f"Total EN keys: {len(en_keys)}")
    print(f"Total DE keys: {len(de_keys)}")
    
    if missing_in_de:
        print(f"\nMissing in DE ({len(missing_in_de)}):")
        for key in sorted(missing_in_de):
            print(f"  - {key}")
            
    if missing_in_en:
        print(f"\nMissing in EN ({len(missing_in_en)}):")
        for key in sorted(missing_in_en):
            print(f"  - {key}")
            
    if not missing_in_de and not missing_in_en:
        print("\nParity check PASSED: All keys are synchronized.")
    else:
        print("\nParity check FAILED: Keys are missing.")

if __name__ == "__main__":
    check_parity()
