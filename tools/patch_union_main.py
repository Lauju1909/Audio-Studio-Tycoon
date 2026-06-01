with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('InfluencerEventMenu,', 'InfluencerEventMenu, UnionEventMenu,')
text = text.replace('"InfluencerEventMenu",', '"InfluencerEventMenu", "UnionEventMenu",')

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('main.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('InfluencerEventMenu,', 'InfluencerEventMenu, UnionEventMenu,')
text = text.replace('"influencer_event_menu": lambda: InfluencerEventMenu(audio, state),', '"influencer_event_menu": lambda: InfluencerEventMenu(audio, state),\n        "union_event_menu": lambda: UnionEventMenu(audio, state),')

# Add the main.py transition
transition = """                # Headhunting Event"""
new_transition = """                # Union Event
                if getattr(state, "pending_union_event", None) and current_key != "union_event_menu":
                    current_key = "union_event_menu"
                    current_menu = menu_factories[current_key]()
                    current_menu.announce_entry()

                # Headhunting Event"""
text = text.replace(transition, new_transition)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched __init__ and main.py.")
