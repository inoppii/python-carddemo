from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.models import User
from ..utils.db import get_db
from ..auth.security import get_password_hash
from pydantic import BaseModel
from .p_COUSR00C import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.usr_id == user_in.usr_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        usr_id=user_in.usr_id,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=get_password_hash(user_in.password),
        usr_type=user_in.usr_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
