
import re

with open("translations.py", "r", encoding="utf-8") as f:
    content = f.read()

# Separate DE and EN blocks
de_start = content.find('"de": {')
en_start = content.find('"en": {', de_start)
de_block = content[de_start:en_start]
en_block = content[en_start:]

# Fix keys in DE block that have English values but the key itself is German-looking
# List from check_translations.py
to_fix = {
    "Audio-Deepfakes": "Audio Deepfakes",
    "Echo-Effekt": "Echo Effect",
    "Extremsport": "Extreme Sports",
    "Fahrsimulation": "Driving Sim",
    "Geheimdienst-Netzwerk": "Intel Network",
    "KI-Mastering": "AI Mastering",
    "Krisenmanagement": "Crisis Management",
    "Lebenssimulation": "Life Simulation",
    "Mannschaftssport": "Team Sports",
    "Multiroom-Audio": "Multi-room Audio",
    "Party-Spiel": "Party Game",
    "Psycho-Horror": "Psychological Horror",
    "Renn-Simulation": "Racing Sim",
    "Rundenbasiert": "Turn-Based",
    "Rätsel-Abenteuer": "Puzzle Adventure",
    "Hörbuch-Boom": "Audiobook Boom"
}

for k, v in to_fix.items():
    # Use regex to find the line in the DE block
    pattern = r'"' + re.escape(k) + r'":\s*"' + re.escape(v) + r'"'
    replacement = f'"{k}": "{k}"'
    de_block = re.sub(pattern, replacement, de_block)

new_content = content[:de_start] + de_block + en_block

with open("translations.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Fixed common translation errors in DE block.")
