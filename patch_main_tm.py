
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        "acquisition_menu": lambda: AcquisitionMenu(audio, state),"""

replacement = """        "acquisition_menu": lambda: AcquisitionMenu(audio, state),
        "transmedia_menu": lambda: __import__('menus.business', fromlist=['']).TransmediaMenu(audio, state),
        "transmedia_deal_menu": lambda: __import__('menus.business', fromlist=['']).TransmediaDealMenu(audio, state),"""

if target in content:
    content = content.replace(target, replacement)
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched main.py routing")
else:
    print("Could not find routing target in main.py")
