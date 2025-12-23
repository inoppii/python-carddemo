from sqlalchemy.orm import Session
from src.models.models import Account
from src.utils.db import SessionLocal

def calculate_interest(interest_rate: float = 0.01, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    
    try:
        accounts = db.query(Account).filter(Account.acct_status == 'A').all()
        for acct in accounts:
            interest = float(acct.acct_balance) * interest_rate
            acct.acct_balance = float(acct.acct_balance) + interest
        db.commit()
        return len(accounts)
    finally:
        if own_session:
            db.close()
