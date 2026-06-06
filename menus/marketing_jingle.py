from .base import Menu, TextInputMenu
import random

class JingleNameInputMenu(TextInputMenu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        
        # Falls in translations.py jingle_name_prompt fehlt, nutzen wir einen Fallback
        prompt_key = 'jingle_name_prompt' if game_state.get_text('jingle_name_prompt') != 'jingle_name_prompt' else 'hardware_project_name_prompt'
        
        super().__init__(
            title="jingle_menu_title",
            prompt=prompt_key,
            audio=audio,
            game_state=game_state,
            on_confirm=self._on_confirm,
            on_cancel=self._on_cancel
        )

    def generate_random_name(self):
        prefixes = ["Mega Radio", "Hype FM", "Chart Breaker", "Studio Promo", "Sound Blast", "Audiomax", "Future Sound"]
        suffixes = ["Ad", "Jingle", "Spot", "Promo", "Commercial", "Teaser", "Intro"]
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"

    def _on_confirm(self, name):
        self.game_state.temp_jingle_name = name
        self.game_state.temp_jingle_music = "none"
        self.game_state.temp_jingle_voice = "none"
        self.game_state.temp_jingle_sfx = "none"
        return "jingle_generator"

    def _on_cancel(self):
        return "marketing_menu"


class JingleGeneratorMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('jingle_menu_title')
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        gs = self.game_state
        
        name = getattr(gs, 'temp_jingle_name', "Jingle")
        music = getattr(gs, 'temp_jingle_music', "none")
        voice = getattr(gs, 'temp_jingle_voice', "none")
        sfx = getattr(gs, 'temp_jingle_sfx', "none")
        
        # Basiskosten berechnen
        cost = 5000
        if music != "none": cost += 2000
        if voice != "none": cost += 1500
        if sfx != "none": cost += 1000
        
        # Hype Bonus berechnen
        hype = 5.0
        if music != "none": hype += 3.0
        if voice != "none": hype += 2.0
        if sfx != "none": hype += 2.0
        
        # 1. Option: Jingle-Name ändern
        self.options.append({
            'text': f"Name: {name}",
            'action': lambda: "jingle_name_input"
        })
        
        # 2. Option: Musikspur wählen
        music_display = gs.get_text(f"jingle_music_{music}", default=music)
        self.options.append({
            'text': f"{gs.get_text('jingle_comp_music')}: {music_display}",
            'action': lambda: "jingle_select_music"
        })
        
        # 3. Option: Sprecher-Stil wählen
        voice_display = gs.get_text(f"jingle_voice_{voice}", default=voice)
        self.options.append({
            'text': f"{gs.get_text('jingle_comp_voice')}: {voice_display}",
            'action': lambda: "jingle_select_voice"
        })
        
        # 4. Option: Soundeffekt wählen
        sfx_display = gs.get_text(f"jingle_sfx_{sfx}", default=sfx)
        self.options.append({
            'text': f"{gs.get_text('jingle_comp_sfx')}: {sfx_display}",
            'action': lambda: "jingle_select_sfx"
        })
        
        # 5. Option: Produzieren
        prod_txt = gs.get_text('jingle_opt_create', cost=cost) + f" (Hype: +{hype})"
        self.options.append({
            'text': prod_txt,
            'action': lambda cost=cost: self._produce_jingle(cost)
        })
        
        # Aktive Jingles Übersicht
        active_count = len(getattr(gs, 'active_jingles', []))
        if active_count > 0:
            self.options.append({
                'text': gs.get_text('jingle_active_list', count=active_count),
                'action': self._show_active_jingles
            })
            
        self.options.append({'text': gs.get_text('creator_menu_title'), 'action': lambda: "creator_menu"})
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "marketing_menu"})

    def announce_entry(self):
        gs = self.game_state
        self.title = gs.get_text('jingle_menu_title')
        active_count = len(getattr(gs, 'active_jingles', []))
        welcome_info = gs.get_text('jingle_menu_intro') + " " + gs.get_text('jingle_active_list', count=active_count)
        
        self.audio.speak(self.title)
        self.audio.speak(welcome_info, interrupt=False)
        self._update_options()
        
        if self.options:
            self.speak_current(interrupt=False)

    def _show_active_jingles(self):
        gs = self.game_state
        active = getattr(gs, 'active_jingles', [])
        if not active:
            self.audio.speak(gs.get_text('jingle_no_active'))
        else:
            self.audio.speak(gs.get_text('jingle_active_list', count=len(active)))
            for j in active:
                txt = gs.get_text('jingle_active_entry', name=j.name, hype=j.hype_bonus, weeks=j.weeks_left)
                self.audio.speak(txt, interrupt=False)
        return None

    def _produce_jingle(self, cost):
        gs = self.game_state
        if gs.money < cost:
            self.audio.play_sound("error")
            self.audio.speak(gs.get_text('not_enough_money'))
            return None
            
        name = getattr(gs, 'temp_jingle_name', "Jingle")
        music = getattr(gs, 'temp_jingle_music', "none")
        voice = getattr(gs, 'temp_jingle_voice', "none")
        sfx = getattr(gs, 'temp_jingle_sfx', "none")
        
        # Jingle über die Spiel-Logik erstellen
        success = gs.create_radio_jingle(name, music, voice, sfx)
        if success:
            # Hype-Bonus berechnen für Erfolgsansage
            hype = 5.0
            if music != "none": hype += 3.0
            if voice != "none": hype += 2.0
            if sfx != "none": hype += 2.0
            
            self.audio.play_sound("success")
            self.audio.speak(gs.get_text('jingle_created_success', name=name, cost=cost, hype=hype))
            
            # Zurück zum Marketing-Menü
            return "marketing_menu"
        else:
            self.audio.play_sound("error")
            self.audio.speak(gs.get_text('error'))
            return None


class JingleMusicMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = game_state.get_text('jingle_select_music')
        
        # Optionen aufbauen
        self.tracks = ["none", "pop", "synthwave", "rock", "chiptune"]
        options = []
        for t in self.tracks:
            display = game_state.get_text(f"jingle_music_{t}", default=t)
            cost_info = " (+2,000 €)" if t != "none" else ""
            options.append({
                'text': f"{display}{cost_info}",
                'action': lambda t_id=t: self._select_track(t_id)
            })
        options.append({'text': game_state.get_text('back'), 'action': lambda: "jingle_generator"})
        
        super().__init__(title, options, audio, game_state)

    def speak_current(self, interrupt=True):
        super().speak_current(interrupt)
        
        # Bumper-Sound-Vorschau abspielen basierend auf Fokuseintrag
        if self.current_index < len(self.tracks):
            track = self.tracks[self.current_index]
            if track == "chiptune":
                self.audio.play_sound("typing")
            elif track == "pop":
                self.audio.play_sound("select")
            elif track == "synthwave":
                self.audio.play_sound("blip")
            elif track == "rock":
                self.audio.play_sound("drumroll")

    def _select_track(self, track_id):
        self.game_state.temp_jingle_music = track_id
        self.audio.play_sound("confirm")
        return "jingle_generator"


class JingleVoiceMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = game_state.get_text('jingle_select_voice')
        
        self.styles = ["none", "hype", "soft", "serious"]
        options = []
        for s in self.styles:
            display = game_state.get_text(f"jingle_voice_{s}", default=s)
            cost_info = " (+1,500 €)" if s != "none" else ""
            options.append({
                'text': f"{display}{cost_info}",
                'action': lambda s_id=s: self._select_style(s_id)
            })
        options.append({'text': game_state.get_text('back'), 'action': lambda: "jingle_generator"})
        
        super().__init__(title, options, audio, game_state)

    def speak_current(self, interrupt=True):
        super().speak_current(interrupt)
        
        if self.current_index < len(self.styles):
            style = self.styles[self.current_index]
            if style == "hype":
                self.audio.play_sound("confirm")
            elif style == "soft":
                self.audio.play_sound("select")
            elif style == "serious":
                self.audio.play_sound("click")

    def _select_style(self, style_id):
        self.game_state.temp_jingle_voice = style_id
        self.audio.play_sound("confirm")
        return "jingle_generator"


class JingleSFXMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = game_state.get_text('jingle_select_sfx')
        
        self.effects = ["none", "laser", "explosion", "cash"]
        options = []
        for e in self.effects:
            display = game_state.get_text(f"jingle_sfx_{e}", default=e)
            cost_info = " (+1,000 €)" if e != "none" else ""
            options.append({
                'text': f"{display}{cost_info}",
                'action': lambda e_id=e: self._select_effect(e_id)
            })
        options.append({'text': game_state.get_text('back'), 'action': lambda: "jingle_generator"})
        
        super().__init__(title, options, audio, game_state)

    def speak_current(self, interrupt=True):
        super().speak_current(interrupt)
        
        if self.current_index < len(self.effects):
            effect = self.effects[self.current_index]
            if effect == "cash":
                self.audio.play_sound("cash")
            elif effect == "laser":
                self.audio.play_sound("blip")
            elif effect == "explosion":
                self.audio.play_sound("warn")

    def _select_effect(self, effect_id):
        self.game_state.temp_jingle_sfx = effect_id
        self.audio.play_sound("confirm")
        return "jingle_generator"
