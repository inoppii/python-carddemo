from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.models import User
from ..utils.db import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.delete("/{usr_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(usr_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.usr_id == usr_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None
