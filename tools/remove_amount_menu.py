with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('SupportGiftCardAmountMenu,', '')
text = text.replace('SupportGiftCardAmountMenu', '')

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('main.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('SupportGiftCardAmountMenu,', '')
text = text.replace('SupportGiftCardAmountMenu', '')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(text)
