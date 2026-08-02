import os
import re

vulture_output = """
logic.py:859: unused method 'can_start_development' (60% confidence)
logic.py:922: unused method 'start_port_project' (60% confidence)
logic.py:973: unused method 'start_merch_campaign' (60% confidence)
logic.py:1033: unused method 'start_manufacturing_job' (60% confidence)
logic.py:1984: unused method '_generate_industry_news' (60% confidence)
logic.py:2016: unused method 'generate_candidate' (60% confidence)
logic.py:2058: unused method 'pay_salaries' (60% confidence)
logic.py:2098: unused method 'release_patch' (60% confidence)
logic.py:2107: unused method 'release_dlc' (60% confidence)
logic.py:2122: unused method 'release_mmo_update' (60% confidence)
logic.py:2267: unused method 'get_status_text' (60% confidence)
logic.py:2388: unused method 'create_engine' (60% confidence)
logic.py:2399: unused method 'get_researchable_topics' (60% confidence)
logic.py:2403: unused method 'get_researchable_genres' (60% confidence)
logic.py:2407: unused method 'get_researchable_audiences' (60% confidence)
logic.py:2411: unused method 'get_researchable_technologies' (60% confidence)
logic.py:2454: unused method 'can_upgrade_office' (60% confidence)
logic.py:2457: unused method 'upgrade_office' (60% confidence)
logic.py:2460: unused method 'get_office_info' (60% confidence)
logic.py:2579: unused method 'generate_publisher_deals' (60% confidence)
logic.py:2613: unused method 'get_active_licenses' (60% confidence)
logic.py:3178: unused method 'train_employee' (60% confidence)
logic.py:3211: unused method 'is_bankrupt' (60% confidence)
logic.py:3235: unused method 'generate_trend' (60% confidence)
logic.py:4267: unused method 'produce_physical_copies' (60% confidence)
logic.py:4296: unused method 'build_server_room' (60% confidence)
logic.py:4306: unused method 'expand_server_capacity' (60% confidence)
logic.py:4315: unused method 'apply_mmo_update' (60% confidence)
logic.py:4609: unused method 'get_office_item' (60% confidence)
logic.py:4941: unused method 'get_yearly_report' (60% confidence)
logic.py:4974: unused method '_send_monthly_bank_statement' (60% confidence)
logic.py:5066: unused method 'place_office_room' (60% confidence)
logic.py:5089: unused method 'buy_office_furniture' (60% confidence)
logic.py:5110: unused method 'expand_office_grid' (60% confidence)
logic.py:5128: unused method 'delete_bank_statement' (60% confidence)
logic.py:5243: unused method '_process_streaming_platform_monthly' (60% confidence)
logic.py:5307: unused function 'update_game_state' (60% confidence)
"""

methods = []
for line in vulture_output.strip().split('\n'):
    if "unused method" in line or "unused function" in line:
        method = line.split("'")[1]
        methods.append(method)

def count_occurrences(word):
    count = 0
    for root, _, files in os.walk('.'):
        if '.git' in root or '__pycache__' in root or 'venv' in root:
            continue
        for file in files:
            if file.endswith('.py') and file not in ['clean.py', 'clean_regex.py', 'find_truly_dead.py']:
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Count whole word occurrences
                        count += len(re.findall(r'\b' + re.escape(word) + r'\b', content))
                except:
                    pass
    return count

truly_dead = []
for m in methods:
    c = count_occurrences(m)
    if c <= 1:
        truly_dead.append(m)

print("Truly dead methods:")
for td in truly_dead:
    print(td)
