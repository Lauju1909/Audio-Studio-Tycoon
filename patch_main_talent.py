
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        "transmedia_deal_menu": lambda: __import__('menus.business', fromlist=['']).TransmediaDealMenu(audio, state),"""

replacement = """        "transmedia_deal_menu": lambda: __import__('menus.business', fromlist=['']).TransmediaDealMenu(audio, state),
        "talent_tree_menu": lambda: __import__('menus.office', fromlist=['']).TalentTreeMenu(audio, state),
        "employee_talent_menu": lambda: __import__('menus.office', fromlist=['']).EmployeeTalentMenu(audio, state),"""

if target in content:
    content = content.replace(target, replacement)
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched main.py routing for talent trees")
else:
    print("Could not find target in main.py")
