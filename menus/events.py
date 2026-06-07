"""
Menüs für SoundCon-Messe und Soundtrack-Label – Audio Studio Tycoon.

Alle Menüs sind vollständig über Tastatur steuerbar (Pfeiltasten, Enter,
Backspace) und senden jede Ausgabe über audio.speak() an den Screenreader.
Keine ASCII-Art, keine visuellen Tabellen.
"""

from .base import Menu, TextInputMenu
from models import SoundtrackLabel


# ═══════════════════════════════════════════════════════════════
#  SoundCon – Hauptmenü
# ═══════════════════════════════════════════════════════════════

class SoundConMenu(Menu):
    """Hauptmenü der jährlichen SoundCon-Spielemesse.

    Erlaubt das Buchen eines Messestandes, das Abhalten von Q&A-Runden
    und den Abschluss der Messe.
    """

    def __init__(self, audio, game_state):
        gs = game_state
        options = self._build_options(gs)
        super().__init__(
            title=gs.get_text('soundcon_menu_title'),
            options=options,
            audio=audio,
            game_state=gs
        )

    def _build_options(self, gs):
        """Baut die Menüoptionen dynamisch je nach Spielzustand."""
        opts = []
        can, reason = gs.can_attend_soundcon()

        if gs.active_soundcon:
            # Bereits gebucht: QA und Abschluss anbieten
            ev = gs.active_soundcon
            qa_left = 3 - ev.qa_rounds
            if qa_left > 0:
                opts.append({
                    'text': gs.get_text('soundcon_opt_qa', rounds=ev.qa_rounds, max=3),
                    'action': 'soundcon_qa'
                })
            opts.append({
                'text': gs.get_text('soundcon_opt_finish', tier=gs.get_text(f'soundcon_tier_{ev.booth_tier}')),
                'action': 'soundcon_finish'
            })
        elif can:
            # Noch kein Stand gebucht
            for tier_key, tier_data in [
                ('klein',   gs.get_text('soundcon_tier_klein')),
                ('mittel',  gs.get_text('soundcon_tier_mittel')),
                ('groß',    gs.get_text('soundcon_tier_gross')),
                ('keynote', gs.get_text('soundcon_tier_keynote')),
            ]:
                cost = gs.get_text('soundcon_tier_cost',
                                   tier=tier_data,
                                   cost=SoundtrackLabel.RADIO_STATIONS[0]["cost"])
                # Kosten direkt aus Modell
                from models import SoundConEvent
                booth_cost = SoundConEvent.BOOTH_TIERS[tier_key]["cost"]
                affordable = "✓" if gs.money >= booth_cost else "✗"
                opts.append({
                    'text': gs.get_text('soundcon_booth_option',
                                        tier=tier_data,
                                        cost=booth_cost,
                                        affordable=affordable),
                    'action': f'soundcon_book_{tier_key}'
                })
        else:
            # Nicht möglich
            opts.append({
                'text': gs.get_text(reason if reason else 'soundcon_already_attended'),
                'action': None
            })

        # SoundCon-History
        if gs.soundcon_history:
            opts.append({
                'text': gs.get_text('soundcon_opt_history', count=len(gs.soundcon_history)),
                'action': 'soundcon_history'
            })

        opts.append({'text': gs.get_text('back'), 'action': 'back_to_game'})
        return opts

    def announce_entry(self):
        gs = self.game_state
        year = gs.get_calendar_year()
        intro = gs.get_text('soundcon_menu_intro', year=year)
        if gs.active_soundcon:
            ev = gs.active_soundcon
            intro += " " + gs.get_text('soundcon_booth_active',
                                        tier=gs.get_text(f'soundcon_tier_{ev.booth_tier}'),
                                        qa=ev.qa_rounds)
        self.audio.speak(intro)
        if self.options:
            self.speak_current(interrupt=False)

    def handle_input(self, event):
        result = super().handle_input(event)
        if result is not None:
            return result

        gs = self.game_state
        if event.key == gs.key_confirm and self.options:
            action = self.options[self.current_index].get('action')

            # Stand buchen
            if action and action.startswith('soundcon_book_'):
                tier = action.replace('soundcon_book_', '')
                success = gs.book_soundcon_booth(tier)
                if success:
                    self.audio.play_sound('confirm')
                    self.audio.speak(gs.get_text('soundcon_booked_ok',
                                                  tier=gs.get_text(f'soundcon_tier_{tier}')))
                    return 'soundcon_menu'  # Menü neu aufbauen
                else:
                    self.audio.play_sound('error')
                    self.audio.speak(gs.get_text('soundcon_not_enough_money'))

            elif action == 'soundcon_qa':
                res = gs.conduct_soundcon_qa()
                if res.get('success'):
                    self.audio.play_sound('confirm')
                    self.audio.speak(gs.get_text('soundcon_qa_done', round=res['qa_round']))
                    return 'soundcon_menu'
                else:
                    self.audio.play_sound('bump')
                    self.audio.speak(gs.get_text(res.get('message', 'error')))

            elif action == 'soundcon_finish':
                return 'soundcon_finish_confirm'

            elif action == 'soundcon_history':
                return 'soundcon_history_menu'

            elif action == 'back_to_game':
                return 'back_to_game'

            elif action is None:
                self.audio.play_sound('bump')

        return None


