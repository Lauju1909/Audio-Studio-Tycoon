class MetaverseMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("AudioVerse", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        gs = self.game_state
        
        if getattr(gs, 'metaverse_burst', False):
            self.title = "AudioVerse (OFFLINE)"
            self.options.append({'text': "Das AudioVerse ist gecrasht. Geld ist weg.", 'action': lambda: "service_menu"})
            return
            
        self.title = f"AudioVerse (Investiert: ${gs.metaverse_investment:,.0f} | Wert: ${gs.metaverse_land_value:,.0f})"
        
        # Investieren
        if gs.money >= 500000:
            self.options.append({'text': "Investiere $500k in AudioVerse-Land", 'action': self._invest})
        
        # Verkaufen
        if gs.metaverse_land_value > 0:
            self.options.append({'text': f"Alles verkaufen (Gewinn mitnehmen)", 'action': self._sell})
            
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "service_menu"})

    def _invest(self):
        gs = self.game_state
        if gs.money >= 500000:
            gs.money -= 500000
            gs.track_expense("metaverse", 500000)
            gs.metaverse_investment += 500000
            gs.metaverse_land_value += 500000
            self.audio.play_sound("buy")
            self._update_options()
        return "metaverse_menu"

    def _sell(self):
        gs = self.game_state
        if gs.metaverse_land_value > 0:
            gs.money += gs.metaverse_land_value
            gs.metaverse_investment = 0
            gs.metaverse_land_value = 0
            gs.metaverse_weeks_active = 0
            self.audio.play_sound("money")
            self._update_options()
        return "metaverse_menu"
