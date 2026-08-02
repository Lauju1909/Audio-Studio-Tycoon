from logic import GameState
from models import BankLoan

def test_bank_loan_repayment():
    gs = GameState()
    gs.week = 5
    gs.money = 100000
    
    # 10k loan, 10% interest, 10 weeks -> total 11k -> 1100 per week
    gs.bank_loan = BankLoan(10000, 0.1, 10)
    
    # We tick the finance manager
    gs.finance_manager._process_bank_loan()
    
    # Assert money has been reduced by weekly_payment
    assert gs.money == 100000 - 1100
    assert gs.bank_loan.amount_remaining == 11000 - 1100
    assert gs.bank_loan.weeks_remaining == 9
