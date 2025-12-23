from sqlalchemy.orm import Session
from src.models.models import Transaction, Account, Customer
from src.utils.db import SessionLocal
from datetime import datetime

def generate_account_statement(acct_id: int, folder_path: str, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
        
    try:
        account, customer = db.query(Account, Customer).\
            join(Customer, Account.cust_id == Customer.cust_id).\
            filter(Account.acct_id == acct_id).first()
            
        transactions = db.query(Transaction).\
            filter(Transaction.card_num.in_(
                db.query(CardXref.card_num).filter(CardXref.acct_id == acct_id)
            )).all()
            
        file_path = f"{folder_path}/statement_{acct_id}.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Statement for Account: {acct_id}\n")
            f.write(f"Customer: {customer.first_name} {customer.last_name}\n")
            f.write(f"Current Balance: {account.acct_balance:.2f}\n")
            f.write("-" * 30 + "\n")
            for t in transactions:
                f.write(f"{t.trn_timestamp} | {t.trn_desc} | {t.trn_amount:.2f}\n")
        
        return len(transactions)
    except Exception as e:
        print(f"Error generating statement: {e}")
        return 0
    finally:
        if own_session:
            db.close()
