
with open('menus/business.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """class ServiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('service_menu')
        options = []
        if self.game_state.get_calendar_year() >= 2000:
            options.append({'text': self.game_state.get_text('service_manage_subscription'), 'action': lambda: "subscription_service_menu"})
            options.append({'text': self.game_state.get_text('cloud_gaming_title', default="Cloud Gaming Service"), 'action': lambda: "cloud_gaming_menu"})
        options.extend([
            {'text': self.game_state.get_text('game_service_options'), 'action': lambda: "game_service_options"},
            {'text': self.game_state.get_text('contract_work_menu_title', default="Auftragsarbeiten"), 'action': lambda: "contract_work_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ])
        super().__init__(title, options, audio, game_state)"""

replacement = """class ServiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('service_menu')
        options = []
        
        def add_locked_feature(feature_id, text, action):
            if self.game_state.is_feature_unlocked(feature_id):
                options.append({'text': text, 'action': action})
            else:
                from game_data import FEATURE_UNLOCKS
                if feature_id in FEATURE_UNLOCKS:
                    options.append({'text': f"{text} (Ab {FEATURE_UNLOCKS[feature_id].get('year', '???')})", 'action': lambda: None})
        
        add_locked_feature("subscription_vault", self.game_state.get_text('service_manage_subscription'), lambda: "subscription_service_menu")
        add_locked_feature("cloud_gaming", self.game_state.get_text('cloud_gaming_title', default="Cloud Gaming Service"), lambda: "cloud_gaming_menu")
        
        options.extend([
            {'text': self.game_state.get_text('game_service_options'), 'action': lambda: "game_service_options"},
            {'text': self.game_state.get_text('contract_work_menu_title', default="Auftragsarbeiten"), 'action': lambda: "contract_work_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ])
        super().__init__(title, options, audio, game_state)"""

if target in content:
    content = content.replace(target, replacement)
    with open('menus/business.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched ServiceMenu in menus/business.py!")
else:
    print("Could not find ServiceMenu in menus/business.py!")
