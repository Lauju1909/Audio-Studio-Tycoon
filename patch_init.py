import re

with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = "from .office import HRMenu, HireMenu, FireMenu, EmployeeOverviewMenu, TrainingEmployeeSelectMenu, TrainingCourseSelectMenu, TeambuildingMenu"
replace = target + ", OfficePerksMenu, HeadhuntingEventMenu"
content = content.replace(target, replace)

target_all = '    "HRMenu", "HireMenu", "FireMenu", "EmployeeOverviewMenu", "TrainingEmployeeSelectMenu", "TrainingCourseSelectMenu", "TeambuildingMenu",'
replace_all = target_all + '\n    "OfficePerksMenu", "HeadhuntingEventMenu",'
content = content.replace(target_all, replace_all)

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('menus/__init__.py updated')
