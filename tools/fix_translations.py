#!/usr/bin/env python3
"""
Bereinige doppelte Keys in translations.py.
Entfernt alle frueheren Vorkommen eines Keys und behaelt nur das letzte.
"""

import re
import os
import sys

game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = os.path.join(game_dir, "translations.py")

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split('\n')

# Finde den Start jedes Sprach-Blocks
lang_blocks = {}
current_lang = None
current_start = None
brace_depth = 0
in_translations = False

for i, line in enumerate(lines):
    if "TRANSLATIONS = {" in line:
        in_translations = True
        continue
    
    if in_translations:
        # Erkenne Sprach-Start
        m = re.match(r"\s+'(\w+)'\s*:\s*\{", line)
        if m and brace_depth == 0:
            current_lang = m.group(1)
            current_start = i
            brace_depth = 1
            lang_blocks[current_lang] = {"start": i, "end": None, "lines": []}
            continue
        
        if current_lang:
            brace_depth += line.count('{') - line.count('}')
            lang_blocks[current_lang]["lines"].append((i, line))
            if brace_depth <= 0:
                lang_blocks[current_lang]["end"] = i
                current_lang = None
                brace_depth = 0

# Fuer jeden Sprach-Block: Finde und entferne doppelte Keys
total_removed = 0
lines_to_remove = set()

for lang, block in lang_blocks.items():
    key_last_occurrence = {}  # key -> line_index
    key_first_occurrence = {}  # key -> line_index
    
    for line_idx, line_content in block["lines"]:
        # Matche Key-Definition: 'key_name': "..."  oder 'key_name': f"..." etc
        m = re.match(r"\s+'([^']+)'\s*:", line_content)
        if m:
            key = m.group(1)
            if key in key_last_occurrence:
                # Doppelter Key! Merke die erste Zeile zum Loeschen
                lines_to_remove.add(key_first_occurrence[key])
                total_removed += 1
                print(f"  [{lang}] Doppelter Key '{key}': Zeile {key_first_occurrence[key]+1} entfernt (behalte Zeile {line_idx+1})")
            key_first_occurrence[key] = key_last_occurrence.get(key, line_idx)
            key_last_occurrence[key] = line_idx

print(f"\nInsgesamt {total_removed} doppelte Zeilen gefunden.")

if total_removed > 0:
    # Neue Datei schreiben ohne die doppelten Zeilen
    new_lines = []
    for i, line in enumerate(lines):
        if i not in lines_to_remove:
            new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"\n{total_removed} doppelte Zeilen entfernt und Datei gespeichert!")
else:
    print("Keine doppelten Zeilen gefunden.")
