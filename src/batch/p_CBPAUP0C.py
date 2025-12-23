from sqlalchemy.orm import Session
from src.models.models import Transaction, AuthDetail
from src.utils.db import SessionLocal
from datetime import datetime, timedelta

def purge_old_data(days: int = 365, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    try:
        # 取引履歴の削除
        deleted_trns = db.query(Transaction).filter(Transaction.trn_timestamp < cutoff_date).delete()
        
        # 承認履歴の削除
        deleted_auths = db.query(AuthDetail).filter(AuthDetail.auth_timestamp < cutoff_date).delete()
        
        db.commit()
        return {"deleted_transactions": deleted_trns, "deleted_auths": deleted_auths}
    finally:
        if own_session:
            db.close()
