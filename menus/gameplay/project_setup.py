from ..base import Menu, TextInputMenu, SliderMenu
from game_data import (
    SLIDER_NAMES, GAME_SIZES,
)
import random


class CoDevPartnerMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('menu_co_dev_partner_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for rival in self.game_state.rivals:
            self.options.append({'text': self.game_state.get_text('co_dev_partner_option', name=rival.name), 'action': lambda r=rival.name: self._select(r)})
        
        # Falls es keine Konkurrenten gibt:
        if not self.options:
            self.options.append({'text': self.game_state.get_text('co_dev_no_partners'), 'action': lambda: "game_menu"})
        else:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})

    def _select(self, partner_name):
        self.game_state.co_dev_partner = partner_name
        self.audio.play_sound("confirm")
        self.audio.speak(self.game_state.get_text('co_dev_started', name=partner_name))
        return "project_type_menu"


class ProjectTypeMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('project_type_title', default='Projektart wÃ¤hlen'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('project_type_new', default='Neues Spiel entwickeln'), 'action': lambda: self._select('new')},
            {'text': self.game_state.get_text('project_type_sequel', default='Fortsetzung (Sequel)'), 'action': lambda: "sequel_menu"},
            {'text': self.game_state.get_text('project_type_f2p', default='Free-to-Play Spiel entwickeln'), 'action': lambda: self._select('f2p')},
            {'text': self.game_state.get_text('project_type_remake', default='Remake (Klassiker neu auflegen)'), 'action': lambda: "remake_select_menu"},
            {'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"}
        ]

    def _select(self, p_type):
        if p_type == 'f2p':
            self.game_state.current_draft['is_f2p'] = True
            self.game_state.current_draft['is_remake'] = False
        else:
            self.game_state.current_draft['is_f2p'] = False
            self.game_state.current_draft['is_remake'] = False
        return "topic_menu"


class TopicMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('topic_menu'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        for topic in self.game_state.unlocked_topics:
            self.options.append({'text': self.game_state.get_text(topic), 'action': lambda t=topic: self._select(t)})
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
            self.options.append({'text': self.game_state.get_text(genre), 'action': lambda g=genre: self._select(g)})
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
            self.options.append({'text': self.game_state.get_text(aud), 'action': lambda a=aud: self._select(a)})
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
            self.options.append({'text': self.game_state.get_text(name), 'action': lambda s=name: self._select(s)})
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
        return "team_select_menu"


class ProjectTeamSelectMenu(Menu):
    """MenÃ¼ zur Auswahl der Mitarbeiter fÃ¼r ein Projekt."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        # Standard: Alle verfÃ¼gbaren Mitarbeiter sind ausgewÃ¤hlt
        if "assigned_employee_ids" not in self.game_state.current_draft:
             self.game_state.current_draft["assigned_employee_ids"] = [i for i, e in enumerate(self.game_state.employees) if not getattr(e, 'is_sick', False) and not getattr(e, 'is_training', False) and getattr(e, 'vacation_weeks_left', 0) <= 0]
        
        super().__init__(self.game_state.get_text('menu_team_select'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        assigned_ids = self.game_state.current_draft.get("assigned_employee_ids", [])
        
        # IDs der Mitarbeiter, die bereits in anderen Projekten arbeiten
        busy_ids = []
        for ap in self.game_state.active_projects:
            busy_ids.extend(getattr(ap["project"], 'assigned_employee_ids', []))

        for i, emp in enumerate(self.game_state.employees):
            # Kranke, trainierende oder beurlaubte MA können nicht gewählt werden
            if getattr(emp, 'is_sick', False) or getattr(emp, 'is_training', False) or getattr(emp, 'vacation_weeks_left', 0) > 0:
                continue
            
            # Bereits beschÃ¤ftigte MA (auÃŸer sie sind bereits diesem Projekt zugewiesen)
            if i in busy_ids and i not in assigned_ids:
                continue
                
            is_assigned = i in assigned_ids
            status_text = self.game_state.get_text('team_status_assigned' if is_assigned else 'team_status_not_assigned')
            text = self.game_state.get_text('team_member_status', name=emp.name, role=self.game_state.get_text(emp.role), status=status_text)
            
            # Spezialisierungs-Indikator
            if emp.specialization:
                spec = emp.specialization
                # BUG-FIX v3.3.9: Sicherer .get()-Zugriff statt [] um KeyError/TypeError bei None-Werten nach reset_draft zu vermeiden
                draft_genre = self.game_state.current_draft.get('genre')
                draft_topic = self.game_state.current_draft.get('topic')
                draft_sub_genre = self.game_state.current_draft.get('sub_genre')
                if spec.get("bonus_type") == "Genre" and (draft_genre == spec.get("target") or draft_sub_genre == spec.get("target")):
                    text += " [BONUS!]"
                elif spec.get("bonus_type") == "Topic" and draft_topic == spec.get("target"):
                    text += " [BONUS!]"
            
            # WICHTIG: idx=i fixiert den aktuellen Wert von i fÃ¼r die Lambda-Funktion
            self.options.append({'text': text, 'action': lambda idx=i: self._toggle(idx)})

        # BestÃ¤tigen Option
        count = len(assigned_ids)
        self.options.append({'text': self.game_state.get_text('team_confirm', count=count), 'action': self._confirm})
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "marketing_menu"})

    def _toggle(self, real_idx):
        assigned_ids = self.game_state.current_draft.get("assigned_employee_ids", [])
        
        if real_idx in assigned_ids:
            assigned_ids.remove(real_idx)
        else:
            assigned_ids.append(real_idx)
            
        self.game_state.current_draft["assigned_employee_ids"] = assigned_ids
        self._update_options()
        return None

    def _confirm(self):
        if not self.game_state.current_draft.get("assigned_employee_ids"):
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('team_none_selected_error'))
            return None
        
        # ZeitschÃ¤tzung ansagen
        weeks = self.game_state.estimate_dev_time()
        self.audio.speak(self.game_state.get_text('dev_time_estimate', weeks=weeks))
        
        return "game_name_input"


class GameNameMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('game_name_title', 'game_name_prompt', audio, game_state,
                         on_confirm=self._on_confirm, on_cancel=lambda: "marketing_menu")

    def _on_confirm(self, name):
        self.game_state.current_draft['name'] = name
        return "slider_menu"

    def generate_random_name(self):
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
        
        # DRM Menu first (ab 1995 verfgbar)
        current_year = 1980 + (self.game_state.week // 52)
        if current_year >= 1995:
            return "drm_choice"
        else:
            if current_year >= 2009:
                return "crowdfunding_choice"
            else:
                est = self.game_state.estimate_dev_time()
                self.game_state.start_development()
                self.audio.speak(
                    self.game_state.get_text('dev_started', duration=est),
                    interrupt=False
                )
                return "dev_progress_menu"


class DRMChoiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('drm_choice_title', default="Kopierschutz (DRM) whlen"), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('drm_none', default="Kein DRM (Massive Piraterie, +Review Bonus)"), 'action': lambda: self._select_drm(0)},
            {'text': self.game_state.get_text('drm_standard', default="Standard DRM (50.000 EUR, 15% Piraterie)"), 'action': lambda: self._select_drm(1)},
            {'text': self.game_state.get_text('drm_aggressive', default="Aggressives DRM (200.000 EUR, 2% Piraterie, -Review Strafe)"), 'action': lambda: self._select_drm(2)}
        ]

    def _select_drm(self, level):
        self.game_state.current_draft['drm_level'] = level
        
        # Pay for DRM
        if level == 1:
            if self.game_state.money < 50000:
                self.audio.speak(self.game_state.get_text('not_enough_money'), interrupt=True)
                return self
            self.game_state.money -= 50000
            self.game_state.track_expense("production", 50000)
        elif level == 2:
            if self.game_state.money < 200000:
                self.audio.speak(self.game_state.get_text('not_enough_money'), interrupt=True)
                return self
            self.game_state.money -= 200000
            self.game_state.track_expense("production", 200000)
            
        current_year = 1980 + (self.game_state.week // 52)
        if current_year >= 2009:
            return "crowdfunding_choice"
        else:
            est = self.game_state.estimate_dev_time()
            self.game_state.start_development()
            self.audio.speak(
                self.game_state.get_text('dev_time_estimate', weeks=est),
                interrupt=False
            )
            return "dev_progress_menu"


class CrowdfundingChoiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('cf_choice_title', default="Entwicklung starten"), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('cf_normal_dev', default="Normale Entwicklung starten"), 'action': self._start_normal}
        ]
        
        # Crowdfunding-Optionen
        targets = [100000, 500000, 1000000, 5000000]
        for t in targets:
            self.options.append({
                'text': self.game_state.get_text('cf_start_campaign', target=t, default=f"SoundStarter Kampagne ({t} EUR)"), 
                'action': lambda amt=t: self._start_cf(amt)
            })
            
        self.options.append({'text': self.game_state.get_text('cancel'), 'action': self._cancel})

    def _start_normal(self):
        est = self.game_state.estimate_dev_time()
        self.game_state.start_development()
        self.audio.speak(
            self.game_state.get_text('dev_time_estimate', weeks=est),
            interrupt=False
        )
        return "dev_progress_menu"
        
    def _start_cf(self, target):
        success, reason = self.game_state.start_crowdfunding_campaign(target)
        if success:
            self.audio.speak(self.game_state.get_text('cf_success', amount=target, default=f"Kampagne erfolgreich! {target} EUR gesammelt!"), interrupt=True)
            return "dev_progress_menu"
        else:
            self.audio.speak(self.game_state.get_text('cf_failed', default="Kampagne gescheitert! Zu wenig Hype/Fans."), interrupt=True)
            return "main_menu" # Bricht den Draft ab
            
    def _cancel(self):
        return "slider_menu"


class RemasterSelectMenu(Menu):
    def __init__(self, audio, game_state):
         super().__init__(game_state.get_text('remaster_title'), [], audio, game_state)


class PublisherMenu(Menu):
    def __init__(self, audio, game_state):
         super().__init__(game_state.get_text('publisher_title'), [], audio, game_state)


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


class RemakeSelectMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('remake_title', default='Remake wÃ¤hlen'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        from game_data import WEEKS_PER_YEAR
        for game in self.game_state.game_history:
            weeks_since_release = self.game_state.week - getattr(game, 'release_week', 0)
            if weeks_since_release >= WEEKS_PER_YEAR * 10:
                self.options.append({
                    'text': f"{game.name} (10+ Jahre alt)", 
                    'action': lambda g=game: self._select(g)
                })
        
        if not self.options:
            self.options.append({'text': self.game_state.get_text('no_remakes', default='Keine Spiele Ã¤lter als 10 Jahre'), 'action': lambda: "project_type_menu"})
            
        self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "project_type_menu"})

    def _select(self, game):
        self.game_state.current_draft['topic'] = game.topic
        self.game_state.current_draft['genre'] = game.genre
        self.game_state.current_draft['is_remake'] = True
        self.game_state.current_draft['is_f2p'] = False
        self.game_state.current_draft['sequel_to'] = game.name
        self.game_state.current_draft['sequel_number'] = game.sequel_number + 1
        return "sub_genre_menu"
