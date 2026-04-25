import os
import sys
import random
import traceback
import pygame

# Verzeichnis-Pfad korrigieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import GameState
from translations import set_language
from main import get_menu_factories

class MockEvent:
    def __init__(self, key, unicode_char='', mods=0):
        self.type = pygame.KEYDOWN
        self.key = key
        self.unicode = unicode_char
        self.mods = mods

class MockAudioManager:
    def speak(self, text, interrupt=True):
        pass
    def play_sound(self, sound_name):
        pass
    def play_music(self, music_name):
        pass
    def cleanup(self):
        pass
    def apply_volumes(self, settings):
        pass
    def set_music_enabled(self, enabled):
        pass
    def update_tts_engine(self, engine_mode):
        pass

class AIAgent:
    def __init__(self, language='de', target_money=500000, max_weeks=3000):
        self.language = language
        self.target_money = target_money
        self.max_weeks = max_weeks
        
        self.audio = MockAudioManager()
        self.state = GameState()
        self.state.audio = self.audio
        self.state.load_global_settings()
        self.state.settings['language'] = language
        self.state.settings['auto_update'] = False # Kein Auto-Update beim Test
        set_language(language)
        
        self.factories = get_menu_factories(self.audio, self.state)
        
        # 1. Teste Updater UI sofort beim Start
        self.state.pending_update = {"version": "9.9.9", "changelog": "Test update", "download_url": None, "hash": None}
        self.current_key = "update_confirm_menu"
        self.current_menu = self.factories[self.current_key]()
        
        self.menu_history = []
        
        # Stats
        self.crashes = 0
        self.ticks_simulated = 0
        self.successful = False

    def send_key(self, key, unicode_char=''):
        event = MockEvent(key, unicode_char)
        try:
            result = self.current_menu.handle_input(event)
            if result == "quit":
                return "quit"
            elif result and result in self.factories:
                self.menu_history.append(self.current_key)
                if len(self.menu_history) > 10:
                    self.menu_history.pop(0)
                    
                self.current_key = result
                self.current_menu = self.factories[self.current_key]()
                # Debug info
                print(f"[Nav] -> {self.current_key}")
                if hasattr(self.current_menu, "announce_entry"):
                    self.current_menu.announce_entry()
            return result
        except Exception as e:
            print(f"\n[CRASH] Fehler im Menü '{self.current_key}'!")
            print(f"Pfad Historie: {self.menu_history}")
            print(f"State Woche: {self.state.week}, Geld: {self.state.money}")
            traceback.print_exc()
            self.crashes += 1
            return "crash"

    def navigate_standard_menu(self):
        if not hasattr(self.current_menu, 'options') or not self.current_menu.options:
            return self.send_key(self.state.key_back)
            
        options = self.current_menu.options
        back_idx = -1
        for i, opt in enumerate(options):
            txt = opt['text'].lower()
            if "zurück" in txt or "back" in txt or "abbrechen" in txt or "cancel" in txt:
                back_idx = i
                
        # Menüs in denen wir niemals zurückgehen sollten (um den Flow nicht zu brechen)
        no_back_menus = ["topic_menu", "genre_menu", "platform_menu", "audience_menu", "game_size_menu", "engine_select_menu", "marketing_menu", "sub_genre_menu", "sequel_menu", "difficulty_menu", "email_inbox", "email_detail"]
        
        # Filtere Optionen heraus, die das Spiel beenden würden (quit)
        valid_options = []
        for i, opt in enumerate(options):
            if "quit" not in str(opt['action']).lower() and "beenden" not in opt['text'].lower():
                valid_options.append(i)
                
        if not valid_options:
            return self.send_key(self.state.key_back)
            
        target_idx = random.choice(valid_options)
        
        # Zu 15% gehen wir zurück, wenn möglich und nicht in einem Dev-Flow
        if back_idx != -1 and self.current_key not in no_back_menus and random.random() < 0.15:
            target_idx = back_idx
            
        # In Dev-Flows überspringen wir den Zurück-Button komplett bei der zufälligen Auswahl
        if back_idx != -1 and self.current_key in no_back_menus:
            while target_idx == back_idx and len(options) > 1:
                target_idx = random.randrange(len(options))
            
        self.send_key(self.state.key_home)
        current = 0
        while current < target_idx:
            self.send_key(self.state.key_down)
            current += 1
            
        return self.send_key(self.state.key_confirm)

    def fill_text_input(self):
        import string
        length = random.randint(4, 12)
        word = ''.join(random.choices(string.ascii_letters, k=length))
        for char in word:
            self.send_key(0, char)
        return self.send_key(self.state.key_confirm)

    def fill_sliders(self):
        if not hasattr(self.current_menu, 'slider_names'):
            return self.send_key(self.state.key_back)
            
        budget = getattr(self.current_menu, 'budget', 10)
        for _ in range(budget):
            self.send_key(pygame.K_RIGHT)
            if random.random() < 0.3:
                self.send_key(self.state.key_down)
        return self.send_key(self.state.key_confirm)

    def think_and_act(self):
        if self.state.is_bankrupt():
            return "quit"
        if self.state.money >= self.target_money:
            self.successful = True
            return "quit"
            
        menu_type = type(self.current_menu).__name__
        
        if menu_type == "TextInputMenu" or getattr(self.current_menu, 'is_text_input', False):
            if random.random() < 0.5 and hasattr(self.current_menu, 'generate_random_name'):
                self.send_key(pygame.K_F2)
                return self.send_key(self.state.key_confirm)
            return self.fill_text_input()
            
        elif menu_type == "SliderMenu" or "Slider" in menu_type:
            return self.fill_sliders()
            
        elif self.current_key == "dev_progress_menu":
            if self.state.dev_progress >= self.state.dev_total_weeks:
                # Force finish (finish is usually option 0)
                self.send_key(self.state.key_home)
                return self.send_key(self.state.key_confirm)
            else:
                # Still developing, go back to game_menu
                return self.send_key(self.state.key_back)
                
        elif self.current_key == "game_menu":
            # Idle/Base check
            
            # 1. Mails prüfen
            unread = [e for e in self.state.emails if not getattr(e, 'is_read', True)]
            if unread and random.random() < 0.7:
                for i, opt in enumerate(self.current_menu.options):
                    if "E-Mail" in opt['text'] or "Email" in opt['text'] or "Postfach" in opt['text']:
                        self.send_key(self.state.key_home)
                        for _ in range(i): self.send_key(self.state.key_down)
                        return self.send_key(self.state.key_confirm)
            
            # 2. Entwicklung läuft?
            if self.state.is_developing:
                if self.state.dev_progress >= self.state.dev_total_weeks:
                    # Springe manuell in den DevScreen
                    # print(f"[Dev] Finished! State money: {self.state.money}")
                    self.current_key = "dev_progress_menu"
                    self.current_menu = self.factories[self.current_key]()
                    if hasattr(self.current_menu, "announce_entry"):
                        self.current_menu.announce_entry()
                    return None
                    
                # Zeit vorspulen (1 Woche)
                self.state.update_tick(15000)
                self.ticks_simulated += 1
                if hasattr(self.current_menu, 'update'):
                    self.current_menu.update()
                
                # Wenn AAA Event triggert und Spiel pausiert:
                if self.state.time_speed == 0 and getattr(self.state, "pending_dev_event", None):
                    self.state.time_speed = 1.0 
                    self.current_key = "aaa_dev_event_menu"
                    self.current_menu = self.factories[self.current_key]()
                    if hasattr(self.current_menu, "announce_entry"):
                        self.current_menu.announce_entry()
                return None
                
            # 4. Standard Zeitablauf oder Spiel entwickeln
            if random.random() < 0.3:
                self.state.update_tick(15000)
                self.ticks_simulated += 1
                return None
                
            # Erhöhe Chance massiv ein neues Spiel zu starten, wenn wir nichts tun
            if not self.state.is_developing and random.random() < 0.5:
                # Entwickeln-Button ist meist Index 0 im game_menu
                self.send_key(self.state.key_home)
                return self.send_key(self.state.key_confirm)
                
            # 5. Menüs öffnen (Random)
            return self.navigate_standard_menu()

        elif self.current_key == "main_menu":
            # Erhöhe Chance auf 'Neues Spiel' (Index 0), um nicht ewig im Hauptmenü festzuhängen
            if random.random() < 0.3:
                self.send_key(self.state.key_home)
                return self.send_key(self.state.key_confirm)
            return self.navigate_standard_menu()
            
        else:
            return self.navigate_standard_menu()

    def run(self):
        print(f"\n{'='*60}")
        print(f"STARTE ERWEITERTEN KI-PLAYTEST: {self.language.upper()}")
        print(f"Ziel: {self.target_money:,} EUR, Max Wochen: {self.max_weeks}")
        print(f"{'='*60}")
        
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        
        loops = 0
        max_loops = self.max_weeks * 20 # Höheres Loop-Limit durch Menü-Tasten
        
        while loops < max_loops:
            loops += 1
            res = self.think_and_act()
            
            # Bei Erfolg quit signalisieren
            if getattr(self, 'successful', False):
                print(f"[Success] Reached target money!")
                break
                
            if res == "quit" or self.crashes >= 3 or self.state.week >= self.max_weeks:
                print(f"[Quit] Loops: {loops}, Res: {res}, Week: {self.state.week}")
                break
                
        pygame.quit()
        
        print(f"\n--- Simulation beendet ({self.language.upper()}) ---")
        print(f"Dauer: {self.state.week} Wochen ({self.state.week//52} Jahre)")
        print(f"Endkontostand: {self.state.money:,} Euro")
        print(f"Spiele entwickelt: {len(self.state.game_history)}")
        print(f"Menü-Crashes: {self.crashes}")
        
        return self.successful and self.crashes == 0

if __name__ == "__main__":
    try:
        agent_de = AIAgent(language='de', target_money=500000, max_weeks=3000)
        success_de = agent_de.run()
        
        if success_de:
            print("\nDEUTSCH TEST ERFOLGREICH!")
            
            agent_en = AIAgent(language='en', target_money=500000, max_weeks=3000)
            success_en = agent_en.run()
            
            if success_en:
                print("\nENGLISCH TEST ERFOLGREICH!")
                print("\n" + "#"*40)
                print("ALLE TESTS ERFOLGREICH BESTANDEN OHNE CRASHES!")
                print("#"*40)
                sys.exit(0)
            else:
                print("\nENGLISCH TEST FEHLGESCHLAGEN (Oder Crashes gefunden)!")
                sys.exit(1)
        else:
            print("\nDEUTSCH TEST FEHLGESCHLAGEN (Oder Crashes gefunden)!")
            sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
