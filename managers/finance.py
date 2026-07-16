import random
from models import Email
from game_data import WEEKS_PER_YEAR

class FinanceManager:
    def __init__(self, state):
        self.state = state

    def tick(self, is_new_month):
        self._process_passive_income()
        self._process_office_perks()
        
        if (self.state.week == 1) or (is_new_month and self.state.week > 4):
            self.state._send_monthly_bank_statement()
            self.state._process_streaming_platform_monthly()

        self._process_yearly_accounting()
        self._check_bankruptcy()
        self._process_salaries(is_new_month)
        self._process_bank_loan()

    def _process_passive_income(self):
        for rival in self.state.rivals:
            if getattr(rival, 'is_owned_by_player', False):
                passive_income = random.randint(10000, 50000)
                self.state.money += passive_income
                self.state.track_income("other", passive_income)

    def _process_office_perks(self):
        if getattr(self.state, 'office_perks', []):
            perk_cost = 0
            for perk in self.state.office_perks:
                if perk == "hr_department": perk_cost += 10000
                elif perk == "therapist": perk_cost += 5000
                elif perk == "wellness_benefits": perk_cost += 2000
                else: perk_cost += 500
                
            self.state.money -= perk_cost
            self.state.track_expense("other", perk_cost)

    def _process_yearly_accounting(self):
        if (self.state.week - 1) % WEEKS_PER_YEAR == 0:
            if self.state.week > 1 and hasattr(self.state, "accounting"):
                inc = self.state.accounting.get("income", 0)
                exp = self.state.accounting.get("expenses", 0)
                prof = inc - exp
                from notifications import dispatcher, Event
                dispatcher.dispatch(Event("yearly_report", {"year": self.state.get_calendar_year() - 1, "income": inc, "expenses": exp, "profit": prof}))
            self.state.accounting = {"income": 0, "expenses": 0, "loan_paid": 0}
            self.state._unlock_historical_topics()

    def _check_bankruptcy(self):
        if self.state.is_bankrupt() and not getattr(self.state, "pending_bankrupt", False):
            self.state.pending_bankrupt = True
            self.state.time_speed = 0
            if hasattr(self.state, 'audio'):
                self.state.audio.play_sound('warn')
                self.state.audio.speak(self.state.get_text('bankruptcy_warning'), interrupt=True)
            
        if self.state.money < 5000 and self.state.week > 10:
            if hasattr(self.state, 'audio'):
                self.state.audio.play_sound('warn')
                self.state.audio.speak(self.state.get_text('low_money_warning', amount=self.state.money), interrupt=False)

    def _process_salaries(self, is_new_month):
        self.state.pay_salaries()
        
        if is_new_month and self.state.week > 1:
            total_salary = self.state.accrued_salaries
            self.state.track_expense("salaries", total_salary)
            self.state.accrued_salaries = 0

    def _process_bank_loan(self):
        if getattr(self.state, "bank_loan", None):
            payment = min(self.state.bank_loan.weekly_payment, self.state.bank_loan.amount_remaining)
            if self.state.money < payment:
                if not getattr(self.state, "pending_bankrupt", False):
                    self.state.pending_bankrupt = True
                    self.state.time_speed = 0
                    if hasattr(self.state, 'audio'):
                        self.state.audio.play_sound('warn')
                        self.state.audio.speak(self.state.get_text('loan_default_warning'), interrupt=True)
            else:
                self.state.track_expense("loan_repayment", payment)
                self.state.accounting["loan_paid"] += payment
                self.state.bank_loan.amount_remaining -= payment
                self.state.bank_loan.weeks_remaining -= 1
                if self.state.bank_loan.amount_remaining <= 0 or self.state.bank_loan.weeks_remaining <= 0:
                    self.state.bank_loan = None
                    from notifications import dispatcher, Event
                    dispatcher.dispatch(Event("loan_paid"))
                    if hasattr(self.state, 'audio'):
                        self.state.audio.play_sound('success')
                        self.state.audio.speak(self.state.get_text('subject_loan_paid'), interrupt=False)
