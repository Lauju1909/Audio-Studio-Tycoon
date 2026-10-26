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
        self.prism = None
        self.prism_ctx = None
        self.prism_backend = None
        self.prism_active = False
        self.prism_backend_name_str = None
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
            # --- STUFE 1: Prism Universal Screenreader & Speech Abstraction (bevorzugt) ---
            self._init_prism()

            # --- STUFE 2: Tolk-Ausgabe für Windows (Fallback wenn Prism nicht aktiv) ---
            if not self.prism_active:
                self._init_tolk()

            # --- STUFE 3: Windows SAPI Direktfallback (wenn Prism und Tolk versagen) ---
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

    def _init_prism(self):
        """Initialisiert die moderne Prism-Bibliothek für universelle Screenreader- & TTS-Ausgabe (NVDA, JAWS, OneCore, SAPI)."""
        try:
            possible_paths = [
                os.path.join(os.path.abspath("."), "prism.dll"),
                resource_path("prism.dll"),
                os.path.join(os.path.dirname(sys.executable), "prism.dll") if getattr(sys, 'frozen', False) else ""
            ]
            dll_path = None
            for p in possible_paths:
                if p and os.path.exists(p):
                    dll_path = p
                    break

            if not dll_path:
                print("[Audio] prism.dll wurde an keinem Ort gefunden.")
                return

            print(f"[Audio] Lade Prism von: {dll_path}")
            self.prism = ctypes.CDLL(dll_path)

            self.prism.prism_init.restype = ctypes.c_void_p
            self.prism.prism_init.argtypes = [ctypes.c_void_p]

            self.prism.prism_shutdown.argtypes = [ctypes.c_void_p]

            self.prism.prism_registry_count.restype = ctypes.c_size_t
            self.prism.prism_registry_count.argtypes = [ctypes.c_void_p]

            self.prism.prism_registry_name.restype = ctypes.c_char_p
            self.prism.prism_registry_name.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

            self.prism.prism_registry_id_at.restype = ctypes.c_uint64
            self.prism.prism_registry_id_at.argtypes = [ctypes.c_void_p, ctypes.c_size_t]

            self.prism.prism_registry_create.restype = ctypes.c_void_p
            self.prism.prism_registry_create.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

            self.prism.prism_registry_create_best.restype = ctypes.c_void_p
            self.prism.prism_registry_create_best.argtypes = [ctypes.c_void_p]

            self.prism.prism_backend_name.restype = ctypes.c_char_p
            self.prism.prism_backend_name.argtypes = [ctypes.c_void_p]

            self.prism.prism_backend_initialize.restype = ctypes.c_int
            self.prism.prism_backend_initialize.argtypes = [ctypes.c_void_p]

            self.prism.prism_backend_speak.restype = ctypes.c_int
            self.prism.prism_backend_speak.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]

            self.prism.prism_backend_stop.restype = ctypes.c_int
            self.prism.prism_backend_stop.argtypes = [ctypes.c_void_p]

            self.prism.prism_backend_braille.restype = ctypes.c_int
            self.prism.prism_backend_braille.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

            self.prism.prism_backend_get_features.restype = ctypes.c_uint64
            self.prism.prism_backend_get_features.argtypes = [ctypes.c_void_p]

            self.prism.prism_backend_free.argtypes = [ctypes.c_void_p]

            self.prism_ctx = self.prism.prism_init(None)
            if not self.prism_ctx:
                print("[Audio Fehler]: prism_init lieferte keinen Kontext.")
                self.prism = None
                return

            self.prism_backend = self.prism.prism_registry_create_best(self.prism_ctx)
            if self.prism_backend:
                self.prism.prism_backend_initialize(self.prism_backend)
                b_name = self.prism.prism_backend_name(self.prism_backend)
                self.prism_backend_name_str = b_name.decode('utf-8', errors='ignore') if b_name else "Unknown"
                self.prism_active = True
                print(f"[Audio] Prism: Screenreader/TTS initialisiert mit Backend: {self.prism_backend_name_str}")
            else:
                print("[Audio] Prism geladen, aber kein Backend aktiv.")
        except Exception as e:
            print(f"[Audio Exception]: Prism-Init fehlgeschlagen: {e}")
            self.prism = None
            self.prism_ctx = None
            self.prism_backend = None
            self.prism_active = False

    def _init_tolk(self):
        """Initialisiert Tolk als Fallback-Screenreader-Schnittstelle."""
        try:
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
                    self.tolk.Tolk_TrySAPI(True)
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
                print("[Audio Fehler]: Tolk.dll wurde an keinem Ort gefunden.")
        except Exception as e:
            print(f"[Audio Exception]: Tolk-Init fehlgeschlagen: {e}")
            self.tolk = None
            self.tolk_active = False

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
            import comtypes.client
            from comtypes import CoInitialize
            CoInitialize()
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

                # === STUFE 1: Prism Universal Screenreader & TTS ===
                if self.prism_active and self.prism and self.prism_backend:
                    try:
                        if interrupt:
                            try:
                                self.prism.prism_backend_stop(self.prism_backend)
                            except Exception:
                                pass
                        res = self.prism.prism_backend_speak(
                            self.prism_backend,
                            text.encode('utf-8', errors='replace'),
                            ctypes.c_bool(interrupt)
                        )
                        # Braille-Ausgabe mitsenden
                        try:
                            self.prism.prism_backend_braille(
                                self.prism_backend,
                                text.encode('utf-8', errors='replace')
                            )
                        except Exception:
                            pass
                        spoken = (res == 0)
                    except Exception as e:
                        print(f"[Prism Speak Fehler]: {e}")
                        spoken = False

                # === STUFE 2: Tolk-Ausgabe (Fallback) ===
                if not spoken and self.tolk_active and self.tolk:
                    tolk_has_sr = False
                    try:
                        tolk_has_sr = bool(self.tolk.Tolk_HasSpeech())
                    except Exception:
                        tolk_has_sr = False

                    if tolk_has_sr:
                        try:
                            self.tolk.Tolk_Output(ctypes.c_wchar_p(text), ctypes.c_bool(interrupt))
                            spoken = True
                        except Exception as e:
                            print(f"[Tolk SR Fehler]: {e}")
                
                # === STUFE 3: SAPI Direktfallback ===
                if not spoken:
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
                            thread_sapi = None

                    # Fallback pyttsx3 (wenn SAPI versagt hat)
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

                # Linux (speech-dispatcher)
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

        # Prism Backend-Umschaltung
        if self.prism_active and self.prism and self.prism_ctx:
            try:
                target_backend = None
                if engine_mode == "auto":
                    target_backend = self.prism.prism_registry_create_best(self.prism_ctx)
                else:
                    cnt = self.prism.prism_registry_count(self.prism_ctx)
                    for i in range(cnt):
                        bid = self.prism.prism_registry_id_at(self.prism_ctx, i)
                        bname = self.prism.prism_registry_name(self.prism_ctx, bid)
                        name_str = bname.decode('utf-8', errors='ignore').lower() if bname else ""
                        if engine_mode == "nvda" and ("nvda" in name_str or "jaws" in name_str):
                            target_backend = self.prism.prism_registry_create(self.prism_ctx, bid)
                            break
                        elif engine_mode == "sapi" and ("sapi" in name_str or "onecore" in name_str):
                            target_backend = self.prism.prism_registry_create(self.prism_ctx, bid)
                            break

                if target_backend:
                    if self.prism_backend:
                        try:
                            self.prism.prism_backend_stop(self.prism_backend)
                            self.prism.prism_backend_free(self.prism_backend)
                        except Exception:
                            pass
                    self.prism_backend = target_backend
                    self.prism.prism_backend_initialize(self.prism_backend)
                    b_name = self.prism.prism_backend_name(self.prism_backend)
                    self.prism_backend_name_str = b_name.decode('utf-8', errors='ignore') if b_name else "Unknown"
                    print(f"[Audio] Prism Backend gewechselt zu: {self.prism_backend_name_str}")
            except Exception as e:
                print(f"[Prism Mode Change Fehler]: {e}")

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
        try:
            print(f"[TTS]: {text}")
        except Exception:
            # Fallback for encoding issues
            try:
                safe_text = str(text).encode('ascii', errors='replace').decode('ascii')
                print(f"[TTS (Safe)]: {safe_text}")
            except Exception:
                pass
        
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
                
        if self.prism_active and self.prism:
            try:
                if self.prism_backend:
                    try:
                        self.prism.prism_backend_stop(self.prism_backend)
                    except Exception:
                        pass
                    self.prism.prism_backend_free(self.prism_backend)
                    self.prism_backend = None
                if self.prism_ctx:
                    self.prism.prism_shutdown(self.prism_ctx)
                    self.prism_ctx = None
                self.prism_active = False
            except Exception as e:
                print(f"[Prism Cleanup Fehler]: {e}")

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

def Tolk_Speak(*args, **kwargs): pass
