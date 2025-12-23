from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import User
from ..utils.db import get_db
from ..auth.security import get_password_hash
from pydantic import BaseModel
from typing import Optional
from .p_COUSR00C import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

class UserUpdateIn(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    usr_type: Optional[str] = None

@router.put("/{usr_id}", response_model=UserResponse)
def update_user(usr_id: str, user_in: UserUpdateIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.usr_id == usr_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_in.first_name: user.first_name = user_in.first_name
    if user_in.last_name: user.last_name = user_in.last_name
    if user_in.usr_type: user.usr_type = user_in.usr_type
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)
    
    db.commit()
    db.refresh(user)
    return user
