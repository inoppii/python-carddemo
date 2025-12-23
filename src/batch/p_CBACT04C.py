from sqlalchemy.orm import Session
from src.models.models import Account
from src.utils.db import SessionLocal

def update_account_status(db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    
    try:
        # 例：長期間アクティビティがないアカウントを Inactive にする
        # (ここでは簡略化のため、特定の条件で更新するロジックのみ)
        accounts = db.query(Account).all()
        for acct in accounts:
            if float(acct.acct_balance) < 0:
                acct.acct_status = 'O' # Overdrawn
        db.commit()
        return len(accounts)
    finally:
        if own_session:
            db.close()
