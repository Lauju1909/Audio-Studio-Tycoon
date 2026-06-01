with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('MovieDealMenu,', 'MovieDealMenu, AntiCheatMenu,')
text = text.replace('"MovieDealMenu",', '"MovieDealMenu", "AntiCheatMenu",')

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('main.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('MovieDealMenu,', 'MovieDealMenu, AntiCheatMenu,')
text = text.replace('"movie_deal_menu": lambda: MovieDealMenu(audio, state),', '"movie_deal_menu": lambda: MovieDealMenu(audio, state),\n        "anti_cheat_menu": lambda: AntiCheatMenu(audio, state),')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched.")
