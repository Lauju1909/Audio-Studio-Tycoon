"""
Multiplayer-Modul für Audio Studio Tycoon.
Handhabt die WebSocket-Verbindung, Raum-Management und Datensynchronisation.
"""

import asyncio
import json
import threading
import websockets
from typing import Optional, Callable

class MultiplayerManager:
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.base_uri = "ws://localhost:8000/ws/multiplayer"
        self.websocket = None
        self.thread = None
        self.is_connected = False
        self.room_id = None
        self.players = []
        self.on_message_received: Optional[Callable[[dict], None]] = None
        self._loop = None

    def connect(self, room_id, username):
        """Verbindet asynchron zum Server."""
        self.room_id = room_id
        uri = f"{self.base_uri}/{room_id}/{username}"
        
        self.thread = threading.Thread(target=self._run_event_loop, args=(uri,), daemon=True)
        self.thread.start()

    def _run_event_loop(self, uri):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect_and_listen(uri))

    async def _connect_and_listen(self, uri):
        try:
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                self.is_connected = True
                self.audio.speak(self.game_state.get_text("online_connected", default="Verbunden mit dem Online-Dienst."))
                
                async for message in websocket:
                    data = json.loads(message)
                    self._handle_message(data)
        except Exception as e:
            self.is_connected = False
            self.audio.speak(self.game_state.get_text("online_error", default="Verbindung zum Server fehlgeschlagen."))
            print(f"Multiplayer Error: {e}")

    def _handle_message(self, data):
        msg_type = data.get("type")
        
        if msg_type == "player_joined":
            player_name = data.get("username", "Unbekannt")
            self.players.append(data)
            self.audio.play_sound("online_join", default=None) # Später Sound hinzufügen
            self.audio.speak(f"{player_name} ist dem Raum beigetreten.")
        
        elif msg_type == "player_left":
            player_id = data.get("player_id")
            # Spieler aus Liste entfernen
            self.players = [p for p in self.players if p.get("id") != player_id]
            self.audio.play_sound("online_leave", default=None)
            self.audio.speak("Ein Spieler hat den Raum verlassen.")

        elif msg_type == "sync_state":
            # Empfange Spieldaten von anderen (z.B. Geld der Konkurrenz)
            if self.on_message_received:
                self.on_message_received(data)

    def send_message(self, data):
        """Sendet eine Nachricht an den Server."""
        if self.is_connected and self.websocket:
            asyncio.run_coroutine_threadsafe(
                self.websocket.send(json.dumps(data)),
                asyncio.get_event_loop()
            )

    def create_room(self, room_name):
        self.send_message({
            "type": "create_room",
            "name": room_name,
            "username": self.game_state.company_name
        })

    def join_room(self, room_id):
        self.send_message({
            "type": "join_room",
            "room_id": room_id,
            "username": self.game_state.company_name
        })

    def sync_game_state(self):
        """Sendet den aktuellen Spielzustand an andere Spieler."""
        self.send_message({
            "type": "sync_state",
            "money": self.game_state.money,
            "week": self.game_state.week,
            "hype": self.game_state.hype
        })
