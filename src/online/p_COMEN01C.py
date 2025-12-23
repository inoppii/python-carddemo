from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/menu", tags=["menu"])

class MenuItem(BaseModel):
    id: str
    label: str
    path: str

@router.get("/main", response_model=List[MenuItem])
def get_main_menu():
    return [
        {"id": "1", "label": "Account View", "path": "/accounts/view"},
        {"id": "2", "label": "Card List", "path": "/cards/list"},
        {"id": "3", "label": "Transaction Register", "path": "/transactions/reg"},
        {"id": "4", "label": "Logon/Off", "path": "/auth/login"}
    ]

@router.get("/admin", response_model=List[MenuItem])
def get_admin_menu():
    return [
        {"id": "1", "label": "User Management", "path": "/users/mgmt"},
        {"id": "2", "label": "Report List", "path": "/reports/list"},
        {"id": "3", "label": "System Status", "path": "/system/status"}
    ]
