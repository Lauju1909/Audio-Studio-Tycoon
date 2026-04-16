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
        """Injiziert Mod-Inhalte direkt ins Laufzeit-Zentrum des Spiels (game_data)."""
        import game_data
        
        active_mod_data = [m for m in self.installed_mods if m.get("id") in self.active_mod_ids]
        
        for mod in active_mod_data:
            # Topics hinzufügen
            if "add_topics" in mod:
                for topic in mod["add_topics"]:
                    topic_name = topic.get("name") if isinstance(topic, dict) else topic
                    topic_text = topic.get("trend_text", f"{topic_name} ist gerade ein Trend!") if isinstance(topic, dict) else f"{topic_name} ist gerade ein Trend!"
                    if topic_name not in game_data.START_TOPICS:
                        game_data.START_TOPICS.append(topic_name)
                    existing_trend_names = [t["topic"] for t in game_data.TREND_TOPICS]
                    if topic_name not in existing_trend_names:
                        game_data.TREND_TOPICS.append({"topic": topic_name, "text": topic_text})

            # Genres hinzufügen
            if "add_genres" in mod:
                for genre in mod["add_genres"]:
                    genre_name = genre.get("name") if isinstance(genre, dict) else genre
                    genre_text = genre.get("trend_text", f"{genre_name} erlebt gerade einen Boom!") if isinstance(genre, dict) else f"{genre_name} erlebt gerade einen Boom!"
                    if genre_name not in game_data.START_GENRES:
                        game_data.START_GENRES.append(genre_name)
                    existing_trend_genres = [g["genre"] for g in game_data.TREND_GENRES]
                    if genre_name not in existing_trend_genres:
                        game_data.TREND_GENRES.append({"genre": genre_name, "text": genre_text})

            # Engine-Features hinzufügen
            if "add_engine_features" in mod:
                for feature in mod["add_engine_features"]:
                    if feature.get("name") not in [f["name"] for f in game_data.ENGINE_FEATURES]:
                        game_data.ENGINE_FEATURES.append(feature)

            # Büro-Einrichtung / Objekte hinzufügen
            if "add_office_rooms" in mod:
                for item_id, item_data in mod["add_office_rooms"].items():
                    if item_id not in game_data.BUILD_OBJECTS:
                        game_data.BUILD_OBJECTS[item_id] = item_data
                # Alias Liste aktualisieren
                game_data.OFFICE_ROOMS = [dict(id=k, **v) for k, v in game_data.BUILD_OBJECTS.items()]

            # Mitarbeiter-Traits hinzufügen
            if "add_employee_traits" in mod:
                for trait in mod["add_employee_traits"]:
                    if trait.get("name") not in [t["name"] for t in game_data.EMPLOYEE_TRAITS]:
                        game_data.EMPLOYEE_TRAITS.append(trait)

            # Plattformen hinzufügen
            if "add_platforms" in mod:
                for platform in mod["add_platforms"]:
                    if platform.get("name") not in [p["name"] for p in game_data.PLATFORMS]:
                        game_data.PLATFORMS.append(platform)

            # Publisher hinzufügen
            if "add_publishers" in mod:
                for publisher in mod["add_publishers"]:
                    if publisher.get("name") not in [p["name"] for p in game_data.PUBLISHERS]:
                        game_data.PUBLISHERS.append(publisher)
