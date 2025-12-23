import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.utils.db import get_db
from fastapi.testclient import TestClient
from main import app # main.py を後で作成する

import os

# テスト用 SQLite (ファイルベース)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_carddemo.db"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    # テストごとにテーブルをクリーンな状態にする
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    # テスト後にファイルを削除するのは session ごとは重いので、最後に行うかそのままにする

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            # ここで close してはいけない（db_session fixture が管理するため）
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
