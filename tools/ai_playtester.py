import os
import sys
import time
import random
import traceback
import pygame

# Mache Module aus dem Hauptverzeichnis verfügbar
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setze Dummy-Treiber für Pygame, damit kein echtes Fenster rendert
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1,1))

from logic import GameState
from main import get_menu_factories
from translations import set_language
from menus.gameplay import SliderMenu, TextInputMenu

class MockAudioManager:
    def speak(self, text, interrupt=True): pass
    def play_sound(self, snd): pass
    def play_music(self, snd): pass
    def stop_music(self): pass
    def set_music_enabled(self, val): pass
    def update_tts_engine(self, name): pass
    def cleanup(self): pass

class AIPlayer:
    """Die Heuristik-KI für den Playtester 3.0."""
    def __init__(self, state):
        self.state = state
        self.visited_keys = set()
        self.errors_found = []
        self.last_lang_switch = 0
        self.game_names = ["Sonic Sound", "Music Master", "Studio Sim", "Audio Adventure"]
        self.engine_names = ["SoundEngine X", "AudioCore"]

    def validate_ui_text(self, text, menu_key):
        """Prüft UI-Texte auf Lokalisierungsfehler."""
        if not text: return
        
        # 1. Fehlender Key (Key wird als Text zurückgegeben)
        if text == menu_key or text.islower() and "_" in text:
             self._add_error(f"Möglicher fehlender Key oder Fallback: '{text}' in Menü '{menu_key}'")

        # 2. Unaufgelöster Platzhalter
        if "{" in text and "}" in text:
             # Manchmal sind Platzhalter gewollt (z.B. in der Hilfe), aber meistens ein Fehler
             if menu_key not in ["wiki", "help"]:
                self._add_error(f"Unaufgelöster Platzhalter in '{text}' (Menü: {menu_key})")

        # 3. Sprache-Mismatch (Denglisch Check)
        from translations import CURRENT_LANGUAGE
        if CURRENT_LANGUAGE == 'de':
             leaks = [w for w in [' the ', ' is ', ' and ', ' with '] if w in text.lower()]
             if leaks and "award" not in text.lower(): # Ausnahmeregel für GOTY
                 self._add_error(f"Denglisch-Verdacht in DE: '{text}' (Gefunden: {leaks})")
        elif CURRENT_LANGUAGE == 'en':
             leaks = [w for w in [' der ', ' die ', ' das ', ' und '] if w in text.lower()]
             if leaks:
                 self._add_error(f"German Leak in EN: '{text}' (Gefunden: {leaks})")

    def _add_error(self, msg):
        if msg not in self.errors_found:
            self.errors_found.append(msg)
            print(f"[AUDIT-WARN] {msg}")

    def decide_action(self, menu_key, current_menu):
        """Entscheidet, welche Taste in welchem Menü gedrückt wird."""
        self.visited_keys.add(menu_key)
        
        # UI-Validierung
        if hasattr(current_menu, 'title'):
            self.validate_ui_text(current_menu.title, menu_key)
        if hasattr(current_menu, 'options'):
            for opt in current_menu.options:
                self.validate_ui_text(opt.get('text', ''), menu_key)

        # 0. ReviewResultMenu - Einfach wegklicken
        if menu_key == "review_result":
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')

        # 1. Texteingabe abhandeln
        if getattr(current_menu, 'is_text_input', False) or "input" in menu_key:
            name = random.choice(self.game_names) if "game" in menu_key else "TestBot Studio"
            # Tippe den Namen
            for _ in range(20): current_menu.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode=''))
            for char in name: current_menu.handle_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, unicode=char))
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')
        
        # 2. SliderMenu abhandeln
        if isinstance(current_menu, SliderMenu):
            name = current_menu.slider_names[current_menu.current_index]
            target_val = random.randint(5, 10)
            if current_menu.values[name] < target_val and current_menu.remaining > 0:
                return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT, unicode='')
            elif current_menu.values[name] > target_val:
                return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT, unicode='')
            else:
                return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN if current_menu.current_index < len(current_menu.slider_names)-1 else pygame.K_RETURN, unicode='')

        # 3. Hat das Menü Optionen?
        if not hasattr(current_menu, 'options') or not current_menu.options:
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')
        
        options = current_menu.options
        target_index = -1
        
        # NAVIGATIONSLOGIK
        if menu_key == "main_menu":
            target_index = self._find_option(options, ["neues spiel", "new game"])
        
        elif menu_key == "difficulty_menu":
            target_index = random.randint(0, min(2, len(options)-1)) # Nicht zu schwer testen am Anfang
            
        elif menu_key == "game_menu":
            # Priorität: Benachrichtigungen > Forschung > Entwicklung > Wiki > Settings
            if self.state.emails: target_index = self._find_option(options, ["posteingang", "emails"])
            elif "settings_menu" not in self.visited_keys: target_index = self._find_option(options, ["einstellungen", "settings"])
            elif "research_menu" not in self.visited_keys: target_index = self._find_option(options, ["forschung", "research"])
            elif not self.state.is_developing and self.state.money > 20000: target_index = self._find_option(options, ["entwicklung", "develop"])
            elif "wiki" not in self.visited_keys: target_index = self._find_option(options, ["wiki", "hilfe", "help"])
            else: target_index = -1 # Abwarten
        
        elif menu_key == "settings_menu":
            if self.state.week - self.last_lang_switch > 50:
                target_index = self._find_option(options, ["sprache", "language"])
                if target_index == current_menu.current_index:
                    self.last_lang_switch = self.state.week
            else:
                target_index = self._find_option(options, ["zurück", "back"])

        # Fallback: Wenn wir nicht wissen was tun, einfach "Bestätigen" (Forward) anstatt "Back"
        if target_index == -1:
             if menu_key == "game_menu": return None
             # Versuche eine Option zu wählen, die nicht 'Back' heißt
             valid_indices = [i for i, o in enumerate(options) if "back" not in o['text'].lower() and "zurück" not in o['text'].lower()]
             target_index = random.choice(valid_indices) if valid_indices else 0

        # Navigiere zum target_index
        if target_index != current_menu.current_index:
            return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN if target_index > current_menu.current_index else pygame.K_UP, unicode='')
        
        return pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, unicode='')

    def _find_option(self, options, keywords):
        for i, opt in enumerate(options):
            txt = opt['text'].lower()
            if any(k in txt for k in keywords): return i
        return -1


