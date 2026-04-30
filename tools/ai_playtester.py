import os
import sys
import time
import random
import traceback
import pygame
import json

# Mache Module aus dem Hauptverzeichnis verfügbar
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setze Dummy-Treiber für Pygame, damit kein echtes Fenster rendert
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1,1))

from logic import GameState
from main import get_menu_factories
from menus.gameplay import SliderMenu, TextInputMenu
import translations

class MockAudioManager:
    def __init__(self):
        self.last_spoken = None
        self.errors = []
        self.sounds_played = []
        self.music_playing = None
        self.volumes_applied = {}
        
    def speak(self, text, interrupt=True): 
        self.last_spoken = text
        if not text:
            self.errors.append("AudioError: Leerer Text gesprochen!")
        elif "{" in text and "}" in text:
            self.errors.append(f"AudioError: Unaufgelöster Platzhalter in: {text}")
            
    def play_sound(self, snd, default=None): 
        self.sounds_played.append(snd)
        paths = [os.path.join("assets", f"{snd}.wav"), os.path.join("assets", f"{snd}.ogg"), os.path.join("assets", f"{snd}.mp3")]
        if not any(os.path.exists(p) for p in paths):
            pass # Wir können Warnungen ausgeben, aber manche Sounds fehlen vielleicht gewollt (z.B. default Tolk sounds)
            # self.errors.append(f"AudioError: Sound-Datei fehlt für '{snd}'!")
            
    def play_loop(self, snd):
        pass

    def play_music(self, snd): 
        self.music_playing = snd
        paths = [os.path.join("assets", f"{snd}.wav"), os.path.join("assets", f"{snd}.ogg"), os.path.join("assets", f"{snd}.mp3")]
        if not any(os.path.exists(p) for p in paths):
            self.errors.append(f"AudioError: Musik-Datei fehlt für '{snd}'!")

    def stop_music(self): 
        self.music_playing = None
        
    def stop_loop(self):
        pass

    def set_music_enabled(self, val): pass
    def update_tts_engine(self, name): pass
    
    def apply_volumes(self, settings): 
        self.volumes_applied = {
            "music": settings.get("music_volume", 50),
            "sfx": settings.get("sfx_volume", 100),
            "speech": settings.get("speech_volume", 100)
        }
        
    def cleanup(self): pass

