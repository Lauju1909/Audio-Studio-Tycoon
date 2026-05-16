import sys
import os
import json
import re

# Add the project root to sys.path to import translations
PROJECT_ROOT = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon'
sys.path.append(PROJECT_ROOT)

try:
    import translations
    from translations import TRANSLATIONS
except ImportError as e:
    print(f"Error importing translations: {e}")
    sys.exit(1)

def analyze():
    en_keys = set(TRANSLATIONS.get('en', {}).keys())
    de_keys = set(TRANSLATIONS.get('de', {}).keys())
    
    missing_in_de = en_keys - de_keys
    missing_in_en = de_keys - en_keys
    
    print(f"Total English keys: {len(en_keys)}")
    print(f"Total German keys: {len(de_keys)}")
    print(f"Missing in German: {len(missing_in_de)}")
    print(f"Missing in English: {len(missing_in_en)}")
    
    # Check for mangled chars in German
    mangled_patterns = [
        ('ðŸ †', '🏆'),
        ('Ã¤', 'ä'),
        ('Ã¶', 'ö'),
        ('Ã¼', 'ü'),
        ('ÃŸ', 'ß'),
        ('Ã„', 'Ä'),
        ('Ã–', 'Ö'),
        ('Ãœ', 'Ü'),
        ('Ã©', 'é'),
        ('Ã', ' (potential mangled start)')
    ]
    
    mangled_findings = []
    for key, val in TRANSLATIONS.get('de', {}).items():
        for pattern, replacement in mangled_patterns:
            if pattern in val:
                mangled_findings.append((key, val))
                break
                
    print(f"\nFound {len(mangled_findings)} potentially mangled strings in German.")
    for key, val in mangled_findings[:10]:
        print(f"  {key}: {val}")

    # Check for 'ae', 'oe', 'ue' used as fallbacks
    safe_patterns = [
        (r'[a-z]ae[a-z]', 'ae'),
        (r'[a-z]oe[a-z]', 'oe'),
        (r'[a-z]ue[a-z]', 'ue')
    ]
    
    # This is trickier because some words legitimately have 'ae' (like 'Gitarre'? No, 'Aera'?).
    # But in context of 'moeglich', 'laeuft', etc.
    
    # Let's just output the missing keys to a file for review
    results = {
        "missing_in_de": list(missing_in_de),
        "missing_in_en": list(missing_in_en),
        "mangled_findings": mangled_findings
    }
    
    with open('scratch/analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    analyze()
