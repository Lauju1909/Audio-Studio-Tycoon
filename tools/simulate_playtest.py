import os
import sys
import random
import traceback

# Verzeichnis-Pfad korrigieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import GameState
from models import GameProject, Employee, EngineFeature, Engine
from game_data import (
    TOPICS, GENRES, PLATFORMS, AUDIENCES, ENGINE_FEATURES, 
    LICENSES, ADDON_DATA, BUNDLE_DATA, EMPLOYEE_ROLES, get_compatibility
)

def run_simulation(language='de', target_money=500000):
    print(f"\n{'='*60}")
    print(f"STARTE SIMULATION: Sprache={language}, Ziel={target_money:,} Euro")
    print(f"{'='*60}")
    
    state = GameState()
    state.settings['language'] = language
    state.company_name = f"SimStudio {language.upper()}"
    state.money = 50000 # Startkapital
    
    weeks_passed = 0
    max_weeks = 3000 # Erhöht auf 3000 Wochen (~60 Jahre)
    
    while state.money < target_money and weeks_passed < max_weeks:
        weeks_passed += 1
        
        # 1. Management: Mitarbeiter einstellen
        office_info = state.get_office_info()
        if len(state.employees) < office_info['max_employees'] and state.money > 35000:
            # Simuliere Einstellung
            role_data = random.choice(EMPLOYEE_ROLES)
            new_emp = Employee(name=f"Worker {len(state.employees)+1}", role_data=role_data)
            state.employees.append(new_emp)
            print(f"[Woche {state.week}] + Mitarbeiter eingestellt: {new_emp.name} ({new_emp.role})")

        # 2. Management: Büro-Upgrade
        if state.money > 250000 and state.office_level < 2:
            if state.upgrade_office():
                print(f"[Woche {state.week}] ++ Büro auf Level {state.office_level} aufgerüstet!")

        # 3. Forschung
        if not state.is_developing and state.money > 50000:
            # Suche nach ungelösten Features
            for feat_data in ENGINE_FEATURES:
                if feat_data['name'] not in [f.name for f in state.unlocked_features]:
                    if state.money >= feat_data['cost'] + 20000:
                        state.start_research(feat_data, "feature")
                        print(f"[Woche {state.week}] * Forschung gestartet: {feat_data['name']}")
                        # Simuliere Forschungsdauer
                        state.week += 4
                        state.complete_research()
                        break

        # 4. Engine Erstellung
        if len(state.unlocked_features) > (len(state.engines) * 3) and state.money > 80000:
            new_engine = Engine(f"SuperEngine v{len(state.engines)+1}", state.unlocked_features.copy())
            state.engines.append(new_engine)
            print(f"[Woche {state.week}] # Neue Engine erstellt: {new_engine.name}")

        # 5. Lizenzen kaufen
        if state.money > 150000 and len(state.owned_licenses) < 3:
            lic_idx = random.randrange(len(LICENSES))
            if state.buy_license(lic_idx):
                print(f"[Woche {state.week}] $ Lizenz gekauft: {LICENSES[lic_idx]['name']}")

        # 6. Spielentwicklung
        if not state.is_developing:
            # Wähle gute Kombi
            best_topic = random.choice(TOPICS)
            best_genre = random.choice(GENRES)
            for _ in range(15):
                t = random.choice(TOPICS)
                g = random.choice(GENRES)
                if get_compatibility(t, g) >= 3.0: # Strengere Wahl für mehr Erfolg
                    best_topic, best_genre = t, g
                    break
            
            avail_platforms = [p['name'] for p in PLATFORMS if p['available_week'] <= state.week and (p['end_week'] is None or p['end_week'] >= state.week)]
            proj_platform = random.choice(avail_platforms) if avail_platforms else "PC (MS-DOS)"

            # Lizenz nutzen?
            active_lics = state.get_active_licenses()
            used_lic_name = None
            if active_lics:
                used_lic_name = active_lics[0]['name']

            proj = GameProject(
                name=f"Game {len(state.game_history)+1}",
                topic=best_topic,
                genre=best_genre,
                sliders={"Gameplay": 8, "Grafik": 7, "Sound": 6, "Story": 5, "KI": 5, "Welt": 4},
                platform=proj_platform,
                audience="Jeder",
                engine=state.engines[-1] if state.engines else None,
                size="Mittel" if len(state.employees) >= 2 else "Klein",
                marketing="Große Kampagne" if state.money > 200000 else "Mittelgroße Kampagne"
            )
            
            state.current_draft = {
                "topic": proj.topic,
                "genre": proj.genre,
                "sub_genre": None,
                "platform": proj.platform,
                "audience": proj.audience,
                "size": proj.size,
                "marketing": proj.marketing,
                "engine": proj.engine
            }
            
            if used_lic_name:
                state.use_license(used_lic_name)
            
            state.finalize_game(proj)
            last_game = state.game_history[-1]
            print(f"[Woche {state.week}] !!! Spiel veröffentlicht: {last_game.name} ({last_game.topic}/{last_game.genre})")
            print(f"      Score: {last_game.review.average:.1f} | Sales: {last_game.sales:,} | Gewinn: {last_game.revenue - last_game.dev_cost:,} Euro")
            print(f"      Status: Geld={state.money:,} | Fans={state.fans:,}")

        # 7. Addons (Phase B)
        if len(state.game_history) > 2 and random.random() < 0.1:
            best_game_idx = 0
            max_rev = 0
            for i, g in enumerate(state.game_history):
                if g.revenue > max_rev:
                    max_rev = g.revenue
                    best_game_idx = i
            
            addon = state.create_addon(best_game_idx)
            if addon:
                print(f"[Woche {state.week}] + Addon veröffentlicht für {state.game_history[best_game_idx].name} (Gewinn: {addon['revenue'] - addon['cost']:,} Euro)")

        # 8. Marktanalyse Simulation (für GOTY etc.)
        if state.week % 52 == 0:
            print(f"--- Jahreswechsel Jahr {state.week//52} ---")

        if state.is_bankrupt():
            print(f"\n!!! BANKROTT IN WOCHE {state.week} !!!")
            return False

    print(f"\n--- Simulation {language.upper()} beendet ---")
    print(f"Dauer: {state.week} Wochen ({state.week//52} Jahre)")
    print(f"Endkontostand: {state.money:,} Euro")
    print(f"Fans: {state.fans:,}")
    print(f"Spiele: {len(state.game_history)}")
    
    if state.money >= target_money:
        return True
    return False

if __name__ == "__main__":
    try:
        success_de = run_simulation('de', 500000)
        if success_de:
            print("\nDEUTSCH TEST ERFOLGREICH!")
            success_en = run_simulation('en', 500000)
            if success_en:
                print("\nENGLISCH TEST ERFOLGREICH!")
                print("\n" + "#"*40)
                print("ALLE TESTS ERFOLGREICH BESTANDEN!")
                print("#"*40)
                sys.exit(0)
            else:
                print("\nENGLISCH TEST FEHLGESCHLAGEN!")
        else:
            print("\nDEUTSCH TEST FEHLGESCHLAGEN!")
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