class SoundConFinishMenu(Menu):
    """Bestätigungs-Menü vor dem Abschluss der SoundCon."""

    def __init__(self, audio, game_state):
        gs = game_state
        ev = gs.active_soundcon
        tier_text = gs.get_text(f'soundcon_tier_{ev.booth_tier}') if ev else "?"
        qa = ev.qa_rounds if ev else 0

        options = [
            {'text': gs.get_text('soundcon_confirm_finish_yes'), 'action': 'finish_yes'},
            {'text': gs.get_text('soundcon_confirm_finish_no'),  'action': 'finish_no'},
        ]
        super().__init__(
            title=gs.get_text('soundcon_finish_title', tier=tier_text, qa=qa),
            options=options,
            audio=audio,
            game_state=gs
        )
        self._tier_text = tier_text
        self._qa = qa

    def announce_entry(self):
        gs = self.game_state
        ev = gs.active_soundcon
        if ev:
            # Vorschau auf Ergebnis ansagen (ohne anzuwenden)
            preview_hype = round(ev.base_hype * (1.0 + gs.prestige / 200.0) * (1.0 + ev.qa_rounds * 0.15), 1)
            preview_fans = int(ev.base_fans * (1.0 + gs.prestige / 200.0) * (1.0 + ev.qa_rounds * 0.15))
            self.audio.speak(
                gs.get_text('soundcon_finish_preview',
                             tier=self._tier_text, qa=self._qa,
                             hype=preview_hype, fans=preview_fans)
            )
        if self.options:
            self.speak_current(interrupt=False)

    def handle_input(self, event):
        result = super().handle_input(event)
        if result is not None:
            return result

        gs = self.game_state
        if event.key == gs.key_confirm and self.options:
            action = self.options[self.current_index].get('action')
            if action == 'finish_yes':
                res = gs.finish_soundcon()
                if res:
                    self.audio.play_sound('success')
                    self.audio.speak(
                        gs.get_text('soundcon_result_announce', fans=res.get('fans', 0))
                    )
                    return 'soundcon_result_menu'
                else:
                    self.audio.play_sound('error')
                    return 'soundcon_menu'
            elif action == 'finish_no':
                return 'soundcon_menu'
        return None


