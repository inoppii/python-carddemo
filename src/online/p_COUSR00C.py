from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.models import User
from ..utils.db import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])

class UserResponse(BaseModel):
    usr_id: str
    first_name: str
    last_name: str
    usr_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    usr_id: str
    first_name: str
    last_name: str
    password: str
    usr_type: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    usr_type: Optional[str] = None

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{usr_id}", response_model=UserResponse)
def get_user(usr_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.usr_id == usr_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
