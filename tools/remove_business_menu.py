with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('BusinessMenu,', '')

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('main.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('BusinessMenu,', '')
if '"business_menu": lambda: BusinessMenu(audio, state),' in text:
    text = text.replace('"business_menu": lambda: BusinessMenu(audio, state),', '')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed BusinessMenu")
