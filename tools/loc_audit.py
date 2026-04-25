import os
import sys
import re

# Mache Module aus dem Hauptverzeichnis verfügbar
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from translations import TRANSLATIONS

def audit_translations():
    print(f"{'='*60}")
    print("STARTE LOKALISIERUNGS-AUDIT")
    print(f"{'='*60}\n")

    de = TRANSLATIONS.get('de', {})
    en = TRANSLATIONS.get('en', {})

    de_keys = set(de.keys())
    en_keys = set(en.keys())

    all_keys = de_keys | en_keys
    errors = 0
    warnings = 0

    # 1. Missing Keys
    missing_in_en = de_keys - en_keys
    missing_in_de = en_keys - de_keys

    if missing_in_en:
        print(f"[FEHLER] Keys fehlen in EN: {len(missing_in_en)}")
        for k in sorted(missing_in_en):
            print(f"  - {k}")
        errors += len(missing_in_en)

    if missing_in_de:
        print(f"[FEHLER] Keys fehlen in DE: {len(missing_in_de)}")
        for k in sorted(missing_in_de):
            print(f"  - {k}")
        errors += len(missing_in_de)

    # 2. Placeholder Consistency & Language Leaks
    for key in sorted(all_keys):
        txt_de = de.get(key, "")
        txt_en = en.get(key, "")

        # Platzhalter finden (z.B. {name})
        placeholders_de = set(re.findall(r"\{(\w+)\}", str(txt_de)))
        placeholders_en = set(re.findall(r"\{(\w+)\}", str(txt_en)))

        if placeholders_de != placeholders_en and key in de and key in en:
            print(f"[FEHLER] Platzhalter-Mismatch bei '{key}':")
            print(f"  DE: {placeholders_de}")
            print(f"  EN: {placeholders_en}")
            errors += 1

        # Language Leak Check (Sehr einfach: Suche nach ' the ', ' is ', ' and ', ' you ' in Deutsch)
        # Wir ignorieren Keys, die technische Namen sind oder absichtlich Englisch (z.B. Genres)
        if key in de:
            val_de = str(de[key]).lower()
            # Ignoriere bekannte englische Begriffe wie "Action", "RPG", "Settings" etc.
            # Aber warne bei kompletten Sätzen oder Artikeln.
            leaks = [w for w in [' the ', ' is ', ' and ', ' will ', ' with '] if w in val_de]
            if leaks and key not in ['Action', 'RPG', 'MMO', 'AAA', 'settings', 'DevKit']:
                 print(f"[WARNUNG] Möglicher Language-Leak (Englisch in DE) bei '{key}':")
                 print(f"  Text: {de[key]}")
                 print(f"  Gefunden: {leaks}")
                 warnings += 1

    print(f"\n{'='*60}")
    print(f"AUDIT BEENDET")
    print(f"Fehler: {errors}")
    print(f"Warnungen: {warnings}")
    print(f"{'='*60}")

    return errors == 0

if __name__ == "__main__":
    success = audit_translations()
    sys.exit(0 if success else 1)
