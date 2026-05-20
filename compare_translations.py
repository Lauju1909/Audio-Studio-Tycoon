import sys
import os

# Force utf-8 stdout/stderr on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Add the scratch directory to sys.path to import translations
sys.path.append(r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon')

try:
    import translations
    en_keys = set(translations.TRANSLATIONS.get("en", {}).keys())
    de_keys = set(translations.TRANSLATIONS.get("de", {}).keys())
    
    missing_in_de = en_keys - de_keys
    missing_in_en = de_keys - en_keys
    
    print(f"Missing in German: {len(missing_in_de)}")
    for key in sorted(missing_in_de):
        print(f"  - {key}: {translations.TRANSLATIONS['en'][key]}")
        
    print(f"\nMissing in English: {len(missing_in_en)}")
    for key in sorted(missing_in_en):
        print(f"  - {key}: {translations.TRANSLATIONS['de'][key]}")
        
except Exception as e:
    print(f"Error: {e}")
