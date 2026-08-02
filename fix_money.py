import re
import os

def fix_file(f):
    try:
        with open(f, encoding='utf-8') as file:
            c = file.read()
    except Exception:
        return
    
    # Replace cases where self.money += <amount> is followed immediately by track_income
    c = re.sub(r'self(\.state)?\.money \+= ([^\n]+)\n(\s+)self(\.state)?\.track_income\(([^)]+)\)', r'\3self\4.track_income(\5)', c)
    # Replace cases where self.money -= <amount> is followed immediately by track_expense
    c = re.sub(r'self(\.state)?\.money -= ([^\n]+)\n(\s+)self(\.state)?\.track_expense\(([^)]+)\)', r'\3self\4.track_expense(\5)', c)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(c)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and file not in ['fix_money.py', 'gamestate.py', 'snippets.py']:
            fix_file(os.path.join(root, file))
