
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '"metaverse_menu": lambda: MetaverseMenu(audio, state),' not in content:
    # First, need to import MetaverseMenu
    import_target = "from menus.business import ("
    import_replace = "from menus.business import (\n    MetaverseMenu,"
    if import_target in content:
        content = content.replace(import_target, import_replace)
    
    # Then add the route
    route_target = '        "transmedia_deal_menu": lambda: TransmediaDealMenu(audio, state),'
    route_replace = '        "transmedia_deal_menu": lambda: TransmediaDealMenu(audio, state),\n        "metaverse_menu": lambda: MetaverseMenu(audio, state),'
    if route_target in content:
        content = content.replace(route_target, route_replace)
        
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added metaverse_menu route to main.py")
else:
    print("Already added")
