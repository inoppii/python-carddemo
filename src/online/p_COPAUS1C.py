from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import AuthDetail
from ..utils.db import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/reports", tags=["reports"])

class AuthDetailResponse(BaseModel):
    auth_key: str
    acct_id: int
    card_num: str
    auth_amount: float
    auth_response_cd: str
    auth_timestamp: datetime

    class Config:
        from_attributes = True

@router.get("/auth-detail/{auth_key}", response_model=AuthDetailResponse)
def get_auth_detail(auth_key: str, db: Session = Depends(get_db)):
    detail = db.query(AuthDetail).filter(AuthDetail.auth_key == auth_key).first()
    if not detail:
        raise HTTPException(status_code=404, detail="Auth detail not found")
    return detail

@router.get("/fraud-report")
def get_fraud_report(db: Session = Depends(get_db)):
    # 簡易な不正検知ロジック（例：1000以上の承認を抽出）
    results = db.query(AuthDetail).filter(AuthDetail.auth_amount > 1000).all()
    return results