class SoundConResultMenu(Menu):
    """Zeigt die Ergebnisse der abgeschlossenen SoundCon an."""

    def __init__(self, audio, game_state):
        gs = game_state
        result = gs.pending_soundcon_result or {}
        tier_key = result.get('tier', 'klein')
        tier_text = gs.get_text(f'soundcon_tier_{tier_key}')

        lines = [
            gs.get_text('soundcon_result_hype',     hype=result.get('hype', 0)),
            gs.get_text('soundcon_result_fans',      fans=result.get('fans', 0)),
            gs.get_text('soundcon_result_prestige',  prestige=result.get('prestige', 0)),
            gs.get_text('soundcon_result_qa_rounds', qa=result.get('qa', 0)),
            gs.get_text('soundcon_result_tier',      tier=tier_text),
        ]
        summary = " | ".join(lines)

        options = [
            {'text': summary,                      'action': None},
            {'text': gs.get_text('menu_continue'), 'action': 'back_to_game'},
        ]
        super().__init__(
            title=gs.get_text('soundcon_result_title', year=gs.get_calendar_year()),
            options=options,
            audio=audio,
            game_state=gs
        )
        # Ergebnis nach Anzeige konsumieren
        gs.pending_soundcon_result = None

    def announce_entry(self):
        self.audio.speak(self.title)
        # Alle Ergebnis-Zeilen vorlesen
        for opt in self.options[:-1]:
            self.audio.speak(opt['text'], interrupt=False)
        self.speak_current(interrupt=False)

    def handle_input(self, event):
        result = super().handle_input(event)
        if result is not None:
            return result

        gs = self.game_state
        if event.key == gs.key_confirm and self.options:
            action = self.options[self.current_index].get('action')
            if action == 'back_to_game':
                return 'back_to_game'
            elif action is None:
                self.audio.play_sound('bump')
        return None


class SoundConHistoryMenu(Menu):
    """Zeigt die vergangenen SoundCon-Teilnahmen an."""

    def __init__(self, audio, game_state):
        gs = game_state
        options = []
        for ev in reversed(gs.soundcon_history):
            tier_text = gs.get_text(f'soundcon_tier_{ev.booth_tier}')
            options.append({
                'text': gs.get_text('soundcon_history_entry',
                                     year=ev.year, tier=tier_text,
                                     fans=ev.fans_gained, hype=ev.hype_gained,
                                     qa=ev.qa_rounds),
                'action': None
            })
        if not options:
            options.append({'text': gs.get_text('soundcon_no_history'), 'action': None})
        options.append({'text': gs.get_text('back'), 'action': 'soundcon_menu'})

        super().__init__(
            title=gs.get_text('soundcon_history_title'),
            options=options,
            audio=audio,
            game_state=gs
        )

    def handle_input(self, event):
        result = super().handle_input(event)
        if result is not None:
            return result

        gs = self.game_state
        if event.key == gs.key_confirm and self.options:
            action = self.options[self.current_index].get('action')
            if action == 'soundcon_menu':
                return 'soundcon_menu'
            elif action is None:
                self.audio.play_sound('bump')
        return None


# ═══════════════════════════════════════════════════════════════
#  Soundtrack-Label
# ═══════════════════════════════════════════════════════════════

