from .base import Menu, TextInputMenu
from game_data import (
    RESEARCHABLE_TOPICS, RESEARCHABLE_GENRES, RESEARCHABLE_AUDIENCES, 
    RESEARCHABLE_TECHNOLOGIES, ENGINE_FEATURES
)

class ResearchMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('research_menu')
        options = [
            {'text': self.game_state.get_text('research_topic'), 'action': lambda: "topic_research_menu"},
            {'text': self.game_state.get_text('research_genre'), 'action': lambda: "genre_research_menu"},
            {'text': self.game_state.get_text('research_audience'), 'action': lambda: "audience_research_menu"},
            {'text': self.game_state.get_text('research_feature'), 'action': lambda: "feature_research_menu"},
            {'text': self.game_state.get_text('research_technology'), 'action': lambda: "technology_research_menu"},
            {'text': self.game_state.get_text('create_engine'), 'action': lambda: "engine_create_name"},
            {'text': self.game_state.get_text('hardware_dev'), 'action': lambda: "hardware_dev_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]
        super().__init__(title, options, audio, game_state)

class FeatureResearchMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('research_feature'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        features = self.game_state.get_researchable_features()
        for f in features:
            self.options.append({'text': f"{f['name']} ({f['cost']} EUR)", 'action': lambda feat=f: self._research(feat)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})

    def _research(self, feat):
        if self.game_state.money >= feat['cost']:
            self.game_state.start_research(feat, "feature")
            self.audio.play_sound("confirm")
            return "game_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

class TopicResearchMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('research_topic'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for t in RESEARCHABLE_TOPICS:
            if self.game_state.week < t.get("week", 1): continue
            if t["name"] not in self.game_state.unlocked_topics:
                 self.options.append({'text': f"{t['name']} ({t['cost']:,} EUR)", 'action': lambda topic=t: self._research(topic)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})

    def _research(self, topic):
        if self.game_state.money >= topic['cost']:
            if self.game_state.start_research(topic, "topic"):
                self.audio.play_sound("confirm")
                return "game_menu"
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('research_already_active'))
                return None
        return None

class GenreResearchMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('research_genre'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for g in RESEARCHABLE_GENRES:
            if self.game_state.week < g.get("week", 1): continue
            if g["name"] not in self.game_state.unlocked_genres:
                self.options.append({'text': f"{g['name']} ({g['cost']:,} EUR)", 'action': lambda gen=g: self._research(gen)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})

    def _research(self, genre):
        if self.game_state.money >= genre['cost']:
            if self.game_state.start_research(genre, "genre"):
                self.audio.play_sound("confirm")
                return "game_menu"
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('research_already_active'))
                return None
        return None

class AudienceResearchMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('research_audience'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for a in RESEARCHABLE_AUDIENCES:
            if self.game_state.week < a.get("week", 1): continue
            if a["name"] not in self.game_state.unlocked_audiences:
                self.options.append({'text': f"{a['name']} ({a['cost']:,} EUR)", 'action': lambda aud=a: self._research(aud)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})

    def _research(self, aud):
        if self.game_state.money >= aud['cost']:
            if self.game_state.start_research(aud, "audience"):
                self.audio.play_sound("confirm")
                return "game_menu"
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('research_already_active'))
                return None
        return None

class TechnologyResearchMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('research_technology'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for t in RESEARCHABLE_TECHNOLOGIES:
            if self.game_state.week < t.get("week", 1): continue
            if t["name"] not in self.game_state.unlocked_technologies:
                self.options.append({'text': f"{t['name']} ({t['cost']:,} EUR)", 'action': lambda tech=t: self._research(tech)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})

    def _research(self, tech):
        if self.game_state.money >= tech['cost']:
            if self.game_state.start_research(tech, "technology"):
                self.audio.play_sound("confirm")
                return "game_menu"
            else:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('research_already_active'))
                return None
        return None

class EngineCreateNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('create_engine_title'), 'engine_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "research_menu")

    def _on_confirm(self, name):
        self.game_state.current_engine_draft = {"name": name, "features": []}
        return "engine_feature_select"

class EngineFeatureSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('engine_feature_select'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        draft = self.game_state.current_engine_draft
        for f in self.game_state.unlocked_features:
            status = "[x] " if f in draft["features"] else "[ ] "
            self.options.append({'text': f"{status}{f.name}", 'action': lambda feat=f: self._toggle(feat)})
        self.options.append({'text': self.game_state.get_text('confirm'), 'action': self._confirm})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})

    def _toggle(self, feat):
        draft = self.game_state.current_engine_draft
        if feat in draft["features"]:
             draft["features"].remove(feat)
        else:
             draft["features"].append(feat)
        self._update_options()
        return None

    def _confirm(self):
        draft = self.game_state.current_engine_draft
        if not draft["features"]:
            self.audio.speak(self.game_state.get_text('engine_no_features'))
            return None
        from models import Engine
        new_engine = Engine(draft["name"], draft["features"])
        self.game_state.engines.append(new_engine)
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('engine_success', name=new_engine.name))
        return "research_menu"

class HardwareDevMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hardware_dev')
        options = [
            {'text': self.game_state.get_text('create_console'), 'action': lambda: "console_name_input"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"}
        ]
        super().__init__(title, options, audio, game_state)

class ConsoleNameInput(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('create_console_title'), 'console_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "hardware_dev_menu")

    def _on_confirm(self, name):
        self.game_state.current_console_draft = {"name": name, "tech_level": 1, "cost": 500000}
        return "console_specs_menu"

class ConsoleSpecsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('console_specs'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        draft = getattr(self.game_state, 'current_console_draft', None)
        if not draft:
            self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "hardware_dev_menu"}]
            return
        self.options = [
            {'text': f"{self.game_state.get_text('tech_level_label')}: {draft['tech_level']} (+100.000 EUR)", 'action': self._inc_tech},
            {'text': self.game_state.get_text('start_development_cost', cost=f"{draft['cost']:,}"), 'action': self._start},
            {'text': self.game_state.get_text('back'), 'action': lambda: "hardware_dev_menu"}
        ]

    def _inc_tech(self):
        draft = self.game_state.current_console_draft
        draft['tech_level'] += 1
        draft['cost'] += 100000
        self.audio.play_sound("click")
        self._update_options()
        return None

    def _start(self):
        draft = self.game_state.current_console_draft
        if self.game_state.money >= draft['cost']:
             self.game_state.money -= draft['cost']
             self.game_state.is_developing_console = True
             self.game_state.console_progress = 0
             self.audio.play_sound("confirm")
             return "game_menu"
        return None