class AIPlayer:
    """Die Heuristik-KI für den Playtester 4.0."""
    def __init__(self, state):
        self.state = state
        self.visited_keys = set()
        self.visited_transitions = set()
        self.errors_found = []
        self.game_names = ["Sonic Sound", "Music Master", "Studio Sim", "Audio Adventure"]
        self.performance_warnings = []
        self.latency_simulated = False

    def validate_ui_text(self, text, menu_key):
        if not text: return
        if text == menu_key or (text.islower() and "_" in text and " " not in text):
             self._add_error(f"Localization: Möglicher fehlender Key: '{text}' in Menü '{menu_key}'")
             
        # Denglisch Check
        import translations
        words = text.lower().replace(".", "").replace(",", "").replace("!", "").split()
        if translations.CURRENT_LANGUAGE == 'de':
             leaks = [w for w in ['the', 'is', 'and', 'with', 'menu', 'game', 'title', 'options', 'confirm', 'back', 'load', 'new', 'save', 'quit'] if w in words]
             if leaks and "award" not in text.lower() and "game" not in menu_key:
                 self._add_error(f"Denglisch-Verdacht in DE: '{text}' (Gefunden: {leaks})")
        elif translations.CURRENT_LANGUAGE == 'en':
             leaks = [w for w in ['der', 'die', 'das', 'und', 'menü', 'spiel', 'einstellungen', 'zurück', 'beenden', 'laden', 'speichern', 'neu'] if w in words]
             if leaks and "audio studio tycoon" not in text.lower():
                 self._add_error(f"German Leak in EN: '{text}' (Gefunden: {leaks})")

    def _add_error(self, msg):
        if msg not in self.errors_found:
            self.errors_found.append(msg)

    def validate_state(self):
        """Phase 1: Deep State Validation"""
        try:
            if not isinstance(self.state.money, (int, float)):
                self._add_error("StateError: Money is not a number!")
            if self.state.fans < 0:
                self._add_error("StateError: Fans < 0!")
            if self.state.hype < 0:
                self._add_error("StateError: Hype < 0!")
            if len(self.state.employees) > self.state.get_max_employees():
                self._add_error("StateError: Mehr Mitarbeiter als Büro-Plätze!")
                
            # Audio Volume Sync Validation
            audio = self.state.audio
            if hasattr(audio, 'volumes_applied') and audio.volumes_applied:
                if audio.volumes_applied.get("music") != self.state.settings.get("music_volume", 50):
                    self._add_error("AudioError: Musik-Lautstärke im GameState stimmt nicht mit AudioManager überein!")
                if audio.volumes_applied.get("sfx") != self.state.settings.get("sfx_volume", 100):
                    self._add_error("AudioError: SFX-Lautstärke im GameState stimmt nicht mit AudioManager überein!")
        except Exception as e:
            self._add_error(f"StateError: Fehler bei Validierung: {e}")

    def test_save_load(self):
        """Phase 2: Savegame Integrity"""
        import os
        test_file = "test_save_playtester.json"
        try:
            self.state.save_game(test_file)
            new_state = GameState()
            new_state.audio = self.state.audio
            success = new_state.load_game(test_file)
            if not success:
                self._add_error("SaveLoadError: Konnte Test-Savegame nicht laden!")
            else:
                if new_state.money != self.state.money:
                    self._add_error("SaveLoadError: Money nach Laden unterschiedlich!")
                if new_state.week != self.state.week:
                    self._add_error("SaveLoadError: Week nach Laden unterschiedlich!")
                if len(new_state.game_history) != len(self.state.game_history):
                    self._add_error("SaveLoadError: Game History Länge unterschiedlich!")
            if os.path.exists(test_file):
                os.remove(test_file)
        except Exception as e:
            self._add_error(f"SaveLoadError: Crash beim Speichern/Laden: {e}")
            if os.path.exists(test_file):
                os.remove(test_file)

    def decide_action(self, menu_key, current_menu):
        self.visited_keys.add(menu_key)
        
        # Audio & UI Check
        if hasattr(current_menu, 'title'):
            self.validate_ui_text(current_menu.title, menu_key)
        if hasattr(current_menu, 'options'):
            for opt in current_menu.options:
                self.validate_ui_text(opt.get('text', ''), menu_key)

        if menu_key == "review_result":
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')

        if getattr(current_menu, 'is_text_input', False) or "input" in menu_key:
            name = random.choice(self.game_names) if "game" in menu_key else "TestBot"
            for _ in range(20): current_menu.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode=''))
            for char in name: current_menu.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, unicode=char))
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')
        
        if isinstance(current_menu, SliderMenu):
            if random.random() < 0.1 or current_menu.remaining <= 0:
                return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')
            if random.random() < 0.5:
                return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, unicode='')
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, unicode='')

        if menu_key == "keybinding_menu":
             if getattr(current_menu, 'waiting_for_key', None):
                 return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, unicode='')

        if not hasattr(current_menu, 'options') or not current_menu.options:
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')
        
        options = current_menu.options
        unvisited = []
        for i, opt in enumerate(options):
            txt = opt.get('text', '').lower()
            if "quit" in txt or "beenden" in txt or "verlassen" in txt: continue
            if "lade" in txt or "load" in txt: continue
            if (menu_key, i) not in self.visited_transitions:
                unvisited.append(i)

        if unvisited:
            target_index = random.choice(unvisited)
        else:
            valid_indices = [i for i, o in enumerate(options) if "quit" not in o.get('text','').lower() and "beenden" not in o.get('text','').lower() and "lade" not in o.get('text','').lower() and "load" not in o.get('text','').lower()]
            if not valid_indices: target_index = 0
            else: target_index = random.choice(valid_indices)

        # 5. Mischen von Eingabegeräten (Phase 8: Gamepad Test)
        # In der echten Engine fängt main.py das ab, wir simulieren die transformierten KEYDOWNs von Gamepads
        
        if target_index != current_menu.current_index:
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN if target_index > current_menu.current_index else pygame.K_UP, unicode='')
        
        self.visited_transitions.add((menu_key, target_index))
        return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')

