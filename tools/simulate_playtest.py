import os
import sys
import random

# Verzeichnis-Pfad korrigieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import GameState
from models import GameProject, Employee, EngineFeature
from game_data import TOPICS, GENRES, PLATFORMS, AUDIENCES, ENGINE_FEATURES

def run_simulation():
    print("Starte umfassende Spielsimulation (3 In-Game-Jahre) ...")
    state = GameState()
    state.settings['language'] = 'de'
    state.company_name = "Super Code Studio"
    state.money = 1000000  # Give it lots of money for testing so it doesn't just go bankrupt 
    
    # Simuliere 1500 Loops (ca. 300 Wochen)
    for total_weeks in range(1500):
        # Update State in 1000ms Schritten (simulierte Zeit, 1 Woche ~ 1 Sekunde mit 1.0 Tempo, wir nehmen 1 Tick = 1000ms an)
        state.update_tick(1000) 
        
        # Umgehe blockierende UI-Pausen (durch Random Events oder Emails)
        if state.pause_for_menu:
            state.pause_for_menu = False
            state.active_events = []
            state.emails = []
            
        print(f"DEBUG: loop={total_weeks}, week={state.week}, time_speed={state.time_speed}")

        
        # Gelegentlich Mitarbeiter einstellen (z.B. Woche 10)
        if state.week == 10 and len(state.employees) < 2:
            new_dev = Employee(name="Simulated Dev")
            new_dev.skills = {"Design": 5, "Programmierung": 5, "Audio": 5, "Grafik": 5}
            state.employees.append(new_dev)
            print(f"[Woche {state.week}] Neuer Entwickler eingestellt!")

        # Gelegentlich Forschung betreiben (Woche 20)
        if state.week == 20:
            for feat in ENGINE_FEATURES:
                already_unlocked = any(f.name == feat['name'] for f in state.unlocked_features)
                if not already_unlocked and state.money >= feat['cost']:
                    new_feat = EngineFeature(feat['category'], feat['name'], feat['tech_bonus'])
                    state.unlocked_features.append(new_feat)
                    state.money -= feat['cost']
                    print(f"[Woche {state.week}] Engine Feature '{feat['name']}' erforscht.")
                    break

        # Gelegentlich Engine updaten (Woche 30)
        if state.week == 30 and len(state.unlocked_features) > 0 and len(state.engines) < 2:
            from models import Engine
            new_engine = Engine(f"Engine v{len(state.engines)+1}", state.unlocked_features.copy())
            state.engines.append(new_engine)
            print(f"[Woche {state.week}] Neue {new_engine.name} entwickelt!")

        # Gelegentlich Spiele entwickeln (alle 40 Wochen)
        if state.week % 40 == 0 and not state.is_developing:
            print(f"\n[Woche {state.week}] Starte neue Spieleentwicklung...")
            
            # Wähle zufällige Parameter
            proj_topic = random.choice(TOPICS)
            proj_genre = random.choice(GENRES)
            
            avail_platforms = [p for p in PLATFORMS if p['available_week'] <= state.week and (p['end_week'] is None or p['end_week'] >= state.week)]
            proj_platform = random.choice(avail_platforms)['name'] if avail_platforms else "Computer"
            
            proj_audience = random.choice(AUDIENCES)
            
            proj = GameProject(
                name=f"Sim Game {state.week}",
                topic=proj_topic,
                genre=proj_genre,
                sliders={"Gameplay": 5, "Grafik": 5, "Sound": 5, "Story": 5, "KI": 5, "Welt": 5},
                platform=proj_platform,
                audience=proj_audience,
                engine=state.engines[-1] if state.engines else None,
                size="Klein",
                marketing="Kein Marketing"
            )
            
            # Entwicklungsstart validieren
            state.finalize_game(proj)
            print(f"[Woche {state.week}] Spiel in Entwicklung => {proj.name} ({proj.topic}/{proj.genre})")
            
        # Wenn Spiel fertig, veröffentlichen
        if state.is_developing and state.dev_progress >= state.dev_total_weeks:
            print(f"[Woche {state.week}] Entwicklung abgeschlossen! Veröffentliche...")
            state.finish_game()
            
        # Überprüfe Bankrott
        if state.is_bankrupt():
            print(f"!!! BANKROTT IN WOCHE {state.week} !!!")
            break

    print("\n--- Simulation abgeschlossen ---")
    print(f"Firmenname: {state.company_name}")
    print(f"Geld am Ende: {state.money}")
    print(f"Fans am Ende: {state.fans}")
    print(f"Anzahl Entwickler: {len(state.employees)}")
    print(f"Veröffentlichte Spiele: {len(state.game_history)}")
    for g in state.game_history:
        print(f" - {g.name} (Review: {g.review.average if hasattr(g, 'review') and g.review else 'N/A'}) = {g.sales} Verkäufe")
    
    if len(state.game_history) > 0:
        print("\nTest erfolgreich: Kompletter Logik-Throughput ohne Crashes.")
    else:
        print("\nAchtung: Es wurden keine Spiele beendet (vielleicht Simulation zu kurz oder Bugs).")

if __name__ == "__main__":
    try:
        run_simulation()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\n!!! FEHLER WÄHREND DER SIMULATION !!!")
