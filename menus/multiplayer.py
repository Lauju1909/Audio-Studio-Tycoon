from .base import Menu, TextInputMenu

class MultiplayerMainMenu(Menu):
    def __init__(self, audio, game_state):
        if not getattr(game_state, 'multiplayer', None):
            from multiplayer import MultiplayerManager
            game_state.multiplayer = MultiplayerManager(audio, game_state)
        self.audio = audio
        self.game_state = game_state
        t = game_state.get_text
        title = t('multiplayer_menu_title', default="Multiplayer Hauptmenü")
        options = [
            {'text': t('multiplayer_host_local', default="Lokalen Server hosten (Auto-Setup)"), 'action': self._host_local_server},
            {'text': t('multiplayer_join_room', default="Raum beitreten"), 'action': self._join_room_input},
            {'text': t('multiplayer_create_room', default="Raum erstellen"), 'action': self._create_room_input},
            {'text': t('back', default="Zurück"), 'action': lambda: "main_menu"}
        ]
        super().__init__(title, options, audio, game_state)

    def _host_local_server(self):
        if not hasattr(self.game_state, 'server_launcher'):
            from server_launcher import ServerLauncher
            self.game_state.server_launcher = ServerLauncher(self.audio, self.game_state)
        
        self.game_state.server_launcher.setup_and_start()
        return None # Bleibt im Menü, Launcher gibt Audio-Feedback

    def _join_room_input(self):
        return "multiplayer_room_id_input"

    def _create_room_input(self):
        return "multiplayer_create_id_input"

class MultiplayerRoomIdInput(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(
            title="multiplayer_join_room",
            prompt="multiplayer_enter_room_id",
            audio=audio,
            game_state=game_state,
            on_confirm=self._confirm,
            on_cancel=lambda: "multiplayer_main"
        )

    def _confirm(self, room_id):
        if not getattr(self.game_state, 'multiplayer', None):
            from multiplayer import MultiplayerManager
            self.game_state.multiplayer = MultiplayerManager(self.audio, self.game_state)
        
        self.game_state.multiplayer.connect(room_id, self.game_state.company_name)
        return "multiplayer_lobby"

class MultiplayerLobbyMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self._update_options()
        super().__init__(self.title, self.options, audio, game_state)

    def _update_options(self):
        t = self.game_state.get_text
        self.title = t('multiplayer_lobby_title', default="Lobby: {id}").format(id=getattr(self.game_state.multiplayer, 'room_id', '???'))
        
        player_list = []
        if hasattr(self.game_state, 'multiplayer'):
            for p in self.game_state.multiplayer.players:
                player_list.append({'text': p.get('username', 'Spieler'), 'action': None})
        
        self.options = player_list + [
            {'text': t('multiplayer_start_game', default="Spiel starten"), 'action': self._start_game},
            {'text': t('back', default="Verlassen"), 'action': self._leave}
        ]

    def _start_game(self):
        # In einer echten Implementierung würde hier ein Signal an alle gesendet
        self.audio.speak("Spiel wird gestartet...")
        return "game_menu"

    def _leave(self):
        # TODO: WebSocket schließen
        return "multiplayer_main"

    def update(self):
        # Lobby-Liste regelmäßig aktualisieren (einfache Lösung für Demo)
        pass
