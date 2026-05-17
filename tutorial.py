
"""
Tutorial-System für Audio Studio Tycoon.
Verwaltet interaktive, sprachgeführte Einführungen.
"""

import pygame

class TutorialStep:
    def __init__(self, text_key, trigger_type="any_key", trigger_value=None):
        self.text_key = text_key
        self.trigger_type = trigger_type # any_key, input_key, menu_change
        self.trigger_value = trigger_value # z.B. pygame.K_UP

class Tutorial:
    def __init__(self, id, steps):
        self.id = id
        self.steps = steps

class TutorialManager:
    def __init__(self, audio, state):
        self.audio = audio
        self.state = state
        self.tutorials = self._init_tutorials()

    def _init_tutorials(self):
        return {
            "welcome": Tutorial("welcome", [
                TutorialStep("tut_welcome_1"), # Willkommen!
                TutorialStep("tut_welcome_2", "input_key", pygame.K_DOWN), # Navigiere mit Pfeiltasten. Drücke Runter.
                TutorialStep("tut_welcome_3", "input_key", pygame.K_UP), # Drücke Hoch.
                TutorialStep("tut_welcome_4", "input_key", pygame.K_RETURN), # Enter bestätigt. Wähle 'Neues Spiel'.
            ]),
            "office": Tutorial("office", [
                TutorialStep("tut_office_1"), # Dein Büro! Hier läuft die Zeit.
                TutorialStep("tut_office_2", "input_key", pygame.K_s), # Drücke S für Status.
                TutorialStep("tut_office_3", "input_key", pygame.K_f), # Drücke F für Finanzen.
                TutorialStep("tut_office_4"), # Viel Erfolg!
            ]),
            "game_dev": Tutorial("game_dev", [
                TutorialStep("tut_dev_1"), # Spielentwicklung! Wähle ein Thema.
                TutorialStep("tut_dev_2"), # Achte auf die Kombination von Thema und Genre.
                TutorialStep("tut_dev_3"), # Platformen kosten Lizenzgebühren.
                TutorialStep("tut_dev_4"), # Slider bestimmen die Qualität.
            ]),
            "research": Tutorial("research", [
                TutorialStep("tut_research_1"),
                TutorialStep("tut_research_2"),
                TutorialStep("tut_research_3"),
            ]),
            "hr": Tutorial("hr", [
                TutorialStep("tut_hr_1"),
                TutorialStep("tut_hr_2"),
                TutorialStep("tut_hr_3"),
                TutorialStep("tut_hr_4"),
            ]),
            "marketing": Tutorial("marketing", [
                TutorialStep("tut_marketing_1"),
                TutorialStep("tut_marketing_2"),
                TutorialStep("tut_marketing_3"),
            ]),
            "finance": Tutorial("finance", [
                TutorialStep("tut_finance_1"),
                TutorialStep("tut_finance_2"),
                TutorialStep("tut_finance_3"),
            ]),
            "multiplayer": Tutorial("multiplayer", [
                TutorialStep("tut_multiplayer_1"),
                TutorialStep("tut_multiplayer_2"),
                TutorialStep("tut_multiplayer_3"),
            ])
        }

    def start_tutorial(self, tut_id):
        if tut_id in self.tutorials and tut_id not in self.state.completed_tutorials:
            self.state.active_tutorial = self.tutorials[tut_id]
            self.state.tutorial_step_index = 0
            self._play_current_step()
            return True
        return False

    def _play_current_step(self):
        tut = self.state.active_tutorial
        step = tut.steps[self.state.tutorial_step_index]
        msg = self.state.get_text(step.text_key)
        self.audio.speak(msg, interrupt=True)

    def handle_input(self, event):
        if not self.state.active_tutorial:
            return False

        tut = self.state.active_tutorial
        step = tut.steps[self.state.tutorial_step_index]

        advance = False
        if step.trigger_type == "any_key":
            if event.type == pygame.KEYDOWN:
                advance = True
        elif step.trigger_type == "input_key":
            if event.type == pygame.KEYDOWN and event.key == step.trigger_value:
                advance = True
        
        if advance:
            self.state.tutorial_step_index += 1
            if self.state.tutorial_step_index >= len(tut.steps):
                self.finish_tutorial()
            else:
                self._play_current_step()
            return True # Input wurde vom Tutorial konsumiert
            
        return False # Tutorial ignoriert diesen Input (oder wartet auf speziellen)

    def finish_tutorial(self):
        if self.state.active_tutorial:
            self.state.completed_tutorials.append(self.state.active_tutorial.id)
            self.state.save_global_settings()
            self.state.active_tutorial = None
            self.audio.play_sound("confirm")
            self.audio.speak(self.state.get_text("tut_finished"), interrupt=False)
