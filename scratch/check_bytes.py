import os

TRANS_PATH = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'

with open(TRANS_PATH, 'rb') as f:
    content = f.read()
    
# Search for the pattern for subject_achievement
# "subject_achievement": "ðŸ † MEILENSTEIN ERREICHT: {title}"
# In UTF-8, ð is C3 B0
# Ÿ is C5 B8
# † is E2 80 A0

target = b'"subject_achievement": "'
idx = content.find(target)
if idx != -1:
    snippet = content[idx:idx+100]
    print(f"Found at {idx}: {snippet}")
    print(f"Hex: {snippet.hex(' ')}")
else:
    print("Pattern not found")
