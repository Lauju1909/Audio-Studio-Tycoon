import os

with open("translations.py", "r", encoding="utf-8") as f:
    content = f.read()

new_content = ""
in_quotes = False
escape = False

for char in content:
    if char == "\\" and not escape:
        escape = True
        new_content += char
        continue
    
    if char == "\"" and not escape:
        in_quotes = not in_quotes
    
    if char == "\n" and in_quotes:
        new_content += "\\n"
    else:
        new_content += char
    
    escape = False

with open("translations.py", "w", encoding="utf-8") as f:
    f.write(new_content)
