"""
Audio-Manager für Audio Studio Tycoon - Audio Edition.
Kommuniziert direkt mit NVDA über Tolk.
Nutzt Windows SAPI als Fallback wenn kein Screenreader aktiv ist.
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
        self.sapi_voice = None       # Windows SAPI Fallback
        self.sapi_active = False     # Windows SAPI Status
        
        # Audio Queue und Threading
        self.speech_queue = queue.Queue()
        self.stop_worker = False
        
        # Betriebssystem-Check
        self.is_windows = sys.platform.startswith('win')
        self.is_linux = sys.platform.startswith('linux')

        if self.is_windows:
            # --- STUFE 1: Tolk-Ausgabe für Windows (bevorzugt: NVDA/JAWS) ---
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
                    self.tolk_active = bool(self.tolk.Tolk_IsLoaded())
                    if self.tolk_active:
                        # SAPI als Fallback in Tolk aktivieren
                        self.tolk.Tolk_TrySAPI(True)
                        
                        # Prüfe ob wirklich ein Screenreader erkannt wurde
                        has_sr = False
                        try:
                            has_sr = bool(self.tolk.Tolk_HasSpeech())
                        except Exception:
                            pass
                        
                        if has_sr:
                            print("[Audio] Tolk: Screenreader erkannt und aktiv.")
                        else:
                            print("[Audio] Tolk geladen, aber kein Screenreader erkannt. Nutze SAPI über Tolk.")
                else:
                    print(f"[Audio Fehler]: Tolk.dll wurde an keinem Ort gefunden.")
            except Exception as e:
                print(f"[Audio Exception]: Tolk-Init fehlgeschlagen: {e}")
                self.tolk = None
                self.tolk_active = False

            # --- STUFE 2: Windows SAPI Direktfallback (wenn Tolk versagt) ---
            # Immer SAPI initialisieren als Sicherheitsnetz
            self._init_sapi()

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

        if not self.tolk_active and not self.sapi_active and not self.linux_speech:
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

    def _init_sapi(self):
        """Initialisiert Windows SAPI als Direktfallback über win32com oder pyttsx3."""
        # Methode 1: win32com (am zuverlässigsten)
        try:
            import win32com.client
            self.sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
            self.sapi_active = True
            print("[Audio] Windows SAPI (win32com) erfolgreich initialisiert.")
            return
        except Exception as e:
            print(f"[Audio] win32com SAPI nicht verfügbar: {e}")

        # Methode 2: pyttsx3 (Fallback)
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            engine.setProperty('volume', 1.0)
            # Deutschen Voice bevorzugen
            voices = engine.getProperty('voices')
            for v in voices:
                if 'de' in v.id.lower() or 'german' in v.name.lower() or 'deutsch' in v.name.lower():
                    engine.setProperty('voice', v.id)
                    break
            self._pyttsx3_engine = engine
            self.sapi_voice = "pyttsx3"
            self.sapi_active = True
            print("[Audio] pyttsx3 SAPI erfolgreich initialisiert.")
            return
        except Exception as e:
            print(f"[Audio] pyttsx3 nicht verfügbar: {e}")

        # Methode 3: Direkt über ctypes/SAPI COM (letzter Ausweg)
        try:
            # SpVoice über ctypes direkt ansprechen
            from ctypes import POINTER, byref
            import comtypes.client
            from comtypes import CoInitialize
            CoInitialize()
            from comtypes.gen import SpeechLib
            voice = comtypes.client.CreateObject("SAPI.SpVoice")
            self.sapi_voice = voice
            self.sapi_active = True
            print("[Audio] comtypes SAPI erfolgreich initialisiert.")
        except Exception as e:
            print(f"[Audio] comtypes SAPI nicht verfügbar: {e}")
            self.sapi_active = False

    def _sapi_speak(self, text, interrupt=True):
        """Spricht Text direkt über Windows SAPI aus."""
        try:
            if self.sapi_voice == "pyttsx3":
                engine = getattr(self, '_pyttsx3_engine', None)
                if engine:
                    if interrupt:
                        try:
                            engine.stop()
                        except Exception:
                            pass
                    engine.say(text)
                    engine.runAndWait()
            elif self.sapi_voice is not None:
                # win32com oder comtypes SpVoice
                SVSFlagsAsync = 1
                SVSFPurgeBeforeSpeak = 2
                flags = SVSFlagsAsync
                if interrupt:
                    flags |= SVSFPurgeBeforeSpeak
                try:
                    self.sapi_voice.Speak(text, flags)
                except Exception:
                    # Synchron versuchen falls async nicht klappt
                    try:
                        self.sapi_voice.Speak(text, 0)
                    except Exception as e2:
                        print(f"[SAPI Speak Fehler]: {e2}")
        except Exception as e:
            print(f"[SAPI Worker Fehler]: {e}")

    def _speech_worker(self):
        """Hintergrund-Thread zur sequentiellen Verarbeitung der Sprachausgabe."""
        # COM für diesen Thread initialisieren (wichtig für SAPI)
        # WICHTIG: SAPI-Objekt MUSS im selben Thread erstellt werden, in dem Speak() aufgerufen wird!
        thread_sapi = None
        if self.is_windows:
            try:
                ctypes.windll.ole32.CoInitialize(None)
            except Exception:
                pass
            # SAPI direkt im Worker-Thread erstellen (COM-Thread-Affinität!)
            try:
                import win32com.client
                thread_sapi = win32com.client.Dispatch("SAPI.SpVoice")
                thread_sapi.Volume = self.speech_volume
                print("[Audio Worker] SAPI Thread-Instanz erstellt.")
            except Exception as e:
                print(f"[Audio Worker] SAPI Thread-Init fehlgeschlagen: {e}")
                thread_sapi = None

        while not self.stop_worker:
            try:
                # Warte auf neue Nachrichten
                item = self.speech_queue.get(timeout=0.1)
                if item is None:
                    break
                text, interrupt = item

                spoken = False

                # STUFE 1: SAPI direkt (IMMER zuerst auf Windows - zuverlässigster Weg)
                if thread_sapi is not None and self.is_windows:
                    try:
                        SVSFlagsAsync = 1
                        SVSFPurgeBeforeSpeak = 2
                        flags = SVSFlagsAsync
                        if interrupt:
                            flags |= SVSFPurgeBeforeSpeak
                        thread_sapi.Speak(text, flags)
                        spoken = True
                    except Exception as e:
                        print(f"[SAPI Worker Speak Fehler]: {e}")
                        thread_sapi = None  # SAPI kaputt, beim nächsten Mal Tolk versuchen

                # STUFE 2: Tolk (für echte Screenreader wie NVDA/JAWS - zusätzlich!)
                # Tolk gibt Text an den Screenreader weiter ZUSÄTZLICH zu SAPI
                # (Screenreader-Nutzer hören dann Tolk statt SAPI, weil SR Priorität hat)
                if self.tolk_active and self.tolk:
                    try:
                        self.tolk.Tolk_Output(ctypes.c_wchar_p(text), ctypes.c_bool(interrupt))
                    except Exception:
                        pass  # Tolk-Fehler ignorieren, SAPI hat bereits gesprochen

                # STUFE 3: Fallback pyttsx3 (wenn SAPI und Tolk beide versagt haben)
                if not spoken and self.is_windows:
                    try:
                        engine = getattr(self, '_pyttsx3_engine', None)
                        if engine:
                            if interrupt:
                                try: engine.stop()
                                except Exception: pass
                            engine.say(text)
                            engine.runAndWait()
                            spoken = True
                    except Exception as e:
                        print(f"[pyttsx3 Fallback Fehler]: {e}")

                # STUFE 4: Linux (speech-dispatcher)
                if not spoken and self.linux_speech:
                    try:
                        if interrupt:
                            self.linux_speech.cancel()
                        self.linux_speech.speak(text)
                    except Exception as e:
                        print(f"Linux Worker Fehler: {e}")

                self.speech_queue.task_done()
            except queue.Empty:
                continue

        # COM aufräumen
        if self.is_windows:
            try:
                ctypes.windll.ole32.CoUninitialize()
            except Exception:
                pass

    def apply_volumes(self, settings):
        """Übernimmt die Volumen-Einstellungen aus dem GameState."""
        self.music_volume = settings.get("music_volume", 50)
        self.sfx_volume = settings.get("sfx_volume", 100)
        self.speech_volume = settings.get("speech_volume", 100)
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume / 100.0 * 0.5)
            
        if self.current_loop:
            self.current_loop.set_volume(self.sfx_volume / 100.0 * 0.6)
        
        # SAPI Lautstärke anpassen (win32com)
        if self.sapi_active and self.sapi_voice and self.sapi_voice != "pyttsx3":
            try:
                self.sapi_voice.Volume = self.speech_volume
            except Exception:
                pass
        
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
        if not text:
            return
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
        self.speech_queue.put(None)  # Worker-Thread beenden
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

        # SAPI aufräumen
        if self.sapi_voice == "pyttsx3":
            try:
                engine = getattr(self, '_pyttsx3_engine', None)
                if engine:
                    engine.stop()
            except Exception:
                pass
        else:
            self.sapi_voice = None
        self.sapi_active = False

        try:
            pygame.mixer.quit()
        except Exception:
            pass
