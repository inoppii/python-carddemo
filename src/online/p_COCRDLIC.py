from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import CardXref, Account, Customer
from ..utils.db import get_db
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/cards", tags=["cards"])

class CardListItem(BaseModel):
    card_num: str
    acct_id: int
    cust_id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[CardListItem])
def list_cards(db: Session = Depends(get_db)):
    results = db.query(CardXref, Account, Customer).\
        join(Account, CardXref.acct_id == Account.acct_id).\
        join(Customer, Account.cust_id == Customer.cust_id).all()
    
    return [
        {
            "card_num": card.card_num,
            "acct_id": acct.acct_id,
            "cust_id": cust.cust_id,
            "first_name": cust.first_name,
            "last_name": cust.last_name
        } for card, acct, cust in results
    ]

@router.get("/{card_num}", response_model=CardListItem)
def get_card(card_num: str, db: Session = Depends(get_db)):
    result = db.query(CardXref, Account, Customer).\
        join(Account, CardXref.acct_id == Account.acct_id).\
        join(Customer, Account.cust_id == Customer.cust_id).\
        filter(CardXref.card_num == card_num).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Card not found")
    
    card, acct, cust = result
    return {
        "card_num": card.card_num,
        "acct_id": acct.acct_id,
        "cust_id": cust.cust_id,
        "first_name": cust.first_name,
        "last_name": cust.last_name
    }
