from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import Account, Transaction
from ..utils.db import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/billing", tags=["billing"])

class BillPaymentRequest(BaseModel):
    acct_id: int
    amount: float
    payment_desc: str

@router.post("/pay")
def process_bill_payment(req: BillPaymentRequest, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.acct_id == req.acct_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # 残高への反映 (支払いは減算)
    account.acct_balance = float(account.acct_balance) - req.amount
    
    # 取引履歴登録
    new_trn = Transaction(
        card_num="PAYMENT", # 特別な識別子
        trn_type_cd="PY",
        trn_cat_cd=9,
        trn_amount=-req.amount,
        trn_desc=req.payment_desc,
        trn_timestamp=datetime.utcnow()
    )
    db.add(new_trn)
    
    db.commit()
    return {"status": "Success", "new_balance": account.acct_balance}
