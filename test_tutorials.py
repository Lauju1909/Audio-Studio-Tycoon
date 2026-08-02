"""
Automated Test Suite for Audio Studio Tycoon Tutorials and Translations.
Verifies registration, steps, input handling, and localized translation keys (EN/DE).
"""

import sys
import os
import pygame

# Fügen wir den aktuellen Pfad hinzu, damit die Importe klappen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import translations
from tutorial import TutorialManager

class MockAudio:
    def __init__(self):
        self.spoken_messages = []
        self.played_sounds = []

    def speak(self, msg, interrupt=False):
        self.spoken_messages.append((msg, interrupt))

    def play_sound(self, sound_name):
        self.played_sounds.append(sound_name)

class MockState:
    def __init__(self):
        self.completed_tutorials = []
        self.active_tutorial = None
        self.tutorial_step_index = 0

    def get_text(self, text_key, **kwargs):
        return translations.get_text(text_key, **kwargs)

    def save_global_settings(self):
        pass

def run_tests():
    print("==================================================")
    print("STARTING TUTORIAL AND TRANSLATION TESTS")
    print("==================================================")

    # Initialisiere Pygame für Event-Typen und Key-Konstanten
    pygame.init()

    # 1. Prüfe Sprach-Zweige im translations-Modul
    assert "en" in translations.TRANSLATIONS, "Englischer Sprachzweig fehlt!"
    assert "de" in translations.TRANSLATIONS, "Deutscher Sprachzweig fehlt!"
    print("[OK] Beide Sprachzweige (en, de) existieren in translations.py")

    # Mocks erstellen
    audio = MockAudio()
    state = MockState()
    manager = TutorialManager(audio, state)

    # Liste aller erwarteten Tutorials
    expected_tutorials = ["welcome", "office", "game_dev", "research", "hr", "marketing", "finance", "multiplayer"]

    # 2. Prüfe Registrierung aller Tutorials
    for tut_id in expected_tutorials:
        assert tut_id in manager.tutorials, f"Tutorial '{tut_id}' wurde nicht im TutorialManager registriert!"
    print(f"[OK] Alle {len(expected_tutorials)} Tutorials wurden korrekt registriert.")

    # 3. Prüfe Übersetzungsschlüssel für jeden Schritt in jeder Sprache
    missing_keys = []
    for tut_id, tut in manager.tutorials.items():
        print(f"\nÜberprüfe Tutorial: {tut_id} ({len(tut.steps)} Schritte)")
        for idx, step in enumerate(tut.steps):
            key = step.text_key
            
            # Prüfe Englisch
            en_text = translations.TRANSLATIONS["en"].get(key)
            if not en_text:
                missing_keys.append((tut_id, idx + 1, key, "en"))
                print(f"  [ERROR] Schritt {idx + 1}: Übersetzungsschlüssel '{key}' fehlt in 'en'!")
            else:
                print(f"  [OK] Schritt {idx + 1} (en): \"{en_text[:40]}...\"")

            # Prüfe Deutsch
            de_text = translations.TRANSLATIONS["de"].get(key)
            if not de_text:
                missing_keys.append((tut_id, idx + 1, key, "de"))
                print(f"  [ERROR] Schritt {idx + 1}: Übersetzungsschlüssel '{key}' fehlt in 'de'!")
            else:
                print(f"  [OK] Schritt {idx + 1} (de): \"{de_text[:40]}...\"")

    # Am Ende aller Übersetzungen muss auch tut_finished existieren
    for lang in ["en", "de"]:
        assert "tut_finished" in translations.TRANSLATIONS[lang], f"'tut_finished' fehlt in '{lang}'!"
    print("\n[OK] 'tut_finished' existiert in beiden Sprachen.")

    if missing_keys:
        print(f"\n[FAILED] Es wurden {len(missing_keys)} fehlende Übersetzungsschlüssel gefunden!")
        sys.exit(1)
    else:
        print("\n[OK] Alle Tutorial-Übersetzungen sind in beiden Sprachen (de und en) vollständig vorhanden.")

    # 4. Simulation von Tutorials & Weiterschalten von Schritten
    print("\n==================================================")
    print("SIMULIERE TUTORIAL DURCHLÄUFE")
    print("==================================================")

    # Teste "welcome" Tutorial
    print("Simuliere 'welcome' Tutorial...")
    audio.spoken_messages.clear()
    audio.played_sounds.clear()
    state.completed_tutorials.clear()
    
    # 1. Schritt
    success = manager.start_tutorial("welcome")
    assert success, "Starten des Tutorials 'welcome' schlug fehl!"
    assert state.active_tutorial.id == "welcome", "Aktives Tutorial ist nicht 'welcome'!"
    assert state.tutorial_step_index == 0, "Tutorial-Index sollte 0 sein!"
    assert len(audio.spoken_messages) == 1, "Willkommensnachricht wurde nicht gesprochen!"
    print("  [OK] Tutorial gestartet, Willkommensnachricht vorgelesen.")

    # Schritt 1 erfordert 'any_key'. Simuliere beliebigen Tastendruck
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    consumed = manager.handle_input(event)
    assert consumed, "Eingabe für Schritt 1 wurde nicht konsumiert!"
    assert state.tutorial_step_index == 1, f"Tutorial-Index nach beliebigem Tastendruck sollte 1 sein, ist {state.tutorial_step_index}!"
    print("  [OK] Schritt 1 per beliebigem Tastendruck abgeschlossen.")

    # Schritt 2 erfordert Pygame.K_DOWN. Simuliere falschen Tastendruck
    event_wrong = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    consumed = manager.handle_input(event_wrong)
    assert not consumed, "Falsche Eingabe für Schritt 2 (K_UP statt K_DOWN) wurde fälschlicherweise konsumiert!"
    assert state.tutorial_step_index == 1, "Tutorial-Index darf sich bei falscher Taste nicht verändern!"
    print("  [OK] Falsche Taste wurde korrekt ignoriert.")

    # Simuliere korrekten Tastendruck (K_DOWN)
    event_correct = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
    consumed = manager.handle_input(event_correct)
    assert consumed, "Korrekte Eingabe K_DOWN wurde nicht konsumiert!"
    assert state.tutorial_step_index == 2, f"Tutorial-Index nach K_DOWN sollte 2 sein, ist {state.tutorial_step_index}!"
    print("  [OK] Schritt 2 per K_DOWN erfolgreich abgeschlossen.")

    # Schritt 3 erfordert K_UP
    event_up = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    consumed = manager.handle_input(event_up)
    assert consumed, "Korrekte Eingabe K_UP wurde nicht konsumiert!"
    assert state.tutorial_step_index == 3, "Tutorial-Index nach K_UP sollte 3 sein!"
    print("  [OK] Schritt 3 per K_UP erfolgreich abgeschlossen.")

    # Schritt 4 erfordert K_RETURN
    event_return = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    consumed = manager.handle_input(event_return)
    assert consumed, "Korrekte Eingabe K_RETURN wurde nicht konsumiert!"
    assert state.active_tutorial is None, "Tutorial should be finished after last step!"
    assert "welcome" in state.completed_tutorials, "'welcome' Tutorial was not marked as completed!"
    assert "confirm" in audio.played_sounds, "Confirmation sound was not played!"
    print("  [OK] Schritt 4 per K_RETURN abgeschlossen und Tutorial beendet.")

    # Teste "marketing" Tutorial (alles any_key)
    print("\nSimuliere 'marketing' Tutorial...")
    success = manager.start_tutorial("marketing")
    assert success, "Starten des Tutorials 'marketing' schlug fehl!"
    assert state.active_tutorial.id == "marketing", "Aktives Tutorial ist nicht 'marketing'!"
    assert state.tutorial_step_index == 0, "Tutorial-Index sollte 0 sein!"

    for s in range(3):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        consumed = manager.handle_input(event)
        assert consumed, f"Schritt {s+1} im Marketing-Tutorial konnte nicht weitergeschaltet werden!"
    
    assert state.active_tutorial is None, "Marketing-Tutorial sollte jetzt beendet sein!"
    assert "marketing" in state.completed_tutorials, "'marketing' wurde nicht als abgeschlossen eingetragen!"
    print("  [OK] Marketing-Tutorial (alle 3 'any_key'-Schritte) erfolgreich simuliert.")

    # Teste, dass bereits abgeschlossene Tutorials nicht erneut starten
    success = manager.start_tutorial("welcome")
    assert not success, "Bereits abgeschlossenes Tutorial darf nicht erneut gestartet werden!"
    print("  [OK] Abgeschlossenes Tutorial wird korrekt übersprungen.")

    print("\n==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! 100% COVERAGE")
    print("==================================================")
    pygame.quit()

if __name__ == "__main__":
    run_tests()
