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
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS (one-file)
        base_path = sys._MEIPASS
    except Exception:
        # Fallback for dev or multi-file build
        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
    
    # Check normal path
    path = os.path.join(base_path, relative_path)
    if os.path.exists(path):
        return path
        
    # Check _internal path (common in PyInstaller 6 multi-file builds)
    internal_path = os.path.join(base_path, "_internal", relative_path)
    if os.path.exists(internal_path):
        return internal_path
        
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
                dll_path = os.path.join(os.path.abspath("."), "Tolk.dll")
                if not os.path.exists(dll_path):
                    dll_path = resource_path("Tolk.dll")
                    
                if os.path.exists(dll_path):
                    self.tolk = ctypes.windll.LoadLibrary(dll_path)
                    self.tolk.Tolk_Load()
                    self.tolk_active = self.tolk.Tolk_IsLoaded()
                    if self.tolk_active:
                        self.tolk.Tolk_TrySAPI(True)
                else:
                    print(f"[Tolk Fehler]: Tolk.dll nicht gefunden.")
            except Exception as e:
                print(f"[Tolk Init Exception]: {e}")
        
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
            pygame.mixer.init()
        except Exception:
            pass

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
            pygame.mixer.music.set_volume(self.music_volume / 100.0 * 0.05)
            
        if self.current_loop:
            self.current_loop.set_volume(self.sfx_volume / 100.0 * 0.1)
        
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
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.sfx_volume / 100.0 * 0.15)
                    sound.play()
                    return
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
                    self.current_loop.set_volume(self.sfx_volume / 100.0 * 0.1)
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
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(self.music_volume / 100.0 * 0.05)
                    pygame.mixer.music.play(loops=-1)
                    return
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
