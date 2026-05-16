import os

def add_keys():
    base_path = r"C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon"
    current_file = os.path.join(base_path, "translations.py")
    
    with open(current_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    new_keys_en = {
        "slot_label": "Slot",
        "update_waiting": "Waiting for game to exit...",
        "update_unpacking": "Unpacking update...",
        "update_installing": "Installing files...",
        "update_finished": "Update finished! Starting game...",
        "update_error_unpack": "ERROR: Unpacking failed!",
    }
    
    new_keys_de = {
        "slot_label": "Slot",
        "update_waiting": "Warte auf Spielende...",
        "update_unpacking": "Entpacke Update...",
        "update_installing": "Installiere Dateien...",
        "update_finished": "Update abgeschlossen! Starte Spiel...",
        "update_error_unpack": "FEHLER: Entpacken fehlgeschlagen!",
    }
    
    # Insert before the end of 'en' block
    # The 'en' block ends at the last "    }," before "    \"de\": {"
    en_end_marker = '    },\n    "de": {'
    if en_end_marker in content:
        en_insertion = ""
        for k, v in new_keys_en.items():
            en_insertion += f'        "{k}": "{v}",\n'
        content = content.replace(en_end_marker, en_insertion + en_end_marker)
        
    # Insert before the end of 'de' block
    # The 'de' block ends at the last "    }\n}"
    de_end_marker = '    }\n}'
    if content.strip().endswith(de_end_marker):
        de_insertion = ""
        for k, v in new_keys_de.items():
            de_insertion += f'        "{k}": "{v}",\n'
        # Replace the last occurrence
        content = content.replace(de_end_marker, de_insertion + de_end_marker)

    with open(current_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Keys erfolgreich hinzugefügt.")

if __name__ == "__main__":
    add_keys()
