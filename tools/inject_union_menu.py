with open('menus/gameplay.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_menu = """
class UnionEventMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.event_data = getattr(game_state, 'pending_union_event', {"type": "formation"})
        
        if self.event_data["type"] == "formation":
            title = self.game_state.get_text('union_form_title', default="GEWERKSCHAFTS-GRÜNDUNG!")
            desc = self.game_state.get_text('union_form_desc', default="Boss, die miese Moral und der Stress haben das Fass zum Überlaufen gebracht. Die Mitarbeiter haben eine Gewerkschaft gegründet! Sie fordern sofortige Verhandlungen.")
        else:
            title = self.game_state.get_text('union_strike_title', default="STREIKDROHUNG!")
            desc = self.game_state.get_text('union_strike_desc', default="Die Gewerkschaft ist unzufrieden! Wenn wir nicht zahlen, legen sie ab morgen die Arbeit nieder. Was sollen wir tun?")
            
        super().__init__(title, [], audio, game_state)
        self.audio.speak(desc, interrupt=True)
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('error')
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('union_opt_1', default="Gehälter anpassen (+30% für alle, Moral steigt)"), 'action': self._raise_salaries},
            {'text': self.game_state.get_text('union_opt_2', default="Einmaliger Bonus (10k pro Mitarbeiter, keine Dauerlösung)"), 'action': self._pay_bonus},
            {'text': self.game_state.get_text('union_opt_3', default="Union-Busting betreiben (Feuert Rädelsführer, illegal & riskant)"), 'action': self._union_busting},
            {'text': self.game_state.get_text('union_opt_4', default="Ignorieren (STREIK!)"), 'action': self._ignore}
        ]

    def _raise_salaries(self):
        for emp in self.game_state.employees:
            emp.salary = int(emp.salary * 1.3)
            emp.morale = 100
        self.game_state.has_union = True
        self.audio.speak(self.game_state.get_text('union_res_1', default="Die Gehälter wurden erhöht. Die Mitarbeiter sind glücklich und die Arbeit geht weiter!"))
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('cash')
        self._clear_event()
        return "game_menu"

    def _pay_bonus(self):
        cost = len(self.game_state.employees) * 10000
        self.game_state.money -= cost
        self.game_state.track_expense("other", cost)
        for emp in self.game_state.employees:
            emp.morale = min(100, emp.morale + 30)
        self.game_state.has_union = True
        self.audio.speak(self.game_state.get_text('union_res_2', cost=cost, default=f"Ein Bonus von {cost} € wurde gezahlt. Sie sind vorerst ruhig."))
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('cash')
        self._clear_event()
        return "game_menu"

    def _union_busting(self):
        import random
        # Fire 1-2 employees
        fired_count = min(random.randint(1, 2), len(self.game_state.employees))
        for _ in range(fired_count):
            self.game_state.employees.pop(random.randrange(len(self.game_state.employees)))
        
        self.game_state.fans = max(0, self.game_state.fans - 50000)
        
        if random.random() < 0.5:
            self.game_state.has_union = False
            self.audio.speak(self.game_state.get_text('union_res_3_success', default="Rädelsführer gefeuert! Die Gewerkschaft ist zerschlagen, aber die Fans sind angewidert!"))
        else:
            self.game_state.has_union = True
            fine = 500000
            self.game_state.money -= fine
            self.game_state.track_expense("other", fine)
            self.audio.speak(self.game_state.get_text('union_res_3_fail', default="Union-Busting aufgeflogen! Strafzahlung von 500.000 €! Fans hassen uns und die Gewerkschaft bleibt!"))
        self._clear_event()
        return "game_menu"

    def _ignore(self):
        import random
        self.game_state.has_union = True
        self.game_state.strike_weeks_left = random.randint(3, 6)
        self.audio.speak(self.game_state.get_text('union_res_4', default="STREIK! Die gesamte Spieleentwicklung ruht und es kostet uns jede Woche ein Vermögen!"))
        self._clear_event()
        return "game_menu"

    def _clear_event(self):
        self.game_state.pending_union_event = None
        self.game_state.stress_level = 0.0

"""

text = text.replace("class ExpoMenu(Menu):", new_menu + "\nclass ExpoMenu(Menu):")

with open('menus/gameplay.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Injected UnionEventMenu.")
