import pygame
from menus.base import Menu
from translations import get_text

class BuildMenu(Menu):
    """
    Erweitertes Menü für den Büro-Ausbau.
    Unterstützt Strukturen (Wände/Türen), Möbel und Abreißen.
    """
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.title = get_text('menu_build_office')
        self.cursor_x = 0
        self.cursor_y = 0
        
        # Zustände: "navigation", "mode_selection", "item_selection"
        self.state = "navigation"
        self.selected_category = None # "structure", "furniture"
        self.category_items = []
        self.category_idx = 0
        
        super().__init__(self.title, [], audio, game_state)

    def announce_entry(self):
        self.audio.speak(self.title)
        self._speak_position()

    def _speak_position(self):
        item = self.game_state.office_grid[self.cursor_y][self.cursor_x]
        from game_data import BUILD_OBJECTS
        item_text = get_text('empty')
        if item:
            item_id = item["type"]
            item_text = BUILD_OBJECTS.get(item_id, {}).get("name", item_id)
            
        pos_text = f"X {self.cursor_x}, Y {self.cursor_y}. {item_text}"
        self._play_radar_cues()
        self.audio.speak(pos_text)

    def _play_radar_cues(self):
        """Akustisches Feedback über Objekte in der Nachbarschaft."""
        found_count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0: continue
                nx, ny = self.cursor_x + dx, self.cursor_y + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    if self.game_state.office_grid[ny][nx] is not None:
                        found_count += 1
        if found_count > 0:
            # Ein kurzer Klick-Sound signalisiert 'etwas im Radar'
            self.audio.play_sound("click")

    def _check_req(self, obj_dict):
        req = obj_dict.get("req_tech")
        if not req: return True
        return req in self.game_state.unlocked_technologies

    def _announce_inventory(self):
        from game_data import BUILD_OBJECTS
        counts = {}
        for item in self.game_state.office_items:
            t = item.get("type")
            if t in counts:
                counts[t] += 1
            else:
                counts[t] = 1
                
        if not counts:
            self.audio.speak("Dein Büro ist komplett leer.")
            return
            
        parts = []
        for k, v in counts.items():
            name = BUILD_OBJECTS.get(k, {}).get("name", k)
            parts.append(f"{v} mal {name}")
            
        msg = "Inventar: " + ", ".join(parts)
        self.audio.speak(msg)

    def handle_input(self, event):
        gs = self.game_state
        t = gs.get_text

        if event.key == pygame.K_TAB:
            if self.state == "navigation":
                self.state = "mode_selection"
                self._announce_category()
            else:
                self.state = "navigation"
                self._speak_position()
            return None

        if event.key == pygame.K_i:
            self._announce_inventory()
            return None

        if self.state == "mode_selection":
            if event.key == gs.key_up:
                self.category_idx = (self.category_idx - 1) % 3
                self._announce_category()
            elif event.key == gs.key_down:
                self.category_idx = (self.category_idx + 1) % 3
                self._announce_category()
            elif event.key == gs.key_confirm:
                self._select_mode()
            elif event.key == gs.key_back:
                self.state = "navigation"
                self._speak_position()
            return None

        if self.state == "item_selection":
            if event.key == gs.key_up:
                self.item_idx = (self.item_idx - 1) % len(self.category_items)
                self._announce_item()
            elif event.key == gs.key_down:
                self.item_idx = (self.item_idx + 1) % len(self.category_items)
                self._announce_item()
            elif event.key == gs.key_confirm:
                self.state = "placement"
                self.audio.play_sound("click")
                self.audio.speak(get_text('build_placement_mode', default="Platzieren. Bewegen und Enter drücken."))
            elif event.key == gs.key_back:
                self.state = "mode_selection"
                self._announce_category()
            return None

        if self.state == "placement":
            if event.key == gs.key_up and self.cursor_y > 0:
                self.cursor_y -= 1
                self._speak_position()
            elif event.key == gs.key_down and self.cursor_y < 9:
                self.cursor_y += 1
                self._speak_position()
            elif event.key == pygame.K_LEFT and self.cursor_x > 0:
                self.cursor_x -= 1
                self._speak_position()
            elif event.key == pygame.K_RIGHT and self.cursor_x < 9:
                self.cursor_x += 1
                self._speak_position()
            elif event.key == gs.key_confirm:
                self._confirm_placement()
            elif event.key == gs.key_back:
                self.state = "item_selection"
                self._announce_item()
            return None

        # Navigation-Modus
        if event.key == gs.key_up and self.cursor_y > 0:
            self.cursor_y -= 1
            self._speak_position()
        elif event.key == gs.key_down and self.cursor_y < 9:
            self.cursor_y += 1
            self._speak_position()
        elif event.key == pygame.K_LEFT and self.cursor_x > 0:
            self.cursor_x -= 1
            self._speak_position()
        elif event.key == pygame.K_RIGHT and self.cursor_x < 9:
            self.cursor_x += 1
            self._speak_position()
        elif event.key == gs.key_confirm:
            self.state = "mode_selection"
            self.category_idx = 0
            self._announce_category()
        elif event.key == gs.key_back:
            return "office_menu"
            
        return None

    def _announce_category(self):
        cats = [get_text('build_cat_structure'), get_text('build_cat_furniture'), get_text('build_cat_remove')]
        self.audio.speak(cats[self.category_idx])

    def _select_mode(self):
        from game_data import BUILD_OBJECTS
        if self.category_idx == 0: # Strukturen
            self.category_items = [k for k,v in BUILD_OBJECTS.items() if v["layer"] == "structure" and self._check_req(v)]
            if not self.category_items:
                self.audio.speak("Keine Strukturen verfügbar.")
                return
            self.state = "item_selection"
            self.item_idx = 0
            self._announce_item()
        elif self.category_idx == 1: # Möbel
            self.category_items = [k for k,v in BUILD_OBJECTS.items() if v["layer"] == "furniture" and self._check_req(v)]
            if not self.category_items:
                self.audio.speak("Keine Möbel verfügbar.")
                return
            self.state = "item_selection"
            self.item_idx = 0
            self._announce_item()
        else: # Abreißen
            success = self.game_state.remove_office_item(self.cursor_x, self.cursor_y)
            if success:
                self.audio.play_sound("confirm")
                self.audio.speak(get_text('build_remove_success'))
            else:
                self.audio.play_sound("error")
                self.audio.speak(get_text('build_remove_failed'))
            self.state = "navigation"
            self._speak_position()

    def _announce_item(self):
        from game_data import BUILD_OBJECTS
        item_id = self.category_items[self.item_idx]
        obj = BUILD_OBJECTS[item_id]
        text = f"{obj['name']}, {obj['cost']} Euro. {obj['desc']}"
        self.audio.speak(text)

    def _confirm_placement(self):
        item_id = self.category_items[self.item_idx]
        success, msg_key = self.game_state.place_office_item(item_id, self.cursor_x, self.cursor_y)
        if success:
            self.audio.play_sound("build")
            self.audio.speak(get_text('build_success', default="Gebaut."))
            # Wir bleiben im 'placement' state für weiteres Bauen!
        else:
            self.audio.play_sound("error")
            self.audio.speak(get_text(f'build_error_{msg_key}', default="Bau fehlgeschlagen."))

