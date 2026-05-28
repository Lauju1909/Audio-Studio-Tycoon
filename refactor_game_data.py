import re

with open('game_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'START_YEAR\s*=\s*1930', 'START_YEAR = 1970', content)

def year_replacer(match):
    prop = match.group(1)
    week_str = match.group(2)
    try:
        week = int(week_str)
        year = 1930 + (week // 48)
        if 'end_week' in prop:
            return f'\"end_year\": {year}'
        else:
            return f'\"unlock_year\": {year}'
    except:
        return match.group(0)

content = re.sub(r'\"(available_week|end_week)\":\s*(\d+)', year_replacer, content)

def math_replacer(match):
    prop = match.group(1)
    expr = match.group(2)
    try:
        val = eval(expr, {'WEEKS_PER_YEAR': 48})
        year = 1930 + (val // 48)
        prop_name = 'end_year' if 'end' in prop else 'unlock_year'
        return f'\"{prop_name}\": {year}'
    except Exception as e:
        return match.group(0)

content = re.sub(r'\"(week|unlock_week|available_week|end_week)\":\s*([0-9\s\*\+WEEKS_PER_YEAR]+)', math_replacer, content)

with open('game_data_new.py', 'w', encoding='utf-8') as f:
    f.write(content)
