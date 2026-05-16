import re

def convert_weeks(match):
    val = int(match.group(1))
    if val == 1:
        return '"week": 1'
    if val % 48 == 0:
        years = val // 48
        if years == 1:
            return f'"week": WEEKS_PER_YEAR'
        else:
            return f'"week": {years} * WEEKS_PER_YEAR'
    return match.group(0)

with open('C:/Users/lauri/.gemini/antigravity/scratch/Audio_Studio_Tycoon/game_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Ersetze "week": [Zahl]
new_content = re.sub(r'"week":\s*(\d+)', convert_weeks, content)

with open('C:/Users/lauri/.gemini/antigravity/scratch/Audio_Studio_Tycoon/game_data.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Konvertierung abgeschlossen.")