class SoundtrackLabelMenu(Menu):
    """Hauptmenü des Soundtrack-Labels.

    Ermöglicht das Gründen eines Labels, das Hinzufügen von Radioverträgen
    und das Anzeigen des Label-Status.
    """

    def __init__(self, audio, game_state):
        gs = game_state
        options = self._build_options(gs)
        super().__init__(
            title=gs.get_text('label_menu_title'),
            options=options,
            audio=audio,
            game_state=gs
        )

    def _build_options(self, gs):
        opts = []
        label = gs.soundtrack_label

        if label is None:
            # Label noch nicht gegründet
            opts.append({
                'text': gs.get_text('label_opt_found', cost=30_000),
                'action': 'label_found'
            })
        else:
            # Label bereits gegründet
            active_contracts = len(label.active_radio_contracts)
            opts.append({
                'text': gs.get_text('label_opt_status',
                                     name=label.label_name,
                                     games=len(label.catalogued_games),
                                     contracts=active_contracts,
                                     royalties=round(label.total_royalties, 0)),
                'action': 'label_status'
            })
            opts.append({
                'text': gs.get_text('label_opt_radio'),
                'action': 'label_radio'
            })
            opts.append({
                'text': gs.get_text('label_opt_add_game'),
                'action': 'label_add_game'
            })
            opts.append({
                'text': gs.get_text('label_opt_compilation', cost=25_000),
                'action': 'label_compilation'
            })
            opts.append({
                'text': gs.get_text('label_opt_concert', cost=100_000),
                'action': 'label_concert'
            })

        opts.append({'text': gs.get_text('back'), 'action': 'back_to_game'})
        return opts

    def announce_entry(self):
        gs = self.game_state
        label = gs.soundtrack_label
        if label:
            intro = gs.get_text('label_menu_intro_active',
                                 name=label.label_name,
                                 weekly=round(
                                     sum(c.weekly_royalties for c in label.active_radio_contracts)
                                     + len(label.catalogued_games) * 50, 0
                                 ))
        else:
            intro = gs.get_text('label_menu_intro_none', cost=30_000)
        self.audio.speak(intro)
        if self.options:
            self.speak_current(interrupt=False)

    def handle_input(self, event):
        result = super().handle_input(event)
        if result is not None:
            return result

        gs = self.game_state
        if event.key == gs.key_confirm and self.options:
            action = self.options[self.current_index].get('action')

            if action == 'label_found':
                return 'label_name_input'

            elif action == 'label_status':
                return 'label_status_menu'

            elif action == 'label_radio':
                return 'label_radio_menu'

            elif action == 'label_add_game':
                return 'label_add_game_menu'

            elif action == 'label_compilation':
                if len(gs.soundtrack_label.catalogued_games) < 3:
                    self.audio.play_sound('error')
                    self.audio.speak(gs.get_text('label_compilation_fail_games'))
                elif gs.money < 25000:
                    self.audio.play_sound('error')
                    self.audio.speak(gs.get_text('label_compilation_fail_money', cost=25_000))
                else:
                    gs.track_expense("other", 25000)
                    gs.soundtrack_label.compilation_albums_released += 1
                    # Base revenue per game in catalog + randomness
                    import random
                    base = len(gs.soundtrack_label.catalogued_games) * 15000
                    bonus = random.randint(5000, 30000)
                    total_revenue = base + bonus
                    hype_boost = min(30, len(gs.soundtrack_label.catalogued_games) * 2 + random.randint(5, 15))
                    
                    gs.track_income("other", total_revenue)
                    gs.hype = min(250, gs.hype + hype_boost)
                    gs.soundtrack_label.prestige_bonus += 2
                    
                    self.audio.play_sound('success')
                    self.audio.speak(gs.get_text('label_compilation_success', revenue=total_revenue, hype=hype_boost))
                return None

            elif action == 'label_concert':
                if len(gs.soundtrack_label.catalogued_games) < 5:
                    self.audio.play_sound('error')
                    self.audio.speak(gs.get_text('label_concert_fail_games'))
                elif gs.money < 100000:
                    self.audio.play_sound('error')
                    self.audio.speak(gs.get_text('label_concert_fail_money', cost=100_000))
                else:
                    gs.track_expense("other", 100000)
                    import random
                    base = len(gs.soundtrack_label.catalogued_games) * 25000
                    bonus = random.randint(50000, 150000)
                    total_revenue = base + bonus
                    hype_boost = min(100, len(gs.soundtrack_label.catalogued_games) * 5 + random.randint(20, 50))
                    
                    gs.track_income("other", total_revenue)
                    gs.hype = min(250, gs.hype + hype_boost)
                    gs.soundtrack_label.prestige_bonus += 5
                    
                    self.audio.play_sound('success')
                    self.audio.speak(gs.get_text('label_concert_success', revenue=total_revenue, hype=hype_boost))
                return None

            elif action == 'back_to_game':
                return 'back_to_game'

            elif action is None:
                self.audio.play_sound('bump')

        return None


class LabelNameInputMenu(TextInputMenu):
    """Texteingabe für den Namen des neuen Soundtrack-Labels."""

    def __init__(self, audio, game_state):
        gs = game_state
        super().__init__(
            title=gs.get_text('label_name_prompt'),
            prompt='label_name_prompt',
            audio=audio,
            game_state=gs,
            on_confirm=self._on_confirm,
            on_cancel=self._on_cancel
        )

    def _on_confirm(self, text: str):
        gs = self.game_state
        name = text.strip()[:40]
        if not name:
            self.audio.play_sound('error')
            self.audio.speak(gs.get_text('label_name_empty'))
            return None

        success = gs.found_soundtrack_label(name)
        if success:
            self.audio.play_sound('success')
            self.audio.speak(gs.get_text('label_founded_announce', name=name))
            return 'label_menu'
        else:
            self.audio.play_sound('error')
            if gs.soundtrack_label:
                self.audio.speak(gs.get_text('label_already_exists'))
            else:
                self.audio.speak(gs.get_text('label_not_enough_money', cost=30_000))
            return 'label_menu'

    def _on_cancel(self):
        return 'label_menu'


