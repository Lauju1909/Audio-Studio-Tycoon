from .base import Menu, TextInputMenu
import pygame
import random
from game_data import HARDWARE_TECH_LIST

class HardwareLabMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hardware_menu_title')
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        gs = self.game_state
        
        # Jahr prüfen
        if gs.get_calendar_year() < 2001:
            self.title = gs.get_text('hardware_menu_title') + " (Gesperrt)"
            self.options.append({'text': gs.get_text('back'), 'action': lambda: "game_menu"})
            return
            
        self.title = gs.get_text('hardware_menu_title')
        
        # 1. Option: Neue Soundkarte entwickeln
        active_proj = next((p for p in getattr(gs, 'sound_card_projects', []) if not p.is_released), None)
        if active_proj:
            txt = gs.get_text('hardware_active_project', name=active_proj.name, progress=active_proj.progress)
            # Wenn fertig (progress >= 100%), füge Option zum Veröffentlichen hinzu
            if active_proj.progress >= 100.0:
                self.options.append({
                    'text': gs.get_text('hardware_opt_release', name=active_proj.name),
                    'action': lambda name=active_proj.name: self._release_card(name)
                })
            else:
                self.options.append({'text': txt, 'action': self._active_proj_action})
        else:
            self.options.append({'text': gs.get_text('hardware_opt_develop'), 'action': lambda: "hardware_create_name"})
            
        # 2. Option: Sound-Technologie lizenzieren
        self.options.append({'text': gs.get_text('hardware_opt_license'), 'action': lambda: "hardware_licensing"})
        
        # 3. Option: Veröffentlichte Soundkarten & Tantiemen
        self.options.append({'text': gs.get_text('hardware_opt_overview'), 'action': lambda: "hardware_overview"})
        
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "game_menu"})

    def announce_entry(self):
        gs = self.game_state
        if gs.get_calendar_year() < 1980:
            self.audio.speak(gs.get_text('hardware_year_error'))
            super().announce_entry()
            return
            
        # Infos vorlesen
        unlocked_count = len(getattr(gs, 'unlocked_hardware_tech', []))
        welcome_info = gs.get_text('hardware_menu_intro') + " " + gs.get_text('hardware_unlocked_techs', count=unlocked_count)
        
        self.audio.speak(self.title)
        self.audio.speak(welcome_info, interrupt=False)
        
        active_proj = next((p for p in getattr(gs, 'sound_card_projects', []) if not p.is_released), None)
        if active_proj:
            txt = gs.get_text('hardware_active_project', name=active_proj.name, progress=active_proj.progress)
            self.audio.speak(txt, interrupt=False)
            
        if self.options:
            self.speak_current(interrupt=False)

    def _active_proj_action(self):
        self.audio.play_sound("error")
        active_proj = next((p for p in getattr(self.game_state, 'sound_card_projects', []) if not p.is_released), None)
        if active_proj:
            txt = self.game_state.get_text('hardware_active_project', name=active_proj.name, progress=active_proj.progress)
            self.audio.speak(txt)
        return None

    def _release_card(self, name):
        success = self.game_state.release_sound_card(name)
        if success:
            card = next((p for p in getattr(self.game_state, 'sound_card_projects', []) if p.name == name), None)
            share = card.market_share if card else 0.0
            self.audio.play_sound("confirm")
            self.audio.speak(self.game_state.get_text('hardware_release_success', name=name, share=share))
            self._update_options()
            return "hardware_menu"
        else:
            self.audio.play_sound("error")
            return None


class HardwareLicensingMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hardware_licensing_title')
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        gs = self.game_state
        
        for tech in HARDWARE_TECH_LIST:
            tech_id = tech["id"]
            name = gs.get_text(tech["name_key"]) if gs.get_text(tech["name_key"]) else tech["id"]
            
            # Status ermitteln
            if tech_id in getattr(gs, 'unlocked_hardware_tech', []):
                status_str = gs.get_text('hardware_license_owned')
                action_fn = None
            elif gs.get_calendar_year() < tech["year"]:
                status_str = gs.get_text('hardware_license_locked_year', year=tech["year"])
                action_fn = lambda t=tech: self._locked_tech_action(t)
            else:
                status_str = ""
                action_fn = lambda t_id=tech_id: self._buy_license(t_id)
                
            opt_text = gs.get_text('hardware_license_option', name=name, year=tech["year"], cost=tech["cost"], status=status_str)
            self.options.append({
                'text': opt_text,
                'action': action_fn
            })
            
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "hardware_menu"})

    def announce_entry(self):
        self.audio.speak(self.title)
        self.audio.speak(self.game_state.get_text('hardware_licensing_intro'), interrupt=False)
        if self.options:
            self.speak_current(interrupt=False)

    def _locked_tech_action(self, tech):
        self.audio.play_sound("error")
        name = self.game_state.get_text(tech["name_key"])
        msg = f"{name} {self.game_state.get_text('hardware_license_locked_year', year=tech['year'])}"
        self.audio.speak(msg)
        return None

    def _buy_license(self, tech_id):
        success = self.game_state.unlock_hardware_technology(tech_id)
        if success:
            tech = next((t for t in HARDWARE_TECH_LIST if t["id"] == tech_id), None)
            name = self.game_state.get_text(tech["name_key"]) if tech else tech_id
            self.audio.play_sound("buy")
            self.audio.speak(self.game_state.get_text('hardware_license_success', name=name))
            self._update_options()
        else:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
        return None


class SoundCardCreateMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        
        # Initialisieren mit on_confirm und on_cancel Callbacks
        super().__init__(
            title="hardware_name",
            prompt="hardware_project_name_prompt",
            audio=audio,
            game_state=game_state,
            on_confirm=self._on_confirm,
            on_cancel=self._on_cancel
        )

    def generate_random_name(self):
        # Generiert echte Retro-Soundkarten-Namen
        prefixes = ["Sound Blaster", "Gravis UltraSound", "AdLib", "Sound Canvas", "AWE", "Covox Speech", "WaveBlaster"]
        suffixes = ["1.0", "2.0", "Pro", "16", "32", "64", "Gold", "Classic", "Max", "Ultra"]
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"

    def _on_confirm(self, name):
        self.game_state.temp_sound_card_name = name
        return "hardware_project_features"

    def _on_cancel(self):
        return "hardware_menu"


class SoundCardFeaturesMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.selected_techs = []
        
        name = getattr(self.game_state, 'temp_sound_card_name', "Soundkarte")
        title = self.game_state.get_text('hardware_project_features_title') + f" ({name})"
        
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        gs = self.game_state
        name = getattr(gs, 'temp_sound_card_name', "Soundkarte")
        
        # Nur freigeschaltete Lizenzen auflisten
        unlocked = getattr(gs, 'unlocked_hardware_tech', [])
        
        # Berechnung der vorläufigen Entwicklungskosten
        dev_cost = 20000 # Grundkosten
        for t_id in self.selected_techs:
            tech = next((t for t in HARDWARE_TECH_LIST if t["id"] == t_id), None)
            if tech:
                dev_cost += tech["cost"]
                
        for tech in HARDWARE_TECH_LIST:
            tech_id = tech["id"]
            if tech_id not in unlocked:
                continue # Nicht besessen -> kann nicht eingebaut werden
                
            tech_name = gs.get_text(tech["name_key"]) if gs.get_text(tech["name_key"]) else tech["id"]
            status = "[X] " if tech_id in self.selected_techs else "[ ] "
            
            txt = f"{status}{tech_name} (+{int(tech['sound_bonus']*100)}% Sound, Kosten: {tech['cost']:,} €)"
            self.options.append({
                'text': txt,
                'action': lambda t_id=tech_id: self._toggle_feature(t_id)
            })
            
        # Option zum Starten der Entwicklung
        start_txt = gs.get_text('hardware_dev_start', cost=dev_cost, tech=len(self.selected_techs))
        self.options.append({
            'text': start_txt,
            'action': lambda cost=dev_cost: self._start_development(cost)
        })
        
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "hardware_menu"})

    def announce_entry(self):
        self.selected_techs = []
        name = getattr(self.game_state, 'temp_sound_card_name', "Soundkarte")
        
        self.audio.speak(self.title)
        self.audio.speak(self.game_state.get_text('hardware_project_features_intro', name=name), interrupt=False)
        
        # Kassenstand & Info ansagen
        gs = self.game_state
        cost_txt = gs.get_text('hardware_dev_cost_info', cost=20000, money=gs.money)
        self.audio.speak(cost_txt, interrupt=False)
        
        self._update_options()
        if self.options:
            self.speak_current(interrupt=False)

    def _toggle_feature(self, tech_id):
        if tech_id in self.selected_techs:
            self.selected_techs.remove(tech_id)
            self.audio.play_sound("click")
        else:
            self.selected_techs.append(tech_id)
            self.audio.play_sound("click")
            
        self._update_options()
        self.speak_current()
        return None

    def _start_development(self, total_cost):
        name = getattr(self.game_state, 'temp_sound_card_name', "Soundkarte")
        
        if self.game_state.money < total_cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None
            
        success = self.game_state.start_sound_card_project(name, list(self.selected_techs))
        if success:
            self.audio.play_sound("confirm")
            # Ungefähre Dauer: 20 Wochen Grundzeit + 6 Wochen pro Feature
            duration = 20 + len(self.selected_techs) * 6
            self.audio.speak(self.game_state.get_text('hardware_project_started', name=name, weeks=duration))
            return "hardware_menu"
        else:
            self.audio.play_sound("error")
            return None


class SoundCardOverviewMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('hardware_overview_title')
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        gs = self.game_state
        
        released = [p for p in getattr(gs, 'sound_card_projects', []) if p.is_released]
        if not released:
            self.options.append({'text': gs.get_text('hardware_no_released'), 'action': lambda: None})
        else:
            for card in released:
                txt = gs.get_text('hardware_overview_entry',
                                  name=card.name,
                                  share=card.market_share,
                                  weekly=int(card.royalties_gained),
                                  total=int(card.lifetime_royalties))
                self.options.append({'text': txt, 'action': lambda: None})
                
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "hardware_menu"})

from menus.base import TextInputMenu

class ConsoleCreateMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        super().__init__('hardware_menu_title', 'console_name_prompt', audio, game_state,
                         on_confirm=self._confirm, on_cancel=lambda: "hardware_menu")

    def _confirm(self, name):
        if not name:
            self.audio.speak(self.game_state.get_text('invalid_name'))
            return "console_create"
            
        self.game_state._pending_console_name = name
        return "console_components"

class ConsoleComponentsMenu(Menu):
    def __init__(self, audio, game_state):
        super().__init__(game_state.get_text('console_comp_title'), [], audio, game_state)
        
    def announce_entry(self):
        self.options = []
        gs = self.game_state
        
        tiers = [
            ("Budget", 20000000, 199, 10),
            ("Standard", 50000000, 299, 20),
            ("High-End", 100000000, 499, 40)
        ]
        
        for t, cost, price, tech in tiers:
            self.options.append({
                'text': gs.get_text('console_tier_opt', tier=t, cost=cost, price=price, tech=tech),
                'action': lambda t=t, c=cost, p=price, tc=tech: self._start_console(t, c, p, tc)
            })
            
        self.options.append({'text': gs.get_text('cancel'), 'action': lambda: "hardware_menu"})
        super().announce_entry()

    def _start_console(self, tier, cost, price, tech):
        gs = self.game_state
        if gs.money < cost:
            self.audio.speak(gs.get_text('not_enough_money_hardware'))
            return None
            
        gs.track_expense("other", cost)
        name = getattr(gs, '_pending_console_name', "MyConsole")
        
        from models import CustomConsoleProject
        cc = CustomConsoleProject(name=name, tech_level=tech, dev_cost=cost, price=price)
        cc.total_weeks = 50 if tier == "Budget" else 100 if tier == "Standard" else 150
        gs.active_custom_console = cc
        
        self.audio.play_sound("confirm")
        self.audio.speak(gs.get_text('console_started', name=name))
        return "hardware_menu"
