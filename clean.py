import ast
import astor

vulture_output = """
logic.py:62: unused attribute 'stress_level' (60% confidence)
logic.py:114: unused attribute 'mail_client' (60% confidence)
logic.py:137: unused attribute 'accrued_salaries' (60% confidence)
logic.py:160: unused attribute 'active_expo_hype' (60% confidence)
logic.py:235: unused attribute 'has_union' (60% confidence)
logic.py:241: unused attribute 'current_production_draft' (60% confidence)
logic.py:261: unused attribute 'key_cancel' (60% confidence)
logic.py:282: unused attribute 'background_dev_active' (60% confidence)
logic.py:300: unused attribute 'active_tutorial' (60% confidence)
logic.py:301: unused attribute 'tutorial_step_index' (60% confidence)
logic.py:542: unused attribute 'difficulty_trend' (60% confidence)
logic.py:566: unused attribute 'game_over' (60% confidence)
logic.py:567: unused attribute 'game_over_reason' (60% confidence)
logic.py:584: unused attribute 'aaa_event_triggered' (60% confidence)
logic.py:799: unused attribute 'founding_week' (60% confidence)
logic.py:859: unused method 'can_start_development' (60% confidence)
logic.py:922: unused method 'start_port_project' (60% confidence)
logic.py:973: unused method 'start_merch_campaign' (60% confidence)
logic.py:1033: unused method 'start_manufacturing_job' (60% confidence)
logic.py:1647: unused attribute 'total_sales' (60% confidence)
logic.py:1653: unused attribute 'player_profit' (60% confidence)
logic.py:1984: unused method '_generate_industry_news' (60% confidence)
logic.py:2016: unused method 'generate_candidate' (60% confidence)
logic.py:2058: unused method 'pay_salaries' (60% confidence)
logic.py:2064: unused attribute 'accrued_salaries' (60% confidence)
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
logic.py:2983: unused attribute 'pirated_copies' (60% confidence)
logic.py:3178: unused method 'train_employee' (60% confidence)
logic.py:3194: unused attribute 'trait_learned' (60% confidence)
logic.py:3211: unused method 'is_bankrupt' (60% confidence)
logic.py:3235: unused method 'generate_trend' (60% confidence)
logic.py:3420: unused attribute 'selected_option' (60% confidence)
logic.py:3932: unused attribute 'total_sales' (60% confidence)
logic.py:3934: unused attribute 'player_profit' (60% confidence)
logic.py:3977: unused attribute 'server_cost_per_10k' (60% confidence)
logic.py:4267: unused method 'produce_physical_copies' (60% confidence)
logic.py:4296: unused method 'build_server_room' (60% confidence)
logic.py:4306: unused method 'expand_server_capacity' (60% confidence)
logic.py:4315: unused method 'apply_mmo_update' (60% confidence)
logic.py:4493: unused attribute 'training_skill_boost' (60% confidence)
logic.py:4609: unused method 'get_office_item' (60% confidence)
logic.py:4799: unused attribute 'weeks_running' (60% confidence)
logic.py:4941: unused method 'get_yearly_report' (60% confidence)
logic.py:4974: unused method '_send_monthly_bank_statement' (60% confidence)
logic.py:5046: unused attribute 'total_bugs_fixed' (60% confidence)
logic.py:5066: unused method 'place_office_room' (60% confidence)
logic.py:5089: unused method 'buy_office_furniture' (60% confidence)
logic.py:5110: unused method 'expand_office_grid' (60% confidence)
logic.py:5128: unused method 'delete_bank_statement' (60% confidence)
logic.py:5243: unused method '_process_streaming_platform_monthly' (60% confidence)
logic.py:5307: unused function 'update_game_state' (60% confidence)
"""

methods_to_remove = set()
for line in vulture_output.strip().split('\n'):
    if "unused method" in line or "unused function" in line:
        methods_to_remove.add(line.split("'")[1])

print(f"Removing methods: {methods_to_remove}")

class MethodRemover(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        if node.name in methods_to_remove:
            return None
        self.generic_visit(node)
        return node

with open('logic.py', 'r', encoding='utf-8') as f:
    code = f.read()

tree = ast.parse(code)
remover = MethodRemover()
tree = remover.visit(tree)

with open('logic.py', 'w', encoding='utf-8') as f:
    f.write(astor.to_source(tree))
    
print("Cleaned logic.py")
