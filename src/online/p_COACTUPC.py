from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import Account
from ..utils.db import get_db
from pydantic import BaseModel
from typing import Optional
from .p_COACTVWC import AccountViewResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])

class AccountUpdateIn(BaseModel):
    acct_balance: Optional[float] = None
    acct_status: Optional[str] = None

@router.put("/{acct_id}", response_model=AccountViewResponse)
def update_account(acct_id: int, acct_in: AccountUpdateIn, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.acct_id == acct_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if acct_in.acct_balance is not None:
        account.acct_balance = acct_in.acct_balance
    if acct_in.acct_status:
        account.acct_status = acct_in.acct_status
    
    db.commit()
    
    from .p_COACTVWC import get_account_details
    return get_account_details(acct_id, db)
