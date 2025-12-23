from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import TransactionType
from ..utils.db import get_db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/transaction-types", tags=["transaction-types"])

class TranTypeResponse(BaseModel):
    trn_type_cd: str
    trn_type_desc: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[TranTypeResponse])
def list_tran_types(db: Session = Depends(get_db)):
    return db.query(TransactionType).all()

@router.put("/{trn_type_cd}", response_model=TranTypeResponse)
def update_tran_type(trn_type_cd: str, trn_type_desc: str, db: Session = Depends(get_db)):
    tt = db.query(TransactionType).filter(TransactionType.trn_type_cd == trn_type_cd).first()
    if not tt:
        raise HTTPException(status_code=404, detail="Transaction Type not found")
    tt.trn_type_desc = trn_type_desc
    db.commit()
    return tt
