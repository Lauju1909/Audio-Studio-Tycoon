import os
import re

# 1. Update logic.py
with open('logic.py', 'r', encoding='utf-8') as f:
    logic_code = f.read()

interactive_qa_code = """
    def conduct_soundcon_qa_interactive(self, hype_bonus, prestige_bonus, fan_bonus) -> dict:
        if not self.active_soundcon:
            return {"success": False, "message": "soundcon_not_booked"}
        if self.active_soundcon.qa_rounds >= 3:
            return {"success": False, "message": "soundcon_qa_max"}
            
        self.active_soundcon.qa_rounds += 1
        
        # Manuell Bonus hinzufügen
        self.active_soundcon.hype_gained = getattr(self.active_soundcon, 'hype_gained', 0) + hype_bonus
        self.active_soundcon.fans_gained = getattr(self.active_soundcon, 'fans_gained', 0) + fan_bonus
        self.active_soundcon.prestige_gained = getattr(self.active_soundcon, 'prestige_gained', 0) + prestige_bonus
        
        if hasattr(self, 'audio'):
            self.audio.play_sound('confirm')
            
        return {"success": True, "qa_round": self.active_soundcon.qa_rounds}
"""

if "conduct_soundcon_qa_interactive" not in logic_code:
    # Insert it before finish_soundcon
    logic_code = logic_code.replace("    def finish_soundcon(self) -> dict:", interactive_qa_code + "\n    def finish_soundcon(self) -> dict:")
    with open('logic.py', 'w', encoding='utf-8') as f:
        f.write(logic_code)

# 2. Update menus/events.py
with open('menus/events.py', 'r', encoding='utf-8') as f:
    events_code = f.read()

# Replace the action in SoundConMenu
old_qa_action = """            elif action == 'soundcon_qa':
                res = gs.conduct_soundcon_qa()
                if res['success']:
                    self.audio.speak(gs.get_text('soundcon_qa_done', round=res['qa_round']))
                    return 'soundcon_menu'
                else:
                    self.audio.speak(gs.get_text(res['message']))"""
                    
new_qa_action = """            elif action == 'soundcon_qa':
                res = gs.conduct_soundcon_qa() # Check if possible
                if res['success']:
                    # Revert qa_rounds increment because we will do it in interactive
                    gs.active_soundcon.qa_rounds -= 1
                    return 'soundcon_qa_menu'
                else:
                    self.audio.speak(gs.get_text(res['message']))"""

if "return 'soundcon_qa_menu'" not in events_code:
    events_code = events_code.replace(old_qa_action, new_qa_action)

menu_class_code = """
class SoundConQAMenu(Menu):
    \"\"\"Interaktives Q&A Menü für die SoundCon.\"\"\"
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.round_num = getattr(game_state.active_soundcon, 'qa_rounds', 0) + 1 if game_state.active_soundcon else 1
        
        import random
        self.q_idx = random.randint(1, 3)
        question = self.game_state.get_text(f'soundcon_qa_question_{self.q_idx}')
        
        options = []
        if self.q_idx == 1:
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_1_1'), 'action': lambda: self._answer(15, 0, 0, 'hype')})
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_1_2'), 'action': lambda: self._answer(2, 5, 0, 'neutral')})
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_1_3'), 'action': lambda: self._answer(0, 0, 0, 'neutral')})
        elif self.q_idx == 2:
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_2_1'), 'action': lambda: self._answer(20, -5, 0, 'hype')})
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_2_2'), 'action': lambda: self._answer(5, 10, 500, 'prestige')})
        elif self.q_idx == 3:
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_3_1'), 'action': lambda: self._answer(25, 0, 0, 'hype')})
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_3_2'), 'action': lambda: self._answer(5, 15, 0, 'prestige')})
            
        super().__init__(question, options, audio, game_state)
        
    def _answer(self, hype, prestige, fans, result_type):
        res = self.game_state.conduct_soundcon_qa_interactive(hype, prestige, fans)
        if res['success']:
            if result_type == 'hype':
                msg = self.game_state.get_text('soundcon_qa_result_hype', hype=hype)
            elif result_type == 'prestige':
                msg = self.game_state.get_text('soundcon_qa_result_prestige', prestige=prestige, fans=fans)
            else:
                msg = self.game_state.get_text('soundcon_qa_result_neutral', fans=fans)
                
            self.audio.speak(msg)
        return 'soundcon_menu'
"""

if "class SoundConQAMenu(Menu):" not in events_code:
    events_code = events_code + "\n" + menu_class_code
    with open('menus/events.py', 'w', encoding='utf-8') as f:
        f.write(events_code)

# 3. Update menus/__init__.py
with open('menus/__init__.py', 'r', encoding='utf-8') as f:
    init_code = f.read()

if "SoundConQAMenu" not in init_code:
    init_code = init_code.replace("SoundConHistoryMenu,", "SoundConHistoryMenu, SoundConQAMenu,")
    init_code = init_code.replace('"SoundConHistoryMenu",', '"SoundConHistoryMenu", "SoundConQAMenu",')
    with open('menus/__init__.py', 'w', encoding='utf-8') as f:
        f.write(init_code)

# 4. Update main.py
with open('main.py', 'r', encoding='utf-8') as f:
    main_code = f.read()

if "soundcon_qa_menu" not in main_code:
    main_code = main_code.replace('"soundcon_history_menu": lambda: SoundConHistoryMenu(audio, state),', '"soundcon_history_menu": lambda: SoundConHistoryMenu(audio, state),\n        "soundcon_qa_menu": lambda: SoundConQAMenu(audio, state),')
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_code)

print("Patch applied.")
