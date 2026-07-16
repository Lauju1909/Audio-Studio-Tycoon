import sys
import traceback

from logic import GameState
from models import GameProject

def run_bot():
    print("Starte Bot-Test für 100 Runden...")
    state = GameState()
    state.money = 100000000  # Genug Geld
    
    class DummyAudio:
        def play_sound(self, *args, **kwargs): pass
        def speak(self, *args, **kwargs): pass
        def play_music(self, *args, **kwargs): pass
        def stop_music(self, *args, **kwargs): pass
        def set_music_volume(self, *args, **kwargs): pass

    state.audio = DummyAudio()
    
    rounds = 100
    for r in range(1, rounds + 1):
        try:
            state.current_draft = {
                "name": f"Bot Game {r}",
                "topic": "Fantasy",
                "genre": "RPG",
                "platform": {"name": "PC", "market_multi": 1.0},
                "audience": "Jeder",
                "engine": state.engines[0] if state.engines else None,
                "size": "Mittel",
                "marketing": "none",
                "sliders": {"Gameplay": 50, "Graphics": 50, "Story": 50, "Sound": 50}
            }
            state.start_development()
            
            ap = state.active_projects[-1]
            week_count = 0
            while not ap["ready_to_finish"]:
                state.update_tick(15000) # 15000ms = 1 Woche
                week_count += 1
                
                # Unpause and clear blocking events to keep bot running
                if state.time_speed == 0:
                    state.time_speed = 1.0
                state.pause_for_menu = False
                state.pending_headhunt_event = None
                state.pending_union_event = None
                state.pending_dev_event = None
                state.pending_influencer_event = None
                state.pending_goty_results = None
                
                if week_count > 1000:
                    print("TIMEOUT in Runde", r, "Wochen:", week_count, "Bugs:", ap.get('bugs'), "Progress:", ap.get('progress'))
                    sys.exit(1)
                
            state.finalize_game(ap)
            print(f"Runde {r} abgeschlossen: {ap['project'].name} veröffentlicht. Fans: {state.fans}")
        except Exception as e:
            print(f"Fehler in Runde {r}:")
            traceback.print_exc()
            sys.exit(1)

    print(f"100 Runden erfolgreich abgeschlossen. Spiele: {len(state.game_history)}")
    
if __name__ == "__main__":
    run_bot()
