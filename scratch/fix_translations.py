
import sys
import os
import re

def fix_mojibake(text):
    if not isinstance(text, str):
        return text
    
    # Try automatic recovery first
    for codec in ['cp1252', 'latin-1']:
        try:
            if any(c in text for c in "Ãðâ"):
                recovered = text.encode(codec).decode('utf-8')
                if recovered != text:
                    # Check if it looks reasonable (no excessive replacement chars)
                    if recovered.count('\ufffd') < 2:
                        return recovered
        except Exception:
            pass
            
    # Manual fallback for specific stubborn patterns
    replacements = {
        'ðŸ †': '🏆',
        'ðŸ’°': '💰',
        'ðŸ’ˆ': '💊',
        'ðŸ“ˆ': '📈',
        'ðŸ“‰': '📉',
        'ðŸŽ®': '🎮',
        'ðŸ“§': '📧',
        'ðŸš€': '🚀',
        'ðŸ“¹': '🎥',
        'ðŸŽ¤': '🎙️',
        'ðŸ’»': '💻',
        'Ã¤': 'ä',
        'Ã¶': 'ö',
        'Ã¼': 'ü',
        'Ã„': 'Ä',
        'Ã–': 'Ö',
        'Ãœ': 'Ü',
        'ÃŸ': 'ß',
        'â€“': '–',
        'â€ž': '„',
        'â€œ': '“',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
        
    return text

def run():
    print("Starting translation fix and synchronization...")
    
    # Import the current translations
    sys.path.append(os.getcwd())
    if 'translations' in sys.modules:
        del sys.modules['translations']
    import translations
    
    trans = translations.TRANSLATIONS
    de = trans.get('de', {})
    en = trans.get('en', {})
    
    # Collect all keys from both
    all_keys = set(de.keys()) | set(en.keys())
    
    new_de = {}
    new_en = {}
    
    for k in all_keys:
        # Fix the key itself if it has mojibake
        k_fixed = fix_mojibake(k)
        
        # Get values, fallback to the other language if missing
        val_de = de.get(k, en.get(k, k_fixed))
        val_en = en.get(k, de.get(k, k_fixed))
        
        # Fix mojibake in values
        val_de = fix_mojibake(val_de)
        val_en = fix_mojibake(val_en)
        
        new_de[k_fixed] = val_de
        new_en[k_fixed] = val_en

    # Read the original file to preserve the header
    with open('translations.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    header = []
    for line in lines:
        if 'TRANSLATIONS = {' in line:
            header.append(line)
            break
        header.append(line)
    
    # Write the new file
    with open('translations.py', 'w', encoding='utf-8') as f:
        f.writelines(header)
        
        f.write('    "de": {\n')
        for k in sorted(new_de.keys()):
            # Escape double quotes for the python string
            v = new_de[k].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            f.write(f'        "{k}": "{v}",\n')
        f.write('    },\n')
        
        f.write('    "en": {\n')
        for k in sorted(new_en.keys()):
            v = new_en[k].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            f.write(f'        "{k}": "{v}",\n')
        f.write('    }\n')
        f.write('}\n')

    print(f"Successfully synchronized {len(all_keys)} keys.")
    print("File saved as UTF-8.")

if __name__ == "__main__":
    run()
