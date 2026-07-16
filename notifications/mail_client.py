from notifications.event_system import dispatcher, Event
from models import Email

class MailClient:
    """
    Listens to events from the EventDispatcher and generates translated
    emails or UI notifications, decoupling presentation from logic.
    """
    def __init__(self, game_state):
        self.game_state = game_state
        self._register_listeners()

    def _register_listeners(self):
        # Base/test
        dispatcher.add_listener("game_started", self.on_game_started)
        
        # HR
        dispatcher.add_listener("employee_hired", self.on_employee_hired)
        dispatcher.add_listener("strike_ended", self.on_strike_ended)
        dispatcher.add_listener("training_done", self.on_training_done)
        dispatcher.add_listener("burnout", self.on_burnout)
        dispatcher.add_listener("sick_recovered", self.on_sick_recovered)
        dispatcher.add_listener("sick", self.on_sick)
        dispatcher.add_listener("burnout_quit", self.on_burnout_quit)
        dispatcher.add_listener("salary_raise_request", self.on_salary_raise_request)
        dispatcher.add_listener("employee_quit", self.on_employee_quit)
        dispatcher.add_listener("poach_offer", self.on_poach_offer)
        dispatcher.add_listener("employee_left_poach", self.on_employee_left_poach)
        
        # Marketing
        dispatcher.add_listener("merch_ended", self.on_merch_ended)
        dispatcher.add_listener("cf_fail", self.on_cf_fail)
        dispatcher.add_listener("intel_report", self.on_intel_report)
        dispatcher.add_listener("soundcon_announcement", self.on_soundcon_announcement)
        
        # Finance
        dispatcher.add_listener("yearly_report", self.on_yearly_report)
        dispatcher.add_listener("loan_paid", self.on_loan_paid)

    def _send_mail(self, sender: str, subject: str, body: str, **kwargs):
        mail = Email(
            sender=sender,
            subject=subject,
            body=body,
            date_week=self.game_state.week if self.game_state else 1
        )
        for k, v in kwargs.items():
            setattr(mail, k, v)
            
        if self.game_state and hasattr(self.game_state, 'emails'):
            self.game_state.emails.insert(0, mail)
        else:
            print(f"MailClient | NEW MAIL - Subject: {subject} | Body: {body}")

    def get_text(self, key: str, **kwargs) -> str:
        if self.game_state and hasattr(self.game_state, 'get_text'):
            return self.game_state.get_text(key, **kwargs)
        return key

    # --- Event Handlers ---

    def on_game_started(self, event: Event):
        self._send_mail("System", "Welcome!", "Welcome to Audio Studio Tycoon.")

    def on_employee_hired(self, event: Event):
        emp_name = event.data.get("name", "Unknown Employee")
        self._send_mail("HR", f"New Employee: {emp_name}", f"We have successfully hired {emp_name}.")

    # HR Events
    def on_strike_ended(self, event: Event):
        self._send_mail(
            self.get_text('sender_union'),
            self.get_text('subject_strike_ended'),
            self.get_text('body_strike_ended')
        )

    def on_training_done(self, event: Event):
        emp = event.data["emp"]
        self._send_mail(
            self.get_text('sender_hr'),
            self.get_text('subject_training_done', name=emp.name),
            self.get_text('body_training_done', name=emp.name, skill=emp.primary_skill, value=emp.skills[emp.primary_skill])
        )

    def on_burnout(self, event: Event):
        emp = event.data["emp"]
        self._send_mail(
            self.get_text('sender_hr'),
            self.get_text('subject_burnout', default='Mitarbeiter-Burnout!'),
            self.get_text('body_burnout', name=emp.name, default=f'{emp.name} hat einen Burnout erlitten und faellt fuer {emp.sick_weeks_left} Wochen aus!')
        )

    def on_sick_recovered(self, event: Event):
        emp = event.data["emp"]
        self._send_mail(
            self.get_text('sender_hr'),
            self.get_text('subject_sick_recovered', name=emp.name),
            self.get_text('body_sick_recovered', name=emp.name)
        )

    def on_sick(self, event: Event):
        emp = event.data["emp"]
        self._send_mail(
            self.get_text('sender_hr'),
            self.get_text('subject_sick', name=emp.name),
            self.get_text('body_sick', name=emp.name, weeks=emp.sick_weeks_left)
        )

    def on_burnout_quit(self, event: Event):
        emp = event.data["emp"]
        self._send_mail(
            self.get_text('sender_hr'),
            self.get_text('subject_burnout_quit'),
            self.get_text('body_burnout_quit', name=emp.name)
        )

    def on_salary_raise_request(self, event: Event):
        emp = event.data["emp"]
        new_salary = event.data["new_salary"]
        self._send_mail(
            emp.name,
            self.get_text('subject_salary_raise'),
            self.get_text('body_salary_raise', name=emp.name, current=emp.salary, expected=new_salary),
            is_salary_request=True,
            employee_idx=event.data["emp_idx"],
            requested_salary=new_salary
        )

    def on_employee_quit(self, event: Event):
        emp = event.data["emp"]
        self._send_mail(
            emp.name,
            self.get_text('subject_quit'),
            self.get_text('body_quit', name=emp.name)
        )

    def on_poach_offer(self, event: Event):
        emp = event.data["emp"]
        offer_salary = event.data["offer_salary"]
        self._send_mail(
            "Headhunter",
            self.get_text('subject_poach_offer', name=emp.name),
            self.get_text('body_poach_offer', name=emp.name, rival=event.data["rival_name"], salary=offer_salary),
            is_poach_offer=True,
            employee_idx=event.data["emp_idx"],
            offered_salary=offer_salary
        )

    def on_employee_left_poach(self, event: Event):
        emp = event.data["emp"]
        self._send_mail(
            "System",
            self.get_text('subject_employee_left', name=emp.name),
            self.get_text('body_employee_left_poach', name=emp.name)
        )

    # Marketing Events
    def on_merch_ended(self, event: Event):
        d = event.data
        self._send_mail(
            self.get_text("sender_marketing"),
            f"Merch beendet: {d['game_name']}",
            f"Die {d['merch_type']}-Kampagne für {d['game_name']} ist beendet.\nGesamtumsatz: {d['total_revenue']} Euro"
        )

    def on_cf_fail(self, event: Event):
        proj = event.data["project_name"]
        self._send_mail(
            self.get_text('sender_angry_backers', default="Wütende Backer"),
            self.get_text('subject_cf_fail', default="Wo ist unser Spiel?!"),
            self.get_text('body_cf_fail', name=proj, default=f"Wir haben {proj} vor einem Jahr unterstützt und es ist immer noch nicht fertig! Betrug!")
        )

    def on_intel_report(self, event: Event):
        d = event.data
        self._send_mail(
            self.get_text('sender_intel'),
            self.get_text('subject_intel_report', name=d["target_name"]),
            self.get_text('body_intel_report', name=d["target_name"], genre=self.get_text(d["genre"]))
        )

    def on_soundcon_announcement(self, event: Event):
        year = event.data["year"]
        self._send_mail(
            self.get_text('soundcon_sender'),
            self.get_text('soundcon_email_subject', year=year),
            self.get_text('soundcon_email_body')
        )

    # Finance Events
    def on_yearly_report(self, event: Event):
        d = event.data
        self._send_mail(
            self.get_text('sender_accounting'),
            self.get_text('subject_yearly_report', year=d["year"]),
            self.get_text('body_yearly_report', income=d["income"], expenses=d["expenses"], profit=d["profit"])
        )

    def on_loan_paid(self, event: Event):
        self._send_mail(
            self.get_text('sender_bank'),
            self.get_text('subject_loan_paid'),
            self.get_text('body_loan_paid')
        )
