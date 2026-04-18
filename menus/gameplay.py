from .base import Menu, TextInputMenu, SliderMenu
from game_data import (
    GENRES, SLIDER_NAMES, AUDIENCES,
    OFFICE_LEVELS, GAME_SIZES,
    get_compatibility, get_compatibility_text,
    get_available_platforms,
)
import random

class MainMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('main_title')
        options = [
            {'text': self.game_state.get_text('menu_new_game'), 'action': lambda: "company_name_input"},
            {'text': self.game_state.get_text('menu_load_game'), 'action': lambda: "load_menu"},
            {'text': self.game_state.get_text('menu_mod_portal'), 'action': lambda: "mod_portal"},
            {'text': self.game_state.get_text('menu_settings'), 'action': lambda: "settings_menu"},
            {'text': self.game_state.get_text('menu_help'), 'action': lambda: "help_menu"},
            {'text': self.game_state.get_text('menu_credits'), 'action': self.show_credits},
            {'text': self.game_state.get_text('menu_quit'), 'action': lambda: "quit"}
        ]
        super().__init__(title, options, audio, game_state)

    def show_credits(self):
        return "credits_menu"

class CompanyNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('company_name_title', 'company_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "main_menu")

    def _on_confirm(self, name):
        self.game_state.company_name = name
        return "difficulty_menu"

    def generate_random_name(self):
        import random
        names = [
            "Pixel Studios", "Audio Vision", "Red Barrels", "Lauju Games", 
            "Blind Box", "Sound Wave Games", "Next Gen Studios", "Echo Games", 
            "Visionary Devs", "Gamer Forge", "Creative Minds", "Virtual Dynamics"
        ]
        return random.choice(names)

class GameMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('game_menu')
        options = [
            {'text': self.game_state.get_text('menu_develop_game'), 'action': lambda: "topic_menu"},
            {'text': self.game_state.get_text('hr_menu'), 'action': lambda: "hr_menu"},
            {'text': self.game_state.get_text('research_menu'), 'action': lambda: "research_menu"},
            {'text': self.game_state.get_text('office_menu'), 'action': lambda: "office_menu"},
            {'text': self.game_state.get_text('email_inbox'), 'action': lambda: "email_inbox"},
            {'text': self.game_state.get_text('bank_menu'), 'action': lambda: "bank_menu"},
            {'text': self.game_state.get_text('service_menu'), 'action': lambda: "service_menu"},
            {'text': self.game_state.get_text('save_menu'), 'action': lambda: "save_menu"},
            {'text': self.game_state.get_text('menu_settings'), 'action': lambda: "settings_menu_ingame"},
            {'text': self.game_state.get_text('menu_quit'), 'action': lambda: "main_menu"}
        ]
        super().__init__(title, options, audio, game_state)

class TopicMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('topic_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for topic in self.game_state.unlocked_topics:
            self.options.append({'text': topic, 'action': lambda t=topic: self._select(t)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select(self, topic):
        self.game_state.current_draft['topic'] = topic
        return "genre_menu"

class GenreMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('genre_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for genre in self.game_state.unlocked_genres:
            self.options.append({'text': genre, 'action': lambda g=genre: self._select(g)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "topic_menu"})

    def _select(self, genre):
        self.game_state.current_draft['genre'] = genre
        return "platform_menu"

class PlatformMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('platform_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        platforms = self.game_state.get_market_platforms()
        for p in platforms:
            self.options.append({'text': f"{p['name']} ({p['license_fee']} EUR)", 'action': lambda plat=p: self._select(plat)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "genre_menu"})

    def _select(self, plat):
        self.game_state.current_draft['platform'] = plat
        return "audience_menu"

class AudienceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('audience_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for aud in self.game_state.unlocked_audiences:
            self.options.append({'text': aud, 'action': lambda a=aud: self._select(a)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "platform_menu"})

    def _select(self, aud):
        self.game_state.current_draft['audience'] = aud
        return "game_size_menu"

class GameSizeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('game_size_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for size in GAME_SIZES:
            name = size['name'] if isinstance(size, dict) else size
            self.options.append({'text': name, 'action': lambda s=name: self._select(s)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "audience_menu"})

    def _select(self, size):
        self.game_state.current_draft['size'] = size
        return "engine_select_menu"

class EngineSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('engine_select_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for engine in self.game_state.engines:
            self.options.append({'text': engine.name, 'action': lambda e=engine: self._select(e)})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_size_menu"})

    def _select(self, engine):
        self.game_state.current_draft['engine'] = engine
        return "marketing_menu"

class MarketingMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('marketing_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('marketing_none'), 'action': lambda: self._select('none')},
            {'text': self.game_state.get_text('marketing_small'), 'action': lambda: self._select('small')},
            {'text': self.game_state.get_text('marketing_medium'), 'action': lambda: self._select('medium')},
            {'text': self.game_state.get_text('marketing_large'), 'action': lambda: self._select('large')},
            {'text': self.game_state.get_text('back'), 'action': lambda: "engine_select_menu"}
        ]

    def _select(self, level):
        self.game_state.current_draft['marketing'] = level
        return "game_name_input"

class GameNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('game_name_title', 'game_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "marketing_menu")

    def _on_confirm(self, name):
        self.game_state.current_draft['name'] = name
        return "slider_menu"

    def generate_random_name(self):
        import random
        prefixes = ["Project", "The Last", "Super", "Mega", "Blind", "Dark", "Crazy", "Epic", "Legend of", "Call of", "Return to"]
        suffixes = ["Adventure", "Strike", "Hero", "Tycoon", "Quest", "Legends", "Warriors", "Audio", "World", "Chronicles"]
        
        draft = getattr(self.game_state, 'current_draft', {})
        topic = draft.get('topic', '')
        genre = draft.get('genre', '')
        
        choices = [
            f"{random.choice(prefixes)} {random.choice(suffixes)}",
            f"{random.choice(prefixes)} {topic}" if topic else f"{random.choice(prefixes)} Game"
        ]
        
        if topic:
            choices.append(f"{topic} {random.choice(suffixes)}")
        if genre and topic:
            choices.append(f"{topic} {genre}")
            
        return random.choice(choices)

class DevelopmentSliderMenu(SliderMenu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('dev_sliders_title'), audio, game_state,
                         SLIDER_NAMES, budget=15, 
                         on_confirm=self._on_confirm, on_cancel=lambda: "game_name_input")

    def _on_confirm(self, values):
        self.game_state.current_draft['sliders'] = values
        self.game_state.start_development()
        return "dev_progress_menu"

class DevProgressMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('dev_progress_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('finish_game'), 'action': self._finish},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]

    def _finish(self):
        if not self.game_state.active_project:
            return "game_menu"
            
        if self.game_state.dev_progress >= self.game_state.dev_total_weeks:
            self.game_state.finalize_game(self.game_state.active_project)
            self.game_state.dev_ready_to_finish = False
            return "review_result"
        else:
            self.audio.speak(self.game_state.get_text('dev_not_finished'))
            return None

    def update(self):
        """Wird in der Hauptschleife aufgerufen."""
        if self.game_state.dev_progress >= self.game_state.dev_total_weeks:
            # Automatisches Sprechen wenn fertig (optional, falls Menü offen)
            pass

    def speak_current(self, interrupt=True):
        progress = int((self.game_state.dev_progress / max(1, self.game_state.dev_total_weeks)) * 100)
        progress = min(100, progress)
        text = self.options[self.current_index]['text']
        status = f"{progress}% {self.game_state.get_text('completed_label')}"
        self.audio.speak(f"{status}. {text}", interrupt=interrupt)

class ReviewResultMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('review_result'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        if not self.game_state.game_history:
            self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "main_menu"}]
            return
        game = self.game_state.game_history[-1]
        score = game.review.average if game.review else 0
        self.options = [
            {'text': self.game_state.get_text('score_label', score=score), 'action': lambda: "game_menu"}
        ]

    def announce_entry(self):
        super().announce_entry()
        game = self.game_state.game_history[-1]
        score = game.review.average if game.review else 0
        self.audio.speak(self.game_state.get_text('reviews_for', name=game.name, score=score), interrupt=False)

class RemasterSelectMenu(Menu):
    def __init__(self, audio, game_state):
         super().__init__(game_state.get_text('remaster_title'), [], audio, game_state)

class PublisherMenu(Menu):
    def __init__(self, audio, game_state):
         super().__init__(game_state.get_text('publisher_title'), [], audio, game_state)

class GOTYMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('goty_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        # Zeige GOTY Historie
        for year, winner in self.game_state.goty_history.items():
             self.options.append({'text': f"Jahr {year}: {winner}", 'action': lambda: None})
        
        if not self.options:
             self.options.append({'text': self.game_state.get_text('goty_no_awards'), 'action': lambda: "game_menu"})
             
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

class DifficultyMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('difficulty_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        from game_data import DIFFICULTY_LEVELS
        self.options = []
        for idx, diff in enumerate(DIFFICULTY_LEVELS):
             self.options.append({
                 'text': f"{diff['name']}: {diff['description']}", 
                 'action': lambda i=idx: self._select(i)
             })
             
    def _select(self, idx):
        self.game_state.difficulty = idx
        # Startgeld etc. setzen
        from game_data import DIFFICULTY_LEVELS
        self.game_state.money = DIFFICULTY_LEVELS[idx]['start_money']
        return "game_menu"

class SubGenreMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('subgenre_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [{'text': self.game_state.get_text('no_subgenre'), 'action': lambda: "platform_menu"}]
        
        genre = self.game_state.current_draft.get('genre')
        from game_data import SUB_GENRES
        if genre in SUB_GENRES:
             for sub in SUB_GENRES[genre]:
                  self.options.append({
                      'text': sub['name'], 
                      'action': lambda s=sub['name']: self._select(s)
                  })
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "genre_menu"})

    def _select(self, name):
        self.game_state.current_draft['sub_genre'] = name
        return "platform_menu"

class SequelMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('sequel_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [{'text': self.game_state.get_text('new_ip'), 'action': lambda: "topic_menu"}]
        
        # Nur Spiele mit IP-Rating > 20
        for game in self.game_state.game_history:
             if game.ip_rating > 20:
                  self.options.append({
                      'text': f"{game.name} (IP: {game.ip_rating})", 
                      'action': lambda g=game: self._select(g)
                  })
                  
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select(self, game):
        self.game_state.current_draft['topic'] = game.topic
        self.game_state.current_draft['genre'] = game.genre
        self.game_state.current_draft['sequel_to'] = game.name
        self.game_state.current_draft['sequel_number'] = game.sequel_number + 1
        return "sub_genre_menu"

class ChartMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('charts_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        # Charts berechnen
        charts = self.game_state.get_current_charts()
        for idx, entry in enumerate(charts):
             text = f"{idx+1}. {entry['name']} ({entry['studio']}) - {entry['sales']:,} Sales"
             self.options.append({'text': text, 'action': lambda: None})
             
        if not self.options:
             self.options.append({'text': self.game_state.get_text('charts_empty'), 'action': lambda: "game_menu"})
             
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

class AAADevEventMenu(Menu):
    def __init__(self, audio, game_state):
         super().__init__(game_state.get_text('aaa_event_title'), [], audio, game_state)

class ExpoMenu(Menu):
    def __init__(self, audio, game_state):
         super().__init__(game_state.get_text('expo_menu_title'), [], audio, game_state)

class CreditsMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_credits'), [], audio, game_state)

    def announce_entry(self):
        self.current_index = 0
        self.audio.speak(self.title)
        self.audio.speak(self.game_state.get_text('credits_text'), interrupt=False)
        self.options = [{'text': self.game_state.get_text('back'), 'action': lambda: "main_menu"}]
        self.speak_current(interrupt=False)
