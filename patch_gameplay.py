
with open('menus/gameplay.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        options.extend([
            {'text': self.game_state.get_text('hr_menu'), 'action': lambda: "hr_menu"},
            {'text': self.game_state.get_text('research_menu'), 'action': lambda: "research_menu"},
            {'text': self.game_state.get_text('office_menu'), 'action': lambda: "office_menu"},
            {'text': self.game_state.get_text('email_inbox_status', total=total_emails, unread=unread_emails), 'action': lambda: "email_inbox"},
            {'text': self.game_state.get_text('community_menu_title'), 'action': lambda: "community_menu"},
            {'text': self.game_state.get_text('hardware_menu_title'), 'action': lambda: "hardware_menu"},
            {'text': self.game_state.get_text('esports_menu_title', default='E-Sports Zentrale'), 'action': lambda: "esports_menu"},
            {'text': self.game_state.get_text('soundcon_menu_title', default='SoundCon Messe'), 'action': lambda: "soundcon_menu"},
            {'text': self.game_state.get_text('label_menu_title', default='Soundtrack-Label'), 'action': lambda: "label_menu"},
            {'text': self.game_state.get_text('merch_menu_title', default='Merchandising'), 'action': lambda: "merch_menu"},
            {'text': self.game_state.get_text('creator_menu_title', default='Content Creators Sponsern'), 'action': lambda: "creator_menu"},
            {'text': self.game_state.get_text('streaming_platform_menu_title', default='Streaming-Plattform'), 'action': lambda: "streaming_platform_menu"},
            {'text': self.game_state.get_text('jingle_menu_title'), 'action': lambda: "jingle_name_input"},
            {'text': self.game_state.get_text('bank_menu'), 'action': lambda: "bank_menu"},
            {'text': self.game_state.get_text('service_menu'), 'action': lambda: "service_menu"},
            {'text': self.game_state.get_text('game_porting_title', default='Spiel Portieren'), 'action': lambda: "game_porting_menu"},
            {'text': self.game_state.get_text('active_games_menu_title', default="Aktive Spiele & Einnahmen"), 'action': lambda: "active_games_menu"},
            {'text': self.game_state.get_text('save_menu'), 'action': lambda: "save_menu"},
            {'text': self.game_state.get_text('menu_settings'), 'action': lambda: "settings_menu_ingame"},
            {'text': self.game_state.get_text('menu_quit'), 'action': lambda: "main_menu"}
        ])"""

replacement = """        options.extend([
            {'text': self.game_state.get_text('hr_menu'), 'action': lambda: "hr_menu"},
            {'text': self.game_state.get_text('research_menu'), 'action': lambda: "research_menu"},
            {'text': self.game_state.get_text('office_menu'), 'action': lambda: "office_menu"},
            {'text': self.game_state.get_text('email_inbox_status', total=total_emails, unread=unread_emails), 'action': lambda: "email_inbox"},
            {'text': self.game_state.get_text('community_menu_title'), 'action': lambda: "community_menu"},
            {'text': self.game_state.get_text('hardware_menu_title'), 'action': lambda: "hardware_menu"}
        ])
        
        # Locked features
        def add_locked_feature(feature_id, text, action):
            if self.game_state.is_feature_unlocked(feature_id):
                options.append({'text': text, 'action': action})
            else:
                from game_data import FEATURE_UNLOCKS
                if feature_id in FEATURE_UNLOCKS:
                    options.append({'text': f"{text} (Ab {FEATURE_UNLOCKS[feature_id].get('year', '???')})", 'action': lambda: None})
                
        add_locked_feature("esports", self.game_state.get_text('esports_menu_title', default='E-Sports Zentrale'), lambda: "esports_menu")
        add_locked_feature("soundcon", self.game_state.get_text('soundcon_menu_title', default='SoundCon Messe'), lambda: "soundcon_menu")
        add_locked_feature("soundtrack_label", self.game_state.get_text('label_menu_title', default='Soundtrack-Label'), lambda: "label_menu")
        add_locked_feature("merch", self.game_state.get_text('merch_menu_title', default='Merchandising'), lambda: "merch_menu")
        add_locked_feature("creator_sponsorship", self.game_state.get_text('creator_menu_title', default='Content Creators Sponsern'), lambda: "creator_menu")
        add_locked_feature("streaming_platform", self.game_state.get_text('streaming_platform_menu_title', default='Streaming-Plattform'), lambda: "streaming_platform_menu")
        
        options.extend([
            {'text': self.game_state.get_text('jingle_menu_title'), 'action': lambda: "jingle_name_input"},
            {'text': self.game_state.get_text('bank_menu'), 'action': lambda: "bank_menu"},
            {'text': self.game_state.get_text('service_menu'), 'action': lambda: "service_menu"},
            {'text': self.game_state.get_text('game_porting_title', default='Spiel Portieren'), 'action': lambda: "game_porting_menu"},
            {'text': self.game_state.get_text('active_games_menu_title', default="Aktive Spiele & Einnahmen"), 'action': lambda: "active_games_menu"},
            {'text': self.game_state.get_text('save_menu'), 'action': lambda: "save_menu"},
            {'text': self.game_state.get_text('menu_settings'), 'action': lambda: "settings_menu_ingame"},
            {'text': self.game_state.get_text('menu_quit'), 'action': lambda: "main_menu"}
        ])"""

if target in content:
    content = content.replace(target, replacement)
    with open('menus/gameplay.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched menus/gameplay.py!")
else:
    print("Could not find target block in menus/gameplay.py!")
