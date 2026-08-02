
with open('menus/business.py', 'r', encoding='utf-8') as f:
    content = f.read()

with open('add_metaverse_menu.py', 'r', encoding='utf-8') as f:
    metaverse_code = f.read()

if "class MetaverseMenu" not in content:
    content += "\n\n" + metaverse_code

# Add to ServiceMenu
service_target = "{'text': gs.get_text('back'), 'action': lambda: \"game_menu\"}"
service_replace = """{'text': "Das AudioVerse (Metaverse)", 'action': lambda: "metaverse_menu"} if gs.is_feature_unlocked("metaverse") else None,
            {'text': gs.get_text('back'), 'action': lambda: "game_menu"}"""

if service_target in content:
    content = content.replace(service_target, service_replace)
    # clean up None options
    cleanup_target = "self.options = ["
    if "self.options = [opt for opt in self.options if opt is not None]" not in content:
        # We need to filter options in _update_options of ServiceMenu
        # ServiceMenu is at the top of the file
        content = content.replace(
            "self.options = [",
            "opts = ["
        )
        content = content.replace(
            "            {'text': gs.get_text('back'), 'action': lambda: \"game_menu\"}\n        ]",
            "            {'text': gs.get_text('back'), 'action': lambda: \"game_menu\"}\n        ]\n        self.options = [o for o in opts if o is not None]"
        )

with open('menus/business.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added MetaverseMenu and linked in ServiceMenu")
