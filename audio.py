"""
Audio-Manager für Audio Studio Tycoon - Audio Edition.
Kommuniziert direkt mit NVDA über accessible_output2.
Nutzt pygame.mixer für Sound-Effekte.
"""

import pygame
import os
import sys

import ctypes

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
                    self.tolk = ctypes.windll.LoadLibrary(dll_path)
                    self.tolk.Tolk_Load()
                    self.tolk_active = self.tolk.Tolk_IsLoaded()
                    if self.tolk_active:
                        self.tolk.Tolk_TrySAPI(True)
                        print("[Audio] Tolk Screenreader-Support aktiv.")
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
        """
        Text an Tolk (Windows) oder speechd (Linux) senden. Fallback: Konsole.
        """
        print(f"[SPRACHE]: {text}")
        
        # Windows (Tolk)
        if self.tolk_active and self.tolk:
            try:
                self.tolk.Tolk_Output(ctypes.c_wchar_p(text), ctypes.c_bool(interrupt))
            except Exception as e:
                print(f"[Tolk Speak Fehler]: {e}")
        
        # Linux (speech-dispatcher)
        elif self.linux_speech:
            try:
                if interrupt:
                    self.linux_speech.cancel()
                self.linux_speech.speak(text)
            except Exception as e:
                print(f"[Linux Speak Fehler]: {e}")

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
        self.stop_loop()
        
        if self.linux_speech:
            try:
                self.linux_speech.close()
            except Exception:
                pass
                
        try:
            pygame.mixer.quit()
        except Exception:
            pass
