"""
Netzwerk-Manager für Audio Studio Tycoon v3.0.
Verantwortlich für die Kommunikation mit dem Mod-Portal und dem Backend.
"""

import requests
import json
import os

class NetworkManager:
    def __init__(self, api_base_url="http://localhost:8000"):
        self.api_base_url = api_base_url
        self.token = None
        self.is_connected = False
        
    def login(self, username, password):
        """
        Versucht den Nutzer am Backend einzuloggen.
        Gibt True bei Erfolg zurück.
        """
        try:
            # Reale API Kommunikation
            response = requests.post(f"{self.api_base_url}/auth/login", json={"username": username, "password": password})
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.is_connected = True
                return True
            return False
        except Exception as e:
            print(f"Netzwerk-Fehler: {e}")
            return False

    def get_mod_list(self):
        """
        Ruft die Liste der verfügbaren Mods ab.
        """
        if not self.is_connected:
            return []
            
        try:
            response = requests.get(f"{self.api_base_url}/mods")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []

    def download_mod(self, mod_id, target_path="mods/"):
        """
        Lädt einen Mod herunter und speichert ihn lokal.
        """
        if not self.is_connected:
            return False
            
        # Logik zum Downloaden und Entpacken...
        print(f"Lade Mod {mod_id} herunter...")
        return True


# --- Top-Level Helfer-Funktionen (für direkten Import) ---

def fetch_mod_list(api_base_url="http://localhost:8000"):
    """
    Hilfsfunktion: Ruft die Mod-Liste vom Server ab.
    Gibt eine leere Liste zurück, wenn keine Verbindung besteht.
    Nutzbar als: from network import fetch_mod_list
    """
    nm = NetworkManager(api_base_url)
    return nm.get_mod_list()
