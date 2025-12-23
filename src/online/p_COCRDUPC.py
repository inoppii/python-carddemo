from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import CardXref
from ..utils.db import get_db
from pydantic import BaseModel
from .p_COCRDLIC import CardListItem

router = APIRouter(prefix="/cards", tags=["cards"])

class CardUpdateIn(BaseModel):
    acct_id: int

@router.put("/{card_num}", response_model=CardListItem)
def update_card(card_num: str, card_in: CardUpdateIn, db: Session = Depends(get_db)):
    card = db.query(CardXref).filter(CardXref.card_num == card_num).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # 実際にはカード番号変更不可、紐付け先アカウントの変更などを想定
    card.acct_id = card_in.acct_id
    db.commit()
    
    # 最新情報を取得して返却
    from .p_COCRDLIC import get_card
    return get_card(card_num, db)
