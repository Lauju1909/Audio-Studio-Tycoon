from ..base import Menu, TextInputMenu, SliderMenu
from game_data import (
    SLIDER_NAMES, GAME_SIZES,
)
import random


class DevProgressMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('dev_progress_menu'), [], audio, game_state)
        self.selected_project_idx = -1
        self._update_options()

    def _update_options(self):
        self.options = []
        if self.selected_project_idx == -1:
            for i, ap in enumerate(self.game_state.active_projects):
                prog = int((ap["progress"] / ap["total_weeks"]) * 100)
                name = ap["project"].name
                # Closure fÃ¼r idx
                def make_select(idx):
                    return lambda: self._select_project(idx)
                self.options.append({'text': f"{name} ({prog}%)", 'action': make_select(i)})
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
        else:
            ap = self.game_state.active_projects[self.selected_project_idx]
            prog = int((ap["progress"] / ap["total_weeks"]) * 100)
            self.options = [
                {'text': self.game_state.get_text('get_progress_label', default="Fortschritt abfragen"), 'action': self._speak_progress},
            ]
            is_engine = getattr(ap["project"], "is_engine_project", False) or ap["project"].__class__.__name__ == "EngineProject"
            
            if not getattr(ap["project"], "used_ai_assets", False) and not is_engine:
                if self.game_state.is_feature_unlocked("ai_tools"):
                    self.options.append({
                        'text': self.game_state.get_text('use_ai_assets', default="KI-Assets generieren (Risikoreich!)"),
                        'action': self._use_ai_assets
                    })
                else:
                    from game_data import FEATURE_UNLOCKS
                    if "ai_tools" in FEATURE_UNLOCKS:
                        self.options.append({
                            'text': f"{self.game_state.get_text('use_ai_assets', default='KI-Assets generieren (Risikoreich!)')} (Ab {FEATURE_UNLOCKS['ai_tools'].get('year', '???')})",
                            'action': lambda: None
                        })

            if "KI-Soundtrack Generation" in self.game_state.unlocked_technologies and not getattr(ap["project"], "used_ai_soundtrack", False) and not is_engine:
                self.options.append({
                    'text': self.game_state.get_text('use_ai_soundtrack', default="KI-Soundtrack integrieren (Riskant!)"),
                    'action': self._use_ai_soundtrack
                })
            
            # Early Access Option (30-50% progress minimum, we'll check >= 30%)
            if prog >= 30 and not getattr(ap["project"], "is_early_access", False) and not is_engine:
                self.options.append({
                    'text': self.game_state.get_text('release_early_access', default="Als Early Access verÃ¶ffentlichen"),
                    'action': self._release_early_access
                })
                
            self.options.extend([
                {'text': self.game_state.get_text('finish_game'), 'action': self._finish},
                {'text': self.game_state.get_text('back'), 'action': self._back_to_list}
            ])

    def _select_project(self, idx):
        self.selected_project_idx = idx
        self._update_options()
        self.current_index = 0
        return None

    def _back_to_list(self):
        self.selected_project_idx = -1
        self._update_options()
        self.current_index = 0
        return None

    def _speak_progress(self):
        if self.selected_project_idx < 0 or self.selected_project_idx >= len(self.game_state.active_projects):
            return self._back_to_list()
        ap = self.game_state.active_projects[self.selected_project_idx]
        progress = int((ap["progress"] / ap["total_weeks"]) * 100)
        progress = min(100, progress)
        status = f"{progress}% {self.game_state.get_text('completed_label')}. Bugs: {ap['bugs']}"
        self.audio.speak(status)
        return None

    def _finish(self):
        if self.selected_project_idx < 0 or self.selected_project_idx >= len(self.game_state.active_projects):
            return self._back_to_list()
        ap = self.game_state.active_projects[self.selected_project_idx]
        if ap["progress"] >= ap["total_weeks"]:
            is_engine = getattr(ap["project"], "is_engine_project", False) or ap["project"].__class__.__name__ == "EngineProject"
            if is_engine:
                self.game_state.finalize_engine(ap)
                self.audio.speak(self.game_state.get_text('engine_project_started', default="Engine-Entwicklung abgeschlossen!"))
                return "game_menu"
                
            # Check if it is a Contract Work
            if getattr(ap["project"], "target_points", None) is not None:
                # Beende Auftragsarbeit
                self.game_state.finish_contract_work(ap)
                self.audio.play_sound("cash")
                self.audio.speak(self.game_state.get_text('contract_finished', payout=ap["project"].payout))
                return "game_menu"
            else:
                self.game_state.finalize_game(ap)
                if getattr(ap["project"], "is_early_access", False):
                    # It was in early access, now it's fully released
                    ap["project"].is_early_access = False
                    self.audio.speak(self.game_state.get_text('early_access_full_release_msg', default="Das Spiel hat den Early Access verlassen!"))
                return "review_result"
        else:
            self.audio.speak(self.game_state.get_text('dev_not_finished'))
            return None

    def _release_early_access(self):
        if self.selected_project_idx < 0 or self.selected_project_idx >= len(self.game_state.active_projects):
            return self._back_to_list()
        ap = self.game_state.active_projects[self.selected_project_idx]
        
        # Set to Early Access
        ap["project"].is_early_access = True
        
        # We need to finalize it partially so it goes on sale, but keep it in active_projects
        # We call finalize_game with early_access=True to keep it in active_projects
        self.game_state.finalize_game(ap, early_access=True)
        
        self.audio.speak(self.game_state.get_text('early_access_released_msg', default="Das Spiel ist nun im Early Access verfÃ¼gbar."))
        return "review_result"

    def _use_ai_assets(self):
        if self.game_state.use_ai_assets(self.selected_project_idx):
            if hasattr(self.audio, 'play_sound'):
                self.audio.play_sound('cash')
            self.audio.speak(self.game_state.get_text('ai_assets_used_msg', default="KI-Assets generiert! Der Fortschritt ist massiv gestiegen."))
        self._update_options()
        return None

    def _use_ai_soundtrack(self):
        if self.game_state.use_ai_soundtrack(self.selected_project_idx):
            if hasattr(self.audio, 'play_sound'):
                self.audio.play_sound('cash')
            self.audio.speak(self.game_state.get_text('ai_soundtrack_used_msg', default="KI-Soundtrack eingebaut! Das könnte einen Shitstorm geben..."))
        self._update_options()
        return None

    def speak_current(self, interrupt=True):
        text = self.options[self.current_index]['text']
        self.audio.speak(text, interrupt=interrupt)


