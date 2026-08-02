import os
import re

classes = [
    "ESportsSponsorMenu",
    "ConsoleCreateMenu",
    "ConsoleComponentsMenu",
    "PodcastMenu",
    "PublisherHubMenu",
    "PublisherDealsListMenu"
]

def search_usages(word):
    usages = []
    for root, _, files in os.walk('.'):
        if '.git' in root or '__pycache__' in root or 'venv' in root:
            continue
        for file in files:
            if file.endswith('.py') and file not in ['find_menus.py']:
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if re.search(r'\b' + re.escape(word) + r'\b', line):
                                if not re.match(r'^\s*class\s+' + re.escape(word) + r'\b', line):
                                    usages.append(f"{os.path.join(root, file)}:{i+1}")
                except:
                    pass
    return usages

for c in classes:
    u = search_usages(c)
    if len(u) == 0:
        print(f"TRULY DEAD: {c}")
    else:
        print(f"USED {c} in: {u}")