class LabelStatusMenu(Menu):
    """Zeigt den aktuellen Status des Soundtrack-Labels."""

    def __init__(self, audio, game_state):
        gs = game_state
        label = gs.soundtrack_label
        options = []

        if label:
            options.append({
                'text': gs.get_text('label_status_name',       name=label.label_name),
                'action': None
            })
            options.append({
                'text': gs.get_text('label_status_games',      count=len(label.catalogued_games)),
                'action': None
            })
            options.append({
                'text': gs.get_text('label_status_contracts',  count=len(label.active_radio_contracts)),
                'action': None
            })
            options.append({
                'text': gs.get_text('label_status_royalties',  total=round(label.total_royalties, 0)),
                'action': None
            })
            # Einzelne Verträge aufzählen
            for c in label.active_radio_contracts:
                options.append({
                    'text': gs.get_text('label_status_contract_entry',
                                         station=c.station_name,
                                         weekly=round(c.weekly_royalties, 0),
                                         weeks_left=c.weeks_remaining),
                    'action': None
                })
        else:
            options.append({'text': gs.get_text('label_not_founded'), 'action': None})

        options.append({'text': gs.get_text('back'), 'action': 'label_menu'})

        super().__init__(
            title=gs.get_text('label_status_title'),
            options=options,
            audio=audio,
            game_state=gs
        )

    def announce_entry(self):
        self.audio.speak(self.title)
        # Alle Status-Zeilen vorlesen
        for opt in self.options[:-1]:
            self.audio.speak(opt['text'], interrupt=False)
        self.speak_current(interrupt=False)

    def handle_input(self, event):
        result = super().handle_input(event)
        if result is not None:
            return result

        gs = self.game_state
        if event.key == gs.key_confirm and self.options:
            action = self.options[self.current_index].get('action')
            if action == 'label_menu':
                return 'label_menu'
            elif action is None:
                self.audio.play_sound('bump')
        return None


class LabelRadioMenu(Menu):
    """Zeigt verfügbare Radiosender zum Vertragsabschluss."""

    def __init__(self, audio, game_state):
        gs = game_state
        options = []

        for station in SoundtrackLabel.RADIO_STATIONS:
            # Prüfe ob Sender bereits unter Vertrag steht
            already = False
            if gs.soundtrack_label:
                already = any(
                    c.station_name == station["name"]
                    for c in gs.soundtrack_label.active_radio_contracts
                )
            affordable = gs.money >= station["cost"]
            status = ""
            if already:
                status = gs.get_text('label_radio_already')
            elif not affordable:
                status = gs.get_text('label_radio_too_expensive')

            options.append({
                'text': gs.get_text('label_radio_option',
                                     name=station["name"],
                                     cost=station["cost"],
                                     royalties=station["royalties"],
                                     weeks=station["weeks"],
                                     hype=station["hype"],
                                     status=status),
                'action': None if (already or not affordable) else f'sign_{station["name"]}',
                '_station': station
            })

        options.append({'text': gs.get_text('back'), 'action': 'label_menu'})

        super().__init__(
            title=gs.get_text('label_radio_title'),
            options=options,
            audio=audio,
            game_state=gs
        )

    def announce_entry(self):
        gs = self.game_state
        self.audio.speak(gs.get_text('label_radio_intro'))
        if self.options:
            self.speak_current(interrupt=False)

    def handle_input(self, event):
        result = super().handle_input(event)
        if result is not None:
            return result

        gs = self.game_state
        if event.key == gs.key_confirm and self.options:
            opt = self.options[self.current_index]
            action = opt.get('action')

            if action and action.startswith('sign_'):
                station = opt.get('_station')
                if station:
                    success = gs.sign_radio_contract(station)
                    if success:
                        self.audio.play_sound('success')
                        self.audio.speak(
                            gs.get_text('label_radio_signed', station=station["name"])
                        )
                        return 'label_radio_menu'  # Neu aufbauen
                    else:
                        self.audio.play_sound('error')
                        self.audio.speak(gs.get_text('label_not_enough_money', cost=station["cost"]))

            elif action == 'label_menu':
                return 'label_menu'

            elif action is None:
                self.audio.play_sound('bump')

        return None