class AAADevEventMenu(Menu):
    """Zeigt Entwicklungs-Events (AAA und allgemein) mit Entscheidungsoptionen."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.event_ctx = getattr(game_state, 'pending_dev_event', None)
        
        if self.event_ctx:
            event = self.event_ctx["data"]
            proj_name = self.event_ctx["ap"]["project"].name
            title = f"{proj_name}: " + game_state.get_text('dev_event_' + event['id'] + '_title',
                                         default=game_state.get_text('aaa_event_title'))
        else:
            title = game_state.get_text('aaa_event_title')
            
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        if not self.event_ctx:
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "game_menu"})
            return
            
        event = self.event_ctx["data"]
        for opt in event.get('options', []):
            opt_text = self.game_state.get_text(
                'dev_event_opt_' + event['id'] + '_' + opt['id'],
                default=self.game_state.get_text('dev_event_opt_' + opt['id'], default=opt['id'])
            )
            # Konsequenz-Zusammenfassung
            effects = []
            if opt.get('cost', 0) > 0:
                effects.append(f"-{opt['cost']:,} EUR")
            if opt.get('delay', 0) > 0:
                effects.append(f"+{opt['delay']} {self.game_state.get_text('weeks')}")
            if opt.get('speed', 0) > 0:
                effects.append(f"-{opt['speed']} {self.game_state.get_text('weeks')}")
            if opt.get('hype', 0) != 0:
                sign = '+' if opt['hype'] > 0 else ''
                effects.append(f"{sign}{opt['hype']} Hype")
            if opt.get('bugs', 0) > 0:
                effects.append(f"+{opt['bugs']} Bugs")
            if opt.get('morale', 0) != 0:
                sign = '+' if opt['morale'] > 0 else ''
                effects.append(f"{sign}{opt['morale']} {self.game_state.get_text('morale')}")
            suffix = f" [{', '.join(effects)}]" if effects else ""
            full_text = opt_text + suffix
            self.options.append({'text': full_text, 'action': lambda o=opt: self._choose(o)})

    def announce_entry(self):
        self.current_index = 0
        if self.event_ctx:
            event = self.event_ctx["data"]
            desc = self.game_state.get_text(
                'dev_event_' + event['id'] + '_desc',
                default=self.game_state.get_text('aaa_event_title')
            )
            self.audio.speak(self.title)
            self.audio.speak(desc, interrupt=False)
        else:
            self.audio.speak(self.title)
        if self.options:
            self.speak_current(interrupt=False)

    def _choose(self, opt):
        gs = self.game_state
        ap = self.event_ctx["ap"]
        
        # Kosten abziehen
        cost = opt.get('cost', 0)
        if cost > 0:
            if gs.money < cost:
                self.audio.play_sound("error")
                self.audio.speak(gs.get_text('not_enough_money'))
                return None
            gs.track_expense("dev_event", cost)
            
        # ZeitverzÃ¶gerung
        delay = opt.get('delay', 0)
        if delay > 0:
            ap["total_weeks"] += delay
            
        # Beschleunigung
        speed = opt.get('speed', 0)
        if speed > 0:
            ap["progress"] = min(ap["total_weeks"], ap["progress"] + speed)
            
        # Hype (global)
        hype = opt.get('hype', 0)
        if hype != 0:
            gs.hype = max(0, gs.hype + hype)
            
        # Bugs
        bugs = opt.get('bugs', 0)
        if bugs > 0:
            ap["bugs"] += bugs
            
        # Moral (Team des Projekts)
        morale = opt.get('morale', 0)
        if morale != 0:
            active_emps = gs._active_employees(ap["project"])
            for emp in active_emps:
                emp.morale = max(0, min(100, emp.morale + morale))
                
        # Event abschliessen
        gs.pending_dev_event = None
        self.audio.play_sound("confirm")
        return "game_menu"


class InfluencerEventMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.event_data = getattr(game_state, 'pending_influencer_event', None)
        game_name = self.event_data["game_name"] if self.event_data else "Unbekanntes Spiel"
        
        super().__init__(self.game_state.get_text('influencer_event_title', default="INFLUENCER-SKANDAL!"), [], audio, game_state)
        self.audio.speak(self.game_state.get_text('influencer_event_desc', game=game_name, default=f"Boss! Unser gesponserter Streamer hat in {game_name} live vor Millionen Zuschauern Cheats verwendet und das Spiel beleidigt! Die PR ist ein Desaster. Was tun wir?"), interrupt=True)
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('error')
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('influencer_opt_1', default="Ã–ffentlich entschuldigen (-Fans, rettet Image)"), 'action': self._apologize},
            {'text': self.game_state.get_text('influencer_opt_2', default="Fristlos feuern & klagen (-Viel Geld, bewahrt Ehre)"), 'action': self._fire},
            {'text': self.game_state.get_text('influencer_opt_3', default="Ignorieren (Riskant, kann Langzeit-VerkÃ¤ufe ruinieren)"), 'action': self._ignore}
        ]

    def _apologize(self):
        self.game_state.fans = max(0, self.game_state.fans - 25000)
        self.audio.speak(self.game_state.get_text('influencer_res_1', default="Wir haben uns entschuldigt. Die Presse beruhigt sich, aber einige Hardcore-Fans sind weg."))
        self._clear_event()
        return "game_menu"

    def _fire(self):
        fine = 250000
        self.game_state.money -= fine
        self.game_state.track_expense("other", fine)
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('cash')
        self.audio.speak(self.game_state.get_text('influencer_res_2', cost=fine, default=f"Streamer gefeuert! Vertragsstrafen kosten uns {fine} â‚¬, aber die Gamer respektieren uns dafÃ¼r!"))
        self._clear_event()
        return "game_menu"

    def _ignore(self):
        if random.random() < 0.6:
            game_name = self.event_data["game_name"] if self.event_data else ""
            for g in self.game_state.game_history:
                if g.name == game_name:
                    g.sales = int(g.sales * 0.5)
                    g.is_active = False
            self.game_state.fans = max(0, int(self.game_state.fans * 0.8))
            self.audio.speak(self.game_state.get_text('influencer_res_3_bad', default="Das Ignorieren war ein Fehler! Ein gigantischer Shitstorm zerstÃ¶rt das Spiel und wir verlieren massig Fans!"))
        else:
            self.audio.speak(self.game_state.get_text('influencer_res_3_good', default="GlÃ¼ck gehabt. Das Internet hat den Skandal in wenigen Tagen vergessen. Keine Konsequenzen!"))
        self._clear_event()
        return "game_menu"

    def _clear_event(self):
        self.game_state.pending_influencer_event = None
        if self.event_data and "sponsorship" in self.event_data:
            s = self.event_data["sponsorship"]
            if s in self.game_state.active_sponsorships:
                self.game_state.streamer_hype_multi /= s["boost"]
                self.game_state.active_sponsorships.remove(s)


class UnionEventMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        raw_event = getattr(game_state, 'pending_union_event', None)
        self.event_data = raw_event if isinstance(raw_event, dict) else {"type": "formation"}
        
        if self.event_data.get("type", "formation") == "formation":
            title = self.game_state.get_text('union_form_title', default="GEWERKSCHAFTS-GRÃœNDUNG!")
            desc = self.game_state.get_text('union_form_desc', default="Boss, die miese Moral und der Stress haben das Fass zum Ãœberlaufen gebracht. Die Mitarbeiter haben eine Gewerkschaft gegrÃ¼ndet! Sie fordern sofortige Verhandlungen.")
        else:
            title = self.game_state.get_text('union_strike_title', default="STREIKDROHUNG!")
            desc = self.game_state.get_text('union_strike_desc', default="Die Gewerkschaft ist unzufrieden! Wenn wir nicht zahlen, legen sie ab morgen die Arbeit nieder. Was sollen wir tun?")
            
        super().__init__(title, [], audio, game_state)
        self.audio.speak(desc, interrupt=True)
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('error')
        self._update_options()

    def _update_options(self):
        self.options = [
            {'text': self.game_state.get_text('union_opt_1', default="GehÃ¤lter anpassen (+30% fÃ¼r alle, Moral steigt)"), 'action': self._raise_salaries},
            {'text': self.game_state.get_text('union_opt_2', default="Einmaliger Bonus (10k pro Mitarbeiter, keine DauerlÃ¶sung)"), 'action': self._pay_bonus},
            {'text': self.game_state.get_text('union_opt_3', default="Union-Busting betreiben (Feuert RÃ¤delsfÃ¼hrer, illegal & riskant)"), 'action': self._union_busting},
            {'text': self.game_state.get_text('union_opt_4', default="Ignorieren (STREIK!)"), 'action': self._ignore}
        ]

    def _raise_salaries(self):
        for emp in self.game_state.employees:
            emp.salary = int(emp.salary * 1.3)
            emp.morale = 100
        self.game_state.has_union = True
        self.audio.speak(self.game_state.get_text('union_res_1', default="Die GehÃ¤lter wurden erhÃ¶ht. Die Mitarbeiter sind glÃ¼cklich und die Arbeit geht weiter!"))
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('cash')
        self._clear_event()
        return "game_menu"

    def _pay_bonus(self):
        cost = len(self.game_state.employees) * 10000
        self.game_state.money -= cost
        self.game_state.track_expense("other", cost)
        for emp in self.game_state.employees:
            emp.morale = min(100, emp.morale + 30)
        self.game_state.has_union = True
        self.audio.speak(self.game_state.get_text('union_res_2', cost=cost, default=f"Ein Bonus von {cost} â‚¬ wurde gezahlt. Sie sind vorerst ruhig."))
        if hasattr(self.audio, 'play_sound'):
            self.audio.play_sound('cash')
        self._clear_event()
        return "game_menu"

    def _union_busting(self):
        # Fire 1-2 employees
        fired_count = min(random.randint(1, 2), len(self.game_state.employees))
        for _ in range(fired_count):
            self.game_state.employees.pop(random.randrange(len(self.game_state.employees)))
        
        self.game_state.fans = max(0, self.game_state.fans - 50000)
        
        if random.random() < 0.5:
            self.game_state.has_union = False
            self.audio.speak(self.game_state.get_text('union_res_3_success', default="RÃ¤delsfÃ¼hrer gefeuert! Die Gewerkschaft ist zerschlagen, aber die Fans sind angewidert!"))
        else:
            self.game_state.has_union = True
            fine = 500000
            self.game_state.money -= fine
            self.game_state.track_expense("other", fine)
            self.audio.speak(self.game_state.get_text('union_res_3_fail', default="Union-Busting aufgeflogen! Strafzahlung von 500.000 â‚¬! Fans hassen uns und die Gewerkschaft bleibt!"))
        self._clear_event()
        return "game_menu"

    def _ignore(self):
        self.game_state.has_union = True
        self.game_state.strike_weeks_left = random.randint(3, 6)
        self.audio.speak(self.game_state.get_text('union_res_4', default="STREIK! Die gesamte Spieleentwicklung ruht und es kostet uns jede Woche ein VermÃ¶gen!"))
        self._clear_event()
        return "game_menu"

    def _clear_event(self):
        self.game_state.pending_union_event = None
        self.game_state.stress_level = 0.0


class ExpoMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Spiele-Messe veranstalten", [], audio, game_state)
        self.state = "size"
        self.cost = 0
        self.base_hype = 0
        self._update_options()

    def _update_options(self):
        self.options = []
        if self.state == "size":
            self.title = "Spiele-Messe: StandgrÃ¶ÃŸe wÃ¤hlen"
            self.options.append({'text': self.game_state.get_text('expo_small_stand'), 'action': lambda: self._select_size(50000, 5)})
            self.options.append({'text': self.game_state.get_text('expo_medium_stand'), 'action': lambda: self._select_size(250000, 15)})
            self.options.append({'text': self.game_state.get_text('expo_large_stand'), 'action': lambda: self._select_size(1000000, 40)})
            self.options.append({'text': self.game_state.get_text('back'), 'action': lambda: "service_menu"})
        elif self.state == "demo":
            self.title = "Spiele-Messe: Demo zeigen?"
            # BUG-FIX v3.3.9: active_projects statt veraltetes dev_progress-Attribut nutzen
            first_prog = self.game_state.active_projects[0]["progress"] if self.game_state.active_projects else 0
            if self.game_state.is_developing and first_prog > 10:
                self.options.append({'text': self.game_state.get_text('expo_demo_current'), 'action': lambda: self._select_demo(10000, 5)})
            self.options.append({'text': self.game_state.get_text('expo_demo_none'), 'action': lambda: self._select_demo(0, 0)})
        elif self.state == "influencer":
            self.title = "Spiele-Messe: Influencer einladen?"
            self.options.append({'text': self.game_state.get_text('expo_influencer_hire'), 'action': lambda: self._select_influencer(100000, 10)})
            self.options.append({'text': self.game_state.get_text('expo_influencer_none'), 'action': lambda: self._select_influencer(0, 0)})
        elif self.state == "event":
            self.title = self.game_state.get_text('expo_event_overcrowded_title')
            self.options.append({'text': self.game_state.get_text('expo_event_overcrowded_opt1'), 'action': lambda: self._resolve_event("security")})
            self.options.append({'text': self.game_state.get_text('expo_event_overcrowded_opt2'), 'action': lambda: self._resolve_event("chaos")})

    def _select_size(self, cost, hype):
        if self.game_state.money < cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None
        self.cost += cost
        self.base_hype += hype
        self.state = "demo"
        self._update_options()
        self.announce_entry()
        return None

    def _select_demo(self, cost, hype):
        if self.game_state.money < self.cost + cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None
        self.cost += cost
        self.base_hype += hype
        self.state = "influencer"
        self._update_options()
        self.announce_entry()
        return None

    def _select_influencer(self, cost, hype):
        if self.game_state.money < self.cost + cost:
            self.audio.play_sound("error")
            self.audio.speak(self.game_state.get_text('not_enough_money'))
            return None
        self.cost += cost
        self.base_hype += hype
        
        if random.random() < 0.4:
            self.state = "event"
            self._update_options()
            self.announce_entry()
            return None
        else:
            return self._finish_expo()

    def _resolve_event(self, choice):
        if choice == "security":
            if self.game_state.money < self.cost + 50000:
                self.audio.play_sound("error")
                self.audio.speak(self.game_state.get_text('not_enough_money'))
                self._apply_chaos()
            else:
                self.cost += 50000
                self.audio.play_sound("cash")
                self.audio.speak(self.game_state.get_text('expo_event_security_safe'))
        elif choice == "chaos":
            if random.random() < 0.5:
                self.audio.play_sound("cheer")
                self.audio.speak(self.game_state.get_text('expo_event_success_mega'))
                self.base_hype *= 2
            else:
                self._apply_chaos()
        return self._finish_expo()

    def _apply_chaos(self):
        self.audio.play_sound("error")
        self.audio.speak(self.game_state.get_text('expo_event_fail_damage'))
        self.game_state.fans = max(0, self.game_state.fans - 10000)
        self.base_hype = max(0, self.base_hype - 10)

    def _finish_expo(self):
        self.game_state.track_expense("marketing", self.cost)
        self.game_state.hype += self.base_hype
        self.audio.play_sound("cheer")
        self.audio.speak(self.game_state.get_text('expo_finished', cost=self.cost, hype=self.base_hype))
        return "game_menu"
