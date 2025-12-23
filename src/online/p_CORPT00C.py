from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.models import AuthSummary, AuthDetail
from ..utils.db import get_db
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/reports", tags=["reports"])

class SummaryResponse(BaseModel):
    acct_id: int
    total_auth_amount: float
    last_auth_timestamp: Optional[datetime]

@router.get("/auth-summary", response_model=List[SummaryResponse])
def get_auth_summaries(db: Session = Depends(get_db)):
    return db.query(AuthSummary).all()

@router.post("/submit")
def submit_report(report_type: str):
    # 本来はバッチキューに投入するロジック
    return {"status": "Report job submitted", "type": report_type}
