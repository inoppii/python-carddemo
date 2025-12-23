from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.models import Account, Customer
from ..utils.db import get_db
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/accounts", tags=["accounts"])

class AccountViewResponse(BaseModel):
    acct_id: int
    cust_id: int
    first_name: str
    last_name: str
    acct_balance: float
    acct_status: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/{acct_id}", response_model=AccountViewResponse)
def get_account_details(acct_id: int, db: Session = Depends(get_db)):
    result = db.query(Account, Customer).\
        join(Customer, Account.cust_id == Customer.cust_id).\
        filter(Account.acct_id == acct_id).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    account, customer = result
    return {
        "acct_id": account.acct_id,
        "cust_id": customer.cust_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "acct_balance": float(account.acct_balance),
        "acct_status": account.acct_status,
        "created_at": account.created_at
    }
