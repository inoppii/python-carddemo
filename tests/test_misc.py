import pytest
from src.models.models import Account, Transaction

def test_menu_and_billing(client, db_session):
    # 1. Menu check
    resp = client.get("/menu/main")
    assert resp.status_code == 200
    assert len(resp.json()) > 0
    
    # 2. Billing check
    acct = Account(acct_id=30001, cust_id=1, acct_balance=500.0, acct_status="A")
    db_session.add(acct)
    db_session.commit()
    
    pay_data = {"acct_id": 30001, "amount": 100.0, "payment_desc": "Mobile Bill"}
    resp = client.post("/billing/pay", json=pay_data)
    assert resp.status_code == 200
    assert resp.json()["new_balance"] == 400.0
    
    # 3. Transaction record check
    resp = client.get("/transactions/?card_num=PAYMENT")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

def test_reports(client, db_session):
    resp = client.post("/reports/submit?report_type=EOD")
    assert resp.status_code == 200
    assert "EOD" in resp.json()["type"]
