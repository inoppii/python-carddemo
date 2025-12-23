import pytest
from src.models.models import Transaction, CardXref, Account, Customer
from src.batch.p_CBTRN01C import validate_transactions

def test_transaction_full_flow(client, db_session):
    # 1. 準備
    cust = Customer(cust_id=1, first_name="Taro", last_name="Yamada")
    db_session.add(cust)
    acct = Account(acct_id=10001, cust_id=1, acct_balance=1000.0, acct_status="A")
    db_session.add(acct)
    card = CardXref(card_num="1111222233334444", acct_id=10001)
    db_session.add(card)
    db_session.commit()

    # 2. 取引登録
    trn_data = {
        "card_num": "1111222233334444",
        "trn_type_cd": "01",
        "trn_cat_cd": 1,
        "trn_amount": -200.0,
        "trn_desc": "Dinner"
    }
    response = client.post("/transactions/", json=trn_data)
    assert response.status_code == 201
    trn_id = response.json()["trn_id"]

    # 3. 残高反映確認
    db_session.refresh(acct)
    assert float(acct.acct_balance) == 800.0

    # 4. バッチ整合性検証 (正常系)
    errors = validate_transactions(db=db_session)
    assert len(errors) == 0

    # 5. 異常データ作成 (カードが存在しない取引)
    bad_trn = Transaction(card_num="9999", trn_type_cd="01", trn_cat_cd=1, trn_amount=0, trn_desc="Bad")
    db_session.add(bad_trn)
    db_session.commit()

    # 6. バッチ整合性検証 (異常系)
    errors = validate_transactions(db=db_session)
    assert any("invalid card 9999" in e for e in errors)
