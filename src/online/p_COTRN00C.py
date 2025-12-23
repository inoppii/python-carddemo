from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import Transaction
from ..utils.db import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["transactions"])

class TransactionResponse(BaseModel):
    trn_id: int
    card_num: str
    trn_type_cd: str
    trn_cat_cd: int
    trn_amount: float
    trn_desc: str
    trn_timestamp: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[TransactionResponse])
def list_transactions(card_num: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if card_num:
        query = query.filter(Transaction.card_num == card_num)
    return query.all()

@router.get("/{trn_id}", response_model=TransactionResponse)
def get_transaction(trn_id: int, db: Session = Depends(get_db)):
    trn = db.query(Transaction).filter(Transaction.trn_id == trn_id).first()
    if not trn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return trn
