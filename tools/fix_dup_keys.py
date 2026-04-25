"""
fix_dup_keys.py
Entfernt die veralteten doppelten Keys aus translations.py,
die durch die Phase-2-Keys bereits oben definiert worden sind.
"""
import re

path = "../translations.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Entferne den alten doppelten Block (DE-Sektion, nach body_sick_recovered)
# Die Zeilen 1082-1089 (die alten upgrade_intel/security/pr/legal/bought/accounting/...)
old_block_pattern = (
    r"        'upgrade_intel': \"Marktforschungs-Abo\",\r?\n"
    r"        'upgrade_security': \"Security-Dienst\",\r?\n"
    r"        'upgrade_pr': \"PR-Agentur Retainer\",\r?\n"
    r"        'upgrade_legal': \"Anwaltskanzlei Retainer\",\r?\n"
    r"        'upgrade_bought': \"\{name\} wurde gekauft und im B.{1,5}ro installiert!\",\r?\n"
    r"        'sender_accounting': \"Buchhaltung\",\r?\n"
    r"        'subject_yearly_report': \"Jahresbilanz \{year\}\",\r?\n"
    r"        'body_yearly_report': \"Hier ist der Bericht f.{1,5}r das vergangene Jahr\.\\\\nEinnahmen: \{income\} EUR\\\\nAusgaben: \{expenses\} EUR\\\\n------------------\\\\nGewinn: \{profit\} EUR\\\\nWeiter so!\",\r?\n"
)

new_content, count = re.subn(old_block_pattern, "", content, count=1)
if count > 0:
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Entfernt {count} alten doppelten Block.")
else:
    print("Kein alter Block gefunden (moeglicherweise bereits bereinigt).")
