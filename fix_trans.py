import os
with open('translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"key_down": "Down",`n        "key_left": "Left",`n        "key_right": "Right",', '"key_down": "Down",\n        "key_left": "Left",\n        "key_right": "Right",')
content = content.replace('"key_down": "Nach unten",`n        "key_left": "Nach links",`n        "key_right": "Nach rechts",', '"key_down": "Nach unten",\n        "key_left": "Nach links",\n        "key_right": "Nach rechts",')

with open('translations.py', 'w', encoding='utf-8') as f:
    f.write(content)
