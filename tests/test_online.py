import pytest
from src.models.models import Account, Customer, CardXref, AuthDetail, AuthSummary
from datetime import datetime

def test_get_account_success(client, db_session):
    # テストデータ作成
    test_customer = Customer(
        cust_id=1, first_name="Taro", last_name="Yamada", 
        city="Tokyo", created_at=datetime.utcnow()
    )
    db_session.add(test_customer)
    db_session.commit()

    test_account = Account(
        acct_id=10001, cust_id=1, acct_balance=500.50, 
        acct_status="A", created_at=datetime.utcnow()
    )
    db_session.add(test_account)
    db_session.commit()

    # リクエスト
    response = client.get("/accounts/10001")
    
    assert response.status_code == 200
    data = response.json()
    assert data["acct_id"] == 10001
    assert data["first_name"] == "Taro"
    assert data["acct_balance"] == 500.50

def test_get_account_not_found(client, db_session):
    response = client.get("/accounts/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"

def test_process_authorization_success(client, db_session):
    # テストデータ
    cust = Customer(cust_id=1, first_name="Taro", last_name="Yamada")
    db_session.add(cust)
    acct = Account(acct_id=10001, cust_id=1, acct_balance=1000.0, acct_status="A")
    db_session.add(acct)
    card = CardXref(card_num="1234567812345678", acct_id=10001)
    db_session.add(card)
    db_session.commit()

    # 承認リクエスト
    req_data = {
        "card_num": "1234567812345678",
        "amount": 100.0,
        "merchant_id": "M001",
        "merchant_name": "Test Merchant"
    }
    response = client.post("/auth-req/process", json=req_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["response_cd"] == "00"
    assert data["status"] == "Approved"
    assert "auth_key" in data

    # 残高が減っているか確認
    db_session.refresh(acct)
    assert float(acct.acct_balance) == 900.0

def test_process_authorization_insufficient_funds(client, db_session):
    cust = Customer(cust_id=1, first_name="Taro", last_name="Yamada")
    db_session.add(cust)
    acct = Account(acct_id=10001, cust_id=1, acct_balance=50.0, acct_status="A")
    db_session.add(acct)
    card = CardXref(card_num="1234567812345678", acct_id=10001)
    db_session.add(card)
    db_session.commit()

    req_data = {
        "card_num": "1234567812345678",
        "amount": 100.0,
        "merchant_id": "M001",
        "merchant_name": "Test Merchant"
    }
    response = client.post("/auth-req/process", json=req_data)
    
    assert response.status_code == 200 # 業務エラーなので 200 + response_cd
    data = response.json()
    assert data["response_cd"] == "02"
    assert "Insufficient Funds" in data["status"]
