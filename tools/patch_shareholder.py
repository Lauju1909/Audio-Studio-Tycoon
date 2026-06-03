import codecs

lines = []
with codecs.open('menus/gameplay.py', 'r', 'utf-8') as f:
    lines = f.readlines()

new_block = """class ShareholderMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        game_state.pending_shareholder_meeting = False
        
        target = getattr(game_state, 'shareholder_target', 0)
        target_met = game_state.money >= target
        
        if target_met:
            game_state.shareholder_trust = min(100, getattr(game_state, 'shareholder_trust', 100) + 10)
            msg = game_state.get_text('shareholder_happy', default="Aktionaere sind gluecklich! Umsatzziele erreicht.")
            audio.play_sound("cheer")
        else:
            game_state.shareholder_trust = getattr(game_state, 'shareholder_trust', 100) - 25
            msg = game_state.get_text('shareholder_angry', default="Aktionaere sind unzufrieden! Ziele verfehlt.")
            audio.play_sound("error")
            
        game_state.shareholder_target = game_state.money * 1.10 # Neues Ziel
        
        if game_state.shareholder_trust <= 0:
            msg += " " + game_state.get_text('shareholder_fired', default="Du wurdest als CEO entlassen! GAME OVER.")
            options = [{'text': "Game Over", 'action': lambda: "main_menu"}]
        else:
            msg += " " + game_state.get_text('shareholder_trust_msg', trust=game_state.shareholder_trust, default=f"Vertrauen liegt bei {game_state.shareholder_trust}%.")
            options = [{'text': "Verstanden", 'action': lambda: "game_menu"}]
            
        super().__init__(game_state.get_text('shareholder_title', default='Jahreshauptversammlung'), options, audio, game_state)
        self.audio.speak(msg, interrupt=True)
"""

start = -1
end = -1
for i, line in enumerate(lines):
    if 'class ShareholderMenu(Menu):' in line:
        start = i
    if start != -1 and 'self.audio.speak(f"Shareholder Meeting' in line:
        end = i + 1
        break

if start != -1 and end != -1:
    lines = lines[:start] + [new_block] + lines[end:]

with codecs.open('menus/gameplay.py', 'w', 'utf-8') as f:
    f.writelines(lines)
