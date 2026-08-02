import os
import json

class ModManager:
    """Verwaltet lokale Mods aus dem ./mods/ Ordner ohne Serveranbindung."""
    def __init__(self, base_path="."):
        self.mods_path = os.path.join(base_path, "mods")
        self.active_mods_file = os.path.join(base_path, "active_mods.json")
        self.installed_mods = []
        self.active_mod_ids = []
        self.ensure_paths()
        self.load_active_mod_ids()
        self.scan_installed_mods()

    def ensure_paths(self):
        if not os.path.exists(self.mods_path):
            try:
                os.makedirs(self.mods_path)
            except Exception:
                pass
        if not os.path.exists(self.active_mods_file):
            with open(self.active_mods_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_active_mod_ids(self):
        try:
            with open(self.active_mods_file, "r", encoding="utf-8") as f:
                self.active_mod_ids = json.load(f)
        except Exception:
            self.active_mod_ids = []

    def save_active_mod_ids(self):
        try:
            with open(self.active_mods_file, "w", encoding="utf-8") as f:
                json.dump(self.active_mod_ids, f, indent=4)
        except Exception as e:
            print(f"Fehler beim Speichern von active_mods.json: {e}")

    def scan_installed_mods(self):
        """Scant das Verzeichnis 'mods' auf mod.json Dateien."""
        self.installed_mods = []
        if not os.path.exists(self.mods_path):
            return

        for folder_name in os.listdir(self.mods_path):
            folder_path = os.path.join(self.mods_path, folder_name)
            mod_file = os.path.join(folder_path, "mod.json")
            if os.path.isdir(folder_path) and os.path.exists(mod_file):
                try:
                    with open(mod_file, "r", encoding="utf-8") as f:
                        mod_data = json.load(f)
                        mod_data["folder"] = folder_name
                        self.installed_mods.append(mod_data)
                except Exception as e:
                    print(f"Konnte Mod in '{folder_name}' nicht lesen: {e}")

    def get_installed_mods(self):
        return self.installed_mods

    def is_mod_active(self, mod_id):
        return mod_id in self.active_mod_ids

    def toggle_mod(self, mod_id):
        if mod_id in self.active_mod_ids:
            self.active_mod_ids.remove(mod_id)
            state = False
        else:
            self.active_mod_ids.append(mod_id)
            state = True
        self.save_active_mod_ids()
        return state

    def apply_active_mods(self):
        """Injiziert Mod-Inhalte direkt ins Laufzeit-Zentrum des Spiels (game_data) und wendet Custom Scripts/Assets an."""
        import game_data
        
        active_mod_data = [m for m in self.installed_mods if m.get("id") in self.active_mod_ids]
        
        # Sicherstellen, dass ASSET_OVERRIDES existiert
        if not hasattr(game_data, "ASSET_OVERRIDES"):
            game_data.ASSET_OVERRIDES = {}

        for mod in active_mod_data:
            try:
                mod_id = mod.get("id", "Unbekannte_Mod")
                mod_folder = mod.get("folder", "")
                
                # Topics hinzufügen
                if "add_topics" in mod:
                    try:
                        for topic in mod["add_topics"]:
                            topic_name = topic.get("name") if isinstance(topic, dict) else topic
                            topic_text = topic.get("trend_text", f"{topic_name} ist gerade ein Trend!") if isinstance(topic, dict) else f"{topic_name} ist gerade ein Trend!"
                            if topic_name not in game_data.START_TOPICS:
                                game_data.START_TOPICS.append(topic_name)
                            existing_trend_names = [t["topic"] for t in game_data.TREND_TOPICS]
                            if topic_name not in existing_trend_names:
                                game_data.TREND_TOPICS.append({"topic": topic_name, "text": topic_text})
                    except Exception as e:
                        print(f"[{mod_id}] Fehler beim Hinzufügen von Topics: {e}")

                # Genres hinzufügen
                if "add_genres" in mod:
                    try:
                        for genre in mod["add_genres"]:
                            genre_name = genre.get("name") if isinstance(genre, dict) else genre
                            genre_text = genre.get("trend_text", f"{genre_name} erlebt gerade einen Boom!") if isinstance(genre, dict) else f"{genre_name} erlebt gerade einen Boom!"
                            if genre_name not in game_data.START_GENRES:
                                game_data.START_GENRES.append(genre_name)
                            existing_trend_genres = [g["genre"] for g in game_data.TREND_GENRES]
                            if genre_name not in existing_trend_genres:
                                game_data.TREND_GENRES.append({"genre": genre_name, "text": genre_text})
                    except Exception as e:
                        print(f"[{mod_id}] Fehler beim Hinzufügen von Genres: {e}")

                # Engine-Features hinzufügen
                if "add_engine_features" in mod:
                    try:
                        for feature in mod["add_engine_features"]:
                            if feature.get("name") not in [f["name"] for f in game_data.ENGINE_FEATURES]:
                                game_data.ENGINE_FEATURES.append(feature)
                    except Exception as e:
                        print(f"[{mod_id}] Fehler beim Hinzufügen von Engine-Features: {e}")

                # Büro-Einrichtung / Objekte hinzufügen
                if "add_office_rooms" in mod:
                    try:
                        for item_id, item_data in mod["add_office_rooms"].items():
                            if item_id not in game_data.BUILD_OBJECTS:
                                game_data.BUILD_OBJECTS[item_id] = item_data
                        # Alias Liste aktualisieren
                        game_data.OFFICE_ROOMS = [dict(id=k, **v) for k, v in game_data.BUILD_OBJECTS.items()]
                    except Exception as e:
                        print(f"[{mod_id}] Fehler beim Hinzufügen von Büro-Einrichtung: {e}")

                # Mitarbeiter-Traits hinzufügen
                if "add_employee_traits" in mod:
                    try:
                        for trait in mod["add_employee_traits"]:
                            if trait.get("name") not in [t["name"] for t in game_data.EMPLOYEE_TRAITS]:
                                game_data.EMPLOYEE_TRAITS.append(trait)
                    except Exception as e:
                        print(f"[{mod_id}] Fehler beim Hinzufügen von Mitarbeiter-Traits: {e}")

                # Plattformen hinzufügen
                if "add_platforms" in mod:
                    try:
                        for platform in mod["add_platforms"]:
                            if platform.get("name") not in [p["name"] for p in game_data.PLATFORMS]:
                                game_data.PLATFORMS.append(platform)
                    except Exception as e:
                        print(f"[{mod_id}] Fehler beim Hinzufügen von Plattformen: {e}")

                # Publisher hinzufügen
                if "add_publishers" in mod:
                    try:
                        for publisher in mod["add_publishers"]:
                            if publisher.get("name") not in [p["name"] for p in game_data.PUBLISHERS]:
                                game_data.PUBLISHERS.append(publisher)
                    except Exception as e:
                        print(f"[{mod_id}] Fehler beim Hinzufügen von Publishern: {e}")
                        
                # Asset Overrides (Audio, Bilder) hinzufügen
                base_mods_dir = os.path.abspath(self.mods_path)
                if "replace_assets" in mod:
                    try:
                        for orig_asset, mod_asset in mod["replace_assets"].items():
                            mod_asset_path = os.path.join(self.mods_path, mod_folder, mod_asset)
                            real_asset_path = os.path.abspath(mod_asset_path)
                            if not os.path.commonpath([base_mods_dir, real_asset_path]) == base_mods_dir:
                                print(f"[{mod_id}] Pfadsicherheitswarnung: Versuchter Ausbruch bei Asset '{mod_asset}'")
                                continue
                            if os.path.exists(mod_asset_path):
                                game_data.ASSET_OVERRIDES[orig_asset] = mod_asset_path
                            else:
                                print(f"[{mod_id}] Asset nicht gefunden: '{mod_asset}'")
                    except Exception as e:
                        print(f"[{mod_id}] Fehler bei Asset-Overrides: {e}")
                        
                # Custom Scripts laden und ausführen
                if "custom_scripts" in mod:
                    try:
                        for script_file in mod["custom_scripts"]:
                            script_path = os.path.join(self.mods_path, mod_folder, script_file)
                            real_script_path = os.path.abspath(script_path)
                            if not os.path.commonpath([base_mods_dir, real_script_path]) == base_mods_dir:
                                print(f"[{mod_id}] Pfadsicherheitswarnung: Versuchter Ausbruch bei Script '{script_file}'")
                                continue
                            if os.path.exists(script_path):
                                try:
                                    with open(script_path, "r", encoding="utf-8") as sf:
                                        script_code = sf.read()
                                    # Exec in the context of game_data to allow modifications
                                    exec_globals = {"game_data": game_data, "os": os, "mod_id": mod_id}
                                    exec(script_code, exec_globals)
                                    print(f"[{mod_id}] Script erfolgreich ausgeführt: '{script_file}'")
                                except Exception as e:
                                    print(f"[{mod_id}] Fehler bei der Ausführung von Custom Script '{script_file}': {e}")
                            else:
                                print(f"[{mod_id}] Custom Script nicht gefunden: '{script_file}'")
                    except Exception as e:
                        print(f"[{mod_id}] Fehler beim Laden von Custom Scripts: {e}")

            except Exception as e:
                print(f"Kritischer Fehler beim Anwenden von Mod {mod.get('id', 'Unbekannt')}: {e}")
