from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
from dotenv import load_dotenv

import os

load_dotenv()

# Supabase Client Initialisierung
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

supabase = None
try:
    from supabase import create_client
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except ImportError:
    print("[Server Warning] 'supabase' Python-Paket ist nicht installiert. DB-Funktionen deaktiviert.")
except Exception as e:
    print(f"[Server Warning] Supabase-Initialisierungsfehler: {e}")

# Multiplayer State
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {} # room_id -> list of websockets
        self.player_data: Dict[WebSocket, dict] = {}

    async def connect(self, websocket: WebSocket, room_id: str, username: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        self.player_data[websocket] = {"username": username, "room_id": room_id}
        
        # Broadcast: Neuer Spieler
        await self.broadcast(room_id, {
            "type": "player_joined",
            "username": username,
            "id": str(id(websocket))
        })

    def disconnect(self, websocket: WebSocket):
        data = self.player_data.get(websocket)
        if data:
            room_id = data["room_id"]
            if room_id in self.active_connections:
                self.active_connections[room_id].remove(websocket)
            del self.player_data[websocket]
            return data
        return None

    async def broadcast(self, room_id: str, message: dict, exclude: WebSocket = None):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                if connection != exclude:
                    await connection.send_json(message)

manager = ConnectionManager()

app = FastAPI(title="Audio Studio Tycoon Mod & Multiplayer API")

# Datenmodelle
class User(BaseModel):
    username: str
    password: str

class Mod(BaseModel):
    id: str
    name: str
    author: str
    version: str
    description: str
    download_url: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Audio Studio Tycoon v3.0 API", "db_connected": supabase is not None}

@app.post("/auth/login")
def login(user: User):
    if not supabase:
        raise HTTPException(
            status_code=503, 
            detail="Supabase-Authentifizierung ist serverseitig nicht konfiguriert (SUPABASE_URL/SUPABASE_KEY fehlen)."
        )
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.username,
            "password": user.password
        })
        return {"access_token": response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials: {str(e)}")

@app.get("/mods", response_model=List[Mod])
def list_mods():
    if not supabase:
        return []
    try:
        # Fetching all verified mods from Supabase
        response = supabase.table("mods").select("*").eq("is_verified", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# --- Multiplayer WebSockets ---

@app.websocket("/ws/multiplayer/{room_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    await manager.connect(websocket, room_id, username)
    try:
        while True:
            data = await websocket.receive_json()
            # Nachrichten-Relay an alle im Raum (außer Sender)
            await manager.broadcast(room_id, data, exclude=websocket)
    except WebSocketDisconnect:
        p_data = manager.disconnect(websocket)
        if p_data:
            await manager.broadcast(p_data["room_id"], {
                "type": "player_left",
                "username": p_data["username"],
                "player_id": str(id(websocket))
            })

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run(app, host=host, port=8000)
