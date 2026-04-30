import os
import sys
import json
import re

def find_missing_keys():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import translations
    existing_en = translations.TRANSLATIONS.get("en", {})
    existing_de = translations.TRANSLATIONS.get("de", {})
    
    # We will just grep through all .py files for get_text('key'
    import glob
    files = glob.glob("*.py") + glob.glob("menus/*.py")
    
    keys_found = set()
    pattern = re.compile(r"get_text\(['\"]([^'\"]+)['\"]")
    
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
            for match in pattern.findall(content):
                keys_found.add(match)
                
    missing_de = {}
    missing_en = {}
    
    for key in keys_found:
        if key not in existing_de:
            # Generate a nice German translation
            pretty = key.replace("_", " ").title()
            if "Menu" in pretty: pretty = pretty.replace("Menu", "Menü")
            missing_de[key] = pretty
        if key not in existing_en:
            pretty = key.replace("_", " ").title()
            missing_en[key] = pretty
            
    with open("missing_de.json", "w", encoding="utf-8") as f:
        json.dump(missing_de, f, indent=4, ensure_ascii=False)
    with open("missing_en.json", "w", encoding="utf-8") as f:
        json.dump(missing_en, f, indent=4, ensure_ascii=False)
        
    print(f"Gefunden: {len(missing_de)} fehlende DE Keys, {len(missing_en)} fehlende EN Keys")

if __name__ == "__main__":
    find_missing_keys()
