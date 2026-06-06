from .base import Menu

class CommunityMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        title = self.game_state.get_text('community_menu_title')
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        self.options = []
        gs = self.game_state
        
        # 1. Fanpost-Eingang
        unresolved_count = len([m for m in getattr(gs, 'fan_mail_inbox', []) if not m.is_answered])
        fanmail_text = gs.get_text('fan_mail_inbox', count=unresolved_count)
        self.options.append({'text': fanmail_text, 'action': lambda: "fan_mail_inbox"})

        lab_text = gs.get_text(
            'access_lab_menu_option',
            score=getattr(gs, "accessibility_reputation", 0),
            weekly=gs.get_accessibility_weekly_fans()
        )
        self.options.append({'text': lab_text, 'action': lambda: "accessibility_lab"})
        
        # 2. Büro-Ereignis (nur wählbar, wenn eines aktiv ist)
        if getattr(gs, 'active_personality_event', None) is not None:
            emp = getattr(gs, 'active_personality_employee', None)
            emp_name = emp.name if emp else "Mitarbeiter"
            opt_text = gs.get_text('office_event_menu_title') + f" ({emp_name})"
            self.options.append({'text': opt_text, 'action': lambda: "office_event_menu"})
        else:
            # Ein inaktives Element zur Information
            opt_text = gs.get_text('office_event_menu_title') + " " + gs.get_text('jingle_no_active', default="(Keine aktiven)")
            self.options.append({'text': opt_text, 'action': self._no_event_action})
            
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "game_menu"})

    def _no_event_action(self):
        self.audio.play_sound("error")
        self.audio.speak(self.game_state.get_text('jingle_no_active', default="Keine aktiven Ereignisse."))
        return None


class AccessibilityLabMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__(self.game_state.get_text('access_lab_title'), [], audio, game_state)
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        score = getattr(gs, "accessibility_reputation", 0)
        weekly = gs.get_accessibility_weekly_fans()
        history_count = len(getattr(gs, "accessibility_lab_history", []))

        self.options = [{
            'text': gs.get_text(
                'access_lab_status',
                score=score,
                weekly=weekly,
                count=history_count
            ),
            'action': self._announce_status
        }]

        for action in gs.get_accessibility_lab_actions():
            text = gs.get_text(
                'access_lab_action_option',
                name=gs.get_text(action["name_key"]),
                cost=action["cost"],
                rep=action["reputation"],
                fans=action["fans"],
                hype=action["hype"]
            )
            self.options.append({
                'text': text,
                'action': lambda action_id=action["id"]: self._run_action(action_id)
            })

        self.options.append({'text': gs.get_text('back'), 'action': lambda: "community_menu"})

    def announce_entry(self):
        self.current_index = 0
        gs = self.game_state
        self.audio.speak(gs.get_text('access_lab_intro'))
        self.speak_current(interrupt=False)

    def _announce_status(self):
        gs = self.game_state
        self.audio.speak(
            gs.get_text(
                'access_lab_status',
                score=getattr(gs, "accessibility_reputation", 0),
                weekly=gs.get_accessibility_weekly_fans(),
                count=len(getattr(gs, "accessibility_lab_history", []))
            )
        )
        return None

    def _run_action(self, action_id):
        success, result = self.game_state.run_accessibility_lab_action(action_id)
        if not success:
            self.audio.play_sound("error")
            if result == "no_money":
                self.audio.speak(self.game_state.get_text('not_enough_money'))
            else:
                self.audio.speak(self.game_state.get_text('access_lab_failed'))
            return None

        self.audio.play_sound("confirm")
        self.audio.speak(
            self.game_state.get_text(
                'access_lab_success',
                name=self.game_state.get_text(result["name_key"]),
                score=getattr(self.game_state, "accessibility_reputation", 0)
            )
        )
        self._update_options()
        return None


class FanMailInboxMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        super().__init__("Fan-Post-Eingang", [], audio, game_state)
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        inbox = getattr(gs, 'fan_mail_inbox', [])
        unresolved_count = len([m for m in inbox if not m.is_answered])
        
        self.title = gs.get_text('fan_mail_inbox', count=unresolved_count)
        self.options = []
        
        for i, mail in enumerate(inbox):
            status = ""
            if not mail.is_read:
                status += gs.get_text('new_label') + " "
            if mail.is_answered:
                status += "[Beantwortet] "
            else:
                status += "[Offen] "
                
            sender = mail.sender
            # Betreff-Key übersetzen
            subject = gs.get_text(mail.subject_key)
            txt = f"{status}{sender}: {subject}"
            
            self.options.append({
                'text': txt,
                'action': lambda idx=i: self._select_mail(idx)
            })
            
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "community_menu"})

    def _select_mail(self, idx):
        inbox = getattr(self.game_state, 'fan_mail_inbox', [])
        if 0 <= idx < len(inbox):
            mail = inbox[idx]
            mail.is_read = True
            self.game_state.selected_fan_mail_id = mail.mail_id
            return "fan_mail_detail"
        return None


class FanMailDetailMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        self.mail = None
        
        mail_id = getattr(self.game_state, 'selected_fan_mail_id', None)
        inbox = getattr(self.game_state, 'fan_mail_inbox', [])
        self.mail = next((m for m in inbox if m.mail_id == mail_id), None)
        
        if self.mail:
            sender = self.mail.sender
            title = self.game_state.get_text('fan_mail_detail_title', sender=sender)
        else:
            title = "Fan-Post-Details"
            
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        self.options = []
        
        if not self.mail:
            self.options.append({'text': gs.get_text('back'), 'action': lambda: "fan_mail_inbox"})
            return
            
        if self.mail.is_answered:
            # Bereits beantwortet -> nur Info und zurück
            self.options.append({'text': gs.get_text('fan_mail_answered'), 'action': lambda: None})
            self.options.append({'text': gs.get_text('back'), 'action': lambda: "fan_mail_inbox"})
        else:
            # Antwortoptionen linear auflisten
            for idx, opt in enumerate(self.mail.options):
                opt_text = gs.get_text(opt['text_key'])
                btn_txt = gs.get_text('fan_mail_option_btn', idx=idx + 1, text=opt_text)
                self.options.append({
                    'text': btn_txt,
                    'action': lambda o_idx=idx: self._answer_mail(o_idx)
                })
            self.options.append({'text': gs.get_text('back'), 'action': lambda: "fan_mail_inbox"})

    def announce_entry(self):
        self.current_index = 0
        self.audio.speak(self.title)
        
        if self.mail:
            gs = self.game_state
            # Betreff und Inhalt vorlesen
            subject = gs.get_text(self.mail.subject_key)
            body = gs.get_text(self.mail.text_key)
            
            subj_text = gs.get_text('fan_mail_detail_subject', subject=subject)
            body_text = gs.get_text('fan_mail_detail_body', body=body)
            
            self.audio.speak(subj_text, interrupt=False)
            self.audio.speak(body_text, interrupt=False)
            
        if self.options:
            self.speak_current(interrupt=False)

    def _answer_mail(self, option_idx):
        if self.mail and not self.mail.is_answered:
            success = self.game_state.answer_fan_mail(self.mail.mail_id, option_idx)
            if success:
                self.audio.play_sound("confirm")
                # Verkündige die unmittelbaren Auswirkungen der Option
                opt = self.mail.options[option_idx]
                fans = opt.get('fans', 0)
                hype = opt.get('hype', 0.0)
                money = opt.get('money', 0)
                
                feedback = self.game_state.get_text('fan_mail_reply_success') + " "
                parts = []
                if fans != 0:
                    parts.append(f"{'+' if fans > 0 else ''}{fans} Fans")
                if hype != 0.0:
                    parts.append(f"{'+' if hype > 0 else ''}{hype:.1f} Hype")
                if money != 0:
                    parts.append(f"{'+' if money > 0 else ''}{money:,} €")
                
                if parts:
                    feedback += "(" + ", ".join(parts) + ")"
                    
                self.audio.speak(feedback)
            else:
                self.audio.play_sound("error")
        return "fan_mail_inbox"


class OfficeEventMenu(Menu):
    def __init__(self, audio, game_state):
        self.audio = audio
        self.game_state = game_state
        
        event = getattr(self.game_state, 'active_personality_event', None)
        if event:
            title = self.game_state.get_text('office_event_menu_title')
        else:
            title = "Büro-Ereignis"
            
        super().__init__(title, [], audio, game_state)
        self._update_options()

    def _update_options(self):
        gs = self.game_state
        self.options = []
        
        event = getattr(gs, 'active_personality_event', None)
        if not event:
            self.options.append({'text': gs.get_text('back'), 'action': lambda: "community_menu"})
            return
            
        # Optionen auflisten
        for idx, opt in enumerate(event['options']):
            opt_text = gs.get_text(opt['text_key'])
            btn_txt = gs.get_text('office_event_option', idx=idx + 1, text=opt_text)
            self.options.append({
                'text': btn_txt,
                'action': lambda o_idx=idx: self._resolve_event(o_idx)
            })
            
        self.options.append({'text': gs.get_text('back'), 'action': lambda: "community_menu"})

    def announce_entry(self):
        self.current_index = 0
        self.audio.speak(self.title)
        
        event = getattr(self.game_state, 'active_personality_event', None)
        emp = getattr(self.game_state, 'active_personality_employee', None)
        
        if event and emp:
            gs = self.game_state
            # Betroffenen Mitarbeiter & Beschreibung vorlesen
            trait_localized = gs.get_text(emp.personality) if gs.get_text(emp.personality) else emp.personality
            emp_info = gs.get_text('office_event_employee', name=emp.name, trait=trait_localized)
            desc = gs.get_text(event['text_key'])
            
            self.audio.speak(emp_info, interrupt=False)
            self.audio.speak(desc, interrupt=False)
            
        if self.options:
            self.speak_current(interrupt=False)

    def _resolve_event(self, option_idx):
        event = getattr(self.game_state, 'active_personality_event', None)
        if event:
            success = self.game_state.answer_personality_event(option_idx)
            if success:
                self.audio.play_sound("confirm")
                self.audio.speak(self.game_state.get_text('office_event_resolved'))
            else:
                self.audio.play_sound("error")
        return "community_menu"
