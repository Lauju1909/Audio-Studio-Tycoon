import re
content = open('menus/business.py', 'r', encoding='utf-8').read()
pattern = r"get_text\('(esports[^']+)'"
matches = re.findall(pattern, content)
for k in sorted(set(matches)):
    print(k)
