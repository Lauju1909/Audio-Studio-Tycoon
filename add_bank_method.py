code = '''
    def _send_monthly_bank_statement(self):
        """Sendet monatlichen Kontoauszug per E-Mail (alle 4 Wochen)."""
        if not hasattr(self, "financial_history") or not self.financial_history:
            return
        last_4 = self.financial_history[-4:] if len(self.financial_history) >= 4 else self.financial_history
        total_inc = sum(w["total_income"] for w in last_4)
        total_exp = sum(w["total_expenses"] for w in last_4)
        profit = total_inc - total_exp
        income_detail = {}
        expense_detail = {}
        for w in last_4:
            for cat, val in w["income"].items():
                income_detail[cat] = income_detail.get(cat, 0) + val
            for cat, val in w["expenses"].items():
                expense_detail[cat] = expense_detail.get(cat, 0) + val
        inc_lines = ["  + " + self.get_text("finance_" + c) + ": " + f"{v:,.0f}" + " EUR"
                     for c, v in income_detail.items() if v > 0]
        exp_lines = ["  - " + self.get_text("finance_" + c) + ": " + f"{v:,.0f}" + " EUR"
                     for c, v in expense_detail.items() if v > 0]
        cal = self.get_calendar_text()
        sign = "+" if profit >= 0 else ""
        body_lines = [
            self.get_text("monthly_statement_period") + ": " + cal,
            "",
            self.get_text("finance_total_income") + ": " + f"{total_inc:,.0f}" + " EUR",
        ] + inc_lines + [
            "",
            self.get_text("finance_total_expenses") + ": " + f"{total_exp:,.0f}" + " EUR",
        ] + exp_lines + [
            "",
            self.get_text("finance_net_profit") + ": " + sign + f"{profit:,.0f}" + " EUR",
            self.get_text("current_balance") + ": " + f"{self.money:,.0f}" + " EUR",
        ]
        from models import Email
        self.emails.insert(0, Email(
            sender=self.get_text("sender_bank"),
            subject=self.get_text("subject_monthly_statement", date=cal),
            body="\\n".join(body_lines),
            date_week=self.week
        ))

'''

with open("logic.py", "a", encoding="utf-8") as f:
    f.write(code)
print("Done.")
