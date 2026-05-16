import json
import os
import sys
import re

# Pfad zur Datei
FILE_PATH = r"C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py"

def repair():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # TRANSLATIONS block extrahieren
    match = re.search(r"TRANSLATIONS = (\{.*?\n\})", content, re.DOTALL)
    if not match:
        print("TRANSLATIONS Block nicht gefunden!")
        return

    translations_str = match.group(1)
    namespace = {}
    try:
        # Wir müssen json nutzen, falls es wie JSON aussieht, oder exec mit Vorsicht.
        # Da es Python-Code ist, nutzen wir exec.
        exec(f"TRANSLATIONS = {translations_str}", namespace)
        translations = namespace["TRANSLATIONS"]
    except Exception as e:
        print(f"Fehler beim Parsen des TRANSLATIONS Blocks: {e}")
        return

    en_dict = translations.get("en", {})
    de_dict = translations.get("de", {})

    print(f"Einträge vor Korrektur: EN={len(en_dict)}, DE={len(de_dict)}")

    manual_fixes = {
        "Echo-Effekt": "Echo-Effekt",
        "Extremsport": "Extremsport",
        "Film-Sync": "Film-Synchronisation",
        "Hörbuch-Boom": "Hörbuch-Boom",
        "Hörgeräte-Tech": "Hörgeräte-Technologie",
        "KI-Mastering": "KI-Mastering",
        "Krisenmanagement": "Krisenmanagement",
        "Lebenssimulation": "Lebenssimulation",
        "Mannschaftssport": "Mannschaftssport",
        "Multiroom-Audio": "Multiroom-Audio",
        "Neuro-Interface": "Neuro-Interface",
        "Party-Spiel": "Party-Spiel",
        "Psycho-Horror": "Psycho-Horror",
        "Reverb-Kammern": "Reverb-Kammern",
        "Rundenbasiert": "Rundenbasiert",
        "Rätsel-Abenteuer": "Rätsel-Abenteuer",
        "SoundCloud-Rap": "SoundCloud-Rap",
        "Surround-Sound": "Surround-Sound",
        "Vinyl-Revival": "Vinyl-Revival",
        "Fahrsimulation": "Fahrsimulation",
        "Geheimdienst-Netzwerk": "Geheimdienst-Netzwerk",
        "Abenteuer": "Abenteuer",
        "Action": "Action",
        "Action-RPG": "Action-RPG",
    }

    count = 0
    for k, v in de_dict.items():
        en_val = en_dict.get(k)
        
        if k in manual_fixes:
            if de_dict[k] != manual_fixes[k]:
                de_dict[k] = manual_fixes[k]
                count += 1
            continue

        if en_val and v == en_val and k != v:
            # Check ob Key Deutsch aussieht (Umlaute oder Großbuchstabe am Anfang bei Worten)
            if re.search(r'[äöüÄÖÜß]', k) or (k[0].isupper() and "_" not in k):
                de_dict[k] = k
                count += 1

    print(f"Anzahl automatischer/manueller Korrekturen: {count}")

    # Synchronisation der Keys
    all_keys = set(en_dict.keys()) | set(de_dict.keys())
    for k in all_keys:
        if k not in en_dict:
            en_dict[k] = k
        if k not in de_dict:
            de_dict[k] = k

    def format_dict(d):
        lines = []
        for k in sorted(d.keys()):
            # JSON dumps sorgt für korrektes Escaping von Newlines und Anführungszeichen
            val_escaped = json.dumps(d[k], ensure_ascii=False)
            lines.append(f'        "{k}": {val_escaped},')
        if lines:
            lines[-1] = lines[-1].rstrip(',')
        return "\n".join(lines)

    new_translations_str = "TRANSLATIONS = {\n"
    new_translations_str += '    "en": {\n'
    new_translations_str += format_dict(en_dict)
    new_translations_str += "\n    },\n"
    new_translations_str += '    "de": {\n'
    new_translations_str += format_dict(de_dict)
    new_translations_str += "\n    }\n"
    new_translations_str += "}"

    new_content = content.replace(match.group(0), new_translations_str)
    
    with open(FILE_PATH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(new_content)
    
    print("Reparatur abgeschlossen.")

if __name__ == "__main__":
    repair()
