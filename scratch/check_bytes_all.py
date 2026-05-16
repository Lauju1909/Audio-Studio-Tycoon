import os

TRANS_PATH = r'C:\Users\lauri\.gemini\antigravity\scratch\Audio_Studio_Tycoon\translations.py'

with open(TRANS_PATH, 'rb') as f:
    content = f.read()
    
target = b'"subject_achievement": "'
start = 0
while True:
    idx = content.find(target, start)
    if idx == -1: break
    snippet = content[idx:idx+100]
    print(f"Found at {idx}: {snippet}")
    print(f"Hex: {snippet.hex(' ')}")
    start = idx + 1
