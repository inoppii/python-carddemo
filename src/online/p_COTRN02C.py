from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.models import Transaction, Account, CardXref
from ..utils.db import get_db
from pydantic import BaseModel
from datetime import datetime
from .p_COTRN00C import TransactionResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])

class TransactionCreate(BaseModel):
    card_num: str
    trn_type_cd: str
    trn_cat_cd: int
    trn_amount: float
    trn_desc: str

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def register_transaction(trn_in: TransactionCreate, db: Session = Depends(get_db)):
    # 簡易バリデーション (カード存在チェック)
    card = db.query(CardXref).filter(CardXref.card_num == trn_in.card_num).first()
    if not card:
        raise HTTPException(status_code=400, detail="Invalid card number")
    
    new_trn = Transaction(
        card_num=trn_in.card_num,
        trn_type_cd=trn_in.trn_type_cd,
        trn_cat_cd=trn_in.trn_cat_cd,
        trn_amount=trn_in.trn_amount,
        trn_desc=trn_in.trn_desc,
        trn_timestamp=datetime.utcnow()
    )
    db.add(new_trn)
    
    # 残高への即時反映 (本来はバッチか非同期だが、オンライン登録時は即時反映とする簡略化)
    account = db.query(Account).filter(Account.acct_id == card.acct_id).first()
    if account:
        account.acct_balance = float(account.acct_balance) + trn_in.trn_amount
    
    db.commit()
    db.refresh(new_trn)
    return new_trn
