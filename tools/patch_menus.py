with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('AddMtxMenu,', 'AddMtxMenu, MovieDealMenu,')
text = text.replace('"AddMtxMenu",', '"AddMtxMenu", "MovieDealMenu",')

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('main.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('AddMtxMenu,', 'AddMtxMenu, MovieDealMenu,')
text = text.replace('"add_mtx_menu": lambda: AddMtxMenu(audio, state),', '"add_mtx_menu": lambda: AddMtxMenu(audio, state),\n        "movie_deal_menu": lambda: MovieDealMenu(audio, state),')

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched.")
