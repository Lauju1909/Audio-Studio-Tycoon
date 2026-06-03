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
            {'text': self.game_state.get_text('research_technology'), 'action': lambda: "technology_research_menu"}
        ]
        
        if self.game_state.get_calendar_year() >= 1998:
            options.append({'text': self.game_state.get_text('create_engine'), 'action': lambda: "engine_create_name"})
            options.append({'text': self.game_state.get_text('engine_licensing_title', default='Engine-Lizenzierung'), 'action': lambda: "engine_licensing_menu"})
            
        options.append({'text': self.game_state.get_text('hardware_dev'), 'action': lambda: "hardware_dev_menu"})
        options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
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
                reason = self.game_state.get_research_block_reason() or self.game_state.get_text('research_already_active')
                self.audio.speak(reason)
                return None
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
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
                reason = self.game_state.get_research_block_reason() or self.game_state.get_text('research_already_active')
                self.audio.speak(reason)
                return None
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
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
                reason = self.game_state.get_research_block_reason() or self.game_state.get_text('research_already_active')
                self.audio.speak(reason)
                return None
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
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
                reason = self.game_state.get_research_block_reason() or self.game_state.get_text('research_already_active')
                self.audio.speak(reason)
                return None
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
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
        draft = getattr(self.game_state, 'current_engine_draft', None)
        if not draft:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})
            return
        for f in self.game_state.unlocked_features:
            status = "[x] " if f in draft["features"] else "[ ] "
            self.options.append({'text': f"{status}{f.name}", 'action': lambda feat=f: self._toggle(feat)})
        self.options.append({'text': self.game_state.get_text('confirm'), 'action': self._confirm})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})

    def _toggle(self, feat):
        draft = getattr(self.game_state, 'current_engine_draft', None)
        if not draft:
            return "research_menu"
        if feat in draft["features"]:
             draft["features"].remove(feat)
        else:
             draft["features"].append(feat)
        self._update_options()
        return None

    def _confirm(self):
        draft = getattr(self.game_state, 'current_engine_draft', None)
        if not draft:
            return "research_menu"
        if not draft["features"]:
            self.audio.speak(self.game_state.get_text('engine_no_features'))
            return None
        
        # NEU: Startet ein Projekt statt sofortiger Erstellung
        success = self.game_state.start_engine_project(draft["name"], draft["features"])
        if success:
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('engine_project_started', name=draft["name"]))
            return "research_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None

class HardwareDevMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hardware_dev')
        options = []
        if self.game_state.get_calendar_year() >= 2001 and self.game_state.money >= 100000000:
            options.append({'text': self.game_state.get_text('create_console'), 'action': lambda: "console_name_input"})
        else:
            options.append({'text': self.game_state.get_text('console_reqs_not_met', default="Konsole (Benoetigt Jahr 2001 & 100 Mio EUR)"), 'action': lambda: None})
            
        if getattr(self.game_state, 'custom_consoles', []):
            options.append({'text': self.game_state.get_text('my_consoles', default='Meine Konsolen'), 'action': lambda: "console_overview_menu"})
            
        options.append({'text': self.game_state.get_text('back'), 'action': lambda: "research_menu"})
        super().__init__(title, options, audio, game_state)

class ConsoleNameInput(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('create_console_title'), 'console_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "hardware_dev_menu")

    def _on_confirm(self, name):
        self.game_state.current_console_draft = {
            "name": name, 
            "performance": 1, 
            "architecture": "RISC", 
            "marketing_budget": 0, 
            "cost": 50000000 # 50 Mio Base Cost!
        }
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
            
        archs = ["RISC", "x86", "Cell", "ARM"]
        
        self.options = [
            {'text': f"{self.game_state.get_text('console_arch', default='Architektur')}: {draft['architecture']}", 'action': self._cycle_arch},
            {'text': f"{self.game_state.get_text('console_perf', default='Leistung (1-10)')}: {draft['performance']} (+10 Mio EUR)", 'action': self._inc_perf},
            {'text': f"{self.game_state.get_text('console_marketing', default='Marketing-Budget')}: {draft['marketing_budget'] // 1000000} Mio (+5 Mio EUR)", 'action': self._inc_marketing},
            {'text': self.game_state.get_text('start_development_cost', cost=draft['cost']), 'action': self._start},
            {'text': self.game_state.get_text('back'), 'action': lambda: "hardware_dev_menu"}
        ]

    def _cycle_arch(self):
        archs = ["RISC", "x86", "Cell", "ARM"]
        draft = self.game_state.current_console_draft
        idx = archs.index(draft['architecture'])
        draft['architecture'] = archs[(idx + 1) % len(archs)]
        self.audio.play_sound("click")
        self._update_options()
        return None

    def _inc_perf(self):
        draft = self.game_state.current_console_draft
        if draft['performance'] < 10:
            draft['performance'] += 1
            draft['cost'] += 10000000
            self.audio.play_sound("click")
        else:
            self.audio.play_sound("error")
        self._update_options()
        return None

    def _inc_marketing(self):
        draft = self.game_state.current_console_draft
        draft['marketing_budget'] += 5000000
        draft['cost'] += 5000000
        self.audio.play_sound("click")
        self._update_options()
        return None

    def _start(self):
        draft = self.game_state.current_console_draft
        if self.game_state.money >= draft['cost']:
            self.game_state.track_expense("research", draft['cost'])
            self.game_state.is_developing_console = True
            self.game_state.console_progress = 0
            self.game_state.console_total_weeks = 100 + (draft['performance'] * 10) # Takes years!
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('console_dev_started', default="Entwicklung gestartet! Dies wird Jahre dauern."), interrupt=True)
            return "game_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
        return None


class ConsoleOverviewMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(game_state.get_text('my_consoles', default='Meine Konsolen'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        consoles = getattr(self.game_state, 'custom_consoles', [])
        for i, c in enumerate(consoles):
            self.options.append({
                'text': c.name,
                'action': lambda idx=i: self._view_console(idx)
            })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "hardware_dev_menu"})

    def _view_console(self, idx):
        self.game_state.ui_context['selected_console_idx'] = idx
        return "console_detail_menu"

class ConsoleDetailMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        idx = self.game_state.ui_context.get('selected_console_idx', 0)
        c = self.game_state.custom_consoles[idx]
        
        info = f"{c.name} - Architektur: {getattr(c, 'architecture', 'RISC')}, Leistung: {getattr(c, 'performance', getattr(c, 'tech_level', 1))}. "
        info += f"Verkaufte Einheiten: {getattr(c, 'units_sold', 0):,}. Marktanteil: {getattr(c, 'market_share', 0)*100:.1f}%."
        
        super().__init__(info, [{'text': self.game_state.get_text('back'), 'action': lambda: "console_overview_menu"}], audio, game_state)
        self.audio.speak(info, interrupt=False)
