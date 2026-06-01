with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('AAADevEventMenu,', 'AAADevEventMenu, InfluencerEventMenu,')
text = text.replace('"AAADevEventMenu",', '"AAADevEventMenu", "InfluencerEventMenu",')

with open('menus/__init__.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open('main.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('AAADevEventMenu,', 'AAADevEventMenu, InfluencerEventMenu,')
text = text.replace('"aaa_dev_event_menu": lambda: AAADevEventMenu(audio, state),', '"aaa_dev_event_menu": lambda: AAADevEventMenu(audio, state),\n        "influencer_event_menu": lambda: InfluencerEventMenu(audio, state),')

# Add the main.py transition
transition = """                # Headhunting Event"""
new_transition = """                # Influencer Event
                if getattr(state, "pending_influencer_event", None) and current_key != "influencer_event_menu":
                    current_key = "influencer_event_menu"
                    current_menu = menu_factories[current_key]()
                    current_menu.announce_entry()

                # Headhunting Event"""
text = text.replace(transition, new_transition)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patched __init__ and main.py.")
