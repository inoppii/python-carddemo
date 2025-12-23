from sqlalchemy.orm import Session
from src.models.models import Transaction, Account, Customer
from src.utils.db import SessionLocal

def generate_eod_report(file_path: str, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
        
    try:
        # 本日の取引サマリー等
        results = db.query(Transaction).all()
        total_amount = sum(float(t.trn_amount) for t in results)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"End of Day Report - {datetime.utcnow().date()}\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Transactions: {len(results)}\n")
            f.write(f"Total Amount: {total_amount:.2f}\n")
            
        return len(results)
    finally:
        if own_session:
            db.close()
