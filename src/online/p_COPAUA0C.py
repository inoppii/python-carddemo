from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.models import CardXref, Account, AuthDetail, AuthSummary
from ..utils.db import get_db
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(prefix="/auth-req", tags=["auth-request"])

class AuthRequest(BaseModel):
    card_num: str
    amount: float
    merchant_id: str
    merchant_name: str

class AuthResponse(BaseModel):
    auth_key: str
    response_cd: str
    status: str

@router.post("/process", response_model=AuthResponse)
def process_authorization(req: AuthRequest, db: Session = Depends(get_db)):
    # 1. カード存在チェック
    card = db.query(CardXref).filter(CardXref.card_num == req.card_num).first()
    if not card:
        return AuthResponse(auth_key="", response_cd="01", status="Declined: Invalid Card")
    
    # 2. アカウント残高チェック
    account = db.query(Account).filter(Account.acct_id == card.acct_id).first()
    if account.acct_balance < req.amount:
        return AuthResponse(auth_key="", response_cd="02", status="Declined: Insufficient Funds")
    
    # 3. 承認番号発行と履歴登録
    auth_key = str(uuid.uuid4())[:8].upper()
    new_auth = AuthDetail(
        auth_key=auth_key,
        acct_id=account.acct_id,
        card_num=req.card_num,
        auth_amount=req.amount,
        auth_response_cd="00",
        merchant_id=req.merchant_id,
        merchant_name=req.merchant_name,
        auth_timestamp=datetime.utcnow()
    )
    db.add(new_auth)
    
    # 4. 承認サマリー更新
    summary = db.query(AuthSummary).filter(AuthSummary.acct_id == account.acct_id).first()
    if not summary:
        summary = AuthSummary(acct_id=account.acct_id, total_auth_amount=0)
        db.add(summary)
    
    summary.total_auth_amount = float(summary.total_auth_amount) + req.amount
    summary.last_auth_timestamp = datetime.utcnow()
    
    # 5. 残高減算（ホールド処理）
    account.acct_balance = float(account.acct_balance) - req.amount
    
    db.commit()
    
    # 本来はここで Pub/Sub に通知を投げるが、ここではロジック完結
    return AuthResponse(auth_key=auth_key, response_cd="00", status="Approved")
