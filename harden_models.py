import re

def fix_models():
    f = 'models.py'
    c = open(f, encoding='utf-8').read()
    
    # 1. BankLoan
    old_loan = '''class BankLoan:
    """Aktiver Kredit bei der Bank."""
    def __init__(self, amount_borrowed, interest_rate, duration_weeks, amount_remaining=None, weeks_remaining=None):
        self.amount_borrowed = amount_borrowed
        # Feste Gesamtr\u00fcckzahlung: z.B. 100k + 20% = 120k
        total_repayment = int(amount_borrowed * (1.0 + interest_rate))
        self.amount_remaining = amount_remaining if amount_remaining is not None else total_repayment
        self.weeks_remaining = weeks_remaining if weeks_remaining is not None else duration_weeks
        # Guard: duration_weeks must be >= 1 to avoid ZeroDivisionError
        safe_weeks = max(1, duration_weeks)
        self.weekly_payment = int(total_repayment / safe_weeks)'''
        
    new_loan = '''class BankLoan:
    """Aktiver Kredit bei der Bank."""
    def __init__(self, amount_borrowed, interest_rate, duration_weeks, amount_remaining=None, weeks_remaining=None):
        self.amount_borrowed = max(0, amount_borrowed)
        safe_rate = max(0.0, interest_rate)
        total_repayment = int(self.amount_borrowed * (1.0 + safe_rate))
        self.amount_remaining = max(0, amount_remaining) if amount_remaining is not None else max(0, total_repayment)
        self.weeks_remaining = max(0, weeks_remaining) if weeks_remaining is not None else max(0, duration_weeks)
        safe_weeks = max(1, duration_weeks)
        self.weekly_payment = max(0, int(total_repayment / safe_weeks))'''
    
    c = c.replace(old_loan, new_loan)
    
    # 2. Employee Salary
    old_salary = '''    def _calculate_salary(self):
        """Monatliches Gehalt basierend auf Gesamtskills und Eigenschaft."""
        total_skill = sum(self.skills.values())
        base_salary = total_skill * 5 + 500
        if self.trait and self.trait["effect"] == "salary":
            base_salary *= self.trait["value"]
        if getattr(self, "personality", None) == "showman":
            base_salary *= 1.05
        return int(base_salary)'''
        
    new_salary = '''    def _calculate_salary(self):
        """Monatliches Gehalt basierend auf Gesamtskills und Eigenschaft."""
        total_skill = sum(self.skills.values())
        base_salary = max(500, int(total_skill * 5 + 500))
        if self.trait and self.trait["effect"] == "salary":
            base_salary *= self.trait["value"]
        if getattr(self, "personality", None) == "showman":
            base_salary *= 1.05
        return max(500, int(base_salary))'''
        
    c = c.replace(old_salary, new_salary)
    open(f, 'w', encoding='utf-8').write(c)
    
def fix_logic():
    f = 'logic.py'
    c = open(f, encoding='utf-8').read()
    
    # Tax fix 1
    c = re.sub(r'elif effect_type == "tax_increase":\s*self\.tax_rate \+= val', r'elif effect_type == "tax_increase":\n                self.tax_rate = max(0.0, min(0.99, self.tax_rate + val))', c)
    
    # Tax calculate fix
    old_tax = '''        if profit > 0:
            taxes = int(profit * self.tax_rate)
            self.track_expense("taxes", taxes)'''
            
    new_tax = '''        if profit > 0:
            taxes = max(0, int(profit * max(0.0, self.tax_rate)))
            self.track_expense("taxes", taxes)'''
    c = c.replace(old_tax, new_tax)
    
    open(f, 'w', encoding='utf-8').write(c)

fix_models()
fix_logic()
