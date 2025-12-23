from fastapi import FastAPI
from src.auth import p_COSGN00C
from src.online import p_COACTVWC, p_COPAUA0C, p_COUSR00C, p_COUSR01C, p_COUSR02C, p_COUSR03C, p_COCRDLIC, p_COCRDUPC, p_COACTUPC, p_COTRN00C, p_COTRN02C, p_COMEN01C, p_COBIL00C, p_CORPT00C, p_COTRTLIC, p_COPAUS1C, p_COBTUPDT
from src.models.base import Base
from src.utils.db import engine

# 開発時はここでテーブル作成（実運用は Alembic 等を推奨）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CardDemo API")

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
def read_root():
    return {"message": "Welcome to CardDemo API"}
