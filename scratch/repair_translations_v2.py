import os
import re
import json

def repair():
    base_path = r"C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon"
    current_file = os.path.join(base_path, "translations.py")
    backup_file = os.path.join(base_path, "translations.py.bak")
    
    # 1. Read the logic from current file (lines 1-133)
    with open(current_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        logic_part = "".join(lines[:133])
    
    # 2. Read the dictionary from backup file (from line 111)
    with open(backup_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        dict_part = "".join(lines[110:]) # Line 111 is index 110
        
    # 3. Clean the dictionary part
    # Fix common UTF-8 mangling
    replacements = {
        'Ã¤': 'ä',
        'Ã¶': 'ö',
        'Ã¼': 'ü',
        'Ã': 'Ä',
        'Ã': 'Ö',
        'Ã': 'Ü',
        'Ã': 'ß',
        'ðŸ †': '🏆',
        'ðŸŽ®': '🎮',
        'ðŸ’°': '💰',
        'ðŸ’Š': '💊',
        'ðŸ’»': '💻',
        'ðŸ“ˆ': '📈',
        'ðŸ“‰': '📉',
        'Ã—': '×',
        'â‚¬': '€',
        'â€¦': '...',
        'â€“': '–',
        'â€”': '—',
        'â€ž': '„',
        'â€œ': '“',
        'â€˜': '‘',
        'â€™': '’',
    }
    
    for mangled, fixed in replacements.items():
        dict_part = dict_part.replace(mangled, fixed)
        
    # 4. Assemble the final file
    final_content = logic_part + "\n" + dict_part
    
    # Ensure it ends with a newline and proper structure
    if not final_content.strip().endswith("}"):
        # If it was truncated in the backup too (unlikely but let's check)
        pass
        
    with open(current_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print("Reparatur abgeschlossen.")

if __name__ == "__main__":
    repair()
