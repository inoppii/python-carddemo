import pytest
from src.models.models import User
from src.auth.security import get_password_hash

def test_login_success(client, db_session):
    # テストユーザー作成
    hashed_pw = get_password_hash("testpassword")
    test_user = User(usr_id="TESTUSER", hashed_password=hashed_pw, usr_type="A")
    db_session.add(test_user)
    db_session.commit()

    # ログインリクエスト
    response = client.post(
        "/auth/login",
        data={"username": "TESTUSER", "password": "testpassword"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, db_session):
    hashed_pw = get_password_hash("testpassword")
    test_user = User(usr_id="TESTUSER", hashed_password=hashed_pw, usr_type="A")
    db_session.add(test_user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "TESTUSER", "password": "wrongpassword"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_user_not_found(client, db_session):
    response = client.post(
        "/auth/login",
        data={"username": "NONEXISTENT", "password": "anypassword"}
    )
    
    assert response.status_code == 401
