from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.auth import p_COSGN00C
from src.online import p_COACTVWC, p_COPAUA0C, p_COUSR00C, p_COUSR01C, p_COUSR02C, p_COUSR03C, p_COCRDLIC, p_COCRDUPC, p_COACTUPC, p_COTRN00C, p_COTRN02C, p_COMEN01C, p_COBIL00C, p_CORPT00C, p_COTRTLIC, p_COPAUS1C, p_COBTUPDT
from src.models.base import Base
from src.utils.db import engine
import os

# 開発時はここでテーブル作成（実運用は Alembic 等を推奨）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CardDemo API")

# Static files setup
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="src/templates")

# Seeding on startup
from src.models.models import User
from src.utils.db import get_db, SessionLocal
from src.auth.security import get_password_hash

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Check and create USER0001
        user = db.query(User).filter(User.usr_id == "USER0001").first()
        if not user:
            print("Seeding USER0001...")
            new_user = User(
                usr_id="USER0001",
                first_name="Regular",
                last_name="User",
                hashed_password=get_password_hash("PASSWORD"),
                usr_type="R"
            )
            db.add(new_user)
        
        # Check and create ADMIN001
        admin = db.query(User).filter(User.usr_id == "ADMIN001").first()
        if not admin:
            print("Seeding ADMIN001...")
            new_admin = User(
                usr_id="ADMIN001",
                first_name="Admin",
                last_name="User",
                hashed_password=get_password_hash("PASSWORD"),
                usr_type="A"
            )
            db.add(new_admin)
            
        db.commit()
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

app.include_router(p_COSGN00C.router)
app.include_router(p_COACTVWC.router)
app.include_router(p_COPAUA0C.router)
app.include_router(p_COUSR00C.router)
app.include_router(p_COUSR01C.router)
app.include_router(p_COUSR02C.router)
app.include_router(p_COUSR03C.router)
app.include_router(p_COCRDLIC.router)
app.include_router(p_COCRDUPC.router)
app.include_router(p_COACTUPC.router)
app.include_router(p_COTRN00C.router)
app.include_router(p_COTRN02C.router)
app.include_router(p_COMEN01C.router)
app.include_router(p_COBIL00C.router)
app.include_router(p_CORPT00C.router)
app.include_router(p_COTRTLIC.router)
app.include_router(p_COPAUS1C.router)
app.include_router(p_COBTUPDT.router)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/dashboard")
def view_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")

@app.get("/admin")
def view_admin(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html")