class TeambuildingMenu(Menu):
    """Menü für Team-Maßnahmen."""
    def __init__(self, audio, game_state):
        options = [
            {"text": get_text('teambuilding_pizza'), "action": lambda: self._do("Pizza")},
            {"text": get_text('teambuilding_party'), "action": lambda: self._do("Party")},
            {"text": get_text('teambuilding_trip'), "action": lambda: self._do("Ausflug")},
            {"text": get_text('back'), "action": lambda: "hr_menu"}
        ]
        super().__init__(get_text('menu_teambuilding'), options, audio, game_state)

    def _do(self, type):
        success = self.game_state.perform_teambuilding(type)
        if success:
            self.audio.play_sound("cheer")
            self.audio.speak(get_text('teambuilding_success', type=type))
        else:
            self.audio.play_sound("error")
            self.audio.speak(get_text('insufficient_funds'))

class ModPortalMenu(Menu):
    """Lokaler Datei-basierter Mod-Manager."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.mod_manager = getattr(game_state, 'mod_manager', None)
        options = []
        if self.mod_manager and hasattr(self.mod_manager, 'installed_mods'):
            for mod in self.mod_manager.installed_mods:
                is_active = self.mod_manager.is_mod_active(mod['id'])
                # Lese-Tipp: Dinosaurier Mod (Aktiv)
                status_key = 'on' if is_active else 'off'
                txt = f"{mod['name']} ({get_text(status_key)})"
                options.append({
                    "text": txt,
                    "action": lambda m=mod['id']: self._toggle_mod(m)
                })
        else:
            options.append({"text": "Fehler: Mod-Manager nicht bereit.", "action": lambda: None})

        options.append({"text": get_text('back'), "action": lambda: "main_menu"})
        super().__init__(get_text('menu_mod_portal'), options, audio, game_state)

    def _toggle_mod(self, mod_id):
        new_state = self.mod_manager.toggle_mod(mod_id)
        if new_state:
            self.audio.play_sound("confirm")
            self.audio.speak(get_text('mod_installed')) # Text wiederverwenden: "Mod aktiviert!"
        else:
            self.audio.play_sound("error")
            self.audio.speak(get_text('mod_turned_off', default="Mod deaktiviert."))
        # Menü neu laden, um Anzeige zu aktualisieren
        return "mod_portal"

class ModBrowserListMenu(Menu):
    """Dummy-Klasse für veraltete Aufrufe, falls sie noch irgendwo existieren."""
    def __init__(self, audio, game_state):
        super().__init__("Veraltet", [{"text": get_text('back'), "action": lambda: "mod_portal"}], audio, game_state)
