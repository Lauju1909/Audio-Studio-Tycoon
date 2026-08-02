
with open('menus/business.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        add_locked_feature("subscription_vault", self.game_state.get_text('service_manage_subscription'), lambda: "subscription_service_menu")
        add_locked_feature("cloud_gaming", self.game_state.get_text('cloud_gaming_title', default="Cloud Gaming Service"), lambda: "cloud_gaming_menu")"""

replacement = """        add_locked_feature("subscription_vault", self.game_state.get_text('service_manage_subscription'), lambda: "subscription_service_menu")
        add_locked_feature("cloud_gaming", self.game_state.get_text('cloud_gaming_title', default="Cloud Gaming Service"), lambda: "cloud_gaming_menu")
        add_locked_feature("transmedia", "Film- & Serienrechte (Transmedia)", lambda: "transmedia_menu")"""

if target in content:
    content = content.replace(target, replacement)
    with open('menus/business.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched ServiceMenu for transmedia button")
else:
    print("Could not find target in ServiceMenu")
