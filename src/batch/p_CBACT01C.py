import csv
import json
import os
from sqlalchemy.orm import Session
from src.models.models import Account, Customer
from src.utils.db import SessionLocal

def extract_accounts_to_csv(file_path: str, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    try:
        results = db.query(Account, Customer).\
            join(Customer, Account.cust_id == Customer.cust_id).all()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['acct_id', 'cust_id', 'first_name', 'last_name', 'acct_balance', 'acct_status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for account, customer in results:
                writer.writerow({
                    'acct_id': account.acct_id,
                    'cust_id': customer.cust_id,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'acct_balance': float(account.acct_balance),
                    'acct_status': account.acct_status
                })
        return len(results)
    finally:
        if own_session:
            db.close()

def extract_accounts_to_jsonl(file_path: str, db: Session = None):
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True
    try:
        results = db.query(Account, Customer).\
            join(Customer, Account.cust_id == Customer.cust_id).all()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for account, customer in results:
                data = {
                    'acct_id': account.acct_id,
                    'cust_id': customer.cust_id,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'acct_balance': float(account.acct_balance),
                    'acct_status': account.acct_status
                }
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        return len(results)
    finally:
        if own_session:
            db.close()

if __name__ == "__main__":
    # 実行例
    count = extract_accounts_to_csv("accounts_extract.csv")
    print(f"Extracted {count} records to CSV.")
