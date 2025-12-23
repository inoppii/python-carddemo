from sqlalchemy.orm import Session
from src.models.models import Transaction, Account, CategoryBalance, TransactionType
from src.utils.db import SessionLocal
from datetime import datetime

def validate_and_update_transaction(trn_data: dict, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    
    try:
        # 1. 取引種別の存在確認
        trn_type = db.query(TransactionType).filter(TransactionType.trn_type_cd == trn_data['trn_type_cd']).first()
        if not trn_type:
            return {"status": "Error", "message": "Invalid transaction type"}
        
        # 2. アカウントの存在・状態確認
        account = db.query(Account).filter(Account.acct_id == trn_data['acct_id']).first()
        if not account or account.acct_status != 'A':
            return {"status": "Error", "message": "Account invalid or inactive"}
        
        # 3. 取引登録 (Transactions テーブル)
        new_trn = Transaction(
            card_num=trn_data['card_num'],
            trn_type_cd=trn_data['trn_type_cd'],
            trn_cat_cd=trn_data['trn_cat_cd'],
            trn_amount=trn_data['trn_amount'],
            trn_desc=trn_data['trn_desc'],
            merchant_id=trn_data.get('merchant_id'),
            merchant_name=trn_data.get('merchant_name'),
            trn_timestamp=datetime.utcnow()
        )
        db.add(new_trn)
        
        # 4. カテゴリ別残高の更新 (CategoryBalances テーブル)
        cat_balance = db.query(CategoryBalance).filter(
            CategoryBalance.acct_id == account.acct_id,
            CategoryBalance.type_cd == trn_data['trn_type_cd'],
            CategoryBalance.cat_cd == trn_data['trn_cat_cd']
        ).first()
        
        if not cat_balance:
            cat_balance = CategoryBalance(
                acct_id=account.acct_id,
                type_cd=trn_data['trn_type_cd'],
                cat_cd=trn_data['trn_cat_cd'],
                balance=0.0
            )
            db.add(cat_balance)
        
        cat_balance.balance = float(cat_balance.balance) + trn_data['trn_amount']
        
        # 5. アカウント合計残高の更新
        account.acct_balance = float(account.acct_balance) + trn_data['trn_amount']
        
        db.commit()
        return {"status": "Success", "trn_id": new_trn.trn_id}
        
    except Exception as e:
        db.rollback()
        return {"status": "Exception", "message": str(e)}
    finally:
        if own_session:
            db.close()
