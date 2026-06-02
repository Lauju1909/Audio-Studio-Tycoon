import sys
with open('test_vr.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"duration_weeks": 8', '"duration_weeks": 8, "bugs": 0')

with open('test_vr.py', 'w', encoding='utf-8') as f:
    f.write(text)
