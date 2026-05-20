"""
Dezidiertes Testskript zur Verifizierung der Hype-Boost-Fehlerbehebung
und des Speicher-Leak-Fixes für historische Ereignisse in Audio Studio Tycoon.
"""

import sys
import os
import pygame

# Aktuellen Pfad hinzufügen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic import GameState, GameProject
from game_data import RANDOM_EVENTS, YEAR_EVENTS

class MockAudio:
    def speak(self, msg, interrupt=False):
        pass
    def play_sound(self, sound_name):
        pass

def run_tests():
    print("==================================================")
    # Pygame headless initialisieren
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()

    print("INITIALISIERE GAMESTATE...")
    state = GameState()
    state.audio = MockAudio()

    print("\n1. TEST: HYPE_BOOST EVENT 'viral_post'")
    # Finde das viral_post Event
    viral_post_event = next((e for e in RANDOM_EVENTS if e["id"] == "viral_post"), None)
    assert viral_post_event is not None, "viral_post Event konnte in game_data.py nicht gefunden werden!"

    # Wende das Event an
    print("Wende 'viral_post' an...")
    state.apply_event(viral_post_event)

    # Verifiziere, dass es in active_events liegt (da es eine duration besitzt)
    assert any(e["id"] == "viral_post" for e in state.active_events), "viral_post Event wurde nicht zu active_events hinzugefügt!"
    print("[OK] viral_post erfolgreich in active_events abgelegt (Dank duration-Check).")

    # Erstelle ein Mock-Projekt
    project = GameProject(name="Test-Soundtrack", size="B-Seite", genre="Ambient", topic="Natur")
    project.marketing = "small" # Standard-Marketing

    # Berechne den Hype
    print("Berechne Hype für Projekt...")
    try:
        hype_value = state.calculate_hype(project)
        print(f"[OK] Hype-Berechnung erfolgreich! Berechneter Hype: {hype_value}")
        # Hype sollte erhöht sein: Marketing small (10) * efficiency (1.0) + viral_post boost (50) = 60
        assert hype_value >= 60, f"Erwarteter Hype mindestens 60, erhalten: {hype_value}"
    except KeyError as e:
        print(f"[FAILED] Hype-Berechnung stürzte mit KeyError ab: {e}")
        sys.exit(1)

    print("\n2. TEST: EVENT-DAUER WÖCHENTLICH VERFOLGEN")
    # Das Event hat eine Dauer von 2 Wochen. Lass uns 1 Woche vergehen lassen
    print("Simuliere 1 Woche...")
    state.week += 1
    state._on_new_week()
    # viral_post sollte noch aktiv sein (Dauer 1 Woche verbleibend)
    event_in_active = next((e for e in state.active_events if e["id"] == "viral_post"), None)
    assert event_in_active is not None, "viral_post wurde zu früh entfernt!"
    assert event_in_active["duration"] == 1, f"Dauer sollte 1 sein, ist {event_in_active['duration']}"
    print("[OK] viral_post verbleibende Dauer beträgt korrekt 1 Woche.")

    # Lass uns eine zweite Woche vergehen lassen
    print("Simuliere 2. Woche...")
    state.week += 1
    state._on_new_week()
    # viral_post sollte nun abgelaufen und entfernt worden sein
    assert not any(e["id"] == "viral_post" for e in state.active_events), "viral_post wurde nach Ablauf der Dauer nicht entfernt!"
    print("[OK] viral_post wurde nach Ablauf von 2 Wochen korrekt entfernt.")

    print("\n3. TEST: SPEICHER-LEAK DURCH HISTORISCHE EVENTS")
    # Setze das Jahr zurück auf 1930 (Weltwirtschaftskrise)
    # START_YEAR ist 1930. Die erste Woche ist Woche 1.
    # Wir löschen alle aktiven Events und leeren die E-Mails
    state.active_events.clear()
    state.emails.clear()

    # Wir rufen _unlock_historical_topics() direkt auf, da dies beim Jahreswechsel passiert
    print("Schalte historische Ereignisse für 1930 frei...")
    state._unlock_historical_topics(silent=False)

    # Überprüfe, dass eine E-Mail über das historische Ereignis gesendet wurde
    assert len(state.emails) > 0, "Keine E-Mail zum historischen Ereignis gesendet!"
    print(f"[OK] Benachrichtigungs-E-Mail gesendet: {state.emails[0].subject}")

    # Überprüfe, dass das historische Ereignis NICHT in active_events liegt!
    assert len(state.active_events) == 0, f"Historisches Ereignis wurde fälschlicherweise zu active_events hinzugefügt! Inhalt: {state.active_events}"
    print("[OK] Historisches Ereignis wurde nicht zu active_events hinzugefügt (Speicher-Leak behoben).")

    print("\n==================================================")
    print("ALL FIXES VERIFIED SUCCESSFULLY!")
    print("==================================================")
    pygame.quit()

if __name__ == "__main__":
    run_tests()
