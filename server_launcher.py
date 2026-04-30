"""
Automatischer Server-Installer und Launcher für Audio Studio Tycoon.
Prüft Abhängigkeiten und startet den lokalen Server.
"""

import subprocess
import sys
import os
import threading
import time

class ServerLauncher:
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.process = None
        self.is_running = False
        self.required_packages = ["fastapi", "uvicorn", "websockets", "python-dotenv", "supabase", "upnpy"]

    def setup_and_start(self):
        """Startet den gesamten Prozess in einem Thread, um das Spiel nicht zu blockieren."""
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        self.audio.speak("Starte automatische Server-Installation. Bitte warten...")
        
        # 1. Abhängigkeiten prüfen und installieren
        if self._install_dependencies():
            # 2. UPnP Port-Freigabe versuchen
            self._setup_upnp()
            
            self.audio.speak("Abhängigkeiten bereit. Starte den Server...")
            # 3. Server starten
            self._start_server()
        else:
            self.audio.speak("Fehler bei der Installation der Abhängigkeiten.")

    def _install_dependencies(self):
        """Installiert benötigte Python-Pakete."""
        try:
            for package in self.required_packages:
                print(f"[ServerLauncher] Prüfe/Installiere {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return True
        except Exception as e:
            print(f"[ServerLauncher] Installationsfehler: {e}")
            return False

    def _setup_upnp(self):
        """Versucht den Port 8000 am Router via UPnP freizugeben."""
        try:
            import upnpy
            self.audio.speak("Versuche automatische Port-Freigabe am Router...")
            upnp = upnpy.UPnP()
            devices = upnp.discover()
            if not devices:
                self.audio.speak("Kein UPnP-fähiger Router im Netzwerk gefunden. Manuelle Portfreigabe eventuell nötig.")
                return

            device = upnp.get_specific_device(devices[0].get_friendly_name())
            # WANIPConnection Dienst suchen
            service = device.get_service('WANIPConnection1') or device.get_service('WANPPPConnection1')
            
            if service:
                # Port 8000 freigeben (TCP)
                service.AddPortMapping(
                    NewRemoteHost='',
                    NewExternalPort=8000,
                    NewProtocol='TCP',
                    NewInternalPort=8000,
                    NewInternalClient=upnp.get_local_ip(),
                    NewEnabled=1,
                    NewPortMappingDescription='Audio Studio Tycoon Server',
                    NewLeaseDuration=0
                )
                self.audio.speak("Port 8000 wurde erfolgreich am Router freigegeben.")
                print(f"[UPnP] Port 8000 freigegeben für {upnp.get_local_ip()}")
            else:
                self.audio.speak("UPnP-Dienst am Router nicht verfügbar.")
        except Exception as e:
            print(f"[UPnP] Fehler: {e}")
            self.audio.speak("Automatische Port-Freigabe fehlgeschlagen.")

    def _start_server(self):
        """Startet den FastAPI Server via Uvicorn."""
        server_path = os.path.join(os.getcwd(), "server", "main.py")
        if not os.path.exists(server_path):
            self.audio.speak("Server-Quelldatei nicht gefunden.")
            return

        try:
            # Starte uvicorn als Subprozess
            self.process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            self.is_running = True
            self.audio.speak("Der Server ist jetzt online und bereit für Verbindungen auf Port 8000.")
            
            # Überwache den Output in der Konsole
            for line in self.process.stdout:
                print(f"[Server] {line.strip()}")
                
        except Exception as e:
            self.is_running = False
            print(f"[ServerLauncher] Server-Startfehler: {e}")
            self.audio.speak("Fehler beim Starten des Servers.")

    def stop_server(self):
        """Stoppt den laufenden Server-Prozess."""
        if self.process:
            self.process.terminate()
            self.is_running = False
            self.audio.speak("Server wurde beendet.")
