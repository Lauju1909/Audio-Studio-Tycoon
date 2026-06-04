import sys
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add to routing dict
if '"subsidiary_manage_menu"' not in content:
    content = content.replace('"acquisition_menu": lambda: AcquisitionMenu(audio, state),', '"acquisition_menu": lambda: AcquisitionMenu(audio, state),\n        "subsidiary_manage_menu": lambda: __import__(\'menus.business\', fromlist=[\'\']).SubsidiaryManagementMenu(audio, state),')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added to main.py")
