import pytest
import os
from src.models.models import Customer, Account, Transaction, CardXref
from src.batch.p_CBEXPORT import export_table_to_csv
from src.batch.p_CBIMPORT import import_csv_to_table
from src.batch.p_CBPAUP0C import purge_old_data
from datetime import datetime, timedelta

def test_batch_maintenance_flow(db_session, tmp_path):
    # 1. Export Test
    cust = Customer(cust_id=1, first_name="Taro", last_name="Yamada")
    db_session.add(cust)
    db_session.commit()
    
    file_path = tmp_path / "export.csv"
    count = export_table_to_csv(Customer, str(file_path), db=db_session)
    assert count == 1
    assert os.path.exists(file_path)

    # 2. Import Test (Update)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # first_name を変更
    lines[1] = lines[1].replace("Taro", "Jiro")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    count = import_csv_to_table(Customer, str(file_path), db=db_session)
    assert count == 1
    db_session.refresh(cust)
    assert cust.first_name == "Jiro"

    # 3. Purge Test
    old_date = datetime.utcnow() - timedelta(days=400)
    old_trn = Transaction(card_num="1", trn_type_cd="01", trn_cat_cd=1, trn_amount=0, trn_desc="Old", trn_timestamp=old_date)
    new_trn = Transaction(card_num="1", trn_type_cd="01", trn_cat_cd=1, trn_amount=0, trn_desc="New", trn_timestamp=datetime.utcnow())
    db_session.add_all([old_trn, new_trn])
    db_session.commit()
    
    res = purge_old_data(days=365, db=db_session)
    assert res["deleted_transactions"] == 1
    assert db_session.query(Transaction).count() == 1
