from sqlalchemy.orm import Session
from src.models.models import Transaction, Account, CardXref
from src.utils.db import SessionLocal
from typing import List

def validate_transactions(db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    
    errors = []
    try:
        # 全取引を取得し、関連するカードやアカウントが存在するか検証
        transactions = db.query(Transaction).all()
        for trn in transactions:
            card = db.query(CardXref).filter(CardXref.card_num == trn.card_num).first()
            if not card:
                errors.append(f"Error: Transaction {trn.trn_id} has invalid card {trn.card_num}")
                continue
            
            account = db.query(Account).filter(Account.acct_id == card.acct_id).first()
            if not account:
                errors.append(f"Error: Card {trn.card_num} linked to missing account {card.acct_id}")
        
        return errors
    finally:
        if own_session:
            db.close()

if __name__ == "__main__":
    errs = validate_transactions()
    if not errs:
        print("All transactions validated successfully.")
    else:
        for e in errs:
            print(e)
