import pytest
import os
from src.models.models import Account, Customer, TransactionType, CategoryBalance
from src.batch.p_CBACT01C import extract_accounts_to_csv, extract_accounts_to_jsonl
from src.batch.p_CBTRN02C import validate_and_update_transaction
from datetime import datetime

# ... (既存のテスト) ...

def test_validate_and_update_transaction_success(db_session):
    # マスターデータ
    tt = TransactionType(trn_type_cd="01", trn_type_desc="Purchase")
    db_session.add(tt)
    cust = Customer(cust_id=1, first_name="Taro", last_name="Yamada")
    db_session.add(cust)
    acct = Account(acct_id=10001, cust_id=1, acct_balance=1000.0, acct_status="A")
    db_session.add(acct)
    db_session.commit()

    # 取引データ
    trn_data = {
        "acct_id": 10001,
        "card_num": "1234",
        "trn_type_cd": "01",
        "trn_cat_cd": 1,
        "trn_amount": -100.0,
        "trn_desc": "Supermarket"
    }
    
    result = validate_and_update_transaction(trn_data, db=db_session)
    
    assert result["status"] == "Success"
    
    # DB 更新確認
    db_session.refresh(acct)
    assert float(acct.acct_balance) == 900.0
    
    cat_bal = db_session.query(CategoryBalance).filter_by(acct_id=10001, type_cd="01", cat_cd=1).first()
    assert float(cat_bal.balance) == -100.0

def test_extract_accounts_csv(db_session, tmp_path):
    # テストデータ作成
    test_customer = Customer(cust_id=1, first_name="Taro", last_name="Yamada", created_at=datetime.utcnow())
    test_account = Account(acct_id=10001, cust_id=1, acct_balance=100.0, acct_status="A", created_at=datetime.utcnow())
    db_session.add(test_customer)
    db_session.add(test_account)
    db_session.commit()

    # バッチ実行
    file_path = tmp_path / "test_extract.csv"
    count = extract_accounts_to_csv(str(file_path), db=db_session)

    assert count == 1
    assert os.path.exists(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "10001" in content
        assert "Yamada" in content

def test_extract_accounts_jsonl(db_session, tmp_path):
    # テストデータ作成 (前のテストのデータは Base.metadata.drop_all で消えているはず)
    test_customer = Customer(cust_id=2, first_name="Jiro", last_name="Sato", created_at=datetime.utcnow())
    test_account = Account(acct_id=10002, cust_id=2, acct_balance=200.0, acct_status="I", created_at=datetime.utcnow())
    db_session.add(test_customer)
    db_session.add(test_account)
    db_session.commit()

    # バッチ実行
    file_path = tmp_path / "test_extract.jsonl"
    count = extract_accounts_to_jsonl(str(file_path), db=db_session)

    assert count == 1
    # ただし今回は conftest.py で Base.metadata.drop_all/create_all しているので 2 になるはず（テストデータは累積される）
    # もし独立させたいなら各テストでクリーンアップが必要だが、ここでは簡易的に。
    
    assert os.path.exists(file_path)