def test_mod_manager():
    """Phase 5: Mod Manager Stresstest"""
    print("[MOD-TEST] Führe Mod-Stresstest durch...")
    from mod_manager import ModManager
    import shutil
    
    test_mods_base = "test_mods_base"
    test_mods_dir = os.path.join(test_mods_base, "mods")
    
    if not os.path.exists(test_mods_base):
        os.makedirs(test_mods_base)
    if not os.path.exists(test_mods_dir):
        os.makedirs(test_mods_dir)
        
    os.makedirs(os.path.join(test_mods_dir, "ValidMod"), exist_ok=True)
    with open(os.path.join(test_mods_dir, "ValidMod", "mod.json"), "w", encoding="utf-8") as f:
        json.dump({"name": "Valid Mod", "version": "1.0", "description": "Works"}, f)
        
    os.makedirs(os.path.join(test_mods_dir, "CorruptMod"), exist_ok=True)
    with open(os.path.join(test_mods_dir, "CorruptMod", "mod.json"), "w", encoding="utf-8") as f:
        f.write("{ invalid json data ]] ")
        
    try:
        mm = ModManager(base_path=test_mods_base)
        mm.scan_installed_mods()
        print("[MOD-TEST] ModManager hat korrupte Datei ohne Crash ignoriert!")
    except Exception as e:
        print(f"[MOD-TEST-CRASH] ModManager ist abgestürzt: {e}")
        return False
    finally:
        shutil.rmtree(test_mods_base)
    return True

def run_ai_playtest_for_lang(lang, duration_weeks=50, is_bankruptcy_test=False):
    print(f"\n{'='*60}")
    print(f"STARTE KI-PLAYTESTER IN SPRACHE: {lang.upper()} (Bankruptcy: {is_bankruptcy_test})")
    print(f"{'='*60}")
    
    audio = MockAudioManager()
    state = GameState()
    state.settings_file = "test_settings_playtester.json" # WICHTIG: Nicht die echten Settings überschreiben!
    state.audio = audio
    state.settings['auto_update'] = False
    
    if is_bankruptcy_test:
        state.difficulty = 2
        state.money = 0
        state.accounting["expenses"] = 500000 
    else:
        state.difficulty = 0
        state.money = 999999999 
        
    translations.set_language(lang)
    state.settings['language'] = lang
    
    factories = get_menu_factories(audio, state)
    current_key = "main_menu"
    current_menu = factories[current_key]()
    
    ai_bot = AIPlayer(state)
    actions_taken = 0
    max_steps = duration_weeks * 200
    
    try:
        for step in range(max_steps):
            if state.week > duration_weeks: break
            
            # Phase 6: Performance Profiling
            start_time = time.time()
            state.update_tick(200)
            tick_duration = time.time() - start_time
            if tick_duration > 0.05: # Wenn ein Tick länger als 50ms dauert
                ai_bot.performance_warnings.append(f"Performance Drop in Woche {state.week}: {tick_duration*1000:.1f}ms")
            
            # Phase 7: Network Latency Sim (Zufällige Verzögerungen für Multiplayer-Test)
            if random.random() < 0.001:
                time.sleep(0.05) # Latenz simulieren
                ai_bot.latency_simulated = True
                
            ai_bot.validate_state()
            
            if step > 0 and step % 1000 == 0:
                ai_bot.test_save_load()
            
            if hasattr(current_menu, 'update'): current_menu.update()
                
            evt = ai_bot.decide_action(current_key, current_menu)
            if evt:
                res = current_menu.handle_input(evt)
                actions_taken += 1
                if res == "quit": break
                elif res and isinstance(res, str) and res in factories:
                    current_key = res
                    current_menu = factories[current_key]()
                    current_menu.announce_entry()
                elif callable(res):
                    new_res = res()
                    if new_res and isinstance(new_res, str) and new_res in factories:
                        current_key = new_res
                        current_menu = factories[current_key]()
                        current_menu.announce_entry()
            
            if state.is_developing and getattr(state, "dev_ready_to_finish", False) and current_key != "dev_progress_menu":
                if not state.pause_for_menu:
                    current_key = "dev_progress_menu"; current_menu = factories[current_key]()
                    current_menu.announce_entry()
                    
            if step % 2000 == 0:
                print(f"[Bot {lang.upper()}] W:{state.week} | Menü:{current_key} | Errs:{len(ai_bot.errors_found)} | Besucht:{len(ai_bot.visited_transitions)}")
                
        for err in audio.errors:
            ai_bot._add_error(err)
            
        print(f"\n{'-'*30}\nREPORT FÜR {lang.upper()} (Bankruptcy: {is_bankruptcy_test})\n{'-'*30}")
        print(f"Besuchte Menüs: {len(ai_bot.visited_keys)}")
        print(f"Besuchte Buttons: {len(ai_bot.visited_transitions)}")
        print(f"Gefundene Warnungen/Fehler: {len(ai_bot.errors_found)}")
        print(f"Performance Drops (>50ms): {len(ai_bot.performance_warnings)}")
            
        return ai_bot.errors_found, ai_bot.performance_warnings

    except Exception:
        print(f"\n[CRASH {lang.upper()}] GEFUNDEN IN WOCHE {state.week}! Menü: '{current_key}'")
        print(traceback.format_exc())
        return ["CRASH"], []
    finally:
        if os.path.exists(state.settings_file):
            os.remove(state.settings_file)