def run_ai_playtest(duration_weeks=300):
    print(f"\n{'='*60}")
    print(f"STARTE KI-PLAYTESTER 3.0 (Vollständiger Audit-Lauf)")
    print(f"{'='*60}")
    
    audio = MockAudioManager()
    state = GameState()
    state.audio = audio
    state.settings['auto_update'] = False
    state.difficulty = 2
    
    factories = get_menu_factories(audio, state)
    current_key = "main_menu"
    current_menu = factories[current_key]()
    
    ai_bot = AIPlayer(state)
    actions_taken = 0
    max_steps = duration_weeks * 500
    
    try:
        for step in range(max_steps):
            if state.week > duration_weeks: break
            state.update_tick(200)
            if hasattr(current_menu, 'update'): current_menu.update()
                
            evt = ai_bot.decide_action(current_key, current_menu)
            if evt:
                res = current_menu.handle_input(evt)
                actions_taken += 1
                if res == "quit": break
                elif res and isinstance(res, str) and res in factories:
                    current_key = res
                    current_menu = factories[current_key]()
                elif callable(res): # Manche Aktionen geben direkt Callables zurück
                    new_res = res()
                    if new_res and isinstance(new_res, str) and new_res in factories:
                        current_key = new_res
                        current_menu = factories[current_key]()
            
            if state.is_developing and getattr(state, "dev_ready_to_finish", False) and current_key != "dev_progress_menu":
                if not state.pause_for_menu:
                    current_key = "dev_progress_menu"; current_menu = factories[current_key]()
                    
            if step % 2000 == 0:
                print(f"[Bot] W:{state.week} | M:{state.money}€ | Menü:{current_key} | Errs:{len(ai_bot.errors_found)}")
                
        print(f"\n{'-'*30}\nFINALER AUDIT-REPORT\n{'-'*30}")
        print(f"Besuchte Menüs: {sorted(list(ai_bot.visited_keys))}")
        print(f"Gefundene Lokalisierungsfehler: {len(ai_bot.errors_found)}")
        for err in ai_bot.errors_found: print(f"  [!] {err}")
        
        print(f"\n[ERFOLG] Durchlauf beendet! Woche {state.week}. Aktionen: {actions_taken}.")
        return len(ai_bot.errors_found) == 0

    except Exception:
        print(f"\n[CRASH] GEFUNDEN IN WOCHE {state.week}! Menü: '{current_key}'")
        print(traceback.format_exc())
        return False
        
if __name__ == "__main__":
    success = run_ai_playtest(duration_weeks=300)
    sys.exit(0 if success else 1)
