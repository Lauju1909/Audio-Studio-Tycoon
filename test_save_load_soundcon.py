import os
from logic import GameState
from models import SoundtrackLabel

def run_test():
    print("Starte automatischen Save/Load Test für SoundCon & Soundtrack-Labels...")
    
    # 1. Initialisiere GameState
    state = GameState()
    state.company_name = "Test Audio Studios"
    state.money = 200000  # Genug Geld zum Gründen und Buchen
    
    # Verifiziere Ausgangszustand
    assert state.soundtrack_label is None, "Fehler: Soundtrack-Label sollte initial None sein"
    assert state.active_soundcon is None, "Fehler: Aktive SoundCon sollte initial None sein"
    assert len(state.soundcon_history) == 0, "Fehler: SoundCon-Historie sollte leer sein"
    
    # 2. Gründe ein Soundtrack-Label
    print("Gründe Soundtrack-Label...")
    success = state.found_soundtrack_label("Rockin Records")
    assert success is True, "Fehler beim Gründen des Labels"
    assert state.soundtrack_label is not None, "Fehler: Label wurde nicht erstellt"
    assert state.soundtrack_label.label_name == "Rockin Records", "Fehler beim Labelnamen"
    assert state.money == 170000, f"Guthaben nach Labelgründung falsch: {state.money}"
    
    # 3. Schließe einen Radiovertrag ab
    print("Schließe Radiovertrag ab...")
    station_data = SoundtrackLabel.RADIO_STATIONS[0] # GameFM
    success_radio = state.sign_radio_contract(station_data)
    assert success_radio is True, "Fehler beim Abschließen des Radiovertrags"
    assert len(state.soundtrack_label.radio_contracts) == 1, "Fehler: Radiovertrag fehlt im Label"
    assert state.soundtrack_label.radio_contracts[0].station_name == "GameFM", "Falscher Sendername im Vertrag"
    assert state.money == 160000, f"Guthaben nach Radiovertrag falsch: {state.money}"
    
    # 4. Buche SoundCon Messestand
    print("Buche SoundCon Messestand...")
    success_booth = state.book_soundcon_booth("mittel")
    assert success_booth is True, "Fehler beim Buchen des Messestands"
    assert state.active_soundcon is not None, "Fehler: Aktive SoundCon fehlt"
    assert state.active_soundcon.booth_tier == "mittel", "Falsche Standgröße"
    assert state.money == 140000, f"Guthaben nach Standbuchung falsch: {state.money}"
    
    # Mache Q&A Runde
    state.conduct_soundcon_qa()
    assert state.active_soundcon.qa_rounds == 1, "Q&A Rundenanzahl falsch"
    
    # 5. Speichere Spielstand in Slot 9 (Test-Slot)
    print("Speichere Spielstand in Slot 9...")
    save_success = state.save_game(slot=9)
    assert save_success is True, "Speichern fehlgeschlagen"
    assert os.path.exists("save_slot_9.json"), "Speicherdatei existiert nicht"
    
    # 6. Lade Spielstand in einen frischen GameState
    print("Lade Spielstand in einen neuen GameState...")
    loaded_state = GameState()
    load_success = loaded_state.load_game(slot=9)
    assert load_success is True, "Laden fehlgeschlagen"
    
    # 7. Verifiziere geladene Daten
    print("Verifiziere geladene Daten...")
    assert loaded_state.company_name == "Test Audio Studios", "Firmenname fehlerhaft geladen"
    assert loaded_state.money == 140000, f"Geladenes Guthaben falsch: {loaded_state.money}"
    
    # SoundCon Verifikation
    assert loaded_state.active_soundcon is not None, "Geladene aktive SoundCon fehlt"
    assert loaded_state.active_soundcon.booth_tier == "mittel", "Geladene Standgröße falsch"
    assert loaded_state.active_soundcon.qa_rounds == 1, "Geladene Q&A Rundenanzahl falsch"
    assert loaded_state.active_soundcon.year == state.get_calendar_year(), "Geladenes SoundCon Jahr falsch"
    
    # Soundtrack-Label Verifikation
    assert loaded_state.soundtrack_label is not None, "Geladenes Soundtrack-Label fehlt"
    assert loaded_state.soundtrack_label.label_name == "Rockin Records", "Geladener Labelname falsch"
    assert len(loaded_state.soundtrack_label.radio_contracts) == 1, "Geladener Radiovertrag fehlt"
    assert loaded_state.soundtrack_label.radio_contracts[0].station_name == "GameFM", "Geladener Radio-Sendername falsch"
    assert loaded_state.soundtrack_label.radio_contracts[0].weeks_remaining == 26, "Geladene Restwochen falsch"
    
    # Säubere Speicherdatei
    os.remove("save_slot_9.json")
    print("--- ALL TESTS PASSED! ---")

if __name__ == "__main__":
    run_test()
