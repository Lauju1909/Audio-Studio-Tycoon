"""
Audio-Manager für Audio Studio Tycoon - Audio Edition.
Kommuniziert direkt mit NVDA über accessible_output2.
Nutzt pygame.mixer für Sound-Effekte.
"""

import pygame
import os
import sys
import ctypes
import queue
import threading
import time

def resource_path(relative_path):
    """ Findet den absoluten Pfad zur Ressource, kompatibel mit Dev-Umgebung und PyInstaller. """
    # 1. Check PyInstaller _MEIPASS (one-file temp folder)
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, relative_path)
        if os.path.exists(path):
            return path

    # 2. Check EXE directory (frozen) or script directory (dev)
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    path = os.path.join(base_path, relative_path)
    if os.path.exists(path):
        return path
        
    # 3. Check _internal directory (PyInstaller 6 one-dir)
    internal_path = os.path.join(base_path, "_internal", relative_path)
    if os.path.exists(internal_path):
        return internal_path
        
    # 4. Check CWD
    cwd_path = os.path.join(os.getcwd(), relative_path)
    if os.path.exists(cwd_path):
        return cwd_path
        
    return path

class AudioManager:
    def __init__(self):
        self.tolk = None
        self.tolk_active = False
        self.linux_speech = None
        
        # Audio Queue und Threading
        self.speech_queue = queue.Queue()
        self.stop_worker = False
        
        # Betriebssystem-Check
        self.is_windows = sys.platform.startswith('win')
        self.is_linux = sys.platform.startswith('linux')

        if self.is_windows:
            # Tolk-Ausgabe für Windows initialisieren
            try:
                # Suche Tolk.dll an verschiedenen Orten
                possible_paths = [
                    os.path.join(os.path.abspath("."), "Tolk.dll"),
                    resource_path("Tolk.dll"),
                    os.path.join(os.path.dirname(sys.executable), "Tolk.dll") if getattr(sys, 'frozen', False) else ""
                ]
                
                dll_path = None
                for p in possible_paths:
                    if p and os.path.exists(p):
                        dll_path = p
                        break
                    
                if dll_path:
                    print(f"[Audio] Lade Tolk von: {dll_path}")
                    try:
                        self.tolk = ctypes.windll.LoadLibrary(dll_path)
                        
                        # Funktionen explizit definieren
                        self.tolk.Tolk_Load.restype = ctypes.c_bool
                        self.tolk.Tolk_IsLoaded.restype = ctypes.c_bool
                        self.tolk.Tolk_Unload.restype = None
                        
                        if hasattr(self.tolk, 'Tolk_TrySAPI'):
                            self.tolk.Tolk_TrySAPI.argtypes = [ctypes.c_bool]
                            self.tolk.Tolk_TrySAPI.restype = ctypes.c_bool
                            
                        if hasattr(self.tolk, 'Tolk_PreferSAPI'):
                            self.tolk.Tolk_PreferSAPI.argtypes = [ctypes.c_bool]
                            self.tolk.Tolk_PreferSAPI.restype = None
                            
                        self.tolk.Tolk_Output.argtypes = [ctypes.c_wchar_p, ctypes.c_bool]
                        self.tolk.Tolk_Output.restype = ctypes.c_bool
                        
                        self.tolk.Tolk_IsSpeaking.restype = ctypes.c_bool
                        
                        # Initialisieren
                        if self.tolk.Tolk_Load():
                            self.tolk_active = self.tolk.Tolk_IsLoaded()
                            if self.tolk_active:
                                if hasattr(self.tolk, 'Tolk_TrySAPI'):
                                    self.tolk.Tolk_TrySAPI(True)
                                print("[Audio] Tolk Screenreader-Support aktiv.")
                        else:
                            print("[Audio] Tolk_Load() gab False zurück.")
                    except Exception as dll_e:
                        print(f"[Audio Fehler] Fehler beim Setup der Tolk-Funktionen: {dll_e}")
                else:
                    print(f"[Audio Fehler]: Tolk.dll wurde an keinem Ort gefunden.")
            except Exception as e:
                print(f"[Audio Exception]: Tolk-Init fehlgeschlagen: {e}")
        
        elif self.is_linux:
            # Linux-Ausgabe über speech-dispatcher (speechd)
            try:
                import speechd
                self.linux_speech = speechd.SSIPClient('AudioStudioTycoon')
                # Standard-Parameter setzen
                self.linux_speech.set_punctuation(speechd.PunctuationMode.SOME)
                print("[Linux] Speech-Dispatcher (speechd) erfolgreich initialisiert.")
            except Exception as e:
                print(f"[Linux Speech Fehler]: speechd konnte nicht geladen werden. ({e})")
                print("Bitte installiere 'python3-speechd' oder 'speech-dispatcher'.")

        if not self.tolk_active and not self.linux_speech:
            print("[INFO] Keine Screenreader-Bibliothek aktiv. Nutze Konsolen-Fallback.")

        # Pygame Mixer für SFX
        try:
            # Puffer und Frequenz für bessere Kompatibilität und Latenz
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
        except Exception as e:
            print(f"[Mixer Init Fehler]: {e}")

        self.music_enabled = True
        self.current_loop = None
        self.tts_engine = "auto"
        
        self.music_volume = 50
        self.sfx_volume = 100
        self.speech_volume = 100

        # Worker Thread starten
        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()

    def _speech_worker(self):
        """Hintergrund-Thread zur sequentiellen Verarbeitung der Sprachausgabe."""
        while not self.stop_worker:
            try:
                # Warte auf neue Nachrichten
                item = self.speech_queue.get(timeout=0.1)
                if item is None: break
                text, interrupt = item
                
                # Windows (Tolk)
                if self.tolk_active and self.tolk:
                    try:
                        # Wenn nicht unterbrochen werden soll, warten bis fertig gesprochen wurde
                        if not interrupt:
                            wait_start = time.time()
                            # Sicherheitstimeout von 5 Sekunden, um Hänger zu vermeiden
                            while self.tolk.Tolk_IsSpeaking():
                                if self.stop_worker or (time.time() - wait_start > 5.0):
                                    break
                                time.sleep(0.01)
                        
                        # Ausgabe tätigen
                        # Bei gesetzten argtypes konvertiert ctypes den String automatisch
                        self.tolk.Tolk_Output(text, interrupt)
                    except Exception as e:
                        print(f"[TTS Worker] Tolk Fehler bei Ausgabe: {e}")
                
                # Linux (speech-dispatcher)
                elif self.linux_speech:
                    try:
                        if interrupt:
                            self.linux_speech.cancel()
                        self.linux_speech.speak(text)
                    except Exception as e:
                        print(f"Linux Worker Fehler: {e}")
                
                self.speech_queue.task_done()
            except queue.Empty:
                continue

    def apply_volumes(self, settings):
        """Übernimmt die Volumen-Einstellungen aus dem GameState."""
        self.music_volume = settings.get("music_volume", 50)
        self.sfx_volume = settings.get("sfx_volume", 100)
        self.speech_volume = settings.get("speech_volume", 100)
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume / 100.0 * 0.5)
            
        if self.current_loop:
            self.current_loop.set_volume(self.sfx_volume / 100.0 * 0.6)
        
    def update_tts_engine(self, engine_mode):
        """Wechselt den TTS-Modus: auto, nvda, sapi"""
        self.tts_engine = engine_mode
        if not self.tolk_active or not self.tolk:
            return
            
        try:
            if engine_mode == "auto":
                if hasattr(self.tolk, 'Tolk_PreferSAPI'):
                    self.tolk.Tolk_PreferSAPI(False)
                if hasattr(self.tolk, 'Tolk_TrySAPI'):
                    self.tolk.Tolk_TrySAPI(True)
            elif engine_mode == "nvda":
                if hasattr(self.tolk, 'Tolk_PreferSAPI'):
                    self.tolk.Tolk_PreferSAPI(False)
                if hasattr(self.tolk, 'Tolk_TrySAPI'):
                    self.tolk.Tolk_TrySAPI(False)
            elif engine_mode == "sapi":
                if hasattr(self.tolk, 'Tolk_PreferSAPI'):
                    self.tolk.Tolk_PreferSAPI(True)
                if hasattr(self.tolk, 'Tolk_TrySAPI'):
                    self.tolk.Tolk_TrySAPI(True)
        except Exception as e:
            print(f"[Tolk Mode Change Fehler]: {e}")

    def set_music_enabled(self, enabled):
        """Aktiviert oder deaktiviert Musik."""
        self.music_enabled = enabled
        if not enabled:
            self.stop_music()

    def speak(self, text, interrupt=True):
        """Fügt Text zur Sprach-Queue hinzu."""
        print(f"[TTS]: {text}")
        
        if interrupt:
            # Leere die aktuelle Queue für sofortige Unterbrechung
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                    self.speech_queue.task_done()
                except queue.Empty:
                    break
        
        # Zur Queue hinzufügen
        self.speech_queue.put((text, interrupt))

    def play_sound(self, sound_name):
        """Spielt einen Sound-Effekt ab (wav, ogg oder mp3)."""
        formats = ["wav", "ogg", "mp3"]
        for fmt in formats:
            try:
                sound_path = resource_path(f"assets/{sound_name}.{fmt}")
                if os.path.exists(sound_path):
                    print(f"[Audio] Spiele Sound: {sound_path}")
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.sfx_volume / 100.0 * 0.8)
                    sound.play()
                    return
                else:
                    # Nur loggen wenn es die letzte Option war (oder gar nicht um Spam zu vermeiden)
                    pass
                    print(f"[Audio] Sound nicht gefunden: {sound_path}")
            except Exception:
                continue

    def play_loop(self, sound_name):
        """Startet einen Sound in Endlosschleife."""
        formats = ["wav", "ogg", "mp3"]
        for fmt in formats:
            try:
                sound_path = resource_path(f"assets/{sound_name}.{fmt}")
                if os.path.exists(sound_path):
                    self.current_loop = pygame.mixer.Sound(sound_path)
                    self.current_loop.set_volume(self.sfx_volume / 100.0 * 0.3)
                    self.current_loop.play(loops=-1)
                    return
            except Exception:
                continue
        self.current_loop = None

    def play_music(self, music_name):
        """Startet Hintergrundmusik über pygame.mixer.music."""
        if not self.music_enabled:
            return
        formats = ["mp3", "ogg", "wav"]
        for fmt in formats:
            try:
                music_path = resource_path(f"assets/{music_name}.{fmt}")
                if os.path.exists(music_path):
                    print(f"[Audio] Spiele Musik: {music_path}")
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(self.music_volume / 100.0 * 0.5)
                    pygame.mixer.music.play(loops=-1)
                    return
                else:
                    print(f"[Audio] Musikdatei nicht gefunden: {music_path}")
            except Exception:
                continue

    def stop_music(self):
        """Stoppt die Hintergrundmusik."""
        pygame.mixer.music.stop()

    def stop_loop(self):
        """Stoppt die aktuelle Schleife."""
        if hasattr(self, 'current_loop') and self.current_loop:
            self.current_loop.stop()
            self.current_loop = None

    def cleanup(self):
        """Ressourcen freigeben."""
        self.stop_worker = True
        self.stop_loop()
        
        if self.linux_speech:
            try:
                self.linux_speech.close()
            except Exception:
                pass
                
        if self.tolk_active and self.tolk:
            try:
                self.tolk.Tolk_Unload()
            except Exception:
                pass

        try:
            pygame.mixer.quit()
        except Exception:
            pass
