import unittest
import pygame
from logic import GameState
from audio import AudioManager
from main import setup_router
from menus.office import VacationMenu, HRMenu, EmployeeOverviewMenu
from menus.settings import CustomLanguageInputMenu, KeybindingMenu
from menus.gameplay import ReviewResultMenu, UnionEventMenu
from menus.research import ConsoleDetailMenu
from menus.business import ESportsMenu, ESportsChampionshipMenu, ESportsSponsorMenu
from models import Employee

class TestAuditFixes(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.audio = AudioManager()
        self.router = setup_router(self.audio, self.state)

    def test_all_registered_routes_instantiate_cleanly(self):
        """Verify that every single registered route in router can be instantiated without raising errors."""
        for route_id, factory in self.router.dynamic_routes.items():
            try:
                menu = factory()
                self.assertIsNotNone(menu, f"Route {route_id} produced None")
            except Exception as e:
                self.fail(f"Route '{route_id}' failed to instantiate: {e}")

    def test_vacation_menu_and_hr(self):
        """Test VacationMenu functionality and HR integration."""
        self.state.employees.clear()
        emp1 = Employee(name="Coder Dave", role_data={"role": "Programmierer", "primary": "Programmierung", "secondary": "Design"})
        emp1.fatigue = 80
        self.state.employees.append(emp1)

        v_menu = VacationMenu(self.audio, self.state)
        # Should have option for Coder Dave
        opt_texts = [o['text'] for o in v_menu.options]
        self.assertTrue(any("Dave" in t for t in opt_texts))

        # Send on vacation
        res = v_menu._send_on_vacation(emp1)
        self.assertEqual(res, "vacation_menu")
        self.assertEqual(emp1.vacation_weeks_left, 4)

        # Overview menu should display vacation status and fatigue
        overview = EmployeeOverviewMenu(self.audio, self.state)
        self.assertTrue(any("Urlaub" in o['text'] for o in overview.options))

        # HR menu should contain vacation option
        hr = HRMenu(self.audio, self.state)
        hr_routes = [o['action']() if callable(o['action']) else o['action'] for o in hr.options]
        self.assertIn("vacation_menu", hr_routes)

    def test_custom_language_input_menu(self):
        """Ensure CustomLanguageInputMenu instantiates and handles submit without error."""
        menu = CustomLanguageInputMenu(self.audio, self.state)
        self.assertEqual(menu.title, "custom_language")
        ret = menu.on_submit("es")
        self.assertEqual(ret, "language_menu")
        self.assertEqual(self.state.settings.get("language"), "es")

    def test_keybinding_keys_left_right(self):
        """Ensure key_left and key_right are in GameState, settings, and KeybindingMenu."""
        self.assertEqual(self.state.key_left, pygame.K_LEFT)
        self.assertEqual(self.state.key_right, pygame.K_RIGHT)

        self.state.key_left = pygame.K_a
        self.state.key_right = pygame.K_d
        self.state.save_global_settings()

        # Re-load
        new_state = GameState()
        new_state.load_global_settings()
        self.assertEqual(new_state.key_left, pygame.K_a)
        self.assertEqual(new_state.key_right, pygame.K_d)

        # Reset to defaults
        self.state.key_left = pygame.K_LEFT
        self.state.key_right = pygame.K_RIGHT
        self.state.save_global_settings()

    def test_review_result_menu_empty_history(self):
        """Ensure ReviewResultMenu does not crash when game_history is empty."""
        self.state.game_history = []
        menu = ReviewResultMenu(self.audio, self.state)
        # announce_entry should not raise IndexError
        menu.announce_entry()
        self.assertTrue(len(menu.options) > 0)

    def test_union_event_menu_safety(self):
        """Ensure UnionEventMenu does not crash when pending_union_event is None."""
        self.state.pending_union_event = None
        menu = UnionEventMenu(self.audio, self.state)
        self.assertIsNotNone(menu)
        # All actions should execute cleanly
        menu._raise_salaries()
        menu._pay_bonus()
        menu._ignore()
        menu._union_busting()

    def test_console_detail_menu_safety(self):
        """Ensure ConsoleDetailMenu handles empty custom_consoles safely."""
        self.state.custom_consoles = []
        self.state.ui_context['selected_console_idx'] = 99
        menu = ConsoleDetailMenu(self.audio, self.state)
        self.assertIsNotNone(menu)

    def test_esports_menus_safety(self):
        """Ensure ESports menus don't crash on year check or empty leagues."""
        self.state.esports_leagues = []
        menu = ESportsMenu(self.audio, self.state)
        menu.announce_entry()

        champ = ESportsChampionshipMenu(self.audio, self.state)
        champ.announce_entry()

        sponsor = ESportsSponsorMenu(self.audio, self.state)
        sponsor.announce_entry()

    def test_prism_integration(self):
        """Ensure Prism is initialized, handles engine switching and speech cleanly."""
        import os
        if os.path.exists("prism.dll"):
            self.assertTrue(self.audio.prism_active)
            self.assertIsNotNone(self.audio.prism_backend)
            # Test engine switching
            self.audio.update_tts_engine("auto")
            self.audio.update_tts_engine("sapi")
            self.audio.update_tts_engine("nvda")
            self.audio.update_tts_engine("auto")

    def test_active_employees_vacation_filtering(self):
        """Ensure _active_employees excludes staff who are on vacation."""
        self.state.employees.clear()
        emp1 = Employee(name="Active Alice", role_data={"role": "Programmierer", "primary": "Programmierung", "secondary": "Design"})
        emp2 = Employee(name="Vacation Bob", role_data={"role": "Sound Designer", "primary": "Sound", "secondary": "Design"})
        emp2.vacation_weeks_left = 3
        self.state.employees.extend([emp1, emp2])

        active = self.state._active_employees()
        self.assertIn(emp1, active)
        self.assertNotIn(emp2, active)

        # Check Training employee select menu blocks vacation staff
        from menus.office import TrainingEmployeeSelectMenu
        t_menu = TrainingEmployeeSelectMenu(self.audio, self.state)
        self.assertIsNone(t_menu._select(1)) # Bob is on vacation

if __name__ == "__main__":
    unittest.main()
