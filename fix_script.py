
def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f'Failed to find: {old} in {filepath}')
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Fix business.py: loan double subtraction and live_services check
replacements_business = [
    (
        "self.game_state.money -= amount_to_pay\n            self.game_state.track_expense(\"loan_repayment\", amount_to_pay)",
        "self.game_state.track_expense(\"loan_repayment\", amount_to_pay)"
    ),
    (
        "if self.game_state.get_calendar_year() >= 2010:",
        "if self.game_state.is_feature_unlocked(\"live_services\"):"
    ),
]
replace_in_file('menus/business.py', replacements_business)

# 2. Fix subscription.py: AudioPass unlock
old_sub = '''        if gs.year < 2015:
            if hasattr(self.audio, 'play_sound'):
                self.options.append({'text': 'AudioPass (Gesperrt bis 2015)', 'action': lambda: None})'''

new_sub = '''        if not gs.is_feature_unlocked("subscription_vault"):
            from game_data import FEATURE_UNLOCKS
            year = FEATURE_UNLOCKS["subscription_vault"].get("year", "???") if "subscription_vault" in FEATURE_UNLOCKS else 2015
            if hasattr(self.audio, 'play_sound'):
                self.options.append({'text': f'AudioPass (Gesperrt bis {year})', 'action': lambda: None})'''

# Wait, the exact string in subscription.py might differ slightly. Let's do it with regex or be more robust.
