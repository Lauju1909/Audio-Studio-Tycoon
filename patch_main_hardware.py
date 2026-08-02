
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '"hardware_type_select":' not in content:
    import_target = "from menus.hardware import ("
    import_replace = "from menus.hardware import (\n    HardwareTypeSelectMenu,"
    if import_target in content:
        content = content.replace(import_target, import_replace)
    
    route_target = '        "hardware_menu": lambda: HardwareLabMenu(audio, state),'
    route_replace = '        "hardware_menu": lambda: HardwareLabMenu(audio, state),\n        "hardware_type_select": lambda: HardwareTypeSelectMenu(audio, state),'
    if route_target in content:
        content = content.replace(route_target, route_replace)
        
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added hardware_type_select route to main.py")
else:
    print("Already added")
