import pytest
from src.models.models import CardXref, Account, Customer

def test_card_and_account_management(client, db_session):
    # 1. 準備 (Customer -> Account -> Card)
    cust = Customer(cust_id=101, first_name="Ichiro", last_name="Suzuki")
    db_session.add(cust)
    acct1 = Account(acct_id=20001, cust_id=101, acct_balance=1000.0, acct_status="A")
    acct2 = Account(acct_id=20002, cust_id=101, acct_balance=0.0, acct_status="A")
    db_session.add_all([acct1, acct2])
    card = CardXref(card_num="9999888877776666", acct_id=20001)
    db_session.add(card)
    db_session.commit()

    # 2. カード一覧
    response = client.get("/cards/")
    assert response.status_code == 200
    assert any(c["card_num"] == "9999888877776666" for c in response.json())

    # 3. カード詳細
    response = client.get("/cards/9999888877776666")
    assert response.status_code == 200
    assert response.json()["acct_id"] == 20001

    # 4. カードの紐付け先アカウント変更
    response = client.put("/cards/9999888877776666", json={"acct_id": 20002})
    assert response.status_code == 200
    assert response.json()["acct_id"] == 20002

    # 5. アカウント情報更新
    response = client.put("/accounts/20001", json={"acct_balance": 1500.0, "acct_status": "I"})
    assert response.status_code == 200
    assert response.json()["acct_balance"] == 1500.0
    assert response.json()["acct_status"] == "I"
