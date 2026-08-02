
with open('menus/gameplay.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """            if not getattr(ap["project"], "used_ai_assets", False) and not is_engine:
                self.options.append({
                    'text': self.game_state.get_text('use_ai_assets', default="KI-Assets generieren (Risikoreich!)"),
                    'action': self._use_ai_assets
                })"""

replacement = """            if not getattr(ap["project"], "used_ai_assets", False) and not is_engine:
                if self.game_state.is_feature_unlocked("ai_tools"):
                    self.options.append({
                        'text': self.game_state.get_text('use_ai_assets', default="KI-Assets generieren (Risikoreich!)"),
                        'action': self._use_ai_assets
                    })
                else:
                    from game_data import FEATURE_UNLOCKS
                    if "ai_tools" in FEATURE_UNLOCKS:
                        self.options.append({
                            'text': f"{self.game_state.get_text('use_ai_assets', default='KI-Assets generieren (Risikoreich!)')} (Ab {FEATURE_UNLOCKS['ai_tools'].get('year', '???')})",
                            'action': lambda: None
                        })"""

if target in content:
    content = content.replace(target, replacement)
    with open('menus/gameplay.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched AI-Assets in menus/gameplay.py!")
else:
    print("Could not find AI-Assets option in menus/gameplay.py!")
