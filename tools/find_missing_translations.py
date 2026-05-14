import sys
import re

def get_translations(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex to find the dicts, assuming the structure is:
    # "de": {
    #     "key": "value",
    #     ...
    # },
    # "en": {
    #     "key": "value",
    #     ...
    # }
    
    de_match = re.search(r'"de":\s*\{(.*?)\s*\},\s*"en":', content, re.DOTALL)
    en_match = re.search(r'"en":\s*\{(.*?)\s*\}', content, re.DOTALL)
    
    if not de_match or not en_match:
        print("Could not find de or en dictionaries")
        return None, None
    
    de_str = de_match.group(1)
    en_str = en_match.group(1)
    
    def parse_dict_str(s):
        # Very simple parser for key: value lines
        d = {}
        for line in s.split('\n'):
            match = re.search(r'"(.*?)"\s*:\s*"(.*?)"', line)
            if match:
                d[match.group(1)] = match.group(2)
        return d
    
    de_dict = parse_dict_str(de_str)
    en_dict = parse_dict_str(en_str)
    
    return de_dict, en_dict

if __name__ == "__main__":
    file_path = 'c:/Users/lauri/.gemini/antigravity/scratch/Audio_Studio_Tycoon/translations.py'
    de, en = get_translations(file_path)
    
    if de and en:
        missing = []
        for key in en:
            if key not in de:
                missing.append(key)
        
        print(f"Total keys in EN: {len(en)}")
        print(f"Total keys in DE: {len(de)}")
        print(f"Missing keys in DE: {len(missing)}")
        for m in missing[:50]: # Show first 50
            print(f"'{m}': '{en[m]}'")
        if len(missing) > 50:
            print("...")
