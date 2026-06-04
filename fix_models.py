import re

with open('models.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"\\"\\"Repräsentiert die Entwicklung einer eigenen Spielekonsole.\\"\\""', '"""Repräsentiert die Entwicklung einer eigenen Spielekonsole."""')
content = content.replace('"\\""Repräsentiert die Entwicklung einer eigenen Spielekonsole."\\""', '"""Repräsentiert die Entwicklung einer eigenen Spielekonsole."""')
content = content.replace('\"\\\"\"Repräsentiert die Entwicklung einer eigenen Spielekonsole.\\\"\"\"', '"""Repräsentiert die Entwicklung einer eigenen Spielekonsole."""')

# Actually, just search for it manually and replace
content = re.sub(r'".*Repräsentiert die Entwicklung einer eigenen Spielekonsole.*"', '"""Repräsentiert die Entwicklung einer eigenen Spielekonsole."""', content)

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax in models.py")
