from .base import Menu

class CryptoMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Web3 & Krypto (Play-to-Earn)", [], audio, game_state)
        
    def announce_entry(self):
        self._update_options()
        super().announce_entry()
        
    def _update_options(self):
        self.options = []
        cm = self.game_state.crypto_manager
        
        if self.game_state.get_calendar_year() < 2019:
            self.options.append({'text': 'Web3 & Krypto (Gesperrt bis 2019)', 'action': lambda: None})
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})
            return
            
        if not cm.ico_launched:
            self.options.append({'text': 'ICO starten (Initial Coin Offering) - Massiver Cash-Injektion', 'action': self._launch_ico})
        elif cm.crashed:
            self.options.append({'text': 'Ihr Coin ist gecrasht. Die Behoerden ermitteln.', 'action': lambda: None})
        else:
            self.options.append({'text': f"Coin-Preis: {cm.coin_price:.4f} EUR | Hype: {cm.hype_level:.1f}%", 'action': lambda: None})
            self.options.append({'text': 'Influencer bezahlen (1.000.000 EUR) - Hype pushen!', 'action': self._pump_coin})
            self.options.append({'text': 'ACHTUNG: Krypto-Markt ist extrem volatil. Ein Crash (Rug Pull) droht!', 'action': lambda: None})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})
        
    def _launch_ico(self):
        cm = self.game_state.crypto_manager
        success, msg = cm.launch_ico(self.game_state)
        if success:
            self.audio.play_sound("cash")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return "crypto_menu"
        
    def _pump_coin(self):
        cm = self.game_state.crypto_manager
        success, msg = cm.pump_coin(self.game_state)
        if success:
            self.audio.play_sound("confirm")
        else:
            self.audio.play_sound("error")
        self.audio.speak(msg, interrupt=True)
        self._update_options()
        return "crypto_menu"