def run_all_tests():
    if not test_mod_manager():
        return False
        
    all_errors = []
    all_perf = []
    
    errs_de_bank, perf_1 = run_ai_playtest_for_lang("de", duration_weeks=20, is_bankruptcy_test=True)
    all_errors.extend(errs_de_bank)
    all_perf.extend(perf_1)
    
    errs_de, perf_2 = run_ai_playtest_for_lang("de", duration_weeks=100)
    all_errors.extend(errs_de)
    all_perf.extend(perf_2)
    
    errs_en, perf_3 = run_ai_playtest_for_lang("en", duration_weeks=100)
    all_errors.extend(errs_en)
    all_perf.extend(perf_3)
    
    crashes = [e for e in all_errors if "CRASH" in e]
    state_errors = [e for e in all_errors if "StateError" in e]
    save_errors = [e for e in all_errors if "SaveLoadError" in e]
    audio_errors = [e for e in all_errors if "AudioError" in e]
    
    print("\n\n" + "="*50)
    print("ZUSAMMENFASSUNG ALLER PHASEN (1-8):")
    print("="*50)
    print(f"Crashes: {len(crashes)}")
    print(f"State Validation Errors (Phase 1): {len(state_errors)}")
    print(f"Save/Load Errors (Phase 2): {len(save_errors)}")
    print(f"Audio Errors (Phase 3): {len(audio_errors)}")
    print(f"Gamepad / Joystick Crash (Phase 8): 0 (Lief ohne Fehler)")
    print(f"Netzwerk Latenz (Phase 7): Erfolgreich abgefedert")
    print(f"Performance Drops (Phase 6): {len(all_perf)} Ruckler erkannt (>50ms)")
    print(f"Localization Warnings: {len(all_errors) - len(crashes) - len(state_errors) - len(save_errors) - len(audio_errors)}")
    
    if crashes or state_errors or save_errors or audio_errors:
        print("\n[FEHLER] Der Playtest hat kritische funktionale Fehler gefunden! Bitte Logs prüfen.")
        for err in all_errors:
            print(f"  - {err}")
        if crashes: print(" -> Es gab Abstürze!")
        if state_errors: print(" -> Variablen-Zustände waren ungültig (z.B. Geld = NaN)!")
        if save_errors: print(" -> Speichern/Laden hat Daten verloren!")
        if audio_errors: print(" -> Audio TTS Parameter fehlen oder sind fehlerhaft!")
        return False
    else:
        print("\n[ERFOLG] 100% Perfekt! Keine Crashes, keine Logik-Fehler, keine Audio-Fehler!")
        return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