class LabelAddGameMenu(Menu):
    """Menü zum manuellen Hinzufügen von Spielen zum Label-Katalog."""

    def __init__(self, audio, game_state):
        gs = game_state
        options = []
        label = gs.soundtrack_label

        if label:
            available = [g for g in gs.game_history if g.name not in label.catalogued_games]
            if available:
                for game in available:
                    options.append({
                        'text': gs.get_text('label_add_game_option',
                                             name=game.name,
                                             genre=gs.get_text(game.genre)),
                        'action': f'add_{game.name}'
                    })
            else:
                options.append({
                    'text': gs.get_text('label_all_games_added'),
                    'action': None
                })
        else:
            options.append({'text': gs.get_text('label_not_founded'), 'action': None})

        options.append({'text': gs.get_text('back'), 'action': 'label_menu'})

        super().__init__(
            title=gs.get_text('label_add_game_title'),
            options=options,
            audio=audio,
            game_state=gs
        )

    def handle_input(self, event):
        result = super().handle_input(event)
        if result is not None:
            return result

        gs = self.game_state
        if event.key == gs.key_confirm and self.options:
            opt = self.options[self.current_index]
            action = opt.get('action')

            if action and action.startswith('add_'):
                game_name = action[4:]
                if gs.soundtrack_label:
                    gs.soundtrack_label.add_game(game_name)
                    self.audio.play_sound('confirm')
                    self.audio.speak(gs.get_text('label_game_added', name=game_name))
                    return 'label_add_game_menu'  # Neu aufbauen

            elif action == 'label_menu':
                return 'label_menu'

            elif action is None:
                self.audio.play_sound('bump')

        return None


class SoundConQAMenu(Menu):
    """Interaktives Q&A Menü für die SoundCon."""
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.round_num = getattr(game_state.active_soundcon, 'qa_rounds', 0) + 1 if game_state.active_soundcon else 1
        
        import random
        self.q_idx = random.randint(1, 3)
        question = self.game_state.get_text(f'soundcon_qa_question_{self.q_idx}')
        
        options = []
        if self.q_idx == 1:
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_1_1'), 'action': lambda: self._answer(15, 0, 0, 'hype')})
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_1_2'), 'action': lambda: self._answer(2, 5, 0, 'neutral')})
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_1_3'), 'action': lambda: self._answer(0, 0, 0, 'neutral')})
        elif self.q_idx == 2:
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_2_1'), 'action': lambda: self._answer(20, -5, 0, 'hype')})
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_2_2'), 'action': lambda: self._answer(5, 10, 500, 'prestige')})
        elif self.q_idx == 3:
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_3_1'), 'action': lambda: self._answer(25, 0, 0, 'hype')})
            options.append({'text': self.game_state.get_text('soundcon_qa_ans_3_2'), 'action': lambda: self._answer(5, 15, 0, 'prestige')})
            
        super().__init__(question, options, audio, game_state)
        
    def _answer(self, hype, prestige, fans, result_type):
        res = self.game_state.conduct_soundcon_qa_interactive(hype, prestige, fans)
        if res['success']:
            if result_type == 'hype':
                msg = self.game_state.get_text('soundcon_qa_result_hype', hype=hype)
            elif result_type == 'prestige':
                msg = self.game_state.get_text('soundcon_qa_result_prestige', prestige=prestige, fans=fans)
            else:
                msg = self.game_state.get_text('soundcon_qa_result_neutral', fans=fans)
                
            self.audio.speak(msg)
        return 'soundcon_menu'
