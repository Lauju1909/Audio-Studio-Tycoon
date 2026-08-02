truly_dead = [
    "can_start_development",
    "start_port_project",
    "_generate_industry_news",
    "generate_candidate",
    "release_patch",
    "release_dlc",
    "release_mmo_update",
    "get_status_text",
    "get_researchable_topics",
    "get_researchable_genres",
    "get_researchable_audiences",
    "get_researchable_technologies",
    "can_upgrade_office",
    "get_office_info",
    "generate_publisher_deals",
    "get_active_licenses",
    "produce_physical_copies",
    "apply_mmo_update",
    "get_office_item",
    "get_yearly_report",
    "place_office_room",
    "buy_office_furniture",
    "expand_office_grid",
    "delete_bank_statement"
]

import re

with open('logic.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_indent = None
i = 0
while i < len(lines):
    line = lines[i]
    
    if skip_indent is not None:
        stripped = line.lstrip()
        if stripped and not stripped.startswith('#'):
            indent = len(line) - len(stripped)
            if indent <= skip_indent:
                skip_indent = None
            else:
                i += 1
                continue
        else:
            i += 1
            continue

    match = re.match(r'^(\s*)def\s+([a-zA-Z0-9_]+)\(', line)
    if match:
        method_name = match.group(2)
        if method_name in truly_dead:
            skip_indent = len(match.group(1))
            i += 1
            continue
            
    new_lines.append(line)
    i += 1

with open('logic.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Cleaned truly dead methods from logic.py!")
