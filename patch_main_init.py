with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'ShareholderMenu' not in content:
    content = content.replace('GOTYMenu,', 'GOTYMenu, ShareholderMenu,')
    content = content.replace('"goty_menu": lambda: GOTYMenu(audio, state),', '"goty_menu": lambda: GOTYMenu(audio, state),\n        "shareholder_meeting": lambda: ShareholderMenu(audio, state),')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'ShareholderMenu' not in content:
    content = content.replace('GOTYMenu,', 'GOTYMenu, ShareholderMenu,')

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patched main.py and menus/__init__.py")
