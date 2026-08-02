
from logic import GameState
from menus.business import MerchMenu

class MockAudio:
    def __init__(self):
        self.spoken = []
        self.sounds = []
    def speak(self, text, interrupt=True):
        self.spoken.append(text)
    def play_sound(self, sound):
        self.sounds.append(sound)

state = GameState()
state.money = 1000000
audio = MockAudio()
menu = MerchMenu(audio, state)

menu.announce_entry()
print("Options:")
for opt in menu.options:
    print(opt['text'])
print("Test OK")
