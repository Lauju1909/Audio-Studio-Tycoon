with open('menus/gameplay.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_menu = """
class InfluencerEventMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.event_data = getattr(game_state, 'pending_influencer_event', None)
        game_name = self.event_data["game_name"] if self.event_data else "Unbekanntes Spiel"
        
        super().__init__(self.game_state.get_text('influencer_event_title', default="INFLUENCER-SKANDAL!"), [], audio, game_state)
        self.audio.speak(self.game_state.get_text('influencer_event_desc', game=game_name, default=f"Boss! Unser gesponserter Streamer hat in {game_name} live vor Millionen Zuschauern Cheats verwendet und das Spiel beleidigt! Die PR ist ein Desaster. Was tun wir?"), interrupt=True)
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('error')
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('influencer_opt_1', default="Öffentlich entschuldigen (-Fans, rettet Image)"), 'action': self._apologize},
            {'text': self.game_state.get_text('influencer_opt_2', default="Fristlos feuern & klagen (-Viel Geld, bewahrt Ehre)"), 'action': self._fire},
            {'text': self.game_state.get_text('influencer_opt_3', default="Ignorieren (Riskant, kann Langzeit-Verkäufe ruinieren)"), 'action': self._ignore}
        ]

    def _apologize(self):
        self.game_state.fans = max(0, self.game_state.fans - 25000)
        self.audio.speak(self.game_state.get_text('influencer_res_1', default="Wir haben uns entschuldigt. Die Presse beruhigt sich, aber einige Hardcore-Fans sind weg."))
        self._clear_event()
        return "game_menu"

    def _fire(self):
        fine = 250000
        self.game_state.money -= fine
        self.game_state.track_expense("other", fine)
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('cash')
        self.audio.speak(self.game_state.get_text('influencer_res_2', cost=fine, default=f"Streamer gefeuert! Vertragsstrafen kosten uns {fine} €, aber die Gamer respektieren uns dafür!"))
        self._clear_event()
        return "game_menu"

    def _ignore(self):
        import random
        if random.random() < 0.6:
            game_name = self.event_data["game_name"] if self.event_data else ""
            for g in self.game_state.game_history:
                if g.name == game_name:
                    g.sales = int(g.sales * 0.5)
                    g.is_active = False
            self.game_state.fans = max(0, int(self.game_state.fans * 0.8))
            self.audio.speak(self.game_state.get_text('influencer_res_3_bad', default="Das Ignorieren war ein Fehler! Ein gigantischer Shitstorm zerstört das Spiel und wir verlieren massig Fans!"))
        else:
            self.audio.speak(self.game_state.get_text('influencer_res_3_good', default="Glück gehabt. Das Internet hat den Skandal in wenigen Tagen vergessen. Keine Konsequenzen!"))
        self._clear_event()
        return "game_menu"

    def _clear_event(self):
        self.game_state.pending_influencer_event = None
        if self.event_data and "sponsorship" in self.event_data:
            s = self.event_data["sponsorship"]
            if s in self.game_state.active_sponsorships:
                self.game_state.streamer_hype_multi /= s["boost"]
                self.game_state.active_sponsorships.remove(s)

"""

text = text.replace("class ExpoMenu(Menu):", new_menu + "\nclass ExpoMenu(Menu):")

with open('menus/gameplay.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Injected InfluencerEventMenu.")
