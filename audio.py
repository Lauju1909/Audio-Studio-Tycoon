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
        
        # Tolk-Ausgabe initialisieren
        try:
            # Versuche Tolk.dll zu laden (aus dem gleichen Ordner oder assets)
            dll_path = os.path.join(os.path.abspath("."), "Tolk.dll")
            if not os.path.exists(dll_path):
                # Fallback für PyInstaller / assets
                dll_path = resource_path("Tolk.dll")
                
            if os.path.exists(dll_path):
                self.tolk = ctypes.windll.LoadLibrary(dll_path)
                self.tolk.Tolk_Load()
                self.tolk_active = self.tolk.Tolk_IsLoaded()
                if self.tolk_active:
                    # Damit Screenreader nicht quatschen bevor das Spiel spricht
                    self.tolk.Tolk_TrySAPI(True)
                else:
                    print("[Tolk Init Fehler]: Tolk_Load() fehlgeschlagen.")
            else:
                print(f"[Tolk Fehler]: Tolk.dll nicht gefunden unter {dll_path}")
                
        except Exception as e:
            print(f"[Tolk Init Exception]: {e}")
            
        if not self.tolk_active:
            print("[INFO] Fallback auf Konsolen-Ausgabe aktiv.")

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
        Text an Tolk senden. Fallback: Konsolen-Ausgabe.
        """
        print(f"[SPRACHE]: {text}")
        if self.tolk_active and self.tolk:
            try:
                # Tolk_Output erwartet wchar_t* (Unicode String)
                self.tolk.Tolk_Output(ctypes.c_wchar_p(text), ctypes.c_bool(interrupt))
            except Exception as e:
                print(f"[Tolk Speak Fehler]: {e}")

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
        try:
            pygame.mixer.quit()
        except Exception:
            pass
