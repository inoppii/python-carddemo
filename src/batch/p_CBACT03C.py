from sqlalchemy.orm import Session
from src.models.models import Account
from src.utils.db import SessionLocal

def deduct_monthly_fees(fee_amount: float = 10.0, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
        
    try:
        # 残高不足でもマイナスを許容するかどうかは要件次第
        accounts = db.query(Account).filter(Account.acct_status == 'A').all()
        for acct in accounts:
            acct.acct_balance = float(acct.acct_balance) - fee_amount
        db.commit()
        return len(accounts)
    finally:
        if own_session:
            db.close()
